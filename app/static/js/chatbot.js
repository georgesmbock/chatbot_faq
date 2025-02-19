document.getElementById('sendButton').addEventListener('click', function() {
    const messageInput = document.getElementById('messageInput');
    const question = messageInput.value;
    const button = document.getElementById('sendButton');
    
    // Validation: Check if the messageInput is empty
    if (question.trim() === "") {
        alert("Please enter a question before submitting.");
        return;  // Exit the function if no input is provided
    }

    // Check if the NLP engine is connected
    checkNLPConnection().then(isConnected => {
        if (!isConnected) {
            alert("NLP engine is currently unavailable. Please try again later.");
            return;  // Exit the function if NLP engine is not connected
        }
        
        button.disabled = true;  // Deactivate the button to prevent multiple clicks

        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        })
        .then(response => response.json())
        .then(data => {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML += `<p><strong>You:</strong> ${data.question}</p>`;
            messagesDiv.innerHTML += `<p><strong>Bot:</strong> ${data.answer}</p>`;
	    messageInput.value = '';
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            button.disabled = false;  // Reactivate the button after the answer is received
        });
    });
});

// Function to check the connection to the NLP engine
function checkNLPConnection() {
    return fetch('/check_nlp_connection')
        .then(response => {
            if (response.status === 200) {
                return true;  // NLP engine is connected
            } else {
                return false;  // NLP engine is disconnected
            }
        })
        .catch(error => {
            console.error('Error connecting to NLP engine:', error);
            return false;  // Return false if the connection fails
        });
}
