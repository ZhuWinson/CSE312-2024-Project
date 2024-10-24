/*
let animalImages = {
    "/static/image/cat.jpg": 50,
    "/static/image/dog.jpg": 25,
}

let trendingImages = {
    "/static/image/meme1.png": 100,
    "/static/image/meme2.webp": 50,
}

let categories = {
    "animals": animalImages,
    "trending": trendingImages,
}

function setFeedCategory(category) {
    let images = categories[category] || trendingImages
    let maxUpvotes = 0
    let feedImage = null
    for(let image in images) {
        let upvotes = images[image]
        if(upvotes > maxUpvotes) {
            feedImage = image
            maxUpvotes = upvotes
        } 
    }
    let element = document.getElementById("feedImage")
    element.src = feedImage
}

setFeedCategory("meme")
*/