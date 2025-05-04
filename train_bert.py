import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import logging # Optional: Track Hugging Face logs

# --- Configuration ---
CSV_FILE_PATH = 'hate_speech_data.csv' # <<< Your final CSV dataset path
TEXT_COLUMN = 'Komentar'             # <<< Exact name of your text column
LABEL_COLUMN = 'Ocena' # <<< Exact name of your 0/1 label column

# Model & Tokenizer Choice
# Common choices:
# - 'bert-base-uncased': Good general English model (ignores case)
# - 'bert-base-multilingual-uncased': Good if your text might contain multiple languages (like Serbian)
# - 'distilbert-base-uncased': Faster, slightly smaller version of BERT
MODEL_NAME = 'classla/bcms-bertic' # <<< USE THIS IDENTIFIER FOR BERTić

# Training Hyperparameters (can keep the same or adjust slightly)
MAX_LENGTH = 128
BATCH_SIZE = 16
EPOCHS = 3
LEARNING_RATE = 5e-5
# Set logging level for transformers (optional)
# logging.getLogger("transformers").setLevel(logging.ERROR)

# --- 1. Load Data ---
try:
    df = pd.read_csv(CSV_FILE_PATH)
    print(f"Data loaded successfully from '{CSV_FILE_PATH}'. Shape: {df.shape}")
    print("Columns:", df.columns.tolist())
    if TEXT_COLUMN not in df.columns or LABEL_COLUMN not in df.columns:
        raise ValueError(f"Expected columns '{TEXT_COLUMN}' and '{LABEL_COLUMN}' not found.")
except FileNotFoundError:
    print(f"Error: File not found at {CSV_FILE_PATH}")
    exit()
except Exception as e:
    print(f"Error loading CSV file: {e}")
    exit()

# --- 2. Preprocess and Prepare Data ---
print("\n--- Preprocessing Data ---")
df.dropna(subset=[TEXT_COLUMN, LABEL_COLUMN], inplace=True)
df[TEXT_COLUMN] = df[TEXT_COLUMN].astype(str)
try:
    df[LABEL_COLUMN] = df[LABEL_COLUMN].astype(int)
    unique_labels = df[LABEL_COLUMN].unique()
    if not all(label in [0, 1] for label in unique_labels):
         print(f"Warning: Labels in '{LABEL_COLUMN}' are not strictly 0 or 1. Found: {unique_labels}.")
except ValueError as e:
    print(f"Error: Could not convert '{LABEL_COLUMN}' to integer. Error: {e}")
    exit()

print("\nLabel Distribution:")
print(df[LABEL_COLUMN].value_counts(normalize=True))

texts = df[TEXT_COLUMN].tolist()
labels = df[LABEL_COLUMN].tolist()

# --- 3. Split Data ---
print("\n--- Splitting Data ---")
X_train_texts, X_val_texts, y_train, y_val = train_test_split(
    texts, labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)
print(f"Training samples: {len(X_train_texts)}, Validation samples: {len(X_val_texts)}")

# --- 4. Tokenization ---
print(f"\n--- Loading Tokenizer: {MODEL_NAME} ---")
# Load the tokenizer specific to the chosen BERT model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("\n--- Tokenizing Data ---")
# Tokenize the texts. BERT needs 'input_ids' and 'attention_mask'.
# padding=True: Pad sequences to the max_length within the batch.
# truncation=True: Truncate sequences longer than max_length.
# return_tensors='tf': Return TensorFlow tensors.
train_encodings = tokenizer(X_train_texts, truncation=True, padding=True, max_length=MAX_LENGTH)
val_encodings = tokenizer(X_val_texts, truncation=True, padding=True, max_length=MAX_LENGTH)

# --- 5. Create TensorFlow Datasets ---
print("\n--- Creating TensorFlow Datasets ---")
# Convert tokenized data and labels into tf.data.Dataset objects for efficient training
# The tokenizer output is a dictionary, which tf.data.Dataset handles nicely.
train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_encodings), # Input features (input_ids, attention_mask, etc.)
    y_train                # Labels
))
val_dataset = tf.data.Dataset.from_tensor_slices((
    dict(val_encodings),
    y_val
))

