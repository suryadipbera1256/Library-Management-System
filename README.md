# Library Management System

This is a simple Library Management System web application built with Flask and Flask-SQLAlchemy.

## Features

- Add, update, delete books in the library.
- Search books by title or author.
- Send automated email notifications for overdue books.
- View inbox of students who have overdue books.
- Responsive and styled UI with a logo and navigation bar.

## Setup Instructions

1. Clone the repository.

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Configure SMTP email settings in `app.py`:

Replace the placeholder SMTP server, port, username, password, and email addresses with your actual email service credentials.

5. Initialize the database:

```bash
python create_db.py
```

6. Run the application:

```bash
python app.py
```

7. Access the app in your browser at `http://127.0.0.1:5000/`.

## Usage

- Use the navigation bar to add books, view the inbox, and send overdue notifications.
- Search for books using the search bar.
- Overdue notifications are sent via email to the borrowers.

## License

This project is licensed under the MIT License.

## Author

Suryadip Bera
