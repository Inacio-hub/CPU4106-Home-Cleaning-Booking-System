"""Hosted frontend regression with an isolated database and ephemeral port."""
import tempfile,threading,unittest,urllib.request,json
from pathlib import Path
from http.server import ThreadingHTTPServer
class HostedFrontendTests(unittest.TestCase):
 def test_hosted_frontend_and_database_routes(self):
  with tempfile.TemporaryDirectory() as d:
   import app,deploy
   original_db=app.DB;app.DB=Path(d)/'test.sqlite3'
   try:
    app.init();server=ThreadingHTTPServer(('127.0.0.1',0),deploy.HostedHandler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base='http://127.0.0.1:'+str(server.server_port)
    try:
     with urllib.request.urlopen(base+'/') as r:html=r.read().decode();self.assertEqual(r.status,200)
     self.assertIn('fetch(',html);self.assertNotIn('localStorage',html)
     self.assertIn('Shared coursework demonstration',html)
     with urllib.request.urlopen(base+'/api/services') as r:self.assertEqual(len(json.load(r)),3)
     with urllib.request.urlopen(base+'/healthz') as r:self.assertEqual(json.load(r)['status'],'ok')
     with app.connection() as c:self.assertEqual(c.execute('SELECT count(*) FROM Bookings').fetchone()[0],0)
    finally:server.shutdown();server.server_close();thread.join()
   finally:app.DB=original_db
if __name__=='__main__':unittest.main()
