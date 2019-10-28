import argparse
import sys

import httplib2

from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools 


"""
  TODO:
    1. Create TagGenerator class 
      - How to decide update or create
    
    2. Create Parse json class
    
    3. Dockernize   
"""


class GtmGenetator:
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
  
  def handle_tag(self, service, workspace, tags):
    #self.tag_manager.create_tag(service, workspace, tags)
    self.tag_manager.update_tag(service, workspace, tags)
  
  def handle_trigger(self, service, workspace, triggers):
    #self.trigger_manager.create_trigger(service, workspace, triggers)
    self.trigger_manager.update_trigger(service, workspace, triggers)
  
  def bind_tag_and_trigger(self, service, workspace, bindings):
    """
     Bind tag and trigger
      Args:
      service: the Tag Manager service object.
      work_space: the workspace you want to get.
      bindings: the pair of tag name and trigger name that you're interested in. 
    """
    # Get existing tags and triggers 
    existing_tags = service.accounts().containers().workspaces().tags().list(parent=workspace['path']).execute()
    existing_trigger = service.accounts().containers().workspaces().triggers().list(parent=workspace["path"]).execute()
    for binding in bindings:
      if binding["tag"] in existing_tags["tag"]["name"] and binding["trigger"] in existing_trigger["trigger"]:
        pass

  def check_tag_and_trigger_is_included(self, existing_tags, existing_trigger, tag, trigger):
    ## Get names of existings tags and check tag you want to bind is included in
    # tag_name_is_included = [for tag["name"] in existing_tags["tag"] if lambda tag : existing_tags["tag"]]
    # trigger_name = map(lambda tag )
    pass