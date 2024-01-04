import streamlit as st
import google.generativeai as genai
import PIL.Image
from re import sub

genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro-vision')

st.header("Palm Reader 🔮")
st.subheader("A funny initiative to bring palm reading to the 21st century. Ideated by @anushreekhadye, developed by @piyushchugeja, & powered by Google's Gemini AI.")

question = st.text_input("Ask a question about your life and the AI will answer it based on the readings of your palm.")
submit = st.button("Submit")

if 'palm_image' not in st.session_state:
    st.session_state.palm_image = None


with st.sidebar:
    st.subheader("Upload image")
    file_raw = st.file_uploader("Upload an image of your palm here and click on 'Process'")
    if st.button("Process"):
        with st.spinner("Processing..."):
            try:
                st.session_state.palm_image = PIL.Image.open(file_raw)
                st.success("Done!")
            except:
                st.error("Please upload an image of your palm.")
                st.session_state.palm_image = None

if submit:
    with st.spinner("Processing..."):
        try:
            if question and st.session_state.palm_image:
                prompt = "You are a very wise palm reader. You are being shown a palm. If you cannot see the palm or if there is no palm present in the image, respond with 'I cannot read the palm. Please try later.'. If you can read the palm, then answer the following question: " + question
                # prompt = question + " based on the readings of my palm"
                print(prompt)
                response = model.generate_content(
                    contents = [question, st.session_state.palm_image]
                )
                st.success(sub(r'(?<=\w)([A-Z])', r' \1', response.text))
            elif not question:
                st.error("Please ask a question.")
            elif not st.session_state.palm_image:
                st.error("Please upload an image of your palm.")
        except Exception as e:
            print(e)
            st.error("Something went wrong. Please try again.")