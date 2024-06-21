import tkinter as tk
from tkinter import filedialog
import os
import time
import gzip
import lzma

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

        self.audio_decompressor_button = tk.Radiobutton(self.menu_frame, text="Audio Decompression", variable=self.task_var, value="Audio Decompression")
        self.audio_decompressor_button.grid(row=0, column=2)

        self.image_compressor_button = tk.Radiobutton(self.menu_frame, text="Image Compression", variable=self.task_var, value="Image Compression")
        self.image_compressor_button.grid(row=0, column=3)

        self.image_decompressor_button = tk.Radiobutton(self.menu_frame, text="Image Decompression", variable=self.task_var, value="Image Decompression")
        self.image_decompressor_button.grid(row=0, column=4)

        self.video_compressor_button = tk.Radiobutton(self.menu_frame, text="Video Compression", variable=self.task_var, value="Video Compression")
        self.video_compressor_button.grid(row=0, column=5)

        self.video_decompressor_button = tk.Radiobutton(self.menu_frame, text="Video Decompression", variable=self.task_var, value="Video Decompression")
        self.video_decompressor_button.grid(row=0, column=6)

        self.perform_button = tk.Button(self.menu_frame, text="Perform Task", command=self.perform_task)
        self.perform_button.grid(row=0, column=7, padx=10)

        # Audio Compression Widgets
        self.audio_frame = tk.Frame(self.main_frame)

        self.load_audio_button = tk.Button(self.audio_frame, text="Load Audio", command=self.load_audio)
        self.load_audio_button.pack(pady=5)

        self.audio_load_label = tk.Label(self.audio_frame)
        self.audio_load_label.pack(pady=5)

        self.algorithm_var_audio = tk.StringVar(value="gzip")
        self.algorithm_label_audio = tk.Label(self.audio_frame, text="Choose Compression Algorithm:")
        self.algorithm_label_audio.pack()

        self.algorithm1_radio_audio = tk.Radiobutton(self.audio_frame, text="gzip", variable=self.algorithm_var_audio, value="gzip")
        self.algorithm1_radio_audio.pack()
        self.algorithm2_radio_audio = tk.Radiobutton(self.audio_frame, text="lzma", variable=self.algorithm_var_audio, value="lzma")
        self.algorithm2_radio_audio.pack()

        self.compress_audio_button = tk.Button(self.audio_frame, text="Compress Audio", command=self.compress_audio)
        self.compress_audio_button.pack(pady=5)

        self.save_audio_button = tk.Button(self.audio_frame, text="Save Audio", command=self.save_compressed_audio)
        self.save_audio_button.pack(pady=5)

        self.audio_result_label = tk.Label(self.audio_frame)
        self.audio_result_label.pack(pady=5)

        # Audio Decompression Widgets
        self.daudio_frame = tk.Frame(self.main_frame)

        self.load_compressed_audio_button = tk.Button(self.daudio_frame, text="Load Compressed Audio", command=self.load_compressed_audio)
        self.load_compressed_audio_button.pack(pady=5)

        self.compressed_audio_load_label = tk.Label(self.daudio_frame)
        self.compressed_audio_load_label.pack(pady=5)

        self.algorithm_var_deaudio = tk.StringVar(value="gzip")
        self.algorithm_label_deaudio = tk.Label(self.daudio_frame, text="Choose Decompression Algorithm:")
        self.algorithm_label_deaudio.pack()

        self.algorithm1_radio_deaudio = tk.Radiobutton(self.daudio_frame, text="gzip", variable=self.algorithm_var_deaudio, value="gzip")
        self.algorithm1_radio_deaudio.pack()
        self.algorithm2_radio_deaudio = tk.Radiobutton(self.daudio_frame, text="lzma", variable=self.algorithm_var_deaudio, value="lzma")
        self.algorithm2_radio_deaudio.pack()

        self.decompress_audio_button = tk.Button(self.daudio_frame, text="Decompress Audio", command=self.decompress_audio)
        self.decompress_audio_button.pack(pady=5)

        self.save_decompressed_audio_button = tk.Button(self.daudio_frame, text="Save Decompressed Audio", command=self.save_decompressed_audio)
        self.save_decompressed_audio_button.pack(pady=5)

        self.decompressed_audio_result_label = tk.Label(self.daudio_frame)
        self.decompressed_audio_result_label.pack(pady=5)

        # Image Compression Widgets
        self.image_frame = tk.Frame(self.main_frame)

        self.load_image_button = tk.Button(self.image_frame, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=5)

        self.image_load_label = tk.Label(self.image_frame)
        self.image_load_label.pack(pady=5)

        self.algorithm_var_image = tk.StringVar(value="gzip")
        self.algorithm_label_image = tk.Label(self.image_frame, text="Choose Compression Algorithm:")
        self.algorithm_label_image.pack()

        self.algorithm1_radio_image = tk.Radiobutton(self.image_frame, text="gzip", variable=self.algorithm_var_image, value="gzip")
        self.algorithm1_radio_image.pack()
        self.algorithm2_radio_image = tk.Radiobutton(self.image_frame, text="lzma", variable=self.algorithm_var_image, value="lzma")
        self.algorithm2_radio_image.pack()

        self.compress_image_button = tk.Button(self.image_frame, text="Compress Image", command=self.compress_image)
        self.compress_image_button.pack(pady=5)

        self.save_image_button = tk.Button(self.image_frame, text="Save Image", command=self.save_image)
        self.save_image_button.pack(pady=5)

        self.image_result_label = tk.Label(self.image_frame)
        self.image_result_label.pack(pady=5)

        # Image Decompression Widgets
        self.dimage_frame = tk.Frame(self.main_frame)

        self.load_compressed_image_button = tk.Button(self.dimage_frame, text="Load Compressed Image", command=self.load_compressed_image)
        self.load_compressed_image_button.pack(pady=5)

        self.compressed_image_load_label = tk.Label(self.dimage_frame)
        self.compressed_image_load_label.pack(pady=5)

        self.algorithm_var_deimage = tk.StringVar(value="gzip")
        self.algorithm_label_deimage = tk.Label(self.dimage_frame, text="Choose Decompression Algorithm:")
        self.algorithm_label_deimage.pack()

        self.algorithm1_radio_deimage = tk.Radiobutton(self.dimage_frame, text="gzip", variable=self.algorithm_var_deimage, value="gzip")
        self.algorithm1_radio_deimage.pack()
        self.algorithm2_radio_deimage = tk.Radiobutton(self.dimage_frame, text="lzma", variable=self.algorithm_var_deimage, value="lzma")
        self.algorithm2_radio_deimage.pack()

        self.decompress_image_button = tk.Button(self.dimage_frame, text="Decompress Image", command=self.decompress_image)
        self.decompress_image_button.pack(pady=5)

        self.save_decompressed_image_button = tk.Button(self.dimage_frame, text="Save Decompressed Image", command=self.save_decompressed_image)
        self.save_decompressed_image_button.pack(pady=5)

        self.decompressed_image_result_label = tk.Label(self.dimage_frame)
        self.decompressed_image_result_label.pack(pady=5)

        # Video Compression Widgets
        self.video_frame = tk.Frame(self.main_frame)

        self.load_video_button = tk.Button(self.video_frame, text="Load Video", command=self.load_video)
        self.load_video_button.pack(pady=5)

        self.video_load_label = tk.Label(self.video_frame)
        self.video_load_label.pack(pady=5)

        self.algorithm_var_video = tk.StringVar(value="gzip")
        self.algorithm_label_video = tk.Label(self.video_frame, text="Choose Compression Algorithm:")
        self.algorithm_label_video.pack()

        self.algorithm1_radio_video = tk.Radiobutton(self.video_frame, text="gzip", variable=self.algorithm_var_video, value="gzip")
        self.algorithm1_radio_video.pack()
        self.algorithm2_radio_video = tk.Radiobutton(self.video_frame, text="lzma", variable=self.algorithm_var_video, value="lzma")
        self.algorithm2_radio_video.pack()

        self.compress_video_button = tk.Button(self.video_frame, text="Compress Video", command=self.compress_video)
        self.compress_video_button.pack(pady=5)

        self.save_video_button = tk.Button(self.video_frame, text="Save Video", command=self.save_video)
        self.save_video_button.pack(pady=5)

        self.video_result_label = tk.Label(self.video_frame)
        self.video_result_label.pack(pady=5)

        # Video Decompression Widgets
        self.dvideo_frame = tk.Frame(self.main_frame)

        self.load_compressed_video_button = tk.Button(self.dvideo_frame, text="Load Compressed Video", command=self.load_compressed_video)
        self.load_compressed_video_button.pack(pady=5)

        self.compressed_video_load_label = tk.Label(self.dvideo_frame)
        self.compressed_video_load_label.pack(pady=5)

        self.algorithm_var_devideo = tk.StringVar(value="gzip")
        self.algorithm_label_devideo = tk.Label(self.dvideo_frame, text="Choose Decompression Algorithm:")
        self.algorithm_label_devideo.pack()

        self.algorithm1_radio_devideo = tk.Radiobutton(self.dvideo_frame, text="gzip", variable=self.algorithm_var_devideo, value="gzip")
        self.algorithm1_radio_devideo.pack()
        self.algorithm2_radio_devideo = tk.Radiobutton(self.dvideo_frame, text="lzma", variable=self.algorithm_var_devideo, value="lzma")
        self.algorithm2_radio_devideo.pack()

        self.decompress_video_button = tk.Button(self.dvideo_frame, text="Decompress Video", command=self.decompress_video)
        self.decompress_video_button.pack(pady=5)

        self.save_decompressed_video_button = tk.Button(self.dvideo_frame, text="Save Decompressed Video", command=self.save_decompressed_video)
        self.save_decompressed_video_button.pack(pady=5)

        self.decompressed_video_result_label = tk.Label(self.dvideo_frame)
        self.decompressed_video_result_label.pack(pady=5)

        self.current_frame = None

    def perform_task(self):
        task = self.task_var.get()
        if task == "Audio Compression":
            self.audio_frame.pack_forget()
            self.daudio_frame.pack_forget()
            self.image_frame.pack_forget()
            self.dimage_frame.pack_forget()
            self.video_frame.pack_forget()
            self.dvideo_frame.pack_forget()

            self.current_frame = self.audio_frame
        elif task == "Audio Decompression":
            self.audio_frame.pack_forget()
            self.daudio_frame.pack_forget()
            self.image_frame.pack_forget()
            self.dimage_frame.pack_forget()
            self.video_frame.pack_forget()
            self.dvideo_frame.pack_forget()

            self.current_frame = self.daudio_frame
        elif task == "Image Compression":
            self.audio_frame.pack_forget()
            self.daudio_frame.pack_forget()
            self.image_frame.pack_forget()
            self.dimage_frame.pack_forget()
            self.video_frame.pack_forget()
            self.dvideo_frame.pack_forget()

            self.current_frame = self.image_frame
        elif task == "Image Decompression":
            self.audio_frame.pack_forget()
            self.daudio_frame.pack_forget()
            self.image_frame.pack_forget()
            self.dimage_frame.pack_forget()
            self.video_frame.pack_forget()
            self.dvideo_frame.pack_forget()
            
            self.current_frame = self.dimage_frame
        elif task == "Video Compression":
            self.audio_frame.pack_forget()
            self.daudio_frame.pack_forget()
            self.image_frame.pack_forget()
            self.dimage_frame.pack_forget()
            self.video_frame.pack_forget()
            self.dvideo_frame.pack_forget()
            
            self.current_frame = self.video_frame
        elif task == "Video Decompression":
            self.audio_frame.pack_forget()
            self.daudio_frame.pack_forget()
            self.image_frame.pack_forget()
            self.dimage_frame.pack_forget()
            self.video_frame.pack_forget()
            self.dvideo_frame.pack_forget()
            
            self.current_frame = self.dvideo_frame

        self.current_frame.pack()

    # Audio Compression Methods
    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg")])
        if path:
            self.audio_path = path
            self.audio_load_label.config(text="Audio Loaded")
        else:
            print("Format not supported.")

    def compress_audio(self):
        if not hasattr(self, 'audio_path'):
            print("Load an audio file first.")
            return

        algorithm = self.algorithm_var_audio.get()

        try:
            with open(self.audio_path, 'rb') as f_in:
                audio_data = f_in.read()

            start_time = time.time()

            if algorithm == "gzip":
                compressed_data = gzip.compress(audio_data)
            elif algorithm == "lzma":
                compressed_data = lzma.compress(audio_data)
            else:
                print("Unknown compression algorithm.")
                return

            self.compressed_audio_data = compressed_data

            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = len(compressed_data)
            self.audio_result_label.config(text=f"Audio Compressed Successfully, Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        except Exception as e:
            self.audio_result_label.config(text=f"Compression error: {str(e)}")
            print(f"Compression error: {str(e)}")

    def save_compressed_audio(self):
        if not hasattr(self, 'compressed_audio_data'):
            print("Compress an audio file first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".bin")
        if save_path:
            with open(save_path, 'wb') as f_out:
                f_out.write(self.compressed_audio_data)
            print(f"Compressed audio saved to {save_path}")

    # Audio Decompression Methods
    def load_compressed_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Compressed Audio Files", "*.bin")])
        if path:
            self.compressed_audio_path = path
            self.compressed_audio_load_label.config(text="Compressed Audio Loaded")
        else:
            print("Format not supported.")

    def decompress_audio(self):
        if not hasattr(self, 'compressed_audio_path'):
            print("Load a compressed audio file first.")
            return

        algorithm = self.algorithm_var_deaudio.get()

        try:
            with open(self.compressed_audio_path, 'rb') as f_in:
                compressed_data = f_in.read()

            start_time = time.time()

            if algorithm == "gzip":
                decompressed_data = gzip.decompress(compressed_data)
            elif algorithm == "lzma":
                decompressed_data = lzma.decompress(compressed_data)
            else:
                print("Unknown decompression algorithm.")
                return

            self.decompressed_audio_data = decompressed_data
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = len(decompressed_data)
            self.decompressed_audio_result_label.config(text=f"Audio Decompressed Successfully, Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        except Exception as e:
            self.decompressed_audio_result_label.config(text=f"Decompression error: {str(e)}")
            print(f"Compression error: {str(e)}")

    def save_decompressed_audio(self):
        if not hasattr(self, 'decompressed_audio_data'):
            print("Decompress an audio file first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".wav")
        if save_path:
            with open(save_path, 'wb') as f_out:
                f_out.write(self.decompressed_audio_data)
            print(f"Decompressed audio saved to {save_path}")

    # Image Compression Methods
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.bmp")])
        if path:
            self.image_path = path
            self.image_load_label.config(text="Image Loaded")
        else:
            print("Format not supported.")

    def compress_image(self):
        if not hasattr(self, 'image_path'):
            print("Load an image first.")
            return

        algorithm = self.algorithm_var_image.get()

        try:
            with open(self.image_path, 'rb') as f_in:
                img_data = f_in.read()

            start_time = time.time()

            if algorithm == "gzip":
                compressed_data = gzip.compress(img_data)
            elif algorithm == "lzma":
                compressed_data = lzma.compress(img_data)
            else:
                print("Unknown compression algorithm.")
                return

            self.compressed_image_data = compressed_data
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = len(compressed_data)
            self.image_result_label.config(text=f"Image Compressed Successfully, Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        except Exception as e:
            self.image_result_label.config(text=f"Compression error: {str(e)}")
            print(f"Compression error: {str(e)}")

    def save_image(self):
        if not hasattr(self, 'compressed_image_data'):
            print("Compress an image first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".bin")
        if save_path:
            with open(save_path, 'wb') as f_out:
                f_out.write(self.compressed_image_data)
            print(f"Compressed image saved to {save_path}")

    # Image Decompression Methods
    def load_compressed_image(self):
        path = filedialog.askopenfilename(filetypes=[("Compressed Image Files", "*.bin")])
        if path:
            self.compressed_image_path = path
            self.compressed_image_load_label.config(text="Compressed Image Loaded")
        else:
            print("Format not supported.")

    def decompress_image(self):
        if not hasattr(self, 'compressed_image_path'):
            print("Load a compressed image first.")
            return

        algorithm = self.algorithm_var_deimage.get()

        try:
            with open(self.compressed_image_path, 'rb') as f_in:
                compressed_data = f_in.read()

            start_time = time.time()

            if algorithm == "gzip":
                decompressed_data = gzip.decompress(compressed_data)
            elif algorithm == "lzma":
                decompressed_data = lzma.decompress(compressed_data)
            else:
                print("Unknown decompression algorithm.")
                return

            self.decompressed_image_data = decompressed_data
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = len(decompressed_data)
            self.decompressed_image_result_label.config(text=f"Image Decompressed Successfully, Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        except Exception as e:
            self.decompressed_image_result_label.config(text=f"Decompression error: {str(e)}")
            print(f"Compression error: {str(e)}")

    def save_decompressed_image(self):
        if not hasattr(self, 'decompressed_image_data'):
            print("Decompress an image first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if save_path:
            with open(save_path, 'wb') as f_out:
                f_out.write(self.decompressed_image_data)
            print(f"Decompressed image saved to {save_path}")

    # Video Compression Methods
    def load_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if path:
            self.video_path = path
            self.video_load_label.config(text="Video Loaded")
        else:
            print("Format not supported.")

    def compress_video(self):
        if not hasattr(self, 'video_path'):
            print("Load a video first.")
            return

        algorithm = self.algorithm_var_video.get()

        try:
            with open(self.video_path, 'rb') as f_in:
                video_data = f_in.read()

            start_time = time.time()

            if algorithm == "gzip":
                compressed_data = gzip.compress(video_data)
            elif algorithm == "lzma":
                compressed_data = lzma.compress(video_data)
            else:
                print("Unknown compression algorithm.")
                return

            self.compressed_video_data = compressed_data
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = len(compressed_data)
            self.decompressed_audio_result_label.config(text=f"Video Compressed Successfully, Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        except Exception as e:
            self.decompressed_audio_result_label.config(text=f"Compression error: {str(e)}")
            print(f"Compression error: {str(e)}")

    def save_video(self):
        if not hasattr(self, 'compressed_video_data'):
            print("Compress a video first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".bin")
        if save_path:
            with open(save_path, 'wb') as f_out:
                f_out.write(self.compressed_video_data)
            print(f"Compressed video saved to {save_path}")

    # Video Decompression Methods
    def load_compressed_video(self):
        path = filedialog.askopenfilename(filetypes=[("Compressed Video Files", "*.bin")])
        if path:
            self.compressed_video_path = path
            self.compressed_video_load_label.config(text="Compressed Video Loaded")
        else:
            print("Format not supported.")

    def decompress_video(self):
        if not hasattr(self, 'compressed_video_path'):
            print("Load a compressed video first.")
            return

        algorithm = self.algorithm_var_devideo.get()

        try:
            with open(self.compressed_video_path, 'rb') as f_in:
                compressed_data = f_in.read()

            start_time = time.time()

            if algorithm == "gzip":
                decompressed_data = gzip.decompress(compressed_data)
            elif algorithm == "lzma":
                decompressed_data = lzma.decompress(compressed_data)
            else:
                print("Unknown decompression algorithm.")
                return

            self.decompressed_video_data = decompressed_data
            end_time = time.time()
            elapsed_time = end_time - start_time

            file_size = len(decompressed_data)
            self.decompressed_audio_result_label.config(text=f"Video Decompressed Successfully, Time Elapsed: {elapsed_time:.2f} seconds, Size: {file_size / 1024:.2f} KB")
        except Exception as e:
            self.decompressed_audio_result_label.config(text=f"Decompression error: {str(e)}")
            print(f"Compression error: {str(e)}")

    def save_decompressed_video(self):
        if not hasattr(self, 'decompressed_video_data'):
            print("Decompress a video first.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp4")
        if save_path:
            with open(save_path, 'wb') as f_out:
                f_out.write(self.decompressed_video_data)
            print(f"Decompressed video saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompressionApp(root)
    root.mainloop()