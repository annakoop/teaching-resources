"""Some utilities for dealing with classification problems"""
import os
import re, collections
from bs4 import BeautifulSoup
import arff

import nltk
from nltk.corpus import stopwords


def most_frequent_words(text, k=10):
    """
    Return a list of the k most frequent words in the supplied text, 
    with the most frequent occuring first.
    Ignore common English words
    """
    # get just the interesting words from the text
    word_list = get_message_body(text).split()
    words = remove_stopwords(word_list)
    counts = collections.Counter(words)
    return counts.most_common(k)

def remove_stopwords(words):
    """
    Go through the list of words and remove all the ones that occur in the stopwords list.
    """
    return [w for w in words if w not in stopwords.words("english")]

def get_message_body(text):
    """
    Return just the text of the message body, none of the header information
    """
    contents = BeautifulSoup(text)
    return contents.get_text()

def parse_email(path_to_emails, label_file, output="train.arff"):
    """
    Create a text file that has one line for each email in the path_to_emails directory.
    That line contains the label in the specified labels file together with some features
    """
    contents = os.listdir(path_to_emails)
    num_words = 10
    
    # get the dictionary of labels
    labels = {}
    with open(label_file, 'r') as fin:
        for line in fin:
            v, k = line.split()
            labels[k] = v
    
    # set up the attribute headers
    names = ['spam'] + ["w{}".format(i) for i in range(num_words)]
    data = []
    
    # write the headers to the file
    #try:
    #    fout = open(output, 'w', encoding='latin-1')
    #except:
    #    print("Could not open output file")
    #fout.write(",".join(names)+"\n")    
    
    max_files = 10
    i = 0
    for file in contents:
        i += 1
        # check extension
        if os.path.splitext(file)[1] != '.eml':
            continue

        print("Parsing {}...".format(file), end='')
        # parse the file contents
        with open(os.path.join(path_to_emails, file), 'r', encoding='latin-1') as fin:
            text = fin.read()
            
            # apply our feature extraction functions
            common = most_frequent_words(text, k=num_words)
            words = [c[0] for c in common]
            data.append([int(labels[file])]+words)
            #t = ",".join([labels[file]]+words)
            #fout.write(t+"\n")
        print("Done")
        if i > max_files:
            break
    #fout.close()
    
    # convert the data to arff
    arff.dump(output, data, relation='spam', names=names)
            

if __name__ == "__main__":
    #nltk.download()
    parse_email('spam/TRAINING', 'spam/SPAMTrain.label')
    