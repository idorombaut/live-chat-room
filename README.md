# Real-Time Chat Application

This is a real-time chat application built using Flask and Socket.IO. It allows users to create or join chat rooms, send messages, and see real-time updates like typing indicators and user presence.

## Demo Chat Example

![Home](https://github.com/idorombaut/live-chat-room/blob/main/screenshots/home.png)

![Chat Room](https://github.com/idorombaut/live-chat-room/blob/main/screenshots/chat_room.png)

![Chatting 1](https://github.com/idorombaut/live-chat-room/blob/main/screenshots/chatting1.png)

![Chatting 2](https://github.com/idorombaut/live-chat-room/blob/main/screenshots/chatting2.png)

![Chatting 3](https://github.com/idorombaut/live-chat-room/blob/main/screenshots/chatting3.png)

## Features
- Responsive Design – Works seamlessly on both desktop and mobile devices.
- Room-Based Chat – Users can create or join chat rooms using a unique room code.
- Real-Time Messaging – Messages are instantly delivered using WebSockets.
- Typing Indicators – Displays when users are typing in a chat room.
- User Presence – Shows the number of active users in a room in real time.
- Automatic Room Cleanup – Rooms are deleted when they become empty.
- Unique User Colors – Each user gets a randomly assigned color per room for better distinction.

## Installation

### Prerequisites
Ensure you have Python 3.7+ installed.

### Steps
1. Clone this repository:
   ```
   git clone https://github.com/idorombaut/live-chat-room.git
   cd chat-app
   ```
2. Set up a virtual environment:
   - On Windows (Command Prompt):
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux (Terminal):
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Access the chat on any device:
   - On Desktop: Open a browser and go to:
     ```
     http://localhost:8080
     ```
   - On Mobile: If on the same Wi-Fi, access the chat from your phone using the server's IP address:
     ```
     http://<your-local-ip>:8080
     ```

## Configuration
You can modify config.py to change the host, port, and debug mode.

## Usage
- Enter a username.
- Either enter an existing Room Code or click Create Room.
- Start chatting in real time!

## Technologies Used
- Flask (for backend)
- Flask-SocketIO (for real-time messaging)
- HTML, CSS, JavaScript (for frontend)
