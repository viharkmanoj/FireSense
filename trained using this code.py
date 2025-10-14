from ultralytics import YOLO
import cv2

# Load your trained YOLO model
model = YOLO("/Users/manojvihar/Developer/Fire/train/weights/best.pt")  # change path if needed

# Input video path
video_path = "/Users/manojvihar/Desktop/small to big fire.mp4"  # replace with your video file

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get video details
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up video writer to save output
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# Run detection on each frame
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run inference
    results = model(frame)

    # Draw boxes and labels on the frame
    annotated_frame = results[0].plot()

    # Write to output file
    out.write(annotated_frame)

    # Show the video during processing (optional)
    cv2.imshow("YOLOv8 Video Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
