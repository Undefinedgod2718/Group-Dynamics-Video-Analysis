import os
from dotenv import load_dotenv
from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import markdown
import re

# Load environment variables from .env file
# 從 .env 文件加載環境變量
load_dotenv()

# Set up Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = "us-central1"  # 替换为您的首选位置

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Define video analysis function
def analyze_video(video_path):
    # 使用 GenerativeModel 来分析视频
    model = GenerativeModel("gemini-1.5-flash-002")
    
    # 读取视频文件
    with open(video_path, "rb") as f:
        video_content = f.read()
    
    # 创建 Part 对象
    video_part = Part.from_data(video_content, mime_type="video/mp4")
    
    # 生成内容
    response = model.generate_content(
        [
            "Analyze this video clip for team dynamics, leadership skills, and activity purpose.",
            video_part
        ]
    )
    return response.text

# Read existing .md analysis file
# 讀取現有的 .md 分析文件
def read_md_analysis(md_file_path, segment):
    # Read the markdown file
    # 讀取 markdown 文件
    with open(md_file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    
    # Convert Markdown to HTML
    # 將 Markdown 轉換為 HTML
    html = markdown.markdown(md_content)
    
    # Extract the content of the specific segment
    # 提取特定段落的內容
    segment_pattern = re.compile(f'<h2>{segment}</h2>(.*?)(<h2>|$)', re.DOTALL)
    segment_match = segment_pattern.search(html)
    
    if segment_match:
        return segment_match.group(1).strip()
    else:
        return f"No {segment} found."

# Main function
# 主函數
def main():
    # Define paths for video files and corresponding md files
    # 定義視頻文件和相應 md 文件的路徑
    video_paths = ["video_output_without_audio.mp4"
       # "video_segment_analysis_1.mp4",
        #"video_segment_analysis_2.mp4",
       # "video_segment_analysis_3.mp4",
        #"video_segment_analysis_4.mp4",
       # "video_segment_analysis_5.mp4"
    ]
    
    md_file_paths = [
      #  "video_segment_analysis.md"
      "Group Dynamics Assessment Scale.md"
    ]
    
    # Initialize the output Markdown content
    output_md = "# Video Analysis Comparisons\n\n"
    
    # Iterate through each video and its corresponding md file
    # 遍歷每個視頻及其對應的 md 文件
    for i, video_path in enumerate(video_paths, start=1):
        print(f"Analyzing video: {video_path}")
        
        # Analyze video using Gemini 1.5 Pro Vision
        # 使用 Gemini 1.5 Pro Vision 分析視頻
        ai_analysis = analyze_video(video_path)
        
        # Read existing .md analysis for the specific segment
        # 讀取特定段落的現有 .md 分析
        human_analysis = read_md_analysis(md_file_paths[0], f"Segment {i}")
        
        # Add comparison result to the output Markdown content
        output_md += f"""
## Video Analysis Comparison: {video_path}

### AI Analysis
{ai_analysis}

### Human Analysis
{human_analysis}

### Comparison
Please manually compare the AI and human analyses for accuracy, depth, and insights.

---

"""
        
        print(f"Completed analysis for {video_path}")
        print("="*50 + "\n")

    # Save all comparisons to a single Markdown file
    output_file = "TEST_video_analysis_comparisons.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_md)
    
    print(f"All comparisons saved to {output_file}")

if __name__ == "__main__":
    main()
