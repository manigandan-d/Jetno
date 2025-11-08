import cv2
import time

dispW = 640
dispH = 480
flip = 2
FPS=30

# CSI CAMERA (index = 0)
gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam_csi = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

# USB WEBCAM (index = 1) - change to 0 if only webcam connected
cam_usb = cv2.VideoCapture(1)
cam_usb.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam_usb.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
cam_usb.set(cv2.CAP_PROP_FPS, FPS)

if not cam_csi.isOpened() or not cam_usb.isOpened():
    print("Camera not detected")
    exit()

while True:
    ret1, frame_csi = cam_csi.read()
    ret2, frame_usb = cam_usb.read()

    if not ret1 or not ret2:
        print("Failed to read from camera(s)")
        break

    gray_csi = cv2.cvtColor(frame_csi, cv2.COLOR_BGR2GRAY)
    gray_usb = cv2.cvtColor(frame_usb, cv2.COLOR_BGR2GRAY)

    cv2.imshow("CSI - Normal", frame_csi)
    cv2.moveWindow("CSI - Normal", 0, 0)

    cv2.imshow("CSI - Gray", gray_csi)
    cv2.moveWindow("CSI - Gray", 0, dispH + 40)

    cv2.imshow("USB - Normal", frame_usb)
    cv2.moveWindow("USB - Normal", dispW + 40, 0)

    cv2.imshow("USB - Gray", gray_usb)
    cv2.moveWindow("USB - Gray", dispW + 40, dispH + 40)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam_csi.release()
cam_usb.release()
cv2.destroyAllWindows()
