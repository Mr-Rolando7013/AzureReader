class DirectorySettings:
    def __init__(self, id, displayName=None, templateId=None, values=None):
        self.id = id  # Required (NOT NULL)
        self.displayName = displayName
        self.templateId = templateId
        self.values = values

    def __repr__(self):
        return f"<DirectorySetting {self.displayName or self.id}>"