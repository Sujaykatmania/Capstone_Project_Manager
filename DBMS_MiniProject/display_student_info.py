import streamlit as st
from database import fetch_data
def display_student_details():
    st.subheader("Your Team Info")
    
    if st.session_state.user and st.session_state.user['Role'] == 'Student':
        student_id = st.session_state.user['Student_ID']
        
        try:
            student_query = f"""
                SELECT 
                    s.Name AS Student_Name,
                    t.Team_Name,
                    m.Name AS Mentor_Name
                FROM 
                    Student s
                    INNER JOIN Team t ON s.Team_ID = t.Team_ID
                    LEFT JOIN Mentor m ON t.Mentor_ID = m.Mentor_ID
                WHERE 
                    s.Student_ID = {student_id};
            """
            student_info = fetch_data(student_query)
            
            if student_info:
                student_info = student_info[0]
                st.write(f"Student Name: {student_info['Student_Name']}")
                st.write(f"Team Name: {student_info['Team_Name']}")
                st.write(f"Mentor: {student_info['Mentor_Name']}")
            
            team_members_query = f"""
                SELECT 
                    GROUP_CONCAT(s.Name SEPARATOR ', ') AS Team_Members
                FROM 
                    Student s
                WHERE 
                    s.Team_ID = (SELECT Team_ID FROM Student WHERE Student_ID = {student_id} LIMIT 1);
            """
            team_members = fetch_data(team_members_query)
            
            if team_members:
                st.write(f"Team Members: {team_members[0]['Team_Members']}")
            else:
                st.write("No team members found.")
            
            project_query = f"""
                SELECT 
                    p.Project_Name,
                    p.Initial_Draft,
                    p.Final_Submission,
                    p.Status,
                    p.Submission_Date,
                    e.Grade,
                    e.Comments AS Evaluation_Comments,
                    e.Evaluation_Date
                FROM 
                    Project p
                    LEFT JOIN Evaluation e ON p.Project_ID = e.Project_ID
                WHERE 
                    p.Team_ID = (SELECT Team_ID FROM Student WHERE Student_ID = {student_id} LIMIT 1);
            """
            project_details = fetch_data(project_query)
            
            if project_details:
                for row in project_details:
                    st.write(f"Project Name: {row['Project_Name']}")
                    st.write(f"Initial Draft: {row['Initial_Draft']}")
                    st.write(f"Final Submission: {row['Final_Submission']}")
                    st.write(f"Status: {row['Status']}")
                    st.write(f"Submission Date: {row['Submission_Date']}")
                    st.write(f"Grade: {row['Grade']}")
                    st.write(f"Evaluation Comments: {row['Evaluation_Comments']}")
                    st.write(f"Evaluation Date: {row['Evaluation_Date']}")
            else:
                st.write("No project details found.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("You must be logged in as a student to view this information.")