const comments = [
    {
        stars: '★★★★★',
        text: '"Amazing experience! I learned guitar from a pro in just a few sessions."',
        author: '- Alex Johnson'
    },
    {
        stars: '★★★★☆',
        text: '"Great platform for skill exchange. Found a cooking teacher quickly."',
        author: '- Maria Garcia'
    },
    {
        stars: '★★★★★',
        text: '"Highly recommend! Learned programming basics in a fun way."',
        author: '- David Lee'
    }
];

let currentCommentIndex = 0; // current card index

function updateComment() {
    const content = document.querySelector('.comment-content'); // find display area
    if (content) {
        const comment = comments[currentCommentIndex]; // get current data
        content.innerHTML = `
            <div class="stars">${comment.stars}</div>
            <p>${comment.text}</p>
            <cite>${comment.author}</cite>
        `;
        console.log('Updated comment to index:', currentCommentIndex);
    } else {
        console.log('Comment content not found');
    }
}

function initComments() {
    console.log('Initializing comments');
    const prevBtn = document.querySelector('.prev-btn'); // previous button
    const nextBtn = document.querySelector('.next-btn'); // next button

    if (prevBtn && nextBtn) {
        console.log('Buttons found, setting up events');
        updateComment(); // show first card

        prevBtn.addEventListener('click', function() {
            // go to previous one and avoid less than zero (loop)
            currentCommentIndex = (currentCommentIndex - 1 + comments.length) % comments.length;
            updateComment();
        });

        nextBtn.addEventListener('click', function() {
            // go to next (loop)
            currentCommentIndex = (currentCommentIndex + 1) % comments.length;
            updateComment();
        });
    } else {
        console.log('Buttons not found');
    }
}

// Initialize comments when the page is loaded (run after page loads)
initComments();