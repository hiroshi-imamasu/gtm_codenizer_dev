import unittest 
from tagManager import TagManager
from triggerManager import TriggerManager
from gtmGenerater import GtmGenetator

class Test_bind_tag_trigger(unittest.TestCase):

    def test_bind_tag_trigger(self):
        tag_manager = TagManager()
        trigger_manager = TriggerManager()
        gtm_generator = GtmGenetator(tag_manager, trigger_manager)
        existing_tags = {'tag': [{'path': 'accounts/4702662944/containers/12751981/workspaces/7/tags/2', 'accountId': '4702662944', 'containerId': '12751981', 'workspaceId': '7', 'tagId': '2', 'name': 'Hello World Tag', 'type': 'html', 'parameter': [{'type': 'template', 'key': 'html', 'value': "<script>alert('updated hello world')</script>"}], 'fingerprint': '1571640840415', 'tagManagerUrl': 'localhost:9001/#/container/accounts/4702662944/containers/12751981/workspaces/7/tags/2?apiLink=tag'}]}
        tags_updated = [
        {
            "name": "Hello World Tag",
            "type": "html",
            "parameter": [{
              "key": "html",
              "type": "template",
              "value": "<script>alert('reupdated hello world')</script>"
            }]
        }] 
        expected_output =  [
            {"path": 'accounts/4702662944/containers/12751981/workspaces/7/tags/2', 
             "tag": {  
                 "name": "Hello World Tag",
                 "type": "html",
                 "parameter": [{
                    "key": "html",
                    "type": "template",
                    "value": "<script>alert('reupdated hello world')</script>"
                 }]
             }
            }
        ]
        # Get names of existing_tags 
        names = list(map((lambda tag : tag["name"]), existing_tags))
        print(names)
        pass


if __name__ == '__main__':
    unittest.main()