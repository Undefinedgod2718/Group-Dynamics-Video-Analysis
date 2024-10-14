from moviepy.editor import VideoFileClip
import os

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

# 如果直接運行此腳本，則執行以下代碼
if __name__ == "__main__":
    video_path = "D:/Users/user/Videos/video test/introduction.wmv"
    audio_output_path = "audio_output.mp3"
    video_output_path = "video_output_without_audio.mp4"
    separate_audio_video(video_path, audio_output_path, video_output_path)