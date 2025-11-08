import cv2

def nothing(x):
    pass

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

cv2.namedWindow("Live")

cv2.createTrackbar("X Pos", "Live", 0, dispW, nothing)
cv2.createTrackbar("Y Pos", "Live", 0, dispH, nothing)
cv2.createTrackbar("Width", "Live", 0, dispW, nothing)
cv2.createTrackbar("Height", "Live", 0, dispH, nothing)

while True:
    ret, frame = cam.read()

    if not ret:
        break

    x = cv2.getTrackbarPos("X Pos", "Live")
    y = cv2.getTrackbarPos("Y Pos", "Live")
    w = cv2.getTrackbarPos("Width", "Live")
    h = cv2.getTrackbarPos("Height", "Live")

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Live", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
