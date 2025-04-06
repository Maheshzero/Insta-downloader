import streamlit as st
import yt_dlp
import os
from io import BytesIO

st.set_page_config(page_title="Instagram Downloader", layout="centered")
st.title("📥 Instagram Video Downloader (Direct to Browser)")

url = st.text_input("Paste Instagram post/reel/video link:")

if url:
    with st.spinner("Fetching video info..."):
        try:
            # Fetch metadata
            ydl_opts_info = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])

            # Filter video formats
            video_formats = [
                f for f in formats if f.get('vcodec') != 'none'
            ]

            if not video_formats:
                st.warning("No downloadable video formats found.")
            else:
                # Show format options
                quality_labels = []
                for f in video_formats:
                    height = f.get('height', '?')
                    size = round(f.get('filesize', 0) / 1024 / 1024, 2) if f.get('filesize') else '?'
                    label = f"{f['format_id']} - {height}p - {size} MB"
                    quality_labels.append(label)

                selected_quality = st.selectbox("Choose video quality:", quality_labels)
                selected_format = video_formats[quality_labels.index(selected_quality)]

                if st.button("Download"):
                    st.info("Downloading... please wait")

                    # Generate safe filename
                    raw_title = info.get("title", "instagram_video")
                    safe_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in raw_title)
                    filename = f"{safe_title}.mp4"

                    # Download to temp file
                    ydl_download_opts = {
                        'format': f"{selected_format['format_id']}+bestaudio[ext=m4a]/best",
                        'merge_output_format': 'mp4',
                        'outtmpl': filename,
                        'quiet': True,
                    }

                    try:
                        with yt_dlp.YoutubeDL(ydl_download_opts) as ydl:
                            ydl.download([url])
                    except Exception as e:
                        st.error(f"Download failed: {e}")
                        raise e

                    # Confirm file exists and load into memory
                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            video_bytes = f.read()
                        os.remove(filename)

                        st.success("✅ Video ready! Click below to download:")
                        st.download_button(
                            label="📥 Download Now",
                            data=video_bytes,
                            file_name=filename,
                            mime="video/mp4"
                        )
                    else:
                        st.error("❌ Video file not found after download.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
