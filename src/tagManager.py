class TagManager:
  def __init__(self):
    pass
  def create_tag(self, service, work_space, tags):
    """Create the Tag.

    Args:
      service: the Tag Manager service object.
      workspace: the workspace to create a tag within.
      tags: the list of tag information you want to create.

    Returns:
      The created tag.
    """
    existing_tags = service.accounts().containers().workspaces().tags().list(parent=work_space['path']).execute()
    if existing_tags == {}:
      ## In case no tag existed
      print("no tags existed...\n")
      return list(map(lambda tag: service.accounts().containers().workspaces().tags().create(parent=work_space['path'],body=tag).execute(), tags))
    elif len(existing_tags["tag"]) > 0:
      existing_tags_name = list(map(lambda x: x["name"], existing_tags["tag"]))
      ## Check tags you want to create is included in existing tags
      new_tags_candidates = self.get_new_candidate(existing_tags_name, tags)
      if len(new_tags_candidates) > 0:
        return list(map(lambda tag: service.accounts().containers().workspaces().tags().create(parent=work_space['path'],body=tag).execute(), new_tags_candidates))
      else: 
        print("You should check config file. Something is wrong\n")
  
  def update_tag(self, service, work_space, tags):
    """
      Update tag. 
    """
    existing_tags = service.accounts().containers().workspaces().tags().list(parent=work_space['path']).execute()
    ## Check tags you want to update is included in existing tags
    tags_to_be_updated = self.compare_existing_tags_and_tags_updated(existing_tags, tags)
    return list(map(lambda tag: service.accounts().containers().workspaces().tags().update(path=tag["path"], body=tag["body"]).execute(), tags_to_be_updated))
  
  def compare_existing_tags_and_tags_updated(self, existing_tags, tags_updated):
    tags_to_be_updated = []
    for existing_tag in existing_tags["tag"]:
      for tag_updated in tags_updated:
        if tag_updated["name"] == existing_tag["name"]:
          tags_to_be_updated.append({"path": existing_tag["path"], "body": tag_updated})
    return tags_to_be_updated
  
  def get_new_candidate(self, existing_tag_names, tags):
     new_tags_candidates = []
     for tag in tags:
       if tag["name"] not in existing_tag_names:
         new_tags_candidates.append(tag)
     return new_tags_candidates