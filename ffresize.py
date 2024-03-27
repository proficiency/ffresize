import subprocess
import os
import sys
import mimetypes

def is_file_video(filename: str) -> bool:
    mimetype = mimetypes.guess_type(filename)
    if (not mimetype or not mimetype[0]):
        return False

    return mimetype[0].startswith("video/")

def get_audio_size(input_file: str, duration: float) -> float:
    # get audio bitrate in bits
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    result = subprocess.check_output(ffprobe_cmd).strip()
    
    # mkv files always seem to return "N/A", I didn't find a solution to this sadly.
    if result.decode('utf-8') == "N/A":
        return 0
    
    # convert from bits to kilobits
    audio_bitrate = int(result) / 1000

    # get a list of all the audio tracks, the length of that list is how many tracks there are
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', input_file]
    num_audio_tracks = len(subprocess.check_output(ffprobe_cmd, text=True).strip().split('\n'))

    return num_audio_tracks * duration * audio_bitrate

def reencode_to_target_size(input_file: str, output_file: str, target_size: int):
    if not os.path.exists(input_file):
        print(f"{input_file} not found")
        return
    
    if not is_file_video(input_file):
         print(f"{input_file} is not a video")
         return
    
    # get duration in seconds
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
    duration = float(subprocess.check_output(ffprobe_cmd).strip())
    
    # convert target_size(in megabytes) to kilobits, subtract size of audio as well as 5% of the desired size to lazily account for container overhead
    target_size *= 8000
    target_size -= get_audio_size(input_file, duration)
    target_size -= target_size * 0.05

    # calculate required bitrate to meet target filesize
    video_bitrate = int(target_size / duration)

    # reencode with our new bitrate
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-pass', '1', '-b:v', str(video_bitrate) + 'k', '-y', output_file]
    subprocess.run(ffmpeg_cmd)
    ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-pass', '2', '-b:v', str(video_bitrate) + 'k', '-y', output_file]
    subprocess.run(ffmpeg_cmd)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: py ffresize.py \"input file\" \"output file\" \"target size in megabytes(e.g. 5)\"")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    target_size = int(sys.argv[3])
    reencode_to_target_size(input_file, output_file, target_size)
