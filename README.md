# 🎬 ASCII Video Player

> A high-performance terminal-based video player that transforms standard video files into vibrant, 256-color ASCII art with synchronized audio.

## 🌟 Overview

The **ASCII Video Player** is a CLI tool designed for developers and terminal enthusiasts who appreciate the aesthetic of low-fidelity visuals combined with modern performance. It leverages ANSI escape sequences to render full-color frames directly into your terminal emulator, providing a "cinema" experience in the command line.

## 🚀 Key Features

- **🌈 256-Color ANSI Support**: Renders high-fidelity colored ASCII using the xterm-256 color palette.
- **🔊 Frame-Perfect Audio**: Synchronized audio playback powered by FFmpeg's `ffplay`.
- **📏 Adaptive Scaling**: Automatically detects terminal dimensions and resizes video frames to fit perfectly.
- **⚡ Real-time Processing**: Optimized conversion algorithms ensure smooth playback at native video framerates.
- **📊 Live Statistics**: Real-time display of FPS, elapsed time, and progress bars.
- **🛠️ Cross-Platform**: Fully compatible with modern terminal emulators on Linux, macOS, and Windows (via WSL or Windows Terminal).

### Prerequisites

Ensure you have the following installed on your system:

1.  **Python 3.8+**
2.  **FFmpeg** (Required for the `ffplay` audio engine):
    - **Ubuntu/Debian**: `sudo apt install ffmpeg`
    - **macOS**: `brew install ffmpeg`
    - **Windows**: [Download from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)

### Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/10xrashed/ASCII_VideoPlayer.git
    cd ASCII_VideoPlayer
    ```

2.  **Install Dependencies**:
    ```bash
    pip install opencv-python
    ```

## 🎮 Usage

Simply run the player script and pass the path to your video file as an argument:

```bash
python ascii_player.py "path/to/your/video.mp4"
```

### Keyboard Controls
- **Ctrl+C**: Stop playback and clean up terminal resources.

## 🛠️ Technical Details

1.  **Frame Extraction**: Uses `OpenCV` to capture raw video frames.
2.  **Luminance Mapping**: Converts pixel brightness to a density-based ASCII character set (` .:-=+*#%@`).
3.  **Color Quantization**: Maps RGB values from the source frame to the nearest available xterm-256 color code.
4.  **Audio Integration**: Spawns a sub-process running `ffplay` with specific offsets to match the visual frame delay.
5.  **Terminal Optimization**: Uses buffer flushing techniques to minimize "ghosting" and flickering in fast-moving scenes.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with by [10xrashed](https://github.com/10xrashed)
