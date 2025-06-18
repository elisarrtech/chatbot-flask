function toggleChat() {
  const chat = document.getElementById("chat-container");
  chat.style.display = (chat.style.display === "none" || chat.style.display === "") ? "flex" : "none";
}

function sendMessage(event) {
  event.preventDefault();
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (message) {
    const log = document.getElementById("chat-log");
    const msgElem = document.createElement("div");
    msgElem.textContent = "Tú: " + message;
    log.appendChild(msgElem);
    log.scrollTop = log.scrollHeight;
    input.value = "";
  }
}
