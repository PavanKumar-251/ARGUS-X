
import cv2
from pathlib import Path
from ultralytics import YOLO

from src.identity_memory import TrackVault
from src.recovery import RecoveryEngine


def process_video(video_path, output_path, progress_callback=None):

    video_path = str(video_path)
    output_path = str(output_path)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    model = YOLO("yolov8n.pt")
    vault = TrackVault(max_missing_frames=150)
    recovery = RecoveryEngine()

    id_mapping = {}

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("Cannot open uploaded video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        fps = 25

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps / 2,
        (width, height)
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Cannot create output video")

    frame_number = 0
    recovery_count = 0

    try:
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

                    if raw_id in id_mapping:
                        identity_id = id_mapping[raw_id]

                    elif raw_id in vault.tracks:
                        identity_id = raw_id
                        id_mapping[raw_id] = identity_id

                    else:
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

                        if (
                            match["decision"] == "RECOVERED"
                            and match["old_id"] not in used_identity_ids
                        ):
                            identity_id = match["old_id"]
                            recovery_count += 1

                        else:
                            identity_id = raw_id

                        id_mapping[raw_id] = identity_id

                    used_identity_ids.add(identity_id)
                    current_ids.append(identity_id)

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

            if progress_callback and frame_number % 20 == 0:
                progress_callback(frame_number, total_frames)

    finally:
        cap.release()
        writer.release()

    if progress_callback:
        progress_callback(total_frames, total_frames)

    return {
        "output_path": output_path,
        "recovery_count": recovery_count,
        "total_frames": total_frames,
        "total_identities": len(vault.tracks)
    }
