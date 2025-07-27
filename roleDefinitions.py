class RoleDefinitions:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 description=None, displayName=None, isBuiltIn=False,
                 isEnabled=False, resourceScopes=None, rolePermissions=None,
                 templateId=None, version=None):
        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.description = description
        self.displayName = displayName
        self.isBuiltIn = isBuiltIn
        self.isEnabled = isEnabled
        self.resourceScopes = resourceScopes
        self.rolePermissions = rolePermissions
        self.templateId = templateId
        self.version = version

    def __repr__(self):
        return f"<RoleDefinition {self.displayName or self.objectId}>"