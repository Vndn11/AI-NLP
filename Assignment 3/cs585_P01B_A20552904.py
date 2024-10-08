# Importing Libraries.
import nltk
from nltk.corpus import brown
from nltk.probability import ConditionalFreqDist
from nltk import bigrams

# Downloading the Corpus --> Brown.
nltk.download('brown')

# Getting the tokens of all the words in the Corpus.
tokens = [word.lower() for word in brown.words()]

# Calculating Conditional Probability of Every Bigram Present in the Corpus.
bigram_freq = ConditionalFreqDist(bigrams(tokens))

# Creating a List for storing Bigram and their probabilities
bigram_probs = {}

# Creating Function to Calculate the Bigram Probability of the Sentence Provided by the User.
def calculate_bigram_probability(S):

    # Adding a Start and End Token to the Sentence
    S1 = '<s> ' + S + ' </s>'

    # Creating Bigrams of the Sentence using ngrams function
    Sentence_Bigrams = nltk.ngrams(S1.split(),2)
    Sentence_Bigrams = list(Sentence_Bigrams)

    # Initializing the Sentence Probability with 1.0
    S_probability = 1.0


    for w1,w2 in Sentence_Bigrams:

        # If the bigram has a Start or End Token , then the probability is 0.25 
        if w1 == '<s>' or w2 == '</s>': 
            probability = 0.25

        # Else extract the bigram frequency from the earlier calculated bigram frequency list, if not present take 0.01 for smoothing purpose 
        else:
            probability = bigram_freq[w1].freq(w2) if bigram_freq[w1][w2] > 0 else 0.01

        w = '( ' + w1 + ', ' + w2 + ' )'
        bigram_probs[w] = probability

        # Multiply Every Bigram Probability of the Sentence
        S_probability *= probability

    return S_probability,Sentence_Bigrams       

# Taking Input from the User
S = input('Enter a Sentence: ')

# Calling the Functions 
Sentence_Probability, Sentence_Bigrams = calculate_bigram_probability(S.lower())

print('\nSentence is:',S)
print('Sentence Bigrams and their Probabilities are:',bigram_probs)
print('Sentence Probability is:',Sentence_Probability)
print('\n')