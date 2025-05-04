# Live Chat Web Application

A real-time chat application built with Django and Django Channels, featuring video calls and user authentication.

## Features

- User Authentication (Register, Login, Logout)
- Real-time Text Chat
- Video Call functionality
- User Profiles
- Multiple Chat Rooms
- Online User Status
- Responsive Design

## Screenshots

Here are some screenshots of the application in action:

### Chat Room Interface
![Chat Room Interface](/demo/chat.png)
*Chat room interface showing real-time messaging and online users*

### Video Call Feature
![Video Call](/demo/videocall.png)
*One-on-one video call interface with controls*

### User Authentication
![Login Screen](/demo/login.png)
*User login screen with email authentication*

### Room Creation
![Room Creation](/demo/room.png)
*Create or join chat rooms with persistent history*

## Tech Stack

- Django 5.0.6
- Django Channels 4.1.0
- Redis (for WebSocket backend)
- Bootstrap 4
- JavaScript (WebRTC for video calls)

## Prerequisites

- Python 3.x
- Redis Server
- Virtual Environment

## Setup Instructions

1. Clone the repository
```bash
git clone <repository-url>
cd Live-Chat-Webapp
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup Redis Server
- Install Redis (required for Django Channels)
- Ensure Redis server is running on localhost:6379

5. Database Setup
```bash
python manage.py migrate
```

6. Create a superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

The application will be available at http://localhost:8000

## Project Structure

```
├── authapp/                 # Authentication application
│   ├── models.py           # Custom user model
│   ├── views.py            # Authentication views
│   └── templates/          # Auth-related templates
├── chatapp/                # Main chat application
│   ├── consumers/          # WebSocket consumers
│   ├── static/             # Static files
│   └── templates/          # Chat templates
└── chatproject/            # Project configuration
```

## Environment Variables

Create a `.env` file in the project root with the following variables:
```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Features Description

### Authentication
- Email-based authentication
- Custom user model with profile pictures
- User profile management

### Chat Features
- Real-time messaging using WebSockets
- Create and join chat rooms
- Message history
- User online status

### Video Call Features
- WebRTC-based video calls
- One-on-one video chat
- Toggle audio/video
- End call functionality

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
