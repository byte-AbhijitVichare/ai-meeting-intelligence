import pandas as pd
import streamlit as st
import whisper
import os

from backend.pdf_generator import generate_pdf
from backend.summarizer import (
    summarize_meeting,
    extract_action_items
)

from backend.database import (
    create_database,
    save_meeting,
    get_meetings,
    get_meeting_by_id,
    search_meetings
)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Meeting Intelligence",
    page_icon="🎙️",
    layout="wide"
)

# -----------------------------
# Load Whisper Model
# -----------------------------
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

create_database()

search_query = st.sidebar.text_input(
    "🔍 Search Meetings"
)

st.sidebar.title(
    "📁 Meeting History"
)

if search_query:

    meetings = search_meetings(
        search_query
    )

else:

    meetings = get_meetings()

if "selected_meeting" not in st.session_state:
    st.session_state["selected_meeting"] = None

for meeting in meetings:

    if st.sidebar.button(
        f"{meeting[0]} - {meeting[1]}"
    ):
        st.session_state["selected_meeting"] = meeting[0]

selected_meeting = st.session_state["selected_meeting"]
    
if selected_meeting:

    meeting = get_meeting_by_id(
        selected_meeting
    )

    st.subheader(
        "📄 Saved Meeting"
    )

    st.write(
        f"File: {meeting[0]}"
    )

    st.subheader(
        "Transcript"
    )

    st.text_area(
        "",
        meeting[1],
        height=300
    )

    st.subheader(
        "Summary"
    )

    st.markdown(
        meeting[2]
    )

    st.stop()

# -----------------------------
# Title
# -----------------------------
st.title("🎙️ AI Meeting Intelligence")
st.write("Upload a meeting audio file and generate insights.")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Meeting Audio",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file:

    # Create uploads folder
    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join(
        "uploads",
        uploaded_file.name
    )

    # Save uploaded file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File Uploaded Successfully")

    # Audio Player
    st.audio(uploaded_file)

    # -----------------------------
    # Transcribe Button
    # -----------------------------
    if st.button("Transcribe"):

        with st.spinner("Transcribing Audio..."):

            result = model.transcribe(
                filepath,
                fp16=False,
                word_timestamps=True
            )

            transcript = result["text"]

            st.session_state["transcript"] = transcript

    # -----------------------------
    # Show Transcript
    # -----------------------------
    if "transcript" in st.session_state:

        st.subheader("Transcript")

        st.text_area(
            "Transcript",
            st.session_state["transcript"],
            height=300
        )

        # -----------------------------
        # Generate Summary
        # -----------------------------
        if st.button("Generate AI Summary"):

            with st.spinner("Generating AI Summary..."):

                try:

                    # Summary
                    summary = summarize_meeting(
                        st.session_state["transcript"]
                    )

                    if (
                        not summary.startswith("⚠")
                        and "Error generating summary" not in summary
                    ):
                        
                        save_meeting(
                            uploaded_file.name,
                            st.session_state["transcript"],
                            summary
                        )

                    st.subheader("Meeting Insights")

                    st.markdown(summary)

                    # Action Items
                    action_items = extract_action_items(
                        st.session_state["transcript"]
                    )

                    if action_items:

                        st.subheader("📋 Action Items")

                        df = pd.DataFrame(action_items)

                        if "person" in df.columns:
                            df["person"] = df["person"].replace(
                                "",
                                "Unassigned"
                            )

                        if "deadline" in df.columns:
                            df["deadline"] = df["deadline"].replace(
                                "",
                                "N/A"
                            )

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                    # PDF Export
                    if not summary.startswith("⚠"):

                        pdf_file = generate_pdf(
                            summary,
                            st.session_state["transcript"]
                        )

                        with open(pdf_file, "rb") as file:

                            st.download_button(
                                label="📄 Download PDF Report",
                                data=file,
                                file_name="Meeting_Report.pdf",
                                mime="application/pdf"
                            )

                except Exception as e:

                    st.error(
                        f"Error: {str(e)}"
                    )