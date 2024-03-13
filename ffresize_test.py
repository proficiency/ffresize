import subprocess
import os
import random

def is_file_video(filename):
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1:nokey=1', '-i', filename], capture_output=True, text=True)
        codec_type = result.stdout.strip()
        return codec_type == 'video'

def get_random_size(filesize):
        return random.randrange(1, int(filesize))
        
def run_ffresize(input_file, output_file, target_size):
        subprocess.run(["py", "ffresize.py", input_file, output_file, str(target_size)], check=True)

if __name__ == "__main__":
        directory = os.listdir("./")
        for filename in directory:
                if is_file_video(filename):
                        original_size = os.path.getsize(filename)
                        target_size = int(get_random_size(original_size) / 1024 / 1024)

                        name, ext = os.path.splitext(filename)
                        out_filename = f"{name}_{target_size}{ext}"

                        run_ffresize(filename, out_filename, target_size)
                        out_size = os.path.getsize(out_filename)

                        log_file = open("ffresize_test.txt", 'a')

                        original_size = int(original_size / 1024 / 1024)
                        out_size = int(out_size / 1024 / 1024)

                        print(f"original size: {original_size}, target size: {target_size}, actual output size: {out_size} difference: {abs(target_size - out_size)}", file = log_file)
                        log_file.close()
