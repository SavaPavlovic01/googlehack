<<<<<<< HEAD

def get_username_twitter(url):
    username =url.split("x.com/")[1].split('/')[0]
    return username
if __name__ == "__main__":
    print(get_username_twitter("https://x.com/MrKimmKE/status/1918582688979493122"))
=======
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import logging # Optional: Track Hugging Face logs

MAX_LENGTH = 175
output_dir = './fine_tuned_bertic_hate_speech'
# print(f"Model and tokenizer saved to {output_dir}")
# To load later:
loaded_tokenizer = AutoTokenizer.from_pretrained(output_dir)
loaded_model = TFAutoModelForSequenceClassification.from_pretrained(output_dir)

# --- 12. Optional: Example Prediction ---
print("\n--- Example Prediction ---")
sample_texts = [
    "Jebem ti mater.",
    "Sram vas bilo, studenti pedercine! Blokaderi žele da predsednik padne mrtav?! Vučiću preti šlog, a oni likuju. Sramotno, jadno i nadasve neljudski. Dok predsednik Srbije Aleksandar Vučić svakodnevno rizikuje svoje zdravlje da bi se borio za interese građana, blokaderi, u nedostatku bilo kakvih argumenata, sprdaju se sa njegovim ozbiljnim zdravstvenim problemima! Predsednik Vučić godinama unazad vodi tešku borbu sa visokim krvnim pritiskom, opasnim stanjem koje može dovesti do infarkta, šloga i drugih životno ugrožavajućih posledica. Uprkos svemu, on nijednog trenutka nije tražio poštedu! Svaki dan je na terenu, među narodom, neumorno radi i daje svoj maksimum, čak i kad mu lekari preporučuju mirovanje. Ali to nije dovoljno za političke parazite i moralne bednike, koji u svom očaju i mržnji nemaju ni trunku ljudskosti. Umesto da pokažu saosećanje, oni se rugaju Vučićevoj borbi za zdravlje, bez ikakvog obzira.", # Replace with actual examples
]
# Tokenize the samples
encoded_samples = loaded_tokenizer(sample_texts, return_tensors='tf', padding=True, truncation=True, max_length=MAX_LENGTH)
# Get model predictions (logits)
raw_predictions = loaded_model.predict(encoded_samples).logits
# Convert logits to probabilities (optional) and get predicted class
probabilities = tf.nn.softmax(raw_predictions, axis=-1).numpy()
predicted_classes = np.argmax(probabilities, axis=-1)

for text, pred_class, prob in zip(sample_texts, predicted_classes, probabilities):
    sentiment = "Hate Speech (1)" if pred_class == 1 else "Not Hate Speech (0)"
    print(f"Text: '{text}'")
    print(f"Prediction: {sentiment}")
    print(f"Probabilities (0, 1): {prob}\n")

print("\n--- Fine-tuning and Evaluation Complete ---")
>>>>>>> f1db0d7b615b8e0f242569ab17daae793814fb9b
