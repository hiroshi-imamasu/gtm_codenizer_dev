import unittest
from src.tagManager import TagManager
from src.triggerManager import TriggerManager
from src.gtmGenerater import GtmGenetator 

class TestUpdateTag(unittest.TestCase):
    def test_tags_update(self):
        tag_manager = TagManager()
        trigger_manager = TriggerManager()
        gtm_generator = GtmGenetator(tag_manager, trigger_manager)
        config_path = "config/template.json"

        account_id, container_name, work_space_name, tags, triggers, bindings, account_path = gtm_generator.initial_setup(config_path)
        updating_tag_candidate = [{
            "name": "test Tag",
            "type": "html",
            "parameter": [{
              "key": "html",
              "type": "template",
              "value": "<script>alert('update test')</script>"
            }]
        }]
        service = gtm_generator.get_service('tagmanager', 'v2', 'client_secret.json')
        # Find the container
        container = gtm_generator.find_container(service, account_path, container_name)
        # Get or Create the workspace
        work_space = gtm_generator.get_work_space(service, container, work_space_name)
        updated_tag = gtm_generator.handle_tag(service, work_space, updating_tag_candidate, operation="UPDATE")
        self.assertTrue(updated_tag[0]["name"], "test Tag")



if __name__ == '__main__':
    unittest.main()