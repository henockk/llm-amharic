import sentencepiece as spm

def train_sentencepiece_model(input_file, model_prefix='amharic', vocab_size=32000):
    spm.SentencePieceTrainer.train(input=input_file, model_prefix=model_prefix, vocab_size=vocab_size)

if __name__ == "__main__":
    train_sentencepiece_model('data/amharic_corpus.txt')
