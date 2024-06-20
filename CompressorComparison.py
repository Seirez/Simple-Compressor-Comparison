import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from pydub import AudioSegment
import os
import time
import subprocess
import numpy as np

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compression Algorithm Comparison")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Menu
        self.menu_frame = tk.Frame(self.main_frame)
        self.menu_frame.pack(pady=5)

        self.choose_label = tk.Label(self.menu_frame, text="Choose Task:")
        self.choose_label.grid(row=0, column=0)

        self.task_var = tk.StringVar()
        self.task_var.set("")

        self.audio_compressor_button = tk.Radiobutton(self.menu_frame, text="Audio Compression", variable=self.task_var, value="Audio Compression")
        self.audio_compressor_button.grid(row=0, column=1)

        self.image_resizer_button = tk.Radiobutton(self.menu_frame, text="Image Compression", variable=self.task_var, value="Image Compression")
        self.image_resizer_button.grid(row=0, column=2)

        self.video_compressor_button = tk.Radiobutton(self.menu_frame, text="Video Compression", variable=self.task_var, value="Video Compression")
        self.video_compressor_button.grid(row=0, column=3)

        self.perform_button = tk.Button(self.menu_frame, text="Perform Task", command=self.perform_task)
        self.perform_button.grid(row=0, column=4, padx=10)

        # Image Compression Widgets
        self.image_frame = tk.Frame(self.main_frame)

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        self.load_image_button = tk.Button(self.image_frame, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=5)

        self.algorithm_var = tk.StringVar(value="DCT")
        self.algorithm_label = tk.Label(self.image_frame, text="Choose Compression Algorithm:")
        self.algorithm_label.pack()

        self.algorithm1_radio = tk.Radiobutton(self.image_frame, text="DCT", variable=self.algorithm_var, value="DCT")
        self.algorithm1_radio.pack()
        self.algorithm2_radio = tk.Radiobutton(self.image_frame, text="Fractal", variable=self.algorithm_var, value="Fractal")
        self.algorithm2_radio.pack()

        self.compress_image_button = tk.Button(self.image_frame, text="Compress Image", command=self.compress_image)
        self.compress_image_button.pack(pady=5)

        self.save_image_button = tk.Button(self.image_frame, text="Save Image", command=self.save_image)
        self.save_image_button.pack(pady=5)

        self.image_result_label = tk.Label(self.image_frame)
        self.image_result_label.pack(pady=5)

        # Audio Compression Widgets
        self.audio_frame = tk.Frame(self.main_frame)

        self.load_audio_button = tk.Button(self.audio_frame, text="Load Audio", command=self.load_audio)
        self.load_audio_button.pack(pady=5)

        self.algorithm_var_audio = tk.StringVar(value="DCT")
        self.algorithm_label_audio = tk.Label(self.audio_frame, text="Choose Compression Algorithm:")
        self.algorithm_label_audio.pack()

        self.algorithm1_radio_audio = tk.Radiobutton(self.audio_frame, text="DCT", variable=self.algorithm_var_audio, value="DCT")
        self.algorithm1_radio_audio.pack()
        self.algorithm2_radio_audio = tk.Radiobutton(self.audio_frame, text="Fractal", variable=self.algorithm_var_audio, value="Fractal")
        self.algorithm2_radio_audio.pack()

        self.compress_audio_button = tk.Button(self.audio_frame, text="Compress Audio", command=self.compress_audio)
        self.compress_audio_button.pack(pady=5)

        self.save_audio_button = tk.Button(self.audio_frame, text="Save Audio", command=self.save_audio)
        self.save_audio_button.pack(pady=5)

        self.audio_result_label = tk.Label(self.audio_frame)
        self.audio_result_label.pack(pady=5)

        # Video Compression Widgets
        self.video_frame = tk.Frame(self.main_frame)

        self.load_video_button = tk.Button(self.video_frame, text="Load Video", command=self.load_video)
        self.load_video_button.pack(pady=5)

        self.algorithm_var_video = tk.StringVar(value="DCT")
        self.algorithm_label_video = tk.Label(self.video_frame, text="Choose Compression Algorithm:")
        self.algorithm_label_video.pack()

        self.algorithm1_radio_video = tk.Radiobutton(self.video_frame, text="DCT", variable=self.algorithm_var_video, value="DCT")
        self.algorithm1_radio_video.pack()
        self.algorithm2_radio_video = tk.Radiobutton(self.video_frame, text="Fractal", variable=self.algorithm_var_video, value="Fractal")
        self.algorithm2_radio_video.pack()

        self.compress_video_button = tk.Button(self.video_frame, text="Compress Video", command=self.compress_video)
        self.compress_video_button.pack(pady=5)

        self.save_video_button = tk.Button(self.video_frame, text="Save Video", command=self.save_video)
        self.save_video_button.pack(pady=5)

        self.video_result_label = tk.Label(self.video_frame)
        self.video_result_label.pack(pady=5)

        # Hide processing frames by default
        self.image_frame.pack_forget()
        self.audio_frame.pack_forget()
        self.video_frame.pack_forget()

        # Initialize attributes
        self.image = None
        self.audio = None
        self.video = None
        self.compressed_image = None
        self.compressed_audio = None
        self.compressed_video = None

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image = cv2.imread(path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, image):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image

    def compress_image_dct(self, image):
        # Convert image to float32 and grayscale
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image_float32 = np.float32(image_gray) / 255.0
        
        # Apply DCT
        image_dct = cv2.dct(image_float32)
        
        # Perform quantization (optional)
        # Example: quantization_matrix = np.ones(image_dct.shape, dtype=np.float32) * 0.1
        # image_dct_quantized = np.round(image_dct / quantization_matrix)
        # compressed_image_float32 = cv2.idct(image_dct_quantized * quantization_matrix)
        
        # Apply inverse DCT
        compressed_image_float32 = cv2.idct(image_dct)
        
        # Convert back to uint8 for display
        compressed_image = np.uint8(compressed_image_float32 * 255.0)
        
        return compressed_image

    def compress_image_fractal(self, image):
        height, width = image.shape[:2]
        block_size = 8  # Assuming a block size of 8

        fractal_image = np.zeros_like(image)

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                avg = np.mean(image[max(0, y - block_size):y, max(0, x - block_size):x].ravel()) if (y >= block_size and x >= block_size) else image[y, x]
                fractal_image[y, x] = avg

                if y > block_size and x > block_size:
                    fractal_image[y - block_size, x] = (image[y - block_size, x] + avg) / 2 if (y - block_size) >= 0 else avg
                    fractal_image[y, x - block_size] = (image[y, x - block_size] + avg) / 2 if (x - block_size) >= 0 else avg

                if y > block_size and (x + block_size) < width:
                    temp_avg = avg if (x - block_size) < 0 or (y + block_size) >= height else (fractal_image[y + block_size, x - block_size] + avg) / 2
                if (y + block_size) < height and x > block_size:
                    fractal_image[y + block_size, x - block_size] = (image[y + block_size, x - block_size] + avg) / 2 if (x - block_size) >= 0 and (y + block_size) < height else avg

        print("Compressed a frame.")
        return fractal_image
    
    def compress_image(self):
        if self.image is not None:
            algorithm = self.algorithm_var.get()
            start_time = time.time()
            if algorithm == "DCT":
                self.compressed_image = self.compress_image_dct(self.image)
            elif algorithm == "Fractal":
                self.compressed_image = self.compress_image_fractal(self.image)
            end_time = time.time()
            elapsed_time = end_time - start_time

            temp_path = "temp_compressed_image.png"
            cv2.imwrite(temp_path, cv2.cvtColor(self.compressed_image, cv2.COLOR_RGB2BGR))
            self.display_image(self.compressed_image)

            file_size = os.path.getsize(temp_path)
            os.remove(temp_path)

            self.image_result_label.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        else:
            print("No image loaded.")

    def save_image(self):
        if self.compressed_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if path:
                cv2.imwrite(path, cv2.cvtColor(self.compressed_image, cv2.COLOR_RGB2BGR))
                print("Image saved successfully.")
        else:
            print("No compressed image to save.")

    def load_audio(self):
        path = filedialog.askopenfilename()
        if path:
            self.audio = AudioSegment.from_file(path)

    def compress_audio_dct(self, audio):
        # Placeholder for DCT compression for audio
        # For simplicity, we'll export the audio at 64 kbps
        return audio.export(format="mp3", bitrate="64k")

    def compress_audio_fractal(self, audio):
        # Placeholder for Fractal compression for audio
        # For simplicity, we'll export the audio at 32 kbps
        return audio.export(format="mp3", bitrate="32k")

    def compress_audio(self):
        if self.audio:
            algorithm = self.algorithm_var_audio.get()
            start_time = time.time()
            temp_path = "temp_compressed_audio.mp3"
            if algorithm == "DCT":
                self.compressed_audio = self.compress_audio_dct(self.audio)
            elif algorithm == "Fractal":
                self.compressed_audio = self.compress_audio_fractal(self.audio)
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = os.path.getsize(temp_path)
            os.remove(temp_path)

            self.audio_result_label.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        else:
            print("No audio loaded.")

    def save_audio(self):
        if self.compressed_audio:
            path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if path:
                self.compressed_audio.export(path, format="mp3")
                print("Audio saved successfully.")
        else:
            print("No compressed audio to save.")

    def load_video(self):
        path = filedialog.askopenfilename()
        if path:
            self.video = path  # Just storing the path for simplicity

    def compress_video_dct(self, video_path):
        # Placeholder for DCT compression for video
        temp_path = "temp_compressed_video.mp4"
        subprocess.run(['ffmpeg', '-i', video_path, '-c:v', 'libx264', temp_path])
        return temp_path

    def compress_video_fractal(self, video_path):
        # Placeholder for Fractal compression for video
        # For simplicity, this function will resize the video
        temp_path = "temp_compressed_video.mp4"
        subprocess.run(['ffmpeg', '-i', video_path, '-vf', 'scale=iw/2:ih/2', temp_path])
        return temp_path

    def compress_video(self):
        if self.video:
            algorithm = self.algorithm_var_video.get()
            start_time = time.time()
            if algorithm == "DCT":
                self.compressed_video = self.compress_video_dct(self.video)
            elif algorithm == "Fractal":
                self.compressed_video = self.compress_video_fractal(self.video)
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = os.path.getsize(self.compressed_video)
            self.video_result_label.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        else:
            print("No video loaded.")

    def save_video(self):
        if self.compressed_video:
            path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
            if path:
                os.rename(self.compressed_video, path)
                print("Video saved successfully.")
        else:
            print("No compressed video to save.")

    def perform_task(self):
        task = self.task_var.get()
        if task == "Image Compression":
            self.audio_frame.pack_forget()
            self.video_frame.pack_forget()
            self.image_frame.pack()
        elif task == "Audio Compression":
            self.image_frame.pack_forget()
            self.video_frame.pack_forget()
            self.audio_frame.pack()
        elif task == "Video Compression":
            self.image_frame.pack_forget()
            self.audio_frame.pack_forget()
            self.video_frame.pack()

def main():
    root = tk.Tk()
    app = CompressionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()