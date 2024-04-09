<script>
// $('#modal_5').modal("show");
export default {
  name: 'HomeView',
  data() {
    return {
      sockets_bay_api_key: "demo",
      connection_ready: false,
      connection_error: false,
      nickname: "",
      websocket: null,
      new_message: "",
      messages: [],
      backend_baseurl: import.meta.env.VITE_BACKEND_BASEURL
    }
  },
  methods: {
    init_chat() {
      //ask for a nickname
      if (this.nickname == "") this.nickname = prompt("Enter a nickname:");
      console.log(import.meta.env.VITE_DOMAIN_NAME)
      //connect to Sockets Bay
      var sockets_bay_url = `ws://` + this.backend_baseurl + `/chatroom?nickname=` + this.nickname;
      this.websocket = new WebSocket(sockets_bay_url);
      //
      this.websocket.onopen = this.onSocketOpen;
      this.websocket.onmessage = this.onSocketMessage;
      this.websocket.onerror = this.onSockerError;
    },
    onSocketOpen(evt) {
      this.connection_ready = true;
    },
    onSocketMessage(evt) {
      //we parse the json that we receive
      var received = JSON.parse(evt.data);
      //check if it's our message or from a friend
      this.messages.push({ from: "other", message: received.content });
      //scroll to the bottom of the messages div
      const messages_div = document.getElementById('messages');
      messages_div.scrollTo({ top: messages_div.scrollHeight, behavior: 'smooth' });
    },

    onSockerError(evt) {
      this.connection_error = true;
    },

    send_message() {
      var to_send = { from: this.nickname, message: this.new_message };
      this.websocket.send(JSON.stringify(to_send));
      this.messages.push({ from: "me", message: this.new_message });
      this.new_message = "";
    }
  },
  mounted() {
    this.init_chat();
  }
}
</script>

<template>
  <span class="mask bg-info alpha-3"></span>
  <nav class="navbar navbar-expand-lg navbar-transparent navbar-dark bg-dark py-4">
    <div class="container">
      <a class="navbar-brand" href=""><strong>Canteen</strong> Chatroom</a>
      <span class="connection_ready" v-if="connection_ready">Connection ready!</span>
    </div>
  </nav>
  <main class="main">
    <section class="pt-lg bg-transparent">
      <div class="container d-flex align-items-center">
        <div class="col">
          <div class="row">
            <div class="col-md-12">
              <div class="card px-3 py-4 border-0 mb-0 mh-500">
                <div class="card-body pt-0 messages">
                  <div v-for="(m, idx) in messages" :key="'m-' + idx" style="clear:both" class="my-2">
                    <span class="avatar avatar-sm bg-purple mx-2">{{ m.from }}</span>
                    <div :class="{ 'msg-from-me py-2': m.from == 'me', 'msg-from-other py-2': m.from == 'other' }">
                      {{ m.message }}
                    </div>
                  </div>
                </div>
                <div class="card-footer py-3">
                  <div class="card-comment-box">
                    <div class="col pt-1">
                      <div class="send-zone">
                        <input v-model="new_message" type="text" placeholder="Type a message"
                          @keyup.enter="send_message" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <!-- Modal -->
  <div class="modal fade" id="modal_5" tabindex="-1" role="dialog" aria-labelledby="modal_5" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modal_title_6">取个名字</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="py-3 text-center">
            <i class="fas fa-exclamation-circle fa-4x"></i>
            <h4 class="heading mt-4" id="nickname"></h4>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-sm btn-outline-warning" onclick="getNickName()">再换亿个</button>
          <button type="button" class="btn btn-sm btn-outline-success" data-dismiss="modal"
            onclick="connect()">就这个！</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
body {
  height: 100vh
}

.messages {
  height: 55vh;
  overflow: auto;
}

.send-zone {
  height: 10vh;
  overflow: auto;

  input[type='text'] {
    font-size: 15px;
  }
}

.msg-from-me {
  float: right;
  position: relative;
  padding: 0.408rem 0.816rem;
  border-radius: 0.3rem;
  background-color: rgba(247, 188, 10, 0.3);
  max-width: 80vh;
}

.msg-from-me:before {
  content: "";
  width: 0px;
  height: 0px;
  border-color: transparent transparent transparent rgba(247, 188, 10, 0.3);
  border-style: solid;
  border-width: 0.5rem;
  position: absolute;
  top: 0.65rem;
  border-radius: 0.1rem;
  left: auto;
  right: -0.95rem;
}

.msg-from-other {
  float: left;
  position: relative;
  padding: 0.408rem 0.816rem;
  border-radius: 0.3rem;
  background-color: rgba(247, 188, 10, 0.3);
  max-width: 80vh;
}

.msg-from-other:before {
  content: "";
  width: 0px;
  height: 0px;
  border-color: transparent rgba(247, 188, 10, 0.3) transparent transparent;
  border-style: solid;
  border-width: 0.5rem;
  position: absolute;
  top: 0.65rem;
  border-radius: 0.1rem;
  left: -0.95rem;
  right: auto;
}
</style>