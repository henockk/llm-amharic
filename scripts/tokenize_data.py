import sentencepiece as spm
from datasets import Dataset

def tokenize_text(input_file, model_file='amharic.model'):
    sp = spm.SentencePieceProcessor(model_file=model_file)
    with open(input_file, 'r', encoding='utf-8') as f:
        texts = f.readlines()
    tokenized_texts = [sp.encode(text.strip(), out_type=int) for text in texts]
    return Dataset.from_dict({'text': tokenized_texts})

if __name__ == "__main__":
    dataset = tokenize_text('data/amharic_corpus.txt')
    dataset.save_to_disk('data/tokenized_dataset')
