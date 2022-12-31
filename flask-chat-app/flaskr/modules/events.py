from flaskr import socketio
from flask_socketio import emit
from flask import session
from flask_socketio import emit, join_room, leave_room

@socketio.on('joined', namespace='/chat')
def joined(data):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print('\n[SERVER] Successful connection with client\n\n')

    # store client room and add client to room
    room = session.get('room')
    join_room(room)

    # emit notification to all clients about new user joining the room
    emit('status', {'user':data['user'], 'status':' the joined room'}, to=room)

@socketio.on('message', namespace='/chat')
def message(data):
    """receive username and message from client and emit it to all clients"""
    room = session.get('room')

    print(f"\n{data['user']} sent a message\n")
    emit('message', {'user':data['user'], 'msg':data['userMsg']}, to=room)

@socketio.on('left', namespace='/chat')
def left(data):
    """receive event when user leaves a room and notify clients about it"""
    room = session.get('room')
    
    leave_room(room)
    emit('status', {'user':data['user'], 'status':' left the room'}, to=room)
