# Tic-Tac-Toe

This is a REST API for playing Tic-Tac-Toe against a computer.

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    python manage.py runserver
    ```
    
## API Endpoints

- `POST /api/games/`: Create a new game.
- `POST /api/games/<game_id>/movements/`: Make a move in a game.
- `GET /api/games/<game_id>/`: Get the state of a game.
- `GET /api/games/`: List all games.
- `GET /api/games/<game_id>/movements/`: List all movement of a specific game.

## Time Spent

Approximately 4 hours.
The first hour was spent thinking about the game logic and overall structure. The second hour involved implementing the planned logic and creating the models, serializers, and views. Finally, the last two hours were dedicated to performing manual tests to verify functionality and creating unit tests.

## Assumptions

- The opponent makes random moves.
- The game logic is implemented in the `logic.py` file.
- The game and movement data are stored using Django's ORM.

## Trade-offs

- No persistent storage for simplicity.

## Special Features

- Validation for moves.
- Simple winner detection.

## Tests

There are test for models, serializers and views. To run the test use the command:

    python manage.py test

## Feedback

This was an interesting challenge! It allowed me to demonstrate my skills in designing a REST API and implementing game logic in Python.
