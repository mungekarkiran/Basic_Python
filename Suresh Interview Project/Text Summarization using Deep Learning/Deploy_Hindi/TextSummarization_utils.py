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

from nltk.tokenize import sent_tokenize
from nltk.tokenize import SpaceTokenizer
from nltk.cluster.util import cosine_distance
from indicnlp.tokenize import sentence_tokenize

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime

import pandas as pd
import numpy as np
import networkx as nx
import re
import math
import string
import operator


# VARIABLES
ROOT_PATH = os.getcwd()
STATIC_DIR = "static"
DATASET_DIR = os.path.join(STATIC_DIR, "dataset")
IMG_DIR = os.path.join(STATIC_DIR, "img")

TRAIN_DATASET_PATH = os.path.join(DATASET_DIR, "train.csv")
train_dataset = pd.read_csv(TRAIN_DATASET_PATH, nrows=200, delimiter=',')
# pd.set_option('display.max_colwidth', None)

patternEnglish = re.compile(r'[[A-Z]|[a-z]]*')
patternNumeric = re.compile(r'.*[0-9]+')
patternBraces = re.compile(r'\[(.*?)\]|\{(.*?)\}|\((.*?)\)')
patternUrl = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")

STOPWORDS_PATH = os.path.join(DATASET_DIR, "final_stopwords.txt")
stopwords = pd.read_csv(STOPWORDS_PATH, header=None)
stopwords.columns = ['stopwords']
stopwords = list(stopwords['stopwords'])
stopwords.extend(['में','के','है','से'])


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


def remove_redundant_sentences(sentences):
    cleaned=[]
    for s in sentences:
        if s in cleaned or s.strip()=='':
            continue
        else:
            cleaned.append(s)
    return cleaned

def clean_corpus(corpus):
    corpus=corpus.replace('।','.')
    corpus=corpus.replace('\xa0','')
    corpus=corpus.replace('\n','')
    corpus=corpus.replace('\r','')
    return corpus

def get_clean_sentences(doc):
    cleaned_doc=clean_corpus(doc)
    sentences=cleaned_doc.split('.')
    sentences=remove_redundant_sentences(sentences)
    return sentences


def create_frequency_table(sentences):
    word_freq = {}
    for sentence in sentences:
        words = SpaceTokenizer().tokenize(sentence)
        for word in words:
            if word in stopwords:
                continue
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
    return word_freq

def score_sentences(sentences,word_freq):
    sentenceValue = {}
    for sentence in sentences:
        words_in_sentence = SpaceTokenizer().tokenize(sentence)
        word_count = len(words_in_sentence)
        for word in word_freq:
            if word in words_in_sentence:
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += word_freq[word]
                else:
                    sentenceValue[sentence[:10]] = word_freq[word]
        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]]/word_count
    return sentenceValue

def average_sentence_value(sentenceValues):
    sum_values = 0
    for sent_id in sentenceValues:
        sum_values += sentenceValues[sent_id]
    sent_count = len(sentenceValues)
    return sum_values/sent_count

def generate_summary(avg_score,sentences,sentenceValue,identifier):
    sentence_count = 0
    summary = ''
    for sentence in sentences:
        if sentence[:identifier] in sentenceValue and sentenceValue[sentence[:identifier]] >= avg_score:
            summary += sentence.strip()+"| "
            sentence_count += 1
    return summary, sentence_count

def summarise_term_frequency_sentence_weighing(sentences):
    word_freq_table = create_frequency_table(sentences)
    scores = score_sentences(sentences,word_freq_table)
    avg_score = average_sentence_value(scores)
    summary, sent_count = generate_summary(avg_score,sentences,scores,10)
    return summary


def calc_term_frequency_sentence_wise(sentences):
    freq_matrix = {}
    for sentence in sentences:
        words = SpaceTokenizer().tokenize(sentence)
        sent_freq_table = {}
        for word in words:
            if word in stopwords:
                continue
            if word in sent_freq_table:
                sent_freq_table[word] += 1
            else:
                sent_freq_table[word] = 1
        freq_matrix[sentence[:15]] = sent_freq_table
    return freq_matrix
        
