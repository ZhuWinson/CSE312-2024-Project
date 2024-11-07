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
    let file = postJSON.file
    let messageHTML = "<pre><b>" + username + ": " + title + "</b><br>" + message + "</pre>"
    let likeButtonHTML = "<button type='submit'>Like (" + likes + ")</button>"
    let fileHTML = "<div class='file' img src=" + file + "/>"
    let postHTML =
        "<div class='post' id='message_" + id + "'>" +
            messageHTML + fileHTML
            "<form action='/like/" + id + "' method='POST'>" +
                likeButtonHTML + 
            "</form>" +
        "</div>"
    
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
    setInterval(update, 3000);
}