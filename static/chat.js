const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');
const ratingPanel = document.getElementById('rating-panel');

function ensureChatSpacer() {
    let spacer = document.querySelector('.chat-spacer');
    if (!spacer) {
        spacer = document.createElement('div');
        spacer.className = 'chat-spacer';
        chatMessages.appendChild(spacer);
    } else {
        chatMessages.appendChild(spacer); // move to end if needed
    }
}

function scrollChatToBottom() {
    const spacer = document.querySelector('.chat-spacer');
    if (spacer) {
        spacer.scrollIntoView({ behavior: "auto", block: "end" });
    }
}

let isRatingActive = false;

function showRatingPanel() {
    ratingPanel.style.display = 'flex';
    isRatingActive = true;
    // Reset stars
    const stars = ratingPanel.querySelectorAll('.star');
    stars.forEach(star => star.classList.remove('active'));
}

function hideRatingPanel() {
    if (!isRatingActive) {
        ratingPanel.style.display = 'none';
    }
}

function handleStarClick(rating) {
    const stars = ratingPanel.querySelectorAll('.star');
    const ratingValue = parseInt(rating);
    
    stars.forEach((star) => {
        const starRating = parseInt(star.getAttribute('data-rating'));
        if (starRating <= ratingValue) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
    
    // Here you can add logic to send the rating to your backend
    console.log(`Rating submitted: ${ratingValue} stars`);
    
    // Hide the rating panel after a short delay
    setTimeout(() => {
        isRatingActive = false;
        ratingPanel.style.display = 'none';
    }, 1500);
}

function addMessage(text, sender) {
    const msg = document.createElement('div');
    msg.className = 'message ' + sender;
    msg.textContent = text;
    chatMessages.appendChild(msg);
    ensureChatSpacer();
    chatMessages.scrollTop = chatMessages.scrollHeight;
    scrollChatToBottom();
    return msg;
}

function addTypingBubble() {
    const msg = document.createElement('div');
    msg.className = 'message ai';
    msg.innerHTML = '<span class="typing-dots"><span></span><span></span><span></span></span>';
    chatMessages.appendChild(msg);
    ensureChatSpacer();
    chatMessages.scrollTop = chatMessages.scrollHeight;
    scrollChatToBottom();
    return msg;
}

async function typeOutText(element, text, delay = 8) {
    element.innerHTML = '';
    let html = '';
    for (let i = 0; i < text.length; i++) {
        if (text[i] === '\n') {
            html += '<br>';
        } else {
            html += text[i];
        }
        element.innerHTML = html;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        scrollChatToBottom();
        await new Promise(r => setTimeout(r, delay));
    }
    scrollChatToBottom();
    
    // Show rating panel after typing is complete
    showRatingPanel();
    ratingPanel.scrollIntoView({ behavior: "smooth", block: "end" });
}

// Add event listeners for rating stars
document.addEventListener('DOMContentLoaded', function() {
    const stars = ratingPanel.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent event bubbling
            const rating = this.getAttribute('data-rating');
            handleStarClick(rating);
        });
    });
    
    // Hide rating panel when user starts typing
    chatInput.addEventListener('input', function() {
        if (!isRatingActive) {
            hideRatingPanel();
        }
    });
    
    // Hide rating panel when user focuses on input
    chatInput.addEventListener('focus', function() {
        if (!isRatingActive) {
            hideRatingPanel();
        }
    });
    
    // Prevent rating panel from being hidden when clicking on it
    ratingPanel.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = chatInput.value.trim();
    if (!question) return;
    
    // Hide rating panel when user submits a new question
    hideRatingPanel();
    
    addMessage(question, 'user');
    chatInput.value = '';
    // Show typing dots animation
    const aiMsg = addTypingBubble();
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await res.json();
        await typeOutText(aiMsg, data.answer, 8);
    } catch (err) {
        aiMsg.textContent = 'Lỗi khi nhận phản hồi từ máy chủ.';
    }
}); 