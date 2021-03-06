# -*- coding: utf-8 -*-
"""CNN_Implementation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PZixzj7Wvuu2qvMNwnRKO61jxEXGigYp

ref:

(1)  https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/

(2)https://machinelearningmastery.com/develop-word-embedding-model-predicting-movie-review-sentiment/

(3)http://ceur-ws.org/Vol-2244/paper_11.pdf

INSTRUCTIONS: Select 'RUN ALL' (if on Google Colab). Otherwise, Select your IDE's/software's version of RUN ALL

GitHub Link: https://github.com/RobertWetzler/CSE3521_EmojiPrediction

Other notes: the very last cell contains the ability to type out your own tweet and have the algorithm try and guess what emoji fits the best with the tweet. The program will keep asking you to enter more tweets until you stop execution of the cell.
"""

us_train = "https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/us_trial.text"
us_train_label= "https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/us_trial.labels"
us_test = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/us_test.text'
us_test_label = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/us_test.labels'

es_train = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/es_trial.text'
es_train_label = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/es_trial.labels'
es_test = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/es_test.text'
es_test_label = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/es_test.labels'

es_mapping = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/es_mapping.txt'
us_mapping = 'https://raw.githubusercontent.com/RobertWetzler/CSE3521_EmojiPrediction/main/us_mapping.txt'

from urllib.request import urlopen
def read_data(data, url, get_token ):
  tokens = []
  file =urlopen(url) 
  for line in file:  
      line = line.decode('utf-8').split("\n")[0]
      data.append(line)   
      if get_token:
        for token in line.split():
          tokens.append(token)
  return tokens

train = []
train_label =[]
test=[]
test_label = []
tokens =[]
tokens = read_data(train, us_train, True )
read_data(train_label, us_train_label, False )
tokens.extend (read_data(test, us_test, True ) )
read_data(test_label, us_test_label ,False)
print("")

s_train = []
s_train_label =[]
s_test=[]
s_test_label = []
s_tokens =[]
s_tokens = read_data(s_train, es_train, True )
read_data(s_train_label, es_train_label, False )
s_tokens.extend (read_data(s_test, es_test, True ) )
read_data(s_test_label, es_test_label ,False)
print("")

"""Find total 32014 unique tokens that has a min occurrence of 2 and store them in a set"""

from string import punctuation
from os import listdir
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
 

def clean_doc(tokens, language):
	# remove punctuation from each token
  table = str.maketrans('', '', punctuation)
  tokens =[w.translate(table) for w in tokens]
	# remove remaining tokens that are not alphabetic
  tokens = [word for word in tokens if word.isalpha()]
  # filter out stop words
  stop_words = set(stopwords.words(language))
  tokens = [w for w in tokens if not w in stop_words]
   
	# filter out short tokens
  tokens = [word for word in tokens if len(word) > 1]
  return tokens

tokens =clean_doc(tokens, "english")
vocabs = Counter()
vocabs.update(tokens)
print(len(vocabs))
print(vocabs.most_common(50))

# keep tokens with a min occurrence 2
min_occurane = 2
tokens = set([k for k,c in vocabs.items() if c >= min_occurane])

print(len(tokens))

##same for spanish data
s_tokens =clean_doc(s_tokens, "spanish")
s_vocabs = Counter()
s_vocabs.update(s_tokens)
print(len(s_vocabs))
print(s_vocabs.most_common(50))

# keep tokens with a min occurrence 2
min_occurane = 2
s_tokens = set([k for k,c in vocabs.items() if c >= min_occurane])

print(len(s_tokens))

#clean x data
def clean_data( data, vocabs):
  x_data=[]
  for line in data: 
    tokens = line.split()
    # remove punctuation from each token
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    # filter out tokens not in vocab
    tokens = [w for w in tokens if w in vocabs]
    tokens = ' '.join(tokens)
    x_data.append(tokens)
  return x_data

x_train = clean_data(train , tokens) #here the tokens are set of tokens(vocabs) that we defined above
x_test = clean_data(test , tokens)
print(x_train[1])

es_x_train = clean_data(s_train , s_tokens) #here the tokens are set of tokens(vocabs) that we defined above
es_x_test = clean_data(s_test , s_tokens)
print(es_x_train[1])

