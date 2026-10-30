"""Local coursework prototype. Python 3.10+; no external packages."""
import os,json,sqlite3,secrets,hashlib,hmac,threading
from pathlib import Path
from datetime import datetime,timedelta
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlparse
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parent
DB=Path(os.environ.get('CLEANING_DB',str(ROOT/'cleaning.db')))
SESSIONS={};LOCK=threading.Lock()
@contextmanager
def connection():
 c=sqlite3.connect(DB,timeout=10);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON')
 try:
  with c:yield c
 finally:c.close()
def password_hash(p,salt=None):
 salt=salt or secrets.token_hex(16);return salt+':'+hashlib.pbkdf2_hmac('sha256',p.encode(),salt.encode(),200000).hex()
def password_ok(p,value):return hmac.compare_digest(password_hash(p,value.split(':')[0]),value)
def init():
 with connection() as c:
  c.executescript((ROOT/'schema.sql').read_text())
  for name,email,role in [('Demo Customer','customer@example.test','customer'),('Demo Administrator','admin@example.test','admin'),('Demo Cleaner','cleaner@example.test','cleaner'),('Other Customer','other@example.test','customer')]:
   c.execute('INSERT OR IGNORE INTO Users(name,email,password_hash,role) VALUES(?,?,?,?)',(name,email,password_hash('DemoPass123!'),role))
  for n,price,dur in [('Standard clean',4500,120),('Deep clean',9000,240),('End of tenancy',15000,360)]:
   if not c.execute('SELECT 1 FROM Services WHERE name=?',(n,)).fetchone():c.execute('INSERT INTO Services(name,price_pence,duration_minutes) VALUES(?,?,?)',(n,price,dur))
  cleaner=c.execute("SELECT user_id FROM Users WHERE role='cleaner'").fetchone()[0]
  for day in range(1,31):
   start=(datetime.now()+timedelta(days=day)).replace(hour=8,minute=0,second=0,microsecond=0)
   if not c.execute('SELECT 1 FROM CleanerAvailability WHERE cleaner_id=? AND start_at=?',(cleaner,start.isoformat())).fetchone():c.execute('INSERT INTO CleanerAvailability(cleaner_id,start_at,end_at) VALUES(?,?,?)',(cleaner,start.isoformat(),start.replace(hour=18).isoformat()))
class Error(Exception):
 def __init__(self,status,message):self.status=status;self.message=message
