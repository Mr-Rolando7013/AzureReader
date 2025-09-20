import sqlalchemy as db
from user import User
from roleAssignments import RoleAssignments
from roleDefinitions import RoleDefinitions
from administrativeUnits import AdministrativeUnits
from lnk_au_member_user import Lnk_au_member_user
from directoryRole import DirectoryRole

import networkx as nx
from pyvis.network import Network

import os
import json

def getResourceScopesIds(resourceScopes):
    if resourceScopes:
        try:
            scopes = json.loads(resourceScopes)
        except json.JSONDecodeError:
            scopes = [resourceScopes]

        scope_ids = [scope.split('/')[-1] if scope != "/" else "tenant" for scope in scopes if scope]
        return scope_ids
    return []

def readTable(filename, user):
    current_path = os.getcwd()
    db_file = "sqlite:///" + current_path + "\\uploads\\" + filename
    engine = db.create_engine(db_file)
    connection = engine.connect()
    metadata = db.MetaData()
    metadata.reflect(bind=engine)
    lnk_table = metadata.tables['lnk_role_member_user']
    directory_roles_data = metadata.tables['DirectoryRoles']
    database_user_data = metadata.tables['Users']

    stmt = db.select(lnk_table.c.DirectoryRole, lnk_table.c.User)
    results = connection.execute(stmt).fetchall()

    stmt_directory_roles = db.select(directory_roles_data)
    directory_results = connection.execute(stmt_directory_roles).fetchall()
    directory_roles_list = []
    directory_roles_id_list = {}

    stmt_user = db.select(database_user_data)
    user_results = connection.execute(stmt_user).fetchall()
    user_list = []
    user_id_list = {}

    for data_tuple in directory_results:
        tempDirectory = DirectoryRole(*data_tuple)
        directory_roles_id_list[tempDirectory.objectId] = tempDirectory
    
    for data_tuple in user_results:
        tempUser = User(*data_tuple)
        if tempUser.userPrincipalName == user:
            user_list.append(tempUser)

    return results, directory_roles_id_list, user_list

def readTableWithRole(filename, roleName):
    current_path = os.getcwd()
    db_file = "sqlite:///" + current_path + "\\uploads\\" + filename
    engine = db.create_engine(db_file)
    connection = engine.connect()
    metadata = db.MetaData()
    metadata.reflect(bind=engine)
    # Get all role data from tables
    role_assignments_data = metadata.tables['RoleAssignments']
    role_definitions_data = metadata.tables['RoleDefinitions']
    # Get all user data from db
    database_user_data = metadata.tables['Users']
    # This one is the link between the AU and the users.
    lnk_au_member_user = metadata.tables['lnk_au_member_user']
    administrative_units_data = metadata.tables['AdministrativeUnits']

    #Get all AU data from db
    stmt_lnk_au = db.select(lnk_au_member_user)
    lnk_au_results = connection.execute(stmt_lnk_au).fetchall()
    lnk_au_list = [Lnk_au_member_user(*row) for row in lnk_au_results]
    user_au_lookup = {u.administrativeUnit: u for u in lnk_au_list}

    #print("USER_AU_LOOKUP: ", user_au_lookup)

    # Get al user data from db
    stmt_user = db.select(database_user_data)
    user_results = connection.execute(stmt_user).fetchall()

    # Save user data into list of user objects and then save it to a dictionary for easy lookup
    users = [User(*row) for row in user_results]
    user_lookup = {u.objectId: u for u in users}

    stmt_role_assignments = db.select(role_assignments_data)
    role_assignments_results = connection.execute(stmt_role_assignments).fetchall()
    role_assignments_list = [RoleAssignments(*row) for row in role_assignments_results]

    stmt_role_definitions = db.select(role_definitions_data)
    role_definitions_results = connection.execute(stmt_role_definitions).fetchall()
    role_definitions_list = [RoleDefinitions(*row) for row in role_definitions_results]
    role_lookup = {rd.objectId: rd for rd in role_definitions_list if rd.displayName == roleName}

    return user_au_lookup, administrative_units_data, lnk_au_member_user, user_lookup, role_lookup, role_assignments_list

