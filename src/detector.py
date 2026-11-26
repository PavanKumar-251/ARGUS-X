
import cv2
from ultralytics import YOLO

VIDEO_PATH = "videos/input.mp4"
OUTPUT_PATH = "output/detection.mp4"

# Load a lightweight YOLO model
model = YOLO("yolov8n.pt")

# COCO classes:
# 0 = Person, 2 = Car, 3 = Motorcycle
# 5 = Bus, 7 = Truck
target_classes = [0, 2, 3, 5, 7]

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise SystemExit("ERROR: Cannot open input video")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Process every third frame to reduce CPU workload
writer = cv2.VideoWriter(
    OUTPUT_PATH,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps / 3,
    (width, height)
)

frame_number = 0
total_detected = 0

print("ARGUS-X OBJECT DETECTION STARTED")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_number += 1

    if frame_number % 3 != 0:
        continue

    results = model.predict(
        frame,
        classes=target_classes,
        imgsz=640,
        device="cpu",
        verbose=False
    )

    annotated_frame = results[0].plot()
    total_detected += len(results[0].boxes)

    writer.write(annotated_frame)

    if frame_number % 150 == 0:
        print("Processed frames:", frame_number)

cap.release()
writer.release()

print("DETECTION COMPLETED")
print("Detected objects:", total_detected)
print("Saved result:", OUTPUT_PATH)
