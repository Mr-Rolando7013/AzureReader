class Contacts:
    def __init__(self, objectType=None, objectId=None, deletionTimestamp=None,
                 city=None, cloudAudioConferencingProviderInfo=None,
                 cloudMSRtcIsSipEnabled=False, cloudMSRtcOwnerUrn=None,
                 cloudMSRtcPolicyAssignments=None, cloudMSRtcPool=None,
                 cloudMSRtcServiceAttributes=None, cloudRtcUserPolicies=None,
                 cloudSipLine=None, companyName=None, country=None,
                 department=None, dirSyncEnabled=False, displayName=None,
                 facsimileTelephoneNumber=None, givenName=None, jobTitle=None,
                 lastDirSyncTime=None, mail=None, mailNickname=None, mobile=None,
                 onPremisesObjectIdentifier=None, physicalDeliveryOfficeName=None,
                 postalCode=None, provisioningErrors=None, proxyAddresses=None,
                 sipProxyAddress=None, state=None, streetAddress=None,
                 surname=None, telephoneNumber=None, thumbnailPhoto=None):

        self.objectType = objectType
        self.objectId = objectId  # Required (NOT NULL)
        self.deletionTimestamp = deletionTimestamp
        self.city = city
        self.cloudAudioConferencingProviderInfo = cloudAudioConferencingProviderInfo
        self.cloudMSRtcIsSipEnabled = cloudMSRtcIsSipEnabled
        self.cloudMSRtcOwnerUrn = cloudMSRtcOwnerUrn
        self.cloudMSRtcPolicyAssignments = cloudMSRtcPolicyAssignments
        self.cloudMSRtcPool = cloudMSRtcPool
        self.cloudMSRtcServiceAttributes = cloudMSRtcServiceAttributes
        self.cloudRtcUserPolicies = cloudRtcUserPolicies
        self.cloudSipLine = cloudSipLine
        self.companyName = companyName
        self.country = country
        self.department = department
        self.dirSyncEnabled = dirSyncEnabled
        self.displayName = displayName
        self.facsimileTelephoneNumber = facsimileTelephoneNumber
        self.givenName = givenName
        self.jobTitle = jobTitle
        self.lastDirSyncTime = lastDirSyncTime
        self.mail = mail
        self.mailNickname = mailNickname
        self.mobile = mobile
        self.onPremisesObjectIdentifier = onPremisesObjectIdentifier
        self.physicalDeliveryOfficeName = physicalDeliveryOfficeName
        self.postalCode = postalCode
        self.provisioningErrors = provisioningErrors
        self.proxyAddresses = proxyAddresses
        self.sipProxyAddress = sipProxyAddress
        self.state = state
        self.streetAddress = streetAddress
        self.surname = surname
        self.telephoneNumber = telephoneNumber
        self.thumbnailPhoto = thumbnailPhoto

    def __repr__(self):
        return f"<Contact {self.displayName or self.mail or self.objectId}>"