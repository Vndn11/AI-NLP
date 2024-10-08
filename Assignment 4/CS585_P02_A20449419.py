import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
import re 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag
import sys
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report
import matplotlib.pyplot as plt

df = pd.read_csv('IMDB Dataset.csv')

# Text_PreProcessing

# 1. Lowercasing

df['review'] = df['review'].str.lower()

# 2. Remove HTML tags

df['review'] = df['review'].str.replace('<.*?>', '', regex=True)

# # 3. Remove URLs

df['review'] = df['review'].str.replace('https?://\S+|www\.\S+', '', regex=True)

# 4. Remove Punctuation

punc = string.punctuation

def remove_punc(text):
    return text.translate(str.maketrans('', '', punc))

df['review'] = df['review'].apply(remove_punc)

# 5. Handling Chatwords

chat_words = {
    "AFAIK": "As Far As I Know",
    "AFK": "Away From Keyboard",
    "ASAP": "As Soon As Possible",
    "ATK": "At The Keyboard",
    "ATM": "At The Moment",
    "A3": "Anytime, Anywhere, Anyplace",
    "BAK": "Back At Keyboard",
    "BBL": "Be Back Later",
    "BBS": "Be Back Soon",
    "BFN": "Bye For Now",
    "B4N": "Bye For Now",
    "BRB": "Be Right Back",
    "BRT": "Be Right There",
    "BTW": "By The Way",
    "B4": "Before",
    "B4N": "Bye For Now",
    "CU": "See You",
    "CUL8R": "See You Later",
    "CYA": "See You",
    "FAQ": "Frequently Asked Questions",
    "FC": "Fingers Crossed",
    "FWIW": "For What It's Worth",
    "FYI": "For Your Information",
    "GAL": "Get A Life",
    "GG": "Good Game",
    "GN": "Good Night",
    "GMTA": "Great Minds Think Alike",
    "GR8": "Great!",
    "G9": "Genius",
    "IC": "I See",
    "ICQ": "I Seek you (also a chat program)",
    "ILU": "ILU: I Love You",
    "IMHO": "In My Honest/Humble Opinion",
    "IMO": "In My Opinion",
    "IOW": "In Other Words",
    "IRL": "In Real Life",
    "KISS": "Keep It Simple, Stupid",
    "LDR": "Long Distance Relationship",
    "LMAO": "Laugh My A.. Off",
    "LOL": "Laughing Out Loud",
    "LTNS": "Long Time No See",
    "L8R": "Later",
    "MTE": "My Thoughts Exactly",
    "M8": "Mate",
    "NRN": "No Reply Necessary",
    "OIC": "Oh I See",
    "PITA": "Pain In The A..",
    "PRT": "Party",
    "PRW": "Parents Are Watching",
    "QPSA?": "Que Pasa?",
    "ROFL": "Rolling On The Floor Laughing",
    "ROFLOL": "Rolling On The Floor Laughing Out Loud",
    "ROTFLMAO": "Rolling On The Floor Laughing My A.. Off",
    "SK8": "Skate",
    "STATS": "Your sex and age",
    "ASL": "Age, Sex, Location",
    "THX": "Thank You",
    "TTFN": "Ta-Ta For Now!",
    "TTYL": "Talk To You Later",
    "U": "You",
    "U2": "You Too",
    "U4E": "Yours For Ever",
    "WB": "Welcome Back",
    "WTF": "What The F...",
    "WTG": "Way To Go!",
    "WUF": "Where Are You From?",
    "W8": "Wait...",
    "7K": "Sick:-D Laugher",
    "TFW": "That feeling when",
    "MFW": "My face when",
    "MRW": "My reaction when",
    "IFYP": "I feel your pain",
    "TNTL": "Trying not to laugh",
    "JK": "Just kidding",
    "IDC": "I don't care",
    "ILY": "I love you",
    "IMU": "I miss you",
    "ADIH": "Another day in hell",
    "ZZZ": "Sleeping, bored, tired",
    "WYWH": "Wish you were here",
    "TIME": "Tears in my eyes",
    "BAE": "Before anyone else",
    "FIMH": "Forever in my heart",
    "BSAAW": "Big smile and a wink",
    "BWL": "Bursting with laughter",
    "BFF": "Best friends forever",
    "CSL": "Can't stop laughing"
}

