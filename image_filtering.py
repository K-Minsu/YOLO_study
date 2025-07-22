import os
import zipfile
import json
import shutil

# ✅ 경로 설정 (역슬래시 이스케이프 또는 슬래시 사용)
base_dir = "{BASE_PATH}"    # 압축 해제, 필터링 저장 경로
zip_path = "{ZIP_PATH}"     # 저장된 .zip 경로

os.makedirs(base_dir, exist_ok=True)

# ✅ 압축 해제 함수
def unzip_files(zip_file_path, target_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)
    print(f"압축 해제 완료: {zip_file_path} -> {target_dir}")

# ✅ 압축 파일명
file_name_images = "{IMAGE_ZIP_FILE_NAME}"
file_name_labels_json = "{LABELS_JSON_ZIP_FILE_NAME}"

# ✅ 압축 해제
unzip_files(os.path.join(zip_path, file_name_images), os.path.join(base_dir, "images"))
unzip_files(os.path.join(zip_path, file_name_labels_json), os.path.join(base_dir, "labels_json"))

# ✅ 클래스 필터링 설정
target_classes = {"01", "03", "07"}    # 안전벨트, 안전고리, 안전모

# ✅ train/val 두 개의 데이터셋을 각각 처리
for split in ["train", "val"]:
    # 라벨(JSON) 디렉토리 경로: base_dir/labels_json/train 또는 val
    labels_dir = os.path.join(base_dir, "labels_json", split)
    
    # 이미지 디렉토리 경로: base_dir/images/train 또는 val
    images_dir = os.path.join(base_dir, "images", split)

    # 필터링된 라벨 저장 경로: base_dir/filtered/train/labels_json 또는 val
    filtered_labels_dir = os.path.join(base_dir, "filtered", split, "labels_json")
    
    # 필터링된 이미지 저장 경로: base_dir/filtered/train/images 또는 val
    filtered_images_dir = os.path.join(base_dir, "filtered", split, "images")

    # 디렉토리 생성 (이미 존재하면 무시)
    os.makedirs(filtered_labels_dir, exist_ok=True)
    os.makedirs(filtered_images_dir, exist_ok=True)

    # JSON 라벨 파일들을 순회
    for json_file in os.listdir(labels_dir):
        # .json 확장자가 아니면 건너뜀
        if not json_file.endswith(".json"):
            continue

        # JSON 파일 경로 설정
        json_path = os.path.join(labels_dir, json_file)

        # JSON 파일 열기 및 파싱
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # annotations 리스트 가져오기 (객체 정보가 들어 있음)
        annotations = data.get("annotations", [])

        # ✅ target_classes(예: 안전모, 안전고리 등)에 해당하는 객체가 하나라도 있는지 확인
        contains_target_class = any(
            ann.get("class") in target_classes for ann in annotations
        )

        # 만약 타겟 클래스가 없으면 해당 JSON/이미지 건너뜀
        if not contains_target_class:
            continue

        # 이미지 정보 중 filename 값 가져오기
        image_info = data.get("image", {})
        filename = image_info.get("filename")

        # filename이 없으면 건너뜀 (예외 상황)
        if not filename:
            print(f"⚠️ filename 없음 in {json_file}")
            continue

        # 원본 이미지 경로와 복사 대상 경로 설정
        src_img_path = os.path.join(images_dir, filename)
        dst_img_path = os.path.join(filtered_images_dir, filename)

        # ✅ 실제 이미지가 존재할 경우에만 JSON과 이미지 모두 복사
        if os.path.exists(src_img_path):
            # JSON 복사
            shutil.copy(json_path, os.path.join(filtered_labels_dir, json_file))
            # 이미지 복사
            shutil.copy(src_img_path, dst_img_path)
        else:
            # 이미지가 없을 경우 경고 출력
            print(f"❌ 이미지 없음: {src_img_path}")
