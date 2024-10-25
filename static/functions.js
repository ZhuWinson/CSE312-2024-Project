function addPost(postJSON) {
    let postList = document.getElementById("post_list");
    let postHTML = createPostHTML(postJSON)
    postList.insertAdjacentHTML("beforeend", postHTML);
    postList.scrollIntoView(false);
    postList.scrollTop = postList.scrollHeight - postList.clientHeight;
}

function createPostHTML(postJSON) {
    let username = postJSON.username
    let title = postJSON.title
    let message = postJSON.message
    let id = postJSON.id
    let postHTML = 
        "<div class='post' id='message_" + id + "'>" +
            "<pre><b>" + username + ": " + title + "</b><br>" + message + "</pre>"+
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
    postList.innerHTML = ""
    for(element of serverMessages) {
        addPost(element)
    }
}

function setup() {
    update()
    setInterval(update, 3000);
}