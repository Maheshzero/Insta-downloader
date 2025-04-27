from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('test.html')

@app.route("/submit", methods=["POST"])
def submit():
    url = request.form.get('link')

    if not url:
        return "No link provided.", 400

    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(download_folder, exist_ok=True)

    ydl_opts = {
        'quiet': True,
        'format': 'best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        downloaded_file = os.path.join(download_folder, '%(title)s.mp4')

        if os.path.exists(downloaded_file):
            return send_file(
                downloaded_file,
                as_attachment=True,
                download_name="video.mp4",
                mimetype="video/mp4"
            )
        else:
            return "Error: Video file not found after download."

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
