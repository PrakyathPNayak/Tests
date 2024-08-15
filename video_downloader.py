import tkinter as tk
from tkinter import filedialog, messagebox
import youtube_dl
import os

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")
        self.root.geometry("500x250")

        self.url_label = tk.Label(root, text="Video URL:", font=('Arial', 12))
        self.url_label.pack(pady=10)

        self.url_entry = tk.Entry(root, width=60, font=('Arial', 12))
        self.url_entry.pack(pady=5)

        self.path_label = tk.Label(root, text="Save to:", font=('Arial', 12))
        self.path_label.pack(pady=10)

        self.path_frame = tk.Frame(root)
        self.path_frame.pack(pady=5)

        self.path_entry = tk.Entry(self.path_frame, width=40, font=('Arial', 12))
        self.path_entry.pack(side=tk.LEFT, padx=(10, 5))

        self.browse_button = tk.Button(self.path_frame, text="Browse", font=('Arial', 10), command=self.browse_directory)
        self.browse_button.pack(side=tk.LEFT, padx=(5, 10))

        self.download_button = tk.Button(root, text="Download", font=('Arial', 12), command=self.download_video)
        self.download_button.pack(pady=20)

        self.progress_label = tk.Label(root, text="", font=('Arial', 12))
        self.progress_label.pack(pady=5)

    def browse_directory(self):
        download_directory = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, download_directory)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.progress_label.config(text=f"Downloading... {d['_percent_str']} complete")
        elif d['status'] == 'finished':
            self.progress_label.config(text="Download complete")
            messagebox.showinfo("Info", "Download complete")

    def download_video(self):
        url = self.url_entry.get()
        download_path = self.path_entry.get()

        if not url:
            messagebox.showwarning("Warning", "Please enter a URL")
            return

        if not download_path:
            messagebox.showwarning("Warning", "Please select a download directory")
            return

        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()
