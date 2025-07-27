class AdministrativeUnits():
    def __init__(self, objectType, objectId, deletionTimestamp, displayName, description, isMemberManagementRestricted, 
                 membershipRule, membershipProcessingState, membershipType, visibility):
        self.objectType = objectType
        self.objectId = objectId
        self.deletionTimestamp = deletionTimestamp
        self.displayName = displayName
        self.description = description
        self.isMemberManagementRestricted = isMemberManagementRestricted
        self.membershipRule = membershipRule
        self.membershipProcessingState = membershipProcessingState
        self.membershipType = membershipType
        self.visibility = visibility

    def __str__(self):
        return f"AdminUnit: {self.displayName}"