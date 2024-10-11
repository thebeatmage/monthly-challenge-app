# Monthly Challenge Tracker

This is a Django-based web application for creating and tracking monthly challenges with friends. It allows users to set goals, track their progress, and engage in friendly competition based on goal completion rates. The project is designed with a modern aesthetic and includes features like a calendar view, goal management, and personalized dashboards.

## Features

- **User Accounts**: Invite-only signups with a whitelist-based email verification.
- **Goal Tracking**: Set daily goals and track them on a calendar view.
- **Progress Dashboard**: View goal completion statistics for the week and month.
- **Challenge Management**: Create and manage challenges, and view challenge completion rates.
- **Admin Management**: Manage whitelisted emails directly from the admin panel.

## Tech Stack

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: PostgreSQL
- **Deployment**: Docker for containerized deployment

## Configuration

The application uses a .env file to manage sensitive information like secret keys, database credentials, and allowed hosts. Ensure that you create a .env file in the project root directory with the required configuration variables.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/monthly-challenge-tracker.git
    cd monthly-challenge-tracker
    ```
2. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate  # For Windows: `env\Scripts\activate`
    ```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
 4. Apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Create a superuser for admin access:

    '''bash
    python manage.py createsuperuser

6. Run the server:

    ```bash
    python manage.py runserver
    ```
7. Build and run the Docker container:

    ```bash
    docker-compose up --build
    ```

8. Access the app at `http://localhost:8000`.

## Usage

- Logged in as Superuser, add your friends' email address to the whitelist.
- Signup, Login, and set and track your goals!
- Use the calendar view to visualize your progress.

## Features to Come / To-Dos:

- Leaderboards
- Achievements
- Group Goals and Challenges

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.
