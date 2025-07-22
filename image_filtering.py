import os
import zipfile
import json
import shutil

# ✅ 경로 설정 (역슬래시 이스케이프 또는 슬래시 사용)
base_dir = "C:/Users/User/Desktop/safety"
zip_path = "C:/Users/User/Desktop/사용데이터"

os.makedirs(base_dir, exist_ok=True)

# ✅ 압축 해제 함수
def unzip_files(zip_file_path, target_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    print(f"압축 해제 완료: {zip_file_path} -> {target_dir}")

# ✅ 압축 파일명
file_name_images = "2.공연장_부산_오페라_하우스_신축공사_images.zip"
file_name_labels_json = "2.공연장_부산_오페라_하우스_신축공사_labels_json.zip"

# ✅ 압축 해제
unzip_files(os.path.join(zip_path, file_name_images), os.path.join(base_dir, "images"))
unzip_files(os.path.join(zip_path, file_name_labels_json), os.path.join(base_dir, "labels_json"))

# ✅ 클래스 필터링 설정
target_classes = {"01", "02", "03", "04", "07", "08"}

# ✅ train/val 각각 처리
for split in ["train", "val"]:
    labels_dir = os.path.join(base_dir, "labels_json", split)
    images_dir = os.path.join(base_dir, "images", split)

    filtered_labels_dir = os.path.join(base_dir, "filtered", split, "labels_json")
    filtered_images_dir = os.path.join(base_dir, "filtered", split, "images")

    os.makedirs(filtered_labels_dir, exist_ok=True)
    os.makedirs(filtered_images_dir, exist_ok=True)

    for json_file in os.listdir(labels_dir):
        if not json_file.endswith(".json"):
            continue

        json_path = os.path.join(labels_dir, json_file)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        annotations = data.get("annotations", [])
        contains_target_class = any(
            ann.get("middle classification") in target_classes for ann in annotations
        )

        if contains_target_class:
            shutil.copy(json_path, os.path.join(filtered_labels_dir, json_file))

            image_info = data.get("image", {})
            filename = image_info.get("filename")

            if filename:
                src_img_path = os.path.join(images_dir, filename)
                dst_img_path = os.path.join(filtered_images_dir, filename)

                if os.path.exists(src_img_path):
                    shutil.copy(src_img_path, dst_img_path)
                else:
                    print(f"❌ 이미지 없음: {src_img_path}")
