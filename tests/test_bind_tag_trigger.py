import unittest 
from src.tagManager import TagManager
from src.triggerManager import TriggerManager
from src.gtmGenerater import GtmGenetator

class Test_bind_tag_trigger(unittest.TestCase):

    def test_bind_tag_trigger(self):
        tag_manager = TagManager()
        trigger_manager = TriggerManager()
        gtm_generator = GtmGenetator(tag_manager, trigger_manager)
        config_path = "config/template.json"
        account_id, container_name, work_space_name, tags, triggers, bindings, account_path = gtm_generator.initial_setup(config_path)
        service = gtm_generator.get_service('tagmanager', 'v2', 'client_secret.json')
        # Find the container
        container = gtm_generator.find_container(service, account_path, container_name)
        work_space = gtm_generator.get_work_space(service, container, work_space_name)
        updated_tag = gtm_generator.handle_bind_tag_and_trigger(service, work_space, bindings, operation="YES")

if __name__ == '__main__':
    unittest.main()