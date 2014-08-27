import flask
import flask_kerberos
import kerberos
import mock
import unittest


class BasicAppTestCase(unittest.TestCase):
    def setUp(self):
        app = flask.Flask(__name__)
        app.config['TESTING'] = True

        @app.route('/')
        @flask_kerberos.requires_authentication
        def index(user):
            return user

        self.app = app

    def test_unauthorized(self):
        '''
        Ensure that when the client does not send an authorization token, they
        receive a 401 Unauthorized response which includes a www-authenticate
        header field which indicates the server supports Negotiate
        authentication.
        '''
        flask_kerberos.init_kerberos(self.app, 'HTTP', 'example.org')
        c = self.app.test_client()
        r = c.get('/')
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.headers.get('www-authenticate'), 'Negotiate')

    @mock.patch('kerberos.authGSSServerInit')
    @mock.patch('kerberos.authGSSServerStep')
    @mock.patch('kerberos.authGSSServerResponse')
    @mock.patch('kerberos.authGSSServerUserName')
    @mock.patch('kerberos.authGSSServerClean')
    def test_authorized(self, clean, name, response, step, init):
        '''
        Ensure that when the client sends an correct authorization token,
        they receive a 200 OK response and the user principal is extracted and
        passed on to the routed method.
        '''
        state = object()
        init.return_value = (kerberos.AUTH_GSS_COMPLETE, state)
        step.return_value = kerberos.AUTH_GSS_COMPLETE
        name.return_value = "user@EXAMPLE.ORG"
        response.return_value = "STOKEN"
        flask_kerberos.init_kerberos(self.app, 'HTTP', 'example.org')
        c = self.app.test_client()
        r = c.get('/', headers={'Authorization': 'Negotiate CTOKEN'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, 'user@EXAMPLE.ORG')
        self.assertEqual(r.headers.get('WWW-Authenticate'), 'negotiate STOKEN')
        self.assertEqual(init.mock_calls, [mock.call('HTTP@example.org')])
        self.assertEqual(step.mock_calls, [mock.call(state, 'CTOKEN')])
        self.assertEqual(name.mock_calls, [mock.call(state)])
        self.assertEqual(response.mock_calls, [mock.call(state)])
        self.assertEqual(clean.mock_calls, [mock.call(state)])

    @mock.patch('kerberos.authGSSServerInit')
    @mock.patch('kerberos.authGSSServerStep')
    @mock.patch('kerberos.authGSSServerResponse')
    @mock.patch('kerberos.authGSSServerUserName')
    @mock.patch('kerberos.authGSSServerClean')
    def test_authorized_no_mutual_auth(self, clean, name, response, step, init):
        '''
        Ensure that when a client does not request mutual authentication, we
        don't provide a token & that we don't throw an exception.
        '''
        state = object()
        init.return_value = (kerberos.AUTH_GSS_COMPLETE, state)
        step.return_value = kerberos.AUTH_GSS_COMPLETE
        name.return_value = "user@EXAMPLE.ORG"
        response.return_value = None
        flask_kerberos.init_kerberos(self.app, 'HTTP', 'example.org')
        c = self.app.test_client()
        r = c.get('/', headers={'Authorization': 'Negotiate CTOKEN'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, 'user@EXAMPLE.ORG')
        self.assertEqual(r.headers.get('WWW-Authenticate'), None)
        self.assertEqual(init.mock_calls, [mock.call('HTTP@example.org')])
        self.assertEqual(step.mock_calls, [mock.call(state, 'CTOKEN')])
        self.assertEqual(name.mock_calls, [mock.call(state)])
        self.assertEqual(response.mock_calls, [mock.call(state)])
        self.assertEqual(clean.mock_calls, [mock.call(state)])

    @mock.patch('kerberos.authGSSServerInit')
    @mock.patch('kerberos.authGSSServerStep')
    @mock.patch('kerberos.authGSSServerResponse')
    @mock.patch('kerberos.authGSSServerUserName')
    @mock.patch('kerberos.authGSSServerClean')
    def test_forbidden(self, clean, name, response, step, init):
        '''
        Ensure that when the client sends an incorrect authorization token,
        they receive a 403 Forbidden response.
        '''
        state = object()
        init.return_value = (kerberos.AUTH_GSS_COMPLETE, state)
        step.side_effect = kerberos.GSSError("FAILURE")
        flask_kerberos.init_kerberos(self.app, 'HTTP', 'example.org')
        c = self.app.test_client()
        r = c.get('/', headers={'Authorization': 'Negotiate CTOKEN'})
        self.assertEqual(r.status_code, 403)
        self.assertEqual(init.mock_calls, [mock.call('HTTP@example.org')])
        self.assertEqual(step.mock_calls, [mock.call(state, 'CTOKEN')])
        self.assertEqual(name.mock_calls, [])
        self.assertEqual(response.mock_calls, [])
        self.assertEqual(clean.mock_calls, [mock.call(state)])


if __name__ == '__main__':
    unittest.main()
