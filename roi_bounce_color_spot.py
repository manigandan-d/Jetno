import cv2

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

x, y = 50, 50         
w, h = 150, 100       
dx, dy = 5, 5         

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR) 

    if x + w >= frame.shape[1] or x <= 0:
        dx = -dx
    if y + h >= frame.shape[0] or y <= 0:
        dy = -dy

    x += dx
    y += dy

    roi_color = frame[y:y+h, x:x+w]
    gray[y:y+h, x:x+w] = roi_color

    cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("ROI Bounce", gray)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
