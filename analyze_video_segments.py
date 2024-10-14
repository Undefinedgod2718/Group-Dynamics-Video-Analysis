import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from .env file
load_dotenv()

# Load the API key from the environment variable
api_key = os.getenv("ANTHROPIC_API_KEY")

# Check if the API key is available
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

# API endpoint
url = "https://api.anthropic.com/v1/messages"

# Headers for the API request
headers = {
    "Content-Type": "application/json",
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01"
}

# Function to read the content of a file
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Read the subtitle content
subtitle_content = read_file('subtitle_output.srt')

# Construct the prompt
prompt = f"""
You are an excellent group leadership trainer. Based on the following subtitle content, please select 5 key segments for video analysis. For each segment:

1. Keep the original timestamp
2. Keep the corresponding dialogue
3. Add a brief explanation of why this segment is important for analysis

Consider aspects such as the leader's guidance style, member interactions, overall atmosphere, and key activity phases.

Format your response as a Markdown file, where each segment follows this structure:

## Segment [Number]

**Timestamp:** [Original Timestamp]
**Dialogue:** [Original Dialogue]

**Analysis:**
[Your explanation in traditional chinese]

Subtitle content:
{subtitle_content}

Please provide your analysis in traditional chinese, formatted as described above.
"""

# Prepare the request payload
payload = {
    "model": "claude-3-sonnet-20240229",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 2000
}

# Send the request to the Claude API
response = requests.post(url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    result = response.json()
    
    # Extract the analysis
    analysis = result['content'][0]['text']
    
    # Save the analysis to a Markdown file
    with open('video_segment_analysis.md', 'w', encoding='utf-8') as f:
        f.write(analysis)
    
    print("Analysis saved to video_segment_analysis.md")

    # Extract timestamps and dialogues for .srt file
    import re
    srt_content = ""
    segments = re.findall(r'\*\*Timestamp:\*\* (.*?)\n\*\*Dialogue:\*\* (.*?)\n', analysis, re.DOTALL)
    for i, (timestamp, dialogue) in enumerate(segments, 1):
        srt_content += f"{i}\n{timestamp.strip()}\n{dialogue.strip()}\n\n"

    # Save the .srt file
    with open('video_segment_analysis.srt', 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    print("Timestamps and dialogues saved to video_segment_analysis.srt")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
