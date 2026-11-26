
import cv2

VIDEO_PATH = "videos/input.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Could not open video.")
    raise SystemExit(1)

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("ARGUS-X VIDEO PROCESSOR")
print("-----------------------")
print("Resolution:", width, "x", height)
print("FPS:", fps)
print("Total frames:", total_frames)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("ARGUS-X - Video Input", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Video processing completed.")
