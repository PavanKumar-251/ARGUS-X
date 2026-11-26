
import cv2


class RecoveryEngine:
    def __init__(self, threshold=0.75, uncertain_threshold=0.45):
        self.threshold = threshold
        self.uncertain_threshold = uncertain_threshold

    def extract_appearance(self, frame, bbox):
        x1, y1, x2, y2 = map(int, bbox)

        height, width = frame.shape[:2]

        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))
        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        crop = frame[y1:y2, x1:x2]

        if crop.size == 0:
            return None

        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

        histogram = cv2.calcHist(
            [hsv], [0, 1], None,
            [30, 32], [0, 180, 0, 256]
        )

        cv2.normalize(
            histogram, histogram,
            alpha=1, norm_type=cv2.NORM_L1
        )

        return histogram

    def compare_appearance(self, old_histogram, new_histogram):
        if old_histogram is None or new_histogram is None:
            return 0.0

        score = cv2.compareHist(
            old_histogram,
            new_histogram,
            cv2.HISTCMP_CORREL
        )

        return max(0.0, min(1.0, float(score)))

    def decide(self, similarity):
        if similarity >= self.threshold:
            return "RECOVERED"
        elif similarity >= self.uncertain_threshold:
            return "UNCERTAIN"
        return "NEW ID"

    def find_match(self, new_histogram, class_name, missing_tracks):
        best_match = None
        best_score = 0.0

        for old_id, old_data in missing_tracks.items():

            if old_data["class_name"] != class_name:
                continue

            old_histogram = old_data.get("appearance")

            score = self.compare_appearance(
                old_histogram,
                new_histogram
            )

            if score > best_score:
                best_score = score
                best_match = old_id

        decision = self.decide(best_score)

        return {
            "decision": decision,
            "old_id": best_match if decision == "RECOVERED" else None,
            "similarity": best_score
        }
