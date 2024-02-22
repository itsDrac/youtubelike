# YoutubeLike

This is a web api app build in python fastapi framework, its functonility are similar to youtube where in you can make user(channel) who can upload videos and twittes and subcribe to other channels.

## Setup
The code is using python3 and mongodb, prefired way of using would be docker (Still learning it), you can spin up a mongodb docker container(Not included in this repo as i an doing it via docker command with fixed image I'll probably add dockerfile for then when I'll know how to run cli command in dockerfile)
and another container for python3 -> copy files in container or make a virtual enviroment locally and user command
```
python run.py
```

### Thoughts as per this commit
The file system pattern or program structure I am using is of my own (I didn't invent it) but its not same as in nodejs. 
In this pattern I assume every functionality is a app of itself.
meaning everything related to user would go in `user` folder and everything related to video would go in `video` folder

I am not using middleware for uploading the file first in server than in clodinary, for this I have just created some helper function which can do same task for me.

In refersh access token I am accepting refersh token from cookie and/or header

I have added aggregation pipeline to best of my knowledge please have a look.
**Feedback required** let me know if this is write approch and this is something used is production grade apps aswell.
**Feedback required** Please test this API from Postman you'll just need to set some `.env` variable and a mangodb database, I am using docker for mongodb

## Error code and Meaning

| Error     | Meaning                   |
|-----------|:-------------------------:|
|511        |File not saved in server   |
|512        |File not saved in clodinary|

## Code Syntax guideline
- All the variable should be `camelCase`
- All the class name should be `PascalCase`
- All method/function name should be `snake_case`

__Note:__ Please follow these guideline, or if you see anyplace I have not followed please make a pull request.

## Contribution
All contribution are welcomed specially code review 
Please watch [this](https://youtu.be/EKRdobRY-fc?si=6pxqDU3C8fgeWsHB) before opening PR

## Showcase
[Here](https://www.loom.com/share/4387f24102394f5da4089abb2ebf1b8a?sid=6d094760-f7c4-470f-a72b-79c6f81b8b26) is the link to a video I recorded showcasing some functionility of application
