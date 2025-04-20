
import streamlit as st
import requests
import time

st.title("🧠 WordBlitzML - Word Prediction Game")

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if st.button("Start New Game"):
    res = requests.get("http://127.0.0.1:8000/start_game").json()
    st.session_state.true_word = res['true_word']
    st.session_state.masked = res['word']
    st.session_state.length = res['length']
    st.session_state.freq = res['frequency']
    st.session_state.hints = 0
    st.session_state.start_time = time.time()

if 'masked' in st.session_state:
    st.write(f"Guess the word: {st.session_state.masked}")
    guess = st.text_input("Your Guess:")
    if st.button("Submit Guess"):
        if guess.lower() == st.session_state.true_word:
            time_taken = time.time() - st.session_state.start_time
            payload = {
                "hints_used": st.session_state.hints,
                "time_taken": time_taken,
                "word_length": st.session_state.length,
                "word_frequency": st.session_state.freq
            }
            pred = requests.post("http://localhost:8000/predict_difficulty", json=payload).json()
            st.success(f"Correct! Predicted difficulty: {pred['predicted_difficulty']}")
        else:
            st.error("Wrong guess!")

    if st.button("Get Hint"):
        st.session_state.hints += 1
        st.info(f"Hint {st.session_state.hints}: First letter is '{st.session_state.true_word[0]}'")
