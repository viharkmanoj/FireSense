from ultralytics import YOLO
import cv2

# Load your Roboflow-trained YOLO model
model = YOLO("best.pt")

# Example: Webcam detection
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)
    annotated = results[0].plot()
    cv2.imshow("Fire Detection", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
