# PROJECT INFO
#
# Facial Recognition Using CNN
# Using threads to try to seamlessly 
# transition between functions
#

'''Modules'''
import UserManager
import UserDB

from LibraryImporter import *

'''Housekeeping'''
def Animate():
    start_time = time.perf_counter()
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    end_time = time.perf_counter()
    sys.stdout.write(f'\rDone in {end_time - start_time-2:.4f} seconds     ')

'''Config'''
#region
def EncodeOneFace(img_path):
   global encoded_face
   global current_encoded_face

   ref_image = face_recognition.load_image_file(img_path)
   try:
      encoded_face = face_recognition.face_encodings(ref_image)[0]
   except IndexError:
      print("Error...")
      quit()
   
   current_encoded_face = [encoded_face]
   # //UserDB.encoded_face_DB =

def EncodeKnownFaces():
   global images_folder

   images_folder = os.getcwd()
   images_folder += "\\images\\"
   img_path = f"{images_folder}\\{username}.jpg"

   t1 = Thread(target=EncodeOneFace, args=(img_path,))
   t1.start()
   t1.join()

   for user in UserDB.usernames:
      img_path = f"{images_folder}\\{user}.jpg"
      ref_image = face_recognition.load_image_file(img_path)

      try:
         encoded_face = face_recognition.face_encodings(ref_image)[0]
      except IndexError:
         print("Error...")
         quit()
      
      UserDB.encoded_faces_DB.append(encoded_face)
   print(f"Loaded {len(UserDB.encoded_faces_DB)} encoded faces.")




def StartStream():
  global vs
  vs = VideoStream(src=0).start()

def StartCamera(name, prompt):
  global key
  while True:
    frame = vs.read()
    key = cv2.waitKey(1)
    if key == ord("q"):
      break
    elif key == ord("c"):
      print(f"\n{prompt}")
      break
    cv2.imshow(name, frame)


#endregion

'''Face Recog In Sequence'''

#region

def LoadCNNModel():
  global small_frame
  global rgb
  global boxes

  small_frame = imutils.resize(vs.read(), width=200)
  rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
  boxes = face_recognition.face_locations(rgb,model="cnn")

def ScanCamera():
   global face_encodings
   face_encodings = face_recognition.face_encodings(rgb, boxes)

def DrawBox():
   global ind
   cv2.imshow("Scanning...", small_frame)
   for ind, encoding in enumerate(face_encodings):
      t1 = Thread(target=GetResults, args=(current_encoded_face, encoding,), daemon=True)
      t2 = Thread(target=GetDistance, args=(current_encoded_face, encoding,), daemon=True)
      t3 = Thread(target=VerifyFace)

      t1.start()
      t2.start()

      t1.join()
      t2.join()

      t3.start()
      t3.join()

def GetResults(kf, e):
   global results
   results = face_recognition.compare_faces(kf, e)

def GetDistance(kf, e):
   global distance
   distance = face_recognition.face_distance(kf, e)

def VerifyFace():
   global y
   if results[0] == True:
      print("Face Recognized...Access Granted.")
      t1 = Thread(target=GetTopVertex)
      t2 = Thread(target=GetRightVertex)
      t3 = Thread(target=GetBottomVertex)
      t4 = Thread(target=GetLeftVertex)
      t5 = Thread(target=DrawRectangle)
      t1.start()
      t2.start()
      t3.start()
      t4.start()

      t1.join()
      t2.join()
      t3.join()
      t4.join()

      t5.start() # Draw Rectangle
      t5.join()
   else:
      os.system("cls")
      print("Unrecognized Face... Access Denied.\n")
      os.abort()
      cv2.destroyAllWindows()
      vs.stop()
      
 
'''Get Vertices'''
#region
def GetTopVertex():
   global top
   top = boxes[ind][0]
   print(f"top vertex: {top}")

def GetRightVertex():
   global right
   right = boxes[ind][1]
   print(f"right vertex: {right}")

def GetBottomVertex():
   global bottom
   bottom = boxes[ind][2]
   print(f"bottom vertex: {bottom}")

def GetLeftVertex():
   global left
   left = boxes[ind][3]
   print(f"left vertex: {left}")
#endregion

def DrawRectangle():
   global boxed_frame 
   boxed_frame = small_frame.copy()
   time.sleep(0.1)
   cv2.rectangle(boxed_frame, (left, top), (right, bottom), (255, 0, 0), 2) # Draw Rectangle on copy

def ShowScannedFrame(name):
   while True:
      key = cv2.waitKey(1)
      if key == ord("c"):
         break
      try:
         cv2.imshow(name, boxed_frame)
      except NameError:
         break

#endregion

'''Creating Threads'''
#region
#Config
w0 = Thread(target=Animate)
t0 = Thread(target=EncodeKnownFaces)
# Start Program
t1 = Thread(target=StartStream)
next_prompt = "Loading CNN Model"
t2 = Thread(target=StartCamera, args=("Camera", next_prompt,), daemon=True)

# Load Model
t3 = Thread(target=LoadCNNModel, daemon=True)
w1 = Thread(target=Animate)
next_prompt = "\nVerifying Face"
t4 = Thread(target=StartCamera, args=("Initializing...", next_prompt,), daemon=True)

