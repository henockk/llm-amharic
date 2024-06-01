import os
import sentencepiece as spm
from utils.fetch_data_from_db import fetch_data_from_database

def save_articles_to_file(articles, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for article in articles:
            f.write(article + '\n')

def train_sentencepiece_model(input_file, model_prefix='amharic', vocab_size=32000):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    
    if os.path.getsize(input_file) == 0:
        raise ValueError(f"The file {input_file} is empty.")
    
    # Optional: Print the first few lines to check the file content
    with open(input_file, 'r', encoding='utf-8') as f:
        for _ in range(5):
            print(f.readline().strip())
    
    spm.SentencePieceTrainer.train(input=input_file, model_prefix=model_prefix, vocab_size=vocab_size)

if __name__ == "__main__":
    articles = fetch_data_from_database()
    input_file = 'data/amharic_corpus.txt'
    save_articles_to_file(articles, input_file)
    train_sentencepiece_model(input_file)
