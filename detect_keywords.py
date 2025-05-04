import stanza
import pandas as pd
# stanza.download('sr')  # 'sr' = Serbian

def normalize_serbian(text):
    replacements = {
        'č': 'c', 'ć': 'c',
        'š': 's', 'ž': 'z',
        'đ': 'dj',
        'Č': 'C', 'Ć': 'C',
        'Š': 'S', 'Ž': 'Z',
        'Đ': 'Dj'
    }
    for src, target in replacements.items():
        text = text.replace(src, target)
    return text



# Load and normalize keywords to lowercase
df_keywords = pd.read_csv("keywords.csv", header=None)
keyword_set = set(df_keywords[0].str.lower())

keyword_set = set(normalize_serbian(word.lower()) for word in keyword_set)

nlp = stanza.Pipeline(lang='sr', processors='tokenize,pos,lemma')
doc = nlp("Sram vas bilo, studenti pedercine! Blokaderi žele da predsednik padne mrtav?! Vučiću preti šlog, a oni likuju. Sramotno, jadno i nadasve neljudski. Dok predsednik Srbije Aleksandar Vučić svakodnevno rizikuje svoje zdravlje da bi se borio za interese građana, blokaderi, u nedostatku bilo kakvih argumenata, sprdaju se sa njegovim ozbiljnim zdravstvenim problemima! Predsednik Vučić godinama unazad vodi tešku borbu sa visokim krvnim pritiskom, opasnim stanjem koje može dovesti do infarkta, šloga i drugih životno ugrožavajućih posledica. Uprkos svemu, on nijednog trenutka nije tražio poštedu! Svaki dan je na terenu, među narodom, neumorno radi i daje svoj maksimum, čak i kad mu lekari preporučuju mirovanje. Ali to nije dovoljno za političke parazite i moralne bednike, koji u svom očaju i mržnji nemaju ni trunku ljudskosti. Umesto da pokažu saosećanje, oni se rugaju Vučićevoj borbi za zdravlje, bez ikakvog obzira.")

lemmas = [normalize_serbian(word.lemma.lower()) for sentence in doc.sentences for word in sentence.words]


# Extract lemmatized words
lemmas = []
for sentence in doc.sentences:
    for word in sentence.words:
        lemmas.append(word.lemma.lower())

# Find matches
matched_keywords = set(lemmas) & keyword_set
print("Matched keywords:", matched_keywords)