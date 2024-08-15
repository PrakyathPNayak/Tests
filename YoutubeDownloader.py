import sys
import os
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pytube import YouTube

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, link, quality):
        super().__init__()
        self.link = link
        self.quality = quality
        self.output_dir = "C:\\Users\\praky\\Videos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def sanitize_filename(self, title):
        return re.sub(r'[\\/*?:"<>|]', "_", title)

    def run(self):
        try:
            yt = YouTube(self.link, on_progress_callback=self.on_progress)
            video_title = self.sanitize_filename(yt.title)
            video_stream = yt.streams.filter(only_video=True, res=self.quality).first()
            audio_stream = yt.streams.filter(only_audio=True).first()

            if video_stream and audio_stream:
                video_path = video_stream.download(output_path=self.output_dir, filename="video1.mp4")
                audio_path = audio_stream.download(output_path=self.output_dir, filename="audio1.mp4")

                # Use ffmpeg to merge video and audio, GPU ACCELERATION WHOOOOO
                output_path = os.path.join(self.output_dir, f"{video_title}_final.mp4")
                command = [
                    'ffmpeg', '-y',
                    '-i', f'"{video_path}"',
                    '-i', f'"{audio_path}"',
                    '-c:v', 'h264_nvenc',
                    '-c:a', 'aac',
                    f'"{output_path}"'
                ]

                subprocess.run(' '.join(command), shell=True, check=True)

                self.status.emit("Download completed")
            else:
                self.status.emit(f"No {self.quality} stream found")
        except subprocess.CalledProcessError as e:
            self.status.emit(f"FFmpeg error: {e}")
        except Exception as e:
            self.status.emit(f"Error: {e}")
        finally:
            self.finished.emit()

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress.emit(int(percentage_of_completion))


class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.download_thread = None

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter YouTube link:')
        self.layout.addWidget(self.label)

        self.link_entry = QLineEdit(self)
        self.layout.addWidget(self.link_entry)

        self.quality_label = QLabel('Select Quality:')
        self.layout.addWidget(self.quality_label)

        self.quality_combobox = QComboBox(self)
        self.quality_combobox.addItems(["144p", "240p", "360p", "480p", "720p", "1080p"])
        self.quality_combobox.setCurrentIndex(4)  # Default to 720p
        self.layout.addWidget(self.quality_combobox)

        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.start_download_thread)
        self.layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel('', self)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def start_download_thread(self):
        link = self.link_entry.text()
        quality = self.quality_combobox.currentText()
        self.download_button.setEnabled(False)

        self.download_thread = DownloadThread(link, quality)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.status.connect(self.update_status)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, status):
        self.status_label.setText(status)

    def download_finished(self):
        self.download_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = YouTubeDownloader()
    downloader.show()
    sys.exit(app.exec_())
