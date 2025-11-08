import cv2

video = cv2.VideoCapture("output.mp4")

while True:
    ret, frame = video.read()
    
    if not ret:
        print("Video finished or cannot read frame.")
        break

    cv2.imshow("Video Playback", frame)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
