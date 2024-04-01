var ws = null;
function joinRoom(event) {
    var roomId = document.getElementById("roomId")
    var userId = document.getElementById("userId")
    ws = new WebSocket("ws://localhost:8000/" + roomId.value + "/" + userId.value);
    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('p')
        message.className = "mt-4"
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
    event.preventDefault()
}
function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
function leaveRoom(event) {
    ws.close()
}