class EligibleRoleAssignments:
    def __init__(self, id, principalId=None, resourceScopes=None, roleDefinitionId=None):
        self.id = id  # Required (NOT NULL, PRIMARY KEY)
        self.principalId = principalId
        self.resourceScopes = resourceScopes
        self.roleDefinitionId = roleDefinitionId

    def __repr__(self):
        return f"<EligibleRoleAssignment {self.id} for Principal {self.principalId}>"