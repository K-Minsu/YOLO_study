# 🦺 안전 보호구 다중 객체 인식 시스템

안전모, 안전벨트, 안전고리 등의 **안전 보호구 착용 여부**를 YOLO 모델 기반으로 실시간 인식하는 프로젝트입니다.

## 📁 프로젝트 구조

```plaintext
project_root/
├── YOLO_study.ipynb # 모델 학습 코드
├── YOLO_test.ipynb # 이미지/동영상 기반 테스트 코드
├── test.py # 웹캠 실시간 테스트 코드
└── README.md
```

## 🔧 모델 학습 (`YOLO_study.ipynb`)

- 사용 프레임워크: **Ultralytics YOLOv8**
- 학습 대상 클래스 예시:
  - `helmet_on`, `helmet_off`
  - `vest_on`, `vest_off`
  - `lanyard_on`, `lanyard_off`
- 학습 시 사용한 주요 파라미터:
  - `epochs`, `imgsz`, `batch`, `patience`, `device` 등

## 🧪 모델 테스트 (`YOLO_test.ipynb`)

- 정적 이미지 또는 동영상 파일 기반의 테스트
- 객체 인식 결과 시각화 및 예측 클래스 확인 가능

## 🎥 실시간 웹캠 테스트 (`test.py`)

- 노트북 혹은 외부 **웹캠을 이용한 실시간 탐지**
- 객체 탐지 후 Bounding Box 및 클래스 표시
- 실시간 FPS 및 프레임 처리 속도 확인 가능

## ✅ TODO (선택 사항)

- [ ] 미착용 보호구에 대해 경고 메시지 출력
- [ ] 탐지 결과를 DB 또는 로그 파일에 저장
- [ ] Streamlit 기반 데모 앱 배포

## 📝 참고사항

- YOLOv8 설치: `pip install ultralytics`
- 실행 전, `weights/best.pt` 가 사전에 존재해야 함
- 라벨링 형식은 `YOLO JSON` 또는 `YOLO TXT` 포맷 지원

## 📌 기여 및 문의

> 본 프로젝트는 건설 현장 등에서 안전 보호구 착용 점검 자동화를 목표로 개발되었습니다.  
> 문의: [minsue9608@naver.com]

- ## 📄 라이선스

본 프로젝트는 비영리 목적의 연구/학습 용도로 개발되었으며, Ultralytics YOLOv8 모델을 기반으로 합니다.  
YOLOv8은 [GNU AGPLv3 License](https://www.gnu.org/licenses/agpl-3.0.html)를 따르며, 사용 시 해당 라이선스를 준수해야 합니다.

> 이 저장소는 개인 학습/연구용으로만 사용되며, 상업적 목적의 사용은 금지됩니다.
