import os

'''Database'''
db_folder = os.getcwd()
db_folder += "\\database\\"
db_path = f"{db_folder}credentials.txt"

'''Variables'''
attempts_made = 0

encoded_faces_DB = []

images_folder = os.getcwd()
images_folder += "\\images\\"

bini_gwen_filename = f"{images_folder}glapuli.jpg"
tim_filename = f"{images_folder}tjcguela.jpg"
soph_filename = f"{images_folder}sdgrefaldo.jpg"

# '''Lists'''
# usernames = []
# roles = {}
# passwords = {}

'''Load Users'''
with open(db_path, 'r') as file:
  usernames = []
  roles = {}
  passwords = {}
  for line in file:
    username, password, role = line.strip().split(',')
    usernames.append(username)
    passwords[username] = password
    roles[username] = role