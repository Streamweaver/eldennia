# Welcome to Eldennia!

This is a playspace for me to experiment with docker deployments and some code related to procedural genreation of text descriptions from NLP processing of literary sources that I will dump to a MUD


Your game's main configuration file is found in
`server/conf/settings.py` but for development I'm passing development settings via the --settings flag with evennia commands.

    evennia migrate --settings conf/dev/settings.py

To start the server, stand in this directory and run

    evennia start [-i to run in forground] --settings conf/dev/settings.py

MUD client connect is on port 4000, Webclient connect is on port 8000

# Resources

From here on you might want to look at one of the beginner tutorials:
http://github.com/evennia/evennia/wiki/Tutorials.

Evennia's documentation is here:
https://github.com/evennia/evennia/wiki.

Enjoy!
