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

