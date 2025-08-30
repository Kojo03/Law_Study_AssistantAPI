# ⚖️ Law Study Assistant API

A comprehensive Django REST Framework API designed for law students and legal professionals. This system provides complete law study functionality including library management, legal case studies, educational content, user management, and study tracking.

---

## 🚀 Features

### 🔐 Authentication & User Management
- **Token-based Authentication** - Secure login with DRF tokens
- **Role-based Access Control** - Member, Librarian, and Administrator roles
- **User Registration & Profile Management** - Complete member profiles with contact information

### 📖 Library Management
- **Book Catalog** - Comprehensive book management with categories
- **Category System** - Organize books by legal specialties
- **Inventory Tracking** - Track total and available copies
- **Location Management** - Shelf location tracking for easy retrieval

### 📚 Circulation System
- **Checkout/Return Operations** - Complete borrowing system
- **Due Date Management** - Automatic 14-day loan periods
- **Fine Calculation** - Automatic overdue fine calculation ($1/day)
- **Reservation System** - Reserve unavailable books
- **Overdue Tracking** - Monitor and manage overdue items

### 📖 Educational Content Management
- **Subject Organization** - Structured legal subjects and topics
- **Study Notes** - Personal note-taking system for each topic
- **Interactive Quizzes** - Multiple-choice quizzes with scoring
- **Progress Tracking** - Monitor quiz attempts and scores

### ⚖️ Legal Case Management
- **Case Database** - Comprehensive legal case repository
- **Case Details** - Title, suit number, citation, and summary
- **Topic Association** - Link cases to relevant study topics
- **Inventory System** - Track physical case document copies

### 🛡️ Security & Quality
- **Permission-based Access** - Role-specific permissions
- **Input Validation** - Comprehensive data validation
- **CORS Support** - Ready for frontend integration
- **Comprehensive Testing** - Full test coverage

---

## 🛠 Tech Stack
- **Framework**: Django 5.2.4 + Django REST Framework 3.15.2
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Authentication**: Token Authentication + JWT (optional)
- **API Documentation**: drf-spectacular (OpenAPI 3.0 + Swagger UI)
- **CORS**: django-cors-headers for frontend integration
- **Environment**: python-decouple for configuration management
- **Static Files**: WhiteNoise for production static file serving
- **Filtering**: django-filter for advanced API filtering

---

## 📂 Project Structure

```
Law_Study_AssistantAPI/
├── accounts/              # User management & authentication
│   ├── models.py         # Enhanced User model with library roles
│   ├── views.py          # Registration, login, profile views
│   ├── serializers.py    # User serialization
│   ├── permissions.py    # Custom permission classes
│   ├── urls.py           # Auth endpoints
│   ├── user_urls.py      # User profile endpoints
│   ├── validators.py     # Input validation utilities
│   └── tests.py          # Authentication tests
├── library/              # Core library management
│   ├── models.py         # Book, Category, Checkout, Reservation, Transaction models
│   ├── views.py          # Library CRUD operations
│   ├── serializers.py    # Library serialization
│   ├── urls.py           # Library endpoints
│   ├── admin.py          # Django admin configuration
│   ├── notifications.py  # Overdue notification system
│   ├── tests.py          # Library management tests
│   └── management/       # Management commands
│       └── commands/
├── books/                # Educational content management
│   ├── models.py         # Subject, Topic, Note, Quiz, Answer models
│   ├── views.py          # Educational content CRUD operations
│   ├── serializers.py    # Educational content serialization
│   ├── urls.py           # Educational content endpoints
│   ├── admin.py          # Django admin configuration
│   └── tests.py          # Educational content tests
├── cases/                # Legal case management
│   ├── models.py         # Case model with topic association
│   ├── views.py          # Case CRUD operations
│   ├── serializers.py    # Case serialization
│   ├── urls.py           # Case endpoints
│   ├── admin.py          # Django admin configuration
│   └── tests.py          # Case management tests
├── Law_Study_AssistantAPI/
│   ├── settings.py       # Django configuration
│   ├── security.py       # Security configurations
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── logs/                 # Application logs
│   └── security.log      # Security-related logs
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database
├── .env                 # Environment variables
└── README.md            # Project documentation
```

---

## 🔌 API Endpoints

### Authentication
```
POST /auth/register/      # User registration
POST /auth/login/         # User login (returns token)
GET  /users/me/           # User profile
GET  /auth/admin/users/   # List all users (Admin)
PUT  /auth/admin/users/{id}/role/  # Update user role (Admin)
```

