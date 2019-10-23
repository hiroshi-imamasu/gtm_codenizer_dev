"""Access and manage a Google Tag Manager account."""

import argparse
import sys

import httplib2
import json

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from tagManager import TagManager
from triggerManager import TriggerManager
from util import find_work_space 


"""
  TODO:
    1. Create TagGenerator class 
      - How to decide update or create
    
    2. Create Parse json class
    
    3. Dockernize   
"""


class TagGenetator:
  def __init__(self, tag_manager, trigger_manager):
    print("instantiated")
    # Define the auth scopes to request.
    self.scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers']
    self.tag_manager = tag_manager
    self.trigger_manager = trigger_manager
  
  def get_service(self, api_name, api_version, client_secrets_path):
    """Get a service that communicates to a Google API.

    Args:
    api_name: string The name of the api to connect to.
    api_version: string The api version to connect to.
    client_secrets_path: string A path to a valid client secrets file. 
    """
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=self.scope,
      message=tools.message_if_missing(client_secrets_path))
  
    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(api_name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
      credentials = tools.run_flow(flow, storage, flags)
    
    http = credentials.authorize(http=httplib2.Http())
    # Build the service object.
    service = build(api_name, api_version, http=http)
    
    return service

  def find_container(self, service, account_path, container_name):
    """Find a container named <container_name>.

    Args:
      service: the Tag Manager service object.
      account_path: the path of the Tag Manager account from which to retrieve the container.
      container_name: the container name concerned.
    """
    # Query the Tag Manager API to list all containers for the given account.
    container_wrapper = service.accounts().containers().list(
      parent=account_path).execute()

    # Find and return the container if it exists.
    for container in container_wrapper['container']:
      if container['name'] == container_name:
        return container
      else: 
        print("No container is found")
    return None

  def create_work_space(self, service, container, work_space_name):
    """Creates a workspace named <work_space_name>.

    Args:
      service: the Tag Manager service object.
      container: the container to insert the workspace within.
      work_space_name: the workspace name you want to create 

    Returns:
      The created workspace object.
    """
    return service.accounts().containers().workspaces().create(
        parent=container['path'],
        body={
            'name': work_space_name,
        }).execute()

  def get_work_space(self, service, container, work_space_name):
    """
     Get a workspace named <work_space_name>.

     Args:
      service: the Tag Manager service object.
      container: the container the workspace exists.
      work_space_name: the workspace name you want to get.

    Returns:
      If workspce exists, return the workspace
      If not existed, Create a new workspace. 
    """
    path = container["path"]
    workspaces = service.accounts().containers().workspaces().list(
        parent=path).execute()

    workspace = list(filter(lambda x:x['name'] == work_space_name, workspaces["workspace"]))
    if len(workspace) > 0:
      return workspace[0]
    else:
      self.create_work_space(service, container, work_space_name) 
  





def CreateHelloWorldTrigger(service, workspace):
  """Create the Hello World Trigger.

  Args:
    service: the Tag Manager service object.
    workspace: the workspace to create the trigger within.

  Returns:
    The created trigger.
  """

  hello_world_trigger = {
      'name': 'Hello World Rule',
      'type': 'PAGEVIEW'
  }

  return service.accounts().containers().workspaces().triggers().create(
      parent=workspace['path'],
      body=hello_world_trigger).execute()


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
    
    

def main(argv):
  with open("template.json") as config:
    data = json.load(config)
     # Get tag manager account ID
    account_id = data["account_id"]
    container_name = data["container_name"]
    work_space_name = data["work_space_name"]
    account_path = 'accounts/%s' % account_id
    
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/tagmanager.edit.containers']
    
    # Authenticate and construct service.
    service = GetService('tagmanager', 'v2', scope, 'client_secret.json')
    
    # Find the container.
    container = FindContainer(service, account_path, container_name)
    
    # Get or Create workspace. 
    workspace = GetWorkspace(service, container, work_space_name)
    
    # Create tag
    tag = CreateHelloWorldTag(service, workspace)

    # Create trigger 
    trigger = CreateHelloWorldTrigger(service, workspace)

    # Update tag to bind trigger
    UpdateHelloWorldTagWithTrigger(service, tag, trigger)






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

    
