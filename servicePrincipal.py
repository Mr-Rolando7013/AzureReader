class ServicePrincipals:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 accountEnabled=False, addIns=None, alternativeNames=None,
                 appBranding=None, appCategory=None, appData=None, appDisplayName=None,
                 appId=None, applicationTemplateId=None, appMetadata=None,
                 appOwnerTenantId=None, appRoleAssignmentRequired=False,
                 appRoles=None, authenticationPolicy=None, disabledByMicrosoftStatus=None,
                 displayName=None, errorUrl=None, homepage=None, informationalUrls=None,
                 keyCredentials=None, logoutUrl=None, managedIdentityResourceId=None,
                 microsoftFirstParty=False, notificationEmailAddresses=None,
                 oauth2Permissions=None, passwordCredentials=None,
                 preferredSingleSignOnMode=None, preferredTokenSigningKeyEndDateTime=None,
                 preferredTokenSigningKeyThumbprint=None, publisherName=None,
                 replyUrls=None, samlMetadataUrl=None, samlSingleSignOnSettings=None,
                 servicePrincipalNames=None, tags=None, tokenEncryptionKeyId=None,
                 servicePrincipalType=None, useCustomTokenSigningKey=False,
                 verifiedPublisher=None):
        
        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.accountEnabled = accountEnabled
        self.addIns = addIns
        self.alternativeNames = alternativeNames
        self.appBranding = appBranding
        self.appCategory = appCategory
        self.appData = appData
        self.appDisplayName = appDisplayName
        self.appId = appId
        self.applicationTemplateId = applicationTemplateId
        self.appMetadata = appMetadata
        self.appOwnerTenantId = appOwnerTenantId
        self.appRoleAssignmentRequired = appRoleAssignmentRequired
        self.appRoles = appRoles
        self.authenticationPolicy = authenticationPolicy
        self.disabledByMicrosoftStatus = disabledByMicrosoftStatus
        self.displayName = displayName
        self.errorUrl = errorUrl
        self.homepage = homepage
        self.informationalUrls = informationalUrls
        self.keyCredentials = keyCredentials
        self.logoutUrl = logoutUrl
        self.managedIdentityResourceId = managedIdentityResourceId
        self.microsoftFirstParty = microsoftFirstParty
        self.notificationEmailAddresses = notificationEmailAddresses
        self.oauth2Permissions = oauth2Permissions
        self.passwordCredentials = passwordCredentials
        self.preferredSingleSignOnMode = preferredSingleSignOnMode
        self.preferredTokenSigningKeyEndDateTime = preferredTokenSigningKeyEndDateTime
        self.preferredTokenSigningKeyThumbprint = preferredTokenSigningKeyThumbprint
        self.publisherName = publisherName
        self.replyUrls = replyUrls
        self.samlMetadataUrl = samlMetadataUrl
        self.samlSingleSignOnSettings = samlSingleSignOnSettings
        self.servicePrincipalNames = servicePrincipalNames
        self.tags = tags
        self.tokenEncryptionKeyId = tokenEncryptionKeyId
        self.servicePrincipalType = servicePrincipalType
        self.useCustomTokenSigningKey = useCustomTokenSigningKey
        self.verifiedPublisher = verifiedPublisher

    def __repr__(self):
        return f"<ServicePrincipal {self.displayName or self.appDisplayName or self.objectId}>"