from flask import Flask, request, redirect
from flask_cors import CORS
import boto3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)  # FlaskアプリケーションにCORSを適用

# AWS情報を設定
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
S3_BUCKET_NAME = "testunity1.0"

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, S3_BUCKET_NAME, filename)
            return redirect('/')
            
if __name__ == '__main__':
    app.run(debug=True)

