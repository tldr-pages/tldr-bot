tldr-bot
========

A simple [bot](https://github.com/tldr-bot) that performs automation tasks on the main [tldr repo](https://github.com/tldr-pages/tldr).

Quick start
-----------

First of all, set the needed environment variables:

    FLASK_APP=/path/to/app/tldr_bot.py
    BOT_TOKEN=<token>
    REPO_SLUG=tldr-pages/tldr
    PORT=<port>

Then run using Flask:

    flask run --port=$PORT

Run as a service
----------------

See the [`tldr-bot.service`](/tldr-bot.service) file for an example systemd unit configuration.

Typically, the service is running under uWSGI and fronted by nginx. So you need to set the proper nginx config too.

    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:6129;
    }
