CREATE SCHEMA "team_capacity";

CREATE TABLE "team_capacity"."Member" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "email" varchar,
  "capacity" int DEFAULT 100,
  "uploaded" datetime DEFAULT (now())
);

CREATE TABLE "team_capacity"."Skill" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "name" varchar,
  "uploaded" datetime DEFAULT (now())
);

CREATE TABLE "team_capacity"."MemberSkills" (
  "member_id" int,
  "skill_id" int,
  "uploaded" datetime DEFAULT (now())
);

CREATE TABLE "team_capacity"."Project" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "name" varchar,
  "uploaded" datetime DEFAULT (now())
);

CREATE TABLE "team_capacity"."Assingment" (
  "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  "project_id" int NOT NULL,
  "member_id" int NOT NULL,
  "capacity" int NOT NULL DEFAULT 100,
  "uploaded" datetime DEFAULT (now())
);

ALTER TABLE "team_capacity"."MemberSkills" ADD FOREIGN KEY ("member_id") REFERENCES "team_capacity"."Member" ("id");

ALTER TABLE "team_capacity"."MemberSkills" ADD FOREIGN KEY ("skill_id") REFERENCES "team_capacity"."Skill" ("id");

ALTER TABLE "team_capacity"."Assingment" ADD FOREIGN KEY ("member_id") REFERENCES "team_capacity"."Member" ("id");

ALTER TABLE "team_capacity"."Assingment" ADD FOREIGN KEY ("project_id") REFERENCES "team_capacity"."Project" ("id");