import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import src.database as database
from src.database.auth import router as auth_router





app = fastapi.FastAPI()


app.include_router(database.router)
app.include_router(auth_router)




@app.get("/")
def root():
    return RedirectResponse(url="/login")

