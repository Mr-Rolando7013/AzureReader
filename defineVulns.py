import json
from collections import defaultdict, deque
from locateADVulnerabilities import *

computers_file = 'bloodhound/20260407101035_computers.json'
containers_file = 'bloodhound/20260407101035_containers.json'
domains_file = 'bloodhound/20260407101035_domains.json'
gpos_file = 'bloodhound/20260407101035_gpos.json'
groups_file = 'bloodhound/20260407101035_groups.json'
ous_file = 'bloodhound/20260407101035_ous.json'
users_file = 'bloodhound/20260407101035_users.json'

TIER0_GROUPS = ["DOMAIN ADMINS", "ENTERPRISE ADMINS", "ADMINISTRATORS"]
TIER1_GROUPS = [
    "ACCOUNT OPERATORS",
    "BACKUP OPERATORS",
    "SERVER OPERATORS",
    "PRINT OPERATORS"
]

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


def get_dc_nodes(nodes):
    return {
        node for node, props in nodes.items()
        if props.get("isDomainController") is True
    }

def build_attack_graph(data, dangerous_privs, permissions_baseline, userClassificationFile):
    reverse_graph = defaultdict(list)
    nodes = {}
    edges = []

    with open(userClassificationFile, 'r') as f:
        user_data = json.load(f)


    for obj in data:
        properties = obj.get("Properties", {})
        target = properties.get("name")

        if not target:
            continue

        target_norm = target.split("@")[0].upper()

        # ensure node exists
        nodes.setdefault(target_norm, {"isDomainController": False})

        # detect DC properly from metadata
        if properties.get("primaryGroupID") == 516:
            nodes[target_norm]["isDomainController"] = True

        if "DOMAIN CONTROLLERS" in properties.get("memberOf", []):
            nodes[target_norm]["isDomainController"] = True

        if "DC" in target_norm:
            nodes[target_norm]["isDomainController"] = True

        aces = obj.get("Aces", [])

        for ace in aces:
            right = ace.get("RightName")
            if right not in dangerous_privs:
                continue

            principal = retrieveNameFromSid(ace.get("PrincipalSID", ""))
            if not principal:
                continue

            principal_norm = principal.split("@")[0].upper()

            # ensure node exists
            nodes.setdefault(principal_norm, {"isDomainController": False})

            # base score
            score = permissions_baseline.get(right, 0)

            # enrichment score
            for obj in user_data:
                if obj["User"] == target_norm:
                    score += obj["Score"]
            

            edge = {
                "from": principal_norm,
                "to": target_norm,
                "type": right,
                "score": score
            }

            edges.append(edge)
            reverse_graph[target_norm].append(principal_norm)

    return edges, reverse_graph, nodes

def bfs_with_paths(sources, reverse_graph, edges):
    # build quick lookup: (from, to) → edge
    edge_lookup = defaultdict(list)
    for e in edges:
        edge_lookup[(e["from"], e["to"])].append(e)

    queue = deque(sources)
    visited = {s: 0 for s in sources}
    parent = {s: None for s in sources}

    while queue:
        node = queue.popleft()

        for neighbor in reverse_graph.get(node, []):
            if neighbor not in visited:
                visited[neighbor] = visited[node] + 1

                edge = edge_lookup.get((neighbor, node))  # important: reversed direction
                parent[neighbor] = {
                    "prev": node,
                    "edge": edge
                }

                queue.append(neighbor)

    return visited, parent

def reconstruct_path_with_edges(node, parent):
    path = []

    while node in parent and parent[node] is not None:
        entry = parent[node]

        edge = entry["edge"]

        # handle list vs dict
        if isinstance(edge, list):
            edge = edge[0] if edge else None

        path.append({
            "node": node,
            "edge_type": edge["type"] if edge else None
        })

        node = entry["prev"]

    path.append({"node": node, "edge_type": None})
    return list(reversed(path))

if __name__ == "__main__":

    dangerousPrivs = [
        "GenericAll", "GenericWrite", "WriteProperty", "WriteSPN",
        "Validated-SPN", "Self", "AllExtendedRights", "Self-Membership",
        "User-Force-Change-Password", "ForceChangePassword",
        "ReadLAPSPassword", "ReadGMSAPassword", "Owns", "WriteDacl", 
        "AddMember", "WriteOwner"
    ]

    permissions_baseline = {
        "GenericAll": 2.5,
        "GenericWrite": 2.0,
        "WriteDacl": 1.8,
        "WriteSPN": 2.2
    }

    files = [
        computers_file,
        containers_file,
        users_file,
        ous_file,
        groups_file,
        gpos_file,
        domains_file
    ]

    data = []
    for file in files:
        with open(file, "r") as f:
            content = json.load(f)
            data.extend(content.get("data", []))

   
    edges, reverse_graph, nodes = build_attack_graph(
        data,
        dangerousPrivs,
        permissions_baseline,
        "userClassification.json"
    )

    dc_nodes = get_dc_nodes(nodes)

    distances, parent = bfs_with_paths(dc_nodes, reverse_graph, edges)
    #print("Edges: ", edges)

    hops_baseline = {
        1: 2.5,
        2: 1.8,
        3: 1.2
    }
    for edge in edges:
        node = edge["from"]  # attacker side

        hops = distances.get(node)

        if hops is None:
            continue  # unreachable from DC

        hop_weight = hops_baseline.get(hops, 0)

        # combine them
        edge["score"] = edge["score"] * hop_weight


    for node, hops in distances.items():
        path = reconstruct_path_with_edges(node, parent)

        formatted = []
        for step in path:
            if step["edge_type"]:
                formatted.append(f"--[{step['edge_type']}]--> {step['node']}")
            else:
                formatted.append(step["node"])

        print(f"{node}: {hops} hops -> " + " ".join(formatted))
    print("Max hops:", max(distances.values()))

    edges_sorted = sorted(
        edges,
        key=lambda e: e.get("score", 0),
        reverse=True
    )
    print("Edges: ", edges_sorted)
    