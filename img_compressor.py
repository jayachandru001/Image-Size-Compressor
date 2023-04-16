from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from flask import send_file

import os

app = Flask(__name__)

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = './static/compressed'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    # Check if the file extension is allowed
    return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def compress_image(input_path, output_path, desired_size, desired_byte_format):
    # Open the input image
    with Image.open(input_path) as img:
        # Calculate the initial size of the image
        size = os.path.getsize(input_path)
        # Convert the desired size to bytes
        if desired_byte_format == 'KB':
            desired_size = int(desired_size.replace("KB", "")) * 1024
        elif desired_byte_format == 'MB':
            desired_size = int(desired_size.replace("MB", "")) * 1024 * 1024
        elif desired_byte_format == 'GB':
            desired_size = int(desired_size.replace("GB", "")) * 1024 * 1024 * 1024
        else:
            raise ValueError("Invalid size format! Use KB, MB or GB.")
        
        # If the image size is already smaller than the desired size, return the input image
        if size < desired_size:
            return img
        
        # Initialize the quality parameter
        quality = 100
        
        # Compress the image until the desired size is reached
        while size > desired_size:
            if quality <= 0:
                break
            img.save(output_path, "JPEG", quality=quality)
            size = os.path.getsize(output_path)
            quality -= 5
        
        # Return the compressed image
        return img

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        print("1 clear")
        file = request.files['file']
        
        # If the user does not select a file, submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Save the uploaded file to the uploads folder
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            print("2")
            # Compress the image and save it to the uploads folder with a "_compressed" suffix
            output_path = os.path.join(app.config['COMPRESSED_FOLDER'], os.path.splitext(filename)[0] + "_compressed.jpg")
            desired_size = request.form['size']
            desired_byte_format = request.form['option']
            compress_image(input_path, output_path, desired_size, desired_byte_format)
            
            # Return the download link for the compressed image
            return render_template('./result.html', filename=os.path.basename(output_path))
            
    return render_template('./index.html')

'''
@app.route('/static/compressed/<filename>')
def download(filename):
    # Get the path to the compressed image file
    compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if the compressed image file exists
    if not os.path.exists(compressed_path):
        return "Error: File not found"
    
    # Return the compressed image file for download
    return send_file(compressed_path, as_attachment=True)
'''
@app.route('/static/compressed/<filename>')
def download(filename):
    # Return the download link for the compressed image
    #path = output_path
    #return send_file(path, as_attachment=True)
    path = os.path.join(app.config['COMPRESSED_FOLDER'], filename)
    # Return the file for download
    return send_file(path, as_attachment=True)
    #return redirect(url_for('static', filename=os.path.join('compressed/', filename)), code=301)

if __name__ == '__main__':
    app.run(debug=True)
