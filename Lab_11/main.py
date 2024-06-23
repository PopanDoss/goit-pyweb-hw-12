from fastapi import FastAPI

from routes.contacts import router as contact_router
from routes.users import router as users_router

app = FastAPI()

app.include_router(contact_router, prefix='/api')
app.include_router(users_router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}