def getDataFromRole(filename, roleName):
    user_au_lookup, administrative_units_data, lnk_au_member_user, user_lookup, role_lookup, role_assignments_list = readTableWithRole(filename, roleName)
    # Dictionaries to hold role names and user-role mappings
    role_names = {}
    user_roles = {}
    roleOutput = []
    userOutput = []
    scopedUsersOutput = []
    
    # Loop through role assignments to map users to roles and scopes
    for ra in role_assignments_list:
        scoped_users = ""
        user = user_lookup.get(ra.principalId)
        role_definition = role_lookup.get(ra.roleDefinitionId)
        
        # Map users to their roles
        if user:
            user_roles.setdefault(user, []).append(ra)
        if role_definition:
            role_names.setdefault(role_definition, []).append(ra)
    
    for user, roles in user_roles.items():
        print(f"USER: {user.displayName} ({user.objectId})")
        userOutput.append(user)
        for ra in roles:
            for name in role_names:
                if ra in role_names[name]:
                    print("   ROLE:", name.displayName, name.description, ra.resourceScopes, ra.roleDefinitionId)
                    roleOutput.append(name)
            # Find scoped users based on scope IDs.
            scope_ids = getResourceScopesIds(ra.resourceScopes)
            for scope in scope_ids:
                if scope == "tenant":
                    pass
                else:
                    scoped_user1 = user_au_lookup.get(scope)
                    if scoped_user1:
                        scoped_users = (user_lookup.get(scoped_user1.user))
                    scopedUsersOutput.append(scoped_users)
                    print("   SCOPE USER:", scoped_users.displayName if scoped_users else "Unknown", ra.resourceScopes)
    return roleOutput, scopedUsersOutput, userOutput



def generate_graph(data=None):
    if data == None:
        pass
    else:
        user = data['user']
        filename = data['filename']
        fTableResults, directoryRoleresults, userResults = readTable(filename, user)
        # Delete later
        #getDataFromRole(filename, user)
        G = nx.DiGraph()
        user_obj = userResults[0]
        user_node_id = f"user_{user_obj.userPrincipalName}"
        G.add_node(f"{user_node_id}", type="user" ,data=user_obj)
        net = Network(height="100vh ", width="100%", bgcolor="#ffffff", font_color="black")
        # Add only related roles from the linking table
        for role_id, user_id in fTableResults:
            if user_id == user_obj.objectId and role_id in directoryRoleresults:
                role_obj = directoryRoleresults[role_id]
                role_node_id = f"role_{role_obj.displayName}"

                # Add role node if not already added
                if role_node_id not in G:
                    G.add_node(role_node_id, type="role", data=role_obj)

                # Add edge: user → role
                G.add_edge(user_node_id, role_node_id)
        
        for node in G.nodes():
            net.add_node(node, label=str(node))  # You can customize label to show useful info

        # Add edges
        for source, target in G.edges():
            net.add_edge(source, target)
        net.from_nx(G)
        static_path = os.path.join(os.path.dirname(__file__), "static")
        os.makedirs(static_path, exist_ok=True)
        net.save_graph(os.path.join(static_path, "graph.html"))

def generate_graph_with_role(data=None):
    if data == None:
        pass
    else:
        role = data['role']
        filename = data['filename']
        roleOutput, scopedUsersOutput, userOutput = getDataFromRole(filename, role)
        print("OUTPUTTTTTTT: ", roleOutput, scopedUsersOutput, userOutput)
        G = nx.DiGraph()
        for user, role, scope_user in zip(userOutput, roleOutput, scopedUsersOutput):
            print("JIJIJIJI: ", user.userPrincipalName, role.displayName, scope_user.userPrincipalName)
            G.add_node(f"user_{user.userPrincipalName}", type="user", data=user)
            G.add_node(f"role_{role.displayName}", type="role", data=role)
            G.add_node(f"scope_user_{scope_user.userPrincipalName}", type="scope_user", data=scope_user) if scope_user else None

            G.add_edge(user, role, relation="has_role")
            G.add_edge(role, scope_user, relation="scoped_to") if scope_user else None

            
        net = Network(height="100vh ", width="100%", bgcolor="#ffffff", font_color="black")
        net.from_nx(G)
        static_path = os.path.join(os.path.dirname(__file__), "static")
        os.makedirs(static_path, exist_ok=True)
        net.save_graph(os.path.join(static_path, "graph.html"))

