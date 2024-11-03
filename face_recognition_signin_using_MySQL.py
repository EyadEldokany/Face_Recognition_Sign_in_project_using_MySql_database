import cv2
import numpy as np
import mysql.connector
import face_recognition
import pickle

# Connect to MySQL database
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="face_recognition"
)
cursor = db.cursor()

# Function to encode face and add user to database
def add_user(name):
    print("Capturing face for enrollment...")
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break
            
        # Detect face in the frame
        face_locations = face_recognition.face_locations(frame)
        
        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)
        
        cv2.imshow("Capture - Press 'q' to capture", frame)
        
        # Press 'q' to capture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    # Process the first detected face for enrollment
    if face_locations:
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        encoded_data = pickle.dumps(face_encoding)
        
        # Insert user data into database
        cursor.execute("INSERT INTO users (name, face_encoding) VALUES (%s, %s)", (name, encoded_data))
        db.commit()
        print(f"User {name} added successfully.")
    else:
        print("No face detected. Try again.")

# Function to recognize face for sign-in
def recognize_user():
    print("Recognizing face for sign-in...")
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break
            
        # Detect face in the frame
        face_locations = face_recognition.face_locations(frame)
        
        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        
        cv2.imshow("Sign-In - Press 'q' to capture", frame)
        
        # Press 'q' to capture
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Check if any face was detected
    if face_locations:
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        
        # Fetch all users and their face encodings from the database
        cursor.execute("SELECT id, name, face_encoding FROM users")
        users = cursor.fetchall()
        
        # Initialize variables to track the closest match
        best_match_id = None
        best_match_name = None
        lowest_distance = 0.6  # Threshold for face match

        # Loop through users and calculate face distance
        for user_id, name, encoded_data in users:
            db_face_encoding = pickle.loads(encoded_data)
            face_distance = face_recognition.face_distance([db_face_encoding], face_encoding)[0]
            
            # Check if this is the closest match
            if face_distance < lowest_distance:
                lowest_distance = face_distance
                best_match_id = user_id
                best_match_name = name

        if best_match_id:
            print(f"Welcome, {best_match_name}!")
            # Log the sign-in
            cursor.execute("INSERT INTO sign_in_logs (user_id) VALUES (%s)", (best_match_id,))
            db.commit()
        else:
            print("No matching user found.")
    else:
        print("No face detected. Try again.")


# Main menu to add users or recognize faces
def main():
    while True:
        print("\n--- Face Recognition Sign-In System ---")
        print("1. Add User")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter the name of the new user: ")
            add_user(name)
        elif choice == '2':
            recognize_user()
        elif choice == '3':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
