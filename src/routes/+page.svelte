<script lang="ts">
    import gpt from "./GPT.jpg";
    import you from "./you.jpg";

    let userInput = '';
    let chatboxContent = '';
    let isSidebarOpen = false;
    let messageId = 0;
    let array_message: { id: number, content: string }[] = [];
    let chatbox: HTMLElement | null = null;

    async function sendMessage() {
        console.log('sendMessage called');
        if (userInput.trim() === '') return;

        const currentMessageId = messageId++;
        console.log('Current message ID:', currentMessageId);
        
        array_message.push({
            id: currentMessageId,
            content: `<div class="message user-message flex items-start space-x-4">
                <img src=${you} class="w-10 h-10 rounded-full">
                <div class="bg-blue-500 text-white p-3 rounded-lg shadow">${userInput}</div>
            </div>`
        });
        console.log('User message added:', array_message[array_message.length - 1]);

        array_message.push({
            id: currentMessageId,
            content: `<div class="message gpt-message flex items-start space-x-4" id="message-${currentMessageId}">
                <img src=${gpt} alt="GPT" class="w-10 h-10 rounded-full">
                <div class="bg-gray-600 text-white p-3 rounded-lg shadow">Thinking...</div>
            </div>`
        });
        console.log('GPT thinking message added:', array_message[array_message.length - 1]);

        updateChatboxContent();

        if (chatbox) chatbox.scrollTop = chatbox.scrollHeight;

        try {
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userInput }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const responseMessage = data.response;
            console.log('Response received:', responseMessage);

            // Find the GPT thinking message and update it
            const gptMessageIndex = array_message.findIndex(msg => msg.id === currentMessageId && msg.content.includes('Thinking...'));
            if (gptMessageIndex !== -1) {
                array_message[gptMessageIndex] = {
                    id: currentMessageId,
                    content: `<div class="message gpt-message flex items-start space-x-4" id="message-${currentMessageId}">
                        <img src=${gpt} alt="GPT" class="w-10 h-10 rounded-full">
                        <div class="bg-gray-600 text-white p-3 rounded-lg shadow">${responseMessage}</div>
                    </div>`
                };
                console.log('GPT response message added:', array_message[gptMessageIndex]);
            }

            updateChatboxContent();

            if (chatbox) chatbox.scrollTop = chatbox.scrollHeight;
        } catch (error) {
            console.error('Fetch error: ', error);
        }

        userInput = '';
    }

    function updateChatboxContent() {
        chatboxContent = array_message.map(msg => msg.content).join('');
        console.log('Chatbox content updated:', chatboxContent);
    }

    function handleKeyDown(event: KeyboardEvent) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    }

    function toggleSidebar() {
        isSidebarOpen = !isSidebarOpen;
    }
</script>

<style>
    .typing {
        animation: none;
    }
</style>

<div class="flex h-screen bg-white text-black">
    <!-- Sidebar -->
    <div
        class="bg-white p-4 shadow-lg transition-transform min-w-[200px] transform duration-300 z-50 max-md:hidden absolute h-full"
        style="width: 25%;"
        class:-translate-x-full={!isSidebarOpen}
    >
        <h2 class="text-xl font-bold mb-4">Options</h2>
        <ul class="space-y-2">
            <li><button class="w-full text-left p-2 rounded bg-white">New Chat</button></li>
            <li><button class="w-full text-left p-2 rounded bg-white">Saved Chats</button></li>
            <li><button class="w-full text-left p-2 rounded bg-white">Settings</button></li>
        </ul>
    </div>

    <!-- Chat Area -->
    <div
        class="flex flex-col transition-all duration-300 z-0"
        style="flex-grow: 1;"
        class:ml-0={!isSidebarOpen} class:ml-[25%]={isSidebarOpen}
    >
        <!-- Header -->
        <header class="p-4 bg-white shadow flex justify-between items-center">
            <h1 class="text-2xl font-bold">Peko Chat</h1>
            <button
                on:click={toggleSidebar}
                class="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 max-md:hidden"
            >
                Toggle Sidebar
            </button>
        </header>

        <!-- Chatbox -->
        <main
            id="chatbox"
            class="flex-1 overflow-y-auto p-10 bg-white rounded-lg space-y-4"
            bind:this={chatbox}
        >
            {@html chatboxContent}
        </main>

        <!-- Input -->
        <footer class="p-4 bg-white shadow flex items-center">
            <input
                type="text"
                bind:value={userInput}
                placeholder="Type your message..."
                class="flex-1 p-2 border border-gray-600 rounded bg-white text-black mr-4"
                on:keydown={handleKeyDown}
            />
            <button
                on:click={sendMessage}
                class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-500"
            >
                Send
            </button>
        </footer>
    </div>
</div>