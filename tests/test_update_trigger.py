import unittest
from src.tagManager import TagManager
from src.triggerManager import TriggerManager
from src.gtmGenerater import GtmGenetator

class Test_create_tag(unittest.TestCase):
    def test_create_tag(self):
        ## In case there are more than one triggers
        tag_manager = TagManager()
        trigger_manager = TriggerManager()
        gtm_generator = GtmGenetator(tag_manager, trigger_manager)
        config_path = "config/template.json"

        account_id, container_name, work_space_name, tags, triggers, bindings, account_path = gtm_generator.initial_setup(config_path)
        service = gtm_generator.get_service('tagmanager', 'v2', 'client_secret.json')
        # Find the container
        container = gtm_generator.find_container(service, account_path, container_name)
        # Get or Create the workspace
        work_space = gtm_generator.get_work_space(service, container, work_space_name)
        updated_trigger = gtm_generator.handle_trigger(service, work_space, triggers, operation="UPDATE")
        self.assertTrue(updated_trigger[0]["name"], "example update")