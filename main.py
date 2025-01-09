import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
import os

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

        # Buttons for operations
        tk.Button(self.menu_frame, text="Open files",           command=self.open_files, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Clear files",          command=self.clear_files, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Re-encode to H.265",   command=self.open_h265_window, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Re-encode to HEVC", command=self.open_hevc_window, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Convert MP4 to MP3",   command=self.open_mp4_to_mp3_window, width=25).pack(pady=5)
        tk.Button(self.menu_frame, text="Compress MP3",         command=self.open_compress_mp3_window, width=25).pack(pady=5)

        # Display selected files
        self.file_display = tk.Text(self.root, height=10, width=80)
        self.file_display.pack(pady=10)
        self.file_display.config(state=tk.DISABLED)

    def open_files(self):
        files = filedialog.askopenfilenames(filetypes=[
            ("Supported files", "*.mp4 *.mp3"),
            ("Video files", "*.mp4"),
            ("Audio files", "*.mp3")
        ])
        if files:
            self.selected_files = list(files)
            self.update_file_display()

    def clear_files(self):
        self.selected_files = []
        self.update_file_display()

    def update_file_display(self):
        self.file_display.config(state=tk.NORMAL)
        self.file_display.delete(1.0, tk.END)
        if self.selected_files:
            self.file_display.insert(tk.END, "Selected files:\n")
            for file in self.selected_files:
                self.file_display.insert(tk.END, file + "\n")
        else:
            self.file_display.insert(tk.END, "No files selected.")
        self.file_display.config(state=tk.DISABLED)

    def open_h265_window(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected. Please use 'Open files'.")
            return
        for file in self.selected_files:
            if not os.path.exists(file):
                messagebox.showerror("Error", f"The file does not exist: {file}")
                continue
            if file.endswith(".mp4"):
                output_file = os.path.splitext(file)[0] + "_h265.mp4"
                try:
                    command = (ffmpeg.input(file)
                    .output(output_file,
                            vcodec='libx265',
                            preset='medium',    
                            crf=28,
                            # acodec='aac',
                            # audio_bitrate='128k'
                            acodec = 'copy'
                        )
                    )
                    print(f"FFmpeg command: {command}")
                    command.run()
                    messagebox.showinfo("Success", f"File converted: {output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {file}: {e}")

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
                            cq=28,
                            acodec='aac',
                            audio_bitrate='128k'
                        )
                    )
                    print(f"FFmpeg command: {command}")
                    command.run()
                    messagebox.showinfo("Success", f"File converted: {output_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Error processing {file}: {e}")


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FFmpegApp()
    app.run()
