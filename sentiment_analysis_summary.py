import json
import pandas as pd
import numpy as np
from textblob import TextBlob

# Function to analyze sentiment of a given text
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def main():
    # Read the JSON file containing sentiment analysis results
    with open('subtitle_sentiment_analysis_results.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    print("Type of data loaded from JSON:")
    print(type(data))
    
    if not isinstance(data, list):
        print("Error: Data is not a list as expected.")
        return
    
    # Extract sentiment scores (assuming second value is positive sentiment)
    sentiment_scores = [item['sentiment'][1] for item in data if 'sentiment' in item]
    
    if not sentiment_scores:
        print("Error: No sentiment scores found in the data.")
        return
    
    # Convert sentiment scores to a pandas Series for easier analysis
    sentiment_series = pd.Series(sentiment_scores)
    
    # Calculate probabilities for positive and negative sentiments
    total_comments = len(sentiment_series)
    positive_comments = len(sentiment_series[sentiment_series > 0.5])
    negative_comments = len(sentiment_series[sentiment_series < 0.5])
    neutral_comments = total_comments - positive_comments - negative_comments
    
    positive_prob = positive_comments / total_comments
    negative_prob = negative_comments / total_comments
    neutral_prob = neutral_comments / total_comments
    
    # Print statistical results
    print(f"\nTotal comments: {total_comments}")
    print(f"Probability of positive sentiment: {positive_prob:.2%}")
    print(f"Probability of negative sentiment: {negative_prob:.2%}")
    print(f"Probability of neutral sentiment: {neutral_prob:.2%}")
    
    # Calculate overall statistical description
    sentiment_stats = sentiment_series.describe()
    print("\nStatistical description of sentiment scores:")
    print(sentiment_stats)
    
    # Create a dictionary to store the results
    results = {
        'Metric': ['Positive probability', 'Negative probability', 'Neutral probability',
                   'Positive count', 'Negative count', 'Neutral count'],
        'Value': [positive_prob, negative_prob, neutral_prob,
                  positive_comments, negative_comments, neutral_comments]
    }
    
    # Create a DataFrame from the results dictionary
    results_df = pd.DataFrame(results)
    
    # Concatenate the results DataFrame with the sentiment stats
    sentiment_stats_df = sentiment_stats.reset_index().rename(columns={'index': 'Metric', 0: 'Value'})
    final_results = pd.concat([results_df, sentiment_stats_df], ignore_index=True)
    
    # Add all sentiment scores to the final results
    sentiment_df = pd.DataFrame({'Metric': ['Sentiment_' + str(i) for i in range(len(sentiment_scores))],
                                 'Value': sentiment_scores})
    final_results = pd.concat([final_results, sentiment_df], ignore_index=True)
    
    # Save the final results to a CSV file
    final_results.to_csv('sentiment_analysis_summary.csv', index=False)
    print("\nResults have been saved to 'sentiment_analysis_summary.csv'")

if __name__ == "__main__":
    main()
