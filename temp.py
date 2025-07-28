from flask import Flask, render_template, request, jsonify, url_for, redirect
import sqlalchemy as db
import networkx as nx
import matplotlib.pyplot as plt
from directoryRole import DirectoryRole
from user import User
from werkzeug.utils import secure_filename

from pyvis.network import Network
import os
import requests

ALLOWED_EXTENSIONS = {'db',}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def check_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("main.html")

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
    print("DB FILE: ", db_file)
    #engine = db.create_engine(r'sqlite:///C:\\Users\\Optiplex 3080\\Desktop\\PythonProjects\\AzureReader\\roadrecon.db')
    engine = db.create_engine(db_file)
    connection = engine.connect()
    metadata = db.MetaData()
    # I think that I dont need this one.
    #users = db.Table('users', metadata, autoload_with=engine)
    #print(users.columns.keys())
    inspector = db.inspect(engine)
    table_names = inspector.get_table_names()

    #print(table_names)

    user_foreign_keys = inspector.get_foreign_keys('lnk_role_member_user')

    #print("------")
    #print(user_foreign_keys)

    metadata.reflect(bind=engine)
    lnk_table = metadata.tables['lnk_role_member_user']
    directory_roles_data = metadata.tables['DirectoryRoles']
    database_user_data = metadata.tables['Users']
    administrative_units_data = metadata.tables['AdministrativeUnits']
    app_role_assignments_data = metadata.tables['AppRoleAssignments']
    application_refs_data = metadata.tables['ApplicationRefs']
    application_data = metadata.tables['Applications']
    authorization_policys_data = metadata.tables['AuthorizationPolicys']
    contacts_data = metadata.tables['Contacts']
    devices_data = metadata.tables['Devices']
    directory_settings_data = metadata.tables['DirectorySettings']
    eligible_role_assignments_data = metadata.tables['EligibleRoleAssignments']
    extension_propertys_data = metadata.tables['ExtensionPropertys']
    groups_data = metadata.tables['Groups']
    oauth2_permission_grants_data = metadata.tables['OAuth2PermissionGrants']
    policys_data = metadata.tables['Policys']
    role_assignments_data = metadata.tables['RoleAssignments']
    role_definitions_data = metadata.tables['RoleDefinitions']
    service_principal_data = metadata.tables['ServicePrincipals']
    tenant_details_data = metadata.tables['TenantDetails']
    lnk_application_owner_serviceprincipal_data = metadata.tables['lnk_application_owner_serviceprincipal']
    lnk_application_owner_user_data = metadata.tables['lnk_application_owner_user']
    lnk_au_member_device_data = metadata.tables['lnk_au_member_device']
    lnk_au_member_group_data = metadata.tables['lnk_au_member_group']
    lnk_au_member_user_data = metadata.tables['lnk_au_member_user']
    lnk_device_owner_data = metadata.tables['lnk_device_owner']
    lnk_group_member_contact_data = metadata.tables['lnk_group_member_contact']
    lnk_group_member_device_data = metadata.tables['lnk_group_member_device']
    lnk_group_member_group_data = metadata.tables['lnk_group_member_group']
    lnk_group_member_serviceprincipal_data = metadata.tables['lnk_group_member_serviceprincipal']
    lnk_group_member_user_data = metadata.tables['lnk_group_member_user']
    lnk_group_owner_serviceprincipal_data = metadata.tables['lnk_group_owner_serviceprincipal']
    lnk_group_owner_user_data = metadata.tables['lnk_group_owner_user']
    lnk_role_member_group_data = metadata.tables['lnk_role_member_group']
    lnk_role_member_serviceprincipal_data = metadata.tables['lnk_role_member_serviceprincipal']
    lnk_serviceprincipal_owner_serviceprincipal_data = metadata.tables['lnk_serviceprincipal_owner_serviceprincipal']
    lnk_serviceprincipal_owner_user_data = metadata.tables['lnk_serviceprincipal_owner_user']

    stmt = db.select(lnk_table.c.DirectoryRole, lnk_table.c.User)
    results = connection.execute(stmt).fetchall()

    stmt_directory_roles = db.select(directory_roles_data)
    directory_results = connection.execute(stmt_directory_roles).fetchall()
    directory_roles_list = []
    directory_roles_id_list = {}
    #print(directory_results)
    for objectType, objectId, deletionTimestamp, cloudSecurityIdentifier, description, displayName, isSystem, roleDisabled, roleTemplateId in directory_results:
        tempRole = DirectoryRole(objectType, objectId, deletionTimestamp, cloudSecurityIdentifier, description, displayName, isSystem, roleDisabled, roleTemplateId)
        #print(tempRole)
        directory_roles_id_list[tempRole.objectId] = tempRole
        directory_roles_list.append(tempRole)
    #print(directory_roles_id_list)

    
    stmt_user = db.select(database_user_data)
    user_results = connection.execute(stmt_user).fetchall()
    user_list = []
    user_id_list = {}

    for data_tuple in user_results:
        tempUser = User(*data_tuple)
        user_id_list[tempUser.objectId] = tempUser
        user_list.append(tempUser)

    G = nx.DiGraph()
    net = Network(height="100vh ", width="100%", bgcolor="#ffffff", font_color="black")
    for role_id, role_obj in directory_roles_id_list.items():
        G.add_node(f"role_{role_obj.displayName}", type="role", data=role_obj)
    print("------")
    for user_id, user_obj in user_id_list.items():
        G.add_node(f"user_{user_obj.userPrincipalName}", type="user", data=user_obj)
    #print(results)
    for role, user in results:
        role_node = f"role_{role}"
        user_node = f"user_{user}"
        
        if not G.has_node(user_node):
            G.add_node(user_node, type="user")

        if not G.has_node(role_node):
            G.add_node(role_node, type="role")

        G.add_edge(role_node, user_node)

    '''
    pos = nx.spring_layout(G)
    node_colors = ['lightblue' if G.nodes[n]['type'] == 'user' else 'lightgreen' for n in G.nodes]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray')
    plt.show()
    '''
    for node in G.nodes():
        net.add_node(node, label=str(node))  # You can customize label to show useful info

    # Add edges
    for source, target in G.edges():
        net.add_edge(source, target)

    net_html = net.generate_html()
    return render_template("graph.html", graph_html=net_html)

if __name__ == '__main__':
    app.run(debug=True)

