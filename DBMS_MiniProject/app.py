import streamlit as st
import bcrypt
import re
from admin_functions import add_student, get_all_students, add_mentor, update_project_status, delete_student, get_all_teams, view_deleted_students, create_project, add_team, view_project_evaluation_details
from database import fetch_data, execute_procedure
from display_student_info import display_student_details
from mentor_functions import view_teams_under_mentor, view_project_files, evaluate_project

def initialize_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'page' not in st.session_state:
        st.session_state.page = "home"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def login(email, password, role):
    query = f"SELECT * FROM {role} WHERE Email=%s"
    user_data = fetch_data(query, (email,))

    if user_data:
        user = user_data[0]
        if check_password(password, user['Password']):
            st.session_state.user = user
            st.session_state.logged_in = True
            st.session_state.user['Role'] = role
            
            if role == "Mentor":
                st.session_state.user['ID'] = user['Mentor_ID']  # Store Mentor ID
            elif role == "Student":
                st.session_state.user['ID'] = user['Student_ID']  # Store Student ID
            
            st.success(f"Logged in successfully as {role}")
        else:
            st.error("Incorrect password!")
    else:
        st.error("Invalid email or password!")



def admin_login(email, password):
    admin_email = "admin@123"
    admin_password = "lol"
    if email == admin_email and password == admin_password:
        st.session_state.is_admin = True
        st.session_state.logged_in = True
        st.session_state.user = {'Name': 'Admin', 'Role': 'Admin'}
    else:
        st.error("Invalid admin credentials!")

def sign_in(name, email, password, team_id):
    hashed_password = hash_password(password)
    try:
        execute_procedure("AddStudent", (name, email, hashed_password, team_id))
        st.success("Sign-in successful! You can now log in.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def sign_in_page():
    st.subheader("Sign In")
    name = st.text_input("Name")
    new_email = st.text_input("Email (for Sign In)")
    new_password = st.text_input("Password (for Sign In)", type="password")
    teams = fetch_data("SELECT Team_ID, Team_Name FROM Team")
    team_options = {team["Team_Name"]: team["Team_ID"] for team in teams}
    selected_team_name = st.selectbox("Select Team", list(team_options.keys()))
    team_id = team_options[selected_team_name]
    if st.button("Submit Sign In"):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, new_email):
            st.error("Invalid email format! Please enter a valid email.")
        else:
            sign_in(name, new_email, new_password, team_id)

def main():
    st.title("Capstone Project Manager")
    initialize_session_state()

    if not st.session_state.logged_in:
        st.header("Welcome! Please select your role.")
        selected_section = st.radio("Select the section to login", ("Admin Login", "Mentor/Student Login", "Sign In"))

        if selected_section == "Admin Login":
            admin_email = st.text_input("Admin Email")
            admin_password = st.text_input("Admin Password", type="password")
            if st.button("Login as Admin"):
                admin_login(admin_email, admin_password)

        elif selected_section == "Mentor/Student Login":
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Select Role", ["Student", "Mentor"])
            if st.button("Login"):
                login(email, password, role)

        elif selected_section == "Sign In":
            sign_in_page()

    else:
        st.sidebar.header("Navigation")
        if st.session_state.is_admin:
            handle_admin_dashboard()
        elif st.session_state.user["Role"] == "Student":
            handle_student_dashboard()
        elif st.session_state.user["Role"] == "Mentor":
            handle_mentor_dashboard()

        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.session_state.page = "home"

def handle_admin_dashboard():
    """Admin-specific dashboard navigation and actions."""
    admin_actions = {
        "View All Students": get_all_students,
        "Add Student": add_student,
        "View All Teams": get_all_teams,
        "Add Team": add_team,
        "Add Mentor": add_mentor,
        "Create Project": create_project,
        "Update Project Status": update_project_status,
        "Delete Student": delete_student,
        "View Evaluation Details":view_project_evaluation_details,
        "View Deleted Students": view_deleted_students,
    }

    selected_admin_action = st.sidebar.selectbox("Admin Dashboard", list(admin_actions.keys()))
    admin_actions[selected_admin_action]()



def handle_student_dashboard():
    """Student-specific dashboard navigation and actions."""
    selected_student_action = st.sidebar.selectbox("Student Dashboard", ["Student Details"])
    if selected_student_action == "Student Details":
        display_student_details()

def handle_mentor_dashboard():

    """Mentor-specific dashboard navigation and actions."""
    selected_mentor_action = st.sidebar.selectbox("Mentor Dashboard", ["View All Teams", "View Project Files", "Evaluate Project"])
    if selected_mentor_action == "View All Teams":
        view_teams_under_mentor()
    elif selected_mentor_action == "View Project Files":
        view_project_files()
    elif selected_mentor_action == "Evaluate Project":
        evaluate_project()

if __name__ == "__main__":
    main()