def calc_tf_matrix(freq_matrix):
    for sentence, sent_freq_table in freq_matrix.items():
        tf_sent = {}
        sent_len = len(sent_freq_table)
        for word in sent_freq_table:
            sent_freq_table[word] /= sent_len
    return freq_matrix

def calc_sentence_frequency(freq_matrix):
    sent_freq = {}
    for sentence, freq_matrix_sent in freq_matrix.items():
        for word, count in freq_matrix_sent.items():
            if word in sent_freq:
                sent_freq[word] += 1
            else:
                sent_freq[word] = 1
    return sent_freq

def calc_idf_score(total_sentences,sent_freq,freq_matrix):
    idf = {}
    for sentence, freq_matrix_sent in freq_matrix.items():
        idf_sent = {}
        for word in freq_matrix_sent:
            idf_sent[word] = math.log10(total_sentences / float(sent_freq[word]))
        idf[sentence] = idf_sent
    return idf
    
def calc_tf_idf_score(tf,idf):
    tf_idf = {}
    for (sentence1,tf_sent), (sentence2,idf_sent) in zip(tf.items(),idf.items()):
        tf_idf_sent = {}
        for (word1,tf_score), (word2,idf_score) in zip(tf_sent.items(),idf_sent.items()):
            tf_idf_sent[word1] = tf_score*idf_score
        tf_idf[sentence1] = tf_idf_sent
    return tf_idf

def calc_tf_idf_score_sentence_wise(tf_idf_matrix):
    tf_idf = {}
    for sentence, tf_idf_sent in tf_idf_matrix.items():
        tf_idf_sentence = 0
        for word, tf_idf_score in tf_idf_sent.items():
            tf_idf_sentence += tf_idf_score
        tf_idf[sentence] = tf_idf_sentence
    return tf_idf

def get_tf_idf(sentences):
    sent_freq_matrix = calc_term_frequency_sentence_wise(sentences)
    freq_matrix = calc_tf_matrix(sent_freq_matrix)
    total_sentences = len(sentences)
    sent_freq = calc_sentence_frequency(freq_matrix)
    idf = calc_idf_score(total_sentences,sent_freq,freq_matrix)
    tf_idf_matrix = calc_tf_idf_score(freq_matrix,idf)
    tf_idf = calc_tf_idf_score_sentence_wise(tf_idf_matrix)
    return tf_idf

def summarise_tf_idf_sentence_weighting(sentences):
    tf_idf = get_tf_idf(sentences)
    sentences = remove_redundant_sentences(sentences)
    avg_tf_idf_score = average_sentence_value(tf_idf)
    tf_idf_summary, sent_count = generate_summary(avg_tf_idf_score,sentences,tf_idf,15)
    return tf_idf_summary


def titlewordsScore(sentence,heading_titlewords):
    titlewords_sent = SpaceTokenizer().tokenize(sentence)
    titlewords_count = len(heading_titlewords)
    titlewords_sent = [word for word in titlewords_sent if word in heading_titlewords]
    s1_score = len(titlewords_sent)/titlewords_count
    return s1_score

def get_len_all_sentences(sentences):
    len_of_all_sent = [len(SpaceTokenizer().tokenize(sentence)) for sentence in sentences]
    max_length = np.max(len_of_all_sent)
    return max_length,len_of_all_sent

def searchEnglishWords(sentence):
    words = SpaceTokenizer().tokenize(sentence.strip())
    words = list(filter(None, words))
    english_words = [word for word in words if patternEnglish.match(word)!=None]
    return len(english_words)/len(words)

def positionScore(total_len):
    mid = (total_len/2)
    positions = (np.arange(total_len,mid,-1)/total_len).tolist()
    if (total_len%2==0):
        positions.extend((np.arange(mid+1,total_len+1,1)/total_len).tolist())
    else:
        positions.extend(np.arange(mid,total_len+1,1).tolist())
    return positions

