# Project Description:
A website where you can post funny memes and pictures.
- Sense of time is implemented by keeping track of the recency of posts
- Cool feature is sorting posts by tags

Project Handouts:

# Project Part 1

This project is a team assignment and you will use a public GitHub repository to track all of your progress and contributions to your project. You should use proper git/GitHub practices in this repo. There are no additional submissions for the project as the course staff will check your repo after the deadline to grade your project. Commits made after each deadline will be ignored while grading.

As opposed to the homework, you must use a framework throughout the project. The purpose of the project is to give you experience working on a web app in the way you will outside of this course (You should never build an app starting with TCP outside of an educational environment). In the real world, we use frameworks. Through this experience, you will gain an understanding of what a framework does for you.

You will need a database throughout the project. You may use whatever you'd like for your database, however your database must be used through a second container that is separate from your app and started using docker compose.

In this part of the project, you will become familiar with the idea of using a framework to build a web application. You will choose a web framework, build an app, and set up docker compose for deployment.

## Objective 1: Choosing a Framework and Hosting a Static Page

Build an app. You have freedom in what you build for this objective as long as it contains all of the following that must be hosted by your server:

* HTML hosted at the root path  
* CSS hosted at a separate path  
* JavaScript hosted at a separate path  
* At least one image

Note: You must actually build your own app. You cannot steal someone else's work. If you host, for example, the front end from the homework, your team will not earn any credit for this part of the project.

All of these parts must be hosted by your server (eg. You must serve the image from your server using your framework of choice). Do not add a full url as the src of the image.

**Security**: All files must be served with the correct MIME type and the X-Content-Type-Options: nosniff header must be set.

You must use a web framework for the project (As opposed to the homework where you effectively build your own framework). You are expected to find and study documentation to learn how to use your framework of choice as it will not be covered in lecture.

You may choose from the following approved frameworks:

* Flask / Python  
* Express / Node.js  
* Django / Python  
* gin / go  
* Play / Java;Scala  
* Koa / Node.js  
* FastAPI / Python  
* Elysia / Node.js  
* Spring / Java

If you would like to use a framework that is not in this list, let Jesse know and it will be considered for approval. If approved, it will be added to this list.

You may change your framework in later parts (not recommended), but you must use an approved framework for all parts of the project.

**Docker**: Once you choose a framework, set up your project using Docker and docker compose. Your app must run on local port 8080\.

### Testing Procedure

1. Start your server using "docker compose up"   
2. With the network tab open, navigate to http://localhost:8080/ in a browser  
3. Ensure that a web page appears in the browser  
4. In the network tab, check that at least 4 HTTP requests were sent to load the page containing HTML, CSS, JavaScript, and an image all in separate requests  
5. Check to ensure that each of the 4 parts had some impact on the loaded page (eg. the CSS and JavaScript must do something/anything)  
6. **Security:** Verify that the "X-Content-Type-Options: nosniff" header is set on each response  
7. Check the code to ensure that an approved framework is being used (No credit will be given on any part of the project if the code uses a TCP socket like the HW code does. For all other project objectives, this will be implied to be part of the testing procedures)

## Objective 2: Authentication

Add authentication to your app. When navigating to you home page, the user should be presented with 2 forms:

* A registration from   
  * Used when a user creates an account by entering a username and 2 passwords (They provide the same password twice)  
* A login form  
  * Used to login after a user creates an account by entering the same username and password that was used when they registered

You may use any approach you'd like to build these forms as long as they contain these features:

* After registration or login, the user should still be on the homepage (Either using AJAX or a redirect). The user should not have to manually navigate back to your app  
* Checking if the 2 entered passwords are the same must be done on your server. Do not trust the front end for this verification  
* A user cannot register with a username that is already taken by another user

When a user is logged in, their username must be displayed somewhere on your home page.

A logged in user must have a way to logout that will invalidate their auth token.

When a user sends a **registration** request, store their username and a salted hash of their password in your database.

When a user sends a **login** request, authenticate the request based on the data stored in your database. If the \[salted hash of the\] password matches what you have stored in the database, the user is authenticated.

