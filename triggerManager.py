class TriggerManager:
  def __init__(self):
    print("Trigger Manager is instantiated")
    
  def create_trigger(self, service, workspace, triggers):
    """Create the trigger.

    Args:
      service: the Tag Manager service object.
      workspace: the workspace to create the trigger within.
      triggers: the trigger you want to create

    Returns:
      The created trigger.
    """
    existing_triggers = service.accounts().containers().workspaces().triggers().list(parent=workspace["path"]).execute()
    if existing_triggers == {}:
      return list(map(lambda trigger:service.accounts().containers().workspaces().triggers().create(
      parent=workspace['path'],
      body=trigger).execute()),triggers)
    else:
      existing_trigger_name = list(map(lambda x: x["name"], existing_triggers["trigger"]))
      ## Check tags you want to create is included in existing tags
      new_tags_candidates = [x for x in triggers if lambda x: x["name"] not in existing_trigger_name]
      return list(map(lambda tag: service.accounts().containers().workspaces().tags().create(parent=workspace['path'],body=tag).execute(), new_tags_candidates))