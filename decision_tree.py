import streamlit as st

st.set_page_config(
    page_title="Kahlo Game",
    page_icon="https://upload.wikimedia.org/wikipedia/en/5/59/Fairy_logo.png",
    layout="wide"
)

# Image list corresponding to each question
question_images = ["pic1.png", "pic3.jpeg", "pic1.png"]
default_image = "pic3.jpeg"  # Image to show when game is completed

col1, col2, col3 = st.columns([0.33, 0.33, 0.33], gap="large")

# Define questions, choices, correct answers, and explanations
questions = [
    "Why was the bottle leaking??",
    "Which material was causing the leak?",
    "What's wrong with the trigger?"
]

choices = [
    ["A: Materials", "B: People", "C: Methods", "D: Equipment"],
    ["A: Bottle", "B: Handling of the bottle", "C: Trigger", "D: Handling of the trigger"],
    ["A: Design issue", "B: Assembly mistake of the trigger parts", "C: Product-packaging compatability issue", "D: Component failure"]
]

correct_answers = {"A": "Materials", "C": "Trigger", "D": "Component failure"}

explanations = {
    "A": "✅ Correct! Something was wrong with the materials.",
    "B": "❌ Incorrect! Since this is product qualification, the first time people produce the product",
    "C": "❌ Incorrect! The methods were correct since the leakers were clear",
    "D": "❌ Incorrect! Since some bottles were leaking, but some were not (1/10 leakers)",
    
    "A2": "❌ Incorrect! Leak is coming out of the bottle.",
    "B2": "❌ Incorrect! Leak is coming out of the bottle.",
    "C2": "✅ Correct! Something was wrong with those triggers!",
    "D2": "❌ Incorrect! Some bottles where leaking but others not!",
    
    "A3": "❌ Incorrect! The trigger passed all pilot & supplier quality tests.",
    "B3": "❌ Incorrect! There were no errors found on defective product.",
    "C3": "❌ Incorrect! It was tested upfront with successful results.",
    "D3": "✅ Correct! The valve was smaller than it was supposed to be!."
}

# Initialize session state variables
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "progress_timeline" not in st.session_state:
    st.session_state.progress_timeline = []
if "wrong_answer" not in st.session_state:
    st.session_state.wrong_answer = False
if "feedback" not in st.session_state:
    st.session_state.feedback = ""  # Stores personalized feedback

def check_answer(answer, full_answer):
    """Check if the selected answer is correct and provide personalized feedback."""
    question_index = st.session_state.current_step  # Get the current question index

    # Construct a key for explanation lookup (e.g., "A2" for Question 2, Answer A)
    explanation_key = answer if question_index == 0 else f"{answer}{question_index + 1}"

    if answer in correct_answers and full_answer == correct_answers[answer]:  
        st.session_state.progress_timeline.append(
            f"<span style='color:green;'>{explanations[explanation_key]}</span>"
        )
        st.session_state.feedback = explanations[explanation_key]  # Set feedback message
        st.session_state.current_step += 1
        st.session_state.wrong_answer = False
        if st.session_state.current_step == len(questions):
            st.session_state.game_over = True
    else:  
        st.session_state.wrong_answer = True
        st.session_state.feedback = explanations[explanation_key]  # Set wrong answer feedback

# Ensure we don't go out of bounds when selecting the image
if st.session_state.current_step < len(question_images):
    current_image = question_images[st.session_state.current_step]
else:
    current_image = default_image  # Default image when game is over

# Display the image in col1 and col3 if possible, otherwise in col2
if col1 and col3:
    with col1:
        st.image(current_image)
    with col3:
        st.image(current_image)
else:
    with col2:
        st.image(current_image)

# UI
with col2:
    st.title("The mystery of the leaking bottles")

    # Progress Bar
    progress = (st.session_state.current_step / len(questions)) if len(questions) > 0 else 0

    if st.session_state.wrong_answer:
        st.error(f"{st.session_state.feedback}")  # Show personalized wrong answer message
        if st.button("Restart"):
            st.session_state.current_step = 0
            st.session_state.progress_timeline = []
            st.session_state.game_over = False
            st.session_state.wrong_answer = False
            st.session_state.feedback = ""
            st.rerun()

    elif st.session_state.game_over:
        st.success("🎉 Congratulations! You completed the game!")
        if st.button("Restart"):
            st.session_state.current_step = 0
            st.session_state.progress_timeline = []
            st.session_state.game_over = False
            st.session_state.wrong_answer = False
            st.session_state.feedback = ""
            st.rerun()

    else:
        st.subheader(f"Question {st.session_state.current_step + 1}:")
        st.write(questions[st.session_state.current_step])

        for option in choices[st.session_state.current_step]:
            answer_letter = option[0]  # Extract A, B, C
            full_answer = option[3:]   # Extract full answer (e.g., "4" from "A: 4")
            if st.button(option, key=option):
                check_answer(answer_letter, full_answer)
                st.rerun()

    # # Show feedback when the answer is correct
    # if not st.session_state.wrong_answer and st.session_state.feedback:
    #     st.success(st.session_state.feedback)

    st.subheader("Your Progress:")
    st.progress(progress)
    if st.session_state.progress_timeline:
        timeline = "<br>".join(st.session_state.progress_timeline)
        st.markdown(timeline, unsafe_allow_html=True)
    else:
        st.markdown("_No progress yet. Start answering!_")
