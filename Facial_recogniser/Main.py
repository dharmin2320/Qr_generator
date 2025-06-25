import cv2
import face_recognition
import os

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

    def load_encoding_images(self, folder_path):
        """Load and encode all face images from a given folder."""

        folder_path = r"C:\Users\Dharmin vadher\Desktop\Python_project\image"
        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            os.makedirs(folder_path)  # Create folder if missing
            return

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            img = cv2.imread(file_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)

            if encodings:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(os.path.splitext(filename)[0])  # Use filename as the person's name

    def detect_known_faces(self, frame):
        """Detect faces in a frame and match them with known faces."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = self.known_face_names[match_index]

            face_names.append(name)

        return face_locations, face_names

# Initialize the face recognition system
sfr = SimpleFacerec()
sfr.load_encoding_images(r"C:\Users\Dharmin vadher\Desktop\Python_project\images")  # Ensure this folder exists

# Load Camera
cap = cv2.VideoCapture(0)  # Change index if needed (0, 1, 2, etc.)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame.")
        break

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for (y1, x2, y2, x1), name in zip(face_locations, face_names):
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    # Display the video feed
    cv2.imshow("Face Recognition", frame)

    # Press 'ESC' to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
