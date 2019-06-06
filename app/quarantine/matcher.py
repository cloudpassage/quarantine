import re
import sys


class Matcher(object):
    def __init__(self, match_list):
        """Initialize this class, passing in a list of event types to match."""
        self.match_list = match_list
        if Matcher.verify_match_list(self.match_list) is False:
            sys.exit(2)

    def is_a_match(self, event_type):
        """Test an event type agains the list of targeted events"""
        for match in self.match_list:
            if event_type == match:
                return True
        return False

    @classmethod
    def verify_match_list(cls, match_list):
        """Returns true if match list is sane."""
        sane = True
        if type(match_list) is not list:
            print("Bad input!  Must provide a list of match strings!")
            sane = False
        for item in match_list:
            if type(item) is not str:
                print("Bad input!  All event types must be strings!")
                sane = False
        for item in match_list:
            if not re.match(r'^(\w|_)+$', item):
                print("Invalid match item: %s" % item)
                sane = False
        return sane
