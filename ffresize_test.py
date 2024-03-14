import subprocess
import os
import random
import mimetypes

def is_file_video(filename: str) -> bool:
    mimetype = mimetypes.guess_type(filename)
    if (not mimetype or not mimetype[0]):
        return False
    
    return mimetype[0].startswith("video/")

def get_random_size(filesize: int) -> int:
        return random.randrange(1, int(filesize))
        
def run_ffresize(input_file: str, output_file: str, target_size: int):
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
