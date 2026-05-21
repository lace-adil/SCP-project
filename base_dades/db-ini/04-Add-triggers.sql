USE scp;
CREATE TRIGGER staff_delete_cleanup BEFORE DELETE ON staff
-- For each SCP this researcher was assigned to, assign them a new researcher with the least SCPs assigned
FOR EACH ROW UPDATE scp_subjects SET assigned_researcher_id=(
    SELECT staff.id FROM staff JOIN scp_subjects ON scp_subjects.assigned_researcher_id=staff.id
    GROUP BY staff.id
    ORDER BY COUNT(scp_subjects.id)
    )
WHERE assigned_researcher_id.id = OLD.id;