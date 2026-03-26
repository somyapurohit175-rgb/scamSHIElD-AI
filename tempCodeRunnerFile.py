import string

def clean_text(text):
    text = text.lower()  # lowercase
    
    # remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text

X = X.apply(clean_text)
print("data has been clean successfully")
