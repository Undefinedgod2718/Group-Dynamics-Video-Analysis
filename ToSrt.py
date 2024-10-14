import os
from moviepy.editor import VideoFileClip
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 初始化 OpenAI 客户端
client = OpenAI()

# 設置輸入和輸出路徑
video_path = "D:/Users/user/Videos/video test/introduction.wmv"
audio_output_path = "audio_output.mp3"
video_output_path = "video_output_without_audio.mp4"

def separate_audio_video(video_path, audio_output_path, video_output_path):
    # 检查音频和视频文件是否已存在
    if os.path.exists(audio_output_path) and os.path.exists(video_output_path):
        print("音频和视频文件已存在，跳过转录过程。")
        return audio_output_path, video_output_path

    # 讀取影片
    clip = VideoFileClip(video_path)

    # 提取音頻部分（如果音频文件不存在）
    if not os.path.exists(audio_output_path):
        audio = clip.audio
        audio.write_audiofile(audio_output_path)
        print("音频文件已生成。")
    else:
        print("音频文件已存在，跳过音频提取。")

    # 提取視頻部分（如果无音视频文件不存在）
    if not os.path.exists(video_output_path):
        clip.without_audio().write_videofile(video_output_path, codec="libx264", audio_codec='none')
        print("无音视频文件已生成。")
    else:
        print("无音视频文件已存在，跳过视频提取。")

    clip.close()
    print("影片和音頻分離完成！")
    return audio_output_path, video_output_path

# 使用 Whisper API 轉錄音頻
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="verbose_json"
        )
    return transcript

# 根據字幕內容和時間戳生成 SRT 格式
def generate_srt(transcript, max_chars=20):
    subtitles = []
    for i, segment in enumerate(transcript.segments):
        start_time = segment.start
        end_time = segment.end
        text = segment.text
        
        # 將文本切成每行不超過 max_chars 字的片段
        lines = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
        
        # 將時間格式轉換為 SRT 的標準時間格式
        start = convert_time(start_time)
        end = convert_time(end_time)
        
        # 生成每一段字幕
        for j, line in enumerate(lines):
            subtitles.append(f"{i * len(lines) + j + 1}\n{start} --> {end}\n{line.strip()}\n")
    
    return "\n".join(subtitles)

# 將時間轉換為 SRT 格式 (00:00:00,000)
def convert_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

# 儲存 SRT 文件
def save_srt(subtitles, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(subtitles)

# 主程序
def main():
    # 分離音頻和視頻
    audio_file_path, _ = separate_audio_video(video_path, audio_output_path, video_output_path)

    # 轉錄音頻
    transcript = transcribe_audio(audio_file_path)

    # 生成 SRT 格式的字幕
    srt_content = generate_srt(transcript)

    # 保存 SRT 文件
    srt_output_path = "subtitle_output.srt"
    save_srt(srt_content, srt_output_path)

    print(f"字幕生成完成！SRT文件已保存至 {srt_output_path}")

if __name__ == "__main__":
    main()