def numericScore(sentence):
    words = SpaceTokenizer().tokenize(sentence)
    numbers =[1 for word in words if re.match(patternNumeric,word)]
    return np.sum(numbers)/len(words)

def bracesScore(sentence):
    t = re.findall(patternBraces,sentence)
    words = SpaceTokenizer().tokenize(sentence)
    insideTerms = ()
    for term in t:
        insideTerms += term
    insideTerms = [term for term in insideTerms if term !='']
    return (len(words)-len(insideTerms))/len(words)

def draw_zipf_distribution(sentences):
    zipf_distr = {}
    for sentence in sentences:
        words = SpaceTokenizer().tokenize(sentence)
        for word in words:
            if word in zipf_distr:
                zipf_distr[word] += 1
            else:
                zipf_distr[word] = 1
    # fig = plt.figure(figsize=(20, 20))
    # plt.plot(zipf_distr.keys(), zipf_distr.values())
    # plt.xticks(list(range(len(zipf_distr.keys()))), 
    #            zipf_distr.keys(), 
    #            color="b", 
    #            fontproperties = hindi_font, 
    #            rotation = 45);
    # plt.ylabel('Frequency')
    # plt.title('Zipf Distribution')
    return zipf_distr

def keyword_score(sentences):
    zipf_distr = draw_zipf_distribution(sentences)
    keywords = [] 
    count_keywords = round(0.1*len(zipf_distr))
    keywords = [x for x,y in reversed(sorted(zipf_distr.items(), key = operator.itemgetter(1)))][:count_keywords]
    keyword_score = []
    for sentence in sentences:
        words = SpaceTokenizer().tokenize(sentence)
        keyword_score.append(len([word for word in words if word in keywords])/len(words))
    return keyword_score
    
def url_email_score(sentence):
    words = SpaceTokenizer().tokenize(sentence.strip())
    words = list(filter(None, words))
    urls = [word for word in words if patternUrl.match(word) != None]
    return len(urls)/len(words)

def generate_summary_rule_based(clean_sentences,compression_ratio):
    score_table = pd.DataFrame(clean_sentences)
    score_table.columns = ['sentence']

    sample = train_dataset.iloc[199]
    headlinetokens = SpaceTokenizer().tokenize(sample['headline'])
    heading_titlewords = [ word for word in  headlinetokens if word!= '' and word not in stopwords]
    score_table['S1'] = [titlewordsScore(sentence,heading_titlewords) for sentence in clean_sentences]
    max_length,len_of_all_sent = get_len_all_sentences(clean_sentences)
    score_table['S2'] = [x/max_length for x in len_of_all_sent]
    score_table['S3'] = [searchEnglishWords(sentence) for sentence in clean_sentences]
    score_table['S4'] = [numericScore(sentence) for sentence in clean_sentences]
    score_table['S5'] = [bracesScore(sentence) for sentence in clean_sentences]
    score_table['S6'] = keyword_score(clean_sentences)
    score_table['S7'] = [url_email_score(sentence) for sentence in clean_sentences]
    #score_table['S8'] = positionScore(len(clean_sentences))
    score_table['Total'] = score_table['S1']+score_table['S2']+score_table['S3']+score_table['S4']+score_table['S5']+score_table['S6']+score_table['S7']
    summary_sent_count = round(compression_ratio*len(clean_sentences))
    summary_sent = list(score_table.sort_values('Total',ascending=False).iloc[0:summary_sent_count]['sentence'])
    summary = ""
    for sentence in summary_sent:
        summary += sentence.strip()+"| "
    return summary




def create_hindi_wordcloud(hindi_text, font_path, save_path):
    wordcloud = WordCloud(font_path=font_path, 
                          width=800, 
                          height=400, 
                          background_color='white').generate(hindi_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(save_path)
    plt.close()

def get_hindi_wordcloud(hindi_text):
    font_path = os.path.join(DATASET_DIR, "Nirmala.ttf")
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(IMG_DIR, f"{now}_wordcloud.jpeg")
    create_hindi_wordcloud(hindi_text, font_path, save_path)
    return save_path