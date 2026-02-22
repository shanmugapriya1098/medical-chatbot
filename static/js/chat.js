const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatWindow = document.getElementById('chat-window');
const typingIndicator = document.getElementById('typing-indicator');

function appendMessage(text, sender, type = 'standard') {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`, 'slide-in');

    if (type === 'emergency') {
        messageDiv.querySelector('.bubble')?.classList.add('emergency-bubble');
    }

    const avatar = sender === 'bot' ? '🤖' : '👤';

    messageDiv.innerHTML = `
        <div class="avatar">${avatar}</div>
        <div class="bubble ${type === 'emergency' ? 'emergency-bubble' : ''}">${formatText(text)}</div>
    `;

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function formatText(text) {
    // Basic markdown-like formatting for bold text
    return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Append user message
    appendMessage(message, 'user');
    userInput.value = '';

    // Show typing indicator
    typingIndicator.classList.remove('hidden');
    chatWindow.scrollTop = chatWindow.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // Hide typing indicator and append bot response
        setTimeout(() => {
            typingIndicator.classList.add('hidden');
            appendMessage(data.response, 'bot', data.type);
        }, 600); // Small delay for "realism"

    } catch (error) {
        typingIndicator.classList.add('hidden');
        appendMessage("Sorry, I'm having trouble connecting to my brain. Please try again later.", 'bot');
        console.error("Chat Error:", error);
    }
});
