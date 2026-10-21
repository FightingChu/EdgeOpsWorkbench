import unittest
from edgeops.domain.alerting.routing import destinations

class RoutingTests(unittest.TestCase):
    def test_matching_routes_deduplicate_destinations(self):
        rule={'destination':'ops','when':{'field':'severity','op':'severity','value':'warning'}}
        self.assertEqual(destinations({'severity':'error'},[rule,rule]),['ops'])
        self.assertEqual(destinations({'severity':'debug'},[rule]),[])
    def test_blank_destination_rejected(self):
        with self.assertRaises(ValueError): destinations({},[{'destination':''}])
