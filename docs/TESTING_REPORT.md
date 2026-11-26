# ARGUS-X — Testing Report

## 1. Introduction

This document describes the testing performed on the ARGUS-X multi-object tracking prototype developed by Team 404.

## 2. Testing Environment

| Component | Configuration |
|---|---|
| Operating System | Windows with Kali Linux WSL |
| Programming Language | Python |
| Processor | Snapdragon X |
| Detection Model | YOLOv8n |
| Tracking Algorithm | ByteTrack |
| Video Processing | OpenCV |
| Frontend | Streamlit |

## 3. Test Cases

| Test ID | Test Description | Observed Result |
|---|---|---|
| TC01 | Open input video | Successful |
| TC02 | Read video frames | Successful |
| TC03 | Detect objects using YOLOv8n | Successful |
| TC04 | Track objects using ByteTrack | Successful |
| TC05 | Store identity information in TrackVault | Successful |
| TC06 | Extract HSV appearance histograms | Implemented and tested |
| TC07 | Compare appearance histograms | Implemented and tested |
| TC08 | Process uploaded videos through the pipeline | Successful |
| TC09 | Generate processed output video | Successful |
| TC10 | Display results through Streamlit | Processing functionality tested; final interface requires validation |

## 4. Observations

- YOLOv8n successfully detected supported objects in test videos.
- ByteTrack generated tracking IDs for detected objects.
- TrackVault stored object identity information.
- The recovery module performed appearance similarity comparisons.
- The video-processing pipeline generated processed video files.
- Multiple recorded videos were successfully processed.

## 5. Limitations Identified

- Similar-looking objects can cause incorrect appearance matches.
- Lighting changes can affect HSV histogram similarity.
- Long occlusions can make recovery difficult.
- Live webcam performance requires further optimization.
- Formal recovery accuracy has not been measured against manually annotated ground truth.

## 6. Future Testing

Further testing is planned for:

- Long-duration occlusion.
- Similar-looking objects.
- Camera movement.
- Appearance and lighting changes.
- Annotated MOT benchmark datasets.
- Identity switches and recovery accuracy.

## 7. Conclusion

Initial testing confirms that the main ARGUS-X detection, tracking, identity-memory and video-processing components are implemented and working in the tested scenarios.

Further evaluation is required to establish identity recovery accuracy and reliability.

**Team 404 — CLOCKIT 2026.**
