const btnSend = document.getElementById('btn-send');
const inputMsg = document.getElementById('input-msg');
const resultCon = document.getElementById('result-con');
const suggestionContainer = document.getElementById('suggestion-container');

window.onload = function () {
    initialBotGreeting();
};

btnSend.addEventListener('click', () => {
    sendMessage(inputMsg.value.trim());
    hideSuggestions();
});

function sendMessage(msg) {
    if (msg !== '') {
        const userBubble = createChatBubble(msg, 'user-bubble', true);
        resultCon.appendChild(userBubble);
        resultCon.scrollTop = resultCon.scrollHeight;

        inputMsg.value = '';

        fetch(`/get?message=${msg}`, { method: 'GET' })
            .then(response => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                const botBubble = createChatBubble(data, 'bot-bubble', false);
                resultCon.appendChild(botBubble);
                resultCon.scrollTop = resultCon.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
}

function initialBotGreeting() {
    const initialBotGreeting = 'Hello, how can I help you?';
    const initialBotBubble = createChatBubble(initialBotGreeting, 'bot-bubble', false);

    // Make sure you have a valid container element to append to
    const container = document.getElementById('result-con');
    container.appendChild(initialBotBubble);

    container.scrollTop = container.scrollHeight;
}

function createChatBubble(message, styleClass, isUser) {
    const chatBubble = document.createElement('div');
    chatBubble.classList.add('mb-2');

    // Create a container for the text
    const textContainer = document.createElement('div');
    textContainer.style.overflow = 'hidden'; // Ensure text doesn't overlap with the image

    // Create text node with the message
    const textNode = document.createTextNode(message);
    textContainer.appendChild(textNode);

    // Apply background styling to the text container only
    textContainer.classList.add(isUser ? 'user-bubble' : 'bot-bubble');

    // Append the text container to the chat bubble
    chatBubble.appendChild(textContainer);

    if (!isUser) {
        const imgContainer = document.createElement('div');
        imgContainer.style.position = 'relative';
        imgContainer.style.float = 'left'; 
        imgContainer.style.marginRight = '10px'; 

        const img = document.createElement('img');
        img.src = 'https://scontent.fdvo2-2.fna.fbcdn.net/v/t39.30808-6/408031386_1461251754451232_4323055135001447027_n.jpg?stp=dst-jpg_p843x403&_nc_cat=105&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeFODrIo-Vxn5n_UhREsK5M8f39AUP9yCmV_f0BQ_3IKZXvEVK7Lzrxr4fys1eKjz_A3ETTgSC9IuIUFnuLBWbsw&_nc_ohc=igXAkS1OELAAX8xt0Uy&_nc_ht=scontent.fdvo2-2.fna&oh=00_AfAxiyamnIDzLDo9USufusj8ZL5CH6NICogUEwbcde_p6Q&oe=6574B97B';

        
        img.alt = 'Chatbot Image';
        img.style.width = '40px'; 
        img.style.height = '40px';
        img.style.borderRadius = '50%';
        img.style.display = 'block';

        imgContainer.appendChild(img);

        chatBubble.insertBefore(imgContainer, textContainer); 
    }

    return chatBubble;
}

function hideSuggestions() {
    suggestionContainer.style.display = 'none';
}

function insertSuggestion(suggestion) {
    inputMsg.value = suggestion;
    hideSuggestions();
}
