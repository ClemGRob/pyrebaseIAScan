import cv2
import dlib


def detect_and_validate_person(recognizer):
    # Load the face and mask detectors as before
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    mask_cascade = cv2.CascadeClassifier('haarcascade_mask.xml')

    # Load the landmark detector for eye detection
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    # Capture video from the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a new frame
        ret, frame = cap.read()

        # Convert the frame to grayscale as before
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame as before
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

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
                label, confidence = recognizer.predict(gray_face)

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
