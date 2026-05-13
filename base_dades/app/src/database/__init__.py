from fastapi import APIRouter, Response, Request, responses, requests, HTTPException
import src.utils as utils
import sqlalchemy
from .schemas import *

router = APIRouter(tags=["database"])

@router.get("/update-db")
def update_db():
    utils.updateDatabase()
    return {"message":"done"}


@router.get("/scp/get/{item_id}")
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

    return {"id": item_id, "object_class": object_class, "containment_procedures": procedures, "description": description}


@router.post("/scp/insert")
def insertSCPSubject(scp_subject: SCPSubject):

    order = f"""INSERT INTO scp_subjects ({"id," if scp_subject.id >= 0 else ""} object_class, containment_procedures, description) VALUES
    ({f"{scp_subject.id}," if scp_subject.id>=0 else ""} \"{scp_subject.object_class}\", \"{scp_subject.containment_procedures}\", \"{scp_subject.description}\");"""

    with utils.db_engine.connect() as db_con:
        db_con.execute(sqlalchemy.text(order))
        db_con.commit()
        return {"message":f"Succesfully added item #{scp_subject.id}"}


@router.put("/scp/update/{item_id}")
def updateSCPSubject(item_id: int, scp_subject: SCPSubject):
    """Update an existing SCP subject."""
    order = f"""UPDATE scp_subjects SET object_class="{scp_subject.object_class}", 
    containment_procedures="{scp_subject.containment_procedures}", 
    description="{scp_subject.description}" WHERE id={item_id};"""

    with utils.db_engine.connect() as db_con:
        db_con.execute(sqlalchemy.text(order))
        db_con.commit()
        return {"message": f"Successfully updated item #{item_id}"}


@router.delete("/scp/delete/{item_id}")
def deleteSCPSubject(item_id: int):
    """Delete an SCP subject."""
    with utils.db_engine.connect() as db_con:
        db_con.execute(sqlalchemy.text(f"DELETE FROM scp_subjects WHERE id={item_id};"))
        db_con.commit()
        return {"message": f"Successfully deleted item #{item_id}"}


@router.get("/scp/list")
def showSCPSubjects():
    order = f"""SELECT id, object_class, containment_procedures, description FROM scp_subjects;"""

    with utils.db_engine.connect() as db_con:
        result = db_con.execute(sqlalchemy.text(order))
        result = result.fetchall()

        full_list = {}
        for item in result:
            full_list[item[0]] = {"object_class": item[1], "containment_procedures":item[2],"description":item[3]}

        return full_list


@router.get("/scp", response_class=responses.HTMLResponse)
def listSCPPage():
    """Serve a public page listing all SCP subjects."""
    with utils.db_engine.connect() as db_con:
        result = db_con.execute(sqlalchemy.text("SELECT id, object_class, containment_procedures, description FROM scp_subjects;"))
        subjects = result.fetchall()

    subjects_html = ""
    if subjects:
        for subject in subjects:
            item_id, obj_class, procedures, description = subject
            procedures_preview = procedures[:100] + "..." if len(procedures) > 100 else procedures
            subjects_html += f"""
            <div class="scp-card">
                <div class="scp-id">SCP-{item_id}</div>
                <div class="scp-class">{obj_class}</div>
                <p>{procedures_preview}</p>
                <a href="/scp/{item_id}" class="view-btn">View Full Details →</a>
            </div>
            """
    else:
        subjects_html = '<p style="text-align: center; color: #999; padding: 20px;">No SCP subjects found.</p>'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SCP Database - Public List</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1000px;
                margin: 0 auto;
            }}
            
            .header {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            
            .header h1 {{
                color: #667eea;
                font-size: 36px;
                margin-bottom: 10px;
            }}
            
            .header p {{
                color: #666;
                font-size: 16px;
            }}
            
            .header a {{
                display: inline-block;
                margin-top: 20px;
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }}
            
            .header a:hover {{
                text-decoration: underline;
            }}
            
            .subjects-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
            }}
            
            .scp-card {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            
            .scp-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            }}
            
            .scp-id {{
                color: #667eea;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            
            .scp-class {{
                background: #f0f0f0;
                color: #666;
                padding: 6px 12px;
                border-radius: 5px;
                display: inline-block;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 15px;
            }}
            
            .scp-card p {{
                color: #555;
                line-height: 1.6;
                margin-bottom: 15px;
                font-size: 14px;
            }}
            
            .view-btn {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: 600;
                transition: transform 0.2s;
            }}
            
            .view-btn:hover {{
                transform: translateX(5px);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>SCP Database</h1>
                <p>Browse all Secure, Contain, Protect subjects</p>
                <a href="/login">Login to edit</a>
            </div>
            
            <div class="subjects-grid">
                {subjects_html}
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


@router.get("/scp/{item_id}", response_class=responses.HTMLResponse)
def getSCPSubjectPage(item_id: int):
    """Serve a public page for viewing an SCP subject."""
    with utils.db_engine.connect() as db_con:
        result = db_con.execute(sqlalchemy.text(f"SELECT * FROM scp_subjects WHERE id={item_id};"))
        data = result.fetchone()

    if not data:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SCP Subject Not Found</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 800px; margin: 0 auto; }}
                h1 {{ color: #c33; }}
                a {{ color: #667eea; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>404 - SCP Subject Not Found</h1>
                <p>The SCP subject with ID {item_id} could not be found.</p>
                <p><a href="/scp">← Back to List</a></p>
            </div>
        </body>
        </html>
        """

    item_id_db, object_class, procedures, description = data
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SCP-{item_id_db}</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 36px;
                margin-bottom: 10px;
            }}
            
            .header .object-class {{
                font-size: 18px;
                opacity: 0.9;
                background: rgba(255, 255, 255, 0.2);
                padding: 8px 20px;
                border-radius: 20px;
                display: inline-block;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .section {{
                margin-bottom: 30px;
            }}
            
            .section h2 {{
                color: #667eea;
                font-size: 24px;
                margin-bottom: 15px;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }}
            
            .section p {{
                color: #555;
                line-height: 1.8;
                font-size: 16px;
            }}
            
            .footer {{
                background: #f9f9f9;
                padding: 20px 40px;
                text-align: center;
                border-top: 1px solid #eee;
            }}
            
            .footer a {{
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }}
            
            .footer a:hover {{
                text-decoration: underline;
            }}
            
            .back-link {{
                display: inline-block;
                margin-bottom: 10px;
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }}
            
            .back-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <a href="/scp" class="back-link">← Back to List</a>
                <h1>SCP-{item_id_db}</h1>
                <div class="object-class">{object_class}</div>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>Containment Procedures</h2>
                    <p>{procedures}</p>
                </div>
                
                <div class="section">
                    <h2>Description</h2>
                    <p>{description}</p>
                </div>
            </div>
            
            <div class="footer">
                <p><a href="/scp">View All SCP Subjects</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content