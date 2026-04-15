from fastapi import APIRouter, Response, Request, responses, requests, HTTPException
import src.utils as utils
import sqlalchemy
from .schemas import *

router = APIRouter(tags=["database"])

@router.get("/update-db")
def update_db():
    utils.updateDatabase()
    return {"message":"done"}


@router.get("/scp/{item_id}")
def getSCPSubject(item_id: int, res: Response):

    procedures = 0
    description = 0
    object_class = 0
    data = None

    with utils.db_engine.connect() as db_con:

        result = db_con.execute(sqlalchemy.text(f"SELECT * FROM scp_subjects WHERE id={item_id};"))
        data = result.fetchone()

    if data:
        procedures = data[2]
        description = data[3]
        object_class = data[1]
    else:
        pass
        res = HTTPException(status_code=404, detail="404 Item Not Found")
        return res
        # res = responses.RedirectResponse("/")
        # return res

    return {"Item-#":item_id, "object_class":object_class ,"procedures": procedures, "description":description}


@router.post("/insert/scp")
def insertSCPSubject(scp_subject: SCPSubject):

    order = f"""INSERT INTO scp_subjects ({"id," if scp_subject.id >= 0 else ""} object_class, containment_procedures, description) VALUES
    ({f"{scp_subject.id}," if scp_subject.id>=0 else ""} \"{scp_subject.object_class}\", \"{scp_subject.containment_procedures}\", \"{scp_subject.description}\");"""

    with utils.db_engine.connect() as db_con:
        db_con.execute(sqlalchemy.text(order))
        db_con.commit()
        return {"message":f"Succesfully added item #{scp_subject.id}"}