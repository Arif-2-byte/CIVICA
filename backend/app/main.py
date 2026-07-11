from fastapi import FastAPI

app = FastAPI(
    title="CIVICA API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "project": "CIVICA",
        "status": "Running",
        "version": "0.1.0"
    }