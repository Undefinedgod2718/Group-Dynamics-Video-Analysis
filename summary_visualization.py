# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontManager
from matplotlib.font_manager import FontProperties

# Read data
# 讀取數據
sentiment_df = pd.read_csv('sentiment_analysis_summary.csv', encoding='utf-8')
topics_df = pd.read_csv('all_topics_count.csv', encoding='utf-8')

# Set Chinese font (if needed for displaying Chinese characters)
# 設置中文字體（如果需要顯示中文）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

font_manager = FontManager()
font_names = [f.name for f in font_manager.ttflist]
print(font_names)

# 1. Sentiment distribution bar chart
# 1. 情感分佈柱狀圖
plt.figure(figsize=(10, 6))
sentiment_counts = [
    sentiment_df.loc[sentiment_df['Metric'] == 'Positive count', 'Value'].iloc[0],
    sentiment_df.loc[sentiment_df['Metric'] == 'Negative count', 'Value'].iloc[0],
    sentiment_df.loc[sentiment_df['Metric'] == 'Neutral count', 'Value'].iloc[0]
]
plt.bar(['Positive', 'Negative', 'Neutral'], sentiment_counts)
plt.title('Distribution of Sentiment in Dialogue Segments\nEmotional distribution of dialogue segments') #對話片段情感分佈
plt.ylabel('Count\n數量')
plt.savefig('sentiment_distribution.png')
plt.close()

# 2. Sentiment intensity heatmap
# 2. 情感強度熱力圖
plt.figure(figsize=(12, 8))
heatmap_data = sentiment_df[sentiment_df['Metric'].str.startswith('Sentiment_')].set_index('Metric')['Value'].to_frame().T
sns.heatmap(heatmap_data, annot=False, cmap='YlOrRd')
plt.title('Sentiment Intensity Distribution Heatmap\nEmotion intensity distribution') #情感強度分佈熱力圖
plt.savefig('sentiment_intensity_heatmap.png')
plt.close()

# 3. Topic count bar chart
# 3. 主題計數柱狀圖
plt.figure(figsize=(15, 10))
topics_df_filtered = topics_df[topics_df['Topic'] != '未能提取主題'].sort_values('Count', ascending=False).head(20)
chinese_font = FontProperties(fname='C:\Windows\Fonts/kaiu.ttf', size=10)
plt.bar(topics_df_filtered['Topic'], topics_df_filtered['Count'])
plt.title('前20個主題計數', fontproperties=chinese_font)
plt.xlabel('主題', fontproperties=chinese_font)
plt.ylabel('計數', fontproperties=chinese_font)
plt.xticks(rotation=90, fontproperties=chinese_font)
plt.tight_layout()
plt.savefig('topic_count_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("Visualization charts have been saved as sentiment_distribution.png, sentiment_intensity_heatmap.png, and topic_count_distribution.png")
print("可視化圖表已保存為 sentiment_distribution.png、sentiment_intensity_heatmap.png 和 topic_count_distribution.png")
