import os
import subprocess
from pytube import YouTube

def download_youtube_video(url, output_dir):
    yt = YouTube(url)

    # Get the best video and audio streams available
    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()

    if not video_stream or not audio_stream:
        print("Could not find appropriate streams for video and audio.")
        return

    video_path = os.path.join(output_dir, video_stream.default_filename)
    audio_path = os.path.join(output_dir, yt.title + ".m4a")

    video_stream.download(output_path=output_dir, filename=video_stream.default_filename)
    audio_stream.download(output_path=output_dir, filename=yt.title + ".m4a")

    print(f'Downloaded video to {video_path}')
    print(f'Downloaded audio to {audio_path}')

def merge_audio_video(directory):
    files = os.listdir(directory)
    video_files = [f for f in files if f.endswith('.mp4') and not f.endswith('merged.mp4')]
    audio_files = [f for f in files if f.endswith('.m4a')]

    for video_file in video_files:
        base_name = os.path.splitext(video_file)[0]
        matching_audio_files = [af for af in audio_files if af.startswith(base_name)]

        if matching_audio_files:
            audio_file = matching_audio_files[0]
            video_path = os.path.join(directory, video_file)
            audio_path = os.path.join(directory, audio_file)
            output_path = os.path.join(directory, base_name + 'merged.mp4')

            command = [
                'ffmpeg',
                '-y',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'h264_nvenc',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_path
            ]

            subprocess.run(command, check=True)
            print(f'Merged {audio_file} and {video_file} into {output_path}')

            os.remove(video_path)
            os.remove(audio_path)
            print(f'Deleted {video_file} and {audio_file}')

if __name__ == '__main__':
    video_url = input("Enter the YouTube video URL: ")
    output_directory = 'C:\\Users\\praky\\Videos'

    download_youtube_video(video_url, output_directory)
    merge_audio_video(output_directory)
