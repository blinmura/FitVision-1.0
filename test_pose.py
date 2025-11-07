import mediapipe as mp

print("=== Импорт mediapipe успешен ===")

try:
    mp_pose = mp.solutions.pose
    print("=== Модуль solutions.pose найден ===")

    pose = mp_pose.Pose(model_complexity=1)
    print("=== Pose успешно инициализирован ===")

except Exception as e:
    print("=== Ошибка при инициализации Pose ===")
    print(e)
