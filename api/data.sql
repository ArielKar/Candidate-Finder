BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "skill_skill" (
	"id"	integer NOT NULL,
	"name"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "job_opinion" (
	"id"	integer NOT NULL,
	"created_at"	datetime NOT NULL,
	"liked"	bool NOT NULL,
	"candidate_id"	integer NOT NULL,
	"job_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("candidate_id") REFERENCES "candidate_candidate"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("job_id") REFERENCES "job_job"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "job_job" (
	"id"	integer NOT NULL,
	"title"	varchar(100) NOT NULL,
	"status"	varchar(25) NOT NULL,
	"skill_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("skill_id") REFERENCES "skill_skill"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "candidate_note" (
	"id"	integer NOT NULL,
	"note"	varchar(255) NOT NULL,
	"candidate_id"	integer NOT NULL,
	"job_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("job_id") REFERENCES "job_job"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("candidate_id") REFERENCES "candidate_candidate"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "candidate_candidate" (
	"id"	integer NOT NULL,
	"title"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "candidate_candidate_skills" (
	"id"	integer NOT NULL,
	"candidate_id"	integer NOT NULL,
	"skill_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("skill_id") REFERENCES "skill_skill"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("candidate_id") REFERENCES "candidate_candidate"("id") DEFERRABLE INITIALLY DEFERRED
);
INSERT INTO "skill_skill" ("id","name") VALUES (1,'Guitarist'),
 (2,'Pianist'),
 (3,'Drummer'),
 (4,'Bass Player'),
 (5,'Singer'),
 (6,'Dancer'),
 (7,'Clown');
INSERT INTO "job_opinion" ("id","created_at","liked","candidate_id","job_id") VALUES (3,'2020-09-05 22:01:50.638725',1,1,1),
 (4,'2020-09-06 08:43:06.557449',0,2,1);
INSERT INTO "job_job" ("id","title","status","skill_id") VALUES (1,'Jazz pro guitarist','OPEN',1),
 (2,'Picnic Dad','OPEN',7),
 (3,'Singer','OPEN',5),
 (4,'Gala night pianist','OPEN',2),
 (5,'Rock band drummer','OPEN',3);
INSERT INTO "candidate_note" ("id","note","candidate_id","job_id") VALUES (5,'test note',1,1),
 (6,'test note 2',1,1),
 (7,'test note 2',2,1),
 (8,'test note 2',2,1),
 (9,'test note 2',2,1);
INSERT INTO "candidate_candidate" ("id","title") VALUES (1,'Lead Singer'),
 (2,'Guitarist'),
 (3,'Birthday Clown'),
 (4,'American Idol'),
 (5,'Ballet Dancer'),
 (6,'Rock band memeber'),
 (7,'Picnic Manager');
INSERT INTO "candidate_candidate_skills" ("id","candidate_id","skill_id") VALUES (1,1,1),
 (2,1,5),
 (3,2,1),
 (4,2,4),
 (5,3,6),
 (6,3,7),
 (7,4,1),
 (8,4,2),
 (9,4,3),
 (10,4,4),
 (11,4,5),
 (12,4,6),
 (13,4,7),
 (14,5,6),
 (15,6,2),
 (16,6,3),
 (17,6,5),
 (18,7,2);
CREATE INDEX IF NOT EXISTS "job_opinion_candidate_id_2832e939" ON "job_opinion" (
	"candidate_id"
);
CREATE INDEX IF NOT EXISTS "job_opinion_job_id_2775907d" ON "job_opinion" (
	"job_id"
);
CREATE INDEX IF NOT EXISTS "job_job_skill_id_54b416da" ON "job_job" (
	"skill_id"
);
CREATE INDEX IF NOT EXISTS "candidate_note_candidate_id_afe859e1" ON "candidate_note" (
	"candidate_id"
);
CREATE INDEX IF NOT EXISTS "candidate_note_job_id_12b50a35" ON "candidate_note" (
	"job_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "candidate_candidate_skills_candidate_id_skill_id_e7479459_uniq" ON "candidate_candidate_skills" (
	"candidate_id",
	"skill_id"
);
CREATE INDEX IF NOT EXISTS "candidate_candidate_skills_candidate_id_053033cf" ON "candidate_candidate_skills" (
	"candidate_id"
);
CREATE INDEX IF NOT EXISTS "candidate_candidate_skills_skill_id_7a61e7d7" ON "candidate_candidate_skills" (
	"skill_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "job_opinion_job_id_candidate_id_c224721c_uniq" ON "job_opinion" (
	"job_id",
	"candidate_id"
);
COMMIT;
