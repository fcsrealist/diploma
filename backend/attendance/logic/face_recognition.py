from core.models import Course

import face_recognition
import pickle


class FaceRecognitionUseCase:
    def __init__(self, course: Course, image_path):
        self.course = course
        self.image_path = image_path

    def execute(self, threshold=0.5) -> list:
        test_image = face_recognition.load_image_file(self.image_path)
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = (face_recognition
                          .face_encodings(test_image, face_locations))

        predictions = []

        clf = pickle.load(open('files/trained_model.pickle', 'rb'))

        for x in face_encodings:
            closest = clf.kneighbors([x], n_neighbors=1)
            if closest[0][0][0] <= threshold:
                predictions.append(clf.predict([x])[0])
            else:
                predictions.append('')

        return predictions
