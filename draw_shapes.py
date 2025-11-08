import cv2

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("Camera not detected")
        break

    cv2.rectangle(frame, (50, 50), (300, 200), (0, 255, 0), 2)

    cv2.circle(frame, (400, 200), 60, (255, 0, 0), 2)

    cv2.line(frame, (50, 300), (500, 300), (0, 0, 255), 3)

    cv2.arrowedLine(frame, (50, 400), (500, 400), (0, 255, 255), 3)

    cv2.imshow("Shapes", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
