import json
from collections import Counter
import csv

# Read the JSON file
with open('topic_extraction_results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract all topics and count them
all_topics = [topic for item in data for topic in item.get('topics', [])]
topic_counts = Counter(all_topics)

# Convert the Counter object to a list of tuples
all_topic_counts = list(topic_counts.items())

# Sort the topics by count in descending order
all_topic_counts.sort(key=lambda x: x[1], reverse=True)

# Save all results to a CSV file
with open('all_topics_count.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Topic', 'Count'])  # Write header
    writer.writerows(all_topic_counts)  # Write all data

print("All topics and their counts have been saved to 'all_topics_count.csv'")
