<script setup>
import { ref, computed, watch } from 'vue'

const nickname = ref(null)
let myHeaders = new Headers({
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'text/plain'
});

async function getNickName() {
  const res = await fetch(
    `http://localhost:8000/fake/name`,
    {headers: myHeaders,
    mode: 'cors'}
  )
  nickname.value = await res.json()
}

getNickName()

var ws = null;
function connect() {
    var url = "ws://localhost:8000/chatroom?nickname=" + nickname;
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

// function sendMessage(event) {
//     var input = document.getElementById("messageText")
//     ws.send(input.value)
//     input.value = ''
//     event.preventDefault()
// }
</script>

<template>
  <div class="modal-body">
    <div class="py-3 text-center">
      <i class="fas fa-exclamation-circle fa-4x"></i>
      <h4 class="heading mt-4" id="nickname">{{ nickname }}</h4>
    </div>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-sm btn-outline-warning" @click="getNickName">再换亿个</button>
    <button type="button" class="btn btn-sm btn-outline-success" data-dismiss="modal" @click="connect">就这个！</button>
  </div>
  <div class="card px-3 py-4 border-0 mb-0 mh-500">
    <div class="card-body pt-0" id="messages">
    </div>
    <div class="card-footer py-3">
      <form class="card-comment-box" role="form" onsubmit="sendMessage(event)">
        <div class="row pt-1">
          <div class="col-10" id="input-field">
            <textarea id="messageText" autocomplete="off" rows="2" class="form-control textarea-autosize" placeholder="整两句..."></textarea>
          </div>
          <div class="col-2 text-right">
            <div class="card-icon-actions card-icon-actions-lg">
              <button type="submit" class="btn btn-secondary btn-icon-only">
                <span class="btn-inner--icon"><i class="fas fa-arrow-left"></i></span>
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>

</style>