# Shuffle and batch the datasets
train_dataset = train_dataset.shuffle(len(X_train_texts)).batch(BATCH_SIZE)
val_dataset = val_dataset.batch(BATCH_SIZE)

print(f"Dataset element spec: {train_dataset.element_spec}")

# --- 6. Load Pre-trained Model ---
print(f"\n--- Loading Pre-trained Model for Sequence Classification: {MODEL_NAME} ---")
# Load the BERT model with a classification head on top.
# num_labels=2 indicates binary classification (0 or 1).
# Use from_pt=True if loading PyTorch weights into TF model (sometimes needed)
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2, from_pt=True)

# --- 7. Compile Model ---
print("\n--- Compiling Model ---")
# Use AdamW optimizer (recommended for Transformers)
optimizer = tf.keras.optimizers.AdamW(learning_rate=LEARNING_RATE) # Note: AdamW from tf.keras.optimizers

# Use SparseCategoricalCrossentropy because labels are integers (0, 1) and the model outputs logits
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# Define metrics
metrics = [
    tf.keras.metrics.SparseCategoricalAccuracy('accuracy'), # Use Sparse version for integer labels
    # You might want to add Precision/Recall/AUC later, potentially via custom callbacks or post-training analysis
    # as standard metrics might need logits conversion within the metric function.
]

model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
model.summary() # Print model architecture

# --- 8. Handle Class Imbalance (Optional but Recommended) ---
print("\n--- Calculating Class Weights ---")
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weight_dict = dict(enumerate(class_weights))
print(f"Class Weights: {class_weight_dict}")

# --- 9. Fine-tuning (Train the Model) ---
print("\n--- Starting Fine-tuning ---")

# Add EarlyStopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy', # Monitor validation accuracy (or val_loss)
    patience=1,             # Stop after 1 epoch with no improvement during fine-tuning
    restore_best_weights=True
)

history = model.fit(
    train_dataset,
    epochs=EPOCHS,
    validation_data=val_dataset,
    class_weight=class_weight_dict, # Apply class weights
    callbacks=[early_stopping]
)

# --- 10. Evaluate Model ---
print("\n--- Evaluating Model on Validation Set ---")
results = model.evaluate(val_dataset, verbose=1) # Use verbose=1 to see progress

print("\nEvaluation Results:")
print(f"Validation Loss: {results[0]:.4f}")
print(f"Validation Accuracy: {results[1]:.4f}")
# Add custom calculation for Precision/Recall/AUC if needed, using model.predict() on val_dataset

# --- 11. Optional: Save the Fine-tuned Model & Tokenizer ---
# print("\n--- Saving Model and Tokenizer ---")
output_dir = './fine_tuned_bertic_hate_speech'
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
# print(f"Model and tokenizer saved to {output_dir}")
# To load later:
loaded_tokenizer = AutoTokenizer.from_pretrained(output_dir)
loaded_model = TFAutoModelForSequenceClassification.from_pretrained(output_dir)

# --- 12. Optional: Example Prediction ---
print("\n--- Example Prediction ---")
sample_texts = [
    "Jebem ti mater.",
    "On je nabildovana pedercina.", # Replace with actual examples
]
# Tokenize the samples
encoded_samples = tokenizer(sample_texts, return_tensors='tf', padding=True, truncation=True, max_length=MAX_LENGTH)
# Get model predictions (logits)
raw_predictions = model.predict(encoded_samples).logits
# Convert logits to probabilities (optional) and get predicted class
probabilities = tf.nn.softmax(raw_predictions, axis=-1).numpy()
predicted_classes = np.argmax(probabilities, axis=-1)

for text, pred_class, prob in zip(sample_texts, predicted_classes, probabilities):
    sentiment = "Hate Speech (1)" if pred_class == 1 else "Not Hate Speech (0)"
    print(f"Text: '{text}'")
    print(f"Prediction: {sentiment}")
    print(f"Probabilities (0, 1): {prob}\n")

print("\n--- Fine-tuning and Evaluation Complete ---")