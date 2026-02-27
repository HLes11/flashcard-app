let currentIndex = 0;
let isFlipped = false;

// Initialize the first card if cards array exists
document.addEventListener('DOMContentLoaded', () => {
    if (typeof cards !== 'undefined' && cards.length > 0) {
        updateCardDisplay();
    }
});

function updateCardDisplay() {
    if (typeof cards === 'undefined' || cards.length === 0) return;

    const card = cards[currentIndex];
    document.getElementById('card-word').textContent = card.word;
    document.getElementById('card-meaning').textContent = card.meaning;
    document.getElementById('progress-text').textContent = `${currentIndex + 1} / ${cards.length}`;
    
    // Reset flip state when changing cards
    if (isFlipped) {
        document.getElementById('flashcard').classList.remove('is-flipped');
        isFlipped = false;
    }
}

function flipCard() {
    const flashcard = document.getElementById('flashcard');
    if (flashcard) {
        flashcard.classList.toggle('is-flipped');
        isFlipped = !isFlipped;
    }
}

function nextCard() {
    if (typeof cards === 'undefined' || cards.length === 0) return;
    
    if (currentIndex < cards.length - 1) {
        currentIndex++;
        updateCardDisplay();
    }
}

function prevCard() {
    if (typeof cards === 'undefined' || cards.length === 0) return;
    
    if (currentIndex > 0) {
        currentIndex--;
        updateCardDisplay();
    }
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        nextCard(); // RTL layout, left arrow goes to next
    } else if (e.key === 'ArrowRight') {
        prevCard(); // RTL layout, right arrow goes to prev
    } else if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        flipCard();
    }
});
