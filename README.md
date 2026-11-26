# ARGUS-X — Track the Untrackable

**Long-Horizon Multi-Object Identity Tracking and Recovery**

Developed by **Team 404** for CLOCKIT 2026.

## About the Project

ARGUS-X is a computer vision-based system designed to track multiple objects across video sequences and attempt to recover their identities after temporary disappearance.

It combines object detection, multi-object tracking, identity memory and appearance-based matching.

## Key Features

- Object detection using YOLOv8n.
- Multi-object tracking using ByteTrack.
- Custom TrackVault identity memory.
- HSV histogram-based appearance extraction.
- Appearance similarity comparison using OpenCV.
- Recovery decisions: RECOVERED, UNCERTAIN and NEW ID.
- Streamlit dashboard for video processing and results.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Frontend framework |
| OpenCV | Video and image processing |
| YOLOv8n | Object detection |
| ByteTrack | Object tracking |
| PyTorch | Deep learning framework |
| NumPy | Numerical operations |

## Project Structure

```text
ARGUS-X/
├── dashboard/
│   └── app.py
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   ├── SYSTEM_ARCHITECTURE.md
│   └── TESTING_REPORT.md
├── src/
│   ├── detector.py
│   ├── identity_memory.py
│   ├── live_receiver.py
│   ├── main.py
│   ├── recovery.py
│   ├── tracker.py
│   └── tracking_pipeline.py
├── webcam_sender.py
├── yolov8n.pt
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/PavanKumar-251/ARGUS-X.git
cd ARGUS-X
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
streamlit run dashboard/app.py
```

Upload a video through the Video Tracking page and start processing.

## Identity Recovery Workflow

1. Video input
2. YOLOv8n object detection
3. ByteTrack tracking
4. TrackVault identity memory
5. HSV appearance extraction
6. RecoveryEngine matching
7. Processed video and dashboard results

## Limitations

Appearance-based matching can produce incorrect matches, especially with similar-looking objects, lighting changes and prolonged occlusion. Recovery decisions are estimates and require further validation.

## Documentation

Detailed project documents are available in the `docs/` folder:

- Project Documentation
- System Architecture
- Testing Report

## Team 404

| Member | Responsibility |
|---|---|
| Pavan | Development and Team Coordination |
| Dhanush | Research and AI Ideas |
| Chinmay | Documentation and Presentation |
| Vikas | Testing and Bug Reporting |

**CLOCKIT 2026 — ARGUS-X**
