import cv2
import os
import numpy as np

# Chargez le modèle de détection de visage pré-entraîné
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Définissez le nombre d'images par personne à capturer
images_per_person = 5

# Créez un répertoire pour stocker les images
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# Créez un dictionnaire pour suivre le nombre d'images capturées par personne
images_per_person_dict = {}

# Créez un dictionnaire pour stocker les données d'entraînement
training_data = []

# Démarrez la caméra
cap = cv2.VideoCapture(0)

while True:
    # Capturez l'image
    ret, frame = cap.read()

    # Convertissez l'image en niveau de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détectez les visages dans l'image
    faces_detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces_detected:
        # Demandez à l'utilisateur d'entrer le nom de la personne
        name = input("Veuillez entrer le nom et prénom de la personne : ")

        # Créez un répertoire pour cette personne s'il n'existe pas
        if not os.path.exists(os.path.join('dataset', name)):
            os.makedirs(os.path.join('dataset', name))
            images_per_person_dict[name] = 0  # Initialisation du compteur

        # Capturez plusieurs images de la personne
        for i in range(images_per_person):
            img_name = os.path.join('dataset', name, f"{name}_{i+1}.jpg")
            cv2.imwrite(img_name, gray[y:y+h, x:x+w])
            print(f"Image {i+1} de {name} enregistrée.")
            images_per_person_dict[name] += 1  # Incrémentation du compteur

        print(f"{images_per_person_dict[name]} images de {name} ont été enregistrées.")

        # Ajoutez ces données à l'ensemble de données d'entraînement
        for i in range(images_per_person):
            img_path = os.path.join('dataset', name, f"{name}_{i+1}.jpg")
            training_data.append((cv2.imread(img_path, cv2.IMREAD_GRAYSCALE), name))

    # Arrêtez la collecte d'images lorsque vous avez suffisamment d'images par personne
    enough_data = all(count >= images_per_person for count in images_per_person_dict.values())
    if enough_data:
        break

# Libérez la caméra
cap.release()

# Fermez toutes les fenêtres
cv2.destroyAllWindows()

# Entraînez votre modèle de reconnaissance faciale avec les données d'entraînement
recognizer = cv2.face_LBPHFaceRecognizer.create()
X_train = [data[0] for data in training_data]
y_train = [data[1] for data in training_data]
recognizer.train(X_train, np.array(y_train))

# Enregistrez le modèle entraîné pour une utilisation ultérieure
recognizer.save('face_recognition_model.yml')
