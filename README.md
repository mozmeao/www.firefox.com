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

# SSL Testing

To ensure that we're not changing ssl/tls settings between the existing www.firefox.com and our new setup, we're using the ssllabs command line tool to gather information about the websites.

### Install SSL Labs
Download from, `https://github.com/ssllabs/ssllabs-scan/releases` the right architecture.  I used v1.4.0 for this guide.  Extract it, and place on your path (`/usr/local/bin/ssllabs-scan). Ensure that the bin can be executed, chmod +x. This is a go binary, so it should be ok to run after that.

### To use

Set your BASE_URL environment variable to the website you're trying to test. `export BASE_URL=https://www.firefox.com` for example.
Them, `make test-ssl` to just pull the ssl info. Or `make test-all` to download the info and test it. It will be a bit slow, so you'll want to do `make test-external` to repeat the test
