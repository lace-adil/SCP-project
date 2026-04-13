import fastapi
import sqlalchemy
from .utils import db_engine
app = fastapi.FastAPI()


@app.get("/search")
def root():
    return {"message":"Hello, world!"}


@app.get("/search/{item_id}")
def getSCPSubject(item_id):

    procedures = 0
    description = 0
    object_class = 0
    data = None
    with db_engine.connect() as db_con:

        result = db_con.execute(sqlalchemy.text(f"SELECT * FROM scp_subjects WHERE id={item_id};"))
        data = result.fetchone()

    if data:
        procedures = data[2]
        description = data[3]
        object_class = data[1]

    return {"Item-#":item_id, "object_class":object_class ,"procedures": procedures, "description":description}
