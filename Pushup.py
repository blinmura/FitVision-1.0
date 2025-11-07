import mediapipe as mp
from src.ThreadedCamera import ThreadedCamera
from src.exercies.Exercise import Exercise
from src.utils import *
from progress_manager import ProgressManager

import os
import json

# ---------- ПРОГРЕСС (добавлено) ----------
PROGRESS_FILE = "progress.json"

'''def load_all_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except json.JSONDecodeError:
            pass
    return {}

def get_progress_for(ex_name):
    data = load_all_progress()
    if ex_name in data:
        return data[ex_name]
    low = ex_name.lower()
    cap = ex_name.capitalize()
    return data.get(low, data.get(cap, 0))

def save_progress_for(ex_name, value):
    data = load_all_progress()
    data[ex_name] = value
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=4)
# ------------------------------------------
'''
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255))
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
PRESENCE_THRESHOLD = 0.5
VISIBILITY_THRESHOLD = 0.5
performedPushUp = False


class Pushup(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        scount = int(ProgressManager.load_progress().get("Pushup", 0)) # ← загружаем прогресс

        while True:
            success, image = threaded_camera.show_frame()
            if not success or image is None:
                continue
            image = cv2.flip(image, 1)
            image_orig = cv2.flip(image, 1)
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=pose_landmark_drawing_spec,
                connection_drawing_spec=pose_connection_drawing_spec)
            idx_to_coordinates = get_idx_to_coordinates(image, results)

            try:
                # shoulder - ankle - wrist
                if 12 in idx_to_coordinates and 28 in idx_to_coordinates and 16 in idx_to_coordinates:
                    cv2.line(image, (idx_to_coordinates[12]), (idx_to_coordinates[28]), thickness=4, color=(255, 0, 255))
                    cv2.line(image, (idx_to_coordinates[28]), (idx_to_coordinates[16]), thickness=4, color=(255, 0, 255))
                    eang1 = ang((idx_to_coordinates[12], idx_to_coordinates[28]),
                                (idx_to_coordinates[28], idx_to_coordinates[16]))
                    cv2.putText(image, str(round(eang1, 2)), (idx_to_coordinates[28]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6,
                                color=(0, 255, 0), thickness=2)
            except:
                pass

            try:
                # Count Number of Pushups
                if 12 in idx_to_coordinates:
                    shoulder_coord = idx_to_coordinates[12]
                else:
                    shoulder_coord = idx_to_coordinates[11]

                if 16 in idx_to_coordinates:
                    ankle_coord = idx_to_coordinates[16]
                else:
                    ankle_coord = idx_to_coordinates[15]

                if abs(shoulder_coord[1] - ankle_coord[1]) < 300:
                    performedPushUp = True
                if abs(shoulder_coord[1] - ankle_coord[1]) > 300 and performedPushUp:
                    scount += 1
                    performedPushUp = False
                    ProgressManager.save_progress("Pushup", scount)

            except:
                pass

            if 0 in idx_to_coordinates:
                cv2.putText(image, "Count : " + str(scount),
                            (idx_to_coordinates[0][0] - 60, idx_to_coordinates[0][1] - 140),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.9, color=(0, 0, 0), thickness=2)

            cv2.imshow('Image', rescale_frame(image, percent=100))
            if cv2.waitKey(5) & 0xFF == 27:
                break

        ProgressManager.save_progress("Pushup", scount)  # ← сохраняем прогресс при выходе
        pose.close()
