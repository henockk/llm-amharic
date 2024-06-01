from transformers import Trainer
from datasets import Dataset

def evaluate_model():
    dataset = Dataset.load_from_disk('data/tokenized_dataset')

    trainer = Trainer(
        model_init=lambda: LlamaForCausalLM.from_pretrained('./models/fine_tuned_model'),
        args=TrainingArguments(
            per_device_eval_batch_size=4,
        ),
        eval_dataset=dataset,
    )

    results = trainer.evaluate()
    print(f"Evaluation results: {results}")

if __name__ == "__main__":
    evaluate_model()
