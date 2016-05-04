# Welcome to Eldennia!

This is a playspace for me to experiment with docker deployments and some code related to procedural genreation of text descriptions from NLP processing of literary sources that I will dump to a MUD

## Running from Docker

I've set this project to run under docker as a volume mounted to this directory.

Obviously this is being used for development only and I'll work out a production docker container at a different time.

### Starting Docker Containers

Starting is done via docker compose.  The Dockerfile has already setup the proper working directory and uses "evennia" as the entrypoint internally.  To start via docker-compose it must be started as a deamon like so:

  `> docker-compose up -d`

### Stopping Docker Containers

**It is important** that you stop evennia itself before shutting down the containers.  Do this via docker exec on the container like so:

  `> docker exec elennia evennia stop`

If you don't do this, you will have to remove the *.pid files manually from /eldennia/server/conf in order for the processes to start again.  If you get a PID stale error, this is likely the problem.

Once the MUD itself is stopped just stop the containers with:

  `> docker-compose stop`

# Resources

From here on you might want to look at one of the beginner tutorials:
http://github.com/evennia/evennia/wiki/Tutorials.

Evennia's documentation is here:
https://github.com/evennia/evennia/wiki.

Enjoy!
