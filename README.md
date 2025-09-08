# Engineering Assessment

Starter project to use for the engineering assessment exercise

## Requirements

- Docker
- docker compose

## Getting started

Build the docker container and run the container for the first time
`docker compose up`

Rebuild the container after adding any new packages
` docker compose up --build`

The run command script creates a super-user with username & password picked from `.env` file

To seed the database with sample quizzes, users, and invitations:

```sh
python manage.py seed_quiz_data
```

## Models Overview

- **Quiz**: Represents a quiz, with a name, description, creator, and questions.
- **Question**: Belongs to a quiz, contains the question text and related answers.
- **Answer**: Belongs to a question, contains answer text and whether it is correct.
- **QuizInvitation**: Invitation for a user to participate in a quiz. Tracks acceptance.
- **QuizParticipation**: Tracks a user's participation in a quiz, including progress and score.
- **QuizAnswer**: Stores answers given by a participant for each question.

## API Endpoints & Logic

All endpoints require authentication. Use the seeded users (`creator`/`pass`, `participant`/`pass`) for testing.

- **Quizzes** (`/api/quizzes/`)

  - `GET`: List quizzes relevant to the user (created, invited, or participating).
  - `POST`: Create a quiz with nested questions and answers.
    - Example payload:
      ```json
      {
        "name": "Math Quiz",
        "description": "Basic math questions",
        "questions": [
          {
            "text": "What is 2+2?",
            "answers": [
              { "text": "3", "is_correct": false },
              { "text": "4", "is_correct": true }
            ]
          }
        ]
      }
      ```
  - `progress` action: `/api/quizzes/{id}/progress/` — See all participants' progress.
  - `scores` action: `/api/quizzes/{id}/scores/` — See all participants' scores.

- **Participations** (`/api/participations/`)

  - `GET`: List participations for the current user.
  - `progress` action: `/api/participations/{id}/progress/` — See your progress in a quiz.

- **Invitations** (`/api/invitations/`)
  - `GET`: List invitations for the current user.
  - `accept` action: `/api/invitations/{id}/accept/` — Accept an invitation (creates a participation).

## Admin Interface

Access `/admin/` for full management of quizzes, questions, answers, invitations, participations, and answers. Inline editing is enabled for questions and answers.

## API Documentation

Interactive documentation is available at:

- `/api/swagger/`
- `/api/redoc/`

## Testing

Run tests with:

```sh
python manage.py test
```

## Notes

- Only invited users can participate in a quiz.
- Accepting an invitation automatically creates a participation record.
- All progress and scores are tracked per user and per quiz.

## Extending

- Add more sample data by editing `seed_quiz_data.py`.
- Expand tests in `quiz/tests.py` for more coverage.
- Add custom permissions or business logic as needed.
