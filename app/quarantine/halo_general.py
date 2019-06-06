import cloudpassage
import sys


class HaloGeneral(object):
    """This class wraps Halo API functionality, except for /v1/events."""
    def __init__(self, config):
        """Pass in a quarantine.ConfigHelper object on instantiation."""
        self.ua = config.ua_string
        self.session = cloudpassage.HaloSession(config.halo_key,
                                                config.halo_secret,
                                                integration_string=self.ua)
        self.server_obj = cloudpassage.Server(self.session)
        self.event_obj = cloudpassage.Event(self.session)
        self.group_obj = cloudpassage.ServerGroup(self.session)
        self.target_group_id = self.get_groupid(config.quarantine_grp_name)
        return

    def get_groupid(self, group_name):
        """determine group_id for a named group"""
        for group in self.group_obj.list_all():
            if group["name"] == group_name:
                target_id = group["id"]
                return target_id
        # Fall through if no match
        print("ERROR: No group in account named %s" % group_name)
        sys.exit(2)

    def quarantine_workload(self, agent_id):
        """Move a workload, identified by agent_id, into quarantine"""
        self.server_obj.assign_group(agent_id, self.target_group_id)
        return
