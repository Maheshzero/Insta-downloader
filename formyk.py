import streamlit as st
import yt_dlp
import os
from io import BytesIO

st.set_page_config(page_title="Instagram Downloader ", layout="centered")
st.title("📥 Instagram Video Downloader")

insta_url = st.text_input("Paste the Instagram post/reel/video URL:")

if insta_url:
    with st.spinner("Grabbing video details..."):
        try:
            ydl_info_opts = {'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
                info = ydl.extract_info(insta_url, download=False)
                all_formats = info.get("formats", [])

            video_formats = [f for f in all_formats if f.get('vcodec') != 'none']

            if not video_formats:
                st.warning("No downloadable video formats found.")
            else:
                quality_options = []
                for fmt in video_formats:
                    height = fmt.get('height', '?')
                    size = round(fmt.get('filesize', 0) / 1024 / 1024, 2) if fmt.get('filesize') else '?'
                    label = f"{fmt['format_id']} - {height}p - {size} MB"
                    quality_options.append(label)

                choice = st.selectbox("Choose video quality:", quality_options)
                selected_format = video_formats[quality_options.index(choice)]

                if st.button("Download"):
                    st.info("Starting download...")

                    raw_title = info.get("title", "instagram_video")
                    clean_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in raw_title)
                    filename = f"{clean_title}.mp4"

                    ydl_download_opts = {
                        'format': f"{selected_format['format_id']}+bestaudio[ext=m4a]/best",
                        'merge_output_format': 'mp4',
                        'outtmpl': filename,
                        'quiet': True,
                    }

                    try:
                        with yt_dlp.YoutubeDL(ydl_download_opts) as ydl:
                            ydl.download([insta_url])
                    except Exception as err:
                        st.error(f"Download failed: {err}")
                        raise err

                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            video_data = f.read()
                        os.remove(filename)

                        st.success("Video is ready! Click below to save it:")
                        st.download_button(
                            label="📥 Download Video",
                            data=video_data,
                            file_name=filename,
                            mime="video/mp4"
                        )
                    else:
                        st.error("Something went wrong. Video file not found.")

        except Exception as e:
            st.error(f"Error: {e}")

