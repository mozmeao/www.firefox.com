from operator import itemgetter

import pytest
import json


# Test data
supported_versions = (
    ("tlsv1", "1.0"),
    ("tlsv1_1", "1.1"),
    ("tlsv1_2", "1.2"),
)

unsupported_versions = (
    ("tlsv1_3", "1.3"),
)

# Sampling of valid ciphers, intending to show that we support
# some new secure items for those who want it, and some old
# insecure items for those who need it.
ciphers = (
    ('weak_RSA_3DES_112', 'TLS_RSA_WITH_3DES_EDE_CBC_SHA'),
    ('strong_ECDHE_RSA_AES_256', 'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384'),
)

# Little helper function
def load_json(file='fixtures/ssl.json'):
    with open(file) as f:
        data = json.load(f)

    return data


@pytest.mark.parametrize("version", supported_versions, ids=itemgetter(0))
def test_enabled_protocols(version):
    json = load_json()
    supported_protocols = json[0]['endpoints'][0]['details']['protocols']
    found = False
    for prot in supported_protocols:
        if prot['version'] == version[1]:
            found = True
    assert found


@pytest.mark.parametrize("version", unsupported_versions, ids=itemgetter(0))
def test_disabled_protocols(version):
    json = load_json()
    supported_protocols = json[0]['endpoints'][0]['details']['protocols']
    found = False
    for prot in supported_protocols:
        if prot['version'] == version[1]:
            found = True
    assert ~found


@pytest.mark.parametrize("cipher", ciphers, ids=itemgetter(0))
def test_enabled_ciphers(cipher):
    json = load_json()
    supported_suite = json[0]['endpoints'][0]['details']['suites']['list']
    found = False
    for cipher_description in supported_suite:
        if cipher_description['name'] == cipher[1]:
            found = True
    assert found


