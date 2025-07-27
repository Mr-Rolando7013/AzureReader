class Devices:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 accountEnabled=False, alternativeSecurityIds=None,
                 approximateLastLogonTimestamp=None, bitLockerKey=None,
                 capabilities=None, complianceExpiryTime=None,
                 compliantApplications=None, compliantAppsManagementAppId=None,
                 deviceCategory=None, deviceId=None, deviceKey=None,
                 deviceManufacturer=None, deviceManagementAppId=None,
                 deviceMetadata=None, deviceModel=None, deviceObjectVersion=None,
                 deviceOSType=None, deviceOSVersion=None, deviceOwnership=None,
                 devicePhysicalIds=None, deviceSystemMetadata=None,
                 deviceTrustType=None, dirSyncEnabled=False, displayName=None,
                 domainName=None, enrollmentProfileName=None, enrollmentType=None,
                 exchangeActiveSyncId=None, externalSourceName=None, hostnames=None,
                 isCompliant=False, isManaged=False, isRooted=False,
                 keyCredentials=None, lastDirSyncTime=None, localCredentials=None,
                 managementType=None, onPremisesSecurityIdentifier=None,
                 organizationalUnit=None, profileType=None, reserved1=None,
                 sourceType=None, systemLabels=None):

        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.accountEnabled = accountEnabled
        self.alternativeSecurityIds = alternativeSecurityIds
        self.approximateLastLogonTimestamp = approximateLastLogonTimestamp
        self.bitLockerKey = bitLockerKey
        self.capabilities = capabilities
        self.complianceExpiryTime = complianceExpiryTime
        self.compliantApplications = compliantApplications
        self.compliantAppsManagementAppId = compliantAppsManagementAppId
        self.deviceCategory = deviceCategory
        self.deviceId = deviceId
        self.deviceKey = deviceKey
        self.deviceManufacturer = deviceManufacturer
        self.deviceManagementAppId = deviceManagementAppId
        self.deviceMetadata = deviceMetadata
        self.deviceModel = deviceModel
        self.deviceObjectVersion = deviceObjectVersion
        self.deviceOSType = deviceOSType
        self.deviceOSVersion = deviceOSVersion
        self.deviceOwnership = deviceOwnership
        self.devicePhysicalIds = devicePhysicalIds
        self.deviceSystemMetadata = deviceSystemMetadata
        self.deviceTrustType = deviceTrustType
        self.dirSyncEnabled = dirSyncEnabled
        self.displayName = displayName
        self.domainName = domainName
        self.enrollmentProfileName = enrollmentProfileName
        self.enrollmentType = enrollmentType
        self.exchangeActiveSyncId = exchangeActiveSyncId
        self.externalSourceName = externalSourceName
        self.hostnames = hostnames
        self.isCompliant = isCompliant
        self.isManaged = isManaged
        self.isRooted = isRooted
        self.keyCredentials = keyCredentials
        self.lastDirSyncTime = lastDirSyncTime
        self.localCredentials = localCredentials
        self.managementType = managementType
        self.onPremisesSecurityIdentifier = onPremisesSecurityIdentifier
        self.organizationalUnit = organizationalUnit
        self.profileType = profileType
        self.reserved1 = reserved1
        self.sourceType = sourceType
        self.systemLabels = systemLabels

    def __repr__(self):
        return f"<Device {self.displayName or self.deviceId or self.objectId}>"