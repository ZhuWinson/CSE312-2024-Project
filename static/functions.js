function addPost(postList, postJSON) {
    let postHTML = createPostHTML(postJSON)
    postList.insertAdjacentHTML("beforeend", postHTML);
    postList.scrollIntoView(false);
    postList.scrollTop = postList.scrollHeight - postList.clientHeight;
}

function createPostHTML(postJSON) {
    let postID = postJSON.id
    let username = postJSON.username
    let title = postJSON.title
    let message = postJSON.message
    let likes = postJSON.likes.length
    let age = postJSON.age
    let messageHTML = "<pre><b>" + username + ": " + title + "</b><br>" + message + "</pre>"
    let likeButtonHTML = "<input type='submit' value='Like (" + likes + ")'/>"
    let postDataHTML = "Age: " + age
    let deleteButtonHTML = "<button onclick='deletePost(\"" + postID + "\")'>Delete</button>"
    let postHTML =
        "<div class='post' id='message_" + postID + "'>" +
            messageHTML + 
            postDataHTML +
            "<div class='post_buttons'>" +
                "<form action='/like/" + postID + "' method='post'>" +
                    likeButtonHTML + 
                "</form>" +
                deleteButtonHTML + 
            "</div>"
        "</div>"
    return postHTML
}

function deletePost(postID) {
    let request = new XMLHttpRequest();
    request.open("DELETE", "/posts/" + postID);
    request.send();
}

function findCategory(event) {
    if(event.keyCode == 13) {
        let categoryTextBox = document.getElementById("category_textbox");
        window.location.href = "/" + categoryTextBox.value
    }
}

function update() {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updatePosts(JSON.parse(this.response));
        }
    }
    request.open("GET", "/posts" + window.location.pathname);
    request.send();
}

function updatePosts(serverMessages) {
    let postList = document.getElementById("post_list");
    if(postList != null) {
        postList.innerHTML = ""
        if(serverMessages.length == 0) {
            postList.innerHTML = "There are no posts in " + window.location.pathname
        }
        for(element of serverMessages) {
            addPost(postList, element)
        }
    }
}

function setup() {
    update()
    setInterval(update, 1000);
}