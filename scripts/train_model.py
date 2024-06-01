import os
from transformers import LlamaForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling

def train_model():
    dataset = Dataset.load_from_disk('data/tokenized_dataset')
    
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat")
    model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat")

    training_args = TrainingArguments(
        output_dir='./models/fine_tuned_model',
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='./logs',
        logging_steps=200,
        evaluation_strategy="steps",
        eval_steps=500,
        learning_rate=2e-5,
        weight_decay=0.01,
        warmup_steps=500,
        load_best_model_at_end=True,
        metric_for_best_model="loss",
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model('./models/fine_tuned_model')
    tokenizer.save_pretrained('./models/fine_tuned_model')

if __name__ == "__main__":
    train_model()
