-- View to view to deleted students

-- View Deleted Students
CREATE VIEW Deleted_Students_View AS
SELECT 
    ds.Student_ID,
    ds.Name AS Student_Name,
    ds.Email AS Student_Email,
    ds.Deleted_At
FROM 
    Deleted_Student ds;


-- View Project Eval
CREATE VIEW Project_Evaluation_Details AS
SELECT 
    p.Project_ID,
    p.Project_Name,
    e.Evaluation_ID,
    e.Grade,
    e.Comments AS Evaluation_Comments,
    e.Evaluation_Date,
    pa.Panel_Name
FROM 
    Project p
LEFT JOIN 
    Evaluation e ON p.Project_ID = e.Project_ID
LEFT JOIN 
    Panel pa ON e.Panel_ID = pa.Panel_ID;


-- View teams
CREATE VIEW Project_Team_Mentor AS
SELECT 
    p.Project_ID,
    p.Project_Name,
    p.Status AS Project_Status,
    t.Team_Name,
    m.Name AS Mentor_Name,
    m.Department AS Mentor_Department,
    p.Submission_Date
FROM 
    Project p
JOIN 
    Team t ON p.Team_ID = t.Team_ID
JOIN 
    Mentor m ON p.Mentor_ID = m.Mentor_ID;
