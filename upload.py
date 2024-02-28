from flask import Flask, render_template, request, redirect
import boto3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS情報を設定
AWS_ACCESS_KEY_ID = 'あなたのアクセスキー'
AWS_SECRET_ACCESS_KEY = 'あなたのシークレットキー'
S3_BUCKET_NAME = 'あなたのバケット名'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/')
def upload_form():
    return render_template('upload.html')

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
