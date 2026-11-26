# ARGUS-X — Project Documentation

## 1. Introduction

ARGUS-X (Track the Untrackable) is a computer vision-based multi-object tracking system developed by Team 404 for CLOCKIT 2026.

The project aims to maintain object identities across video sequences, even when objects temporarily disappear and reappear.

It combines object detection, multi-object tracking, identity memory and appearance-based recovery.

## 2. Problem Statement

Traditional tracking systems can experience identity fragmentation due to:

- Object occlusion
- Temporary disappearance
- Similar-looking objects
- Camera movement
- Appearance changes

ARGUS-X attempts to address these challenges using a custom identity-memory and recovery mechanism.

## 3. Objectives

- Detect multiple objects in video frames.
- Track objects across consecutive frames.
- Store historical identity information.
- Compare the appearance of newly detected objects with missing identities.
- Make confidence-based recovery decisions.
- Display tracking results through a dashboard.

## 4. Technologies Used

| Technology | Application |
|---|---|
| Python | Main programming language |
| Streamlit | Frontend framework |
| OpenCV | Video processing and image operations |
| YOLOv8n | Object detection |
| ByteTrack | Multi-object tracking |
| PyTorch | Deep learning framework |
| NumPy | Numerical operations |
| HSV Histogram | Appearance representation |

## 5. System Architecture

The system follows this processing pipeline:

1. Video Input
2. YOLOv8n Object Detection
3. ByteTrack Object Tracking
4. TrackVault Identity Memory
5. Appearance Feature Extraction
6. RecoveryEngine Identity Matching
7. Results Dashboard

## 6. Major Modules

### 6.1 Object Detection

YOLOv8n is used to detect supported object categories, including people and vehicles.

### 6.2 Object Tracking

ByteTrack associates detections across video frames and maintains short-term tracking identities.

### 6.3 TrackVault Identity Memory

TrackVault is a custom module developed for ARGUS-X.

It stores:
- Tracking ID
- Object class
- Last bounding box
- Last-seen frame
- Appearance information
- Tracking status

### 6.4 Appearance Extraction

The system extracts HSV colour histograms from detected object regions.

These histograms provide a visual representation for appearance comparison.

### 6.5 RecoveryEngine

RecoveryEngine compares newly detected object appearance with previously missing identities using OpenCV histogram correlation.

It produces three decisions:

- RECOVERED
- UNCERTAIN
- NEW ID

These decisions are algorithmic estimates and are not guaranteed to represent correct real-world identity matches.

## 7. Frontend and Backend

**Frontend:**
- Streamlit dashboard
- Video upload interface
- Tracking statistics
- Processed video display
- Video download

**Backend:**
- Python
- OpenCV
- YOLOv8n
- ByteTrack
- TrackVault
- RecoveryEngine

## 8. Current Implementation

The current prototype supports:

- Recorded video input
- Object detection
- Multi-object tracking
- Identity memory
- Appearance-based recovery attempts
- Video upload through Streamlit
- Processed video generation
- Results display and download

Live webcam processing has also been implemented experimentally and requires further performance validation.

## 9. Testing

The prototype has been tested with multiple recorded video files.

The tests confirmed that:
- Videos can be opened and processed.
- YOLOv8n detects supported objects.
- ByteTrack generates tracking IDs.
- TrackVault stores identity information.
- The recovery module performs appearance comparisons.
- The video-processing pipeline generates output videos.

Formal recovery accuracy has not yet been established using manually annotated ground truth.

## 10. Limitations

- Similar-looking objects may cause incorrect matches.
- Lighting changes can affect appearance similarity.
- Long occlusions may reduce recovery reliability.
- Camera movement can affect tracking.
- Further evaluation is required to measure recovery accuracy.

## 11. Future Scope

- Integrate stronger Re-identification models.
- Add motion-consistency checks.
- Improve recovery confidence.
- Evaluate using annotated MOT benchmark datasets.
- Improve live webcam performance.
- Add advanced tracking analytics.

## 12. Team Details

| Member | Responsibility |
|---|---|
| Pavan | Development and Team Coordination |
| Dhanush | Research and AI Ideas |
| Chinmay | Documentation and Presentation |
| Vikas | Testing and Bug Reporting |

## 13. Conclusion

ARGUS-X combines object detection, tracking and custom identity memory to attempt long-term object identity recovery.

The project demonstrates a modular computer vision approach to reducing tracking identity fragmentation.

**Developed by Team 404 — CLOCKIT 2026.**
