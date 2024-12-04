const socket = io()

function addPost(postList, postJSON) {
    let postHTML = createPostHTML(postJSON)
    postList.insertAdjacentHTML("beforeend", postHTML)
    postList.scrollIntoView(false)
    postList.scrollTop = postList.scrollHeight - postList.clientHeight
}

function createPostHTML(postJSON) {
    let postId = postJSON.id
    let postHTML =
        "<div class='post' id='message_" + postId + "'>" +
            createPostInnerHTML(postJSON) + 
        "</div>"
    return postHTML
}

function createPostInnerHTML(postJSON) {
    let postId = postJSON.id
    let username = postJSON.username
    let title = postJSON.title
    let message = postJSON.message
    let filePath = postJSON.file_path
    let mimeType = postJSON.mime_type
    let likes = postJSON.likes.length
    let age = postJSON.age
    let messageHTML = "<b>" + username + ": " + title + "</b><br><div class='message'>" + message + "</div></br>"
    let fileHTML = ""
    if(filePath != null) {
        if(mimeType.startsWith("image")) {
            fileHTML = "<img class=\"upload\" type=" + mimeType + " src=\"" + filePath + "\" alt=\"image not found\"/>"
        } else if(mimeType.startsWith("video")) {
            fileHTML =  "<video class=\"upload\" controls autoplay>"
            fileHTML += "<source type=" + mimeType + " src=\"" + filePath + "\" alt=\"video not found\">"
            fileHTML += "</video>"
        }
    }
    let likeButtonHTML = "<button type='button' onclick='wsLikePost(event, \"" + postId + "\")'>Like (" + likes + ")</button>"
    let postDataHTML = "Posted: " + age + " Seconds Ago."
    let deleteButtonHTML = "<button onclick='wsDeletePost(event, \"" + postId + "\")'>Delete</button>"
    let postInnerHTML = 
        messageHTML + 
        fileHTML +
        "</br>" +
        postDataHTML +
        "<div class='post_buttons'>" +
            likeButtonHTML + 
            deleteButtonHTML + 
        "</div>"
    return postInnerHTML
}

function deletePost(postId) {
    let request = new XMLHttpRequest()
    request.open("DELETE", "/posts/" + postId)
    request.send()
}

function enterCategory(event) {
    if(event.keyCode == 13) {
        let categoryTextBox = document.getElementById("category_textbox")
        window.location.href = "/home/" + categoryTextBox.value
    }
}

function getCategory() {
    let path = window.location.pathname
    if(!path.startsWith("/home/")) {
        return null
    }
    return path.replace("/home/", "")
}

function removePost(postId) {
    let postList = document.getElementById("post_list")
    let post = document.getElementById("message_" + postId)
    if(post != null) {
        post.remove()
    }
    if(postList != null && postList.innerHTML == "") {
        postList.innerHTML = "There are no posts in /" + getCategory()
    }
}

function update() {
    let category = getCategory()
    if(category == null) {
        return
    } 
    let request = new XMLHttpRequest()
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updatePostList(JSON.parse(this.response))
        }
    }
    request.open("GET", "/posts/" + category)
    request.send()
}

function updatePostList(serverMessages) {
    let postList = document.getElementById("post_list")
    if(postList != null) {
        postList.innerHTML = ""
        if(serverMessages.length == 0) {
            postList.innerHTML = "There are no posts in /" + getCategory()
        }
        for(element of serverMessages) {
            addPost(postList, element)
        }
    }
}

// Function to handle deleting a post (via WebSockets)
function wsDeletePost(event, postId) {
    socket.emit('delete', postId)
} 

// Function to handle liking a post (via WebSockets)
function wsLikePost(event, postId) {
    socket.emit('like', postId)
}

// Update the like count on the client side
function wsUpdatePost(postJSON) {
    let postId = postJSON.id
    let post = document.getElementById("message_" + postId)
    if(post != null) {
        post.innerHTML = createPostInnerHTML(postJSON)
    }
}

// Listen for new posts being emitted from the server
socket.on('post', function(postJSON) {
    let postList = document.getElementById("post_list")
    if(postList == null) {
        return
    }
    let category = getCategory()
    if(postJSON.category == category || category == "recent") {
        if(postList.innerHTML == "There are no posts in /" + category) {
            postList.innerHTML = ""
        }
        addPost(postList, postJSON)
    }
})

// Listen for delete requests from the server
socket.on('remove', function(postId) {
    removePost(postId)
})

// Listen for like updates from the server
socket.on('update', function(postJSON) {
    wsUpdatePost(postJSON)
})
