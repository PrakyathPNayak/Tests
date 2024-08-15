import os
import subprocess

def merge_audio_video(directory):
    files = os.listdir(directory)
    print(f"Files in directory: {files}")
    audio_files = [f for f in files if f.endswith('audio.mp4')]

    for audio_file in audio_files:
        base_name = audio_file[:-9]
        video_file = base_name + 'video.mp4'

        video_path = os.path.join(directory, video_file)
        audio_path = os.path.join(directory, audio_file)
        output_path = os.path.join(directory, base_name + 'merged.mp4')

        if os.path.exists(video_path) and os.path.exists(audio_path):
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

            print(f"Running command: {' '.join(command)}")

            try:
                subprocess.run(command, check=True)
                print(f'Merged {audio_file} and {video_file} into {output_path}')

                os.remove(video_path)
                os.remove(audio_path)
                print(f'Deleted {video_file} and {audio_file}')
            except subprocess.CalledProcessError as e:
                print(f"Error occurred: {e}")
        else:
            print(f"Video file {video_path} or audio file {audio_path} does not exist.")

directory = 'C:\\Users\\praky\\Videos'
merge_audio_video(directory)
