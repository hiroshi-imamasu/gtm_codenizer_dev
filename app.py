import json
from tagManager import TagManager
from triggerManager import TriggerManager
from tagGenerater import TagGenetator

"""Access and manage a Google Tag Manager account."""
"""
  TODO:
    1. Create TagGenerator class 
      - How to decide update or create
    
    2. Create Parse json class
    
    3. Dockernize   
"""

def UpdateHelloWorldTagWithTrigger(service, tag, trigger):
  """Update a Tag with a Trigger.

  Args:
    service: the Tag Manager service object.
    tag: the tag to associate with the trigger.
    trigger: the trigger to associate with the tag.
  """
  # Get the tag to update.
  tag = service.accounts().containers().workspaces().tags().get(
      path=tag['path']).execute()

  # Update the Firing Trigger for the Tag.
  tag['firingTriggerId'] = [trigger['triggerId']]

  # Update the Tag.
  response = service.accounts().containers().workspaces().tags().update(
      path=tag['path'],
      body=tag).execute()
  
  print(response)
    
    


if __name__ == '__main__':
  tag_manager = TagManager()
  trigger_manager = TriggerManager()
  tag_generator = TagGenetator(tag_manager, trigger_manager)

  with open("template.json") as config:
    data = json.load(config)
    # Get tag manager account ID
    account_id = data["account_id"]
    container_name = data["container_name"]
    work_space_name = data["work_space_name"]
    tags = list(data["tags"])
    triggers = list(data["triggers"])  
    account_path = 'accounts/%s' % account_id
    # Authenticate and construct service.
    service = tag_generator.get_service('tagmanager', 'v2', 'client_secret.json')
    # Find the container
    container = tag_generator.find_container(service, account_path, container_name)
    # Get or Create the workspace
    work_space = tag_generator.get_work_space(service, container, work_space_name)
    # Create or Update tags.
    ## updated_tags = tag_generator.update_tag(service, work_space, tags)
    ## print(updated_tags)
    ## tag_generator.create_tag(service, work_space,tags)
    
    # Create triggers
    print(tag_generator.handle_trigger(service, work_space, triggers))

    
