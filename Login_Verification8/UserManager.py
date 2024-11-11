# Features that user can run after login and facial verification

import UserDB


'''Housekeeping'''
def Animate():
    global done
    start_time = time.perf_counter()
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    end_time = time.perf_counter()
    sys.stdout.write(f'\rDone in {end_time - start_time-2:.4f} seconds     ')

# Libraries
from LibraryImporter import *

def AddUserImage(folder_path, un, frame):
    img_path = f"{folder_path}{un}.jpg"
    cv2.imwrite(img_path, frame)

def AddUserDetails():
    passwords = {}
    roles = {}
    with open(UserDB.db_path, "w") as file:
        for user in UserDB.usernames:
            file.write(f"{user},{UserDB.passwords[user]},{UserDB.roles[user]}\n")
    