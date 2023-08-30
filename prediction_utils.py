import cv2
import shutil
import os
from ultralytics import YOLO

# 허용된 확장자 설정
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# 파일 확장자를 체크하는 함수
def allowed_file(filename):

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 모델을 불러오는 함수
def load_yolo_model(model_path = '/Users/hyunjulee/tp2/TrafficDetection/model/best_1.pt'):
    
    model = YOLO(model_path)
 
    return model

# 모델을 사용해서 예측하는 함수
def predict_image(model, image_path):

    # 이미지 읽어오기
    image = cv2.imread(image_path)

    # 예측 
    model.predict(image, imgsz=640, save = True)

    # predictions 이미지 경로
    source_image_path = "/Users/hyunjulee/tp2/TrafficDetection/runs/detect/predict/image0.jpg"

    # 원본 이미지의 파일 이름 추출
    original_image_name, _ = os.path.splitext(os.path.basename(image_path))

    # 새로운 이름 생성 (원본 이미지 이름 앞에 'pred_'를 붙임)
    new_image_name = f'pred_{original_image_name}.jpg'

    # 새로운 이미지 경로
    predictions = os.path.join("static", "predictions", new_image_name)

    # 이미지 이름 변경 및 이동
    shutil.move(source_image_path, predictions)

    # 이동 후에는 디렉토리 삭제
    directory_to_delete = "/Users/hyunjulee/tp2/TrafficDetection/runs"
    try:
        shutil.rmtree(directory_to_delete)
        print(f"디렉토리 삭제 완료: {directory_to_delete}")
    except Exception as e:
        print(f"디렉토리 삭제 실패: {e}")

    print(f'destination_image_path : {predictions}')

    return predictions
    
