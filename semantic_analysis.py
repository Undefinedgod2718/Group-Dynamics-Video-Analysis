import json
import pickle
import os
from dotenv import load_dotenv
import openai
from tqdm import tqdm
from openai import OpenAIError

# Load environment variables
# 載入環境變數
load_dotenv()

# Set OpenAI API key
# 設置 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

# Read subtitle file
# 讀取字幕檔案
def read_subtitle_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content.split('\n\n')

# Extract dialogue content
# 提取對話內容
def extract_dialogue(subtitle_blocks):
    dialogues = []
    for block in subtitle_blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            dialogue = ' '.join(lines[2:])
            dialogues.append(dialogue)
    return dialogues

# Generate embeddings for a batch of texts
# 為一批文本生成嵌入向量
def get_embeddings_batch(texts, model="text-embedding-3-large"):
    try:
        response = openai.embeddings.create(
            model=model,
            input=texts
        )
        return [item.embedding for item in response.data]
    except OpenAIError as e:
        print(f"An error occurred: {e}")
        # Return a list of None values with the same length as the input texts
        # 返回一個與輸入文本長度相同的 None 值列表
        return [None] * len(texts)

# Save results to JSON and pickle files
# 將結果保存為 JSON 和 pickle 檔案
def save_results(dialogues, embeddings):
    # Save as JSON
    # 保存為 JSON
    result_json = [{"dialogue": d, "embedding": e} for d, e in zip(dialogues, embeddings)]
    with open('semantic_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    
    # Save as pickle
    # 保存為 pickle
    with open('semantic_analysis_results.pkl', 'wb') as f:
        pickle.dump({"dialogues": dialogues, "embeddings": embeddings}, f)

# Main function
# 主函數
def main():
    subtitle_file = 'subtitle_output.srt'
    subtitle_blocks = read_subtitle_file(subtitle_file)
    dialogues = extract_dialogue(subtitle_blocks)
    
    # Process embeddings in batches
    # 批次處理嵌入向量
    batch_size = 100
    all_embeddings = []
    for i in tqdm(range(0, len(dialogues), batch_size), desc="Processing batches"):
        batch = dialogues[i:i+batch_size]
        batch_embeddings = get_embeddings_batch(batch)
        all_embeddings.extend(batch_embeddings)
    
    save_results(dialogues, all_embeddings)
    print("语义分析完成,结果已保存。")

if __name__ == "__main__":
    main()

# 示例用法
#embeddings = get_embeddings_batch(["This is sentence 1", "This is sentence 2"])
