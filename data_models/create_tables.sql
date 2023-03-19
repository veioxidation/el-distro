-- Create Projects table
CREATE TABLE Projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  capacity INTEGER NOT NULL
);

-- Create Team Members table
CREATE TABLE TeamMembers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Create Team Member Skills table
CREATE TABLE TeamMemberSkills (
  id SERIAL PRIMARY KEY,
  team_member_id INTEGER NOT NULL,
  skillset VARCHAR(255) NOT NULL,
  FOREIGN KEY (team_member_id) REFERENCES TeamMembers (id)
);

-- Create Project Assignments table
CREATE TABLE ProjectAssignments (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL,
  team_member_id INTEGER NOT NULL,
  capacity INTEGER NOT NULL,
  FOREIGN KEY (project_id) REFERENCES Projects (id),
  FOREIGN KEY (team_member_id) REFERENCES TeamMembers (id)
);
