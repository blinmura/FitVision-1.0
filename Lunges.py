import mediapipe as mp
from src.ThreadedCamera import ThreadedCamera
from src.exercies.Exercise import Exercise
import time
from src.utils import *
from progress_manager import ProgressManager

import os
import json

# ==== Прогресс: загрузка и сохранение ====
PROGRESS_FILE = "progress.json"

'''def load_progress(exercise_name):
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f).get(exercise_name, 0)
    return 0

def save_progress(exercise_name, count):
    progress = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)
    progress[exercise_name] = count
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)
'''
# ==== MediaPipe и начальные параметры ====
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255))
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
PRESENCE_THRESHOLD = 0.5
VISIBILITY_THRESHOLD = 0.5


class Lunges(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        ang1 = 0
        ang2 = 0
        count = int(ProgressManager.load_progress().get("Lunges", 0))  # <--- Загружаем сохранённый прогресс
        frames = 0
        performedLunge = False
        while True:
            success, image = threaded_camera.show_frame()
            if not success or image is None:
                print("Кадр не получен")
                continue
            print("Кадр получен")
            image = cv2.flip(image, 1)
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
                if 23 in idx_to_coordinates and 25 in idx_to_coordinates and 27 in idx_to_coordinates:
                    cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[25]), thickness=6, color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[25]), (idx_to_coordinates[27]), thickness=6, color=(255, 0, 0))
                    ang1 = ang((idx_to_coordinates[23], idx_to_coordinates[25]),
                               (idx_to_coordinates[25], idx_to_coordinates[27]))
                    cv2.putText(image, str(round(ang1, 2)),
                                (idx_to_coordinates[25][0] - 40, idx_to_coordinates[25][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, (idx_to_coordinates[23]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[25]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[27]), 10, (0, 0, 255), cv2.FILLED)
                if 24 in idx_to_coordinates and 26 in idx_to_coordinates and 28 in idx_to_coordinates:
                    cv2.line(image, (idx_to_coordinates[24]), (idx_to_coordinates[26]), thickness=6, color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[26]), (idx_to_coordinates[28]), thickness=6, color=(255, 0, 0))
                    ang2 = ang((idx_to_coordinates[24], idx_to_coordinates[26]),
                               (idx_to_coordinates[26], idx_to_coordinates[28]))
                    cv2.putText(image, str(round(ang2, 2)),
                                (idx_to_coordinates[26][0] - 40, idx_to_coordinates[26][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
            except:
                pass

            try:
                frames += 1

                # Используем более строгие условия и проверку устойчивости
                if 50 < ang1 < 100 and not performedLunge:
                    performedLunge = True  # начало выпада
                    stable_frames = 0  # для фиксации устойчивости

                if performedLunge:
                    stable_frames += 1

                    # Если колено разогнулось и мы стабильно удерживали "низ" не менее 5 кадров
                    if ang1 > 150 and stable_frames > 5:
                        count += 1
                        performedLunge = False
                        ProgressManager.save_progress("Lunges", count)
                        print(f"Lunge detected, total: {count}")

            except Exception as e:
                print("Ошибка счётчика:", e)

                ang1 = 180 - ang1
                c1 = (0, 255, 0) if ang1 > 70 else (255, 0, 0)
                barLeft = np.interp(ang1, (10, 70), (850, 300))
                perLeft = np.interp(ang1, (10, 70), (0, 100))
                cv2.rectangle(image, (550, 300), (610, 850), c1)
                cv2.rectangle(image, (550, int(barLeft)), (610, 850), c1, cv2.FILLED)
                cv2.putText(image, f'{int(perLeft)} %', (550, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.1, color=c1, thickness=4)

                ang2 = 180 - ang2
                c2 = (0, 255, 0) if ang2 > 40 else (255, 0, 0)
                barRight = np.interp(ang2, (10, 40), (850, 300))
                perRight = np.interp(ang2, (10, 40), (0, 100))
                cv2.rectangle(image, (1400, 300), (1460, 850), c2)
                cv2.rectangle(image, (1400, int(barRight)), (1460, 850), c2, cv2.FILLED)
                cv2.putText(image, f'{int(perRight)} %', (1400, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.1, color=c2, thickness=4)

            except:
                pass

            if 0 in idx_to_coordinates:
                cv2.putText(image, "Lunges : " + str(round(count)),
                            (idx_to_coordinates[0][0] - 40, idx_to_coordinates[0][1] + 290),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.2, color=(0, 255, 0), thickness=5)
            cv2.imshow('Image', rescale_frame(image, percent=150))
            if cv2.waitKey(5) & 0xFF == 27:
                break

        ProgressManager.save_progress("Lunges", count) # <--- Сохраняем прогресс при выходе
        pose.close()
