import sys
import os
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pytube import Playlist, YouTube

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, link):
        super().__init__()
        self.link = link
        self.output_dir = "C:\\Users\\praky\\Videos"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def sanitize_filename(self, title):
        return re.sub(r'[\\/*?:"<>|]', "_", title)

    def run(self):
        try:
            playlist = Playlist(self.link)
            total_videos = len(playlist.video_urls)
            downloaded_files = []

            for index, video_url in enumerate(playlist.video_urls):
                yt = YouTube(video_url, on_progress_callback=self.on_progress)
                video_title = self.sanitize_filename(yt.title)
                video_stream = yt.streams.filter(only_video=True, file_extension='mp4').first()
                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

                if video_stream and audio_stream:
                    video_path = video_stream.download(output_path=self.output_dir, filename=f"{video_title}_video.mp4")
                    audio_path = audio_stream.download(output_path=self.output_dir, filename=f"{video_title}_audio.mp4")

                    downloaded_files.append((video_title, video_path, audio_path))
                    self.status.emit(f"Downloaded: {video_title}")
                else:
                    self.status.emit(f"No suitable streams found for: {video_title}")

                # Bar go mooove
                progress = int((index + 1) / total_videos * 100)
                self.progress.emit(progress)

            self.status.emit("All files downloaded, starting merge process...")

            # Merge video and audio files using ffmpeg and 4050 GPU ACCELERATIOOOOOONNNNN
            for video_title, video_path, audio_path in downloaded_files:
                try:
                    final_path = os.path.join(self.output_dir, f"{video_title}.mp4")
                    command = [
                        'ffmpeg', '-y',
                        '-i', video_path,
                        '-i', audio_path,
                        '-c:v', 'h264_nvenc',
                        '-c:a', 'aac',
                        final_path
                    ]
                    subprocess.run(command, check=True, shell=True)

                    # Remove the temporary video and audio files, comment this if you want all the files seperately
                    os.remove(video_path)
                    os.remove(audio_path)

                    self.status.emit(f"Merged: {video_title}")
                except subprocess.CalledProcessError as e:
                    self.status.emit(f"FFmpeg error merging {video_title}: {e}")
                except Exception as e:
                    self.status.emit(f"Error merging {video_title}: {e}")

            self.status.emit("Playlist download and merge completed")
        except Exception as e:
            self.status.emit(f"Error: {e}")
        finally:
            self.finished.emit()

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress.emit(int(percentage_of_completion))


class YouTubePlaylistDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.download_thread = None

    def initUI(self):
        self.setWindowTitle('YouTube Playlist Downloader')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel('Enter YouTube Playlist link:')
        self.layout.addWidget(self.label)

        self.link_entry = QLineEdit(self)
        self.layout.addWidget(self.link_entry)

        self.download_button = QPushButton('Download Playlist', self)
        self.download_button.clicked.connect(self.start_download_thread)
        self.layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel('', self)
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def start_download_thread(self):
        link = self.link_entry.text()
        self.download_button.setEnabled(False)

        self.download_thread = DownloadThread(link)
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
    downloader = YouTubePlaylistDownloader()
    downloader.show()
    sys.exit(app.exec_())
