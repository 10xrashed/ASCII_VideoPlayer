import cv2
import os
import sys
import time
import subprocess
from pathlib import Path
def get_terminal_size():
    try:
        columns, rows = os.get_terminal_size()
        return columns, rows
    except OSError:
        return 80, 24
def convert_frame_to_colored_ascii(frame, width, ascii_chars=" .:-=+*#%@"):
    height = int(frame.shape[0] * width / frame.shape[1] / 2)
    if height == 0:
        height = 1
    resized = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    normalized = gray / 255.0
    ascii_frame = ""
    num_chars = len(ascii_chars) - 1
    for y in range(height):
        for x in range(width):
            pixel = normalized[y, x]
            index = int(pixel * num_chars)
            char = ascii_chars[index]
            b, g, r = resized[y, x]
            color_code = 16 + 36 * int(r/51) + 6 * int(g/51) + int(b/51)
            ascii_frame += f"\033[38;5;{color_code}m{char}"
        ascii_frame += "\033[0m\n" 
    return ascii_frame.rstrip("\n")
def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"
def create_progress_bar(progress, width=30):
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"
class AudioPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.process = None
    def play(self):
        try:
            self.process = subprocess.Popen(
                ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', self.video_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print("\n ffplay not found - playing without audio")
            print("Install ffmpeg to enable audio:")
            print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("  macOS: brew install ffmpeg\n")
            return False
        except Exception:
            return False
        return True
    def stop(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except:
                try:
                    self.process.kill()
                except:
                    pass
def play_video(video_path):
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    term_width, _ = get_terminal_size()
    width = min(term_width - 2, 120)  
    ascii_chars = " .:-=+*#%@"
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'.")
        return
    video_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / video_fps if video_fps > 0 else 0
    print(f"\n{'='*60}")
    print(f"Video: {Path(video_path).name}")
    print(f"Resolution: {video_width}x{video_height}")
    print(f"Duration: {format_time(duration)}")
    print(f"ASCII Width: {width} characters")
    print(f"Color: Enabled")
    print(f"Audio: Starting...")
    print(f"{'='*60}\n")
    print("Press Ctrl+C to stop\n")
    time.sleep(2)
    frame_delay = 1.0 / video_fps
    clear_cmd = 'cls' if os.name == 'nt' else 'clear'
    if os.name != 'nt':
        print("\033[?25l", end="", flush=True)
    audio_player = AudioPlayer(video_path)
    audio_player.play()
    time.sleep(0.1) 
    frame_count = 0
    start_time = time.perf_counter()
    try:
        while True:
            loop_start = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            ascii_art = convert_frame_to_colored_ascii(frame, width, ascii_chars)
            os.system(clear_cmd)
            print(ascii_art)
            current_time = frame_count / video_fps
            progress = frame_count / total_frames if total_frames > 0 else 0
            progress_bar = create_progress_bar(progress, width=30)        
            elapsed_total = time.perf_counter() - start_time
            actual_fps = frame_count / elapsed_total if elapsed_total > 0 else 0
            info = (f"{format_time(current_time)}/{format_time(duration)} "
                   f"{progress_bar} {int(progress*100):3d}% | FPS: {actual_fps:.1f}")
            print(f"\n{info}")
            elapsed = time.perf_counter() - loop_start
            sleep_time = frame_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("\n\nPlayback stopped.")
    finally:
        cap.release()
        audio_player.stop()
        if os.name != 'nt':
            print("\033[?25h", end="", flush=True)
        print(f"\n Finished playing {frame_count} frames\n")
def main():
    print("\n ASCII Video Player")
    print("=" * 50)
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = input("Enter video file path: ").strip()
    if not video_path:
        print("No video file specified.")
        return
    video_path = video_path.strip('"').strip("'")
    print("\nStarting playback...\n")
    time.sleep(0.5)
    play_video(video_path)
if __name__ == "__main__":  main()
