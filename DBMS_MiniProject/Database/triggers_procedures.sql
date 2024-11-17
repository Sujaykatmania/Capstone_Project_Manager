DELIMITER //
CREATE TRIGGER before_feedback_insert
BEFORE INSERT ON Feedback
FOR EACH ROW
BEGIN
    SET NEW.Date_Provided = CURDATE();
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_project_update
BEFORE UPDATE ON Project
FOR EACH ROW
BEGIN
    IF NEW.Final_Submission IS NOT NULL THEN
        SET NEW.Status = 'Completed';
    END IF;
END //
DELIMITER ;


DELIMITER $$
CREATE TRIGGER before_student_delete
BEFORE DELETE ON Student
FOR EACH ROW
BEGIN
    -- Insert the student data into the backup table
    INSERT INTO Deleted_Student (Student_ID, Name, Email , Team_ID)
    VALUES (OLD.Student_ID, OLD.Name, OLD.Email, OLD.Team_ID);
END$$
DELIMITER ;


DELIMITER //
CREATE TRIGGER check_max_students_in_team
BEFORE INSERT ON Student
FOR EACH ROW
BEGIN
    DECLARE student_count INT;
    -- Check the number of students already in the team
    SELECT COUNT(*) INTO student_count FROM Student WHERE Team_ID = NEW.Team_ID;
    
    -- If the team has 4 or more students, prevent the insert
    IF student_count >= 4 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A team can have a maximum of 4 students.';
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AddStudent(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100),
    IN p_team_id INT
)
BEGIN
    INSERT INTO Student(Name, Email, Password, Team_ID)
    VALUES (p_name, p_email, p_password, p_team_id);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AddMentor(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(100),
    IN p_department ENUM('CSE', 'ECE', 'EEE', 'MECH', 'AIML')
)
BEGIN
    INSERT INTO Mentor(Name, Email, Password, Department)
    VALUES (p_name, p_email, p_password, p_department);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE AssignTeamToProject(
    IN p_project_id INT,
    IN p_team_id INT
)
BEGIN
    UPDATE Project
    SET Team_ID = p_team_id
    WHERE Project_ID = p_project_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE EvaluateProject(
    IN p_project_id INT,
    IN p_panel_id INT,
    IN p_grade DECIMAL(3, 2),
    IN p_comments TEXT
)
BEGIN
    INSERT INTO Evaluation(Project_ID, Panel_ID, Grade, Comments, Evaluation_Date)
    VALUES (p_project_id, p_panel_id, p_grade, p_comments, CURDATE());
END //
DELIMITER ;




DELIMITER //
CREATE PROCEDURE DeleteStudent(
    IN p_student_id INT
)
BEGIN

    -- Delete the student record
    DELETE FROM Student WHERE Student_ID = p_student_id;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE update_project_status(IN p_project_id INT, IN p_status VARCHAR(20))
BEGIN
    UPDATE Project
    SET Status = p_status
    WHERE Project_ID = p_project_id;
END //
DELIMITER ;


DELIMITER $$
CREATE PROCEDURE create_project(
    IN project_name VARCHAR(255),
    IN initial_draft VARCHAR(255),
    IN final_submission VARCHAR(255),
    IN project_status VARCHAR(50),
    IN submission_date DATE,
    IN team_id INT,
    IN mentor_id INT
)
BEGIN
    INSERT INTO Project (
        Project_Name, 
        Initial_Draft, 
        Final_Submission, 
        Status, 
        Submission_Date, 
        Team_ID, 
        Mentor_ID
    ) VALUES (
        project_name, 
        initial_draft, 
        final_submission, 
        project_status, 
        submission_date, 
        team_id, 
        mentor_id
    );
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE add_team(
    IN team_name VARCHAR(255),
    IN mentor_id INT
)
BEGIN
    INSERT INTO Team (Team_Name, Mentor_ID)
    VALUES (team_name, mentor_id);
END $$

DELIMITER ;
