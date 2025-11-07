import cv2

print("=== Открываем камеру ===")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("=== Ошибка: камера не открылась ===")
else:
    print("=== Камера открыта ===")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("=== Ошибка чтения кадра ===")
            break

        cv2.imshow("Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
