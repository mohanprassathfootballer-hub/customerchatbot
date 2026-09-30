let conversationId = null;


const chat = document.getElementById("chat");

const input = document.getElementById(
    "messageInput"
);

const sendButton = document.getElementById(
    "sendButton"
);

const typing = document.getElementById(
    "typing"
);


async function createConversation() {

    try {

        const response = await fetch(
            "/api/conversations",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    customer_name: "Guest"
                })
            }
        );

        const data = await response.json();

        conversationId = data.conversation_id;

    } catch (error) {

        console.error(
            "Conversation error:",
            error
        );

        alert(
            "Unable to connect to the chatbot."
        );
    }
}


function addMessage(
    message,
    sender
) {

    const container =
        document.createElement("div");

    container.className =
        `message ${sender}`;


    const avatar =
        document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent =
        sender === "user"
            ? "You"
            : "AI";


    const bubble =
        document.createElement("div");

    bubble.className = "bubble";

    bubble.textContent = message;


    container.appendChild(avatar);

    container.appendChild(bubble);

    chat.appendChild(container);


    chat.scrollTop =
        chat.scrollHeight;
}


async function sendMessage() {

    const message =
        input.value.trim();


    if (!message) {
        return;
    }


    if (!conversationId) {

        await createConversation();

    }


    addMessage(
        message,
        "user"
    );


    input.value = "";

    sendButton.disabled = true;

    typing.classList.remove(
        "hidden"
    );


    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        conversation_id:
                            conversationId,

                        message:
                            message
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Server error"
            );

        }


        addMessage(
            data.response,
            "bot"
        );


    } catch (error) {

        console.error(error);

        addMessage(
            "Sorry, I couldn't process your request. Please try again.",
            "bot"
        );

    } finally {

        typing.classList.add(
            "hidden"
        );

        sendButton.disabled = false;

        input.focus();
    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);


input.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);


createConversation();

input.focus();