#preprocess label
from numpy import array
from sklearn.preprocessing import OneHotEncoder
def label_preprocess(label): 
  y_temp = []
  for y in label :
    y_temp.append(int(y))
  new_label =array(y_temp)
  #one-hot encoding y_label 
  onehot_encoder = OneHotEncoder(sparse=False)
  new_label = onehot_encoder.fit_transform( new_label.reshape(len(new_label), 1))
  return new_label

y_train = label_preprocess(train_label)
y_test = label_preprocess(test_label)
print(y_train)
print(len(y_train[0]))

es_y_train = label_preprocess(s_train_label)
es_y_test = label_preprocess(s_test_label)
print(es_y_train)
print(len(es_y_train[0]))

#Preprocess x data
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
def x_preprocess(data, max_len  ): 
  # sequence encode
  encoded_docs = tokenizer.texts_to_sequences(data)
  # pad sequences
  max_length = max_len
  data = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
  return data

# define vocabulary size (largest integer value in tokenizer)

max_length = max([len(s.split()) for s in  x_train])
# create the tokenizer
tokenizer = Tokenizer()
# fit the tokenizer on data
tokenizer.fit_on_texts(x_train)  
vocab_size = len(tokenizer.word_index) + 1
print(vocab_size)


s_max_length = max([len(s.split()) for s in  es_x_train])
# create the tokenizer
s_tokenizer = Tokenizer()
# fit the tokenizer on data
s_tokenizer.fit_on_texts(es_x_train)  
es_vocab_size = len(s_tokenizer.word_index) + 1
print(es_vocab_size)

x_train = x_preprocess(x_train, max_length  ) 
x_test = x_preprocess(x_test, max_length  ) 

es_x_train = x_preprocess(es_x_train, max_length  ) 
es_x_test = x_preprocess(es_x_test, max_length  )

#check if size match
print(x_train.shape)
print(len(y_train))
print(x_test.shape)
print(len(y_test))

#check if size match
print(es_x_train.shape)
print(len(es_y_train))
print(es_x_test.shape)
print(len(es_y_test))

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.optimizers import SGD

# define model
from keras.layers import Dropout
model = Sequential()
model.add(Embedding(vocab_size, 100, input_length=max_length))
model.add(Conv1D(filters=32, kernel_size=4, activation='relu')) #4
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dropout(0.4))
model.add(Dense(20, activation='softmax'))
print(model.summary())
# compile network
opt = SGD(lr=0.01, momentum=0.9)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# fit network
model.fit(x_train, y_train, epochs=10, verbose=1)

# define spanish model
from keras.layers import Dropout
s_model = Sequential()
s_model.add(Embedding(vocab_size, 100, input_length=max_length))
s_model.add(Conv1D(filters=32, kernel_size=4, activation='relu')) #4
s_model.add(MaxPooling1D(pool_size=2))
s_model.add(Flatten())
s_model.add(Dropout(0.4))
s_model.add(Dense(19, activation='softmax'))
print(s_model.summary())
# compile network
opt = SGD(lr=0.01, momentum=0.9)
s_model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# Spanish fit network
s_model.fit(es_x_train, es_y_train, epochs=10, verbose=1)
# es_x_train.shape()

# Model evaluate
loss, acc = model.evaluate(x_test, y_test, verbose=1)
print('Test Accuracy: %f' % (acc*100))

# Spanish Model evaluate
loss, acc = s_model.evaluate(es_x_test, es_y_test, verbose=1)
print('Test Accuracy: %f' % (acc*100))

predictions = model.predict(x_test)
predictions

es_predictions = s_model.predict(es_x_test)
es_predictions

emojis = {
0:	'❤',
1:	'😍',
2:	'😂',
3:	'💕',
4:	'🔥',
5:	'😊',	
6:	'😎',
7:	'✨',
8:	'💙',	
9:	'😘',
10:	'📷',
11:	'🇺🇸',
12:	'☀',
13:	'💜',
14:	'😉',	
15:	'💯',	
16:	'😁',
17:	'🎄',	
18:	'📸',
19:	'😜'
}

