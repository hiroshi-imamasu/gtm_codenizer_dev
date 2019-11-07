class TriggerManager:
  def __init__(self):
    pass
    
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
      return list(map(lambda trigger:service.accounts().containers().workspaces().triggers().create(parent=workspace['path'],body=trigger).execute(),triggers))
    else:
      existing_trigger_names = list(map(lambda x: x["name"], existing_triggers["trigger"]))
      ## Check tags you want to create is included in existing tags
      new_triggers_candidates = self.get_new_candidate(existing_trigger_names, triggers)
      return list(map(lambda trigger: service.accounts().containers().workspaces().triggers().create(parent=workspace['path'],body=trigger).execute(), new_triggers_candidates))
  def update_trigger(self, service, workspace, triggers):
     """Update the trigger.

    Args:
      service: the Tag Manager service object.
      workspace: the workspace to create the trigger within.
      triggers: the trigger you want to update

    Returns:
      The updated trigger.
    """
     existing_triggers = service.accounts().containers().workspaces().triggers().list(parent=workspace['path']).execute()
     triggers_to_be_updated = self.compare_existing_triggers_and_triggers_updated(existing_triggers, triggers)
     return list(map(lambda trigger: service.accounts().containers().workspaces().triggers().update(path=trigger["path"], body=trigger["body"]).execute(), triggers_to_be_updated))
  
  def compare_existing_triggers_and_triggers_updated(self, existing_triggers, triggers_updated):
    triggers_to_be_updated = []
    for existing_trigger in existing_triggers["trigger"]:
      for trigger_updated in triggers_updated:
        if trigger_updated["name"] == existing_trigger["name"]:
          triggers_to_be_updated.append({"path": existing_trigger["path"], "body": trigger_updated})
    return triggers_to_be_updated
  
  def get_new_candidate(self, existing_trigger_names, triggers):
    new_triggers_candidates = []
    for trigger in triggers:
      if trigger["name"] not in existing_trigger_names:
        new_triggers_candidates.append(trigger)
    return new_triggers_candidates

