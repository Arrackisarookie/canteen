import json

from canteen.model import Room

with open("resource/rooms.json", "r", encoding="utf-8") as f:
    raw_rooms = json.load(f)
rooms: dict[str, Room] = {
    room_id: Room(room_id) for room_id in raw_rooms
}

with open("resource/index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

with open("resource/pages/login.html", "r", encoding="utf-8") as f:
    signin_html = f.read()
