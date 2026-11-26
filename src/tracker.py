
import cv2
from ultralytics import YOLO

from src.identity_memory import TrackVault
from src.recovery import RecoveryEngine

VIDEO_PATH = "videos/input.mp4"
OUTPUT_PATH = "output/argus_x_recovery.mp4"

model = YOLO("yolov8n.pt")
vault = TrackVault(max_missing_frames=150)
recovery = RecoveryEngine()

# Maps ByteTrack IDs to persistent TrackVault identities
id_mapping = {}

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise SystemExit("Cannot open input video")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer = cv2.VideoWriter(
    OUTPUT_PATH,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps / 2,
    (width, height)
)

frame_number = 0
recovery_count = 0

print("ARGUS-X IDENTITY RECOVERY STARTED")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_number += 1

    if frame_number % 2 != 0:
        continue

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0, 2, 3, 5, 7],
        imgsz=640,
        device="cpu",
        verbose=False
    )

    boxes = results[0].boxes
    current_ids = []
    used_identity_ids = set()

    output_frame = frame.copy()

    if boxes.id is not None:
        track_ids = boxes.id.int().cpu().tolist()
        class_ids = boxes.cls.int().cpu().tolist()
        coordinates = boxes.xyxy.int().cpu().tolist()

        for raw_id, class_id, bbox in zip(
            track_ids, class_ids, coordinates
        ):
            class_name = model.names[class_id]

            appearance = recovery.extract_appearance(
                frame, bbox
            )

            # Check whether this ByteTrack ID already has a mapping
            if raw_id in id_mapping:
                identity_id = id_mapping[raw_id]

            # Existing TrackVault identity
            elif raw_id in vault.tracks:
                identity_id = raw_id
                id_mapping[raw_id] = identity_id

            else:
                # Search only identities not already assigned
                missing_tracks = {
                    old_id: data
                    for old_id, data in vault.get_missing_tracks().items()
                    if old_id not in used_identity_ids
                }

                match = recovery.find_match(
                    appearance,
                    class_name,
                    missing_tracks
                )

                if match["decision"] == "RECOVERED":
                    identity_id = match["old_id"]
                    recovery_count += 1

                    print(
                        f"RECOVERED: New ID {raw_id} -> "
                        f"Old ID {identity_id} | "
                        f"Similarity: {match['similarity']:.2f}"
                    )
                else:
                    identity_id = raw_id

                    if match["decision"] == "UNCERTAIN":
                        print(
                            f"UNCERTAIN: ID {raw_id} | "
                            f"Similarity: {match['similarity']:.2f}"
                        )

                id_mapping[raw_id] = identity_id

            used_identity_ids.add(identity_id)
            current_ids.append(identity_id)

            # Update the persistent identity memory
            vault.update(
                identity_id,
                class_name,
                bbox,
                frame_number,
                appearance=appearance
            )

            x1, y1, x2, y2 = bbox

            cv2.rectangle(
                output_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                output_frame,
                f"ARGUS ID: {identity_id}",
                (x1, max(20, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    vault.update_status(current_ids, frame_number)

    writer.write(output_frame)

    if frame_number % 150 == 0:
        print("Processed frame:", frame_number)
        vault.show_summary()

cap.release()
writer.release()

print("\nARGUS-X RECOVERY PROCESS COMPLETED")
print("Recovery events:", recovery_count)
vault.show_summary()
print("Saved:", OUTPUT_PATH)
