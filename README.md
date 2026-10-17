# Job Application Tracker API

I built this API while learning backend development to prepare for software engineering interviews. I was applying to jobs myself, so I wanted a project that solves a real problem for me: keeping track of where I applied and what stage each application is at.

It lets you add job applications, update their status as they move through the hiring process, filter them by status, and delete them. The data is stored in PostgreSQL and the API is deployed on Render.

**Live API docs:** https://job-application-tracker-api-bh3z.onrender.com/docs

> It's on Render's free plan, so the first request after some inactivity can take 30–60 seconds while the server wakes up.

## What it can do

- Add, view, update and delete job applications
- Track each application's status: `Applied`, `Interview`, `Offer`, `Rejected`
- Filter applications by status, e.g. `/applications?status=Interview`
- Reject bad input with clear errors (empty company, unknown status → `422`)
- Return the right status codes (`200`, `201`, `404`, `422`)
- Keep data safe in PostgreSQL, so nothing is lost when the server restarts

## Built with

Python 3.13 · FastAPI · PostgreSQL · SQLAlchemy · Pydantic · Render

## Endpoints

| Method | Endpoint | What it does | Success |
|---|---|---|---|
| GET | `/applications` | List all applications (optional `?status=`) | 200 |
| GET | `/applications/{id}` | Get one application | 200 |
| POST | `/applications` | Add an application | 201 |
| PATCH | `/applications/{id}` | Update the status | 200 |
| DELETE | `/applications/{id}` | Delete an application | 200 |

If the id doesn't exist, you get `404`. If the input is invalid, you get `422`.

Example: `POST /applications` with `{"company": "Google", "role": "SDE Intern"}` returns:

```json
{"id": 1, "company": "Google", "role": "SDE Intern", "status": "Applied"}
```

## Mistakes I made along the way

**Three applications with the same id**
In my first POST endpoint, I let the user send the id. In Swagger the id field was 0 by default, and I clicked Execute a few times without changing it. Three applications ended up with id 0, and when I called GET /applications/0, I only ever got the first one. The others were basically lost. That's when I understood that the user shouldn't decide the id at all. I made a separate model with only company and role, and let the server set the id and the "Applied" status.

**Ids repeating after a delete**
After that, I used len(applications) + 1 for the next id. It looked fine until I deleted an application from the middle. The list got shorter, so the next new application got an id that already existed. I only noticed because I tested the steps one by one: add, add, delete, add. I changed it to "biggest id + 1", and later PostgreSQL took care of this completely with auto-increment.

**My update worked for id 1 but not id 2**
This one confused me for a while. Updating application 1 worked, but application 2 kept giving 404 even though it existed. The problem was one indentation level: my "not found" error was inside the for loop, so the loop stopped after checking just the first item. Now when I search through a list, I always check that the "not found" part comes after the loop, not inside it.

**Getting 500 instead of 422**
I added a rule that the company name can't be empty, but I put it on the wrong Pydantic model. So an empty company didn't get rejected at the start. It went into my code and crashed it, and the API returned 500. Moving the rule to the request model fixed it, and now the user gets a 422 that tells them what's wrong. It made me realise a 500 means my code broke, while a 422 means the user sent bad data, and the user should never see the first one for something like this.

**Everything disappeared on restart**
For a long time my data was just a Python list, so every time I saved a file and the server reloaded, all my test applications were gone. Moving to PostgreSQL with SQLAlchemy was the hardest part of the project for me, but it was worth it. The first time I stopped the server, started it again, and my data was still there felt really good.

## Project structure

```
main.py        # API endpoints
models.py      # Pydantic models (what the API accepts and returns)
db_models.py   # SQLAlchemy table definition
database.py    # Database connection and sessions
```

## Run it locally

```bash
git clone https://github.com/shubhamkrjha09/job-application-tracker-api.git
cd job-application-tracker-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure PostgreSQL is running and has a database called `jobtracker`. By default the app connects to it on `localhost`. To use a different database, set:

```bash
export DATABASE_URL="postgresql+psycopg://USER@localhost:5432/jobtracker"
```

Then start the server and open http://127.0.0.1:8000/docs:

```bash
fastapi dev main.py
```

## What I'd add next

- Automated tests with pytest
- User accounts with login, so each person sees only their own applications
- Docker setup
