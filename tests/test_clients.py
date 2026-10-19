import unittest

from edgeops.clients import ClientState, apply_event_page
from edgeops.clients.accessibility import inspect_html
from edgeops.clients.desktop import summary_rows
from edgeops.clients.profiles import get_profile


class ClientTests(unittest.TestCase):
    def test_stale_snapshot_is_rejected_and_offline_state_is_marked(self):
        state = ClientState(snapshot_id=10)
        apply_event_page(state, {"snapshot_id": 9, "events": []})
        self.assertTrue(state.stale)
        state.online = False
        apply_event_page(state, {"snapshot_id": 11, "events": [{"id": 1}]})
        self.assertTrue(state.stale)

    def test_profiles_rows_and_dashboard_accessibility(self):
        self.assertEqual(get_profile("target-win").encoding, "gb18030")
        self.assertEqual(summary_rows({"devices": 1})[0].value, "1")
        self.assertTrue(inspect_html('<html lang="en"><meta name="viewport"><script nonce="x">')["passed"] is False)
