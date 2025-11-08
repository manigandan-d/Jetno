import cv2

DISP_W = 640
DISP_H = 480
FLIP = 2

GSTREAMER_PIPELINE = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! "
    f"nvvidconv flip-method={FLIP} ! "
    f"video/x-raw, width={DISP_W}, height={DISP_H}, format=BGRx ! "
    "videoconvert ! video/x-raw, format=BGR ! appsink"
)

cam = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
if not cam.isOpened():
    raise Exception("ERROR: CSI Camera not detected")

logo = cv2.imread("python_logo.jpeg")
if logo is None:
    raise FileNotFoundError("ERROR: python_logo.jpeg not found in working directory")

LOGO_W, LOGO_H = 75, 75
logo = cv2.resize(logo, (LOGO_W, LOGO_H))

logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)

_, bg_mask = cv2.threshold(logo_gray, 230, 255, cv2.THRESH_BINARY)
fg_mask = cv2.bitwise_not(bg_mask)

logo_fg = cv2.bitwise_and(logo, logo, mask=fg_mask)

x, y = 10, 10       
dx, dy = 3, 3   
box_w, box_h = LOGO_W, LOGO_H

while True:
    ret, frame = cam.read()

    if not ret:
        print("Camera frame not received")
        break

    roi = frame[y:y+box_h, x:x+box_w]

    roi_bg = cv2.bitwise_and(roi, roi, mask=bg_mask)

    roi_combined = cv2.add(logo_fg, roi_bg)

    frame[y:y+box_h, x:x+box_w] = roi_combined

    # cv2.rectangle(frame, (x, y), (x + box_w, y + box_h), (0, 255, 0), 1)

    x += dx
    y += dy

    if x <= 0 or x + box_w >= DISP_W:
        dx = -dx
    if y <= 0 or y + box_h >= DISP_H:
        dy = -dy

    cv2.imshow("Bouncing Watermark", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
