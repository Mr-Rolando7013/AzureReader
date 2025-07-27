class Groups:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 appMetadata=None, classification=None, cloudSecurityIdentifier=None,
                 createdDateTime=None, createdByAppId=None, description=None,
                 dirSyncEnabled=False, displayName=None, exchangeResources=None,
                 expirationDateTime=None, externalGroupIds=None, externalGroupProviderId=None,
                 externalGroupState=None, creationOptions=None, groupTypes=None,
                 infoCatalogs=None, isAssignableToRole=False, isMembershipRuleLocked=False,
                 isPublic=False, lastDirSyncTime=None, licenseAssignment=None, mail=None,
                 mailNickname=None, mailEnabled=False, membershipRule=None,
                 membershipRuleProcessingState=None, membershipTypes=None,
                 onPremisesSecurityIdentifier=None, preferredDataLocation=None,
                 preferredLanguage=None, primarySMTPAddress=None, provisioningErrors=None,
                 proxyAddresses=None, renewedDateTime=None, resourceBehaviorOptions=None,
                 resourceProvisioningOptions=None, securityEnabled=False,
                 sharepointResources=None, targetAddress=None, theme=None,
                 visibility=None, wellKnownObject=None):
        
        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.appMetadata = appMetadata
        self.classification = classification
        self.cloudSecurityIdentifier = cloudSecurityIdentifier
        self.createdDateTime = createdDateTime
        self.createdByAppId = createdByAppId
        self.description = description
        self.dirSyncEnabled = dirSyncEnabled
        self.displayName = displayName
        self.exchangeResources = exchangeResources
        self.expirationDateTime = expirationDateTime
        self.externalGroupIds = externalGroupIds
        self.externalGroupProviderId = externalGroupProviderId
        self.externalGroupState = externalGroupState
        self.creationOptions = creationOptions
        self.groupTypes = groupTypes
        self.infoCatalogs = infoCatalogs
        self.isAssignableToRole = isAssignableToRole
        self.isMembershipRuleLocked = isMembershipRuleLocked
        self.isPublic = isPublic
        self.lastDirSyncTime = lastDirSyncTime
        self.licenseAssignment = licenseAssignment
        self.mail = mail
        self.mailNickname = mailNickname
        self.mailEnabled = mailEnabled
        self.membershipRule = membershipRule
        self.membershipRuleProcessingState = membershipRuleProcessingState
        self.membershipTypes = membershipTypes
        self.onPremisesSecurityIdentifier = onPremisesSecurityIdentifier
        self.preferredDataLocation = preferredDataLocation
        self.preferredLanguage = preferredLanguage
        self.primarySMTPAddress = primarySMTPAddress
        self.provisioningErrors = provisioningErrors
        self.proxyAddresses = proxyAddresses
        self.renewedDateTime = renewedDateTime
        self.resourceBehaviorOptions = resourceBehaviorOptions
        self.resourceProvisioningOptions = resourceProvisioningOptions
        self.securityEnabled = securityEnabled
        self.sharepointResources = sharepointResources
        self.targetAddress = targetAddress
        self.theme = theme
        self.visibility = visibility
        self.wellKnownObject = wellKnownObject

    def __repr__(self):
        return f"<Group {self.displayName or self.mailNickname or self.objectId}>"