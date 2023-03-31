import uvicorn

from app.routes import app

if __name__ == "__main__":
    uvicorn.run("app.routes:app", host="0.0.0.0", port=4000, workers=2)
