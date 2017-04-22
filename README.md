# Devolio (WIP)

The project is very new and the code quality is not the best.

## Run on Docker

1. Make sure `docker` is running and that you have `make` is installed.
2. Create your own `env` file by running `cp dev/env.sample dev/env`
3. Edit the `env` file to contain the required environment variables.
    Make sure to not use quotes `"` or `'` around the values.
4. Build the image by running: `make devolio`
5. Run the app: `make rd` (to stop it run `make kd`)
6. [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Code reloading should be working.