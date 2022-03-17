#### Telegram to do list bot

#### Frameworks and languages used

ExpressJS | NodeJS | MongoDB | Python | JavaScript

#### Description

The bot acts as a place for users to track their the tasks they want to accomplish. Since most students and non-students use Telegram the most, I felt that developing a bot that tracks their tasks would not hinder their workflow.

This bot uses the telegram.ext module to design the user interface in the bot. The backend is developed using MongoDB, ExpressJS and NodeJS. The HTTP requests are managed using the requests module in python.

Some challenges I faced was trying to access my REST API using the requests module, as it was the first time using it. But it was a small hurdle to overcome. Another difficulty was the removeTodo function. After using the inlinekeyboardbutton, the callback_query has to send an answer to the bot. I did not understand this concept, and wasn't able to create a multi-select option for deleting the tasks. Thus now only after selecting all the options and clicking "Done" will the callback_query be answered and the operation to delete the selected tasks be executed.

#### Planned improvements

Some changes to be included are in the delete function. Currently it uses a for loop which has a time complexity of O(n). This is not a good way forward for the program, as as the todo-list gets bigger, the time it takes for the user to delete the functions will be increased. I will be exploring other data structures where the delete functionality is of constant time.

Another change would be the due date entry for the user. Currently, the bot accepts only dates in the yyyy-mm-dd option, as I am using monogDB validators for entering the dates. The improvement would be to add a script to detect the date formats entered and then convert it into the date format that is accepted by the mongoDB validators.

#### Using the bot

The bot can be accessed through the link t.me/yyTut_bot.

#### Bot Functions

When you first launch the bot, please press /start for the bot to walk you through the initial few steps. After that you can always go to /help if you can't remember the functions.

The server stores tasks with a createdBy attribute, which links the ID of the user which created the task to the task.

/login performs a POST request to the server with the user's username and password. The program checks the hashed password to see if such a user exists and returns a response which contains the token that carries the userID. The token is decoded and then we only retireve tasks where the createdBy attribute matches the ID in the token.

/register performs a POST request to the server with the user's username and password and stores the password in a hashed formed.

/getAllTasks performs a GET request to the server to get all tasks where the createdBy matches the ID returned in the token.

/addTask performs a POST request to the server to add a new task by the user.

/removeTodo performs a DELETE request to the server to delete the tasks the user has selected.
