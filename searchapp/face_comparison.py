import dlib
import cv2
import numpy as np
from crawlingapp.models import CrawlingData
from .models import SearchedData


# 모델 객체 선언
# 얼굴 탐지 모델
detector = dlib.get_frontal_face_detector()
# 랜드마크 탐지 모델
sp = dlib.shape_predictor('searchapp/models/shape_predictor_68_face_landmarks.dat')
# 얼굴인식 모델
facerec = dlib.face_recognition_model_v1('searchapp/models/dlib_face_recognition_resnet_model_v1.dat')

all_crawling_data = CrawlingData.objects.all().order_by("-id")

# Step 1. 받아온 이미지에서 얼굴을 탐지한다.
# input img에서 얼굴을 찾는 함수,
def find_faces(img_rgb):
    global detector, sp, facerec, all_crawling_data
    # dets -> 얼굴을 찾은 결과물을 담을 변수
    dets = detector(img_rgb, 1)

    # dets에 결과물이 없다 == 얼굴을 하나도 못찾은 경우
    # 빈 배열들을 반환 - 여기서 로직 끝남
    if len(dets) == 0:
        return np.empty(0), np.empty(0), np.empty(0)

    # 결과물 저장 배열
    rects, shapes = [], []
    shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)

    # 얼굴마다(얼굴개수만큼) 루프를 돈다
    # !! -> 우리는 이미지에서 얼굴이 한개여야함.
    # exception 2개 이상이면 다른 이미지로 업로드 하라고 고객에게 안내.
    for k, d in enumerate(dets):
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))
        rects.append(rect)

        # 랜드 마크 구하기
        shape = sp(img_rgb, d)
        for i in range(0, 68):
            shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)
        shapes.append(shape)

        break

    return rects, shapes, shapes_np


# 이미지 인코딩 함수, 랜드마크 결과 벡터 반환
def encode_faces(img, shapes):
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))
    return np.array(face_descriptors)


# Step 2. 크롤링된 데이터를 불러온다.
# Step 3. 크롤링된 데이터와 비교하여 검색 결과값을 만든다.
def comparison(target_desc):
    result_list = []
    for i in range(len(all_crawling_data)):
        img_path = str(all_crawling_data[i].img)
        tmp_desc = img_encoding(img_path)
        dist = np.linalg.norm([target_desc] - tmp_desc, axis=1)
        if dist[0] < 0.45:
            result_list.append(all_crawling_data[i])

    return result_list


# Step 4. 검색 결과를 SearchedData로 저장한다.
def save_result(request, result_list):
    for result in result_list:
        searched_data = SearchedData(
            request=request,
            link=result.link,
            img=result.img,
        )
        searched_data.save()


def img_encoding(img_path):
    # 고객 사진 인코딩
    img_path = "media/"+img_path
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    _, img_shapes, _ = find_faces(img_rgb)
    descs = encode_faces(img_rgb, img_shapes)[0]

    return descs
