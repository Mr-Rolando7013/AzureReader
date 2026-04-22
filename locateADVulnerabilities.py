import json

def loadSIDs(json_computers_file, json_containers_file,
             json_domains_file, json_gpos_file,
             json_groups_file, json_ous_file, json_users_file):
    outputFile = "sids.json"
    
    #Computers
    with open(json_computers_file, 'r') as f:
        data = json.load(f)
    
    computer_output = []

    for obj in data.get("data", []):
        sid = obj.get("ObjectIdentifier")
        property = obj.get("Properties", {})
        name = property.get("name")

        computer_output.append({
            'sid': sid,
            'name': name
        })

    # Containers
    with open(json_containers_file, 'r') as f:
        data = json.load(f)
    
    container_output = []

    for obj in data.get("data", []):
        sid = obj.get("ObjectIdentifier")
        property = obj.get("Properties", {})
        name = property.get("name")

        container_output.append({
            'sid': sid,
            'name': name
        })

    # Domains
    with open(json_domains_file, 'r') as f:
        data = json.load(f)
    
    domains_output = []

    for obj in data.get("data", []):
        sid = obj.get("ObjectIdentifier")
        property = obj.get("Properties", {})
        name = property.get("name")

        domains_output.append({
            'sid': sid,
            'name': name
        })

    # GPOS
    with open(json_gpos_file, 'r') as f:
        data = json.load(f)
    
    gpos_output = []

    for obj in data.get("data", []):
        sid = obj.get("ObjectIdentifier")
        property = obj.get("Properties", {})
        name = property.get("name")

        gpos_output.append({
            'sid': sid,
            'name': name
        })

    # Groups
    with open(json_groups_file, 'r') as f:
        data = json.load(f)
    
    groups_output = []

    for obj in data.get("data", []):
        sid = obj.get("ObjectIdentifier")
        property = obj.get("Properties", {})
        name = property.get("name")

        groups_output.append({
            'sid': sid,
            'name': name
        })

    # OUs
    with open(json_ous_file, 'r') as f:
        data = json.load(f)
    
    ous_output = []

    for obj in data.get("data", []):
        sid = obj.get("ObjectIdentifier")
        property = obj.get("Properties", {})
        name = property.get("name")

        ous_output.append({
            'sid': sid,
            'name': name
        })

    # Users
    with open(json_users_file, 'r') as f:
        data = json.load(f)
    
    users_output = []

    for obj in data.get("data", []):
        sid = obj.get("ObjectIdentifier")
        property = obj.get("Properties", {})
        name = property.get("name")

        users_output.append({
            'sid': sid,
            'name': name
        })

    merged_output = {
        "computers": computer_output,
        "containers": container_output,
        "domains": domains_output,
        "gpos": gpos_output,
        "groups": groups_output,
        "ous": ous_output,
        "users": users_output
    }

    with open(outputFile, 'w') as f:
        json.dump(merged_output, f, indent=2)

def retrieveNameFromSid(sid):
    sid_file = "sids.json"
    if sid == "":
        return ""

    with open(sid_file, 'r') as f:
        data = json.load(f)

    computers = data["computers"]
    for computer in computers:
        if computer["sid"] == sid:
            return computer["name"]
        
    containers = data["containers"]
    for container in containers:
        if container["sid"] == sid:
            return container["name"]
        
    domains = data["domains"]
    for domain in domains:
        if domain["sid"] == sid:
            return domain["name"]
        
    gpos = data["gpos"]
    for gpo in gpos:
        if gpo["sid"] == sid:
            return gpo["name"]
        
    groups = data["groups"]
    for group in groups:
        if group["sid"] == sid:
            return group["name"]
        
    ous = data["ous"]
    for ou in ous:
        if ou["sid"] == sid:
            return ou["name"]
    
    users = data["users"]
    for user in users:
        if user["sid"] == sid:
            return user["name"]
        
    return sid

def identifyKerberoastableAccounts(json_users_file):
    with open(json_users_file, 'r') as f:
        data = json.load(f)

    kerberoastable_users = []
    for user in data.get("data", []):
        property = user.get("Properties", [])
        spn = property.get("serviceprincipalnames", [])
        enabled = property.get("enabled", False)

        if enabled and spn:
            kerberoastable_users.append({
                'attackName': 'kerberoasting',
                "name": property.get("name"),
                "spns": property
            })

    return kerberoastable_users

def identifyAsRepRoast(json_users_file):
    with open(json_users_file, 'r') as f:
        data = json.load(f)

    asrepRoastUsers = []

    for user in data.get("data", []):
        property = user.get("Properties", [])
        preauth = property.get("dontreqpreauth", False)

        if preauth:
            asrepRoastUsers.append({
                'attackName': 'asRepRoasting',
                'name': property.get("name"),
                'spns': property
            })

    return asrepRoastUsers

def retrieveDACLs(files):
    data = []

    for file in files:
        with open(file, 'r') as f:
            content = json.load(f)
            data.extend(content.get("data", []))

    return data

"""
def retrieveDACLs(files):
    data = []
    dangerousPrivs = ["GenericAll", "GenericWrite", "WriteProperty", "WriteSPN", "Validated-SPN",
                      "Self", "AllExtendedRights", "Self-Membership", "User-Force-Change-Password",
                      "ForceChangePassword", "ReadLAPSPassword", "ReadGMSAPassword", "Owns", "WriteDacl"]
    for file in files:
        with open(file, 'r') as f:
            content = json.load(f)
            data.extend(content.get("data", []))

    dacls = []
    for user in data:
        property = user.get("Properties", [])
        dc_nodes = {
            node for node, props in nodes.items()
            if props.get("isDomainController") is True
        }
        aces = user.get("Aces", [])
        for right in aces:
            name = right.get("RightName", False)
            if name in dangerousPrivs:
                potentialAttacker = retrieveNameFromSid(right.get("PrincipalSID", ""))
                dacls.append({
                    'attackName':'targetedKerberoast',
                    'permission': name,
                    'target': property.get("name").split("@")[0].upper(),
                    'principal_type': right.get("PrincipalType", ''),
                    'principal': potentialAttacker.split("@")[0].upper()

                })

    return dacls
"""
    

def exportData(data):
    finalJson = []
    i = 1
    for value in data:
        temp = {}
        graphConditions = []
        riskModifiers = []
        temp2 = {}
        temp3 = {}
        temp["attack_id"] = f"AD-{i}"
        temp["name"] = value["attackName"]
        
        i+=1

if __name__ == '__main__':
    computers_file = 'bloodhound/20260407101035_computers.json'
    containers_file = 'bloodhound/20260407101035_containers.json'
    domains_file = 'bloodhound/20260407101035_domains.json'
    gpos_file = 'bloodhound/20260407101035_gpos.json'
    groups_file = 'bloodhound/20260407101035_groups.json'
    ous_file = 'bloodhound/20260407101035_ous.json'
    users_file = 'bloodhound/20260407101035_users.json'
    
    #print(identifyKerberoastableAccounts(file_name))
    #print(identifyAsRepRoast(file_name))
    #print(identifyTargetedKerberoast(file_name))
    data = identifyAddMember(users_file)
    print(data)
    exportData(data)
    #loadSIDs(computers_file, containers_file,
             #domains_file, gpos_file, groups_file,
             #ous_file, users_file)

