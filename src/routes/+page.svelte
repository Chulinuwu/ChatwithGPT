<script lang="ts">
    let userInput = '';
    let chatboxContent = '';

    async function sendMessage() {
        if (userInput.trim() === '') return;
        
        chatboxContent += `<div class="message user-message"><strong>You:</strong> ${userInput}</div>`;

        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();
        chatboxContent += `<div class="message"><strong>GPT:</strong> ${data.response}</div>`;
        userInput = '';
    }

    function handleKeyDown(event: KeyboardEvent) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    }
</script>

<div class="flex justify-center items-center h-screen bg-gray-800 text-gray-200">
    <div class="bg-gray-700 rounded-lg shadow-lg p-6 w-full max-w-2xl flex flex-col h-4/5">
        <h1 class="text-2xl font-bold mb-4">Chat with GPT</h1>
        <div id="chatbox" class="flex-1 border border-gray-600 p-4 overflow-y-auto mb-4 rounded bg-gray-800" contenteditable=true bind:innerHTML={chatboxContent}></div>
        <div class="flex">
            <input type="text" bind:value={userInput} placeholder="Type your message..." class="flex-1 p-2 border border-gray-600 rounded mr-2 bg-gray-800 text-gray-200" on:keydown={handleKeyDown} />
            <button on:click={sendMessage} class="p-2 bg-green-600 text-white rounded hover:bg-green-500">Send</button>
        </div>
    </div>
</div>