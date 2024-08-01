import streamlit as st

# Initialize chatbot responses
def chatbot_response(user_input):
    return f"You said: {user_input}"

# Function to handle button clicks
def handle_button_click(option, level):
    st.session_state[level] = option
    st.rerun()  # Restart the app to update state

# Function to generate buttons and handle their clicks
def generate_buttons(options, level):
    cols = st.columns(len(options))
    for idx, (col, option) in enumerate(zip(cols, options)):
        if col.button(option, key=f"{level}button{idx}"):
            handle_button_click(option, level)

# Function to handle exit button click for discipline
def handle_exit_discipline():
    st.session_state['discipline'] = None
    st.rerun()  # Restart the app to update state

# Function to handle exit button click for project
def handle_exit_project():
    st.session_state.clear()
    st.session_state['page'] = 'main'
    st.rerun()  # Restart the app to update state

# Function to generate URLs based on input values
def generate_urls(project, discipline, dashboard_name):
    url_mapping = {
        ("gamma", "piping", "test"): {"Google": "https://www.google.com"},
        ("alpha", "electrical", "overview"): {"YouTube": "https://www.youtube.com/"},
        ("beta", "instrument", "details"): {
            "Example Beta Instrument Details": "https://www.youtube.com/",
            "Backup Beta Instrument Details": "https://www.google.com"
        },
        ("delta", "structural", "summary"): {"Example Delta Structural Summary": "https://www.example.com/delta/structural/summary"}
    }
    
    # Normalize input values
    normalized_project = project.strip().lower()
    normalized_discipline = discipline.strip().lower()
    normalized_dashboard_name = dashboard_name.strip().lower()
    
    # Get the URLs from the mapping or return an empty dictionary
    return url_mapping.get((normalized_project, normalized_discipline, normalized_dashboard_name), {})

# Streamlit app
st.title("Dashboard Query ChatBot")

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'
if 'project' not in st.session_state:
    st.session_state['project'] = None
if 'discipline' not in st.session_state:
    st.session_state['discipline'] = None
if 'dashboard_name' not in st.session_state:
    st.session_state['dashboard_name'] = ""

# Main page
if st.session_state['page'] == 'main':
    st.write("Hello! Welcome to the Chatbot. Let's get started.")

    if st.session_state['project'] is None:
        st.write("Please select the PROJECT:")
        project_buttons = ["Alpha", "Beta", "Gamma", "Delta"]
        generate_buttons(project_buttons, 'project')

        st.write("")  # Add a small gap
        project_text = st.text_input("Or enter the project name:")
        if project_text:
            st.session_state['project'] = project_text
            st.rerun()  # Update the app state immediately

    else:
        st.write(f"Selected PROJECT: {st.session_state['project']}")
        if st.button("Change", key="exit_project"):
            handle_exit_project()

    if st.session_state['project'] is not None and st.session_state['discipline'] is None:
        st.write("Please select the Discipline:")
        discipline_buttons = ["ELECTRICAL", "INSTRUMENT", "PIPING", "STRUCTURAL"]
        generate_buttons(discipline_buttons, 'discipline')

        st.write("")  # Add a small gap
        discipline_text = st.text_input("Or enter the discipline name:")
        if discipline_text:
            st.session_state['discipline'] = discipline_text
            st.rerun()  # Update the app state immediately

    else:
        if st.session_state['discipline'] is not None:
            st.write(f"Selected Discipline: {st.session_state['discipline']}")
            if st.button("Change", key="exit_discipline"):
                handle_exit_discipline()

    if st.session_state['project'] is not None and st.session_state['discipline'] is not None:
        st.write("")  # Add a small gap
        dashboard_name = st.text_input("Enter the name of the Dashboard: ", value=st.session_state['dashboard_name'], key="user_input")

        # Handle user input and chatbot response
        if dashboard_name:
            response = chatbot_response(dashboard_name)
            st.write(f"Chatbot: {response}")
            st.session_state['dashboard_name'] = dashboard_name

            st.write("### Collected Values")
            project = st.session_state['project']
            discipline = st.session_state['discipline']
            collected_values = f"The selected project is {project}, the discipline is {discipline}, and the dashboard name is {dashboard_name}."
            st.write(collected_values)

            # Generate and display the URLs
            urls = generate_urls(project, discipline, dashboard_name)
            
            if urls:
                st.write("### Available Links:")
                for name, url in urls.items():
                    st.write(f"[{name}]({url})")
            else:
                st.write("No matching URLs found for the given input.")

            # Exit button to clear session state and restart
            if st.button("New Query", key="exit_final"):
                handle_exit_project()
