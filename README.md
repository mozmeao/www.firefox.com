# www.firefox.com

Project running at www.firefox.com

## Run the tests

```bash
$ make test
```

You may also run the tests against production (https://www.firefox.com), but there
will be a number of failures until this service is in production due to changes
we've made to improve these redirects.

```bash
$ make test-prod
```

## Run the service locally

```bash
$ make run
```

Then open your browser to http://localhost:8080/healthz/ and you should see a page.
The `make test` and `make run` commands will stop the old containers and build new ones every time.
If you're just working with the `content` folder then you shouldn't need to restart
to see your changes. You will need to restart the system for changes to the `nginx.conf`.

