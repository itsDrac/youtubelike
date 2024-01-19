# Coffee aur Backend

This is a replica of project tought in [Chai aur backend](https://youtube.com/playlist?list=PLu71SKxNbfoBGh_8p_NS-ZAh6v7HhYqHW&si=j0kNpJ5cKXvoAtOO) playlist in youtube but in python fastapi

## Setup
The code is using python3 and mongodb, prefired way of using would be docker (Still learning it), you can spin up a mongodb docker container(Not included in this repo as i an doing it via docker command with fixed image I'll probably add dockerfile for then when I'll know how to run cli command in dockerfile)
and another container for python3 -> copy files in container or make a virtual enviroment locally and user command
```
python run.py
```

### Completed video [#12](https://youtu.be/HqcGLJSORaA?si=hFm-Jg4IUhVdjHpX)

### Thoughts as per this commit
The file system pattern or program structure I am using is of my own (I didn't invent it) but its not same as in playlist. 
In this pattern I assume every functionality is a app of itself.
meaning everything related to user would go in `user` folder and everything related to video would go in `video` folder
So, as of this commit the routes and controllers for user are in user folder. Later on I am planning to add models and schema related to user in same folder itself.
**Feedback required** let me know if this is write approch and this is something used is production grade apps aswell.

## Contribution
All contribution are welcomed specially code review 
Please watch [this](https://youtu.be/EKRdobRY-fc?si=6pxqDU3C8fgeWsHB) before opening PR

## Why `Coffee aur Backend`?
Because I dont like chat or nodejs :)