### Library Management
```
# Categories
GET  /library/categories/              # List all categories
POST /library/categories/              # Create category (Librarian+)
GET  /library/categories/{id}/         # Category details
PUT  /library/categories/{id}/         # Update category (Librarian+)
DELETE /library/categories/{id}/       # Delete category (Admin)

# Books
GET  /library/books/                   # List all books (with filters)
POST /library/books/                   # Create book (Librarian+)
GET  /library/books/{id}/              # Book details
PUT  /library/books/{id}/              # Update book (Librarian+)
DELETE /library/books/{id}/            # Delete book (Admin)

# Circulation
POST /library/checkout/                # Check out a book
POST /library/return/                  # Return a book
GET  /library/my-checkouts/            # View checkout history
GET  /library/overdue/                 # View overdue books
GET  /library/transactions/            # View transaction history

# Reservations
GET  /library/reservations/            # List user's reservations
POST /library/reserve/                 # Reserve a book
GET  /library/reservations/{id}/       # Reservation details
DELETE /library/reservations/{id}/     # Cancel reservation

# Admin Operations
GET  /library/admin/overdue/           # All overdue books (Admin)
POST /library/admin/notifications/     # Send overdue notifications (Admin)
```

### Educational Content
```
# Subjects
GET  /books/subjects/                  # List all subjects
POST /books/subjects/                  # Create subject
GET  /books/subjects/{id}/             # Subject details
PUT  /books/subjects/{id}/             # Update subject
DELETE /books/subjects/{id}/           # Delete subject

# Topics
GET  /books/topics/                    # List all topics
POST /books/topics/                    # Create topic
GET  /books/topics/{id}/               # Topic details
PUT  /books/topics/{id}/               # Update topic
DELETE /books/topics/{id}/             # Delete topic

# Notes
GET  /books/notes/                     # List user's notes
POST /books/notes/                     # Create note
GET  /books/notes/{id}/                # Note details
PUT  /books/notes/{id}/                # Update note
DELETE /books/notes/{id}/              # Delete note

# Quizzes
GET  /books/quizzes/                   # List quizzes by topic
POST /books/quizzes/                   # Create quiz
GET  /books/quizzes/{id}/              # Quiz details
POST /books/quizzes/{id}/attempt/      # Attempt quiz
GET  /books/quiz-attempts/             # User's quiz attempts
```

### Legal Cases
```
GET  /cases/                           # List all cases
POST /cases/                           # Create case
GET  /cases/{id}/                      # Case details
PUT  /cases/{id}/                      # Update case
DELETE /cases/{id}/                    # Delete case
GET  /cases/by-topic/{topic_id}/       # Cases by topic
```

### API Documentation
```
GET  /api/schema/                      # OpenAPI 3.0 schema
GET  /api/docs/                        # Interactive Swagger UI
```

---

## 👥 User Roles & Permissions

### 📖 Library Member (Default)
- Browse books, categories, and cases
- Check out and return books
- Make reservations
- View personal checkout history
- Create and manage personal study notes
- Take quizzes and track progress
- Access educational content
- Access own profile

### 👨🏫 Librarian
- All member permissions
- Create and manage books
- Create and manage categories
- Create and manage legal cases
- Create educational content (subjects, topics, quizzes)
- View all checkouts and reservations
- Manage library inventory
- Send overdue notifications

### 🔧 Administrator
- All librarian permissions
- Delete books, categories, and cases
- Full system administration access
- User management capabilities
- Role assignment and management
- System-wide analytics and reporting

---

## 🗄️ Data Models

### User Management
```python
User (extends AbstractUser)
├── role: CharField (member/librarian/admin)
├── phone_number: CharField
├── address: TextField
├── membership_date: DateField
└── is_active_member: BooleanField
```

### Library System
```python
Category
├── name: CharField (unique)
└── description: TextField

Book
├── title: CharField
├── author: CharField
├── isbn: CharField (unique)
├── published_date: DateField
├── publisher: CharField
├── category: ForeignKey(Category)
├── total_copies: PositiveIntegerField
├── available_copies: PositiveIntegerField
├── description: TextField
├── location: CharField
└── added_date: DateTimeField

BookCheckout
├── user: ForeignKey(User)
├── book: ForeignKey(Book)
├── checkout_date: DateTimeField
├── due_date: DateTimeField
├── return_date: DateTimeField
├── is_returned: BooleanField
└── fine_amount: DecimalField

Reservation
├── user: ForeignKey(User)
├── book: ForeignKey(Book)
├── reservation_date: DateTimeField
├── is_active: BooleanField
└── notified: BooleanField

Transaction
├── user: ForeignKey(User)
├── book: ForeignKey(Book)
├── transaction_type: CharField (checkout/return/reservation)
├── transaction_date: DateTimeField
└── notes: TextField
```

