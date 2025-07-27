class ExtensionPropertys:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 appDisplayName=None, name=None, dataType=None,
                 isSyncedFromOnPremises=False, targetObjects=None):
        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.appDisplayName = appDisplayName
        self.name = name
        self.dataType = dataType
        self.isSyncedFromOnPremises = isSyncedFromOnPremises
        self.targetObjects = targetObjects

    def __repr__(self):
        return f"<ExtensionProperty {self.name or self.objectId}>"