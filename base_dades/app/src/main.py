import fastapi
import src.database as database





app = fastapi.FastAPI()


app.include_router(database.router)




@app.get("/")
def root():
    return {"message":"Hello, world!"}