def chat_conversion(text):
    new_text = []
    for i in text.split():
        if i.upper() in chat_words:
            new_text.append(chat_words[i.upper()])
        else:
            new_text.append(i)
    return " ".join(new_text)

df['review'] = df['review'].apply(chat_conversion)

# 6. Removing Stopwords

nltk.download('stopwords')
stopword = stopwords.words('english')
stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    return ' '.join(word for word in text.split() if word not in stop_words)

df['review'] = df['review'].apply(remove_stopwords)

# 7. Removing Emoji

def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  
                           u"\U0001F300-\U0001F5FF"  
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

df['review'] = df['review'].apply(remove_emoji)

# # 8. Tokenization

# nltk.download('punkt')


def word_tokenizer(text):
    return word_tokenize(text)

df['tokenized_review'] = df['review'].apply(word_tokenizer)

# 8. Tokenize and Lemmatize
# nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
def lemmatize_text(tokens):
    tagged_tokens = pos_tag(tokens)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in tagged_tokens]
    lemmatized_sentence = ' '.join(lemmatized_tokens)
    return lemmatized_sentence

df['lemmatized_review'] = df['tokenized_review'].apply(lemmatize_text)

########################################################################################################################################

argv1=sys.argv[1]
# argv1 = int(input('Enter the split index'))

# Splitting the Data
total_reviews = len(df)
split_index = int(total_reviews * (argv1/100))

train_df = df[:split_index]
test_df = df[split_index:]

#Function to Create Vocabulary
def create_vocabulary(docs):
    vocabulary = set(word for doc in docs for word in doc.split())
    return list(vocabulary)

# Function to Create Binary Bag of Words using Sparse Matrix
def binary_bow_sparse(reviews, vocabulary):
    rows, cols, data = [], [], []
    vocab_list = list(vocabulary)
    vocab_index = {word: i for i, word in enumerate(vocab_list)}

    for i, review in enumerate(reviews):
        words = set(review.split())
        for word in words:
            if word in vocab_index:  # Only if the word is in the vocabulary
                rows.append(i)
                cols.append(vocab_index[word])
                data.append(1)
    
    return csr_matrix((data, (rows, cols)), shape=(len(reviews), len(vocabulary)), dtype=int)

# Function to Create Parameters using Naive Bayes Theorem
def train_naive_bayes(train_vectors, train_labels, vocabulary):
    n_docs = train_vectors.shape[0]
    n_words = len(vocabulary)
    classes = ["positive", "negative"]
    
    class_word_counts = {cls: np.ones(n_words) for cls in classes}  # Add-1 smoothing
    class_doc_counts = {cls: 1 for cls in classes}  # Add-1 smoothing for document counts
    
    for vector, label in zip(train_vectors, train_labels):
        class_word_counts[label] += vector
        class_doc_counts[label] += 1
    
    params = {
        'priors': {cls: np.log(class_doc_counts[cls] / n_docs) for cls in classes},
        'likelihoods': {cls: np.log(class_word_counts[cls] / class_doc_counts[cls]) for cls in classes}
    }
    
    return params

def predict(test_vector, params):
    class_scores = {cls: params['priors'][cls] + np.sum(test_vector.multiply(params['likelihoods'][cls]).toarray()) for cls in params['priors']}
    return max(class_scores, key=class_scores.get) 

########################################################################################################################################
# Function to Calculate Metrics
def calculate_metrics(true_labels, predicted_labels):
    # Calculate confusion matrix elements
    tn, fp, fn, tp = confusion_matrix(true_labels, predicted_labels, labels=["negative", "positive"]).ravel()
    
    # Metrics calculations
    sensitivity = tp / (tp + fn)  
    specificity = tn / (tn + fp)
    precision = tp / (tp + fp)
    negative_predictive_value = tn / (tn + fn)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    f_score = 2 * precision * sensitivity / (precision + sensitivity)  # F1 Score
    
    # Display metrics
    print(f"Number of True Positives: {tp}")
    print(f"Number of True Negatives: {tn}")
    print(f"Number of False Positives: {fp}")
    print(f"Number of False Negatives: {fn}")
    print(f"Sensitivity (Recall): {sensitivity}")
    print(f"Specificity: {specificity}")
    print(f"Precision: {precision}")
    print(f"Negative Predictive Value: {negative_predictive_value}")
    print(f"Accuracy: {accuracy}")
    print(f"F-score: {f_score}")