### Educational Content System
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

### Legal Case System
```python
Case
├── topic: ForeignKey(Topic)
├── title: CharField
├── suit_number: CharField (unique)
├── number_of_pages: PositiveIntegerField
├── summary: TextField
├── citation: CharField
├── year: IntegerField
├── total_copies: PositiveIntegerField
└── available_copies: PositiveIntegerField
```

---

## 🧪 Testing

Comprehensive test suite covering:

- **Model Tests**: Data integrity and relationships
- **API Tests**: Endpoint functionality and responses
- **Authentication Tests**: Registration, login, and token handling
- **Permission Tests**: Role-based access control
- **Library Tests**: Book management, checkout/return operations

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test accounts
python manage.py test library
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
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Populate library data**
```bash
python manage.py populate_library_data
```

8. **Run development server**
```bash
python manage.py runserver
```

9. **Access the API**
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
    "username": "member1",
    "email": "member@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "password2": "securepass123",
    "phone_number": "555-0123",
    "address": "123 Main St, City, State"
  }'
```

### Create a Book (Librarian)
```bash
curl -X POST http://127.0.0.1:8000/library/books/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Evidence Law Handbook",
    "author": "Legal Expert",
    "isbn": "9781234567899",
    "published_date": "2023-01-15",
    "publisher": "Law Publishers",
    "category": 1,
    "total_copies": 3,
    "description": "Comprehensive guide to evidence law",
    "location": "H8-042"
  }'
```

### Check Out a Book
```bash
curl -X POST http://127.0.0.1:8000/library/checkout/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1
  }'
```

### Reserve a Book
```bash
curl -X POST http://127.0.0.1:8000/library/reserve/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 2
  }'
```

### Search Books
```bash
# Search by title
curl "http://127.0.0.1:8000/library/books/?title=constitutional"

# Filter available books only
curl "http://127.0.0.1:8000/library/books/?available_only=true"

# Search by category
curl "http://127.0.0.1:8000/library/books/?category=criminal"
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
DATABASE_URL=postgresql://user:password@localhost:5432/lawlibrarydb
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

## 📈 Sample Data

The system includes 7 law book categories and sample books:

### Categories
- Constitutional Law
- Criminal Law
- Contract Law
- Tort Law
- Administrative Law
- International Law
- Corporate Law

### Sample Data

**Library Books:**
1. Constitutional Law Principles (3 copies)
2. Criminal Law Cases (2 copies)
3. Contract Law Fundamentals (4 copies)
4. Tort Law Analysis (1 copy)
5. Administrative Law Guide (5 copies)
6. International Law Treaties (2 copies)
7. Corporate Law Handbook (3 copies)

**Educational Subjects:**
- Constitutional Law
- Criminal Law
- Contract Law
- Tort Law
- Administrative Law
- International Law
- Corporate Law

**Legal Cases:**
- Landmark constitutional cases
- Criminal law precedents
- Contract dispute cases
- Tort liability cases

---

## 🚀 Production Deployment

### Database Migration
```python
# settings.py - Production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lawlibrarydb',
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

### Library Features
- **Digital Resources**: PDF documents and e-books
- **Advanced Search**: Full-text search across content
- **Notification System**: Email/SMS notifications for due dates
- **Reports & Analytics**: Library usage statistics
- **Barcode Integration**: Barcode scanning for books
- **Multi-library Support**: Support for multiple library branches

### Educational Features
- **Video Content**: Integration with video learning materials
- **Study Groups**: Collaborative study features
- **Progress Analytics**: Detailed learning progress tracking
- **Flashcards**: Interactive flashcard system
- **Discussion Forums**: Topic-based discussion boards
- **AI-Powered Recommendations**: Personalized content suggestions

### Case Management
- **Case Analysis Tools**: Built-in case analysis features
- **Citation Management**: Automatic citation generation
- **Case Comparison**: Side-by-side case comparison tools
- **Legal Research**: Integration with legal databases

### Technical Enhancements
- **Mobile App**: Dedicated mobile application
- **Real-time Notifications**: WebSocket-based notifications
- **Advanced Security**: Multi-factor authentication
- **API Rate Limiting**: Enhanced API security
- **Caching**: Redis-based caching for performance