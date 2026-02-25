import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Initialize the app and specify the template folder as 'frontpage'
app = Flask(__name__, template_folder='frontpage')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload/image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return 'No selected file or invalid format'
        
        # Save file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"Image '{filename}' uploaded successfully! (Ready for Deepfake Analysis)"
        
    return render_template('upload_image.html')

@app.route('/upload/video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return 'No selected file or invalid format'
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"Video '{filename}' uploaded successfully! (Ready for Deepfake Analysis)"
        
    return render_template('upload_video.html')

if __name__ == '__main__':
    app.run(debug=True)
