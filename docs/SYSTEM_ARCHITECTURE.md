# ARGUS-X — System Architecture

## 1. Architecture Overview

ARGUS-X follows a modular computer vision pipeline for multi-object detection, tracking and identity recovery.

The system processes video frames and uses object appearance information and stored identity history to attempt to recover previously missing tracking identities.

## 2. System Workflow

```text
       VIDEO INPUT
            |
            v
     OPENCV PROCESSING
            |
            v
      YOLOv8n DETECTION
            |
            v
       BYTETRACK
            |
            v
   TRACKVAULT IDENTITY MEMORY
            |
            v
   HSV APPEARANCE EXTRACTION
            |
            v
     RECOVERY ENGINE
            |
            v
   RECOVERY DECISION
    /       |       \
RECOVERED UNCERTAIN NEW ID
            |
            v
    PROCESSED VIDEO
            |
            v
    STREAMLIT DASHBOARD
```

## 3. Main Components

### 3.1 Video Input

OpenCV reads the input video and extracts individual frames for processing.

### 3.2 Object Detection — YOLOv8n

YOLOv8n detects supported object categories in each processed frame and provides bounding-box coordinates and class information.

### 3.3 Object Tracking — ByteTrack

ByteTrack associates detections across consecutive frames and assigns tracking IDs.

### 3.4 TrackVault — Identity Memory

TrackVault is the custom identity-memory component of ARGUS-X.

It stores:
- Object tracking ID
- Object category
- Last bounding box
- Last-seen frame
- Appearance information
- Current tracking status

Objects can be maintained as ACTIVE, MISSING or EXPIRED according to their tracking history.

### 3.5 Appearance Extraction

The RecoveryEngine extracts an HSV colour histogram from the detected object's image region.

This histogram is used as an appearance representation.

### 3.6 Identity Recovery

The recovery module compares the new object's histogram with stored missing identities using OpenCV histogram correlation.

The system makes one of three decisions:

- RECOVERED — similarity meets the recovery threshold.
- UNCERTAIN — similarity falls into the uncertain range.
- NEW ID — no suitable recovery match is found.

These decisions are estimates and require further validation.

### 3.7 Results Dashboard

Streamlit provides the user interface for:

- Video uploading
- Starting video processing
- Displaying tracking statistics
- Comparing original and processed videos
- Downloading processed results

## 4. Technologies and Their Roles

| Technology | Role |
|---|---|
| Python | Application development |
| OpenCV | Video and image processing |
| YOLOv8n | Object detection |
| ByteTrack | Multi-object tracking |
| PyTorch | Deep learning framework |
| NumPy | Numerical operations |
| Streamlit | Frontend dashboard |

## 5. Data Flow

1. The user uploads a video.
2. OpenCV reads the video frames.
3. YOLOv8n detects objects.
4. ByteTrack tracks detected objects.
5. TrackVault maintains identity information.
6. The recovery module compares object appearance.
7. Recovery decisions are used to assign persistent ARGUS IDs.
8. The processed video and statistics are displayed in Streamlit.

## 6. Conclusion

ARGUS-X combines object detection, multi-object tracking and custom identity memory in a modular architecture.

Its main contribution is the TrackVault identity-memory and appearance-based recovery approach, which attempts to reduce tracking identity fragmentation.

**Developed by Team 404 — CLOCKIT 2026.**
