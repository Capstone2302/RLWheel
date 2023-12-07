import cv2

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
camera.set(cv2.CAP_PROP_FPS, 30)

print(f"Resolution: {camera.get(cv2.CAP_PROP_FRAME_WIDTH)} x {camera.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
print(f"Frame rate: {camera.get(cv2.CAP_PROP_FPS)} FPS")

while True:
    ret, frame = camera.read()
    if not ret:
        break

    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()