import streamlit as st
import requests
import time

st.set_page_config(page_title="WordBlitzML", layout="centered")
st.title("🧠 WordBlitzML - Word Prediction Game")

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if st.button("Start New Game"):
    try:
        res = requests.get("http://127.0.0.1:8000/start_game")

        if res.status_code == 200:
            data = res.json()
            st.session_state.true_word = data.get('true_word', '')
            st.session_state.masked = data.get('word', '')
            st.session_state.length = data.get('length', 0)
            st.session_state.freq = data.get('frequency', 0.0)
            st.session_state.hints = 0
            st.session_state.start_time = time.time()
            st.success("New game started!")
        else:
            st.error("Failed to start game. Backend did not return 200 OK.")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")

if 'masked' in st.session_state:
    st.write(f"🔤 Guess the word: `{st.session_state.masked}`")

    guess = st.text_input("💭 Your Guess:")

    if st.button("Submit Guess"):
        if guess.lower() == st.session_state.true_word.lower():
            time_taken = time.time() - st.session_state.start_time
            payload = {
                "hints_used": st.session_state.hints,
                "time_taken": time_taken,
                "word_length": st.session_state.length,
                "word_frequency": st.session_state.freq
            }

            try:
                pred = requests.post("http://127.0.0.1:8000/predict_difficulty", json=payload).json()
                st.success(f"✅ Correct! Predicted difficulty: `{pred['predicted_difficulty']}`")
            except Exception as e:
                st.error(f"Error predicting difficulty: {e}")
        else:
            st.error("❌ Wrong guess! Try again.")

    if st.button("Get Hint"):
        st.session_state.hints += 1
        st.info(f"🧠 Hint #{st.session_state.hints}: The first letter is `{st.session_state.true_word[0]}`")
