class DirectoryRole():

    def __init__(self, objectType, objectId, deletionTimestamp, cloudSecuirtyIdentifier, description, displayName, isSystem, roleDisabled, roleTemplateid):
        self.objectType = objectType
        self.objectId = objectId
        self.deletionTimestamp = deletionTimestamp
        self.cloudSecurityIdentifier = cloudSecuirtyIdentifier
        self.description = description
        self.displayName = displayName
        self.isSystem = isSystem
        self.roleDisabled = roleDisabled
        self.roleTemplateId = roleTemplateid

    def __str__(self):
        return f"Directory Role: {self.displayName}"