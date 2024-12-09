import re
import nltk
import spacy
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.tokenize import sent_tokenize

def remove_html_tags(text):
    '''Remove HTML tags from text.'''
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text

def format_summary(summary_text):
    sentences = sent_tokenize(summary_text)  # Segment into sentences
    formatted_summary = ', '.join(sentences)  # Rejoin sentences with commas for flow
    return formatted_summary

def correct_grammar(summary_text):
    blob = TextBlob(summary_text)
    return str(blob.correct())  # Apply corrections

# Download NLTK stopwords if not already done
# nltk.download('stopwords')

# Load NLTK stopwords
nltk_stopwords = set(stopwords.words('english'))

# Load the spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Contraction dictionary
contractions = { 
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he's": "he is",
    "how'd": "how did",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'll": "i will",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it will",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "must've": "must have",
    "mustn't": "must not",
    "needn't": "need not",
    "oughtn't": "ought not",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "that'd": "that would",
    "that's": "that is",
    "there'd": "there had",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "where'd": "where did",
    "where's": "where is",
    "who'll": "who will",
    "who's": "who is",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are"
}


def clean_text(text, remove_stopwords=True):
    '''Remove unwanted characters, HTML tags, stopwords, format the text, and correct typos.'''
    
    # Remove HTML tags
    text = remove_html_tags(text)
    
    # Convert text to lowercase
    text = text.lower()
    
    # Normalize text to handle encoding issues
    text = text.encode('ascii', 'ignore').decode()  # Remove non-ASCII characters
    
    # Expand contractions
    for contraction, expanded in contractions.items():
        text = text.replace(contraction, expanded)
    
    # Remove URLs and special characters
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
    text = re.sub(r'\'', ' ', text)

    # Tokenize and lemmatize with spaCy
    doc = nlp(text)

    # Perform selective lemmatization
    processed_tokens = []
    for token in doc:
        if token.pos_ in ('NOUN', 'VERB') and token.text not in nltk_stopwords:
            processed_tokens.append(token.lemma_)
        elif token.pos_ in ('ADJ', 'ADV') and token.text not in nltk_stopwords:
            processed_tokens.append(token.text)
        elif not remove_stopwords:
            processed_tokens.append(token.text)

    # Validate cleaned tokens
    if len(processed_tokens) < 15:  # Discard if too few tokens
        return ""
    
    # Join tokens into a cleaned-up text string
    cleaned_text = " ".join(processed_tokens)

    return cleaned_text
