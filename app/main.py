from fastapi import FastAPI


app = FastAPI(title="FastAPI DevOps Example")


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"message": "Hello World 2, pois essa é uma nova versão!"}