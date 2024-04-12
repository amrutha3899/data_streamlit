import streamlit as st
import pandas as pd
from functools import reduce

# Load data from CSV
@st.cache_data
def load_data():
    return pd.read_csv("complete_data.csv")

def get_subcategories(category):
    subcategories = {
        'Physical': ['Trauma', 'Physical Labor', 'Illness', 'Dietary Stress'],
        'Psychological': ['Emotional Stress', 'Cognitive Stress', 'Perceptual Stress'],
        'Psychosocial': ['Relationships', 'Lack of Social Support', 'Financial Stress'],
        'Psychospiritual': ['Values of Life', 'Purpose of Living', 'Joyless Striving', 'Loss of Faith']
    }
    return subcategories.get(category, [])

# Function to filter data based on selected category and sub-category
def filter_data(data, category, sub_category, type):
    filtered_data = data.copy()
    conditions = []
    if category:
        conditions.append(filtered_data['Category'] == category)
    if sub_category:
        conditions.append(filtered_data['Sub_category'] == sub_category)
    if type:
        conditions.append(filtered_data['type'] == type)
    if conditions:
        filtered_data = filtered_data[reduce(lambda x, y: x & y, conditions)]
    return filtered_data

# Function to display conversation in a flash card-like box with scrollability
def display_conversation(conversations):
    idx = st.session_state.get("conversation_index", 0)
    if idx < 0:
        idx = 0
    if idx >= len(conversations):
        idx = len(conversations) - 1

    # Display conversation box with scrollability
    with st.expander(f"Conversation {idx + 1}", expanded=False):
        for line in conversations.iloc[idx][0].split("\n"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                speaker, message = parts
                st.markdown(f"**{speaker.strip()}**: {message.strip()}")
            elif len(parts) == 1:
                st.markdown(f"**{parts[0].strip()}**")

    # Arrow buttons for navigation
    col1, col2, col3 = st.columns([5, 8, 2])
    if col1.button("← Previous", key="prev_button") and idx > 0:
        idx -= 1
    if col3.button("Next →", key="next_button") and idx < len(conversations) - 1:
        idx += 1

    st.session_state["conversation_index"] = idx


# Main function
def main():
    # Load data
    data = load_data()

    # Initialize conversation_filters if not set
    if "conversation_filters" not in st.session_state:
        st.session_state.conversation_filters = ("", "", "")

    # Sidebar filters
    st.sidebar.title("Filters")
    category = st.sidebar.selectbox("Category", [""] + data['Category'].unique())
    sub_category = st.sidebar.selectbox("Sub-category", [""] + get_subcategories(category))
    type = st.sidebar.selectbox("Type", [""] + data['type'].unique())

    # Filter data based on selected filters
    filtered_data = filter_data(data, category, sub_category, type)

    # Reset conversation index when filters change
    if st.session_state.conversation_filters != (category, sub_category, type):
        st.session_state["conversation_index"] = 0
        st.session_state.conversation_filters = (category, sub_category, type)

    # Display filtered conversations
    if not filtered_data.empty:
        st.title("Mental Health Simulated Data")
        conversations = pd.DataFrame(filtered_data['generated_conversation'])
        display_conversation(conversations)
    else:
        st.error("No conversations found for selected filters.")

    # Add the description box
    # Add the description box with reduced size and spacing between lines
    st.sidebar.markdown("<h3 style='margin-bottom: 5px;'>Description</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='font-size: 12px; margin-bottom: 5px;'><b>desc</b>: Description of the doctor and the patient.</p>",
        unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='font-size: 12px; margin-bottom: 5px;'><b>tax_description</b>: Description of the taxonomy categories</p>",
        unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='font-size: 12px; margin-bottom: 5px;'><b>pattern</b>: Flow of the conversation: small talk, consultation, end of conversation.</p>",
        unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='font-size: 12px; margin-bottom: 5px;'><b>res:</b> Patients are resistant to share how they feel.</p>",
        unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='font-size: 12px; margin-bottom: 5px;'><b>examples</b>: Couple of real-world examples</p>",
        unsafe_allow_html=True)
    st.sidebar.markdown(
        "<p style='font-size: 12px; margin-bottom: 5px;'><b>followup</b>: Ending the conversation by setting up an appointment for the next meeting.</p>",
        unsafe_allow_html=True)


if __name__ == "__main__":
    main()
