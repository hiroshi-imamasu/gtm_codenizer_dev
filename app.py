from tagManager import TagManager
from triggerManager import TriggerManager
from gtmGenerater import GtmGenetator

"""Access and manage a Google Tag Manager account."""
"""
  TODO:
    1. Create TagGenerator class 
      - How to decide update or create
      - How to bind trigger to tag
    
    2. Create Parse json method

    3. Introduce command line library
    
    4. Dockernize   
"""

if __name__ == '__main__':
  tag_manager = TagManager()
  trigger_manager = TriggerManager()
  gtm_generator = GtmGenetator(tag_manager, trigger_manager)

  print("Processing....")
  
  account_id, container_name, work_space_name, tags, triggers, bindings, account_path = gtm_generator.initial_setup("template.json")
  # Authenticate and construct service.
  service = gtm_generator.get_service('tagmanager', 'v2', 'client_secret.json')
  # Find the container
  container = gtm_generator.find_container(service, account_path, container_name)
  # Get or Create the workspace
  work_space = gtm_generator.get_work_space(service, container, work_space_name)
  # Create or Update tags.
  ## updated_tags = tag_generator.update_tag(service, work_space, tags)
  ## print(updated_tags)
  ## tag_generator.create_tag(service, work_space,tags)
  # Create or Update triggers
  gtm_generator.handle_trigger(service, work_space, triggers)
  # Bind tags and triggers
  gtm_generator.handle_bind_tag_and_trigger(service, work_space, bindings)
  print("Congrats!! gtm has successfully worked")
    
