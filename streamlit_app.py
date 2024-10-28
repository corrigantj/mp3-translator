import streamlit as st
import assemblyai as aai
import uuid

# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

aai.settings.api_key = "98520c19b0d64add971e58dadd0e81f5"

# Function to handle highlighting sections
def highlight_transcript(transcript, highlights):
    for highlight in highlights:
        transcript = transcript.replace(highlight["text"], f'**{highlight["text"]}**')
    return transcript

# Streamlit app
def main():
    st.title("MP3/M4A Transcription and Highlight App")

    # Upload MP3 or M4A file
    uploaded_file = st.file_uploader("Upload an MP3 or M4A file", type=['mp3', 'm4a'])

    # Initialize session state for highlights if it doesn't exist
    if "highlights" not in st.session_state:
        st.session_state.highlights = []

    # Get transcript from AssemblyAI
    if uploaded_file is not None:
        if st.button("Get Transcript"):
            with st.spinner("Transcribing audio..."):
                transcriber = aai.Transcriber()
                transcript_data = transcriber.transcribe(uploaded_file)
                if transcript_data.status == aai.TranscriptStatus.error:
                    st.error(transcript_data.error)
                else:
                    transcript = transcript_data.text
                    st.session_state.transcript = transcript
                    st.write(transcript)

    # Highlight sections of the transcript
    if "transcript" in st.session_state:
        transcript = st.session_state.transcript
        selected_text = st.text_input("Highlight Text:", value="")
        tag = st.text_input("Tag for Highlight:", value="")
        comment = st.text_area("Comment for Highlight:", value="")

        if st.button("Add Highlight"):
            if selected_text:
                highlight = {
                    "id": str(uuid.uuid4()),
                    "text": selected_text,
                    "tag": tag,
                    "comment": comment
                }
                st.session_state.highlights.append(highlight)
                st.success("Highlight added.")
            else:
                st.error("Please enter the text to highlight.")

        # Display the highlighted transcript
        highlighted_transcript = highlight_transcript(transcript, st.session_state.highlights)
        st.write(highlighted_transcript)

    # View all highlights separately
    if st.button("View All Highlights"):
        if st.session_state.highlights:
            st.subheader("Highlights")
            for highlight in st.session_state.highlights:
                st.write(f'Text: {highlight["text"]}')
                st.write(f'Tag: {highlight["tag"]}')
                st.write(f'Comment: {highlight["comment"]}')
                st.write("---")
        else:
            st.write("No highlights added yet.")

if __name__ == "__main__":
    main()
