document.addEventListener("DOMContentLoaded", function () {
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const chatArea = document.getElementById("chat-area");

  function displayMessage(message, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender + "-message");
    messageDiv.textContent = message;
    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
  }

  function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    displayMessage("You: " + message, "user");
    userInput.value = "";

    fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => displayMessage("AI: " + data.response, "AI"))
    .catch(error => console.error("Error:", error));
  }

  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      sendMessage();
      event.preventDefault();
    }
  });
});
