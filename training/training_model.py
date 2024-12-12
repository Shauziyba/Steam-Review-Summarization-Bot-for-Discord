import torch
from datasets import load_dataset
import os
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments

# Check if a GPU is available, otherwise use CPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load Pegasus tokenizer and model
model_name = "google/pegasus-large"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

# Load dataset (replace with your actual dataset path)
dataset = load_dataset('csv', data_files=r'C:\Users\Pegasus\Documents\Pegasus_steam_SUM\Dataset\cleaned_train_data.csv')

# Preprocess the dataset
def preprocess_function(examples):
    inputs = examples['preprocessed_paragraphs_per_reviews']  # Input reviews
    targets = examples['preprocessed_summary']  # Target summaries

    # Tokenize inputs
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True, padding="max_length", return_tensors="pt")

    # Tokenize targets separately
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=150, truncation=True, padding="max_length", return_tensors="pt")

    # Add labels to inputs
    model_inputs["labels"] = labels["input_ids"]

    return model_inputs

# Split the dataset into training and validation sets (80% train, 20% validation)
train_test_split = dataset['train'].train_test_split(test_size=0.2)
tokenized_datasets = train_test_split.map(preprocess_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="steps",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    learning_rate=2e-5,
    num_train_epochs=8,
    weight_decay=0.01,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
    load_best_model_at_end=True,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],  # Use the validation dataset created
    tokenizer=tokenizer,
)

# Train the model
trainer.train()

# Save the model and tokenizer
model_save_path = "./fine_tuned_pegasus_model_test"
os.makedirs(model_save_path, exist_ok=True)
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)