# Scan Camera, Get Face Vertices, and Draw Box
w2 = Thread(target=Animate)
t5 = Thread(target=ScanCamera)
t6 = Thread(target=DrawBox)

# Showing Recognized Face
w3 = Thread(target=Animate)
t7 = Thread(target=ShowScannedFrame, args=("Scanned Frame",))

next_prompt = "\nPress C to continue..."
camAgain = Thread(target=StartCamera, args=("Taking a picture...", next_prompt,), daemon=True)
loadAgain = Thread(target=LoadCNNModel, daemon=True)
scanAgain = Thread(target=ScanCamera, daemon=True)
drawAgain = Thread(target=DrawBox, daemon=True)


#endregion

'''Starting Threads'''
def Start(un, r):
  global role
  global username
  global done
  
  # Get User Data from DB
  role = r
  username = un

  start_time = time.perf_counter()
  done = False
  print("Encoding Faces")
  w0.start()
  t0.start() # Start of Encoding Known Faces
  t0.join()
  time.sleep(2)
  done = True

  t1.start() #Start Video Stream
  t1.join()

  print("\nStarting Camera")
  t2.start() #Start Camera
  t2.join()

  # Load CNN Model
  if key == ord("c"):
    t4.start() # Restart Camera
    done = False
    w1.start() # Animation 
    t3.start() # Load Model
    t3.join()
    time.sleep(2) # Delay to let animation show
    done = True
    print("Press C to continue...")
    t4.join()

  # Verifying Face
  if key == ord("c"):
    done = False
    w2.start() # Animation
    t5.start() # Scan Camera
    t5.join()
    t6.start() # Draw Box
    t6.join()
    time.sleep(2)
    done = True
    w2.join()
    t7.start() # Show Drawn Box
    print("\nPress C to continue...")
    t7.join()

  if key == ord("c"):
     os.system("cls")
     usrInput = input("1.Add User\n2.Remove User\n3.Show Users\n(Enter Q to quit.)\n\nEnter choice: ")
     while not (usrInput == "Q" or usrInput == "q"):
        if usrInput == "1" and role == "admin":
           new_user = input("Enter new user name: ")
           if new_user in UserDB.usernames:
              print("username already exists.")
              continue
           new_pass = input("Enter new password.")
           new_role = input("Enter user's role.")
           UserDB.usernames.append(new_user)
           UserDB.passwords[new_user] = new_pass
           UserDB.roles[new_user] = new_role
           StartCamera("Taking a picture...", "Press C to continue...")
           cv2.destroyWindow("Taking a picture...")
           if key == ord("c"):
              LoadCNNModel()
              ScanCamera()
              for encoding in face_encodings:
                 results = face_recognition.compare_faces(UserDB.encoded_faces_DB, encoding)
                 if any(results) == True:
                    print("Face has already been encoded")
                    input()

                    del UserDB.passwords[new_user]
                    del UserDB.roles[new_user]
                    UserDB.usernames.remove(new_user)

                    break
                 else:
                    os.system("cls")
                    print("\nSaving Changes...")
                    input("")
                    UserManager.AddUserImage(images_folder, new_user, vs.read())
                    UserManager.AddUserDetails()
                    break
                  
        elif usrInput == "2" and role == "admin": # Delete
           list_len = len(UserDB.usernames)
           usr_to_del = input("Enter user to delete: ")

           UserDB.usernames.remove(usr_to_del)
           del UserDB.passwords[usr_to_del]
           del UserDB.roles[usr_to_del]


           db_path = os.getcwd()
           db_path += "\\database\\credentials.txt"
           with open(UserDB.db_path, "w") as file:
              for user in UserDB.usernames:
                 file.write(f"{user},{UserDB.passwords[user]},{UserDB.roles[user]}\n")

           img_path = f"{UserDB.images_folder}{usr_to_del}.jpg"
           os.remove(img_path)

           for i in range(list_len-1):
            img_path = f"{images_folder}\\{UserDB.usernames[i]}.jpg"
            ref_image = face_recognition.load_image_file(img_path)

            try:
               encoded_face = face_recognition.face_encodings(ref_image)[0]
            except IndexError:
               print("Error...")
               quit()
            
            UserDB.encoded_faces_DB.append(encoded_face)
            
         #   del UserDB.passwords[usr_to_del]
         #   del UserDB.roles[usr_to_del]

            # UserManager.AddUserDetails()
            
           print(f"Loaded {len(UserDB.encoded_faces_DB)} encoded faces.")


        elif usrInput == "3":
           for i, user in enumerate (UserDB.usernames, start=1):
              print(f"Figure {i}: {user}")
              image = mpimg.imread(f"{UserDB.images_folder}{user}.jpg")
              plt.imshow(image)
              plt.show()

            #   Image._show(f"{UserDB.images_folder}{user}.jpg", rgb)  

        else:
           print("Access Denied. Requires admin access.")
           input()

        os.system("cls")
        usrInput = input("1.Add User\n2.Remove User\n3.Show Users\n(Enter Q to quit.)\n\nEnter choice: ")


  cv2.destroyAllWindows()
  vs.stop()
  # End
  end_time = time.perf_counter()
  print(f"\nSession Lasted {end_time - start_time:.4f} seconds.")


