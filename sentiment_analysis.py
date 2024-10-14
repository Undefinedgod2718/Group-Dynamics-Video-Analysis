import json
import pickle
from transformers import BertForSequenceClassification, BertTokenizer
import torch
from tqdm import tqdm

# 加载模型和tokenizer
model_name = 'IDEA-CCNL/Erlangshen-MegatronBert-1.3B-Sentiment'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# 设置设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# 读取字幕文件
def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    dialogues = []
    for block in content.strip().split('\n\n'):
        lines = block.split('\n')
        if len(lines) >= 3:
            dialogue = ' '.join(lines[2:])
            dialogues.append(dialogue)
    
    return dialogues

# 加载字幕文件
dialogues = read_srt('subtitle_output.srt')

# 进行情感分析
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probabilities.cpu().numpy()[0]

# 对每个对话片段进行情感分析
sentiments = []
for dialogue in tqdm(dialogues, desc="Analyzing sentiments"):
    sentiment = analyze_sentiment(dialogue)
    sentiments.append(sentiment.tolist())

# 保存结果
results = [
    {"dialogue": d, "sentiment": s}
    for d, s in zip(dialogues, sentiments)
]

# 保存为JSON
with open('subtitle_sentiment_analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 保存为pickle
with open('subtitle_sentiment_analysis_results.pkl', 'wb') as f:
    pickle.dump({"dialogues": dialogues, "sentiments": sentiments}, f)

print("字幕情感分析完成,结果已保存。")
