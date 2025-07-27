class AppRoleAssignments():
    def __init__(self, objectType, objectId, deletionTimestamp, creationTimestamp, id,
                 principalDisplayName, principalId, principalType, resourceDisplayName, resourceId):
        self.objectType = objectType
        self.objectId = objectId
        self.deletionTimestamp = deletionTimestamp
        self.creationTimestamp = creationTimestamp
        self.id = id
        self.principalDisplayName = principalDisplayName
        self.principalId = principalId
        self.principalType = principalType
        self.resourceDisplayName = resourceDisplayName
        self.resourceId = resourceId

    def __str__(self):
        return f"AppRoleAssignments: {self.resourceDisplayName}"