def positive_id(value,label):
 # JSON booleans and fractional values must never become another record ID.
 if type(value) is not int or value<1:raise Error(400,'Choose a positive whole-number '+label+' ID')
 return value
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def send_json(self,status,obj,extra=None):
  b=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store')
  for k,v in (extra or {}).items():self.send_header(k,v)
  self.end_headers();self.wfile.write(b)
 def data(self):
  try:
   length=int(self.headers.get('Content-Length','0'))
   # Reject invalid framing before reading; read(-1) would wait for EOF.
   if length<0:raise Error(400,'Content-Length cannot be negative')
   if length>20000:raise Error(413,'Request too large')
   val=json.loads(self.rfile.read(length))
   if not isinstance(val,dict):raise ValueError()
   return val
  except (ValueError,TypeError):raise Error(400,'Invalid JSON request')
 def user(self,roles=None):
  ck=SimpleCookie();ck.load(self.headers.get('Cookie',''));token=ck.get('session');record=SESSIONS.get(token.value if token else '')
  if not record or record['expires']<datetime.now():raise Error(401,'Sign in required')
  u=record['user']
  if roles and u['role'] not in roles:raise Error(403,'Access denied for this role')
  return u
 def csrf(self):
  origin=self.headers.get('Origin')
  if origin and origin!=('http://'+self.headers.get('Host','')):raise Error(403,'Origin rejected')
 def do_GET(self):
  try:
   path=urlparse(self.path).path
   if path=='/':
    b=(ROOT/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'");self.end_headers();self.wfile.write(b);return
   if path=='/api/services':
    with connection() as c:return self.send_json(200,[dict(r) for r in c.execute('SELECT * FROM Services')])
   if path=='/api/me':return self.send_json(200,self.user())
   if path=='/api/bookings':
    u=self.user()
    with connection() as c:
     sql='SELECT b.*,s.name AS service_name,u.name AS customer_name FROM Bookings b JOIN Services s USING(service_id) JOIN Users u ON b.customer_id=u.user_id';args=[]
     if u['role']=='customer':sql+=' WHERE b.customer_id=?';args=[u['user_id']]
     if u['role']=='cleaner':sql+=" WHERE b.cleaner_id=? AND b.status IN ('assigned','in_progress','completed')";args=[u['user_id']]
     return self.send_json(200,[dict(r) for r in c.execute(sql+' ORDER BY booking_id DESC',args)])
   if path=='/api/admin/schema':
    self.user(['admin'])
    with connection() as c:return self.send_json(200,[dict(r) for r in c.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name")])
   raise Error(404,'Not found')
  except Error as e:self.send_json(e.status,{'error':e.message})
 def do_POST(self):
  try:
   self.csrf();path=urlparse(self.path).path;data=self.data()
   if path=='/api/login':
    with connection() as c:r=c.execute('SELECT * FROM Users WHERE email=?',(str(data.get('email','')).lower(),)).fetchone()
    if not r or not password_ok(str(data.get('password','')),r['password_hash']):raise Error(401,'Invalid email or password')
    u={k:r[k] for k in ['user_id','name','email','role']};token=secrets.token_urlsafe(32);SESSIONS[token]={'user':u,'expires':datetime.now()+timedelta(hours=2)}
    return self.send_json(200,u,{'Set-Cookie':'session='+token+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=7200'})
   if path=='/api/logout':
    ck=SimpleCookie();ck.load(self.headers.get('Cookie',''))
    if ck.get('session'):SESSIONS.pop(ck['session'].value,None)
    return self.send_json(200,{'ok':True},{'Set-Cookie':'session=; Max-Age=0; Path=/'})
   if path=='/api/bookings':
    u=self.user(['customer']);address=data.get('service_address','')
    if not isinstance(address,str):raise Error(400,'Service address must be text')
    address=address.strip()
    if len(address)<8 or len(address)>250:raise Error(400,'Enter a service address of 8–250 characters')
    try:start=datetime.fromisoformat(str(data.get('start_at','')));sid=positive_id(data.get('service_id'),'service')
    except (ValueError,TypeError):raise Error(400,'Select a valid service and date')
    if start.tzinfo is not None:raise Error(400,'Use local business time without timezone suffix')
    if start<=datetime.now():raise Error(400,'Booking date must be in the future')
    if start>datetime.now()+timedelta(days=30):raise Error(400,'Book within the next 30 days')
    if start.minute!=0 or start.second!=0 or start.microsecond!=0:raise Error(400,'Bookings start on the hour')
    with connection() as c:
     service=c.execute('SELECT * FROM Services WHERE service_id=?',(sid,)).fetchone()
     if not service:raise Error(400,'Unknown service')
     end=start+timedelta(minutes=service['duration_minutes'])
     if start.hour<8 or end.date()!=start.date() or end.hour>18 or (end.hour==18 and end.minute):raise Error(400,'Choose a slot entirely between 08:00 and 18:00')
     # Capacity reservation includes requested and assigned jobs. One cleaner in this demo.
     c.execute('BEGIN IMMEDIATE')
     available=c.execute("SELECT a.cleaner_id FROM CleanerAvailability a WHERE a.start_at<=? AND a.end_at>=? AND NOT EXISTS(SELECT 1 FROM Bookings b WHERE b.cleaner_id=a.cleaner_id AND b.status!='cancelled' AND b.start_at<? AND b.end_at>?) LIMIT 1",(start.isoformat(),end.isoformat(),end.isoformat(),start.isoformat())).fetchone()
     if not available:raise Error(409,'No cleaner available for this slot')
     cur=c.execute('INSERT INTO Bookings(customer_id,cleaner_id,service_id,start_at,end_at,service_address,quoted_price_pence) VALUES(?,?,?,?,?,?,?)',(u['user_id'],available[0],sid,start.isoformat(),end.isoformat(),address,service['price_pence']))
     result=dict(c.execute('SELECT * FROM Bookings WHERE booking_id=?',(cur.lastrowid,)).fetchone())
    return self.send_json(201,result)
   if path.startswith('/api/bookings/'):
    parts=path.strip('/').split('/')
    if len(parts)!=4 or not parts[2].isascii() or not parts[2].isdecimal() or int(parts[2])<1:raise Error(404,'Unknown booking action route')
    bid=int(parts[2]);action=parts[3];u=self.user()
    with connection() as c:
     c.execute('BEGIN IMMEDIATE');b=c.execute('SELECT * FROM Bookings WHERE booking_id=?',(bid,)).fetchone()
     if not b:raise Error(404,'Booking not found')
     if action=='cancel':
      if u['role']!='admin' and not(u['role']=='customer' and b['customer_id']==u['user_id']):raise Error(403,'You cannot cancel this booking')
      if b['status'] not in ('requested','assigned') or datetime.fromisoformat(b['start_at'])<=datetime.now():raise Error(409,'Booking can no longer be cancelled')
      c.execute("UPDATE Bookings SET status='cancelled' WHERE booking_id=?",(bid,))
     elif action=='assign':
      if u['role']!='admin':raise Error(403,'Administrator access required')
      if b['status']!='requested':raise Error(409,'Only requested bookings can be assigned')
      cid=positive_id(data.get('cleaner_id'),'cleaner')
      if not c.execute("SELECT 1 FROM Users WHERE user_id=? AND role='cleaner'",(cid,)).fetchone():raise Error(400,'Choose a valid cleaner')
      if not c.execute('SELECT 1 FROM CleanerAvailability WHERE cleaner_id=? AND start_at<=? AND end_at>=?',(cid,b['start_at'],b['end_at'])).fetchone():raise Error(409,'Cleaner is outside working availability')
      if c.execute("SELECT 1 FROM Bookings WHERE cleaner_id=? AND booking_id!=? AND status!='cancelled' AND start_at<? AND end_at>?",(cid,bid,b['end_at'],b['start_at'])).fetchone():raise Error(409,'Cleaner already has an overlapping job')
      c.execute("UPDATE Bookings SET status='assigned',cleaner_id=? WHERE booking_id=?",(cid,bid))
     elif action=='status':
      if not(u['role']=='admin' or u['role']=='cleaner' and b['cleaner_id']==u['user_id']):raise Error(403,'Assigned cleaner or administrator required')
      target=data.get('status');allowed={'assigned':'in_progress','in_progress':'completed'}
      if allowed.get(b['status'])!=target:raise Error(409,'Invalid job status transition')
      c.execute('UPDATE Bookings SET status=? WHERE booking_id=?',(target,bid))
     else:raise Error(404,'Unknown booking action')
     result=dict(c.execute('SELECT * FROM Bookings WHERE booking_id=?',(bid,)).fetchone())
    return self.send_json(200,result)
   raise Error(404,'Not found')
  except Error as e:self.send_json(e.status,{'error':e.message})
  except (ValueError,IndexError,TypeError):self.send_json(400,{'error':'Invalid request values'})
  except sqlite3.Error:self.send_json(500,{'error':'Database operation failed'})
if __name__=='__main__':
 init();port=int(os.environ.get('CLEANING_PORT','8765'));print(f'Cleaning prototype: http://127.0.0.1:{port}',flush=True);ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
