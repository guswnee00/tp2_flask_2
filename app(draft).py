"""
초기 app.py 
    : 모델 연결 없이 사용자가 업로드한 이미지를 웹에 보여주기
"""

from flask import Flask, render_template, request, flash, redirect, url_for
import os

# 플라스크 클래스명 지정
app = Flask(__name__)

# 에러 페이지
@app.errorhandler(404)
def image_upload_retry(error):
    return render_template('error.html'), 404

# 허용된 확장자 설정
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# 파일 확장자를 체크하는 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 메인 페이지
@app.route('/', methods=['GET', 'POST'])
def main():
    # 메인 페이지 처음 열린 경우
    if request.method == 'GET':
        return render_template('main.html')
    
    # 사용자가 이미지를 업로드한 경우
    if request.method == 'POST': 
        if 'image' in request.files:
            image = request.files['image']

            # 파일이 업로드되지 않은 경우 
            if image.filename == '':
                flash('No selected file. Please choose an image to upload.')
                return image_upload_retry(404)
            
            # 확장자가 허용된 확장자인지 확인
            if not allowed_file(image.filename):
                flash('Invalid file. Please upload a valid image file (jpg, jpeg, png, gif).')
                return image_upload_retry(404)
            
            # 사용자가 업로드한 이미지 저장할 경로 설정 -> 메모리에서 읽어오는 대신 파일로 저장하는 것이 좋음
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok = True)     # 업로드 폴더가 없다면 생성
            image_path = os.path.join(upload_folder, image.filename)
            image.save(image_path)

            # 이미지를 페이지에 띄워주기 위해 이미지 경로를 템플릿으로 전달
            return render_template('main.html', image_path=image_path)
        
# 웹 앱 실행
if __name__ == '__main__':
    app.run(debug=True)