from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm 				     import SVC

"""
This script implements the solution to the "Document Classification" problem 
from HackerRank https://www.hackerrank.com/challenges/document-classification 
"""

with open("trainingdata.txt", "r") as f:
	txt = f.read()

lines = txt.split("\n")

"""
This function will process a line of input splitting the text label 
from the text 
"""
def process_line(line):
	i = line.index(" ")
	return (line[i:], int(line[0:i]))

# Process in the input text into test and train sets. 
dataset = list(map(process_line, lines[ 1 : int(lines[0]) ]))
[X_test_raw, Y_test]   = zip(*dataset[0:400])
[X_train_raw, Y_train] = zip(*dataset[400:])

# Get the bag of words vectors 
vectorizer = CountVectorizer(min_df=1)
X_train    = vectorizer.fit_transform(X_train_raw)
X_test     = vectorizer.transform(X_test_raw)

# Train a support vector machine to do the classification. 
model = SVC()
model.fit(X_train, Y_train)

print("Train score:" + str(model.score(X_train, Y_train)))
print("Test score:"  + str(model.score(X_test, Y_test)))