import cv2

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output.mp4", fourcc, 21, (dispW, dispH))

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("Camera not detected")
        break

    out.write(frame)
    cv2.imshow("Recording Preview", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
out.release()
cv2.destroyAllWindows()
