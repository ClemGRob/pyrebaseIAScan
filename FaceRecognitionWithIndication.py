import cv2
import numpy as np
import dlib
import json  # Import the json module
import shutil
import time
import sys
import os
import pyrebase

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.wrapper import *
import config


class FaceRecognition:
    def __init__(self):
        self.name = ""
        self.last_name = ""
        self.apartment_number = ""
        self.input_ID = ""
        self.input_password = ""
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.images_per_person = 5
        self.firebase = pyrebase.initialize_app(config.pirebaseConfig)
        self.storage = self.firebase.storage()
        self.auth = self.firebase.auth()
        self.user = login(self.auth, "password@password.password", "password")
        try:
            file = 'images_per_person_dict.json'  # Change the filename to use JSON
            online_file = 'images_per_person_dict.json'
            download(self.storage, file, online_file, self.user)
            with open('images_per_person_dict.json', 'r') as file:  # Change file format to read JSON
                self.images_per_person_dict = json.load(file)  # Use json.load to read JSON
        except FileNotFoundError:
            self.images_per_person_dict = {}

        try:
            file = 'house_administrator_dict.json'  # Change the filename to use JSON
            online_file = 'house_administrator_dict.json'
            download(self.storage, file, online_file, self.user)
            with open('house_administrator_dict.json', 'r') as file:  # Change file format to read JSON
                self.house_administrator_dict = json.load(file)  # Use json.load to read JSON
        except FileNotFoundError:
            self.house_administrator_dict = {}

        self.training_data = []
        self.recognizer = cv2.face_LBPHFaceRecognizer.create()

    def verify_id(self, entered_id_input, entered_pwd_input):
        correct_id = "cedric"
        correct_password = "1234"
        error_count = 0

        while error_count < 3:
            if entered_id_input == correct_id and entered_pwd_input == correct_password:
                return True
            error_count += 1
            print("Invalid ID or password. Please try again.")

        print("Too many failed attempts. Access denied.")
        return False

    def capture_photos(self, name_client):
        cap = cv2.VideoCapture(0)

        # if not os.path.exists(os.path.join('dataset', name_client)):
        #     os.makedirs(os.path.join('dataset', name_client))
        #     self.images_per_person_dict[name_client] = 0

        while self.images_per_person_dict[name_client] < self.images_per_person:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces_detected = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces_detected:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if self.images_per_person_dict[name_client] <= 2:
                    cv2.putText(frame, "Front face - Press space to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 255), 2)
                elif self.images_per_person_dict[name_client] == 3:
                    cv2.putText(frame, "Left profile - Press space to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 255), 2)
                elif self.images_per_person_dict[name_client] == 4:
                    cv2.putText(frame, "Right profile - Press space to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2)

                key = cv2.waitKey(1)
                if key == ord(' '):

                    img_name = os.path.join('dataset', name_client,
                                            f"{name_client}_{self.images_per_person_dict[name_client] + 1}.jpg")
                    cv2.imwrite(img_name, gray[y:y + h, x:x + w])
                    print(f"Image {self.images_per_person_dict[name_client] + 1} of {name_client} saved.")
                    self.images_per_person_dict[name_client] += 1

            cv2.imshow('Capture', frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def register_faces(self, name, last_name, apartment_number, is_house_admin=False):
        self.name = name
        self.last_name = last_name
        self.apartment_number = apartment_number

        full_name = f"{name}_{last_name}_{apartment_number}"

        if full_name not in self.images_per_person_dict:
            person_id = len(self.images_per_person_dict) + 1
            self.images_per_person_dict[full_name] = person_id

            # Save the updated dictionary to JSON
            with open('images_per_person_dict.json', 'w') as file:
                json.dump(self.images_per_person_dict, file)
            file = 'images_per_person_dict.json'
            online_file = 'images_per_person_dict.json'
            upload(self.storage, file, online_file, self.user)
            if is_house_admin:
                self.house_administrator_dict[full_name] = person_id
                # Save the updated dictionary to JSON
                with open('house_administrator_dict.json', 'w') as file:
                    json.dump(self.house_administrator_dict, file)

                file = 'house_administrator_dict.json'
                online_file = file
                upload(self.storage, file, online_file, self.user)
        self.capture_photos(full_name)

        for i in range(self.images_per_person):
            img_path = os.path.join('dataset', full_name, f"{full_name}_{i + 1}.jpg")
            self.training_data.append(
                (cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), self.images_per_person_dict[full_name]))

        x_train = [data[0] for data in self.training_data]
        y_train = [data[1] for data in self.training_data]
        self.recognizer.train(x_train, np.array(y_train))

        self.recognizer.save('face_recognition_model.yml')

    def delete_person(self, name, last_name, apartment_number):
        self.name = name
        self.last_name = last_name
        self.apartment_number = apartment_number

        full_name = f"{name}_{last_name}_{apartment_number}"

        # Create a list of keys to delete
        keys_to_delete = []

        for key in self.images_per_person_dict:
            if key.lower() == full_name.lower():
                keys_to_delete.append(key)

        # Remove found keys from the dictionary
        for key in keys_to_delete:
            del self.images_per_person_dict[key]

        # Remove associated files
        for key in keys_to_delete:
            person_photos_dir = os.path.join('dataset', key)
            if os.path.exists(person_photos_dir):
                shutil.rmtree(person_photos_dir)

        # Update training data
        self.training_data = [(img, label) for img, label in self.training_data if
                              label not in [self.images_per_person_dict.get(key) for key in keys_to_delete]]

        # Remove from house administrator list if present
        if full_name in self.house_administrator_dict:
            del self.house_administrator_dict[full_name]
            with open('house_administrator_dict.json', 'w') as file:
                json.dump(self.house_administrator_dict, file)

        if len(self.training_data) >= 2:
            x_train = [data[0] for data in self.training_data]
            y_train = [data[1] for data in self.training_data]
            self.recognizer.train(x_train, np.array(y_train))

        # Save the updated dictionaries to JSON
        with open('images_per_person_dict.json', 'w') as file:
            json.dump(self.images_per_person_dict, file)

        # Remove the recognition model if necessary
        if len(self.training_data) < 2 and os.path.exists('face_recognition_model.yml'):
            os.remove('face_recognition_model.yml')

        return True

    def recognize_faces(self):
        cap = cv2.VideoCapture(0)
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        self.recognizer.read('face_recognition_model.yml')

        cv2.namedWindow("Face Detection", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("Face Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        start_time = time.time()
        delay_passed = False

        while True:
            ret, frame = cap.read()

            if not delay_passed:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.imshow('Face Detection', frame)

                if time.time() - start_time > 5:
                    delay_passed = True
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y + h, x:x + w]
                    landmarks = predictor(roi_gray, dlib.rectangle(0, 0, w, h))

                    left_eye = landmarks.part(36)
                    right_eye = landmarks.part(45)
                    eye_distance_x = right_eye.x - left_eye.x

                    if eye_distance_x > 10:
                        gray_face = roi_gray[y:y + h, x:x + w]
                        label, confidence = self.recognizer.predict(gray_face)

                        if confidence < 85:
                            print("Door Open")
                            cap.release()
                            cv2.destroyAllWindows()
                            return True
                        else:
                            print("Unknown person")

                cv2.imshow('Face Detection', frame)

            if time.time() - start_time > 10:
                print("Timeout: No face recognized in 10 seconds.")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        print("Security checks fail")
        return False


if __name__ == "__main__":
    face_recognition = FaceRecognition()
    action = input("Enter 'register' to register faces or 'recognize' for recognition: ")

    if action == "register":
        name = input("Enter the name: ")
        last_name = input("Enter the last name: ")
        apartment_number = input("Enter the apartment number: ")
        face_recognition.register_faces(name, last_name, apartment_number)
    elif action == "recognize":
        face_recognition.recognize_faces()
    elif action == "delete":
        name = input("Enter the name: ")
        last_name = input("Enter the last name: ")
        apartment_number = input("Enter the apartment number: ")
        face_recognition.delete_person(name, last_name, apartment_number)
