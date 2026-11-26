
import streamlit as st
import sys
from pathlib import Path

# Add ARGUS-X project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.tracking_pipeline import process_video

st.set_page_config(
    page_title="ARGUS-X",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 ARGUS-X")
st.subheader("Long-Horizon Multi-Object Identity Tracking")

st.markdown("---")

st.sidebar.title("ARGUS-X Menu")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Video Tracking", "About"]
)

# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Detection", "YOLOv8n")
    col2.metric("Tracking", "ByteTrack")
    col3.metric("Identity Memory", "TrackVault")

    st.markdown("### Project Overview")

    st.write(
        "ARGUS-X maintains object identities across video "
        "sequences using detection, tracking and identity recovery."
    )

    st.success("ARGUS-X frontend is running!")

# ---------------- VIDEO TRACKING ----------------

elif page == "Video Tracking":

    st.header("Upload and Track Video")

    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=["mp4", "avi", "mov", "mkv"]
    )

    if uploaded_file is not None:

        st.video(uploaded_file)
        st.write("Selected video:", uploaded_file.name)

        if st.button("START TRACKING", type="primary"):

            upload_dir = ROOT_DIR / "videos" / "uploads"
            output_dir = ROOT_DIR / "output"

            upload_dir.mkdir(parents=True, exist_ok=True)
            output_dir.mkdir(parents=True, exist_ok=True)

            safe_name = Path(uploaded_file.name).name
            input_path = upload_dir / safe_name

            output_path = output_dir / (
                input_path.stem + "_argus_x_recovery.mp4"
            )

            input_path.write_bytes(uploaded_file.getbuffer())

            progress_bar = st.progress(0)
            status_text = st.empty()

            def update_progress(current, total):
                if total > 0:
                    progress_bar.progress(
                        min(current / total, 1.0)
                    )
                    status_text.write(
                        f"Processing frames: {current} / {total}"
                    )

            try:

                with st.spinner(
                    "ARGUS-X is processing your video..."
                ):

                    result = process_video(
                        str(input_path),
                        str(output_path),
                        update_progress
                    )

                st.success(
                    "ARGUS-X tracking completed successfully!"
                )

                st.markdown("---")
                st.header("📊 Tracking Results")

                # Tracking statistics
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Total Frames",
                    f"{result['total_frames']:,}"
                )

                col2.metric(
                    "Total Identities",
                    result["total_identities"]
                )

                col3.metric(
                    "Recovery Events",
                    result["recovery_count"]
                )

                st.markdown("---")

                # Video comparison
                st.subheader("🎬 Video Comparison")

                original_col, processed_col = st.columns(2)

                with original_col:
                    st.markdown("**Original Video**")
                    st.video(str(input_path))

                with processed_col:
                    st.markdown("**ARGUS-X Processed Video**")
                    st.video(str(output_path))

                st.markdown("---")

                # Identity recovery summary
                st.subheader("🧠 Identity Recovery Summary")

                recovery_col, identity_col = st.columns(2)

                with recovery_col:
                    st.metric(
                        "Recovery Events",
                        result["recovery_count"]
                    )

                with identity_col:
                    st.metric(
                        "Tracked Identities",
                        result["total_identities"]
                    )

                st.info(
                    "ARGUS-X uses appearance similarity and identity "
                    "memory to attempt identity recovery. Recovery "
                    "events are not necessarily verified correct matches."
                )

                # Download result
                st.markdown("---")
                st.subheader("📥 Export Results")

                with open(output_path, "rb") as video_file:

                    st.download_button(
                        label="Download Processed Video",
                        data=video_file,
                        file_name=output_path.name,
                        mime="video/mp4",
                        type="primary"
                    )

                st.caption(
                    "ARGUS-X | Team 404 | Computer Vision Tracking System"
                )

            except Exception as error:

                st.error(f"Tracking failed: {error}")

# ---------------- ABOUT ----------------

elif page == "About":

    st.header("About ARGUS-X")

    st.write("""
    **Project:** ARGUS-X - Track the Untrackable

    **Team:** Team 404

    **Technologies:**
    - Python
    - OpenCV
    - YOLOv8n
    - ByteTrack
    - TrackVault Identity Memory
    - Appearance-based Recovery
    """)
