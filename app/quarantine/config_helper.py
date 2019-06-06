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
        self.match_list = ConfigHelper.get_match_list()
        self.start_timestamp = ConfigHelper.get_timestamp()
        self.ua_string = "Halo-Toolbox-Quarantine/%s" % self.get_tool_version()
        self.max_threads = 1
        self.halo_batch_size = 20

    @classmethod
    def get_match_list(cls):
        match_lines = []
        target_file = os.getenv("MATCH_FILE", "/conf/target_events")
        with open(target_file, 'r') as target:
            for line in target.readlines():
                if not re.match('^$', line):
                    match_lines.append(line.replace('\n', ''))
        print("Target event list:")
        print(match_lines)
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

    def get_tool_version(self):
        """Get version of this tool from the __init__.py file."""
        here_path = os.path.abspath(os.path.dirname(__file__))
        init_file = os.path.join(here_path, "__init__.py")
        ver = 0
        with open(init_file, 'r') as i_f:
            rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
            ver = rx_compiled.search(i_f.read()).group(1)
        return ver
