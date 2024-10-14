import os
from dotenv import load_dotenv
import anthropic
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
import re
import markdown2
from bs4 import BeautifulSoup
import json
import numpy as np
from sklearn.manifold import TSNE
from matplotlib.font_manager import FontProperties

# Load environment variables from .env file
load_dotenv()

# Initialize the Claude API client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in .env file")

client = anthropic.Anthropic(api_key=anthropic_api_key)

# Load the JSON data
with open('semantic_analysis_results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract embeddings and dialogues
embeddings = [item['embedding'] for item in data]
dialogues = [item['dialogue'] for item in data]

# Convert embeddings to numpy array
embeddings_array = np.array(embeddings)

# Apply t-SNE for dimensionality reduction
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings_array)

# Load Chinese font
chinese_font = FontProperties(fname='C:\Windows\Fonts/kaiu.ttf', size=10)

# Create a scatter plot
plt.figure(figsize=(12, 8))
scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], alpha=0.6)

# Add labels for some points (e.g., every 10th point)
for i, dialogue in enumerate(dialogues[::10]):
    plt.annotate(dialogue, (embeddings_2d[i*10, 0], embeddings_2d[i*10, 1]), fontsize=8, fontproperties=chinese_font)

plt.title('Dialogue Embeddings 2D Visualization', fontproperties=chinese_font)
plt.xlabel('t-SNE feature 1', fontproperties=chinese_font)
plt.ylabel('t-SNE feature 2', fontproperties=chinese_font)

# Add a colorbar to show density
plt.colorbar(scatter)

# Show the plot
plt.tight_layout()
plt.show()
