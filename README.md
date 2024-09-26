# FastAPI Library Management service


## API Endpoints

### Authors
1. `POST /authors`: Create author
2. `PUT /authors/:author_id`: Update author by ID
3. `DELETE /authors/:author_id`: Delete author by ID
4. `GET /authors/:author_id`: Get author by ID
5. `GET /authors`: List all authors
6. `GET /authors/:author_id/books`: List all books by specific author ID

### Books
1. `POST /books`: Create book
2. `PUT /books/:book_id`: Update book by ID
3. `DELETE /books/:book_id`: Delete book by ID
4. `GET /books/:book_id`: Get book by ID
5. `GET /books`: List all books


## Tech Stack & Frameworks

- Python with FastAPI framework
- PostgreSQL database with Alembic migration for database schema and management
- Docker for containerization with Docker Compose for multiple containers
- Redis for caching implementation to improve reading performance


## How to run

1.  Start the service by running below command:
    ```
    sudo docker compose up
    ```


## How to test

1. When the service starts, unit tests are already run before application deployment to ensure everything works correctly, so manual pytest execution is not necessary.
2. For convenience, if manual testing feels needed, start the service first, then access http://0.0.0.0:8000/v1/docs for Swagger API testing.


## Database Schema

```
class Author(DateTimeMixin):
    __tablename__ = "author"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    birth_date = Column(Date, nullable=False)

class Book(DateTimeMixin):
    __tablename__ = "book"

    id = Column(String, primary_key=True, default=generate_uuid)
    author_id = Column(String, ForeignKey("author.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    publish_date = Column(Date, nullable=False)
```
