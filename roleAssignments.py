class RoleAssignments:
    def __init__(self, id, principalId=None, resourceScopes=None, roleDefinitionId=None):
        self.id = id  # Required (NOT NULL)
        self.principalId = principalId
        self.resourceScopes = resourceScopes
        self.roleDefinitionId = roleDefinitionId

    def __repr__(self):
        return f"<RoleAssignment {self.id} for Principal {self.principalId}>"