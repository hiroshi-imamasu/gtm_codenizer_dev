from src.tagManager import TagManager
from src.triggerManager import TriggerManager
from src.gtmGenerater import GtmGenetator
import click

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


@click.command()
@click.option("--config", default=None, help="Name of config file")
@click.option("--tag", default=None, help="Operation for tags")
@click.option("--trigger", default=None, help="Operation for triggers")
@click.option("--binding", default="YES", help="Operation for bindings")


def main(config, tag, trigger, binding):
  tag_manager = TagManager()
  trigger_manager = TriggerManager()
  gtm_generator = GtmGenetator(tag_manager, trigger_manager)
  config_file_path = 'config/%s' % config
  print("Processing....\n")
  
  account_id, container_name, work_space_name, tags, triggers, bindings, account_path = gtm_generator.initial_setup(config_file_path)
  # Authenticate and construct service.
  service = gtm_generator.get_service('tagmanager', 'v2', 'client_secret.json')
  # Find the container
  container = gtm_generator.find_container(service, account_path, container_name)
  # Get or Create the workspace
  work_space = gtm_generator.get_work_space(service, container, work_space_name)
  # Create or Update tags.
  gtm_generator.handle_tag(service, work_space, tags, operation=tag)
  # Create or Update triggers
  gtm_generator.handle_trigger(service, work_space, triggers, operation=trigger)
  # Bind tags and triggers
  gtm_generator.handle_bind_tag_and_trigger(service, work_space, bindings, operation=binding)
  print("Congrats!! gtm has successfully worked")


if __name__ == '__main__':
  main()