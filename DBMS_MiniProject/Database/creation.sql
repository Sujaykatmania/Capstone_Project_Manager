-- Database Creation
CREATE DATABASE dbms_proj;
USE dbms_proj;

-- Table Creation Section

-- 1. Mentor Table with Specific Departments
CREATE TABLE Mentor (
    Mentor_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Password VARCHAR(100),
    Department ENUM('CSE', 'ECE', 'EEE', 'MECH', 'AIML'),
    CONSTRAINT email_format CHECK (Email REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
);

-- 2. Team Table
CREATE TABLE Team (
    Team_ID INT PRIMARY KEY AUTO_INCREMENT,
    Team_Name VARCHAR(100),
    Mentor_ID INT,
    FOREIGN KEY (Mentor_ID) REFERENCES Mentor(Mentor_ID)
);

-- 3. Project Table
CREATE TABLE Project (
    Project_ID INT PRIMARY KEY AUTO_INCREMENT,
    Project_Name VARCHAR(100),
    Initial_Draft VARCHAR(255),
    Final_Submission VARCHAR(255),
    Status ENUM('Not Started', 'In Progress', 'Completed'),
    Submission_Date DATE,
    Team_ID INT,
    Mentor_ID INT,
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID),
    FOREIGN KEY (Mentor_ID) REFERENCES Mentor(Mentor_ID)
);

-- 4. Student Table (Removed Role Column)
CREATE TABLE Student (
    Student_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Password VARCHAR(100),
    Team_ID INT,
    FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID),
    CONSTRAINT email_format_student CHECK (Email REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
);

-- 5. Feedback Table
CREATE TABLE Feedback (
    Feedback_ID INT PRIMARY KEY AUTO_INCREMENT,
    Project_ID INT,
    Mentor_ID INT,
    Comments TEXT,
    Date_Provided DATE,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID),
    FOREIGN KEY (Mentor_ID) REFERENCES Mentor(Mentor_ID)
);

-- 6. Panel Table
CREATE TABLE Panel (
    Panel_ID INT PRIMARY KEY AUTO_INCREMENT,
    Panel_Name VARCHAR(100)
);

-- 7. Evaluation Table
CREATE TABLE Evaluation (
    Evaluation_ID INT PRIMARY KEY AUTO_INCREMENT,
    Project_ID INT,
    Panel_ID INT,
    Grade DECIMAL(3, 2),
    Comments TEXT,
    Evaluation_Date DATE,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID),
    FOREIGN KEY (Panel_ID) REFERENCES Panel(Panel_ID)
);

-- 8. Evaluation History Table (for tracking updates)
CREATE TABLE Evaluation_History (
    History_ID INT PRIMARY KEY AUTO_INCREMENT,
    Evaluation_ID INT,
    Project_ID INT,
    Panel_ID INT,
    Grade DECIMAL(3, 2),
    Comments TEXT,
    Evaluation_Date DATE,
    Action ENUM('INSERT', 'UPDATE'),
    Action_Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Project_ID) REFERENCES Project(Project_ID),
    FOREIGN KEY (Panel_ID) REFERENCES Panel(Panel_ID),
    FOREIGN KEY (Evaluation_ID) REFERENCES Evaluation(Evaluation_ID)
);

-- 9. Deleted Student Table (to keep record of deleted students)
CREATE TABLE Deleted_Student (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255),
    Team_ID INT,
    Deleted_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
