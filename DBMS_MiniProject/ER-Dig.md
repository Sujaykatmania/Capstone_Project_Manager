```mermaid
graph TD
    %% Entities (Rectangles)
    Mentor[("Mentor")]
    Team[("Team")]
    Project[("Project")]
    Student[("Student")]
    Feedback[("Feedback")]
    Panel[("Panel")]
    Evaluation[("Evaluation")]
    EvalHistory[("Evaluation_History")]
    DeletedStudent[("Deleted_Student")]

    %% Mentor Attributes
    MentorID((Mentor_ID))
    MentorName((Name))
    MentorEmail((Email))
    MentorPass((Password))
    MentorDept((Department))

    %% Team Attributes
    TeamID((Team_ID))
    TeamName((Team_Name))

    %% Project Attributes
    ProjectID((Project_ID))
    ProjectName((Project_Name))
    InitialDraft((Initial_Draft))
    FinalSub((Final_Submission))
    Status((Status))
    SubDate((Submission_Date))

    %% Student Attributes
    StudentID((Student_ID))
    StudentName((Name))
    StudentEmail((Email))
    StudentPass((Password))

    %% Feedback Attributes
    FeedbackID((Feedback_ID))
    Comments((Comments))
    DateProvided((Date_Provided))

    %% Panel Attributes
    PanelID((Panel_ID))
    PanelName((Panel_Name))

    %% Evaluation Attributes
    EvalID((Evaluation_ID))
    Grade((Grade))
    EvalComments((Comments))
    EvalDate((Evaluation_Date))

    %% Relationships (Rhombuses)
    MentorsTeam{Mentors}
    HasStudents{Has}
    AssignedTo{Assigned To}
    ProvidesFeedback{Provides}
    Evaluates{Evaluates}
    TracksHistory{Tracks}

    %% Mentor Connections
    Mentor --- MentorID
    Mentor --- MentorName
    Mentor --- MentorEmail
    Mentor --- MentorPass
    Mentor --- MentorDept
    Mentor --- MentorsTeam
    MentorsTeam --- Team

    %% Team Connections
    Team --- TeamID
    Team --- TeamName
    Team --- HasStudents
    HasStudents --- Student
    Team --- AssignedTo
    AssignedTo --- Project

    %% Project Connections
    Project --- ProjectID
    Project --- ProjectName
    Project --- InitialDraft
    Project --- FinalSub
    Project --- Status
    Project --- SubDate

    %% Student Connections
    Student --- StudentID
    Student --- StudentName
    Student --- StudentEmail
    Student --- StudentPass

    %% Feedback Connections
    Mentor --- ProvidesFeedback
    ProvidesFeedback --- Feedback
    Feedback --- FeedbackID
    Feedback --- Comments
    Feedback --- DateProvided
    Feedback --- Project

    %% Panel Connections
    Panel --- PanelID
    Panel --- PanelName
    Panel --- Evaluates
    Evaluates --- Evaluation

    %% Evaluation Connections
    Evaluation --- EvalID
    Evaluation --- Grade
    Evaluation --- EvalComments
    Evaluation --- EvalDate
    Evaluation --- Project
    Evaluation --- TracksHistory
    TracksHistory --- EvalHistory

    %% Style
    classDef entity fill:#FF0000,stroke:#222222,stroke-width:3px,color:#ffffff,font-size:20px
    classDef attribute fill:#013220,stroke:#111111,stroke-width:2px,color:#ffffff,font-size:18px
    classDef relationship fill:#00008B,stroke:#333333,stroke-width:2px,color:#ffffff,font-size:18px
    
    class Mentor,Team,Project,Student,Feedback,Panel,Evaluation,EvalHistory,DeletedStudent entity
    class MentorID,MentorName,MentorEmail,MentorPass,MentorDept,TeamID,TeamName,ProjectID,ProjectName,InitialDraft,FinalSub,Status,SubDate,StudentID,StudentName,StudentEmail,StudentPass,FeedbackID,Comments,DateProvided,PanelID,PanelName,EvalID,Grade,EvalComments,EvalDate attribute
    class MentorsTeam,HasStudents,AssignedTo,ProvidesFeedback,Evaluates,TracksHistory relationship

    ```