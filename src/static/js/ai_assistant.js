document.addEventListener("DOMContentLoaded", () => {
  const sendButton = document.getElementById("send-btn");
  const userInput = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  // Function to display messages in chat
  function addMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    // Add sender name
    const senderLabel = document.createElement("strong");
    senderLabel.textContent = sender === "user" ? "You: " : "Aura: ";
    messageDiv.appendChild(senderLabel);

    // Add message text
    const messageText = document.createElement("span");
    messageText.textContent = message;
    messageDiv.appendChild(messageText);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Send message to backend
  async function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    addMessage("user", message);
    userInput.value = "";

    try {
      const response = await fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
      });

      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      addMessage("aura", data.response);
    } catch (error) {
      console.error("Error:", error);
      addMessage("aura", "Oops, something went wrong. Please try again later.");
    }
  }

  // Event listeners
  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});