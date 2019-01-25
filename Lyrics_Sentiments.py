# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 15:16:54 2017

@author: Dieter Erben
"""

import pandas as pd, re, collections, matplotlib.pyplot as plt, numpy as np

#os.chdir('/Users/dietererben/Documents/My Data Projects')


filepath = "NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
emolex_df = pd.read_csv(filepath,  names=["word", "emotion", "association"], skiprows=45, sep='\t')
emolex_df.head

emolex_words = emolex_df.pivot(index='word', columns='emotion', values='association').reset_index()
emolex_words.head()

anger = emolex_words[emolex_words.anger == 1].word
anticipation = emolex_words[emolex_words.anticipation == 1].word
disgust = emolex_words[emolex_words.disgust == 1].word
fear = emolex_words[emolex_words.fear == 1].word
joy = emolex_words[emolex_words.joy == 1].word
negative = emolex_words[emolex_words.negative == 1].word
positive = emolex_words[emolex_words.positive == 1].word
sadness = emolex_words[emolex_words.sadness == 1].word
surprise = emolex_words[emolex_words.surprise == 1].word
trust = emolex_words[emolex_words.trust == 1].word


allsongs = pd.read_csv('songdata.csv')
allsongs = allsongs[['artist','song','text']]

# list of stopwords at the bottom
def removeStopwords(wordlist, stopwords):
    return [w for w in wordlist if w not in stopwords]

artist = input('Enter an artist: ')
while artist not in list(allsongs.artist):
    artist = input('Enter an artist: ')
artist_match = allsongs[allsongs.artist == artist]
all_lyrics = artist_match.text.str.cat()
all_lyrics = all_lyrics.replace("'", "")
words = re.findall('\w+', all_lyrics.lower())
words = removeStopwords(words,stopwords)
top20 = collections.Counter(words).most_common(20)
topwords = pd.DataFrame(top20,columns=['word','count'])
 

freqs = collections.Counter(words)
word_freq = pd.DataFrame.from_dict(freqs, orient='index').reset_index()
word_freq = word_freq.rename(index=str,columns={'index':'word',0:'freq'})
word_freq = pd.merge(word_freq,emolex_words,how='left',on='word')

word_freq['sum'] = word_freq.anger + word_freq.anticipation + word_freq.disgust + word_freq.fear + word_freq.joy + word_freq.negative + word_freq.positive + word_freq.sadness + word_freq.surprise + word_freq.trust
word_freq = word_freq.loc[word_freq['sum'].isin([1,2,3,4,5,6,7,8,9,10])]


word_freq.anger = np.multiply(word_freq.anger,word_freq.freq)
word_freq.anticipation = np.multiply(word_freq.anticipation, word_freq.freq)
word_freq.disgust = np.multiply(word_freq.disgust, word_freq.freq)
word_freq.fear = np.multiply(word_freq.fear, word_freq.freq)
word_freq.joy = np.multiply(word_freq.joy, word_freq.freq)
word_freq.negative = np.multiply(word_freq.negative, word_freq.freq)
word_freq.positive = np.multiply(word_freq.positive, word_freq.freq)
word_freq.sadness = np.multiply(word_freq.sadness, word_freq.freq)
word_freq.surprise = np.multiply(word_freq.surprise, word_freq.freq)
word_freq.trust = np.multiply(word_freq.trust, word_freq.freq)

results = pd.DataFrame(columns=['words','anger','anticipation','disgust','fear','joy','negative','positive','sadness','surprise','trust'], index=['totals'])
results.words = sum(word_freq.freq)
results.anger = sum(word_freq.anger) / results.words
results.anticipation = sum(word_freq.anticipation) / results.words
results.disgust = sum(word_freq.disgust) / results.words
results.fear = sum(word_freq.fear) / results.words
results.joy = sum(word_freq.joy) / results.words
results.negative = sum(word_freq.negative) / results.words
results.positive = sum(word_freq.positive) / results.words
results.sadness = sum(word_freq.sadness) / results.words
results.surprise = sum(word_freq.surprise) / results.words
results.trust = sum(word_freq.trust) / results.words

objects = ('Anger','Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness','Surprise','Trust')
y_pos = np.arange(len(objects))
scores = [results.anger.values,results.anticipation.values,results.disgust.values,results.fear.values,results.joy.values,results.sadness.values,results.surprise.values,results.trust.values]
scores = [y for x in scores for y in x]
graph = plt.barh(y_pos, scores, align='center', alpha=1)
plt.yticks(y_pos, objects)
plt.xlabel('Percent')
plt.title(artist + "'s lyrics emotions") 
plt.show()

objects = ('Negative','Positive')
y_pos = np.arange(len(objects))
scores = [results.negative.values,results.positive.values]
scores = [y for x in scores for y in x]
graph = plt.barh(y_pos, scores, align='center', alpha=1,color=['red', 'green'])
plt.yticks(y_pos, objects)
plt.xlabel('Percent')
plt.title(artist + "'s Positive vs. Negative") 
plt.show()

plot = topwords.plot(x='word',y='count',kind='bar',title=artist + "'s most common words")
    

#Stopwords
"""
stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']
stopwords += ['la','im','like','you','dont','let','youre','gonna','just','ive','got','ha','wont','ill','youll','hes','cause','chorus','bout','oh','aint','ya','verse','ooh','lea','na','id','nah','oo','ah']
"""