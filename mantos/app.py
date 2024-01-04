from fastapi import FastAPI

from mantos.routers import club

app = FastAPI()

app.include_router(club.router)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}
