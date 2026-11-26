
import cv2
import socket
import struct
import numpy as np
import time

from ultralytics import YOLO
from src.identity_memory import TrackVault
from src.recovery import RecoveryEngine

HOST = "172.31.224.1"
PORT = 5000

def recv_exact(conn, size):
    data = bytearray()

    while len(data) < size:
        chunk = conn.recv(size - len(data))

        if not chunk:
            return None

        data.extend(chunk)

    return bytes(data)


print("ARGUS-X LIVE RECEIVER STARTING")

model = YOLO("yolov8n.pt")
vault = TrackVault(max_missing_frames=150)
recovery = RecoveryEngine()

id_mapping = {}
next_identity_id = 1
frame_number = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))

print("WEBCAM CONNECTED")
print("ARGUS-X LIVE TRACKING STARTED")

try:
    while True:
        header = recv_exact(server, 4)

        if header is None:
            break

        message_size = struct.unpack("!I", header)[0]

        if message_size <= 0 or message_size > 5_000_000:
            print("Invalid frame received")
            break

        frame_data = recv_exact(server, message_size)

        if frame_data is None:
            break

        frame = cv2.imdecode(
            np.frombuffer(frame_data, dtype=np.uint8),
            cv2.IMREAD_COLOR
        )

        if frame is None:
            continue

        frame_number += 1

        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0, 2, 3, 5, 7],
            imgsz=416,
            device="cpu",
            verbose=False
        )

        current_ids = set()
        used_identity_ids = set()

        for result in results:
            if result.boxes.id is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()
            raw_ids = result.boxes.id.int().cpu().tolist()
            classes = result.boxes.cls.int().cpu().tolist()

            for bbox, raw_id, class_id in zip(boxes, raw_ids, classes):
                current_ids.add(raw_id)

                class_name = model.names[class_id]
                x1, y1, x2, y2 = map(int, bbox)

                appearance = recovery.extract_appearance(
                    frame, bbox
                )

                if raw_id not in id_mapping:
                    matched_identity = None

                    missing_tracks = vault.get_missing_tracks()

                    decision, old_id, similarity = recovery.find_match(
                        appearance,
                        class_name,
                        missing_tracks
                    )

                    if (
                        decision == "RECOVERED"
                        and old_id not in used_identity_ids
                    ):
                        matched_identity = old_id
                        print(
                            f"RECOVERED: ARGUS ID {old_id} "
                            f"| Similarity: {similarity:.2f}"
                        )

                    if matched_identity is not None:
                        id_mapping[raw_id] = matched_identity
                    else:
                        id_mapping[raw_id] = next_identity_id
                        next_identity_id += 1

                identity_id = id_mapping[raw_id]
                used_identity_ids.add(identity_id)

                vault.update(
                    identity_id,
                    class_name,
                    bbox,
                    frame_number,
                    appearance
                )

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"ARGUS ID: {identity_id}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        vault.update_status(
            set(id_mapping.values()) & {
                id_mapping[rid] for rid in current_ids
                if rid in id_mapping
            },
            frame_number
        )

        cv2.imshow("ARGUS-X LIVE TRACKING", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

except (ConnectionError, OSError) as error:
    print("Connection ended:", error)

finally:
    server.close()
    cv2.destroyAllWindows()
    print("ARGUS-X LIVE RECEIVER STOPPED")
