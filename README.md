# Django REST Messaging Capstone

## Overview
This project is a small Django REST API that allows users to send messages to each other.  
Each message is displayed in the recipient’s preferred language.

Some parts of the codebase are intentionally buggy or poorly designed.  
Your task is to debug, improve, and fix the implementation.

---

## Features
- Users (Django auth)
- Send messages via REST API
- View received messages (inbox)
- Messages translated to the recipient’s language
- Automated tests using pytest

---

## Endpoints
- `POST /api/messages/` — send a message  
- `GET /api/messages/inbox/` — view received messages

---

## Task
Some logic and tests are intentionally buggy.

Your goals:
- Fix the bugs
- Improve the implementation where needed
- Make all tests pass
- Add at least **2 new tests** covering edge cases
- Ensure the code follows Django and REST best practices

---

## Submission Instructions

1. Fork this repository.
2. Create a new branch named:  
   `fix/<your-name>`
3. Complete the assignment on your branch.
4. Push your changes to your fork.
5. Open a Pull Request back to this repository.

Your Pull Request should include:
- A short summary explaining:
  - What was broken  
  - What you fixed  
  - Why you fixed it that way  

Do not squash commits — commit history will be reviewed.

---

## What Happens Next

After you open your Pull Request, you will be invited to a technical interview.

In the interview, you will:
- Walk through your Pull Request  
- Explain the bugs you found and how you fixed them  
- Discuss your design and implementation choices  
- Answer follow-up questions based on your code  

This session is focused on understanding how you think and reason about problems.

---

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
pytest
python manage.py runserver