When a user successfully logs in, set an **authentication token** as a cookie for that user with the HttpOnly directive set. These tokens should be random values that are associated with the user. You must store a **hash** (no salt required) of each token in your database so you can verify them on subsequent requests.

The auth token cookie must have an expiration time of 1 hour or longer. It cannot be a session cookie.

**Security:** Never store plain text passwords. You must only store salted hashes of your users' passwords. It is strongly recommended that you use the bcrypt library to handle salting and hashing.

**Security:** Only hashes of your auth tokens should be stored in your database (Do not store the tokens as plain text). Salting is not expected.

**Security:** Set the HttpOnly directive on your cookie storing the authentication token.

### Testing Procedure

1. Start your server with "docker compose up"   
2. Open a browser and navigate to http://localhost:8080/  
   1. Clear all cookies stored for localhost  
3. Find the registration form and:  
   1. Attempt to register with 2 passwords that do not match   
      1. Verify that the account is not created  
      2. Check to make sure the check was made by the server (It can also be on the front end for UX, so if you find a front end check do not assume that the back end is not also checking. You must check the server code if you find a front end check)  
   2. Register properly with a username and matching passwords  
4. Find the login form and enter your chose  username, but an incorrect password  
   1. Verify that your username is not displayed on the page  
5. Submit the login form again with the correct username and password from the registration step  
6. Verify that your username is displayed on the page  
7. Restart the server with "docker compose restart"  
8. Navigate to http://localhost:8080/  
9. Verify that your username is still displayed on the page  
10. Open a second browser (Use Chrome and Firefox. Switch to the one you didn't use in the previous steps)  
    1. Attempt to register with the same username that you've already registered  
       1. Verify that an account was not created and that you cannot login with that username and password  
    2. Register with a second username and login with this new account  
       1. Verify that your new username is displayed on the page  
11. Refresh the page on the first browser and verify that it still displays your first username  
12. In the first browser:  
    1. Find your auth cookie and copy your auth token. Store this token for later use  
    2. Modify your auth token and refresh the page  
       1. Verify that you are treated as not being logged in  
    3. Paste your auth token back into your cookie and refresh the page  
       1. Verify that you are logged in again (Your username is displayed on the page)  
    4. Find a way to logout through the app's interface and logout  
       1. Refresh and verify that you are logged out  
    5. Modify your cookies to set an auth token with the value saved earlier to simulate the same state you had when you were logged in, then refresh the page  
       1. Verify that you are not logged in  
    6. Log in again by entering your username/password  
       1. Verify that you are logged in  
13. Refresh the second browser and verify that you are still logged in with your second account  
14. **Security:** Check the server code to ensure passwords are being salted and hashed before being stored in the database  
15. **Security:** Look through the code and verify that the authentication tokens are not stored as plain text **and** that the cookie values are not the same as what's stored in the DB (ie. Whatever value you use in cookies, the DB must store a hash of that value. Setting the cookies to the hashed values defeats the purpose of hashing and is a security risk)  
16. **Security:** Verify that the cookies HttpOnly directive is set  
17. **Security:** Look through the code to verify that prepared statements are being used to protect against SQL injection attacks \[If SQL is being used\] (This is true for all project objectives and will not be explicit stated after this objective)  
18. Verify that a database is being used by communicating with a second docker container that was created using docker compose (This is true for all project objectives and will not be explicit stated after this objective)

## Objective 3: Making Interactive Posts

Note: For this objective, you should start thinking about what your app will eventually accomplish. You are free to design whatever type of app you'd like as long as it meets the criteria of each objective. In future parts you will add multimedia uploads, live WebSocket interactions, at least one feature where timing matters, and you will deploy your app to the world at a domain name of your choosing. Start planning what you want to build with all those features.

Add a way for users to make posts to your page. These posts must contain at least two pieces of user-supplied information (eg. This must be more than a simple chat feature). When a user creates a post, their username must be displayed on that post. You may allow guest posts if you'd like, but it is not required (Guest posts can make testing easier though). To build this feature you must include:

* A clear way for users to create posts (A reasonable person who logs in to your app must be able to figure out how to make a post)  
* When a post is created, the server will verify the author and add their username to the post (Do not trust the user to supply their username without proper authentication and verification)  
* All logged in users should be able to see all posts (You may decide if guest users can view posts)  
* It is ok if a refresh is required to see new posts  
* Posts must be stored in your database

Once a post is created, all authenticated users must be able to interact with each post in a way that takes their username and the specific post into account. This is open for interpretation and creativity so it can fit into whatever idea you have for your app. If your entire team is not creative, you can build a like button that prevents a user from liking the same post twice. Any interaction you design must meet the following criteria:

* Interactions are stored in your database  
* All interactions should be visible to all \[authenticated\] users (You decide if guests can see interactions). It is ok if this requires a refresh to see new interactions  
* Your server must verify the user who made the interaction and take their username into account in some way (eg. The server checks if this user already liked this post and blocks the second like) (eg. Users can comment on posts and their username is displayed on their comments)  
* Interaction must be made on a per-post basis (eg. A user can like or comment on a specific post). It should be clear to all users which interactions are related to which posts (eg. Each post displays it's number of likes)

**Security:** You must escape any HTML supplied by your users

### Testing Procedure

1. Start your server using docker compose up  
2. Open a browser and navigate to http://localhost:8080/  
3. Create an account and login (You can reuse an account made while testing a previous objective)  
4. Find the way to create a post, enter all required information, and submit the post  
   1. Verify that the post appear on the page along with your username  
5. Open a second browser (Use Chrome and Firefox. Switch to the one you didn't use in the previous steps), and login with a different account (register a new account if you haven't already)  
   1. Create several posts in the second browser  
   2. Verify that all posts appear on the page along with your second username  
6. Go back to the first browser, refresh the page, and verify that the new posts appeared as expected  
7. Make another post from the first browser and verify that it appears in both browsers  
8. Find a way to interact with posts and from each browser, interact with posts made by the other user. If necessary to test interactions effectively, use a 3rd browser/account  
   1. This step is more open-ended since each team has much freedom in their design. Do whatever is needed to test the feature (eg. For likes, make sure you cannot like a post twice and ensure this check is made on the back end)  
   2. Make sure that the user and post were taken into account for each interaction. Interaction not associated with a specific post, or that make no difference who made the interaction, do not satisfy this objective  
9. Restart the server with "docker compose restart"  
10. Refresh the page in both browsers and verify that all posts and interactions still appear as expected  
11. **Security:** Verify that HTML is escaped in all user supplied strings

## Submission

All of your project files must be in your GitHub repo at the time of the deadline. Please remember to include:

* A docker-compose file in the root directory that exposes your app on port 8080  
* All of the static files you need to serve (HTML/CSS/JavaScript/images)

| It is strongly recommended that you download and test your submission. To do this, clone your repo, enter the directory where the project was cloned, run docker compose up, then navigate to localhost:8080 in your browser. This simulates exactly what the TAs will do during grading. If you have any Docker or docker compose issues during grading, your grade for each objective may be limited to a 1/3. |
| :---- |

Project Part 2
In this part of the project, you will add multimedia uploads and WebSocket interactions to your app. You will have much freedom in the design of your app and what features you build with these technologies.

In the third objective, you will deploy your app to the world. Notice that this part is due right before presentations start and your app must be deployed during your presentation (This way, every team must deploy by the part 2 deadline regardless of when they will present).

### Objective 1: Multimedia Uploads
Add multimedia uploads to your app. You can design your own feature for this objective as long as it meets the following criteria:

Logged in users are provided a clear way to upload multimedia (A reasonable person who logs in to your app must be able to figure out how to upload multimedia)
It is ok if users have to create and/or interact with a post before this feature is apparent
The uploaded multimedia can be an image, video, and/or audio and can be either static or streamed (eg. A group voice chat feature is acceptable even though it's not a static upload)
Other users can consume the multimedia that has been uploaded
It is acceptable if only a subset of users can consume the media (eg. Image uploads in DMs shouldn't be public to all users)

Any feature that meets these criteria will complete this objective. If you are having trouble thinking of an idea, here are some sample features that would meet all criteria:

Users can upload profile pictures which are displayed on each of their posts
Posts can contain images in addition to their text (An imageboard)
Posts can contain video in addition to their text (A YouTube clone)
Use WebRTC to build a voice chat feature
Use WebRTC to build a video conferencing feature (A Zoom clone)
A live-streaming app (A Twitch/YouTube Live clone)

Testing Procedure
Start your server using docker compose up
Open two browsers and navigate to http://localhost:8080/
Create an account and login in both browsers
Find a way to upload multimedia. When you find a way to do this, move on to step 5
If there is no clear way to do this, create and interact with posts and check if there's a way to upload multimedia on the posts
Look for any links to other pages on the app that may contain the feature
Refresh the home page
If there's still no clear way to upload multimedia after following all these steps, the feature is assumed to not be implemented.
Upload multimedia and verify that it is displayed to the other user
This step is open-ended as it will depend on the specific feature implemented by each team. Do whatever is needed to test the feature and verify that it meets the required criteria
If necessary to test interactions effectively, use a 3rd/4th/etc. browser/account
Restart the server with "docker compose restart"
Refresh the page in both/all browsers and verify that all multimedia is still displayed [This step can be skipped if the feature involves streaming multimedia]
Check for relevant security vulnerabilities

## Objective 2: WebSocket Interactions
Add WebSocket interactions to your app. You can design your own feature for this objective as long as it meets the following criteria:

Logged in users are provided a clear way to interact with each other using WebSockets (A reasonable person who logs in to your app must be able to figure out how to use this feature)
It is ok if users have to create and/or interact with a post before this feature is apparent
Interactions must be both sent and received via WebSockets (eg. You can't have messages sent to the server with WebSockets, but nother received by the user. It must be duplex communication)
You must actually use WebSockets. For example, the SocketIO library sometimes falls back to long-polling. You must prevent this from happening and force it to use WebSockets if you use this library
Other users must see the interaction immediately (Minus network delays) without requiring a refresh or any other action on their part
It is acceptable if only a subset of users can see the interactions (eg. DMs over WebSockets that are only shown to sender and recipient)
WebSocket interaction must be authenticated if the user is logged in and this authentication must matter to other users of your app
It's up to you if you want to allow guests to use your WebSocket feature. If they can, they must interact as a guest
If a user is logged in, their identity must be taken into account in all their WebSocket interactions and displayed to other users. If 2 users both take an action, a 3rd user must be able to see who took which action

Any feature that meets these criteria will complete this objective. If you are having trouble thinking of an idea, here are some sample features that would meet all criteria:

Add a user list and a way to send DMs
Convert your post interactions to use WebSockets (No refresh or polling to see new interactions)
Convert uploading posts to use WebSockets (No refresh or polling to see new posts)  -required!!!
Add a live chat feature (Either global or separate chat rooms)
Build a game where player actions are sent to all other players in real-time. Usernames should be displayed to other players
A drawing app where users can all draw on a shared JS canvas with actions shared live. Each user draws in a different color with a key displayed to all users so they know who drew which parts of the drawing
A Google Docs clone where all users can edit the same text and each user can see everyone else's cursor with their username displayed on their cursor
An auction app where bids are sent and updated in real-time. The name of the highest bidder is displayed to all users

Note: You will have to authenticate the WebSocket connections. This can take some work depending on the library you use as some of them make it difficult to access the HTTP upgrade request that contains your auth token. Once a connection is authenticated, you can treat all WS frames over that connection as authenticated.

Testing Procedure
Start your server using docker compose up
Open two browsers and navigate to http://localhost:8080/
Create an account and login in both browsers
Open the network tab and refresh the page
Verify that there is a 101 response that upgrades to WebSockets
View the messages on this connection while testing this objective
Find a way to interact using WebSockets. When you find a way to do this, move on to step 6
While watching for messages on WebSocket connections, use all the features of the app until you find one that sends messages over the connection
Look for any links to other pages on the app that may contain the feature
Refresh the home page
If you've used all apparent features of the app without seeing a message over the WebSocket connection, the feature is assumed to not be implemented.
Use the WebSocket feature
Verify that messages are both sent and received by at least one user each (eg. One user can send with another receiving which would be the case for DMs)
Verify that the messages are critical to the functionality of the feature (eg. The messages should not be superficial just to say it uses WebSockets)
Verify that interactions are real-time and do not require a refresh or polling
Verify that each user's account mattered in the WebSocket interactions as was apparent to other users
If two users can take an action and they appear the same to a third user, this criteria is not met and the objective is not complete (eg. A Google doc clone where you can't identify other users earns a 1/3 for this objective) (eg. If post interactions are converted to WebSockets and the interaction is a like button that only displays the total number of likes, that's a 1/3 for this objective since a 3rd user would only see the number go up with no indication of who liked the post)
As with other objectives, this is open-ended as it will depend on the specific feature implemented by each team. Do whatever else is needed to test the feature and verify that it meets the required criteria
If necessary to test interactions effectively, use a 3rd/4th/etc. browser/account
Check for relevant security vulnerabilities

## Objective 3: Deployment and Encryption
Deploy your app on a publicly available server with a domain name and HTTPS with a valid certificate. You may use any means available to accomplish this, though it is recommended that you take advantage of the GitHub Student Developer Pack.

When deployed, add a link to your app in the readme of your repository so we can find your deployment.

Note the following implications of this objective:

You will use the WSS protocol for your WebSocket connection (If you finished the WebSocket objective)
Your certificate must be valid. It's recommended that you use CertBot to acquire a free certificate
Any HTTP requests must be redirected to use HTTPS. Do not let users access your app with unencrypted requests

Free Clause: You are not required to spend any money to take this course. If your team is in a situation where you need to spend money to deploy your app (eg. Every member of your team already used your student developer pack credit on other projects), please let me (Jesse) know and I'll work with you to ensure you are not required to spend money on the course requirements. You pay enough in tuition. You do not need to pay more to take a class.

Security: Do not map port 27017:27017 for your MongoDB in your docker-compose file. This is a major security risk that makes your database publicly available. Since you are deploying on the Internet in this objective, that means everyone on the planet would have access to your DB and attackers will steal your data. Some of you have been using this in your development environments, but this MUST be removed before deploying. 
Testing Procedure
Find the app url in the project repo and navigate to the public deployment
Ensure the page loads using an HTTPS connection and no security warnings appear
Navigate to the same app using HTTP and verify that you are redirected to the app using HTTPS
If objective 2 is complete, verify that the WebSocket connection is encrypted using WSS
Security: In the repo, check the docker compose file and ensure that port 27017 is not mapped to a local port. If it is, attempt to access the deployed DB and ensure that it is not publicly available. If it is publicly available in production, that's game over for this objective

Submission
All of your project files must be in your GitHub repo at the time of the deadline. Please remember to include:

A docker-compose file in the root directory that exposes your app on port 8080
All of the static files you need to serve (HTML/CSS/JavaScript/images)
Add your public link to your deployment to the README in your repo


It is strongly recommended that you download and test your submission. To do this, clone your repo, enter the directory where the project was cloned, run docker compose up, then navigate to localhost:8080 in your browser. This simulates exactly what the TAs will do during grading.

If you have any Docker or docker compose issues during grading, your grade for each objective may be limited to a 1/3.

# Project Part 3
## Objective 1: A Sense of Time
Add a feature to your app that takes timing into consideration. You can design your own feature for this objective as long as it meets the following criteria:

Timing must be controlled and verified by your server (No front end timing control)
The current timing is sent from the server and displayed to all relevant users in real-time
Timing must have <= 1 second accuracy
There is a fixed point in time where the functionality of the app changes
Timing must be initiated by a user[s]
The feature must involve interactions between users

Any feature that meets these criteria will complete this objective. If you are having trouble thinking of an idea, here are some sample features that would meet all criteria:

A game/auction/sale/quiz/etc with a time limit. The server tracks the time and sends the time remaining to all users every second which is displayed on the front end. When time expires, the game ends / auction ends and is awarded to the highest bidder / the sale ends and the price returns to the original pre-sale price / the quiz ends and submissions are no longer accepted / etc
Each game/auction/sale/quiz/etc is created/started by a user
DMs/video chats/meetings started by the users with a set end time. The server sends the current time every second to all users which is displayed along with the end time. When the event ends, users cannot send messages/all video feeds end
Users can schedule posts. A user can create a post and select a timestamp or delay after which the server will make the post public to all users. The server sends the user who created the post the time remaining before the post goes public every second which is displayed on their app
A turn-based game that tracks the total time taken by each player during their turns. The time is tracked by the server and sent to all players every second
A user list that displays the total time each user has been active on the app. All times are tracked by the server and sent to all users every second
Same idea, but display how long a user has been inactive. Check if the tab is focussed or react to mouse movement to tell the server when to reset the timer

### Testing Procedure
Start your server using docker compose up
Open two browsers and navigate to http://localhost:8080/
Create an account and login in both browsers
Find a feature that implements a sense of timing. When you find a way to do this, move on to step 5
If there is no clear way to do this, create and interact with posts and check if the feature is made apparent
Look for any links to other pages on the app that may contain the feature
Refresh the home page
If there's still no clear feature that uses timing after following all these steps, the feature is assumed to not be implemented.
Interact with the timing feature and verify that it meets all the required criteria
This step is open-ended as it will depend on the specific feature implemented by each team. Do whatever is needed to test the feature and verify that it meets the required criteria
If necessary to test interactions effectively, use a 3rd/4th/etc. browser/account
Check for relevant security vulnerabilities

## Objective 2: DoS Protection (IP rate limiting)
Add very basic DoS protection to your app based on rate limiting IP addresses. Your IP protection should:

Block requests from an IP address if it has made more than 50 requests within a 10 second period
Every single request from an IP should count towards this limit (eg. Just loading your homepage requires ~5 requests that all count toward the limit)
While an IP is blocked, respond to all requests from the IP with a 429 "Too Many Requests" response with a message explaining the issue to the user
When an IP becomes blocked, it should remain blocked for 30 seconds
After 30 seconds pass, requests from the IP should be handled as usual unless they hit your rate limit and become blocked again
### Testing Procedure
Navigate to the public deployment
Count the number of requests made to load the page
Refresh slowly enough times to reach 70 requests, but not fast enough to trigger the rate limiter (<50 requests per 10 seconds)
Ensure all requests are handled as expected
Wait ~10 seconds
Refresh quickly such that >50 requests are sent in at 10 second window
Ensure that after the 50th request, you start seeing 429 responses and the page no longer loads
Wait ~20 seconds
Refresh the page and ensure that you are still blocked
Wait another ~10 seconds
Refresh the page and ensure that it loads
[Hit the rate limit again on the same device] Refresh quickly such that >50 requests are sent in at 10 second window
Ensure that after the 50th request, you start seeing 429 responses and the page no longer loads
Within 30 seconds, on a second device with a different public IP address, navigate to the public deployment and ensure that the page loads
Make sure the other device has a different public IP address. If you are at a residence, all your devices probably have the same public IP address. To ensure you have a different IP, you can use your phone on mobile data, or turn on a VPN

## Objective 3: Creativity and Documentation
Add one more feature to your app of your own design and document this feature in your project's README. You have a significant amount of flexibility for this objective.

Requirements:

Your feature cannot be a subset (⊆) of the requirements, of any other objective in this course across all project parts and homework assignments
It's ok to have overlap with an existing objective [or be a proper superset of the requirements] as long as you add something extra that was not required (eg. You can use WebSockets as long as you do something in addition to basic interactions [part2o2] or timing [part3o1])
Add a description of your feature in the README of your repository on the default branch
Write your own testing procedures for this feature in your README that the TAs will follow during grading

Note: This objective is extremely open-ended and there will likely be many very simple features that can be developed that technically meet the "no subset" requirement. These features will be accepted for credit no matter how simple as long as you can argue that what you did was not required in any other objective.
### Testing Procedure
Navigate to the repository on GitHub and read the README on the default branch (eg. Click the repo link and scroll down to find the documentation. If any other steps are required, the objective is assumed to not be implemented)
Find and review the description of the extra feature in the README
Verify that the description of the feature is clear and understandable 
Verify that the feature is not a subset of any other objective in this course
Find the testing procedures for this feature in the README
Follow the testing procedure and verify that the app passes the teams testing procedures

Submission
All of your project files must be in your GitHub repo at the time of the deadline. Please remember to include:

A docker-compose file in the root directory that exposes your app on port 8080
All of the static files you need to serve (HTML/CSS/JavaScript/images)


It is strongly recommended that you download and test your submission. To do this, clone your repo, enter the directory where the project was cloned, run docker compose up, then navigate to localhost:8080 in your browser. This simulates exactly what the TAs will do during grading.

If you have any Docker or docker compose issues during grading, your grade for each objective may be limited to a 1/3.

Team Scoring
Each objective will be scored on a 0-3 scale as follows:

3 (Complete)
Clearly correct. Following the testing procedure results in all expected behavior
2 (Complete)
Mostly correct, but with some minor issues. Following the testing procedure does not give the exact expected results, but all features are functional
1 (Incomplete)
Not all features outlined in this document are functional, but an honest attempt was made to complete the objective. Following the testing procedure gives an incorrect result, or no results at all, during any step. This includes issues running Docker or docker-compose even if the code for the objective is correct
0.3 (Incomplete)
The objective would earn a 3, but a security risk was found while testing
0.2 (Incomplete)
The objective would earn a 2, but a security risk was found while testing
0.1 (Incomplete)
The objective would earn a 1, but a security risk was found while testing
0 (Incomplete)
No attempt to complete the objective or violation of the assignment (Ex. Using an HTTP library)

Note that for your final grade there is no difference between a 2 and 3, or a 0 and a 1. The numeric score is meant to give you more feedback on your work.

3
Objective Complete
2
Objective Complete
1
Objective Not Complete
0
Objective Not Complete

Please note that there is only one chance to earn these application objectives. There will not be a second deadline for any part of the project.

Individual Grading
The grading above will be used to determine your team score which is based on the functionality of your project. Your actual grade may be adjusted based on your individual contributions to the project. These decisions will be made on a case-by-case basis at the discretion of the course staff. Factors used to determine these adjustments include:

Your meeting form submissions: team meeting and eval form 
You must fill out this form after every meeting. Failure to do so is an easy way to earn a negative individual grade adjustment. Since you have weekly meetings, you are expected to have as many form submissions as there were weeks for this part of the project
The quality of your submissions will be taken into account as well (eg. Saying "I'll do stuff" before the next meeting is a low quality submission)
You may submit more meeting forms than are required even if there was no meeting (eg. If you want to adjust your evals after a deadline without waiting for the next meeting)
Your evaluations from the meeting form
If your teammates rated you poorly/excellently, your grade may be adjusted down/up respectively
Your commits in the team repo
Your commits may be checked to see if you did in fact complete the work you mentioned in the meeting form, as well as compare the amount of work you completed to that of your teammates
You MUST commit your own code! It is not acceptable for your teammate to commit your code for you. You should have a clear separation between your tasks and commit the code for your task. If a commit is not in your name, you effectively did not write that code. If a teammate is making this difficult, let the course staff know in the meeting form
If you don't have any commits on the default branch of the repo, you effectively did not work on the project and will earn a 0 after individual grade adjustments

Security Essay
For each objective for which your team earned a 0.3 or 0.2, you will still have an opportunity to earn credit for the objective by submitting an essay about the security issue you exposed. These essays must:

Be at least 1000 words in length
Explain the security issue from your submission with specific details about your code
Describe how you fixed the issue in your submission with specific details about the code you changed
Explain why this security issue is a concern and the damage that could be done if you exposed this issue in production code with live users

Any submission that does not meet all these criteria will be rejected and you will not earn credit for the objective.

Security essays are individual assignments. It is important that every member of the team understands the importance of preventing security vulnerabilities even if they did not write the offending code. Multiple members of a team submitting the same, or similar, essays is an academic integrity violation.

Due Date: Security essays are due 1-week after grades are released.

Any essay may be subject to an interview with the course staff to verify that you understand the importance of the security issue that you exposed. If an interview is required, you will be contacted by the course staff for scheduling. Decisions of whether or not an interview is required will be made at the discretion of the course staff.


