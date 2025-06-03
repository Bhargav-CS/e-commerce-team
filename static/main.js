let sessionId = Date.now().toString();
let chatBox = null;

window.onload = async () => {
  chatBox = document.getElementById("chat-box");

  // Init session
  await fetch("/session/init", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
};

function appendMessage(text, sender = "user") {
  const div = document.createElement("div");
  div.className = sender === "user" ? "text-right mb-2" : "text-left mb-2";
  div.innerHTML = `<span class="inline-block px-3 py-2 rounded-lg ${
    sender === "user" ? "bg-blue-500 text-white" : "bg-gray-300 text-black"
  }">${text}</span>`;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  input.value = "";

  // Streaming fetch POST
  const response = await fetch("/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!response.body) return;

  let botMessage = "";
  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let temp = document.createElement("div");
  temp.className = "text-left mb-2 bot-temp";
  temp.innerHTML = `<span class="inline-block px-3 py-2 rounded-lg bg-gray-300 text-black"></span>`;
  chatBox.appendChild(temp);

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    botMessage += chunk;
    temp.innerHTML = `<span class="inline-block px-3 py-2 rounded-lg bg-gray-300 text-black">${botMessage}</span>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  temp.classList.remove("bot-temp");
}
