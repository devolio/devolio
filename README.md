# DevChat.dev -- work in progress

[DevChat.dev](https://devchat.dev/questions) is a sister community to [DevChat on Slack][1].
It acts as an open repository for programming/CS related questions and answers. We created it to be a more welcoming, open and friendly alternative to StackOverflow. 


## Help welcome and wanted. Beginners are very welcome too

DevChat.dev (prev. Devolio) is a canvas for developers new and old to work together on a community project.

Developers, designers, and writers are welcome to join. We will be announcing more details in [#community_projects][3].

Check out the [issues][0] to get started. Or ping me @mustafa on our [Slack][1]

## Set up the development environment

1. Make sure that [Docker][2] is running and that you have `make` is installed.
2. Create your own `env` file by running `cp dev/env.sample dev/env`.
3. Edit the `env` file to contain the required environment variables.
    Make sure to not use quotes `"` or `'` around the values.
4. Build the image by running: `make base`
5. Run the app: `make up`
6. Open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
7. Commands:
    - `make down` to shut down the server and the container.
    - `make shell` to "ssh" into the container.
    - `make ds` to start the Django shell.
    - `make logs` to view the server logs.

Code reloading should be working.

[0]: https://github.com/devchat-dev/devolio/issues
[1]: https://devchat.devolio.net/
[2]: https://docs.docker.com/install/
[3]: https://app.slack.com/client/T0Q0J6DM0/C0QBD2WLV
