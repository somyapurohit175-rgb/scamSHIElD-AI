import string
import pickle
import streamlit as st

st.title("Job Scam detector.")

st.write("Paste recived job/internship mail or text below:")

user_input = st.text_area("Enter job description:")


# connecting ML model with streamlit

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# adding logic for app running


def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


if st.button("Check Scam"):
    st.write("Processing...")
    cleaned = clean_text(user_input)

    vectorized = vectorizer.transform([cleaned])

    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0][1]


# for output
    if prediction == 1:
        st.error(f"⚠️ Scam Detected ({probability*100:.2f}% confidence)")
    else:
        st.success(f"✅ Looks Legit ({(1-probability)*100:.2f}% confidence)")

    scam_words = ["fee", "payment", "urgent", "limited", "no interview"]

    found = [word for word in scam_words if word in cleaned]

    if found:
        st.write("⚠️ Suspicious words found:")
        for word in found:
            st.write(f"- {word}")
