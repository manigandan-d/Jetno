import cv2

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

x, y = 50, 50           
w, h = 150, 80         
dx, dy = 5, 5 

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("Camera not detected")
        break

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)

    x += dx
    y += dy

    if x <= 0 or x + w >= dispW:
        dx = -dx
    if y <= 0 or y + h >= dispH:
        dy = -dy

    cv2.imshow("Moving Rectangle", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
