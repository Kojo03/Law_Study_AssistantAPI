# 📚 Law Study Assistant API

A comprehensive Django REST Framework API designed to streamline legal education. This backend system provides a robust foundation for law study applications with role-based access control, content management, and interactive learning features.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- **Token-based Authentication** - Secure login with DRF tokens
- **Role-based Access Control** - Student, Lecturer, and Admin roles
- **User Registration & Profile Management**

### 📖 Content Management
- **Hierarchical Organization** - Subjects → Topics → Content
- **Legal Case Database** - Store cases with citations and summaries
- **Personal Notes System** - User-specific note-taking
- **Interactive Quizzes** - Multiple-choice questions with scoring

### 🛡️ Security & Quality
- **Permission-based Access** - Different permissions for different roles
- **Input Validation** - Comprehensive data validation
- **CORS Support** - Ready for frontend integration
- **Comprehensive Testing** - 13 test cases with 100% pass rate

---

## 🛠 Tech Stack
- **Framework**: Django 5.2.4 + Django REST Framework 3.15.2
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Authentication**: Token Authentication
- **API Documentation**: drf-spectacular (OpenAPI 3.0 + Swagger UI)
- **CORS**: django-cors-headers for frontend integration
- **Environment**: python-decouple for configuration management

---

## 📂 Project Structure

```
Law_Study_AssistantAPI/
├── accounts/              # User management & authentication
│   ├── models.py         # Custom User model with roles
│   ├── views.py          # Registration, login, profile views
│   ├── serializers.py    # User serialization
│   ├── permissions.py    # Custom permission classes
│   ├── urls.py           # Auth endpoints
│   ├── user_urls.py      # User profile endpoints
│   └── tests.py          # Authentication tests
├── books/                # Educational content management
│   ├── models.py         # Subject, Topic, Note, Quiz models
│   ├── views.py          # Content CRUD operations
│   ├── serializers.py    # Content serialization
│   ├── urls.py           # Content endpoints
│   └── tests.py          # Content management tests
├── cases/                # Legal case management
│   ├── models.py         # Case model
│   ├── views.py          # Case CRUD operations
│   ├── serializers.py    # Case serialization
│   ├── urls.py           # Case endpoints
│   └── tests.py          # Case management tests
├── Law_Study_AssistantAPI/
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database
└── README.md            # Project documentation
```

---

## 🔌 API Endpoints

### Authentication
```
POST /auth/register/      # User registration
POST /auth/login/         # User login (returns token)
GET  /users/me/           # User profile
```

### Content Management
```
# Subjects
GET  /books/subjects/              # List all subjects
POST /books/subjects/              # Create subject (Lecturer+)
GET  /books/subjects/{id}/         # Subject details

# Topics
GET  /books/subjects/{id}/topics/  # List topics for subject
POST /books/subjects/{id}/topics/  # Create topic (Lecturer+)
GET  /books/topics/{id}/           # Topic details

# Notes
GET  /books/notes/                 # User's personal notes
POST /books/topics/{id}/notes/     # Create note for topic
GET  /books/notes/{id}/            # Note details
PUT  /books/notes/{id}/            # Update note
DELETE /books/notes/{id}/          # Delete note

# Quizzes
GET  /books/topics/{id}/quiz/      # Get quiz for topic
POST /books/quiz/attempt/          # Submit quiz attempt
GET  /books/quiz/attempts/         # Quiz history
```

### Legal Cases
```
GET  /cases/topics/{id}/cases/     # List cases for topic
POST /cases/topics/{id}/cases/     # Create case (Lecturer+)
GET  /cases/{id}/                  # Case details
```

### API Documentation
```
GET  /api/schema/                  # OpenAPI 3.0 schema
GET  /api/docs/                    # Interactive Swagger UI
```

---

## 👥 User Roles & Permissions

### 🎓 Student (Default)
- View all subjects, topics, and cases
- Create and manage personal notes
- Take quizzes and view attempt history
- Access own profile

### 👨🏫 Lecturer
- All student permissions
- Create and manage subjects and topics
- Create and manage legal cases
- Create quizzes with multiple-choice answers

### 🔧 Admin
- All lecturer permissions
- Full system administration access
- User management capabilities

---

## 🗄️ Data Models

### User Management
```python
User (extends AbstractUser)
├── role: CharField (student/lecturer/admin)
└── Standard Django user fields
```

### Content Hierarchy
```python
Subject
├── title: CharField
└── description: TextField

Topic
├── subject: ForeignKey(Subject)
├── title: CharField
└── description: TextField

Note
├── user: ForeignKey(User)
├── topic: ForeignKey(Topic)
├── content: TextField
└── created_at: DateTimeField

Case
├── topic: ForeignKey(Topic)
├── title: CharField
├── summary: TextField
├── citation: CharField
└── year: IntegerField
```

### Quiz System
```python
Quiz
├── topic: ForeignKey(Topic)
└── question: TextField

Answer
├── quiz: ForeignKey(Quiz)
├── text: CharField
└── is_correct: BooleanField

QuizAttempt
├── user: ForeignKey(User)
├── topic: ForeignKey(Topic)
├── score: IntegerField
└── attempted_at: DateTimeField
```

---

## 🧪 Testing

Comprehensive test suite with **13 tests** covering:

- **Model Tests**: Data integrity and relationships
- **API Tests**: Endpoint functionality and responses
- **Authentication Tests**: Registration, login, and token handling
- **Permission Tests**: Role-based access control

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test accounts
python manage.py test books
python manage.py test cases
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Law_Study_AssistantAPI
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment setup**
```bash
# Create .env file with:
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. **Database setup**
```bash
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the API**
- API Base URL: `http://127.0.0.1:8000/`
- Swagger Documentation: `http://127.0.0.1:8000/api/docs/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

---

## 📊 API Usage Examples

### User Registration
```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }'
```

### User Login
```bash
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "securepass123"
  }'
```

### Create a Note (Authenticated)
```bash
curl -X POST http://127.0.0.1:8000/books/topics/1/notes/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Important notes about constitutional law"
  }'
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/lawstudydb
```

### CORS Settings
Configure allowed origins in `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React dev server
    "http://127.0.0.1:3000",
    "https://yourdomain.com",   # Production frontend
]
```

---

## 🚀 Production Deployment

### Database Migration
```python
# settings.py - Production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lawstudydb',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Security Settings
```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the [API documentation](http://127.0.0.1:8000/api/docs/) for endpoint details
- Review the test files for usage examples

---

## 🔮 Future Enhancements

- **File Upload**: PDF documents and case files
- **Search Functionality**: Full-text search across content
- **Discussion Forums**: Student collaboration features
- **Progress Tracking**: Learning analytics and reports
- **Mobile API**: Enhanced mobile app support
- **Caching**: Redis integration for improved performance