# Function to Plot Metrics
def plot_confusion_matrix(true_labels, predicted_labels, classes):
    cm = confusion_matrix(true_labels, predicted_labels, labels=classes)
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title='Confusion Matrix',
           ylabel='True label',
           xlabel='Predicted label')

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.show()


# Function to Plot ROC Curve
def plot_roc_curve(true_labels, predicted_probs):
    
    fpr, tpr, _ = roc_curve(true_labels, predicted_probs)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

# Calling of Functions
vocabulary = create_vocabulary(train_df['review'])

train_vectors = binary_bow_sparse(train_df['review'], vocabulary)
test_vectors = binary_bow_sparse(test_df['review'], vocabulary)

params = train_naive_bayes(train_vectors, train_df['sentiment'], vocabulary)

predictions = [predict(test_vectors[i], params) for i in range(test_vectors.shape[0])]
test_labels = test_df['sentiment'].tolist()

calculate_metrics(test_labels, predictions)

plot_confusion_matrix(test_labels, predictions, ["negative", "positive"])

# Converting Predictions to 1(positive) and 0(negative)
probs = [1 if label == 'positive' else 0 for label in predictions]

# Converting True Labels to 1(positive) and 0(negative)
test_labels_numerical = [1 if label == 'positive' else 0 for label in test_labels]

# Calling Function to Plot ROC Curve
plot_roc_curve(test_labels_numerical, probs)

########################################################################################################################################

def predict_with_probabilities(test_vector, params):
    # Calculate log probabilities for each class
    class_log_probs = {cls: params['priors'][cls] + np.sum(test_vector.multiply(params['likelihoods'][cls]).toarray()) for cls in params['priors']}
    
    # Find the maximum log probability to use for normalization
    max_log_prob = max(class_log_probs.values())
    
    # Convert log probabilities to linear probabilities for reporting
    # First, subtract the max log probability to avoid underflow when exponentiating
    class_probs_linear = {cls: np.exp(log_prob - max_log_prob) for cls, log_prob in class_log_probs.items()}
    
    # Normalize the probabilities so they sum to 1
    total_prob = sum(class_probs_linear.values())
    class_probs_linear = {cls: prob / total_prob for cls, prob in class_probs_linear.items()}
    
    # Return the class with the highest log probability and the normalized linear probabilities of each class
    predicted_class = max(class_log_probs, key=class_log_probs.get)
    return predicted_class, class_probs_linear

def binary_bow_sparse_single(review, vocabulary):

    row, col, data = [], [], []
    vocab_index = {word: i for i, word in enumerate(vocabulary)}
    words = set(review.split())
    
    for word in words:
        if word in vocab_index:  # Only if the word is in the vocabulary
            row.append(0)
            col.append(vocab_index[word])
            data.append(1)
    
    return csr_matrix((data, (row, col)), shape=(1, len(vocabulary)), dtype=int)

while True:
    print("\nEnter your sentence:")
    sentence = input().lower()

    # Preprocess the sentence (if preprocessing function exists)
    # sentence_processed = preprocess(sentence)  # Uncomment if preprocessing is needed

    # Convert the sentence to the same format as the training data
    test_vector = binary_bow_sparse_single(sentence, vocabulary)
    
    # Classify the sentence and get probabilities
    predicted_class, class_probs = predict_with_probabilities(test_vector, params)
    
    
    # Display the results
    print(f"\nSentence S:\n{sentence}\n")
    print(f"was classified as {predicted_class}.")
    for cls, prob in class_probs.items():
        print(f"P({cls} | S) = {prob:.4f}")
    
    # Ask the user if they want to classify another sentence
    repeat = input("\nDo you want to enter another sentence [Y/N]? ").strip().upper()
    if repeat != 'Y':
        break

########################################################################################################################################