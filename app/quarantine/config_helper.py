from datetime import date
import os
import re


class ConfigHelper(object):
    """Manage all configuration information for the application"""
    def __init__(self):
        self.halo_key = os.getenv("HALO_API_KEY")
        self.halo_secret = os.getenv("HALO_API_SECRET_KEY")
        self.quarantine_grp_name = os.getenv("$QUARANTINE_GROUP_NAME",
                                             "Quarantine")
        self.match_list = ConfigHelper.get_match_list("/conf/target-events")
        self.start_timestamp = ConfigHelper.get_timestamp()
        self.ua_string = "Halo-Toolbox-Quarantine/2.0"
        self.max_threads = 1
        self.halo_batch_size = 20

    @classmethod
    def get_match_list(cls, target_file):
        match_lines = []
        with open(target_file, 'r') as target:
            for line in target.readlines():
                if not re.match('^$', line):
                    match_lines.append(line.replace('\n', ''))
        print "Target event list:"
        print match_lines
        return match_lines

    @classmethod
    def get_timestamp(cls):
        env_time = os.getenv("HALO_EVENTS_START", "")
        if env_time == "":
            env_time = ConfigHelper.iso8601_today()
        return env_time

    @classmethod
    def iso8601_today(cls):
        today = date.today()
        retval = today.isoformat()
        return retval
