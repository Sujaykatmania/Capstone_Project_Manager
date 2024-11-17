import streamlit as st
import pandas as pd
from database import fetch_data, execute_procedure  # Assumes fetch_data and execute_procedure are defined

import pandas as pd
import streamlit as st

def view_teams_under_mentor():
    mentor_id = st.session_state.user.get('ID')
    st.subheader("Teams Under Your Mentorship")

    query = f"""
    SELECT 
        T.Team_Name, 
        T.Team_ID,
        S.Name AS Student_Name, 
        S.Email
    FROM Team T
    LEFT JOIN Student S ON T.Team_ID = S.Team_ID
    WHERE T.Mentor_ID = {mentor_id}
    ORDER BY T.Team_Name, S.Name;
    """
    
    data = fetch_data(query)
    
    if data:
        teams = {}
        for row in data:
            team_name = row['Team_Name']
            if team_name not in teams:
                teams[team_name] = []
            teams[team_name].append(f"{row['Student_Name']} ({row['Email']})")
        
        # Display teams with students
        for team_name, students in teams.items():
            with st.expander(team_name):
                for student in students:
                    st.write(student)
    else:
        st.write("No teams found under your mentorship.")


def evaluate_project():
    mentor_id = st.session_state.user.get('ID')
    st.subheader("Evaluate Projects Assigned to Your Teams")

    query = f"""
    SELECT 
        P.Project_Name, 
        P.Project_ID, 
        P.Status, 
        T.Team_Name
    FROM Project P
    JOIN Team T ON P.Team_ID = T.Team_ID
    WHERE T.Mentor_ID = {mentor_id}
    ORDER BY P.Status, P.Project_Name;
    """
    
    projects = fetch_data(query)
    
    if not projects:
        st.error("No projects assigned to your teams for evaluation.")
        return

    project_options = {project["Project_Name"]: project["Project_ID"] for project in projects}
    selected_project_name = st.selectbox("Select Project", list(project_options.keys()))
    project_id = project_options[selected_project_name]
    
    project_details = next(project for project in projects if project["Project_ID"] == project_id)

    st.write(f"**Status**: {project_details['Status']}")
    
    grade = st.number_input("Grade", min_value=0.0, max_value=10.0, step=0.5)
    comments = st.text_area("Comments")
    
    if st.button("Evaluate Project"):
        execute_procedure("EvaluateProject", (project_id, mentor_id, grade, comments))
        st.success(f"Project {project_details['Project_Name']} evaluated with grade {grade}.")


def view_project_files():
    mentor_id = st.session_state.user.get('ID')

    st.subheader("View Project Files")

    query = f"""
    SELECT 
        P.Project_Name, 
        P.Initial_Draft, 
        P.Final_Submission, 
        T.Team_Name,
        P.Status
    FROM Project P
    JOIN Team T ON P.Team_ID = T.Team_ID
    WHERE T.Mentor_ID = {mentor_id}
    ORDER BY P.Status;
    """
    
    projects = fetch_data(query)
    
    if projects:
        # Grouping projects by their status (e.g., in-progress, completed, etc.)
        project_groups = {}
        for project in projects:
            status = project['Status']
            if status not in project_groups:
                project_groups[status] = []
            project_groups[status].append(project)
        
        # Display projects grouped by their status
        for status, status_projects in project_groups.items():
            with st.expander(f"{status} Projects"):
                for project in status_projects:
                    st.subheader(f"Project: {project['Project_Name']}")
                    st.write(f"Team: {project['Team_Name']}")
                    st.write(f"Status: {project['Status']}")
                    
                    if project['Initial_Draft']:
                        st.write("Initial Draft: Submitted")
                    else:
                        st.write("Initial Draft: Not submitted.")
                    
                    if project['Final_Submission']:
                        st.write("Final Submission: Submitted")
                    else:
                        st.write("Final Submission: Not submitted.")
    else:
        st.write("No projects to display for your teams.")
