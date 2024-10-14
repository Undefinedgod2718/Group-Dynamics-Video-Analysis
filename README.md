# 影片分析流程
##判斷素材
* introduction.wmv (分析用之團動影片)
* 【Group Dynamics Assessment Scale.txt】團體動力學評質表

##應用AI
* OepenAI
* ANTHROPIC
* Google

## 原始影片
using :VideoFileClip.py 
e.g., introduction.wmv
輸入：導入影片作為原始數據，並將其分成 純畫面 與 純音頻。
ex :video_output_without_audio.mp4 and audio_output.mp3
↓

## 音頻轉錄為文字
using :ToSrt.py
步驟：使用 Whisper API 將影片中的音頻轉換為字幕文本。
輸出：生成對話片段的逐字稿或字幕，並將每個片段作為分析單位。
e.g., subtitle_output.srt
↓
## 初步分析（Summary）
using : analyze_group_activity.py
步驟:使用claude api 將文本進行初步摘要
輸出:輸出Summary，以便最後總結
e.g., group_activity_analysis.md
↓

## 語義分析（Semantic Analysis）
using : semantic_analysis.py
步驟：使用 OpenAI Embeddings API 將每個對話片段轉換成嵌入向量，捕捉其語義內容。
輸出：儲存每個片段的嵌入向量，以便進行後續的相似度比較或語境理解。
e.g., semantic_analysis.json, semantic_analysis.pkl
↓

## 情感分析（Sentiment Analysis）
using : sentiment_analysis.py, sentiment_analysis_summary.py, sentiment_visualization.py
步驟：使用 Hugging Face 模型（例如 Erlangshen-Roberta-330M-Sentiment）對每個對話片段進行情感分析。
輸出：儲存每個片段的情感評分（正面、負面或中立）及情感強度（高或低）。
e.g., sentiment_analysis.json, sentiment_analysis_summary.csv, sentiment_distribution.png, sentiment_intensity_heatmap.png
↓

## 主題提取（Topic Extraction）
using : topic_extraction.py, all_topics_count.py
步驟：使用 Claude API 對每個片段進行主題提取，生成關鍵主題或摘要。
輸出：將每個片段的關鍵主題或摘要存儲，方便後續篩選。
e.g., topic_extraction_results.json, all_topics_count.csv
↓

## 加權及篩選機制
using : weighted_filtering.py
步驟：
* 語義匹配度：比較片段的嵌入向量與影片核心主題向量的相似度。(尚未找到方法)
情感強度：根據片段情感波動的高低進行篩選。
主題相關性：檢查片段與重要主題的匹配度。
輸出：設定權重與閾值，篩選出符合條件的關鍵片段。
* 尚且未完成
↓

## 關鍵對話片段的提取
using : analyze_video_segments.py(片段提取), Srt_Video_Clipping.py(影片預處理)
步驟：根據加權篩選結果，提取出符合條件的關鍵對話片段。
輸出：將關鍵對話片段的資訊裁切提取並保存，為後續影片畫面分析做準備。
e.g., video_segment_analysis.srt(影片預處理根據), video_segment_analysis.md(片段提取), video_segment_analysis_1.mp4(影片產出), video_segment_analysis_2.mp4(影片產出), video_segment_analysis_3.mp4(影片產出), video_segment_analysis_4.mp4(影片產出), video_segment_analysis_5.mp4(影片產出)
↓

## 影片畫面分析（Gemini 1.5 Pro video-understanding）
using : video_analysis_comparison.py
步驟：對提取的關鍵片段對應的影片畫面進行分析，如情感波動的可視化，或對應主題畫面的檢測。
輸出：生成影片畫面與對話主題、情感分析的可視化數據。
e.g., video_analysis_comparisons.md
↓

## 數據整合（Claude 綜合分析）
using : 
e.g., sentiment_distribution.png(SmartArt), sentiment_intensity_heatmap.png(SmartArt), topic_count_distribution.png(SmartArt), video_analysis_comparisons.md(證據參考), group_activity_analysis.md(證據參考), Group Dynamics Assessment Scale.txt(依據總結)
步驟：將所有步驟中的語義、情感、主題分析結果與影片畫面分析整合，進行綜合分析。
輸出：綜合情感趨勢、互動模式和影片畫面分析的數據集。
e.g., 
↓

[輸出報告 - 情感趨勢、互動分析、可視化]

步驟：
基於整合的數據生成最終報告，包括情感趨勢、角色互動分析，以及可視化的圖像或圖表。
輸出：最終的報告文件，包含關鍵片段的情感分析、主題提取以及對應畫面的可視化展示。