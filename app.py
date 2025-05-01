from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import boto3
from botocore.exceptions import NoCredentialsError
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

s3 = boto3.client(
    's3',
    aws_access_key_id=app.config['S3_ACCESS_KEY'],
    aws_secret_access_key=app.config['S3_SECRET_KEY']
)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            s3.upload_fileobj(file, app.config['S3_BUCKET'], filename)
            flash('File uploaded successfully')
            return redirect(url_for('index'))
        except NoCredentialsError:
            flash('Credentials not available')
            return redirect(request.url)
    
    flash('File type not allowed')
    return redirect(request.url)

@app.route('/files')
def list_files():
    files = s3.list_objects_v2(Bucket=app.config['S3_BUCKET'])
    file_urls = []
    if 'Contents' in files:
        for file in files['Contents']:
            file_urls.append(app.config['S3_LOCATION'] + file['Key'])
    return render_template('files.html', files=file_urls)

if __name__ == '__main__':
    app.run(debug=True)