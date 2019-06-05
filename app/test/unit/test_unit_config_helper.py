import imp
import os
import re
import sys

module_name = 'quarantine'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
quarantine = imp.load_module(module_name, fp, pathname, description)
fixture_path = os.path.join(here_dir, "../fixture/")


class TestConfigHelper:
    def test_get_match_list(self, monkeypatch):
        control = ["first_event_type", "secondeventtype", "third_event_type"]
        good_file = os.path.join(fixture_path, "good_events")
        monkeypatch.setenv("MATCH_FILE", good_file)
        processed = quarantine.ConfigHelper.get_match_list()
        assert control == processed

    def test_get_timestamp_inferred(self):
        result = quarantine.ConfigHelper.get_timestamp()
        print result
        assert re.match('^\d{4}-\d{2}-\d{2}$', result)

    def test_integration_string(self):
        """Test to confirm user_agent/integration_string is constructed properly"""
        assert quarantine.ConfigHelper().ua_string == quarantine.__version__
