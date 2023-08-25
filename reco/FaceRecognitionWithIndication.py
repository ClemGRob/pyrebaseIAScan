import cv2
import os
import numpy as np
import dlib

class FaceRecognition:
    def __init__(self):
        # Load the pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # Number of images to capture per person
        self.images_per_person = 5
        
        # Dictionary to track the number of captured images per person
        self.images_per_person_dict = {}
        
        # List to store training data
        self.training_data = []
        
        # Create a facial recognition model
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def capture_photos(self, name):
        # Start the camera
        cap = cv2.VideoCapture(0)

        # Create a directory for the person if it doesn't exist
        if not os.path.exists(os.path.join('dataset', name)):
            os.makedirs(os.path.join('dataset', name))
            self.images_per_person_dict[name] = 0  # Initialize the image counter

        # Instructions for the user
        print("Please position yourself for photo capture.")
        print("Capture 3 photos of your front face, one looking left, and one looking right.")
        print("Press the spacebar to capture each photo.")

        while self.images_per_person_dict[name] < self.images_per_person:
            # Capture an image
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect the face in the image
            faces_detected = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces_detected:
                # Draw a rectangle around the detected face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display instructions for the current photo
                if self.images_per_person_dict[name] <= 2:
                    cv2.putText(frame, "Front face - Press space to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 255), 2)
                elif self.images_per_person_dict[name] == 3:
                    cv2.putText(frame, "Left profile - Press space to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 255), 2)
                elif self.images_per_person_dict[name] == 4:
                    cv2.putText(frame, "Right profile - Press space to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 255), 2)

                # Check for user input to capture the photo
                key = cv2.waitKey(1)
                if key == ord(' '):
                    img_name = os.path.join('dataset', name, f"{name}_{self.images_per_person_dict[name] + 1}.jpg")
                    cv2.imwrite(img_name, gray[y:y + h, x:x + w])
                    print(f"Image {self.images_per_person_dict[name] + 1} of {name} saved.")
                    self.images_per_person_dict[name] += 1  # Increment the counter

            # Display the live camera feed
            cv2.imshow('Capture', frame)

            key = cv2.waitKey(1)

            if key == ord('q'):
                break

        # Release the camera
        cap.release()

        # Close the window
        cv2.destroyAllWindows()

    def register_faces(self):
        # Capture the name
        name = input("Please enter the name: ")
        # Capture the last name (surname)
        last_name = input("Please enter the last name (surname): ")
        # Capture the apartment number
        apartment_number = input("Please enter the apartment number: ")


        full_name = f"{name}_{last_name}_{apartment_number}"

        # Check if the name already exists in the dictionary
        if full_name not in self.images_per_person_dict:
            # Assign a unique numeric ID to the person
            person_id = len(self.images_per_person_dict) + 1
            self.images_per_person_dict[full_name] = person_id
        self.capture_photos(full_name)
        # Add this data to the training dataset
        for i in range(self.images_per_person):
            img_path = os.path.join('dataset', full_name, f"{full_name}_{i + 1}.jpg")
            self.training_data.append((cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), self.images_per_person_dict[full_name]))

        # Train the facial recognition model with the training data
        X_train = [data[0] for data in self.training_data]
        y_train = [data[1] for data in self.training_data]
        self.recognizer.train(X_train, np.array(y_train))

        # Save the trained model for future use
        self.recognizer.save('face_recognition_model.yml')

    def recognize_faces(self):
        # Capture video from the camera
        cap = cv2.VideoCapture(0)
        # Load the mask detector as before
        mask_cascade = cv2.CascadeClassifier('haarcascade_mask.xml')
        # Load the landmark detector for eye detection
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        # Load the pre-trained facial recognition model
        self.recognizer.read('face_recognition_model.yml')  # Load your pre-trained model
        while True:
            # Capture a new frame
            ret, frame = cap.read()

            # Convert the frame to grayscale as before
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame as before
            faces = self.recognizer.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Get the region of interest (ROI) for the face as before
                roi_gray = gray[y:y + h, x:x + w]
                # Detect if a person is wearing a mask as before
                masks = mask_cascade.detectMultiScale(roi_gray)

                if len(masks) > 0:
                    print("mask detected")
                    mask_detected = True

                # Use the landmark detector to detect eyes as before
                landmarks = predictor(roi_gray, dlib.rectangle(0, 0, w, h))

                # Extract the eye coordinates as before
                left_eye = landmarks.part(36)
                right_eye = landmarks.part(45)

                # Calculate the horizontal distance between the eyes for eye movement detection
                eye_distance_x = right_eye.x - left_eye.x

                # If the horizontal distance between the eyes changes (eye movement), consider it a person
                if eye_distance_x > 10 and not mask_detected:  # Adjust this threshold as needed
                    # Check if the face matches a known individual
                    gray_face = roi_gray[y:y + h, x:x + w]
                    label, confidence = self.recognizer.predict(gray_face)

                    if confidence < 100:  # Adjust this threshold based on your model
                        print("Door Open")
                        return True

            # Display the frame as before
            cv2.imshow('Face Mask Detection', frame)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close all windows as before
        cap.release()
        cv2.destroyAllWindows()
        # If no person is recognized or security checks fail, return False
        print("No person is recognized or security checks fail")
        return False

if __name__ == "__main__":
    face_recognition = FaceRecognition()
    action = input("Enter 'register' to register faces or 'recognize' for recognition: ")
    
    if action == "register":
        face_recognition.register_faces()
    elif action == "recognize":
        face_recognition.recognize_faces()
