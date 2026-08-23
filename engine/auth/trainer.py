import cv2
import os
import numpy as np
from PIL import Image

# ==============================
# SETTINGS
# ==============================

# Face images folder
path = "engine/auth"

# Maximum photos to train
MAX_PHOTOS = 50

# Haar Cascade
detector = cv2.CascadeClassifier(
    "engine/auth/haarcascade_frontalface_default.xml"
)

# LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()


# ==============================
# LOAD FACE IMAGES
# ==============================

def getImagesAndLabels(path):

    # Get only JPG face images
    imagePaths = [
        os.path.join(path, file)
        for file in os.listdir(path)
        if file.lower().endswith(".jpg")
        and file.lower().startswith("face.")
    ]

    # Sort properly: face.1.1.jpg, face.1.2.jpg...
    def image_number(filename):
        try:
            return int(
                os.path.splitext(filename)[0].split(".")[-1]
            )
        except:
            return 999999

    imagePaths.sort(key=image_number)

    # ==============================
    # ONLY FIRST 50 PHOTOS
    # ==============================
    imagePaths = imagePaths[:MAX_PHOTOS]

    print("\n================================")
    print("FACE TRAINING")
    print("================================")
    print(f"Total images found : {len(imagePaths)}")
    print(f"Training limit     : {MAX_PHOTOS}")
    print("================================\n")

    faceSamples = []
    ids = []

    for index, imagePath in enumerate(imagePaths, start=1):

        try:
            print(f"Processing {index}/{len(imagePaths)} : "
                  f"{os.path.basename(imagePath)}")

            # Convert image to grayscale
            PIL_img = Image.open(imagePath).convert("L")
            img_numpy = np.array(PIL_img, "uint8")

            # Get ID from filename
            # face.1.25.jpg -> ID = 1
            filename = os.path.basename(imagePath)
            parts = filename.split(".")

            if len(parts) < 3:
                print("Skipped: Invalid filename")
                continue

            face_id = int(parts[1])

            # Detect face
            faces = detector.detectMultiScale(
                img_numpy,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            if len(faces) == 0:
                print("  No face detected - skipped")
                continue

            for (x, y, w, h) in faces:
                faceSamples.append(
                    img_numpy[y:y + h, x:x + w]
                )
                ids.append(face_id)

        except Exception as e:
            print(f"  Error: {e}")


    return faceSamples, ids


# ==============================
# TRAIN MODEL
# ==============================

faces, ids = getImagesAndLabels(path)

if len(faces) == 0:
    print("\n❌ No faces found!")
    print("Training cancelled.")
    exit()

print("\n================================")
print("Training LBPH model...")
print("================================")

recognizer.train(faces, np.array(ids))

# Save trained model
trainer_folder = "engine/auth/trainer"

os.makedirs(trainer_folder, exist_ok=True)

trainer_file = os.path.join(
    trainer_folder,
    "trainer.yml"
)

recognizer.write(trainer_file)

print("\n================================")
print("✅ TRAINING COMPLETE")
print("================================")
print(f"Photos processed : {len(faces)}")
print(f"Model saved      : {trainer_file}")
print("Training uses    : MAX 50 JPG photos")
print("================================")