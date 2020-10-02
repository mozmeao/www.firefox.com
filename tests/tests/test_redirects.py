from operator import itemgetter

import pytest
import requests


URLS = (
    ("/m/FOO", "https://www.mozilla.org/firefox/new/?redirect_source=firefox-com"),
    (
        "/universityambassadors",
        "https://campus.mozilla.community/?redirect_source=firefox-com",
    ),
    (
        "/os/FOO",
        "https://support.mozilla.org/products/firefox-os?redirect_source=firefox-com",
    ),
    (
        "/desktop/FOO",
        "https://www.mozilla.org/firefox/desktop/?redirect_source=firefox-com",
        301,
    ),
    (
        "/android/FOO",
        "https://www.mozilla.org/firefox/android/?redirect_source=firefox-com",
        301,
    ),
    (
        "/developer/FOO",
        "https://www.mozilla.org/firefox/developer/?redirect_source=firefox-com",
        301,
    ),
    (
        "/10",
        "https://www.mozilla.org/firefox/features/independent/?redirect_source=firefox-com",
        301,
    ),
    (
        "/independent/FOO",
        "https://www.mozilla.org/firefox/features/independent/?redirect_source=firefox-com",
        301,
    ),
    (
        "/hello/FOO",
        "https://www.mozilla.org/firefox/hello/?redirect_source=firefox-com",
        301,
    ),
    # test extra URL params are passed through
    (
        "/hello/FOO?name=dude",
        "https://www.mozilla.org/firefox/hello/?redirect_source=firefox-com&name=dude",
        301,
    ),
    (
        "/personal/",
        "https://www.mozilla.org/firefox/personal/?redirect_source=firefox-com",
        301,
    ),
    ("/choose/", "https://www.mozilla.org/firefox/choose/?redirect_source=firefox-com"),
    ("/switch/", "https://www.mozilla.org/firefox/switch/?redirect_source=firefox-com"),
    (
        "/enterprise/",
        "https://www.mozilla.org/firefox/enterprise/?redirect_source=firefox-com",
        301,
    ),
    (
        "/containers/",
        "https://www.mozilla.org/firefox/facebookcontainer/?redirect_source=firefox-com",
    ),
    (
        "/pdx/",
        "https://www.mozilla.org/firefox/new/?xv=portland&campaign=city-portland-2018&redirect_source=firefox-com",
    ),
    ("/pair/", "https://accounts.firefox.com/pair/", 301),
    ("/nightly/", "https://www.mozilla.org/en-US/firefox/channel/desktop/#nightly", 301),
    ("/join/", "https://www.mozilla.org/firefox/accounts/?redirect_source=join", 301),
    ("/rejoindre/", "https://www.mozilla.org/firefox/accounts/?redirect_source=join", 301),
    ("/privacy/", "https://www.mozilla.org/firefox/privacy/products/?redirect_source=firefox-com"),
    ("/privatsphaere/", "https://www.mozilla.org/firefox/privacy/products/?redirect_source=firefox-com"),
    ("/vieprivee/", "https://www.mozilla.org/firefox/privacy/products/?redirect_source=firefox-com"),
    ("/vieprivée/", "https://www.mozilla.org/firefox/privacy/products/?redirect_source=firefox-com"),
    ("/unfck/", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                "utm_medium=referral&utm_source=firefox.com&utm_campaign=unfck", 301),
    (
        # any incoming utm params should replace the default ones
        "/unfck/?utm_campaign=social",
        "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&utm_campaign=social",
        301
    ),
    (
        # any incoming utm params should replace the default ones
        "/love?utm_source=twitter&utm_medium=aether",
        "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&utm_source=twitter&utm_medium=aether",
        301
    ),
    ("/unfuck", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                "utm_medium=referral&utm_source=firefox.com&utm_campaign=unfck", 301),
    ("/love", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
              "utm_medium=referral&utm_source=firefox.com&utm_campaign=unfck", 301),
    ("/liebe", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
               "utm_medium=referral&utm_source=firefox.com&utm_campaign=unfck", 301),
    ("/rendonslenetplusnet", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
              "utm_medium=referral&utm_source=firefox.com&utm_campaign=unfck", 301),
    ("/armchair", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                  "utm_medium=audio&utm_source=armchair&utm_campaign=unfck&utm_content=podcast", 301),
    ("/jvn", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
             "utm_medium=audio&utm_source=jvn&utm_campaign=unfck&utm_content=podcast", 301),
    ("/literally", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                   "utm_medium=audio&utm_source=literally&utm_campaign=unfck&utm_content=podcast", 301),
    ("/pivot", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
               "utm_medium=audio&utm_source=pivot&utm_campaign=unfck&utm_content=podcast", 301),
    ("/podsave", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                 "utm_medium=audio&utm_source=podsave&utm_campaign=unfck&utm_content=podcast", 301),
    ("/smartless", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                   "utm_medium=audio&utm_source=smartless&utm_campaign=unfck&utm_content=podcast", 301),
    ("/thedaily", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                  "utm_medium=audio&utm_source=thedaily&utm_campaign=unfck&utm_content=podcast", 301),
    ("/ezra", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
              "utm_medium=audio&utm_source=ezra&utm_campaign=unfck&utm_content=podcast", 301),
    ("/explained", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
                   "utm_medium=audio&utm_source=explained&utm_campaign=unfck&utm_content=podcast", 301),
    ("/wtf", "https://www.mozilla.org/firefox/unfck/?redirect_source=firefox-com&"
             "utm_medium=audio&utm_source=wtf&utm_campaign=unfck&utm_content=podcast", 301),

    ("/any/other/url", "https://www.mozilla.org/firefox/new/?redirect_source=firefox-com"),
    ("/", "https://www.mozilla.org/firefox/new/?redirect_source=firefox-com"),
)
HEADERS = (
    ("Cache-Control", "public, max-age=1800"),
    ("Strict-Transport-Security", "max-age=31536000"),
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("X-XSS-Protection", "1; mode=block"),
)


def assert_redirect(base_url, url, location, code=302):
    resp = requests.get(f"{base_url}{url}", allow_redirects=False)
    assert resp.status_code == code
    assert resp.headers["location"] == location
    assert resp.headers["Strict-Transport-Security"] == "max-age=31536000"
    assert resp.headers["Cache-Control"] == "public, max-age=1800"


@pytest.mark.parametrize("args", URLS, ids=itemgetter(0))
def test_redirect(args, base_url):
    assert_redirect(base_url, *args)


@pytest.mark.parametrize("path", ["/healthz/"])
def test_security_headers(path, base_url):
    resp = requests.get(f"{base_url}{path}", allow_redirects=False)
    for header, value in HEADERS:
        assert resp.headers[header] == value


def test_healthz(base_url):
    resp = requests.get(f"{base_url}/healthz/", allow_redirects=False)
    assert resp.status_code == 200
    assert "Content-Security-Policy" in resp.headers
    assert "Firefox.com Redirector Service" in resp.text
