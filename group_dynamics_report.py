import os
from dotenv import load_dotenv
import anthropic
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
import re
import markdown2
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Initialize the Claude API client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

client = anthropic.Anthropic(api_key=anthropic_api_key)

# Function to read text files using Claude API
def read_file_with_claude(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # If UTF-8 fails, try with cp950
        with open(file_path, 'r', encoding='cp950') as file:
            content = file.read()
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        system="你是一位優秀的團隊領導力培訓師。從這個角度分析以下內容，提供見解並引用相關部分, 回應只能用ZH_TW與English。",
        messages=[
            {"role": "user", "content": f"請分析以下內容：\n\n{content}"}
        ]
    )
    return response.content[0].text if response.content else ""

# Function to analyze images using Claude API
def analyze_image_with_claude(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        system="你是一位優秀的團隊領導力培訓師。從這個角度分析以下圖像，提供見解並引用圖像中的具體元素, 回應只能用ZH_TW與English。",
        messages=[
            {
                "role": "user", 
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64.b64encode(image_data).decode()
                        }
                    },
                    {
                        "type": "text",
                        "text": "請從團隊領導力的角度分析這張圖像並提供見解。"
                    }
                ]
            }
        ]
    )
    return response.content[0].text if response.content else ""

# Function to save response as Markdown
def save_response_as_markdown(response, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        if isinstance(response, list):
            for item in response:
                if isinstance(item, dict) and 'text' in item:
                    f.write(item['text'])
                elif isinstance(item, str):
                    f.write(item)
        elif isinstance(response, dict) and 'text' in response:
            f.write(response['text'])
        elif isinstance(response, str):
            f.write(response)
        else:
            f.write(str(response))

# Read and analyze text files
video_analysis = read_file_with_claude('video_analysis_comparisons.md')
group_activity = read_file_with_claude('group_activity_analysis.md')

# Analyze images
sentiment_distribution = analyze_image_with_claude('sentiment_distribution.png')
sentiment_heatmap = analyze_image_with_claude('sentiment_intensity_heatmap.png')

# Save responses as Markdown files
save_response_as_markdown(video_analysis, 'video_analysis_response.md')
save_response_as_markdown(group_activity, 'group_activity_response.md')
save_response_as_markdown(sentiment_distribution, 'sentiment_distribution_response.md')
save_response_as_markdown(sentiment_heatmap, 'sentiment_heatmap_response.md')
print("Analysis complete. Responses saved as Markdown files.")