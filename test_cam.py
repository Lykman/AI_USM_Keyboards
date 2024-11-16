import cv2

def view_camera(camera_index):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Cannot open camera {camera_index}")
        return

    print(f"Showing camera {camera_index}. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Can't receive frame from camera {camera_index}. Exiting...")
            break

        cv2.imshow(f'Camera {camera_index}', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Просмотр всех доступных камер
max_cameras = 5
for i in range(max_cameras):
    print(f"\nAttempting to open camera {i}")
    view_camera(i)
