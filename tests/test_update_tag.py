import unittest 

class TestUpdateTag(unittest.TestCase):
    def test_tags_update(self):
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
        print(compare_existing_tags_and_tags_updated(existing_tags, tags_updated))
        self.assertEqual(compare_existing_tags_and_tags_updated(existing_tags, tags_updated), expected_output)       
    


def compare_existing_tags_and_tags_updated(existing_tags, tags_updated):
  tags_to_be_updated = []
  for existing_tag in existing_tags["tag"]:
    for tag_updated in tags_updated:
        if tag_updated["name"] == existing_tag["name"]:
            tags_to_be_updated.append({"path": existing_tag["path"], "tag": tag_updated})
  return tags_to_be_updated



if __name__ == '__main__':
    unittest.main()