import sqlalchemy as db
import networkx as nx
import matplotlib.pyplot as plt
from directoryRole import DirectoryRole
from user import User

engine = db.create_engine(r'sqlite:///C:\\Users\\Optiplex 3080\\Desktop\\PythonProjects\\AzureReader\\roadrecon.db')
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
stmt = db.select(lnk_table.c.DirectoryRole, lnk_table.c.User)
results = connection.execute(stmt).fetchall()

directory_roles_data = metadata.tables['DirectoryRoles']
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

database_user_data = metadata.tables['Users']
stmt_user = db.select(database_user_data)
user_results = connection.execute(stmt_user).fetchall()
user_list = []
user_id_list = {}

for data_tuple in user_results:
    tempUser = User(*data_tuple)
    user_id_list[tempUser.objectId] = tempUser
    user_list.append(tempUser)

G = nx.DiGraph()

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
pos = nx.spring_layout(G)
node_colors = ['lightblue' if G.nodes[n]['type'] == 'user' else 'lightgreen' for n in G.nodes]

nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray')
plt.show()