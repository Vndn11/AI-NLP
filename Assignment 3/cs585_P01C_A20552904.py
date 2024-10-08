# Importing Libraries
import nltk
from nltk.probability import ConditionalFreqDist
from nltk import bigrams

# Initializing Sentence List
sentence = []

# Downloading Corpus --> Brown, Stopword(In order to remove stopwords)
nltk.download('brown')
nltk.download('stopwords')

# Removing Stopwords from Brown Corpus
stopWordsCorpus = nltk.corpus.stopwords.words('english')
corpus = nltk.corpus.brown
words = corpus.words()
word_list_brown = []
for word in words:
    if word.lower() not in stopWordsCorpus:
        word_list_brown.append(word.lower())

# Calculating Bigram Frequency of Every Bigrams in the Corpus
tokens = [word.lower() for word in word_list_brown]
bigram_freq = ConditionalFreqDist(bigrams(tokens))

# Creating Function for getting the top 3 frequent words followed by user's choice word
def get_top3_common_following_words(W1, bigram_freq):
    following_words = bigram_freq[W1].most_common(3)
    return following_words

# Creating a Function for Getting the Initial Word/Token word W1 from User    
def get_W1_from_user():
    while True:
        W1 = input('\nEnter the Token Word W1: ').lower()
        if W1 in word_list_brown:
            return W1
        else:
            print('\nThe Word is not in the Corpus.')
            print('A) Enter Again\nB) Quit\n')
            choice = input('Enter your Choice(Y/N): ').lower()
            if choice == 'n':
                print('Exiting the Program')
                return None

# Creating a Function to Display the Top 3 Most Frequent Word Followed by Word given by User
def display_menu(W1,bigram_freq):
    following_words = get_top3_common_following_words(W1, bigram_freq)
    print(W1 + ' ... \n')
    print('Which word should follow:\n')
    for i, (word, freq) in enumerate(following_words, start=1):
        print(f"{i}) {word} P({W1} {word}) = {freq / bigram_freq[W1].N():.2f}")
    print('4) QUIT\n')
    choice2 = input('Enter your choice: ')
    if choice2.isdigit() and int(choice2) in [1,2,3]:
        return following_words[int(choice2)-1][0]
    elif choice2 == '4':
        return 'QUIT'
    else:
        return following_words[0][0]

# Main Fucntion : This runs in a loop and call all the other functions as per user's input
def sentence_building():
    sentence = []
    w1 = get_W1_from_user()
    if w1 is None:
        return
    sentence.append(w1)
    # print('Sentence:',sentence)
    while True:
        next_word = display_menu(w1,bigram_freq)
        if next_word == 'QUIT':
            print('Exiting the Program\n')
            return
        else:
            sentence.append(next_word)
            sentence1 = ' '.join(sentence)
            print('\nSentence:',sentence1)
            print('\n')
            w1 = next_word

# Calling the Main Function
sentence_building()
