var ws = null;

ws = new WebSocket("ws://localhost:8000/room/main");
ws.onmessage = (event) => {
    var message_data = JSON.parse(event.data)
    var message_user = message_data.user
    var message_text = message_data.content
    var message_time = message_data.create_time

    var messages = document.getElementById('messages')

    var div_row = document.createElement("div")
    div_row.className = "row align-items-start py-2"

    var div_avatar = document.createElement("div")
    div_avatar.className = "px-3"
    div_row.appendChild(div_avatar)

    var span_avatar = document.createElement("span")
    span_avatar.className = "avatar avatar-sm bg-purple"
    var avatar_text = document.createTextNode(message_user)
    span_avatar.appendChild(avatar_text)
    div_avatar.appendChild(span_avatar)

    var message = document.createElement("div")
    message.className = "reply py-2"
    var message_text = document.createTextNode(message_text)
    message.appendChild(message_text)
    div_row.appendChild(message)
    messages.appendChild(div_row)

    messages.scrollTop = messages.scrollHeight;
};

function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
