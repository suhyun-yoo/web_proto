import dlib
import dlib, cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
import operator
from crawringapp.models import CrawringData


# 이미지 속 얼굴 탐지,
def find_faces(img):
    dets = detector(img, 1)
    if len(dets) == 0:
        return np.empty(0), np.empty(0), np.empty(0)
    rects, shapes = [], []
    shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)
    for k, d in enumerate(dets):
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))
        rects.append(rect)
        shape = sp(img, d)
        for i in range(0, 68):
            shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)
        shapes.append(shape)
    return rects, shapes, shapes_np


# 이미지 인코딩 함수, 랜드마크 결과 벡터 반환
def encode_faces(img, shapes):
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))
    return np.array(face_descriptors)


def img_encoding(img_path_target):
    # 고객 사진 인코딩
    descs = []
    for img_path in img_path_target:
        img_bgr_target = cv2.imread(img_path_target)
        img_rgb_target = cv2.cvtColor(img_bgr_target, cv2.COLOR_BGR2RGB)
        _, img_shapes_target, _ = find_faces(img_rgb_target)
        descs.append(encode_faces(img_rgb_target, img_shapes_target)[0])

    # 대상 사진 인코딩
    img_bgr_pic = cv2.imread(img_path_pic)
    img_rgb_pic = cv2.cvtColor(img_bgr_pic, cv2.COLOR_BGR2RGB)
    rects, shapes, _ = find_faces(img_rgb_pic)
    descriptors = encode_faces(img_rgb_pic, shapes)

    for i, desc in enumerate(descriptors):
        found = False
        dist = {}
        for j, saved_desc in enumerate(descs):
            dist[j] = np.linalg.norm([desc] - saved_desc, axis=1)
        dist_sorted = sorted(dist.items(), key=operator.itemgetter(1))
        if dist_sorted[0][1] < 0.45:
            print('비슷한 사진을 발견하였습니다.')

        if not found:
            print('없습니다.')


if __name__ == "__main__":
    # 모델 객체 선언
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')
    all_crawring_data = CrawringData.objects.all().order_by("-id")




