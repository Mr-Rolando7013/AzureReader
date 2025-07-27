class OAuth2PermissionGrants:
    def __init__(self, clientId=None, consentType=None, expiryTime=None,
                 objectId=None, principalId=None, resourceId=None,
                 scope=None, startTime=None):
        self.clientId = clientId
        self.consentType = consentType
        self.expiryTime = expiryTime
        self.objectId = objectId  # Required (NOT NULL)
        self.principalId = principalId
        self.resourceId = resourceId
        self.scope = scope
        self.startTime = startTime

    def __repr__(self):
        return f"<OAuth2PermissionGrant {self.objectId} for Client {self.clientId}>"