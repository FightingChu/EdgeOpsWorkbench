"""New CLI commands execute services against isolated data and output real results."""
from contextlib import redirect_stdout,redirect_stderr
import io,json
from edgeops.cli import main
from tests.support import IsolatedCase

class CliExtensionsTests(IsolatedCase):
    def run_cli(self,*args):
        output=io.StringIO();errors=io.StringIO()
        with redirect_stdout(output),redirect_stderr(errors): code=main(['--data-dir',str(self.root),*args])
        return code,output.getvalue(),errors.getvalue()
    def test_analytics_and_configuration_commands(self):
        code,output,_=self.run_cli('analytics','temperature')
        self.assertEqual(code,0);self.assertEqual(json.loads(output)['count'],0)
        code,output,_=self.run_cli('configuration','inspect')
        self.assertEqual(json.loads(output)['host'],'127.0.0.1')
    def test_conversion_exports_real_file(self):
        source=self.root/'source.json';source.write_text('[{"message":"hello"}]')
        target=self.root/'target.csv'
        code,output,errors=self.run_cli('convert-events',str(source),str(target),'--from-format','json','--to-format','csv')
        self.assertEqual(code,0,errors);self.assertEqual(json.loads(output)['records'],1);self.assertTrue(target.is_file())
    def test_invalid_cli_configuration_returns_error(self):
        source=self.root/'bad.json';source.write_text('{"host":"0.0.0.0"}')
        code,_,errors=self.run_cli('configuration','inspect',str(source))
        self.assertEqual(code,2);self.assertIn('loopback',errors)
