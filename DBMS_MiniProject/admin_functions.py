from database import execute_procedure, fetch_data
import streamlit as st
import re
import bcrypt
import pandas as pd

def hash_password(password):
    '''Hash the password using bcrypt'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def add_student():
    '''Handles adding a student'''
    st.subheader("Add Student")
    name = st.text_input("Student Name")
    email = st.text_input("Student Email")
    password = st.text_input("Student Password", type="password")
    teams = fetch_data("SELECT Team_ID, Team_Name FROM Team;")
    
    if teams:
        team_names = [team['Team_Name'] for team in teams]
        selected_team_name = st.selectbox("Select Team", team_names)
        selected_team = next(team for team in teams if team['Team_Name'] == selected_team_name)
        team_id = selected_team['Team_ID']
        
        if name and email and password:
            st.warning("Please review before adding the student to the team.")
        
        if st.button("Add Student"):
            if name and email and password:
                try:
                    hashed_password = hash_password(password)
                    execute_procedure("AddStudent", (name, email, hashed_password, team_id))
                    st.success(f"Student '{name}' added successfully and assigned to team '{selected_team_name}'.")
                except Exception as e:
                    st.error(f"An error occurred while adding the student: {e}")
            else:
                st.error("Please fill in all fields.")
    else:
        st.write("No teams found.")



def add_mentor():
    '''Handles adding a mentor'''
    st.subheader("Add Mentor")
    name = st.text_input("Mentor Name")
    email = st.text_input("Mentor Email")
    password = st.text_input("Mentor Password", type="password")
    departments = ["CSE", "ECE", "EEE", "MECH", "AIML"]
    department = st.selectbox("Department", departments)
    if email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        st.error("Invalid email format.")
    if name and email and password and department:
        st.warning("Please review before adding the mentor.")
    if st.button("Add Mentor"):
        if name and email and password and department:
            try:
                hashed_password = hash_password(password)
                execute_procedure("AddMentor", (name, email, hashed_password, department))
                st.success("Mentor added successfully.")
            except Exception as e:
                st.error(f"An error occurred while adding mentor: {e}")
        else:
            st.error("Please fill in all fields.")

def delete_student():
    ''' Handles deleting a student '''
    st.subheader("Delete Student")
    students = fetch_data("SELECT Student_ID, Name FROM Student;")
    if students:
        student_names = [student['Name'] for student in students]
        selected_student_name = st.selectbox("Select a Student to Delete", student_names)
        selected_student = next(student for student in students if student['Name'] == selected_student_name)
        student_id = selected_student['Student_ID']
        st.warning(f"Review before deleting student '{selected_student_name}'!")
        if st.button(f"Delete the Student '{selected_student_name}'?"):
            try:
                execute_procedure("DeleteStudent", (student_id,))
                st.success(f"Student '{selected_student_name}' marked as deleted successfully.")
            except Exception as e:
                st.error(f"An error occurred while deleting student: {e}")
    else:
        st.write("No students found.")

def update_project_status():
    '''Handles updating project status '''
    st.subheader("Update Project Status")
    projects = fetch_data("SELECT Project_ID, Project_Name FROM Project;")
    if projects:
        project_names = [project['Project_Name'] for project in projects]
        selected_project_name = st.selectbox("Select a Project", project_names)
        selected_project = next(project for project in projects if project['Project_Name'] == selected_project_name)
        project_id = selected_project['Project_ID']
        current_status = fetch_data("SELECT Status FROM Project WHERE Project_ID = %s;", (project_id,))
        if current_status:
            st.write(f"Current Status: {current_status[0]['Status']}")
        status = st.selectbox("Project Status", ["Not Started", "In Progress", "Completed"], index=["Not Started", "In Progress", "Completed"].index(current_status[0]['Status']))
        st.warning(f"Please review before updating project status to '{status}'.")
        if st.button("Update Status"):
            if project_id and status:
                try:
                    execute_procedure("update_project_status", (project_id, status))
                    st.success("Project status updated successfully.")
                except Exception as e:
                    st.error(f"An error occurred while updating project status: {e}")
            else:
                st.error("Please provide valid Project ID and Status.")
    else:
        st.write("No projects found.")

def add_team():
    ''' Handles adding a new team '''
    st.subheader("Add Team")
    team_name = st.text_input("Team Name")
    mentors = fetch_data("SELECT Mentor_ID, Name FROM Mentor;")
    if mentors:
        mentor_names = [mentor['Name'] for mentor in mentors]
        selected_mentor_name = st.selectbox("Assign a Mentor", mentor_names)
        selected_mentor = next(mentor for mentor in mentors if mentor['Name'] == selected_mentor_name)
        mentor_id = selected_mentor['Mentor_ID']
    else:
        st.write("No mentors available. Please add mentors before creating a team.")
        return
    if team_name and mentor_id:
        st.warning(f"Please review before adding the team '{team_name}' under Mentor '{selected_mentor_name}'.")
    if st.button("Add Team"):
        if team_name and mentor_id:
            try:
                execute_procedure("add_team", (team_name, mentor_id))
                st.success(f"Team '{team_name}' added successfully under Mentor '{selected_mentor_name}'.")
            except Exception as e:
                st.error(f"An error occurred while adding the team: {e}")
        else:
            st.error("Please fill in all fields.")

def create_project():
    ''' Handles creating a project and assigning it to a team and mentor '''
    st.subheader("Create a Project")
    
    # Fetch unassigned teams
    unassigned_teams = fetch_data("""
        SELECT Team_ID, Team_Name 
        FROM Team 
        WHERE Team_ID NOT IN (SELECT DISTINCT Team_ID FROM Project WHERE Team_ID IS NOT NULL);
    """)
    
    if unassigned_teams:
        team_names = {team["Team_Name"]: team["Team_ID"] for team in unassigned_teams}
        selected_team_name = st.selectbox("Select an Unassigned Team", list(team_names.keys()))
    else:
        st.warning("No unassigned teams available. Please create a team first.")
        return
    
    # Fetch mentors
    mentors = fetch_data("SELECT Mentor_ID, Name FROM Mentor;")
    if mentors:
        mentor_names = {mentor["Name"]: mentor["Mentor_ID"] for mentor in mentors}
        selected_mentor_name = st.selectbox("Assign Mentor", list(mentor_names.keys()))
    else:
        st.warning("No mentors available. Please add mentors to the system.")
        return
    
    # Input fields for project details
    project_name = st.text_input("Project Name")
    initial_draft = st.text_input("Initial Draft Filename (optional)", placeholder="e.g., draft_v1.docx")
    final_submission = st.text_input("Final Submission Filename (optional)", placeholder="e.g., final_v1.docx")
    project_status = st.selectbox("Project Status", ["Not Started", "In Progress", "Completed"])
    submission_date = st.date_input("Submission Date (if applicable)", value=None)
    
    if project_name:
        st.warning("Please review before creating the project.")
    
    if st.button("Create Project"):
        if project_name:  # Project name is mandatory
            try:
                team_id = team_names[selected_team_name]
                mentor_id = mentor_names[selected_mentor_name]
                submission_date_str = str(submission_date) if submission_date else None
                execute_procedure(
                    "create_project", 
                    (
                        project_name,
                        initial_draft if initial_draft else None,
                        final_submission if final_submission else None,
                        project_status,
                        submission_date_str,
                        team_id,
                        mentor_id
                    )
                )
                st.success(f"Project '{project_name}' created successfully for Team '{selected_team_name}'.")
            except Exception as e:
                st.error(f"An error occurred while creating the project: {e}")
        else:
            st.error("Project Name is mandatory. Please fill it in.")


def view_deleted_students():
    ''' Displays deleted students '''
    st.subheader("View Deleted Students")
    deleted_students = fetch_data("SELECT * FROM Deleted_Students_View;")
    if deleted_students:
        st.table(deleted_students)
    else:
        st.write("No deleted students found.")
        
def view_project_evaluation_details():
    ''' Displays project evaluation details from the view '''
    st.subheader("View Project Evaluation Details")
    evaluation_details = fetch_data("SELECT * FROM Project_Evaluation_Details;")
    
    if evaluation_details:
        st.table(evaluation_details)
    else:
        st.write("No project evaluation details found.")


def get_all_students():
    """Fetches and displays all students' details."""
    st.subheader("All Students")
    query = "SELECT Student_ID,Name,Email FROM Student;"
    students = fetch_data(query)
    
    if students:
        st.dataframe(students)
    else:
        st.write("No students found.")

def get_all_mentors():
    """Fetches and displays all mentors' details."""
    st.subheader("All Mentors")
    query = "SELECT * FROM Mentor;"
    mentors = fetch_data(query)
    
    if mentors:
        st.dataframe(mentors)
    else:
        st.write("No mentors found.")

def get_all_teams():
    """Fetches and displays all teams' details grouped by mentor name."""
    st.subheader("All Teams Grouped by Mentor")

    # Query to fetch team details and mentor names
    query = """
    SELECT 
        Team.Team_ID, 
        Team.Team_Name, 
        Mentor.Name AS Mentor_Name
    FROM 
        Team
    LEFT JOIN 
        Mentor 
    ON 
        Team.Mentor_ID = Mentor.Mentor_ID;
    """
    
    try:
        # Fetching data from the database
        teams = fetch_data(query)

        if teams:
            # Convert to pandas DataFrame for manipulation
            df = pd.DataFrame(teams)

            # Group by mentor name
            grouped = df.groupby("Mentor_Name")
            
            for mentor, team_data in grouped:
                with st.expander(f"Mentor: {mentor if mentor else 'Unassigned'}"):
                    st.dataframe(team_data[["Team_ID", "Team_Name"]])
        else:
            st.write("No teams found.")
    
    except Exception as e:
        st.error(f"An error occurred while fetching teams: {e}")


def get_project_status(project_id):
    """Fetches and displays the status of a project."""
    st.subheader(f"Project Status for Project ID {project_id}")
    query = "SELECT Status FROM Project WHERE Project_ID = %s;"
    status = fetch_data(query, (project_id,))
    
    if status:
        st.write(status)
    else:
        st.write(f"No status found for Project ID {project_id}.")

def get_all_teams():
    """Fetches and displays all teams' details grouped by mentor name, including student and project details."""
    st.subheader("All Teams Grouped by Mentor with Students and Projects")

    query = """
    SELECT 
        Team.Team_ID, 
        Team.Team_Name, 
        Mentor.Name AS Mentor_Name, 
        Student.Name AS Student_Name, 
        Student.Email AS Student_Email,
        Project.Project_Name AS Project_Name
    FROM 
        Team
    LEFT JOIN 
        Mentor 
    ON 
        Team.Mentor_ID = Mentor.Mentor_ID
    LEFT JOIN 
        Student 
    ON 
        Team.Team_ID = Student.Team_ID
    LEFT JOIN 
        Project
    ON 
        Team.Team_ID = Project.Team_ID
    ORDER BY 
        Mentor_Name, Team.Team_Name, Student.Name;
    """
    
    try:
        data = fetch_data(query)

        if data:
            df = pd.DataFrame(data)

            grouped = df.groupby(["Mentor_Name", "Team_Name", "Project_Name"])
            
            for (mentor, team, project), team_data in grouped:
                mentor_name = mentor if mentor else "Unassigned"
                
                with st.expander(f"Mentor: {mentor_name} | Team: {team} | Project: {project if project else 'No Project'}"):
                    st.write(f"**Team Name :** {team}")
                    st.write(f"**Mentor :** {mentor_name}")
                    st.write(f"**Project :** {project if project else 'No project assigned'}")
                                        
                    students = team_data[["Student_Name", "Student_Email"]]
                    if not students.empty:
                        st.write("### Students in this team:")
                        st.dataframe(students)
                    else:
                        st.write("_No students assigned to this team._")
        else:
            st.write("No teams found.")
    
    except Exception as e:
        st.error(f"An error occurred while fetching team details: {e}")
