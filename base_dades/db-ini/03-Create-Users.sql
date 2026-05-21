CREATE ROLE "viewer";
CREATE ROLE "subjectmanager";
CREATE ROLE "usermanager";
CREATE ROLE "staffmanager";
CREATE ROLE "zonemanager";

GRANT SELECT ON scp.* to "viewer";


GRANT SELECT, UPDATE, DELETE, INSERT ON scp.scp_subjects to "subjectmanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.staff to "staffmanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.roles to "staffmanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.users to "usermanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.chambers to "zonemanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.zones to "zonemanager";


CREATE USER "subjectsadmin"@"%" IDENTIFIED BY "VeryHardToCrackPassword.";
GRANT "subjectmanager", "zonemanager" TO "subjectsadmin"@"%";

CREATE USER "staffadmin"@"%" IDENTIFIED BY "AnotherHardToCrackPassword.";
GRANT "viewer", "staffmanager","usermanager" to "staffadmin"@"%";