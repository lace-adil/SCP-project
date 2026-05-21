CREATE ROLE "viewer";
CREATE ROLE "subjectmanager";
CREATE ROLE "usermanager";
CREATE ROLE "staffmanager";
CREATE ROLE "zonemanager";

GRANT SELECT ON scp.* to "viewer";


GRANT SELECT, UPDATE, DELETE, INSERT ON scp.scp_subjects to "subjectmanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.roles, scp.staff to "staffmanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.users to "usermanager";
GRANT SELECT, UPDATE, DELETE, INSERT ON scp.zones, scp.chambers to "zonemanager";

