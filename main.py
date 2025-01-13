import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
import os
import subprocess

############################################
# Graphical user interface for FFmpeg tool #
############################################

class FFmpegApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FFmpeg Tool")
        self.selected_files = []

        # Main menu
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text="Choose an operation", font=("Arial", 16)).pack()

        tk.Button(self.menu_frame, text="Open files", command=self.open_files, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Clear files", command=self.clear_files, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Re-encode to HEVC CPU", command=self.open_h265_window, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Re-encode to HEVC GPU", command=self.open_hevc_window, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Convert MP4 to MP3", command=self.open_mp4_to_mp3_window, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Compress MP3", command=self.open_compress_mp3_window, width=25).pack(pady=5)

        # Display selected files with codecs
        self.file_display = tk.Text(self.root, height=15, width=100)
        self.file_display.pack(pady=10)
        self.file_display.config(state=tk.DISABLED)

    # Get the selected files
    def open_files(self):
        files = filedialog.askopenfilenames(filetypes=[
            ("Supported files", "*.mp4 *.mp3"),
            ("Video files", "*.mp4"),
            ("Audio files", "*.mp3")
        ])
        if files:
            self.selected_files = list(files)
            self.update_file_display()

    # Clear the selected files
    def clear_files(self):
        self.selected_files = []
        self.update_file_display()

    # Update the display of selected files
    def update_file_display(self):
        codec_data = []
        for file in self.selected_files:
            if not os.path.exists(file):
                codec_data.append((file, "File not found", "File not found", "N/A"))
                continue

            try:
                # Command to get the video codec
                video_codec = subprocess.run(
                    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                ).stdout.strip()

                # Command to get the audio codec
                audio_codec = subprocess.run(
                    ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                ).stdout.strip()

                # Get file size in MB
                file_size = os.path.getsize(file) / (1024 * 1024)

                codec_data.append((file, video_codec or "N/A", audio_codec or "N/A", f"{file_size:.2f} MB"))
            except Exception as e:
                codec_data.append((file, "Error", "Error", "N/A"))

        self.file_display.config(state=tk.NORMAL)
        self.file_display.delete(1.0, tk.END)
        if codec_data:
            self.file_display.insert(tk.END, f"{'File':<50}{'Video Codec':<20}{'Audio Codec':<20}{'Size':<10}\n")
            self.file_display.insert(tk.END, f"{'-'*100}\n")
            for file, video_codec, audio_codec, file_size in codec_data:
                self.file_display.insert(tk.END, f"{file:<50}{video_codec:<20}{audio_codec:<20}{file_size:<10}\n")
        else:
            self.file_display.insert(tk.END, "No files selected.")
        self.file_display.config(state=tk.DISABLED)

    # function to convert mp4 to mp3
    def open_mp4_to_mp3_window(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected. Please use 'Open files'.")
            return
        for file in self.selected_files:
            if not os.path.exists(file):
                messagebox.showerror("Error", f"The file does not exist: {file}")
                continue
            if file.endswith(".mp4"):
                output_file = os.path.splitext(file)[0] + ".mp3"
                try:
                    command = (ffmpeg.input(file)
                    .output(output_file, acodec='aac', audio_bitrate='128k'))
                    print(f"FFmpeg command: {command}")
                    command.run()
                    messagebox.showinfo("Success", f"File converted: {output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {file}: {e}")

    # function to compress mp3
    def open_compress_mp3_window(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected. Please use 'Open files'.")
            return
        for file in self.selected_files:
            if not os.path.exists(file):
                messagebox.showerror("Error", f"The file does not exist: {file}")
                continue
            if file.endswith(".mp3"):
                output_file = os.path.splitext(file)[0] + "_compressed.mp3"
                try:
                    command = (ffmpeg.input(file).output(output_file, acodec='aac', audio_bitrate='128k'))
                    print(f"FFmpeg command: {command}")
                    command.run()
                    messagebox.showinfo("Success", f"File compressed: {output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {file}: {e}")

    # function to convert to HEVC
    def open_h265_window(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected. Please use 'Open files'.")
            return
        for file in self.selected_files:
            if not os.path.exists(file):
                messagebox.showerror("Error", f"The file does not exist: {file}")
                continue
            if file.endswith(".mp4"):
                output_file = os.path.splitext(file)[0] + "_hevc.mp4"
                try:
                    command = (ffmpeg.input(file)
                    .output(output_file,
                            # vcodec='hevc_nvenc',
                            vcodec='libx265',
                            preset='medium',    
                            crf=28,
                            acodec='aac',
                            audio_bitrate='128k'
                        )
                    )
                    print(f"FFmpeg command: {command}")
                    command.run()
                    messagebox.showinfo("Success", f"File converted: {output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {file}: {e}")

    # function to convert to HEVC
    def open_hevc_window(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected. Please use 'Open files'.")
            return
        for file in self.selected_files:
            if not os.path.exists(file):
                messagebox.showerror("Error", f"The file does not exist: {file}")
                continue
            if file.endswith(".mp4"):
                output_file = os.path.splitext(file)[0] + "_hevc.mp4"
                try:
                    command = (ffmpeg.input(file)
                    .output(output_file,
                            vcodec='hevc_nvenc',
                            preset='medium',
                            acodec='aac',
                            audio_bitrate='128k'
                        )
                    )
                    print(f"FFmpeg command: {command}")
                    command.run()
                    messagebox.showinfo("Success", f"File converted: {output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {file}: {e}")

    # function to show codec info of the selected files
    def open_codec_info_window(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected. Please use 'Open files'.")
            return

        for file in self.selected_files:
            if not os.path.exists(file):
                messagebox.showerror("Error", f"The file does not exist: {file}")
                continue

            try:
                # Command to get the video codec
                video_codec = subprocess.run(
                    ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                ).stdout.strip()

                # Command to get the audio codec
                audio_codec = subprocess.run(
                    ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                ).stdout.strip()

                if not video_codec and not audio_codec:
                    messagebox.showinfo("Codec info", f"No codec information found for {file}.")
                else:
                    messagebox.showinfo(
                        "Codec info",
                        f"Codec info for {file}:\nVideo codec: {video_codec}\nAudio codec: {audio_codec}"
                    )

            except Exception as e:
                messagebox.showerror("Error", f"Error processing {file}: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FFmpegApp()
    app.run()
