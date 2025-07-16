import streamlit as st
import random
import os

# Import your custom modules
import chatbot  
import simulator 
# Set Streamlit page configuration
st.set_page_config(page_title="MoneyMentor App", layout="centered")

st.title("💰 MoneyMentor: Your Financial Buddy! 🚀")

# Sidebar for navigation
st.sidebar.title("Choose Your Adventure")
app_mode = st.sidebar.radio(
    "Select a feature:",
    ["Chat with MoneyMentor", "Financial Simulation"]
)

# --- Chatbot Interface ---
if app_mode == "Chat with MoneyMentor":
    st.header("Chat with MoneyMentor 💬")
    st.write("Hey, what's good? MoneyMentor here! Ask me anything about managing your bread.")

    # Initialize chat history in session state if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat messages from history
    for human_msg, ai_msg in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(human_msg)
        with st.chat_message("assistant"):
            st.write(ai_msg)

    # Input for new user message
    user_query = st.chat_input("Ask MoneyMentor...")

    if user_query:
        # Display user message
        with st.chat_message("user"):
            st.write(user_query)
        
        # Get AI response using the refactored chatbot function
        with st.chat_message("assistant"):
            with st.spinner("MoneyMentor is cooking up a response..."):
                # Call the chatbot's response function
                ai_response = chatbot.get_chatbot_response(user_query, st.session_state.chat_history)
                st.write(ai_response)
        
        # Update chat history
        st.session_state.chat_history.append((user_query, ai_response))
        # Rerun to ensure chat history updates visually immediately
        st.rerun()

# --- Financial Simulation Interface ---
elif app_mode == "Financial Simulation":
    st.header("Financial Simulation Challenge 🎮")
    st.write("Test your money smarts by choosing the best option for each scenario. Let's get that financial glow-up!")
    
    # Initialize simulation state if not already present
    if 'simulation_state' not in st.session_state:
        st.session_state.simulation_state = {
            'scenarios': [], # Will be loaded from simulator.py
            'current_scenario_index': 0,
            'user_score': 0,
            'scenarios_completed': 0,
            'feedback_message': "",
            'show_feedback': False,
            'choice_made': False # To track if a choice has been made for the current scenario
        }
        # Load scenarios only once when simulation starts or restarts
        loaded_scenarios = simulator.load_scenarios(simulator.SCENARIOS_FILE)
        if loaded_scenarios:
            random.shuffle(loaded_scenarios) # Shuffle a copy
            st.session_state.simulation_state['scenarios'] = loaded_scenarios
        else:
            st.error("No scenarios loaded for the simulation. Please check the 'data/sim_scenarios_fixed.csv' file.")

    state = st.session_state.simulation_state

    # Check if there are scenarios to play
    if not state['scenarios']:
        st.warning("No simulation scenarios are available. Please ensure your `data/sim_scenarios_fixed.csv` file is correctly configured.")
    elif state['current_scenario_index'] < len(state['scenarios']):
        # Display current scenario
        scenario = state['scenarios'][state['current_scenario_index']]
        st.subheader(f"--- Scenario #{scenario.id} ---")
        st.write(scenario.scenario_text)

        # Use st.radio for choices, only if a choice hasn't been made yet for this scenario
        if not state['choice_made']:
            user_choice_raw = st.radio(
                "Choose your option:",
                options=[f"A) {scenario.option_a}", f"B) {scenario.option_b}"],
                index=None, # No default selection
                key=f"scenario_{scenario.id}_radio" # Unique key for each radio button
            )

            if user_choice_raw:
                chosen_option_letter = user_choice_raw[0] # Extract 'A' or 'B'
                
                is_correct, feedback_message = scenario.get_feedback(chosen_option_letter)
                state['feedback_message'] = feedback_message
                state['show_feedback'] = True
                state['choice_made'] = True # Mark that a choice has been made

                if is_correct:
                    state['user_score'] += 1
                    st.success(f"✅ Correct! {state['feedback_message']}")
                else:
                    st.error(f"❌ Oops! {state['feedback_message']}")
                
                state['scenarios_completed'] += 1
                st.write(f"Current Score: {state['user_score']} out of {state['scenarios_completed']}")
                
                # Use a button to advance to the next scenario
                if st.button("Next Scenario", key=f"next_button_{scenario.id}"):
                    state['current_scenario_index'] += 1
                    state['show_feedback'] = False
                    state['choice_made'] = False # Reset for the next scenario
                    st.rerun() # Rerun to show next scenario or end screen
                else:
                    # If button not clicked yet, keep showing feedback and score
                    pass 
        else:
            # If choice was already made, just show feedback and next button
            if state['last_was_correct'] if 'last_was_correct' in state else False: # Check if last_was_correct exists
                st.success(f"✅ Correct! {state['feedback_message']}")
            else:
                st.error(f"❌ Oops! {state['feedback_message']}")
            
            st.write(f"Current Score: {state['user_score']} out of {state['scenarios_completed']}")
            
            if st.button("Next Scenario", key=f"next_button_{scenario.id}"):
                state['current_scenario_index'] += 1
                state['show_feedback'] = False
                state['choice_made'] = False
                st.rerun()

    else:
        # Simulation is over
        st.header("--- Simulation Over ---")
        st.write(f"You completed {state['scenarios_completed']} scenarios.")
        st.write(f"Your final score: {state['user_score']} correct out of {state['scenarios_completed']} attempts.")
        if state['scenarios_completed'] > 0:
            percentage = (state['user_score'] / state['scenarios_completed']) * 100
            st.write(f"That's {percentage:.2f}% accuracy! Keep learning, you got this!")
        else:
            st.write("No scenarios were played.")
        
        if st.button("Restart Simulation"):
            del st.session_state.simulation_state # Clear the state to restart from scratch
            st.rerun()