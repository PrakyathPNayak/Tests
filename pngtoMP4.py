import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def select_files():
    file_paths = filedialog.askopenfilenames(
        title="Select PNG files",
        filetypes=[("PNG files", "*.png")],
        initialdir=os.getcwd()
    )
    return file_paths

def convert_to_mp4(file_paths, output_path, fps=60, use_gpu=True):
    if not file_paths:
        print("No files selected.")
        return
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    file_list_path = "input_files.txt"
    try:
        with open(file_list_path, 'w') as file_list:
            for file_path in file_paths:
                file_list.write(f"file '{file_path.replace(os.sep, '/')}'\n")

        if use_gpu:
            ffmpeg_command = [
                'ffmpeg', '-y', '-r', str(fps), '-f', 'concat', '-safe', '0', '-i', file_list_path,
                '-pix_fmt', 'yuv420p', '-c:v', 'h264_nvenc', '-preset', 'fast', output_path
            ]
        else:
            ffmpeg_command = [
                'ffmpeg', '-y', '-r', str(fps), '-f', 'concat', '-safe', '0', '-i', file_list_path,
                '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-preset', 'fast', output_path
            ]

        process = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode != 0:
            print(f"FFmpeg Error: {process.stderr.decode('utf-8')}")
        else:
            print(f"Video saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if os.path.exists(file_list_path):
            os.remove(file_list_path)

def start_conversion():
    file_paths = select_files()
    if not file_paths:
        return
    output_path = filedialog.asksaveasfilename(
        title="Save MP4 file",
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4")]
    )
    if output_path:
        convert_to_mp4(file_paths, output_path)

root = tk.Tk()
root.title("PNG to MP4 Converter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="Select PNG Files", command=start_conversion)
select_button.pack()

root.mainloop()
