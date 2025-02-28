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
    "Why was the bottle leaking?",
    "Which material was causing the leak?",
    "What's wrong with the trigger?",
    "Let's find the root cause... Which part of the trigger was causing the failure? Clue: Triggers were airshipped from China.",
    "Why did the valve shrink?",
    "Where did it suffer from excessive heat?",
    "In which airport? it was very hot...?",
    "Knowing further airshippments are needed to protect the launch, what was the solution?"
]

choices = [
    ["A: Materials", "B: People", "C: Methods", "D: Equipment"],
    ["A: Bottle", "B: Handling of the bottle", "C: Trigger", "D: Handling of the trigger"],
    ["A: Design issue", "B: Assembly mistake of the trigger parts", "C: Product-packaging compatibility issue", "D: Component failure"],
    ["A: Housing", "B: Finger Trigger", "C: Valve", "D: Trigger Cap"],
    ["A: Heat", "B: Time", "C: Pressure"],
    ["A: Supplier", "B: CM", "C: During Transit"],
    ["A: Istambul Airport", "B: Shanghai Airport"],
    ["A: Delay the launch for further investigation and successful PQ with new triggers", 
     "B: No adjustments and redo PQ with new triggers", 
     "C: Put heat cover sheets around pallets for new air shipments", 
     "D: Put temperature indicators on pallets for new air shipments", 
     "E: Put heat covers and temperature sensors for new air shipments"],
]

correct_answers = ["A", "C", "D", "C", "A", "C", "B", "E"]

explanations = {
    "A1": "✅ Correct! Something was wrong with the materials!",
    "B1": "❌ Incorrect! Since this is product qualification, the first time people produce the product.",
    "C1": "❌ Incorrect! The methods were correct since the leakers were clear.",
    "D1": "❌ Incorrect! Since some bottles were leaking, but some were not (1/10 leakers).",

    "A2": "❌ Incorrect! Leak is coming out of the bottle.",
    "B2": "❌ Incorrect! Leak is coming out of the bottle.",
    "C2": "✅ Correct! Something was wrong with those triggers!",
    "D2": "❌ Incorrect! Some bottles where leaking but others not!",

    "A3": "❌ Incorrect! The trigger passed all pilot & supplier quality tests.",
    "B3": "❌ Incorrect! There were no errors found on defective product.",
    "C3": "❌ Incorrect! It was tested upfront with successful results.",
    "D3": "✅ Correct! There was one component in the trigger that was failing!",

    "A4": "❌ Incorrect! The housing was well sealed.",
    "B4": "❌ Incorrect! The finger triggers were working correctly.",
    "C4": "✅ Correct! The valve was smaller than it was supposed to be!",
    "D4": "❌ Incorrect! The trigger cap was well sealed.",

    "A5": "✅ Correct! Heat can shrink valves. As it was proven both by P&G and the supplier in a heat room!",
    "B5": "❌ Incorrect! No evidence.",
    "C5": "❌ Incorrect! No evidence.",

    "A6": "❌ Incorrect! No evidence, based on temperature loggers.",
    "B6": "❌ Incorrect! No evidence, based on temperature loggers.",
    "C6": "✅ Incorrect! Based on elimination. Temperature loggers at CM and supplier indicated no excessivee temperature was reached.",

    "A7": "❌ Incorrect! Istambul Airport.",
    "B7": "✅ Correct! Shanghai Airport.",

    "A8": "❌ Incorrect! The launch was too important to delay. Big Home Care bet for FY2425!",
    "B8": "❌ Incorrect! The failure would most likely be reproduced.",
    "C8": "❌ Incorrect! Even if there are heat covers, the real temperature reached cannot be measured without a sensor.",
    "D8": "❌ Incorrect! Not enough since there is no preventive measure to protect from the heat.",
    "E8": "✅ Correct!"
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

def check_answer(answer):
    """Check if the selected answer is correct and provide personalized feedback."""
    question_index = st.session_state.current_step  # Get the current question index
    correct_answer = correct_answers[question_index]
    
    # Generate the key for looking up explanations (e.g., "A2", "B3")
    answer_key = f"{answer}{question_index + 1}"
    feedback = explanations.get(answer_key, "❌ Incorrect! Try again.")

    if answer == correct_answer:  
        st.session_state.progress_timeline.append(f"<span style='color:green;'>{feedback}</span>")
        st.session_state.feedback = feedback
        st.session_state.current_step += 1
        st.session_state.wrong_answer = False
        if st.session_state.current_step == len(questions):
            st.session_state.game_over = True
    else:  
        st.session_state.wrong_answer = True
        st.session_state.feedback = feedback

# Ensure we don't go out of bounds when selecting the image
if st.session_state.current_step < len(question_images):
    current_image = question_images[st.session_state.current_step]
else:
    current_image = default_image  # Default image when game is over

# Display the image
with col1:
    st.image(current_image)
with col3:
    st.image(current_image)

# UI
with col2:
    st.title("The mystery of the leaking bottles")

    # Progress Bar
    progress = (st.session_state.current_step / len(questions)) if len(questions) > 0 else 0

    if st.session_state.wrong_answer:
        st.error(f"{st.session_state.feedback}")  # Show incorrect answer feedback
    elif st.session_state.game_over:
        st.success("🎉 Congratulations! You completed the game!")
    
    if st.session_state.game_over or st.session_state.wrong_answer:
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
            answer_letter = option[0]  # Extract A, B, C, etc.
            if st.button(option, key=option):
                check_answer(answer_letter)
                st.rerun()

    st.subheader("Your Progress:")
    st.progress(progress)
    if st.session_state.progress_timeline:
        timeline = "<br>".join(st.session_state.progress_timeline)
        st.markdown(timeline, unsafe_allow_html=True)
    else:
        st.markdown("_No progress yet. Start answering!_")
