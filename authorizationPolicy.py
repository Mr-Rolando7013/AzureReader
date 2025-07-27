class AuthorizationPolicy:
    def __init__(self, id, allowInvitesFrom=None,
                 allowedToSignUpEmailBasedSubscriptions=False,
                 allowedToUseSSPR=False,
                 allowEmailVerifiedUsersToJoinOrganization=False,
                 blockMsolPowerShell=False,
                 defaultUserRolePermissions=None,
                 displayName=None,
                 description=None,
                 enabledPreviewFeatures=None,
                 guestUserRoleId=None,
                 permissionGrantPolicyIdsAssignedToDefaultUserRole=None):
        
        self.id = id
        self.allowInvitesFrom = allowInvitesFrom
        self.allowedToSignUpEmailBasedSubscriptions = allowedToSignUpEmailBasedSubscriptions
        self.allowedToUseSSPR = allowedToUseSSPR
        self.allowEmailVerifiedUsersToJoinOrganization = allowEmailVerifiedUsersToJoinOrganization
        self.blockMsolPowerShell = blockMsolPowerShell
        self.defaultUserRolePermissions = defaultUserRolePermissions
        self.displayName = displayName
        self.description = description
        self.enabledPreviewFeatures = enabledPreviewFeatures
        self.guestUserRoleId = guestUserRoleId
        self.permissionGrantPolicyIdsAssignedToDefaultUserRole = permissionGrantPolicyIdsAssignedToDefaultUserRole

    def __repr__(self):
        return f"<AuthorizationPolicy {self.displayName or self.id}>"