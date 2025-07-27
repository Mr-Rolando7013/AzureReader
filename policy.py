class Policys:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 displayName=None, keyCredentials=None, policyType=None,
                 policyDetail=None, policyIdentifier=None, tenantDefaultPolicy=None):
        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.displayName = displayName
        self.keyCredentials = keyCredentials
        self.policyType = policyType
        self.policyDetail = policyDetail
        self.policyIdentifier = policyIdentifier
        self.tenantDefaultPolicy = tenantDefaultPolicy

    def __repr__(self):
        return f"<Policy {self.displayName or self.objectId}>"