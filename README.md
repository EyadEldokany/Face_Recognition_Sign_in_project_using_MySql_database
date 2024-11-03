# Face Recognition Sign-In System

This project implements a face recognition-based sign-in system using Python, OpenCV, and MySQL. Users can enroll by adding their face to the database, and the system will recognize them for subsequent sign-ins. The face recognition model is powered by the `face_recognition` library, which utilizes deep learning to encode and match facial features.

## Features

- **User Enrollment**: Add new users to the database by capturing their face through the webcam.
- **Face Recognition Sign-In**: Authenticate users by recognizing their face and logging the sign-in event in the database.
- **MySQL Database**: Store user data and sign-in logs in a MySQL database.

## Technologies Used

- Python
- OpenCV
- face_recognition (for face detection and recognition)
- MySQL (for storing user data and sign-in logs)

## Prerequisites

1. **Python 3.x**
2. **MySQL** (with a `face_recognition` database and `users` and `sign_in_logs` tables created)
3. **Required Libraries**:
   - Install the necessary Python libraries using:

     ```bash
     pip install opencv-python face_recognition mysql-connector-python
     ```

## Database Setup

1. **Create Database and Tables**:
   - Open MySQL and create the `face_recognition` database and tables using the following SQL commands:

     ```sql
     CREATE DATABASE face_recognition;

     USE face_recognition;

     CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50),
       face_encoding BLOB
     );

     CREATE TABLE sign_in_logs (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES users(id)
     );
     ```

2. **Configure Database Connection**:
   - In the code, update the `db = mysql.connector.connect(...)` section with your MySQL username, password, and host.

## How to Use

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/face-recognition-sign-in.git
   cd face-recognition-sign-in
   ```

2. **Run the Program**:

   ```bash
   python your_script_name.py
   ```

3. **Enroll a New User**:
   - Select option `1` to add a new user. You will be prompted to enter the user's name and then capture their face using the webcam.

4. **Sign In**:
   - Select option `2` to sign in. The program will attempt to recognize the user’s face and log the sign-in event if a match is found in the database.

5. **Exit**:
   - Select option `3` to exit the program.

## Code Overview

- **`add_user(name)`**: Captures the user's face via webcam, encodes it, and saves the encoding along with the user's name in the MySQL database.
- **`recognize_user()`**: Captures a face for sign-in, compares it with stored encodings in the database, and logs the sign-in event if a match is found.
- **`main()`**: Provides a simple command-line interface for user enrollment, sign-in, and exit options.

## Troubleshooting

- **Multiple Faces Detected**: Ensure only one face is visible during enrollment or sign-in for accurate results.
- **Database Errors**: Check your MySQL configuration and ensure that the `face_recognition` database and required tables are correctly set up.

## Contributing

Contributions are welcome! If you find any issues or want to add features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [face_recognition](https://github.com/ageitgey/face_recognition) - For facial recognition algorithms.
- [OpenCV](https://opencv.org/) - For image and video processing.

---

Replace `your_script_name.py` with the actual filename of your Python script, and update `yourusername` in the clone link with your GitHub username. This README file should provide clear instructions for users and contributors of the project.
