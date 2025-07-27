class Applications():
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 addIns=None, allowActAsForAllClients=False, allowPassthroughUsers=False,
                 appBranding=None, appCategory=None, appData=None, appId=None,
                 applicationTemplateId=None, appMetadata=None, appRoles=None,
                 availableToOtherTenants=False, certification=None,
                 disabledByMicrosoftStatus=None, displayName=None,
                 encryptedMsiApplicationSecret=None, errorUrl=None,
                 groupMembershipClaims=None, homepage=None, identifierUris=None,
                 informationalUrls=None, isDeviceOnlyAuthSupported=False,
                 keyCredentials=None, knownClientApplications=None,
                 logo=None, logoUrl=None, logoutUrl=None, mainLogo=None,
                 oauth2AllowIdTokenImplicitFlow=False, oauth2AllowImplicitFlow=False,
                 oauth2AllowUrlPathMatching=False, oauth2Permissions=None,
                 oauth2RequirePostResponse=False, optionalClaims=None,
                 parentalControlSettings=None, passwordCredentials=None,
                 publicClient=False, publisherDomain=None, recordConsentConditions=None,
                 replyUrls=None, requiredResourceAccess=None, samlMetadataUrl=None,
                 supportsConvergence=False, tokenEncryptionKeyId=None,
                 trustedCertificateSubjects=None, verifiedPublisher=None):

        self.objectType = objectType
        self.objectId = objectId
        self.deletionTimestamp = deletionTimestamp
        self.addIns = addIns
        self.allowActAsForAllClients = allowActAsForAllClients
        self.allowPassthroughUsers = allowPassthroughUsers
        self.appBranding = appBranding
        self.appCategory = appCategory
        self.appData = appData
        self.appId = appId
        self.applicationTemplateId = applicationTemplateId
        self.appMetadata = appMetadata
        self.appRoles = appRoles
        self.availableToOtherTenants = availableToOtherTenants
        self.certification = certification
        self.disabledByMicrosoftStatus = disabledByMicrosoftStatus
        self.displayName = displayName
        self.encryptedMsiApplicationSecret = encryptedMsiApplicationSecret
        self.errorUrl = errorUrl
        self.groupMembershipClaims = groupMembershipClaims
        self.homepage = homepage
        self.identifierUris = identifierUris
        self.informationalUrls = informationalUrls
        self.isDeviceOnlyAuthSupported = isDeviceOnlyAuthSupported
        self.keyCredentials = keyCredentials
        self.knownClientApplications = knownClientApplications
        self.logo = logo
        self.logoUrl = logoUrl
        self.logoutUrl = logoutUrl
        self.mainLogo = mainLogo
        self.oauth2AllowIdTokenImplicitFlow = oauth2AllowIdTokenImplicitFlow
        self.oauth2AllowImplicitFlow = oauth2AllowImplicitFlow
        self.oauth2AllowUrlPathMatching = oauth2AllowUrlPathMatching
        self.oauth2Permissions = oauth2Permissions
        self.oauth2RequirePostResponse = oauth2RequirePostResponse
        self.optionalClaims = optionalClaims
        self.parentalControlSettings = parentalControlSettings
        self.passwordCredentials = passwordCredentials
        self.publicClient = publicClient
        self.publisherDomain = publisherDomain
        self.recordConsentConditions = recordConsentConditions
        self.replyUrls = replyUrls
        self.requiredResourceAccess = requiredResourceAccess
        self.samlMetadataUrl = samlMetadataUrl
        self.supportsConvergence = supportsConvergence
        self.tokenEncryptionKeyId = tokenEncryptionKeyId
        self.trustedCertificateSubjects = trustedCertificateSubjects
        self.verifiedPublisher = verifiedPublisher

    def __repr__(self):
        return f"<Application {self.displayName} ({self.appId})>"