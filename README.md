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

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/monthly-challenge-tracker.git
    cd monthly-challenge-tracker
    ```

2. Build and run the Docker container:
    ```bash
    docker-compose up --build
    ```

3. Access the app at `http://localhost:8000`.

## Usage

- Create an account using an email address in the whitelist.
- Log in to the dashboard to set and track your goals.
- Use the calendar view to visualize your progress.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.
