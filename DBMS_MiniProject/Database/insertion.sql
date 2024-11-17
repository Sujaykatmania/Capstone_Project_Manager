-- Insert Mentors with Specified Departments
INSERT INTO Mentor (Name, Email, Password, Department) VALUES 
('Prof Nithin V Pujari', 'nvp@gmail.com', 'password123', 'CSE'),
('Dr. Jayashree R', 'jayashree@gmail.com', 'password123', 'AIML'),
('Dr. Jawahar', 'jawahar@gmail.com', 'password123', 'EEE'),
('Prof BJD', 'bjd@gmail.com', 'password123', 'MECH');

-- Insert Teams
INSERT INTO Team (Team_Name, Mentor_ID) VALUES 
('Team Alpha', 1),
('Team Beta', 2),
('Team Gamma', 3),
('Team Delta', 4),
('Team Epsilon', 1),
('Team Zeta', 2),
('Team Eta', 3);

-- Insert Projects
INSERT INTO Project (Project_Name, Initial_Draft, Final_Submission, Status, Submission_Date, Team_ID, Mentor_ID) VALUES 
('AI-Powered System', 'draft_v1.docx', 'final_v1.docx', 'In Progress', '2024-10-20', 1, 1),
('ZKP-Blockchain Research', 'draft_v2.docx', 'final_v2.docx', 'Not Started', NULL, 2, 2),
('Smart Grid Project', 'draft_v3.docx', 'final_v3.docx', 'Completed', '2024-10-15', 3, 3),
('Robotics Development', 'draft_v4.docx', 'final_v4.docx', 'In Progress', '2024-10-25', 4, 4),
('Autonomous Vehicle', 'draft_v5.docx', 'final_v5.docx', 'Not Started', NULL, 5, 1),
('Cybersecurity Systems', 'draft_v6.docx', 'final_v6.docx', 'Completed', '2024-09-30', 6, 2),
('Machine Learning Model', 'draft_v7.docx', 'final_v7.docx', 'Not Started', NULL, 7, 3);

-- Insert Students (Make sure each team has 4 students)
INSERT INTO Student (Name, Email, Password, Team_ID) VALUES 
('Adityanath Yogi', 'adityanath@gmail.com', 'yogi', 1),
('Narendra Modi', 'narendra@gmail.com', 'modi', 1),
('Amit Shah', 'amit@gmail.com', 'amit', 1),
('S Jayashankar', 'jayashankar@gmail.com', 'jayshankar', 1),
('Kharge Mallikarjun', 'kharge@gmail.com', 'kharge', 2),
('Rahul Gandhi', 'rahul@gmail.com', 'rahul', 2),
('Priyanka Gandhi', 'priyanka@gmail.com', 'priyanka', 2),
('Manmohan Singh', 'manmohan@gmail.com', 'manmohan', 2),
('Sundar Pichai', 'sundar@gmail.com', 'sundar', 3),
('Satya Nadella', 'satya@gmail.com', 'satya', 3),
('Elon Musk', 'elonmusk@gmail.com', 'elon', 3),
('Jeff Bezos', 'jeff@gmail.com', 'bezos', 3),
('Tim Cook', 'timcook@gmail.com', 'tim', 4),
('Mark Zuckerberg', 'markzuck@gmail.com', 'mark', 4),
('Jack Ma', 'jackma@gmail.com', 'jack', 4),
('Larry Page', 'larry@gmail.com', 'page', 4),
('Sheryl Sandberg', 'sheryl@gmail.com', 'sheryl', 5),
('Reed Hastings', 'reed@gmail.com', 'reed', 5),
('Jeff Weiner', 'jeffw@gmail.com', 'jeffw', 5),
('Brian Chesky', 'brian@gmail.com', 'brian', 5),
('Travis Kalanick', 'travis@gmail.com', 'travis', 6),
('Garrett Camp', 'garrett@gmail.com', 'garrett', 6),
('Dara Khosrowshahi', 'dara@gmail.com', 'dara', 6),
('John Zimmer', 'johnzimmer@gmail.com', 'johnz', 6),
('DeepMind AI', 'deepmind@gmail.com', 'deepmind', 7),
('Geoffrey Hinton', 'geoffreyh@gmail.com', 'hinton', 7),
('Yann LeCun', 'yannlc@gmail.com', 'lecun', 7),
('Andrew Ng', 'andrewng@gmail.com', 'andrewng', 7);

-- Insert Panels
INSERT INTO Panel (Panel_Name) VALUES 
('ISA Panel'),
('ESA Panel'),
('Technical Panel'),
('Innovation Panel');

-- Insert Evaluations
INSERT INTO Evaluation (Project_ID, Panel_ID, Grade, Comments, Evaluation_Date) VALUES
(1, 1, 8.5, 'Good progress, needs more refinement.', '2024-10-22'),
(2, 2, 7.0, 'Project needs further research on blockchain technology.', '2024-10-23'),
(3, 3, 9.0, 'Project is complete and well-executed.', '2024-10-24'),
(4, 4, 8.0, 'Some delays, but overall good development.', '2024-10-25'),
(5, 1, 6.5, 'Not enough progress, needs more work on autonomous systems.', '2024-10-26'),
(6, 2, 8.0, 'Good work, but needs additional testing for scalability.', '2024-10-27'),
(7, 3, 7.5, 'Project in early stages, further improvements required.', '2024-10-28');
