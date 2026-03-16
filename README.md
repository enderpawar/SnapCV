# 🎥 비디오 레코더

OpenCV(Python)로 만든 간단하지만 기능이 풍부한 웹캠 비디오 녹화 프로그램입니다.

---

## 주요 기능

### 코어 기능
| 기능 | 설명 |
|---|---|
| **실시간 미리보기** | 웹캠 영상을 실시간으로 창에 표시 |
| **비디오 녹화** | `cv.VideoWriter`를 사용해 `.mp4` 파일로 저장 |
| **미리보기 / 녹화 모드** | `Space` 키로 모드 전환 |
| **REC 표시** | 녹화 중 화면에 빨간 동그라미와 "REC" 텍스트 표시 |
| **종료** | `ESC` 키로 프로그램 종료 |

### 추가 기능
| 기능 | 설명 |
|---|---|
| **코덱(FourCC)** | `FOURCC` 상수에서 쉽게 변경 가능한 기본 `mp4v` 코덱 사용 |
| **FPS 제어** | `TARGET_FPS` 상수로 목표 녹화 FPS 설정 (기본값: 30) |
| **실시간 FPS 표시** | 현재 캡처 FPS를 화면에 표시 |
| **8가지 필터 모드** | `F` 키로 필터 전환 (아래 표 참고) |
| **타임스탬프 오버레이** | 각 프레임에 현재 날짜/시간 표시 |
| **키보드 힌트** | 화면에 항상 단축키 안내 표시 |

### 필터 모드 (`F` 키로 전환)
| # | 이름 | 효과 |
|---|---|---|
| 0 | Original | 원본 (필터 없음) |
| 1 | Grayscale | 흑백 필터 |
| 2 | Flip-H | 좌우 반전 |
| 3 | Flip-V | 상하 반전 |
| 4 | Brightness+ | 밝기 +50 |
| 5 | Brightness- | 밝기 -50 |
| 6 | Contrast+ | 대비 ×1.5 |
| 7 | Contrast- | 대비 ×0.5 |

---

## 요구 사항

```
Python 3.9+
opencv-python
numpy
```

의존성 설치:

```bash
pip install opencv-python numpy
```

---

## 실행 방법

```bash
python video_recorder.py
```

---

## 키보드 단축키

| 키 | 동작 |
|---|---|
| `Space` | 녹화 시작 / 종료 |
| `F` | 다음 필터로 전환 |
| `ESC` | 프로그램 종료 |

---

## 설정

`video_recorder.py` 상단의 상수를 수정해 설정할 수 있습니다.

```python
CAMERA_ID  = 0          # 카메라 인덱스 (0 = 기본 웹캠)
TARGET_FPS = 30.0       # 녹화 프레임 레이트
FOURCC     = cv.VideoWriter_fourcc(*'mp4v')  # 비디오 코덱
OUTPUT_EXT = '.mp4'     # 출력 파일 확장자
```

---

## 시현 영상

[시현 영상 링크](https://youtu.be/MNX2GbEq0NA)

---

## 출력 파일 형식

녹화된 파일은 현재 디렉터리에 다음 형식으로 저장됩니다.

```
record_YYYYMMDD_HHMMSS.mp4
```
