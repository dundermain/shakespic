import os
import openai
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from dotenv import load_dotenv
import base64


app = Flask(__name__)               #it just creates a flask app instance named app

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER               #configures the upload folder to be usable by flask


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')                                 #decorator tells Flask that this function should handle requests to the root URL.
def index():
    return render_template('index.html')

def generate_image_description(file_path):
    with open(file_path, "rb") as image_file:                                 #rb is read in binary mode
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')   #this is encoding for openai api
    
    prompt = f"Provide a description of this image:\n{encoded_image}"
    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        max_tokens=150
    )
    
    # Extract description from response
    description = response.choices[0].text.strip()
    return description

def to_shakespearean_style(description):
    prompt = f"Describe this in the style of William Shakespeare: {description}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

@app.route('/upload', methods=['POST'])                   #decorator tells Flask that this function should handle POST requests to the /upload URL.
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)            #o sanitize the filename and prevent potential security issues.
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        description = generate_image_description(filepath)
        shakespearean_desc = to_shakespearean_style(description)
        
        return jsonify({'description': shakespearean_desc}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    app.run(debug=True)
