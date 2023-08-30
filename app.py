"""
1차 완성본
    : yolo모델(best_1.pt) 연결해 사용자가 업로드한 이미지를 모델에 넣고 예측
      원본 이미지와 예측 이미지를 함께 볼 수 있도록 함
"""

import os
from flask import Flask, render_template, request, flash
from prediction_utils import allowed_file, load_yolo_model, predict_image

# 플라스크 클래스명 지정
app = Flask(__name__, static_folder='static')

# 에러 페이지
@app.errorhandler(404)
def image_upload_retry(error):
    return render_template('error.html'), 404

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
                return render_template('error.html')
            
            # 확장자가 허용된 확장자인지 확인
            if not allowed_file(image.filename):
                flash('Invalid file. Please upload a valid image file (jpg, jpeg, png, gif).')
                return render_template('error.html')
            
            # 사용자가 업로드한 이미지 저장할 경로 설정 -> 메모리에서 읽어오는 대신 파일로 저장하는 것이 좋음
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok = True)     # 업로드 폴더가 없다면 생성
            image_path = os.path.join(upload_folder, image.filename)
            image.save(image_path)

            # YOLO 모델 로드
            yolo_model = load_yolo_model()

            # 이미지를 YOLO 모델로 예측
            predictions = predict_image(yolo_model, image_path)
            
            # 이미지를 페이지에 띄워주기 위해 이미지 경로와 예측 결과를 템플릿으로 전달
            return render_template('main.html', image_path=image_path, predictions=predictions)
        
# 웹 앱 실행
if __name__ == '__main__':
    app.run(debug=True)
