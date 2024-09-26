import uvicorn
import dotenv

from fastapi import FastAPI
from database import dependencies, orm
from src.author.http import author
from src.book.http import book

orm.Base.metadata.create_all(bind=dependencies.engine)


def create_app() -> FastAPI:
    app = FastAPI(title="Library Service", docs_url="/v1/docs")

    app.include_router(author.router)
    app.include_router(book.router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
