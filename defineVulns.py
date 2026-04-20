
from locateADVulnerabilities import *
import json

permissions_baseline = {
  "GenericAll": 1.0,
  "WriteDACL": 0.95,
  "WriteOwner": 0.93,
  "GenericWrite": 0.8,
  "AllExtendedRights": 0.78,

  "AddMember": 0.85,
  "ForceChangePassword": 0.88,
  "ResetPassword": 0.88,

  "WriteSPN": 0.82,
  "WriteAccountRestrictions": 0.75,
  "WriteUserAccountControl": 0.83,

  "AddAllowedToAct": 0.9,
  "AllowedToAct": 0.9,

  "DCSync": 1.0,
  "GetChanges": 0.92,
  "GetChangesAll": 0.95,

  "AdminTo": 0.9,
  "ExecuteDCOM": 0.7,
  "CanRDP": 0.65,
  "CanPSRemote": 0.7,

  "WriteKeyCredentialLink": 0.9,

  "Owns": 0.85,
  "Contains": 0.4,

  "ReadLAPSPassword": 0.85,
  "ReadGMSAPassword": 0.9,

  "HasSPN": 0.6,
  "HasSession": 0.7,

  "Read": 0.1,
  "Write": 0.5
}

users_baseline = {
    "domainAdmin":2,
    "privilegedUser":1.8,
    "normalUser":1
}

TIER0_GROUPS = [
    "DOMAIN ADMINS",
    "ENTERPRISE ADMINS",
    "ADMINISTRATORS"
]

TIER1_GROUPS = [
    "ACCOUNT OPERATORS",
    "BACKUP OPERATORS",
    "SERVER OPERATORS",
    "PRINT OPERATORS"
]

users_file = 'bloodhound/20260407101035_users.json'
groups_file = 'bloodhound/20260407101035_groups.json'

hops_baseline = {
    "one_hop":2.5,
    "two_hops": 1.8,
    "three_hops":1.2
}

def exportMemberships():
    with open(groups_file, 'r') as f:
        data = json.load(f)
    result = []
    outputFile = "groupMembers.json"

    for group in data.get("data", []):
        property = group.get("Properties", [])
        tempGroup = property.get("name", "").split("@")[0].upper()
        for member in group.get("Members", []):
            tempMember = retrieveNameFromSid(member["ObjectIdentifier"]).split("@")[0].upper()
            tempType = member["ObjectType"]
            result.append({
                "group": tempGroup,
                "member": tempMember,
                "type": tempType
            })

    with open(outputFile, 'w') as f:
        json.dump(result, f, indent=2)

def define_users():
    outputFile = "userClassification.json"
    result = {}

    with open('groupMembers.json', 'r') as f:
        data = json.load(f)

    for value in data:
        if value["type"] == 'User':
            user = value["member"]

            if value["group"] in TIER0_GROUPS:
                score = 2
            elif value["group"] in TIER1_GROUPS:
                score = 1.8
            else:
                score = 1
            if user in result:
                result[user] = max(result[user], score)
            else:
                result[user] = score

    output_list = [
        {"User": user, "Score": score}
        for user, score in result.items()
    ]

    with open(outputFile, 'w') as f:
        json.dump(output_list, f, indent=2)

    

def definePermissionsBaseline(data):
    for value in data:
        perm = value.get("permission")

        if perm in permissions_baseline:
            value["score"] = permissions_baseline[perm]
        else:
            value["score"] = 0.2

    return data

if __name__ == '__main__':
    define_users()