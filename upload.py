from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

# AWS情報を設定
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
S3_BUCKET_NAME = "testunity1.0"
AWS_REGION = "ap-northeast-3"  # 適切なリージョンに変更してください

s3 = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        custom_name = request.form.get('custom_name', '')
        filename = secure_filename(custom_name if custom_name else file.filename)
        folder_name = 'uploads/'
        full_file_name = os.path.join(folder_name, filename)
        
        if file:
            s3.upload_fileobj(file, S3_BUCKET_NAME, full_file_name)
            file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{full_file_name}"
            return jsonify({"message": "Upload successful", "file_url": file_url})

    return jsonify({"message": "Upload failed"}), 400

if __name__ == '__main__':
    app.run(debug=True)

