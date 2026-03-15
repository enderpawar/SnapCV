# 🎥 Video Recorder

A simple yet feature-rich webcam video recorder built with OpenCV (Python).

---

## Features

### Core Features
| Feature | Description |
|---|---|
| **Live Preview** | Displays real-time webcam footage in a window |
| **Video Recording** | Saves camera footage to an `.mp4` file using `cv.VideoWriter` |
| **Preview / Record Modes** | Toggle between modes with the `Space` key |
| **REC Indicator** | A red circle + "REC" text appears on screen while recording |
| **Quit** | Press `ESC` to exit the program |

### Additional Features
| Feature | Description |
|---|---|
| **Codec (FourCC)** | Uses `mp4v` codec; easily configurable in `FOURCC` constant |
| **FPS Control** | Target recording FPS set via `TARGET_FPS` constant (default: 30) |
| **Real-time FPS Display** | Current capture FPS shown on screen |
| **8 Filter Modes** | Cycle through filters with the `F` key (see table below) |
| **Timestamp Overlay** | Current date/time displayed on every frame |
| **Keyboard Hint** | On-screen shortcut guide always visible |

### Filter Modes (`F` key to cycle)
| # | Name | Effect |
|---|---|---|
| 0 | Original | No filter |
| 1 | Grayscale | Black & white |
| 2 | Flip-H | Horizontal mirror |
| 3 | Flip-V | Vertical flip |
| 4 | Brightness+ | Brightness +50 |
| 5 | Brightness- | Brightness -50 |
| 6 | Contrast+ | Contrast ×1.5 |
| 7 | Contrast- | Contrast ×0.5 |

---

## Requirements

```
Python 3.9+
opencv-python
numpy
```

Install dependencies:
```bash
pip install opencv-python numpy
```

---

## How to Run

```bash
python video_recorder.py
```

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `Space` | Start / Stop recording |
| `F` | Cycle to next filter |
| `ESC` | Quit program |

---

## Configuration

Edit the constants at the top of `video_recorder.py`:

```python
CAMERA_ID  = 0          # Camera index (0 = default webcam)
TARGET_FPS = 30.0       # Recording frame rate
FOURCC     = cv.VideoWriter_fourcc(*'mp4v')  # Video codec
OUTPUT_EXT = '.mp4'     # Output file extension
```

---

## Screenshot

> *(Add a screenshot or demo video here)*

---

## Output

Recorded files are saved in the current directory as:
```
record_YYYYMMDD_HHMMSS.mp4
```
