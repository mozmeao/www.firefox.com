from operator import itemgetter

import pytest
import requests


URLS = (
    ('/m/FOO', 'https://www.mozilla.org/m/FOO', 301),
    ('/universityambassadors', 'https://campus.mozilla.community/?redirect_source=firefox-com'),
    ('/os/FOO', 'https://www.mozilla.org/firefox/os/?redirect_source=firefox-com'),
    ('/desktop/FOO', 'https://www.mozilla.org/firefox/desktop/?redirect_source=firefox-com', 301),
    ('/android/FOO', 'https://www.mozilla.org/firefox/android/?redirect_source=firefox-com', 301),
    ('/developer/FOO', 'https://www.mozilla.org/firefox/developer/?redirect_source=firefox-com', 301),
    ('/10', 'https://www.mozilla.org/firefox/features/independent/?redirect_source=firefox-com', 301),
    ('/independent/FOO', 'https://www.mozilla.org/firefox/features/independent/?redirect_source=firefox-com', 301),
    ('/hello/FOO', 'https://www.mozilla.org/firefox/hello/?redirect_source=firefox-com', 301),
    # test extra URL params are passed through
    ('/hello/FOO?name=dude', 'https://www.mozilla.org/firefox/hello/?redirect_source=firefox-com&name=dude', 301),
    ('/personal/', 'https://www.mozilla.org/firefox/personal/?redirect_source=firefox-com', 301),
    ('/choose/', 'https://www.mozilla.org/firefox/choose/?redirect_source=firefox-com'),
    ('/switch/', 'https://www.mozilla.org/firefox/switch/?redirect_source=firefox-com'),
    ('/enterprise/', 'https://www.mozilla.org/firefox/enterprise/?redirect_source=firefox-com', 301),
    ('/containers/', 'https://www.mozilla.org/firefox/facebookcontainer/?redirect_source=firefox-com'),
    ('/pdx/', 'https://www.mozilla.org/firefox/new/?xv=portland&campaign=city-portland-2018&redirect_source=firefox-com'),
    ('/pair/', 'https://accounts.firefox.com/pair/', 301),
    ('/any/other/url', 'https://www.mozilla.org/firefox/new/?redirect_source=firefox-com'),
)


def assert_redirect(base_url, url, location, code=302):
    resp = requests.get(f'{base_url}{url}', allow_redirects=False)
    assert resp.status_code == code
    assert resp.headers['location'] == location


@pytest.mark.parametrize('args', URLS, ids=itemgetter(0))
def test_redirect(args, base_url):
    assert_redirect(base_url, *args)
