# AI based resume screening recruitment

A Django project with 11 models and a REST API (Django REST Framework).

## Tech stack

- Python 3
- Django
- Django REST Framework
- psycopg2 (PostgreSQL)
- Database: PostgreSQL

## Project structure

- `ai_based_resume_screening_recruitment/`: project settings and root URLs
- `screening/`: Django app
- Tests: `screening/tests.py`

## Data model

| Model | App | Fields |
|---|---|---|
| `TimeStampedModel` | `screening` | created_at, updated_at |
| `Applicant` | `screening` | user, full_name, email, phone_number, skills, linkedin_profile |
| `Recruiter` | `screening` | user, company_name, position, contact_email |
| `Job` | `screening` | recruiter, applicants, title, description, required_skills, location, salary_range |
| `Resume` | `screening` | applicant, file, parsed_text, extracted_skills, ai_score |
| `Interview` | `screening` | job, applicant, date, time, mode, status, feedback |
| `ScreeningQuestion` | `screening` | job, question_text, answer_text |
| `ScreeningAnswer` | `screening` | question, applicant, answer_text |
| `Feedback` | `screening` | interview, reviewer, comments, rating |
| `Notification` | `screening` | user, message, is_read |
| `JobApplication` | `screening` | applicant, job, status |

## URL routes

Declared in `urls.py`:

- `/blog/`
- `/applicants/ (router)`
- `/jobs/ (router)`
- `/resumes/ (router)`
- `/interviews/ (router)`
- `/screening-questions/ (router)`
- `/screening-answers/ (router)`
- `/feedback/ (router)`
- `/notifications/ (router)`
- `/applications/ (router)`

## How to run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

`settings.py` is configured for PostgreSQL: create the database and use your own credentials before running `migrate`.

Then open `http://127.0.0.1:8000/`.

---

Author: [Chaouki Bayoudhi](https://github.com/ChaoukiBayoudhi)
