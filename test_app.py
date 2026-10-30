"""Integration tests using real HTTP requests and an isolated temporary database."""
import unittest,subprocess,tempfile,os,time,json,urllib.request,urllib.error,http.cookiejar,sqlite3
from pathlib import Path
from datetime import datetime,timedelta
from contextlib import contextmanager
@contextmanager
def test_connection(path):
 c=sqlite3.connect(path)
 try:
  with c:yield c
 finally:c.close()
ROOT=Path(__file__).resolve().parent
class Integration(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.db=str(Path(cls.temp.name)/'test.db');env=dict(os.environ,CLEANING_DB=cls.db,CLEANING_PORT='8766')
  cls.process=subprocess.Popen([os.sys.executable,str(ROOT/'app.py')],env=env,stdout=subprocess.DEVNULL)
  for _ in range(100):
   try:urllib.request.urlopen('http://127.0.0.1:8766/api/services');break
   except OSError:time.sleep(.05)
  else:raise RuntimeError('Server not ready')
 @classmethod
 def tearDownClass(cls):cls.process.terminate();cls.process.wait();cls.temp.cleanup()
 def client(self,email):
  c=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));self.req(c,'login',{'email':email+'@example.test','password':'DemoPass123!'});return c
 def req(self,c,path,data=None):
  r=urllib.request.Request('http://127.0.0.1:8766/api/'+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
  try:
   with c.open(r) as res:return res.status,json.load(res)
  except urllib.error.HTTPError as e:
   with e:return e.code,json.load(e)
 def setUp(self):
  with test_connection(self.db) as c:c.execute('DELETE FROM Bookings')
  self.customer=self.client('customer');self.admin=self.client('admin');self.other=self.client('other');self.cleaner=self.client('cleaner')
  self.slot=(datetime.now()+timedelta(days=2)).replace(hour=10,minute=0,second=0,microsecond=0).isoformat()
  self.data={'service_id':1,'start_at':self.slot,'service_address':'10 Fictional Demo Road','quoted_price_pence':1,'customer_id':4}
 def booking(self):
  code,b=self.req(self.customer,'bookings',self.data);self.assertEqual(code,201);return b
 def test_valid_booking_persisted_and_server_price(self):
  b=self.booking();self.assertEqual(b['quoted_price_pence'],4500);self.assertEqual(b['customer_id'],1)
  with test_connection(self.db) as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM Bookings').fetchone()[0],1)
  self.assertEqual(self.req(self.admin,'bookings')[1][0]['booking_id'],b['booking_id'])
 def test_past_date_rejected(self):self.assertEqual(self.req(self.customer,'bookings',dict(self.data,start_at='2020-01-01T10:00'))[0],400)
 def test_missing_address_rejected(self):self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_address=''))[0],400)
 def test_unknown_service_rejected(self):self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_id=999))[0],400)
 def test_unauthenticated_request_rejected(self):self.assertEqual(self.req(urllib.request.build_opener(),'bookings',self.data)[0],401)
 def test_role_and_ownership_restrictions(self):
  b=self.booking();self.assertEqual(self.req(self.customer,'admin/schema')[0],403);self.assertEqual(self.req(self.other,'bookings')[1],[]);self.assertEqual(self.req(self.other,f"bookings/{b['booking_id']}/cancel",{})[0],403)
 def test_overlapping_capacity_rejected(self):self.booking();self.assertEqual(self.req(self.other,'bookings',self.data)[0],409)
 def test_cancel_releases_capacity(self):
  b=self.booking();self.assertEqual(self.req(self.customer,f"bookings/{b['booking_id']}/cancel",{})[0],200);self.assertEqual(self.req(self.other,'bookings',self.data)[0],201)
 def test_assignment_and_status_workflow(self):
  b=self.booking();p=f"bookings/{b['booking_id']}";self.assertEqual(self.req(self.admin,p+'/assign',{'cleaner_id':3})[0],200)
  self.assertEqual(self.req(self.cleaner,p+'/status',{'status':'completed'})[0],409)
  self.assertEqual(self.req(self.cleaner,p+'/status',{'status':'in_progress'})[0],200);self.assertEqual(self.req(self.cleaner,p+'/status',{'status':'completed'})[0],200)
 def test_sql_injection_is_data(self):
  b=self.req(self.customer,'bookings',dict(self.data,service_address="10 Demo Road'; DROP TABLE Users; --"));self.assertEqual(b[0],201)
  with test_connection(self.db) as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM Users').fetchone()[0],4)
 def test_assignment_conflict_and_wrong_role(self):
  b=self.booking();self.assertEqual(self.req(self.admin,f"bookings/{b['booking_id']}/assign",{'cleaner_id':1})[0],400)
 def test_concurrent_requests_only_one_succeeds(self):
  from concurrent.futures import ThreadPoolExecutor
  with ThreadPoolExecutor(2) as pool:results=list(pool.map(lambda c:self.req(c,'bookings',self.data)[0],[self.customer,self.other]))
  self.assertEqual(sorted(results),[201,409])
if __name__=='__main__':unittest.main(verbosity=2)
