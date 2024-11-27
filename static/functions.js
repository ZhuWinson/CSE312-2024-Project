const socket = io();

// Listen for like updates from the server
socket.on('like_update', function(postJSON) {
    updateLikeCount(postJSON);
});

// Function to handle liking a post (via WebSocket)
function likePost(event, postId) {
    // Emit the 'like_post' event to the server with the post ID
    socket.emit('like_post', postId);
}

// Update the like count on the client side
function updateLikeCount(postJSON) {
    const postId = postJSON.id;
    const likes = postJSON.likes.length;
    const likeButton = document.querySelector(`#message_${postId} button`);
    if (likeButton) {
        likeButton.textContent = `Like (${likes})`;  // Update the like count on the button
    }
}

// Listen for new posts being emitted from the server
socket.on('new_post', function(postJSON) {
    let postList = document.getElementById("post_list");
    if (postList) {
        addPost(postList, postJSON);
    }
});

function addPost(postList, postJSON) {
    let postHTML = createPostHTML(postJSON)
    postList.insertAdjacentHTML("beforeend", postHTML);
    postList.scrollIntoView(false);
    postList.scrollTop = postList.scrollHeight - postList.clientHeight;
}

function createPostHTML(postJSON) {
    let username = postJSON.username
    let title = postJSON.title
    let message = postJSON.message
    let likes = postJSON.likes.length
    let id = postJSON.id
    let messageHTML = "<pre><b>" + username + ": " + title + "</b><br>" + message + "</pre>"
    let likeButtonHTML = "<button type='button' onclick='likePost(event, \"" + id + "\")'>Like (" + likes + ")</button>";

//    let postHTML =
//        "<div class='post' id='message_" + id + "'>" +
//            messageHTML +
//            "<form action='/like/" + id + "' method='POST'>" +
//                likeButtonHTML +
//            "</form>" +
//        "</div>"
    let postHTML =
        "<div class='post' id='message_" + id + "'>" +
            messageHTML +
            likeButtonHTML +
        "</div>";

    return postHTML
}

function update() {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updatePosts(JSON.parse(this.response));
        }
    }
    request.open("GET", "/posts");
    request.send();
}

function updatePosts(serverMessages) {
    let postList = document.getElementById("post_list");
    if(postList != null) {
        postList.innerHTML = ""
        for(element of serverMessages) {
            addPost(postList, element)
        }
    }
}

function setup() {
    update()
//    setInterval(update, 3000);
}