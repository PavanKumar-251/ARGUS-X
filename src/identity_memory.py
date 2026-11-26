
class TrackVault:
    def __init__(self, max_missing_frames=150):
        self.tracks = {}
        self.max_missing_frames = max_missing_frames

    def update(self, track_id, class_name, bbox, frame_number,
               appearance=None):

        old_data = self.tracks.get(track_id, {})

        self.tracks[track_id] = {
            "track_id": track_id,
            "class_name": class_name,
            "last_bbox": bbox,
            "last_seen": frame_number,
            "status": "ACTIVE",
            "appearance": (
                appearance if appearance is not None
                else old_data.get("appearance")
            ),
            "total_seen": old_data.get("total_seen", 0) + 1
        }

    def update_status(self, current_ids, frame_number):
        for track_id, data in self.tracks.items():
            if track_id in current_ids:
                data["status"] = "ACTIVE"
            else:
                missing = frame_number - data["last_seen"]

                if missing <= self.max_missing_frames:
                    data["status"] = "MISSING"
                else:
                    data["status"] = "EXPIRED"

    def get_missing_tracks(self):
        return {
            track_id: data
            for track_id, data in self.tracks.items()
            if data["status"] == "MISSING"
        }

    def show_summary(self):
        active = sum(
            t["status"] == "ACTIVE"
            for t in self.tracks.values()
        )
        missing = sum(
            t["status"] == "MISSING"
            for t in self.tracks.values()
        )

        print("TRACKVAULT MEMORY")
        print("Total identities:", len(self.tracks))
        print("Active tracks:", active)
        print("Missing tracks:", missing)
