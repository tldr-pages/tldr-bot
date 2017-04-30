# tldr-bot
A simple bot that performs automation tasks on the main tldr repo

## To run as a service, an environment file need to be set
An example of a file

```
GITHUB_URL=https://api.github.com
BOT_TOKEN=<token>
REPO_SLUG=tldr-pages/tldr
PORT=6129
FLASK_APP=/path/to/post_comment.py
```
