import streamlit as st
import os
import yt_dlp
import tempfile

st.title("🎵 YouTube to MP3 Downloader")
st.markdown("Paste a YouTube link below to download its audio as an MP3 file.")

video_url = st.text_input("🎬 YouTube URL")

if st.button("Download MP3"):
    if not video_url:
        st.warning("Please enter a YouTube URL.")
    else:
        try:
            with st.spinner("Fetching video info..."):
                with yt_dlp.YoutubeDL() as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    title = info.get('title', 'untitled')
                    title = title.replace("|", "_").replace(":", "_").strip()

            with tempfile.TemporaryDirectory() as tmpdir:
                mp3_path = os.path.join(tmpdir, f"{title}.mp3")

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(tmpdir, f"{title}.%(ext)s"),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'quiet': True,
                    'noplaylist': True,
                }

                with st.spinner("Downloading and converting to MP3..."):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([video_url])

                with open(mp3_path, "rb") as f:
                    st.success("Download complete!")
                    st.download_button(
                        label="🎧 Download MP3 File",
                        data=f,
                        file_name=f"{title}.mp3",
                        mime="audio/mpeg"
                    )

        except Exception as e:
            st.error(f"Error: {e}")