s_emojis = {
    0:	'❤',
    1:	'😍',	
    2:	'😂',		
    3:	'💕',	
    4:	'🔥',
    5:	'😊',
    6: '😎',
    7:	'✨',
    8:	'💙',
    9:	'😘',
    10:	'📷',	
    11:	'🇺🇸',
    12:	'☀',
    13:	'💜',
    14:	'😉',	
    15:	'💯',
    16:	'😁',
    17:	'🎄',	
    18:	'📸',
    19:	'😜'	
}

datasize =[0]*20
for index in range(len(y_train)):
  emoji_num = y_train [index].tolist().index(1.0)
  datasize[emoji_num ] +=1
print(datasize)

s_datasize =[0]*19
for index in range(len(es_y_train)):
  es_emoji_num = es_y_train [index].tolist().index(1.0)
  s_datasize[es_emoji_num ] +=1
print(s_datasize)

"""
define seperate test dataset for each emoji 
x_test, y_test 
"""



test_by_label_x = [[],[],[],[],[],[], [], [], [], [],[],[],[],[],[],[], [], [], [], [] ]
test_by_label_y = [[],[],[],[],[],[], [], [], [], [],[],[],[],[],[],[], [], [], [], [] ]
def seperate_each_emoji (x , y ): 
  for i in range(len(y )): 
    emoji_num = y [i].tolist().index(1.0)
    test_by_label_x[emoji_num].append(x [i].tolist())
    test_by_label_y[emoji_num].append(y [i].tolist())

x_size = []
y_acc = []

def test_each_emoji(): 
  for j in range(20): #total 20 emojis
    x_test_j = array(test_by_label_x[j])
    y_test_j = array(test_by_label_y[j])
    loss, acc = model.evaluate(x_test_j, y_test_j, verbose=0)
    print('Emoji ',emojis[j], '  Test Accuracy: %f' % (acc*100) ,  "     Training data size: ", datasize[j])
    x_size.append(datasize[j])
    y_acc.append(acc*100)

seperate_each_emoji(x_test , y_test )
test_each_emoji()
print(x_size)
print(y_acc)

"""
Spanish!
define seperate test dataset for each emoji 
es_x_test, es_y_test 
"""



s_test_by_label_x = [[],[],[],[],[],[], [], [], [], [],[],[],[],[],[],[], [], [], [] ]
s_test_by_label_y = [[],[],[],[],[],[], [], [], [], [],[],[],[],[],[],[], [], [], [] ]
def seperate_each_emoji (x , y ): 
  for i in range(len(y )): 
    es_emoji_num = y [i].tolist().index(1.0)
    s_test_by_label_x[es_emoji_num].append(x [i].tolist())
    s_test_by_label_y[es_emoji_num].append(y [i].tolist())

s_x_size = []
s_y_acc = []

def test_each_emoji(): 
  for j in range(19): #total 19 emojis
    s_x_test_j = array(s_test_by_label_x[j])
    s_y_test_j = array(s_test_by_label_y[j])
    loss, acc = s_model.evaluate(s_x_test_j, s_y_test_j, verbose=0)
    print('Emoji ',s_emojis[j], '  Test Accuracy: %f' % (acc*100) ,  "     Training data size: ", s_datasize[j])
    s_x_size.append(s_datasize[j])
    s_y_acc.append(acc*100)

seperate_each_emoji(es_x_test , es_y_test )
test_each_emoji()
print(s_x_size)
print(s_y_acc)

import pprint
from IPython.display import clear_output 



while True:
  sentence = input('Enter a tweet: ')
  clear_output()
  train = clean_data([sentence] , tokens)
  x_train = x_preprocess(train, max_length)
  prediction = model.predict(x_train)[0]
  m = 0
  m_i = 0
  # find max predicted value
  for i in range(len(prediction)):
    if prediction[i] > m:
      m = prediction[i]
      m_i = i
  emojis_predicted = {emojis[i]: prediction[i] for i in range(len(prediction))}
  sorted_emojis = sorted(emojis_predicted.items(), key=lambda kv: -kv[1])
  print(f'Predicted Tweet: {sentence} {emojis[m_i]}')
  print('Top emoji predictions:')
  for emoji, pred  in sorted_emojis:
    print(f'{emoji}: {"{:.2f}".format(pred * 100)}%')