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

# Read the content of the files
subtitle_content = read_file('subtitle_output.srt')
assessment_scale = read_file('Group Dynamics Assessment Scale.txt')

# Construct the prompt
prompt = f"""
You are an excellent group leadership trainer. Please analyze the following subtitle content and provide:
1. Theme
2. Content summary (including theme and activity description)
3. Main dialogues
4. Overall emotional tone

Then, based on the Group Dynamics Assessment Scale, evaluate the leader and provide overall suggestions.

Subtitle content:
{subtitle_content}

Group Dynamics Assessment Scale:
{assessment_scale}

Please provide your analysis and evaluation in traditional chinese, and format your response using Markdown syntax.
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
    with open('group_activity_analysis.md', 'w', encoding='utf-8') as f:
        f.write(analysis)
    
    print("Analysis saved to group_activity_analysis.md")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
