import streamlit as st

# Define the questions, choices, and correct answers
questions = [
    "What is Marielle's last name?",
    "What is the capital of France?",
    "Which is a prime number?"
]

choices = [
    ["A: Stulens", "B: Fernandez", "C: Johnson"],
    ["A: Berlin", "B: Madrid", "C: Paris"],
    ["A: 4", "B: 7", "C: 9"]
]

correct_answers = {"A": "Stulens", "C": "Paris", "B": "7"}  # Maps letter choices to full answers

# Initialize session state variables
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "progress_timeline" not in st.session_state:
    st.session_state.progress_timeline = []  # Stores correct answer history
if "wrong_answer" not in st.session_state:
    st.session_state.wrong_answer = False  # Tracks when a wrong answer is clicked

def check_answer(answer, full_answer):
    """Check if the selected answer is correct."""
    if answer in correct_answers and full_answer == correct_answers[answer]:  # Correct answer
        st.session_state.progress_timeline.append(
            f"<span style='color:green;'>✅ {questions[st.session_state.current_step]} - {full_answer}</span>"
        )
        st.session_state.current_step += 1
        st.session_state.wrong_answer = False  # Reset wrong answer state
        if st.session_state.current_step == len(questions):  # If finished
            st.session_state.game_over = True
    else:  # Wrong answer: Show restart button
        st.session_state.wrong_answer = True

# UI
st.title("The mystery of the leaking bottles")

# Progress Bar
progress = (st.session_state.current_step / len(questions)) if len(questions) > 0 else 0
st.progress(progress)

if st.session_state.wrong_answer:
    st.error("❌ Wrong answer! Click 'Restart' to try again.")
    if st.button("Restart"):
        st.session_state.current_step = 0
        st.session_state.progress_timeline = []
        st.session_state.game_over = False
        st.session_state.wrong_answer = False
        st.rerun()

elif st.session_state.game_over:
    st.success("🎉 Congratulations! You completed the game!")
    if st.button("Restart"):
        st.session_state.current_step = 0
        st.session_state.progress_timeline = []
        st.session_state.game_over = False
        st.session_state.wrong_answer = False
        st.rerun()

else:
    # Show current question
    st.subheader(f"Question {st.session_state.current_step + 1}:")
    st.write(questions[st.session_state.current_step])

    # Display choices as buttons
    for option in choices[st.session_state.current_step]:
        answer_letter = option[0]  # Extract A, B, C
        full_answer = option[3:]   # Extract full answer (e.g., "4" from "A: 4")
        if st.button(option, key=option):
            check_answer(answer_letter, full_answer)  
            st.rerun()

# Show progress timeline
st.subheader("Your Progress:")
if st.session_state.progress_timeline:
    timeline = "<br>".join(st.session_state.progress_timeline)
    st.markdown(timeline, unsafe_allow_html=True)
else:
    st.markdown("_No progress yet. Start answering!_")
