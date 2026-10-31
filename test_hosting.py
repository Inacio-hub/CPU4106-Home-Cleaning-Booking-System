"""New hosted-adapter checks, separate from historical Windows evidence."""
import os
import subprocess
import tempfile
import time
import unittest
import urllib.request
import urllib.error
from pathlib import Path
from unittest.mock import patch
import deploy
from test_audit import AuditTests

class HostedRegression(AuditTests):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.db = str(Path(cls.temp.name) / 'hosted-test.db')
        env = dict(os.environ, CLEANING_DB=cls.db, PORT='8766', CLEANING_HOST='127.0.0.1', CLEANING_PUBLIC_ORIGIN='')
        env.pop('RENDER_EXTERNAL_URL', None)
        cls.process = subprocess.Popen([os.sys.executable, str(Path(__file__).parent/'deploy.py')], env=env, stdout=subprocess.DEVNULL)
        for _ in range(100):
            try:
                urllib.request.urlopen('http://127.0.0.1:8766/healthz').close()
                break
            except OSError:
                time.sleep(.05)
        else:
            cls.process.terminate(); cls.process.wait(); cls.temp.cleanup()
            raise RuntimeError('Hosted launcher not ready')

    def test_host_health(self):
        with urllib.request.urlopen('http://127.0.0.1:8766/healthz') as r:
            self.assertEqual(r.status, 200)
            self.assertIn(b'coursework-demo', r.read())

    def test_host_visible_demo_notice(self):
        with urllib.request.urlopen('http://127.0.0.1:8766/') as r:
            body = r.read()
            self.assertIn(b'Shared coursework demonstration', body)
            self.assertIn(b'may reset', body)
            self.assertEqual(r.headers['X-Robots-Tag'], 'noindex, nofollow')

    def test_host_robots(self):
        with urllib.request.urlopen('http://127.0.0.1:8766/robots.txt') as r:
            self.assertIn(b'Disallow: /', r.read())

    def test_host_rejects_cross_origin(self):
        req = urllib.request.Request('http://127.0.0.1:8766/api/login', data=b'{}', headers={'Origin':'https://foreign.example', 'Content-Type':'application/json'})
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(req)
        self.assertEqual(error.exception.code, 403)
        error.exception.close()

    def test_host_https_origin_uses_configured_url(self):
        handler = deploy.HostedHandler.__new__(deploy.HostedHandler)
        handler.headers = {'Origin':'https://demo.example', 'Host':'internal-proxy'}
        with patch.object(deploy, 'PUBLIC_ORIGIN', 'https://demo.example'):
            handler.csrf()
            handler.headers['Origin'] = 'https://foreign.example'
            with self.assertRaises(deploy.app.Error): handler.csrf()

    def test_host_https_cookie_is_secure(self):
        handler = deploy.HostedHandler.__new__(deploy.HostedHandler)
        with patch.object(deploy, 'PUBLIC_ORIGIN', 'https://demo.example'), patch.object(deploy.app.Handler, 'send_json') as send:
            handler.send_json(200, {'ok':True}, {'Set-Cookie':'session=example; HttpOnly; SameSite=Strict'})
            self.assertIn('; Secure', send.call_args.args[2]['Set-Cookie'])

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(HostedRegression))
    raise SystemExit(not result.wasSuccessful())
