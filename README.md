# GeoWiki

Vector.ai Assignment

## Thought process
Before jumping into the coding, I normally plan, decide on tools,dbs etc.
These tasks are further divided into milestones and tasks.
Tasks are committed only when the delta/changes in the codebase is considerably huge

1. Db, framework, package decisions
2. Setup project(package dependency manager(poetry), pre-commit hooks,README etc.)
Poetry is a cool package manager which is a combination of Pyenv and pip
3. Pre-commit hooks are the best to maintain the standards of the code eg. PEP8 checks,code blunders etc.
It's an overkill for now but, it's a good practice.
4. File Structure - Again may seem like an overkill for now, but some habits die hard.

## Design

As per the assignment, the use-case looks like a classic one-many relationship design
and simple CRUD operations on top of the tables.

I have chosen the async paradigm. Reason is simple - Python is relatively slow and the CRUD operations requires
running multiple SQL queries for one operation. Though the async design can be improved in the code.

FastAPI is a perfect fit for my requirement as
1. it's an ASGI app right out-of-the-box(Starlette)
2. It comes with built-in auto documentation and Pydantic(data validator)
and it's easy to pick up due to its world-class documentation.

The whole code structure can be divided into 2 parts
1. data-store layer(Handles data base connections)
2. Data Access Layer(Handles all data related operations)
3. Pydantic models and routers (Data Validator and API definitions)

## Dependencies
1. docker
2. docker-compose
Application is already dockerized and hence all dependencies are handled.

### Steps to build
1. Navigate into the parent directory and run the following command:
```
docker-compose up -d --build
```
2. The application will be listening to port 80. [link to Swagger UI](http://0.0.0.0/docs#/)

###  Mistakes/ TO-DOs:
1. Move the credentials to a .env file
2. Integrate the API with Db migration tool -[Alembic]("https://alembic.sqlalchemy.org/en/latest/")
3. Better error handling
4. Add logger
5. Better async practices(Eg: We could run Validations and fetching update objects simultaneously )
6. Add proper doc-strings for documentation
