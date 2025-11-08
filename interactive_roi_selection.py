import cv2

drawing = False
ix, iy = -1, -1
roi = None

def mouse_event(event, x, y, flags, param):
    global ix, iy, drawing, frame, roi

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        temp_frame = frame.copy()
        cv2.rectangle(temp_frame, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow("Live", temp_frame)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi = frame[min(iy,y):max(iy,y), min(ix,x):max(ix,x)]
        print("ROI Selected!")
        cv2.imshow("ROI", roi)

dispW = 640
dispH = 480
flip = 2

gst_pipeline = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! \
          nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! \
          videoconvert ! video/x-raw, format=BGR ! appsink'

cam = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

cv2.namedWindow("Live")
cv2.setMouseCallback("Live", mouse_event)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("Live", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
