"""Regression probes for reproducible faults found in the 26 October review."""
import http.client, socket, unittest
from test_week4 import Week4Tests

class AuditTests(Week4Tests):
    def test_cleaner_cannot_view_pending_request(self):
        self.booking()
        self.assertEqual(self.req(self.cleaner,'bookings')[1],[])
    def test_cleaner_cannot_view_cancelled_request(self):
        b=self.booking();self.req(self.customer,f"bookings/{b['booking_id']}/cancel",{})
        self.assertEqual(self.req(self.cleaner,'bookings')[1],[])
    def test_array_address_rejected(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_address=['10 Demo Road']))[0],400)
    def test_numeric_address_rejected(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_address=12345678))[0],400)
    def test_fractional_service_id_rejected(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_id=1.9))[0],400)
    def test_boolean_service_id_rejected(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_id=True))[0],400)
    def test_extra_action_path_rejected(self):
        b=self.booking()
        self.assertEqual(self.req(self.admin,f"bookings/{b['booking_id']}/assign/extra",{'cleaner_id':3})[0],404)
    def test_fractional_cleaner_id_rejected(self):
        b=self.booking()
        self.assertEqual(self.req(self.admin,f"bookings/{b['booking_id']}/assign",{'cleaner_id':3.9})[0],400)
    def test_negative_content_length_rejected_without_wait(self):
        conn=http.client.HTTPConnection('127.0.0.1',8766,timeout=1)
        try:
            conn.putrequest('POST','/api/login');conn.putheader('Content-Length','-1');conn.endheaders()
            try:r=conn.getresponse()
            except socket.timeout:self.fail('Server waited for a body with negative Content-Length')
            self.assertEqual(r.status,400);r.read()
        finally:conn.close()

if __name__=='__main__':unittest.main(defaultTest='AuditTests',verbosity=2)
