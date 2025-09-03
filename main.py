from flask import Flask, render_template, request, jsonify, url_for, redirect
import sqlalchemy as db
import networkx as nx
import matplotlib.pyplot as plt
from directoryRole import DirectoryRole
from user import User
from roleAssignments import RoleAssignments
from roleDefinitions import RoleDefinitions
from administrativeUnits import AdministrativeUnits
from werkzeug.utils import secure_filename

from pyvis.network import Network
import os
import requests
import json

ALLOWED_EXTENSIONS = {'db',}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def getResourceScopesIds(resourceScopes):
    if resourceScopes:
        try:
            scopes = json.loads(resourceScopes)
        except json.JSONDecodeError:
            scopes = [resourceScopes]

        scope_ids = [scope.split('/')[-1] if scope != "/" else "tenant" for scope in scopes if scope]
        return scope_ids
    return []

def getPrincipals(filename, user):
    current_path = os.getcwd()
    db_file = "sqlite:///" + current_path + "\\uploads\\" + filename
    engine = db.create_engine(db_file)
    connection = engine.connect()
    metadata = db.MetaData()
    metadata.reflect(bind=engine)
    role_assignments_data = metadata.tables['RoleAssignments']
    role_definitions_data = metadata.tables['RoleDefinitions']
    database_user_data = metadata.tables['Users']

    stmt_user = db.select(database_user_data)
    user_results = connection.execute(stmt_user).fetchall()

    users = [User(*row) for row in user_results]

    user_lookup = {u.objectId: u for u in users}

    stmt_role_assignments = db.select(role_assignments_data)
    role_assignments_results = connection.execute(stmt_role_assignments).fetchall()
    role_assignments_list = [RoleAssignments(*row) for row in role_assignments_results]

    stmt_role_definitions = db.select(role_definitions_data)
    role_definitions_results = connection.execute(stmt_role_definitions).fetchall()
    role_definitions_list = [RoleDefinitions(*row) for row in role_definitions_results]
    role_lookup = {rd.objectId: rd for rd in role_definitions_list}
    role_names = {}
    user_roles = {}

    # ToDo
    administrative_units_data = metadata.tables['AdministrativeUnits']
    
    for ra in role_assignments_list:
        scoped_users = []
        user = user_lookup.get(ra.principalId)
        role_definition = role_lookup.get(ra.roleDefinitionId)
        scope_ids = getResourceScopesIds(ra.resourceScopes)
        #print(" Scope IDs: ", scope_ids)
        for scope in scope_ids:
            if scope == "tenant":
                pass
            else:
                scoped_users.append(user_lookup.get(scope))
                print(" Scope user: ", scoped_users)
        if user:
            user_roles.setdefault(user, []).append(ra)
        if role_definition:
            role_names.setdefault(role_definition, []).append(ra)
    
    for user, roles in user_roles.items():
        print(f"USER: {user.displayName} ({user.objectId})")
        for ra in roles:
            for name in role_names:
                if ra in role_names[name]:
                    print("   ROLE:", name.displayName, name.description, ra.resourceScopes, ra.roleDefinitionId)
            for scoped_user in scoped_users:
                # print("   SCOPE USER:", scoped_user.displayName if scoped_user else "Unknown", ra.resourceScopes)
                pass

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
    
    

def generate_graph(data=None):
    print("DATAAAA: ", data)
    if data == None:
        pass
    else:
        print("DATAAAA: ", data)
        user = data['user']
        filename = data['filename']
        fTableResults, directoryRoleresults, userResults = readTable(filename, user)
        # Delete later
        getPrincipals(filename, user)
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


    


def check_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/update-graph', methods=['POST'])
def update_graph():
    user = request.json.get("user")
    filename = request.json.get("filename")
    data = {
        "user" : user,
        "filename" : filename
    }
    print("DATAAAA: ", data)
    generate_graph(data)
    return jsonify({"success" : True})

@app.route('/submit-users', methods=['POST'])
def submit_users():
    data = request.get_json()
    print("Received:", data)
    return jsonify({'status': 'success'})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    print("File name: ", file.filename)
    if file and check_extension(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if filename.rsplit('.', 1)[1].lower() == 'db':
            try:
                # Generate full URL to the 'process' route
                #process_url = url_for('graph', filename=file.filename, _external=True)

                # Make HTTP request to the other endpoint
                #response = requests.get(process_url)

                # Process the data as needed
                return redirect(url_for('graph', filename=file.filename))
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"message": "File uploaded successfully."}), 201
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/graph/<filename>')
def graph(filename):
    current_path = os.getcwd()
    db_file = "sqlite:///" + current_path + "\\uploads\\" + filename
    engine = db.create_engine(db_file)
    connection = engine.connect()
    metadata = db.MetaData()

    metadata.reflect(bind=engine)
    database_user_data = metadata.tables['Users']
    stmt_user = db.select(database_user_data)
    user_results = connection.execute(stmt_user).fetchall()
    user_list = []
    user_id_list = {}

    for data_tuple in user_results:
        tempUser = User(*data_tuple)
        user_id_list[tempUser.objectId] = tempUser
        user_list.append(tempUser)

    
    path_list = ["1", "2", "3"]


    return render_template("graph.html", user_list=user_list, path_list=path_list, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)

