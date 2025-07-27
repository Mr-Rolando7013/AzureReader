class TenantDetails:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 assignedPlans=None, authorizedServiceInstance=None, city=None,
                 cloudRtcUserPolicies=None, companyLastDirSyncTime=None, companyTags=None,
                 compassEnabled=False, country=None, countryLetterCode=None,
                 dirSyncEnabled=False, displayName=None,
                 isMultipleDataLocationsForServicesEnabled=False,
                 marketingNotificationEmails=None, postalCode=None,
                 preferredLanguage=None, privacyProfile=None, provisionedPlans=None,
                 provisioningErrors=None, releaseTrack=None, replicationScope=None,
                 securityComplianceNotificationMails=None,
                 securityComplianceNotificationPhones=None,
                 selfServePasswordResetPolicy=None, state=None, street=None,
                 technicalNotificationMails=None, telephoneNumber=None,
                 tenantType=None, createdDateTime=None, verifiedDomains=None,
                 windowsCredentialsEncryptionCertificate=None):
        
        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.assignedPlans = assignedPlans
        self.authorizedServiceInstance = authorizedServiceInstance
        self.city = city
        self.cloudRtcUserPolicies = cloudRtcUserPolicies
        self.companyLastDirSyncTime = companyLastDirSyncTime
        self.companyTags = companyTags
        self.compassEnabled = compassEnabled
        self.country = country
        self.countryLetterCode = countryLetterCode
        self.dirSyncEnabled = dirSyncEnabled
        self.displayName = displayName
        self.isMultipleDataLocationsForServicesEnabled = isMultipleDataLocationsForServicesEnabled
        self.marketingNotificationEmails = marketingNotificationEmails
        self.postalCode = postalCode
        self.preferredLanguage = preferredLanguage
        self.privacyProfile = privacyProfile
        self.provisionedPlans = provisionedPlans
        self.provisioningErrors = provisioningErrors
        self.releaseTrack = releaseTrack
        self.replicationScope = replicationScope
        self.securityComplianceNotificationMails = securityComplianceNotificationMails
        self.securityComplianceNotificationPhones = securityComplianceNotificationPhones
        self.selfServePasswordResetPolicy = selfServePasswordResetPolicy
        self.state = state
        self.street = street
        self.technicalNotificationMails = technicalNotificationMails
        self.telephoneNumber = telephoneNumber
        self.tenantType = tenantType
        self.createdDateTime = createdDateTime
        self.verifiedDomains = verifiedDomains
        self.windowsCredentialsEncryptionCertificate = windowsCredentialsEncryptionCertificate

    def __repr__(self):
        return f"<TenantDetail {self.displayName or self.objectId}>"