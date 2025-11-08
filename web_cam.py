import cv2

dispW = 640
dispH = 480
FPS = 30

# 1 = USB webcam (if CSI camera is also connected)
# If only webcam is connected -> change 1 to 0
cam = cv2.VideoCapture(1)

cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
cam.set(cv2.CAP_PROP_FPS, FPS)

while True:
    ret, frame = cam.read()

    if not ret:
        print("Webcam not detected")
        break

    cv2.imshow("USB Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
