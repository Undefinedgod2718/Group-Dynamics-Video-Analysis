from moviepy.editor import VideoFileClip
import re
import os
from datetime import timedelta

def parse_srt(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    segments = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', content, re.DOTALL)
    return segments

def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    s, ms = s.split(',')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def seconds_to_time(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def cut_video(video_file, srt_file, output_folder):
    segments = parse_srt(srt_file)
    video = VideoFileClip(video_file)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for i, (start, end, text) in enumerate(segments):
        start_time = time_to_seconds(start)
        end_time = time_to_seconds(end)
        
        # Add 3 seconds to the end time
        extended_end_time = end_time + 8
        
        # Ensure the extended end time doesn't exceed the video duration
        extended_end_time = min(extended_end_time, video.duration)

        clip = video.subclip(start_time, extended_end_time)
        output_file = os.path.join(output_folder, f"video_segment_analysis_{i+1}.mp4")
        clip.write_videofile(output_file, codec="libx264")

        # Print the original and extended time ranges
        print(f"Segment {i+1}:")
        print(f"Original: {start} --> {end}")
        print(f"Extended: {start} --> {seconds_to_time(extended_end_time)}")
        print()

    video.close()

# Usage example
video_file = "video_output_without_audio.mp4"  # Replace with your video file path
srt_file = "video_segment_analysis.srt"  # Replace with your .srt file path
output_folder = "D:/Users/user/Documents/Video understanding"  # Replace with your desired output folder path

cut_video(video_file, srt_file, output_folder)
