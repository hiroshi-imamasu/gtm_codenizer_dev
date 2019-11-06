import unittest 
from tagManager import TagManager
from triggerManager import TriggerManager
from gtmGenerater import GtmGenetator

class Test_bind_tag_trigger(unittest.TestCase):

    def test_bind_tag_trigger(self):
        ## WANT TO DO:
        ## Step1. Find trigger and tag which correspond to the names in JSON
        ## Step2. If step1. is successeded, change the 'firingTriggerId' in the tag to 'triggerId' in trigger. 
        ## Step3. Updated tag.   
        tag_manager = TagManager()
        trigger_manager = TriggerManager()
        gtm_generator = GtmGenetator(tag_manager, trigger_manager)
        existing_tags = [{'path': 'accounts/4702662944/containers/12751981/workspaces/7/tags/2', 'accountId': '4702662944', 'containerId': '12751981', 'workspaceId': '7', 'tagId': '2', 'name': 'Hello World Tag', 'type': 'html', 'parameter': [{'type': 'template', 'key': 'html', 'value': "<script>alert('updated hello world')</script>"}], 'fingerprint': '1571640840415', 'tagManagerUrl': 'localhost:9001/#/container/accounts/4702662944/containers/12751981/workspaces/7/tags/2?apiLink=tag'}]
        triggers = [{'name': 'example create', 'triggerId': '8'}]
        expected_output = '8' 
        bindings = [
          {  
            "tag": "Hello World Tag",
            "trigger": "example create"
          }
        ]
        self.find_corresponding_tag_and_trigger(bindings, existing_tags, triggers)
    
    def test_vacant_tag(self):
        ## TO DO 
        ## Check targeted_tag and targeted_trigger is exist
        vacant_tag = []
        vacant_trigger = []
        self.assertFalse(self.check_targeted_tag_and_trigger_exsist(vacant_tag, vacant_trigger))
    
    def test_successfully_pass_the_bindings_existed(self):
        pass
        
    
    def find_corresponding_tag_and_trigger(self, bindings, tags, triggers):
        for binding in bindings:
            targeted_tag = self.get_targeted_tag(binding, tags)
            targeted_trigger = self.get_targeted_trigger(binding, triggers)
            targeted_tag[0]["firingTriggerId"] = targeted_trigger[0]["triggerId"]
            ## Update tag

    
    def get_targeted_tag(self, binding, tags):
       return list(filter(lambda tag: tag["name"] == binding["tag"], tags))
    
    def get_targeted_trigger(self, binding, triggers):
       return list(filter(lambda trigger: trigger["name"] == binding["trigger"], triggers))
    
    def check_targeted_tag_and_trigger_exsist(self, tag, trigger):
       if tag == [] or trigger == []:
           return False
       else:
           return True
       
        


if __name__ == '__main__':
    unittest.main()