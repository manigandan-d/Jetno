import cv2

dispW = 1280
dispH = 720
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

    resized_frame = cv2.resize(frame, (640, 480))
    resized_half = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    resized_quality = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)

    cv2.imshow("Resized Frame", resized_frame)
    cv2.imshow("Resized Half", resized_half)
    cv2.imshow("Quality Shrink", resized_quality)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
