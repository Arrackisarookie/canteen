$('#modal_5').modal("show");
var ws = null;
var nickname = getNickName();

function getNickName() {
    const Http = new XMLHttpRequest();
    const url="https://chat.aiar.site/fake/name";
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
        var nickname_h = document.getElementById('nickname');
        nickname = JSON.parse(Http.responseText).nickname
        nickname_h.textContent = nickname;
    }
}

function connect() {
    var url = "wss://chat.aiar.site/chatroom?nickname=" + nickname;
    ws = new WebSocket(url);
    ws.onmessage = (event) => {
        var message_data = JSON.parse(event.data)
        var message_sender = message_data.sender
        var message_receiver = message_data.receiver
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
        var avatar_text = document.createTextNode(message_sender)
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
}

function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}
