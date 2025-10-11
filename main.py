from flask import Flask, render_template, request, jsonify, url_for, redirect
import sqlalchemy as db
from user import User
from werkzeug.utils import secure_filename

from getData import *

from pyvis.network import Network
import os

ALLOWED_EXTENSIONS = {'db',}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


def check_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/update-graph-resources', methods=['POST'])
def list_resources():
    user = request.json.get("user")
    filename = request.json.get("filename")
    data = {
        "user" : user,
        "filename" : filename
    }
    print("DATAAAA: ", data)
    generate_graph_for_resources(data)
    return jsonify({"success" : True})

@app.route('/update-graph-role', methods=['POST'])
def update_graph_roles():
    role = request.json.get("role")
    filename = request.json.get("filename")
    data = {
        "role" : role,
        "filename" : filename
    }
    print("DATAAAA WITH ROLE: ", data)
    generate_graph_with_role(data)
    return jsonify({"success" : True})

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

    
    path_list = ["Global Administrators", "Privileged Role Administrator",
                  "Application Administrator", "Cloud Application Administrator",
                  "Directory Readers", "Directory Writers", "Security Reader",
                  "Security Administrator", "User Administrator", "Helpdesk Administrator",
                  "Password Administrator", "Service Support Administrator",
                  "Reports Reader", "Exchange Administrator", "SharePoint Administrator",
                  "Teams Administrator", "Compliance Administrator", "Authentication Administrator",
                  "Intune Administrator", "Dynamics 365 Administrator",]


    return render_template("graph.html", user_list=user_list, path_list=path_list, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)

