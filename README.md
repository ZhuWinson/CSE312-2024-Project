# Project Description:
A website where you can post funny memes and pictures.
- lmaowajd.com
- Sense of time is implemented by keeping track of the recency of posts
- Cool feature is sorting posts by tags

# Sense of time feature: post age
lmaowajd.com can track a post's age by seconds. To further elaborate, a post has an age attribute which represents the number of seconds it has been posted for. The attribute can be viewed after creating the post, navigating the page it was posted to (see the creative feature), and viewing the text towards the bottom of the post. It should read something alonf the lines of "Posted x seconds ago", where x represents the post's age in seconds. This feature affects how the app functions, posts that exist for 

# Creative feature: sorting posts by categories
lmaowajd.com allows users to choose which category their post belongs to. This category attribute determines which page their post will be posted to. 

To apply a category, create a page by pressing the "Create" button on the home page. From there, create the post by filling out the entire form, and make sure to provide a category using the bottom text field. Spaces, upperchase letters, and non-letter characters are not considered valid. If a post is given the category of an empty string, the post will have no category and will be posted only to the recent page. Once the post is considered non-recent, it will be lost forever. 

The specific pages can be found by using the search bar on the left side of the screen. This search bar will redirect the user to https://localhost:8080/home/<user_input>, where <user_input> is replaced by the input in the searchbar. Furthermore, specific pages can simply be located by navigating to https://localhost:8080/home/<category_name>, where <category_name> is replaced by the category attribute of all the posts on the page.

To best test the category feature, perform the following procedure:

1) Start the docker container and navigate to localhost:8080
2) Assert that you are redirected to localhost:8080/home/recent/
3) Create a post with a valid category name
4) Assert that you are redirected to localhost:8080/home/<category_name>, and that your post exists on that page
5) Open another browser and navigate to localhost:8080
6) Use the search bar to search for <category_name>
7) Assert that you are redirected to localhost:8080/home/<category_name>, and that the original post still exists
8) Use the search bar to search for <new_category_name>, where <new_category_name> != <category_name>, and is a valid category name
9) Assert that you are redirected to localhost:8080/home/<new_category_name>, and that the original post is not shown on that page
10) Start the docker container and navigate to localhost:8080/home/<category_name>
11) Assert that the original post still exists on that page
