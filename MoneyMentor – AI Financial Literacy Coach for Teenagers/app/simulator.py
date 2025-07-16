import csv 
import os 
import random
import streamlit as st
# No additional imports or code needed here
SCENARIOS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'sim_scenarios_fixed.csv'))

class Scenario:
    def __init__(self, id, scenario_text, option_a, option_b, correct_option, feedback_correct, feedback_incorrect):
        self.id = id
        self.scenario_text = scenario_text
        self.option_a = option_a
        self.option_b = option_b
        self.correct_option = correct_option
        self.feedback_correct = feedback_correct
        self.feedback_incorrect = feedback_incorrect

    def display(self):
        """Displays the scenario and options to the user."""
        return (
            f"--- Scenario #{self.id} ---\n"
            f"{self.scenario_text}\n"
            f"A) {self.option_a}\n"
            f"B) {self.option_b}"
        )

    def get_feedback(self, user_choice):
        """Returns the appropriate feedback based on the user's choice."""
        if user_choice.upper() == self.correct_option.upper():
            return True, self.feedback_correct
        else:
            return False, self.feedback_incorrect

# --- Helper Functions ---

def load_scenarios(file_path):
    """Loads financial scenarios from a CSV file."""
    scenarios = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                scenario = Scenario(
                    id=int(row['id']),
                    scenario_text=row['scenario_text'],
                    option_a=row['option_a'],
                    option_b=row['option_b'],
                    correct_option=row['correct_option'].strip(),
                    feedback_correct=row['feedback_correct'],
                    feedback_incorrect=row['feedback_incorrect']
                )
                scenarios.append(scenario)
    except FileNotFoundError:
        print(f"Error: Scenarios file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error loading scenarios: {e}")
        return []
    return scenarios

# # We need to adapt run_simulation for Streamlit
# # It should return values or update Streamlit components, not use direct input/print
# def run_simulation_streamlit():
#     scenarios = load_scenarios(SCENARIOS_FILE)
#     if not scenarios:
#         st.error("No scenarios loaded. Exiting simulation.")
#         return

#     if 'simulation_state' not in st.session_state:
#         st.session_state.simulation_state = {
#             'scenarios': random.sample(scenarios, len(scenarios)), # Shuffle a copy
#             'current_scenario_index': 0,
#             'user_score': 0,
#             'scenarios_completed': 0,
#             'feedback_message': "",
#             'show_feedback': False
#         }

#     state = st.session_state.simulation_state

#     if state['current_scenario_index'] < len(state['scenarios']):
#         scenario = state['scenarios'][state['current_scenario_index']]
#         st.write(scenario.display())

#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Option A", key="option_a"):
#                 process_choice(scenario, 'A')
#         with col2:
#             if st.button("Option B", key="option_b"):
#                 process_choice(scenario, 'B')

#         if state['show_feedback']:
#             st.info(state['feedback_message'])
#             st.write(f"Current Score: {state['user_score']} out of {state['scenarios_completed']}")
#             if st.button("Next Scenario", key="next_scenario"):
#                 state['current_scenario_index'] += 1
#                 state['show_feedback'] = False
#                 st.rerun() # Rerun to show next scenario immediately
#     else:
#         st.write("--- Simulation Over ---")
#         st.write(f"You completed {state['scenarios_completed']} scenarios.")
#         st.write(f"Your final score: {state['user_score']} correct out of {state['scenarios_completed']} attempts.")
#         if state['scenarios_completed'] > 0:
#             percentage = (state['user_score'] / state['scenarios_completed']) * 100
#             st.write(f"That's {percentage:.2f}% accuracy! Keep learning, you got this!")
#         else:
#             st.write("No scenarios were played.")
#         if st.button("Restart Simulation"):
#             del st.session_state.simulation_state
#             st.rerun()

# def process_choice(scenario, user_choice):
#     state = st.session_state.simulation_state
#     is_correct, feedback_message = scenario.get_feedback(user_choice)

#     if is_correct:
#         state['user_score'] += 1
#         state['feedback_message'] = f"✅ Correct! {feedback_message}"
#     else:
#         state['feedback_message'] = f"❌ Oops! {feedback_message}"
    
#     state['scenarios_completed'] += 1
#     state['show_feedback'] = True
#     st.rerun() # Rerun to show feedback
