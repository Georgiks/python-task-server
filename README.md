# python-task-server

All informations provided in uploaded files.

Game info:
You have 5 factory stations, and each station is connected to every other station with one one-way tube.
And there is only one station which all tubes are going to. You have to find it out.

You have one man on the command center of the factory, which you can ask one simple question (type: 2->5)
if the tube is going to the other tube by this direction (from station 2 to station 5)
He just answer N for no and Y for yes.
You have only (5-1=4) allowed asks. Try to figure out which station is the one within the limits.
If you answer with any result, the task will be closed. (No mistakes!)

Man is server and you asks the server with your commands (see client.py to see more commands).
If the ask is not recongnized, the server will return "ERROR (reason)".

Server can handle many of tasks with their authentication.
Also when the server shutdown, the savefile will be created. After next startup of server, you will be asked to load it.
There is also possibility to give an OP authentication to game, so an admin can have access to any game.

It should be also no problem to create your own game with its mechanics, the server just pass the informations it gets to process to the server. (some methdos should be privded in the game, like- get_id(), process(), save() and should handle loading data like this task can)
