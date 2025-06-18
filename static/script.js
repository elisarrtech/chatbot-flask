<script>
  function toggleChat() {
    const chat = document.getElementById('chat-container');
    chat.style.display = chat.style.display === 'flex' ? 'none' : 'flex';
  }

  function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (message === "") return;

    const chatLog = document.getElementById("chat-log");

    // Mensaje del usuario
    const userMsg = document.createElement("div");
    userMsg.className = "chat-message user-message";
    userMsg.textContent = message;
    chatLog.appendChild(userMsg);

    // Scroll hacia abajo
    chatLog.scrollTop = chatLog.scrollHeight;

    // Enviar al backend con fetch
    fetch("/get", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ msg: message })
    })
    .then(res => res.json())
    .then(data => {
      const botMsg = document.createElement("div");
      botMsg.className = "chat-message bot-message";
      botMsg.textContent = data.response;
      chatLog.appendChild(botMsg);
      chatLog.scrollTop = chatLog.scrollHeight;
    });

    input.value = "";
  }
</script>

