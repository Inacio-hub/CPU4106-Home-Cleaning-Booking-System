"""Week 4 boundary tests plus inherited Week 2 integration regression tests."""
from test_app import Integration
import urllib.request, urllib.error, json

class Week4Tests(Integration):
    def test_address_7_rejected(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_address='1234567'))[0],400)
    def test_address_8_accepted(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_address='12345678'))[0],201)
    def test_address_250_accepted(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_address='x'*250))[0],201)
    def test_address_251_rejected(self):
        self.assertEqual(self.req(self.customer,'bookings',dict(self.data,service_address='x'*251))[0],400)
    def test_array_payload_rejected(self):
        self.assertEqual(self.req(self.customer,'bookings',[])[0],400)
    def test_malformed_json_rejected(self):
        r=urllib.request.Request('http://127.0.0.1:8766/api/bookings',data=b'{',headers={'Content-Type':'application/json'})
        try:
            self.customer.open(r);self.fail('Malformed JSON should fail')
        except urllib.error.HTTPError as e:
            with e:
                self.assertEqual(e.code,400);self.assertEqual(json.load(e)['error'],'Invalid JSON request')

if __name__=='__main__':
    import unittest
    unittest.main(defaultTest='Week4Tests',verbosity=2)
