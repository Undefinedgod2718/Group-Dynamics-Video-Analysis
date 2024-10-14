import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load previous analysis results
# 加載之前的分析結果
with open('semantic_analysis_results.json', 'r', encoding='utf-8') as f:
    semantic_data = json.load(f)

with open('sentiment_analysis_results.json', 'r', encoding='utf-8') as f:
    sentiment_data = json.load(f)

with open('topic_extraction_results.json', 'r', encoding='utf-8') as f:
    topic_data = json.load(f)

# Print the first few entries to check the structure
# 打印前幾個條目以檢查結構
print("Sample of topic data:")
print(json.dumps(topic_data[:3], ensure_ascii=False, indent=2))
print("\nSample of sentiment data:")
print(json.dumps(sentiment_data[:3], ensure_ascii=False, indent=2))

# Define weights
# 定義權重
SEMANTIC_WEIGHT = 0.3
SENTIMENT_WEIGHT = 0.3
TOPIC_WEIGHT = 0.4

# Calculate semantic similarity
# 計算語義相似度
def calculate_semantic_score(embeddings):
    similarity_matrix = cosine_similarity(embeddings)
    return np.mean(similarity_matrix, axis=1)

# Calculate sentiment intensity
# 計算情感強度
def calculate_sentiment_score(sentiments):
    def get_sentiment_intensity(sentiment):
        if isinstance(sentiment, dict):
            # Assume dictionary format is {'positive': x, 'neutral': y, 'negative': z}
            # 假設字典格式為 {'positive': x, 'neutral': y, 'negative': z}
            return max(abs(sentiment.get('positive', 0) - 0.5),
                       abs(sentiment.get('neutral', 0) - 0.5),
                       abs(sentiment.get('negative', 0) - 0.5))
        elif isinstance(sentiment, list):
            # Assume list format is [positive, neutral, negative]
            # 假設列表格式為 [positive, neutral, negative]
            return max(abs(s - 0.5) for s in sentiment)
        else:
            # If it's a single value, assume it represents overall sentiment intensity
            # 如果是單一數值，假設它代表整體情感強度
            return abs(sentiment - 0.5)

    return [get_sentiment_intensity(s) for s in sentiments]

# Calculate topic importance
# 計算主題重要性
def calculate_topic_score(topics):
    # Assume the importance of topics is predefined
    # 假設主題的重要性是預先定義的
    topic_importance = {
        "活動": 1.0,
        "記憶": 0.9,
        "食物": 0.8,
        "家庭": 0.7,
        "合作": 0.6
    }
    
    def get_topic_score(topic):
        if not topic:  # If topic is empty (None, empty string, or empty list)
                       # 如果主題為空（None、空字符串或空列表）
            return 0   # Return default score
                       # 返回默認分數
        if isinstance(topic, list):
            scores = [topic_importance.get(t, 0) for t in topic if t]
        else:
            scores = [topic_importance.get(topic, 0)]
        return max(scores) if scores else 0

    return [get_topic_score(topic) for topic in topics]

# Integrate scores
# 整合分數
def integrate_scores(semantic_scores, sentiment_scores, topic_scores):
    return [
        SEMANTIC_WEIGHT * s + SENTIMENT_WEIGHT * e + TOPIC_WEIGHT * t
        for s, e, t in zip(semantic_scores, sentiment_scores, topic_scores)
    ]

# Main function
# 主函數
def extract_key_dialogues(threshold=0.7):
    embeddings = [d['embedding'] for d in semantic_data]
    sentiments = [d['sentiment'] for d in sentiment_data]
    topics = [d['topics'] for d in topic_data]
    dialogues = [d['dialogue'] for d in semantic_data]

    print(f"\nNumber of dialogues: {len(dialogues)}")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Number of sentiments: {len(sentiments)}")
    print(f"Number of topics: {len(topics)}")

    print("\nSample of topics data:")
    print(json.dumps(topics[:5], ensure_ascii=False, indent=2))

    semantic_scores = calculate_semantic_score(embeddings)
    sentiment_scores = calculate_sentiment_score(sentiments)
    topic_scores = calculate_topic_score(topics)

    print(f"\nSample of semantic scores: {semantic_scores[:5]}")
    print(f"Sample of sentiment scores: {sentiment_scores[:5]}")
    print(f"Sample of topic scores: {topic_scores[:5]}")

    integrated_scores = integrate_scores(semantic_scores, sentiment_scores, topic_scores)

    print(f"\nSample of integrated scores: {integrated_scores[:5]}")
    print(f"Max integrated score: {max(integrated_scores)}")
    print(f"Min integrated score: {min(integrated_scores)}")

    # Select key dialogue segments
    key_dialogues = [
        {"dialogue": d, "score": s}
        for d, s in zip(dialogues, integrated_scores)
        if s >= threshold
    ]

    # Sort by score
    key_dialogues.sort(key=lambda x: x['score'], reverse=True)

    return key_dialogues

# Run extraction process and save results
key_dialogues = extract_key_dialogues(threshold=0.5)  # Lower the threshold to 0.5

with open('key_dialogues.json', 'w', encoding='utf-8') as f:
    json.dump(key_dialogues, f, ensure_ascii=False, indent=2)

print(f"\n{len(key_dialogues)} key dialogue segments extracted and saved to key_dialogues.json")
print(f"已提取 {len(key_dialogues)} 個關鍵對話片段並保存到 key_dialogues.json")

# Print top 5 key dialogues if any
if key_dialogues:
    print("\nTop 5 key dialogues:")
    for i, kd in enumerate(key_dialogues[:5], 1):
        print(f"{i}. Score: {kd['score']:.4f}")
        print(f"   Dialogue: {kd['dialogue'][:100]}...")  # Print first 100 characters
else:
    print("\nNo key dialogues found. Please check the threshold and scoring mechanism.")
