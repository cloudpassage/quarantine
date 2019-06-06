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


class TestHaloEvents:
    def test_build_url(self):
        baseurl = "/99/helololol-world"
        modifiers = {"trolol": "lololol"}
        result = quarantine.HaloEvents.build_url(baseurl, modifiers)
        print(result)
        assert re.match(r'/99/helololol-world\?trolol=lololol', result)
