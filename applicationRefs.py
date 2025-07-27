class ApplicationRefs():
    def __init__(self, appCategory, appContextId, appData, appId, appRoles, availableToOtherTenants, certification, 
                 displayName, errorUrl, homepage, identifierUris, knownClientApplications, logoutUrl, logoUrl,
                 mainLogo, oauth2Permissions, publisherDomain, publisherName, publicClient, replyUrls, requiredResourceAccess,
                 samlMetadataUrl, supportsConvergence, verifiedPublisher):
        self.appCategory = appCategory
        self.appContextId = appContextId
        self.appData = appData
        self.appId = appId
        self.appRoles = appRoles
        self.availableToOtherTenants = availableToOtherTenants
        self.certification = certification
        self.displayName = displayName
        self.errorUrl = errorUrl
        self.homepage = homepage
        self.identifierUris = identifierUris
        self.knownClientApplications = knownClientApplications
        self.logoutUrl = logoutUrl
        self.logoUrl = logoUrl
        self.mainLogo = mainLogo
        self.oauth2Permissions = oauth2Permissions
        self.publisherDomain = publisherDomain
        self.publisherName = publisherName
        self.publicClient = publicClient
        self.replyUrls = replyUrls
        self.requiredResourceAccess = requiredResourceAccess
        self.samlMetadataUrl = samlMetadataUrl
        self.supportsConvergence = supportsConvergence
        self.verifiedPublisher = verifiedPublisher

    def __str__(self):
        return f"Application Refs: {self.displayName}"