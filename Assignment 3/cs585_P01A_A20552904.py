#Import all the packages required

import nltk
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

# downloading the corpus required from NLTK into harddrive
nltk.download('brown')
nltk.download('reuters')
nltk.download('stopwords')

# picking the stopwords for ENGLISH from the whole corpus and store it as list 
stopWordsCorpus = nltk.corpus.stopwords.words('english')

# taking the brown and reuters corpus in a variable as a list
corpus1 = nltk.corpus.brown
corpus2 = nltk.corpus.reuters

# picking only the words list from the whole corpus using .words() function
words1 = corpus1.words()
words2 = corpus2.words()

# Removing the stopwords using the stopword list we have
# Since the words1 and words2 are ConcatenatedCorpusView objects, we cannot modify it. So we will create a new list of words without stopwords

# Initializing Lists

word_list_brown = [] 
word_list_reuters = []  

# ------------------------------1------------------------------


# Removing Stopwords
for word in words1:
    if word.lower() not in stopWordsCorpus:
        word_list_brown.append(word.lower())

for word in words2:
    if word.lower() not in stopWordsCorpus:
        word_list_reuters.append(word.lower())  


# Getting the Frequency of every word in the corpus using FREQDIST Function
freq_distrubution_brown = nltk.FreqDist(word_list_brown)
freq_distrubution_reuters = nltk.FreqDist(word_list_reuters)


# ------------------------------2------------------------------


# Getting the Top ten Frequent words for both corpora using most_common function
top_10_brown = freq_distrubution_brown.most_common(10)
top_10_reuters = freq_distrubution_reuters.most_common(10)

print('Top Ten Frequent Words in Brown Corpora')
for i,j in top_10_brown:
    print(i + '    ' + str(j))

print('\nTop Ten Frequent Words in Reuters Corpora')
for i,j in top_10_reuters:
    print(i + '   ' + str(j))

# ------------------------------3------------------------------

# Getting the Top 1000 words for both corpora using most_common function
top_1000_brown = freq_distrubution_brown.most_common(1000)
top_1000_reuters = freq_distrubution_reuters.most_common(1000)

# Extracting only the frequency of 1000 words
top_1000_brown_freq = [freq for _, freq in top_1000_brown]
top_1000_reuters_freq = [freq for _, freq in top_1000_reuters]

# Converting frequencies into a array format
top_1000_brown_array = np.array(top_1000_brown_freq)
top_1000_reuters_array = np.array(top_1000_reuters_freq)

# Creating a array of Ranks 1 to 1000
ranks = np.arange(1, 1001)

# Applying log to every values
log_ranks = np.log(ranks)
log_top_1000_brown = np.log(top_1000_brown_array)
log_top_1000_reuters = np.log(top_1000_reuters_array)



# Plotting --> log(rank) vs log(frequency) using MATPLOTLIB

fig, ax = plt.subplots(1,2, figsize = (14,6))

ax[0].plot(log_top_1000_brown,log_ranks, marker='o', linestyle = '-', color = 'blue', markersize=4, label = 'Brown Corpus')
ax[0].set_title('Log(Rank) VS Log(Frequency) for Brown Corpus')
ax[0].set_xlabel('Log(Rank)')
ax[0].set_ylabel('Log(Frequency)')
ax[0].grid(True)
ax[0].legend()

ax[1].plot(log_top_1000_reuters,log_ranks, marker='o', linestyle = '-', color = 'green', markersize=4, label = 'Reuters Corpus')
ax[1].set_title('Log(Rank) VS Log(Frequency) for Reuters Corpus')
ax[1].set_xlabel('Log(Rank)')
ax[1].set_ylabel('Log(Frequency)')
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.show()

# ------------------------------4------------------------------

# Taking inputs of a Technical word and Non-Technical word from user

technical_word = input('\nEnter a Technical Word: ')
non_technical_word = input('\nEnter a Non-Technical Word: ')

# Calculating the Unigram occurrence probability

technical_word_freq_brown = freq_distrubution_brown[technical_word.lower()]
technical_word_freq_reuters = freq_distrubution_reuters[technical_word.lower()]
non_technical_word_freq_brown = freq_distrubution_brown[non_technical_word.lower()]
non_technical_word_freq_reuters = freq_distrubution_reuters[non_technical_word.lower()]

Brown_total_words = len(word_list_brown)
Reuters_total_words = len(word_list_reuters)

unigram_probability_Brown_technical = technical_word_freq_brown/Brown_total_words
unigram_probability_Brown_non_technical = non_technical_word_freq_brown/Brown_total_words

unigram_probability_reuters_technical = technical_word_freq_reuters/Reuters_total_words
unigram_probability_reuters_non_technical = non_technical_word_freq_reuters/Reuters_total_words

print('\nThe Frequency Count of Technical Word "' + technical_word.lower() +'" in Brown Corpus is:',technical_word_freq_brown)
print('The Frequency Count of Non-Technical Word "' + non_technical_word.lower() +'" in Brown Corpus is:',non_technical_word_freq_brown)

print('The Frequency Count of Technical Word "' + technical_word.lower() +'" in Reuters Corpus is:',technical_word_freq_reuters)
print('The Frequency Count of Non-Technical Word "' + non_technical_word.lower() +'" in Reuters Corpus is:',non_technical_word_freq_reuters)

print('\n Total number of words in Brown Corpus is:',Brown_total_words)
print('\n Total number of words in Reuters Corpus is:',Reuters_total_words)

print('\nUnigram Probability of Technical Word "'+ technical_word.lower() +'" in Brown Corpus is',unigram_probability_Brown_technical)
print('Unigram Probability of Non Technical Word "'+ non_technical_word.lower() +'" in Brown Corpus is',unigram_probability_Brown_non_technical)

print('\nUnigram Probability of Technical Word "'+ technical_word.lower() +'" in Reuters Corpus is',unigram_probability_reuters_technical)
print('Unigram Probability of Non Technical Word "'+ non_technical_word.lower() +'" in Reuters Corpus is',unigram_probability_reuters_non_technical)





