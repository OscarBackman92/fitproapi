# FitproAPI - Social Fitness Tracking API

[View the API](your-deployed-api-url)
[View Frontend Repository](your-frontend-repo-url)

## Table of Contents

- [Introduction](#introduction)
- [Purpose and Goals](#purpose-and-goals)
- [User Stories](#user-stories)
- [API Integration](#api-integration)
  - [API Endpoints](#api-endpoints)
  - [CRUD Functionality](#crud-functionality)
- [Agile Development](#agile-development)
- [Database Design](#database-design)
  - [ERD](#erd)
  - [Models](#models)
- [Testing](#testing)
  - [Manual Testing](#manual-testing)
  - [Automated Testing](#automated-testing)
  - [Validation](#validation)
- [Set Up and Deployment](#set-up-and-deployment)
  - [Local Setup](#local-setup)
  - [Heroku Deployment](#heroku-deployment)
- [Technologies](#technologies)
- [Credits](#credits)

## Introduction

FitproAPI is a comprehensive Django REST Framework-based API designed to power social fitness applications. It provides a robust backend for tracking workouts, sharing fitness achievements, and building a community through social interactions.

## Purpose and Goals

- Create a secure and scalable fitness tracking backend
- Enable detailed workout logging and progress monitoring
- Foster community engagement through social features
- Ensure user data privacy and security
- Support seamless frontend integration
- Provide comprehensive API documentation

## User Stories

### Authentication & Profiles

1. As a new user, I want to register for an account

   ```

   Acceptance Criteria:
   - Create username and password
   - Automatic profile creation
   - Upload profile image
   - Set basic profile information
   ```

2. As a registered user, I want to manage my profile

   ```
   Acceptance Criteria:
   - Edit profile details
   - Update profile image
   - View my activities
   - Control privacy settings
   ```

### Workouts

3. As a fitness enthusiast, I want to log workouts

   ```
   Acceptance Criteria:
   - Create workout entries
   - Specify type, duration, intensity
   - Add workout notes
   - Edit/delete my workouts
   ```

4. As a user, I want to track my progress

   ```

   Acceptance Criteria:
   - View workout history
   - Filter by workout type
   - See workout statistics
   - Monitor improvement
   ```

### Social Features

5. As a community member, I want to share achievements

   ```
   Acceptance Criteria:
   - Post workouts
   - Add descriptions
   - Share progress
   - Get community feedback
   ```

6. As a user, I want to engage with others

   ```
   Acceptance Criteria:
   - Follow other users
   - Like posts
   - Comment on posts
   - View activity feed
   ```

## API Integration

### API Endpoints

<details>
<summary>Authentication Endpoints</summary>

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/dj-rest-auth/registration/` | Register user | No |
| POST | `/dj-rest-auth/login/` | Login | No |
| POST | `/dj-rest-auth/logout/` | Logout | Yes |
| POST | `/dj-rest-auth/token/refresh/` | Refresh token | Yes |

</details>

<details>
<summary>Workout Endpoints</summary>

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET/POST | `/api/workouts/` | List/Create workouts | No/Yes |
| GET/PUT/DELETE | `/api/workouts/{id}/` | Retrieve/Update/Delete | View: No, Edit: Yes |

</details>

<details>
<summary>Social Interaction Endpoints</summary>

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET/POST | `/api/posts/` | List/Create posts | No/Yes |
| GET/POST | `/api/likes/` | List/Create likes | No/Yes |
| GET/POST | `/api/comments/` | List/Create comments | No/Yes |
| GET/POST | `/api/followers/` | List/Create followers | No/Yes |

</details>

### CRUD Functionality

<details>
<summary>Extended CRUD Operations</summary>

1. Workout Operations

```python
# Create
POST /api/workouts/
{
    "title": "Morning Run",
    "workout_type": "cardio",
    "duration": 30,
    "intensity": "moderate",
    "notes": "5k run",
    "date_logged": "2024-03-14"
}

# Read
GET /api/workouts/
GET /api/workouts/{id}/

# Update
PUT /api/workouts/{id}/
{
    "title": "Updated Run",
    "duration": 45
}

# Delete
DELETE /api/workouts/{id}/
```

2. Post Operations
[Similar CRUD examples for posts]

3. Comment Operations
[CRUD examples for comments]

4. Like Operations
[CRUD examples for likes]

</details>

## Agile Development

Project tracked via GitHub Projects Kanban board: [FitproAPI Board](https://github.com/users/OscarBackman92/projects/11/views/1)

![kanban](/readme_images/kanban_fitness.png)

Categories:

- Backlog
- To Do
- In Progress
- Done

Labels:

- Priority (Must Have, Should Have, Could Have)
- Type (Feature, Bug, Enhancement)
- Sprint number
- Story points

## Database Design

### ERD

![ERD](/readme_images/fitpro_ERD.png)

### Models

<details>
<summary>Model Documentation</summary>

1. **Workout Model**

```python
class Workout(models.Model):
    """Tracks individual workout sessions with type, intensity and duration"""
    CARDIO = 'cardio'
    STRENGTH = 'strength'
    FLEXIBILITY = 'flexibility'
    SPORTS = 'sports'
    OTHER = 'other'

    WORKOUT_TYPES = [
        (CARDIO, 'Cardio'),
        (STRENGTH, 'Strength Training'),
        (FLEXIBILITY, 'Flexibility'),
        (SPORTS, 'Sports'),
        (OTHER, 'Other'),
    ]

    LOW = 'low'
    MODERATE = 'moderate'
    HIGH = 'high'

    INTENSITY_LEVELS = [
        (LOW, 'Low'),
        (MODERATE, 'Moderate'),
        (HIGH, 'High'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    workout_type = models.CharField(max_length=100, choices=WORKOUT_TYPES)
    date_logged = models.DateField(default=timezone.now)
    duration = models.IntegerField()
    intensity = models.CharField(max_length=20, choices=INTENSITY_LEVELS)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)]
```

2. **WorkoutPost Model**

```python
[class WorkoutPost(models.Model):
    """Represents shared workouts in the social feed"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.OneToOneField(
        Workout,
        on_delete=models.CASCADE,
        related_name='post'
    )
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)]
```

3. **Profile Model**

```python
[class Profile(models.Model):
    """Extends User model with additional profile information"""
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/',
        default='../default_profile_qdjgyp'
    )]
```

4. **Like Model**

```python
[class Like(models.Model):
    """Records likes on workout posts"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        WorkoutPost,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'post']]
```

5. **Comment Model**

```python
[class Comment(models.Model):
    """Stores comments on workout posts"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        WorkoutPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
]
```

6. **Follower Model**

```python
class Follower(models.Model):
    """Manages user following relationships"""
    owner = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User,
        related_name='followed',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'followed']]
```

</details>

## Testing

### Manual Testing

- User flow verification
- Error handling validation

### Automated Testing

```bash
python manage.py test
```

### Validation

<details>
<summary>PEP8 Validation</summary>
![fitpro](/readme_images/view_fitpro.png)

![fitpro](/readme_images/fitpro_urls.png)

![fitpro](/readme_images/serializer_fitpro.png)

![fitpro](/readme_images/followers_models.png)

![fitpro](/readme_images/followers_serializer.png)

![fitpro](/readme_images/followers_test.png)

![fitpro](/readme_images/followers_urls.png)

![fitpro](/readme_images/followers_view.png)

![fitpro](/readme_images/like_models.png)

![fitpro](/readme_images/likes_serializer.png)

![fitpro](/readme_images/likes_test.png)

![fitpro](/readme_images/likes_views.png)

![fitpro](/readme_images/likes_urls.png)

![fitpro](/readme_images/post_model.png)

![fitpro](/readme_images/post_serializer.png)

![fitpro](/readme_images/post_test.png)

![fitpro](/readme_images/post_urls.png)

![fitpro](/readme_images/post_view.png)

![fitpro](/readme_images//workout_model.png)

![fitpro](/readme_images/workout_serializer.png)

![fitpro](/readme_images/workout_test.png)

![fitpro](/readme_images/workout_urls.png)

![fitpro](/readme_images/workout_view.png)

![fitpro](/readme_images/profile_model.png)

![fitpro](/readme_images/profile_test.png)

![fitpro](/readme_images/profile_urls.png)

![fitpro](/readme_images/profile_view.png)

![fitpro](/readme_images/profiles_serializer.png)

</details>

## Set Up and Deployment

### Local Setup

```bash
git clone [repository-url]
cd fitproapi
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Heroku Deployment

1. **Project Setup**

```bash
mkdir staticfiles
pip freeze > requirements.txt
```

2. **Create Procfile**

```
release: python manage.py makemigrations && python manage.py migrate
web: gunicorn fitapi.wsgi
```

3. **Heroku Configuration**
   - Create new Heroku app
   - Configure Config Vars:
     - DATABASE_URL: Your database URL
     - SECRET_KEY: Your secret key
     - CLOUDINARY_URL: Your Cloudinary URL
     - ALLOWED_HOSTS: Your app's hostname
     - CLIENT_ORIGIN: Frontend URL
     - CLIENT_ORIGIN_DEV: Development frontend URL
   - Connect GitHub repository
   - Deploy main branch

4. **Important Settings**
   - DEBUG=False for production
   - Configure CORS settings
   - Set up database connection
   - Configure static files

## Technologies

### Languages

- Python 3.11+

### Development Tools

- Git/GitHub
- Visual Studio Code

### Libraries and Frameworks

- Django 5.1.2
- Django REST Framework 3.15.2
- PostgreSQL
- Cloudinary
- JWT Authentication
- django-allauth
- dj-rest-auth
- django-cors-headers
- gunicorn

## Credits

- Django REST Framework documentation
- Stack Overflow community