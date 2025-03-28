import spacy
import argparse

class TextProcessor:
    def __init__(self, model="ru_core_news_sm"):
        self.nlp = spacy.load(model)

    def process_text(self, text):
        text_i = self.nlp(text)
        return {token.lemma_ for token in text_i if not token.is_stop and token.is_alpha}

class TextClassifier:
    def __init__(self, texts):
        self.texts = texts

    def classify_text(self, text_i):
        text_processor = TextProcessor()
        text_t = text_processor.process_text(text_i)

        n = 0
        text_type = ""
        for category, words in self.texts.items():
            common_words = len(text_t & words)
            if common_words > n:
                n = common_words
                text_type = category
        return text_type.split('/')[-1]
        

def load_texts(texts_name):
    texts = {}
    text_processor = TextProcessor()
    
    for text in texts_name:
        with open(text, 'r', encoding='utf-8') as file:
            text_i = file.read()
            text_t = text_processor.process_text(text_i)
            name = text.rstrip('.txt').rstrip('1234')
            if name not in texts:
                texts[name] = set()
            texts[name].update(text_t)
    
    return texts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text_guess', type=str, help="Путь к тексту для классификации")
    parser.add_argument('texts_train_dir', type=str, help="Путь к директории с текстами для базы данных")
    args = parser.parse_args()

    texts_name = [f'{args.texts_train_dir}/{x}{i}.txt' for x in ['мат', 'астроном', 'астро', 'палео'] for i in range(1, 5)]
    texts = load_texts(texts_name)
    
    with open(args.text_guess, 'r', encoding='utf-8') as file:
        new_text = file.read()

    classifier = TextClassifier(texts)
    predicted_category = classifier.classify_text(new_text)
    print(f"Тема текста: {predicted_category}")

if __name__ == "__main__":
    main()
