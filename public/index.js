let animalImages = {
    "image/cat.jpg": 50,
    "image/dog.jpg": 25,
}

let trendingImages = {
    "image/meme1.png": 100,
    "image/meme2.webp": 50,
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