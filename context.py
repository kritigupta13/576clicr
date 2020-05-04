import json
import random
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
from math import floor
 
def read_article(filedata):
    article = filedata.split(" .")
    print(len(article))    
    return article

def sentence_similarity(sent1, ques, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    ques = [w.lower() for w in ques]
 
    all_words = list(set(sent1 + ques))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in ques:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def build_similarity_matrix(sentences, question, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences)))
    for idx1 in range(len(sentences)):
        similarity_matrix[idx1] = sentence_similarity(sentences[idx1], question, stop_words)

    return similarity_matrix


def generate_summary(passage, question, top_n=0.2):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences =  read_article(passage)
    
    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, question, stop_words)
    
    #print(sentence_similarity_martix.shape)
    
    # Step 3 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((sentence_similarity_martix[i],s) for i,s in enumerate(sentences)), reverse=True)    
    #print("Indexes of top ranked_sentence order are ", ranked_sentence)    

    for i in range(floor(len(sentences)*top_n)):
      summarize_text.append("".join(ranked_sentence[i][1]))
    print(len(summarize_text))
    # Step 4 - Offcourse, output the summarize texr
    summary = ". ".join(summarize_text)
    print("Summarize Text: \n" + summary)
    return summary    

file_path = 'dev1.0.json'
output = open('results.txt', 'w+')

with open(file_path) as f:
    data = json.load(f)

### FILE ###
N = len(data['data'])
print("Total = ", N)

#Picking n random passages
pass_n = 100
passages = []

for i in range(0, pass_n):
    temp1 = random.randint(0, N-1)
    passages.append(temp1)

print("Chosen Passages:", passages)

for passage in passages:
    print("Passage ", passage)
    print("Document Title:  ", data['data'][passage]['document']['title'])
    #print(type(data['data'][passage]['document']['context']))
    pass_str = str(data['data'][passage]['document']['context'])
    ques_n = len(data['data'][passage]['document']['qas'])
    print("Questions = ", ques_n)
    for question in range(0, ques_n):
        print("Q "+str(question)+": "+str(data['data'][passage]['document']['qas'][question]['query'])+"\n")
        ques_str = str(data['data'][passage]['document']['qas'][question]['query'])
        short_pass = generate_summary(pass_str, ques_str)
        print("Before: ", len(pass_str), "\nAfter: ", len(short_pass))
    print("\n\n")