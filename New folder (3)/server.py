from flask import Flask
from flask import render_template
from flask import request
import yt_dlp
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('test.html' )

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/submit", methods=["POST"])
def submit():     
  return f"{request.form.get("link")}"  
   
