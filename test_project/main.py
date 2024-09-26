import cv2
from deepface import DeepFace

# Load pre-trained deep learning model for age estimation
model = DeepFace.build_model("Age")

# Load the image
image_path = "path_to_your_image.jpg"
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use a pre-trained Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# If a face is detected, estimate age
if len(faces) > 0:
    (x, y, w, h) = faces[0]
    face = gray_image[y:y+h, x:x+w]
    # Resize the face for better age estimation
    face = cv2.resize(face, (224, 224))
    # Estimate age using the deep learning model
    predicted_age = model.predict(face)[0]
    print("Predicted age:", predicted_age)
else:
    print("No face detected.")
