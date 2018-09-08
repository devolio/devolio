# Devolio (WIP)

The project is very new and the code quality is not the best. 
**Help welcome and wanted. Beginners are very welcome too.**

Check out the [issues][0] to get started. Or ping me @mustafa on [DevChat][1]

## Run on Docker

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

[0]: https://github.com/devolio/devolio/issues
[1]: https://devchat.devolio.net/
[2]: https://docs.docker.com/install/
