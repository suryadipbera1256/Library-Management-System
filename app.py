from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SMTP email configuration (replace with your actual SMTP server details)
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_email_password'
EMAIL_FROM = 'your_email@example.com'
EMAIL_SUBJECT = 'Book Resubmission Reminder'

db.init_app(app)

import models
from models import Book

@app.route('/')
def index():
    search_query = request.args.get('q', '')
    if search_query:
        books = Book.query.filter(
            (Book.title.ilike(f'%{search_query}%')) | (Book.author.ilike(f'%{search_query}%'))
        ).all()
    else:
        books = Book.query.all()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', books=books, current_datetime=current_datetime, search_query=search_query)

def send_email(to_email, subject, body):
    """Send an email using SMTP."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def check_and_notify_overdue_books():
    """Check for overdue books and send notification emails."""
    now = datetime.now()
    overdue_books = []
    books = Book.query.all()
    for book in books:
        if book.added_date and book.duration and book.email:
            try:
                duration_days = int(book.duration)
                due_date = book.added_date + timedelta(days=duration_days)
                if now > due_date:
                    overdue_books.append(book)
            except ValueError:
                # Invalid duration value, skip
                continue

    for book in overdue_books:
        body = f"Dear {book.student_teacher_name},\n\n" \
               f"The book titled '{book.title}' you borrowed is overdue for resubmission.\n" \
               f"Please resubmit it as soon as possible.\n\n" \
               f"Thank you."
        send_email(book.email, EMAIL_SUBJECT, body)

@app.route('/notify_overdue')
def notify_overdue():
    check_and_notify_overdue_books()
    return "Overdue notifications sent."

@app.route('/inbox')
def inbox():
    now = datetime.now()
    overdue_books = []
    books = Book.query.all()
    for book in books:
        if book.added_date and book.duration and book.email:
            try:
                duration_days = int(book.duration)
                due_date = book.added_date + timedelta(days=duration_days)
                if now > due_date:
                    overdue_books.append(book)
            except ValueError:
                continue
    return render_template('inbox.html', overdue_books=overdue_books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        from datetime import datetime
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        student_teacher_name = request.form.get('student_teacher_name')
        department_name = request.form.get('department_name')
        college_name = request.form.get('college_name')
        email = request.form.get('email')
        duration = request.form.get('duration')
        added_date = datetime.now()
        new_book = Book(
            title=title,
            author=author,
            year=year,
            student_teacher_name=student_teacher_name,
            department_name=department_name,
            college_name=college_name,
            email=email,
            duration=duration,
            added_date=added_date
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = request.form['year']
        book.email = request.form.get('email')
        book.duration = request.form.get('duration')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_book.html', book=book)

if __name__ == '__main__':
    import models
    with app.app_context():
        db.create_all()
    app.run(debug=True)
