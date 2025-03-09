from config import HOST, PORT, DEBUG
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from datetime import datetime
import random
import string
import colorsys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

MAX_NAME_LENGTH = 15

# Dictionary to store active rooms
rooms = {}

# Dictionary to keep track of used colors
used_colors = {}


def generate_unique_code(length=6):
    """Generate a random unique room code."""
    while True:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if room_code not in rooms:
            return room_code


def generate_unique_color(room_code):
    """Generate a random unique hex color."""
    while True:
        hue = random.random()  # Random hue between 0 and 1
        saturation = 0.7  # Higher saturation ensures vivid colors
        lightness = 0.5  # Moderate lightness for good contrast

        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
        
        # Convert RGB to hex
        color = "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

        # Check if color is already used
        if color not in used_colors[room_code]:
            return color


@app.route("/", methods=["GET", "POST"])
def home():
    """Render home page and handle room creation/joining."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("name").strip()
        room_code = request.form.get("code").upper()
        is_joining = request.form.get("join")
        is_creating = request.form.get("create")
        
        # Validate name
        if not username:
            return render_template("home.html", error="Please enter your name.", code=room_code, name=username)
        
        if len(username) > MAX_NAME_LENGTH:
            return render_template("home.html", error=f"Name must be less than {MAX_NAME_LENGTH} characters.", code=room_code, name=username)
        
        # Handle room joining
        if is_joining is not None:
            if not room_code:
                return render_template("home.html", error="Please enter a room code.", code=room_code, name=username)
            if room_code not in rooms:
                return render_template("home.html", error="Room does not exist.", code=room_code, name=username)
        
        # Handle room creation
        if is_creating is not None:
            room_code = generate_unique_code()
            rooms[room_code] = {"members": 0, "messages": []}

            used_colors[room_code] = set()
            
        color = generate_unique_color(room_code)
        used_colors[room_code].add(color)

        # Store session data
        session["room"] = room_code
        session["name"] = username
        session["color"] = color
                
        return redirect(url_for("room"))

    return render_template("home.html")


@app.route("/room")
def room():
    """Render the chat room, ensuring user is in a valid room."""
    room_code = session.get("room")
    username = session.get("name")

    # Validate that user has a room and their name, and that the room exists
    if not room_code or not username or room_code not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room_code, messages=rooms[room_code]["messages"])


@socketio.on("message")
def handle_message(data):
    """Handle incoming chat messages."""
    room_code = session.get("room")    

    if room_code not in rooms:
        return
            
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = {
        "name": session.get("name"),
        "color": session.get("color"),
        "timestamp": timestamp,
        "message": data.get("message")
    }
    
    rooms[room_code]["messages"].append(content)

    send(content, to=room_code)  # Broadcast to the room
    
    print(f"{session.get('name')} ({room_code}) at {timestamp}: {data['message']}")


@socketio.on("connect")
def handle_connect(auth):
    """Handle new client connections."""
    room_code = session.get("room")
    username = session.get("name")

    if not room_code or not username:
        return

    if room_code not in rooms:
        leave_room(room_code)
        return
    
    join_room(room_code)

    rooms[room_code]["members"] += 1
        
    emit("update_users", {"count": rooms[room_code]["members"]}, to=room_code)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    send({
        "name": username,
        "message": "has joined the room",
        "timestamp": timestamp,
        "color": session.get("color")
    }, to=room_code)
    
    print(f"{username} joined room {room_code} at {timestamp}")


@socketio.on("disconnect")
def handle_disconnect(reason):
    """Handle client disconnections."""
    room_code = session.get("room")
    username = session.get("name")
    color = session.get("color")

    if not room_code or not username:
        return

    leave_room(room_code)

    if room_code in rooms:
        rooms[room_code]["members"] -= 1
        
        emit("update_users", {"count": rooms[room_code]["members"]}, to=room_code)
        
        if rooms[room_code]["members"] <= 0:
            del rooms[room_code]  # Remove empty room
            
            del used_colors[room_code]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    send({
        "name": username,
        "message": "has left the room",
        "timestamp": timestamp,
        "color": color
    }, to=room_code)
    
    print(f"{username} left room {room_code} at {timestamp}")


@socketio.on("typing")
def handle_typing():
    """Handle typing notifications and broadcast to room."""
    room_code = session.get("room")
    username = session.get("name")
    
    # Broadcast typing event to the room
    emit("user_typing", {"username": username}, to=room_code, include_self=False)


@socketio.on("stop_typing")
def handle_stop_typing():
    """Handle stop typing notifications and broadcast to room."""
    room_code = session.get("room")
    username = session.get("name")

    # Broadcast stop typing event to the room
    emit("user_stopped_typing", {"username": username}, to=room_code, include_self=False)


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG)
