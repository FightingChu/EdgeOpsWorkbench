"""Configuration service resolves layers and compares validated values."""
import json
from edgeops.application.configuration import ConfigurationService
from tests.support import IsolatedCase

class ConfigurationServiceTests(IsolatedCase):
    def test_config_overlay_and_diff(self):
        path=self.root/'settings.json';path.write_text(json.dumps({'port':9000}))
        service=ConfigurationService()
        self.assertEqual(service.inspect([path])['port'],9000)
        self.assertEqual(service.compare({'port':9000},{'port':9001})[0]['path'],'port')
    def test_unsafe_settings_rejected(self):
        with self.assertRaises(ValueError): ConfigurationService().inspect(overrides={'host':'0.0.0.0'})
