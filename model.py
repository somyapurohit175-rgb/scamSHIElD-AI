import pandas as pd

data = pd.read_csv("main_data.csv")
print("data has been read successfully")

# read first 5 line only
print(data.head())

X = data['text']  # input
y = data['label'] # output


import string

def clean_text(text):
    text = text.lower()  # lowercase
    
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text

X = X.apply(clean_text)
print("data has been clean successfully")


# train and testing
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("training and testing has been started.")


# importin TF-IDF vectorizer for text to number changeing
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)   # 👈 THIS LINE IS IMPORTANT
print("data has start to change")





#train our model with logist regression(ml model)
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)
print("we are traing your model.")

# check the accuracy
accuracy = model.score(X_test_vec, y_test)

print("recoded accuracy : ", accuracy)

# check wrong prediction
y_pred = model.predict(X_test_vec)

for i in range(len(y_test)):
    if y_test.iloc[i] != y_pred[i]:
        print("TEXT:", X_test.iloc[i])
        print("ACTUAL:", y_test.iloc[i], "PREDICTED:", y_pred[i])
        print()


# saving files
import pickle

# Save model
pickle.dump(model, open("model.pkl", "wb"))

# Save vectorizer
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model and vectorizer saved successfully!")