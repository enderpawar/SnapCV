import cv2 as cv
import numpy as np
from datetime import datetime

# ── 설정 ──────────────────────────────────────────────────────────────────────
CAMERA_ID  = 0
TARGET_FPS = 30.0
FOURCC     = cv.VideoWriter_fourcc(*'mp4v')   # 코덱 (FourCC): mp4v
OUTPUT_EXT = '.mp4'

# ── 필터 ID 상수 ───────────────────────────────────────────────────────────────
FILTER_NONE      = 0   # 원본
FILTER_GRAYSCALE = 1   # 흑백
FILTER_FLIP_H    = 2   # 좌우 반전
FILTER_FLIP_V    = 3   # 상하 반전
FILTER_BRIGHT    = 4   # 밝기 +50
FILTER_DARK      = 5   # 밝기 -50
FILTER_HIGH_CONT = 6   # 대비 ×1.5
FILTER_LOW_CONT  = 7   # 대비 ×0.5

FILTER_NAMES = {
    FILTER_NONE:      'Original',
    FILTER_GRAYSCALE: 'Grayscale',
    FILTER_FLIP_H:    'Flip-H',
    FILTER_FLIP_V:    'Flip-V',
    FILTER_BRIGHT:    'Brightness+',
    FILTER_DARK:      'Brightness-',
    FILTER_HIGH_CONT: 'Contrast+',
    FILTER_LOW_CONT:  'Contrast-',
}
NUM_FILTERS = len(FILTER_NAMES)


def apply_filter(frame: np.ndarray, filter_id: int) -> np.ndarray:
    """선택된 필터를 프레임에 적용하여 반환."""
    if filter_id == FILTER_NONE:
        return frame
    if filter_id == FILTER_GRAYSCALE:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
    if filter_id == FILTER_FLIP_H:
        return cv.flip(frame, 1)
    if filter_id == FILTER_FLIP_V:
        return cv.flip(frame, 0)
    if filter_id == FILTER_BRIGHT:
        return cv.convertScaleAbs(frame, alpha=1.0, beta=50)
    if filter_id == FILTER_DARK:
        return cv.convertScaleAbs(frame, alpha=1.0, beta=-50)
    if filter_id == FILTER_HIGH_CONT:
        return cv.convertScaleAbs(frame, alpha=1.5, beta=0)
    if filter_id == FILTER_LOW_CONT:
        return cv.convertScaleAbs(frame, alpha=0.5, beta=0)
    return frame


def draw_ui(frame: np.ndarray, is_recording: bool,
            filter_id: int, fps: float) -> np.ndarray:
    """화면에 HUD(녹화 표시, FPS, 필터명, 타임스탬프, 단축키)를 그린다."""
    h, w = frame.shape[:2]

    # ── Record 모드 표시: 빨간 원 + 'REC' 텍스트 ──────────────────────────
    if is_recording:
        cv.circle(frame, (w - 35, 35), 16, (0, 0, 255), -1)
        cv.putText(frame, 'REC', (w - 75, 41),
                   cv.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2, cv.LINE_AA)

    # ── 좌상단: FPS / 필터명 ───────────────────────────────────────────────
    cv.putText(frame, f'FPS : {fps:5.1f}', (10, 28),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv.LINE_AA)
    cv.putText(frame, f'Filter: {FILTER_NAMES[filter_id]}', (10, 56),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv.LINE_AA)

    # ── 좌하단: 타임스탬프 ─────────────────────────────────────────────────
    ts = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    cv.putText(frame, ts, (10, h - 12),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv.LINE_AA)

    # ── 우하단: 단축키 안내 ────────────────────────────────────────────────
    hints = ['ESC : Quit', 'F : Filter', 'SPACE : REC/STOP']
    for i, text in enumerate(hints):
        cv.putText(frame, text, (w - 175, h - 12 - i * 22),
                   cv.FONT_HERSHEY_SIMPLEX, 0.42, (180, 180, 180), 1, cv.LINE_AA)

    return frame


def main() -> None:
    # ── 카메라 열기 ────────────────────────────────────────────────────────
    cap = cv.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print(f'[ERROR] Camera {CAMERA_ID} 을 열 수 없습니다.')
        return

    frame_w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    cam_fps = cap.get(cv.CAP_PROP_FPS)
    print(f'[INFO] 카메라: {frame_w}x{frame_h}, 카메라 FPS={cam_fps:.1f}, '
          f'저장 FPS={TARGET_FPS}, 코덱=mp4v')
    print('[INFO] Space: REC/STOP  |  F: 필터 전환  |  ESC: 종료')

    is_recording = False
    filter_id    = FILTER_NONE
    writer: cv.VideoWriter | None = None
    prev_tick    = cv.getTickCount()
    fps_display  = 0.0

    cv.namedWindow('Video Recorder', cv.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print('[ERROR] 프레임을 읽을 수 없습니다.')
            break

        # ── 실시간 FPS 계산 ────────────────────────────────────────────────
        tick        = cv.getTickCount()
        fps_display = cv.getTickFrequency() / max(tick - prev_tick, 1)
        prev_tick   = tick

        # ── 필터 적용 ──────────────────────────────────────────────────────
        filtered = apply_filter(frame, filter_id)

        # ── 녹화: 필터 적용 프레임을 파일에 기록 (UI 오버레이 전) ────────
        if is_recording and writer is not None:
            writer.write(filtered)

        # ── HUD 오버레이 후 화면 표시 ─────────────────────────────────────
        display = draw_ui(filtered.copy(), is_recording, filter_id, fps_display)
        cv.imshow('Video Recorder', display)

        # ── 키 입력 처리 ───────────────────────────────────────────────────
        key = cv.waitKey(1) & 0xFF

        if key == 27:                          # ESC → 종료
            break

        elif key == ord(' '):                  # Space → Record 토글
            if not is_recording:
                filename = datetime.now().strftime('record_%Y%m%d_%H%M%S') + OUTPUT_EXT
                writer = cv.VideoWriter(filename, FOURCC, TARGET_FPS, (frame_w, frame_h))
                is_recording = True
                print(f'[REC] 녹화 시작: {filename}')
            else:
                if writer:
                    writer.release()
                writer = None
                is_recording = False
                print('[STOP] 녹화 중지 및 파일 저장 완료.')

        elif key in (ord('f'), ord('F')):      # F → 다음 필터
            filter_id = (filter_id + 1) % NUM_FILTERS
            print(f'[FILTER] {FILTER_NAMES[filter_id]}')

    # ── 종료 처리 ──────────────────────────────────────────────────────────
    if writer is not None:
        writer.release()
    cap.release()
    cv.destroyAllWindows()
    print('[INFO] 프로그램을 종료합니다.')


if __name__ == '__main__':
    main()
