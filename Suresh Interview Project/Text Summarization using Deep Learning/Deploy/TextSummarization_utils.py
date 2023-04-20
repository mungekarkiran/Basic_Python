# LIBRARIES
import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from collections import defaultdict

# VARIABLES
ROOT_PATH = os.getcwd()
STATIC_DIR = "static"

# FUNCTIONS
def text_summarizer(text, number_of_sentences):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize each sentence into words and filter out stop words
    stop_words = set(stopwords.words('english'))
    word_tokens = [word_tokenize(sentence.lower()) for sentence in sentences]
    filtered_tokens = [[word for word in words if word not in stop_words] for words in word_tokens]

    # Stem the words to reduce their forms to their base form
    stemmer = PorterStemmer()
    stemmed_tokens = [[stemmer.stem(word) for word in words] for words in filtered_tokens]

    # Flatten the list of tokens and count the frequency of each word
    flat_tokens = [word for sublist in stemmed_tokens for word in sublist]
    word_freq = Counter(flat_tokens)

    # Calculate the score for each sentence based on the frequency of words it contains
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if i in sentence_scores:
                    sentence_scores[i] += word_freq[word]
                else:
                    sentence_scores[i] = word_freq[word]

    # Get the top n sentences with the highest scores to summarize the text
    summary_sentences = []
    n = number_of_sentences # 3  # number of sentences to include in the summary
    sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    for i in range(n):
        summary_sentences.append(sentences[sorted_scores[i][0]])

    # Join the summary sentences into a single string and return it
    summary = ' '.join(summary_sentences)
    # print(summary)

    return summary