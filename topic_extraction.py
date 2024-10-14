import json
import pickle
import os
from dotenv import load_dotenv
import anthropic
from tqdm import tqdm
from anthropic import Anthropic

# Load environment variables
# 加載環境變量
load_dotenv()

# Set up Anthropic API key
# 設置Anthropic API密鑰
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Load previously generated semantic analysis results
# 加載之前生成的語義分析結果
with open('semantic_analysis_results.pkl', 'rb') as f:
    data = pickle.load(f)
dialogues = data['dialogues']

def extract_topics(dialogue):
    # Construct messages for Claude API
    # 構建用於 Claude API 的消息
    messages = [
        {
            "role": "user",
            "content": f"""請為以下對話片段生成一個簡短的摘要（不超過20個字），並提取3個關鍵主題詞。

對話內容：
{dialogue}

請按以下格式輸出：
摘要：[摘要內容]
關鍵主題：[主題1], [主題2], [主題3]"""
        }
    ]

    # Call Claude API to get the response
    # 調用 Claude API 獲取回應
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        messages=messages
    )

    # Extract summary and topics from the response
    # 從回應中提取摘要和主題
    response_text = response.content[0].text.strip()
    
    # Initialize summary and topics
    # 初始化摘要和主題
    summary = ""
    topics = []

    # Try to parse the response
    # 嘗試解析回應
    try:
        lines = response_text.split('\n')
        for line in lines:
            if line.startswith('摘要：'):
                summary = line.replace('摘要：', '').strip()
            elif line.startswith('關鍵主題：'):
                topics = line.replace('關鍵主題：', '').strip().split(', ')
                break  # Exit loop after finding topics
                       # 找到主題後退出循環
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response_text}")

    # If no summary or topics found, use the entire response as summary
    # 如果沒有找到摘要或主題，使用整個回應作為摘要
    if not summary and not topics:
        summary = response_text[:20]  # Limit to 20 characters
                                      # 限制為20個字符
        topics = ["未能提取主題"]

    return {
        'summary': summary,
        'topics': topics
    }

# Process all dialogues and store results
# 處理所有對話並存儲結果
results = []
for dialogue in tqdm(dialogues, desc="Extracting topics"):
    try:
        result = extract_topics(dialogue)
        results.append(result)
    except Exception as e:
        print(f"Error processing dialogue: {e}")
        continue  # Skip this dialogue and continue with the next one
                  # 跳過這個對話，繼續處理下一個

# Save results to JSON file
# 將結果保存到JSON文件
with open('topic_extraction_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Topic extraction completed. Results saved to topic_extraction_results.json")
