import pytest
from pydantic import ValidationError

from wazuh.core.config.models.ssl_config import SSLConfig, IndexerSSLConfig, SSLProtocol, APISSLConfig


@pytest.mark.parametrize("init_values,expected", [
    (
        {"key": "key_example", "cert": "cert_example", "ca": "ca_example"},
        ""
    ),
    (
        {"key": "key_example", "cert": "cert_example", "ca": "ca_example", "keyfile_password": "example"},
        "example"
    )
])
def test_ssl_config_default_values(init_values, expected):
    """Check the correct initialization of the `SSLConfig` class."""
    ssl_config = SSLConfig(**init_values)

    assert ssl_config.keyfile_password == expected


@pytest.mark.parametrize("init_values", [
    {},
    {"key": "key_example"},
    {"key": "key_example", "cert": "cert_example"},
])
def test_ssl_config_fails_without_values(init_values):
    """Check the correct behavior of the `SSLConfig` class validations."""
    with pytest.raises(ValidationError):
        _ = SSLConfig(**init_values)


@pytest.mark.parametrize("init_values,expected", [
    (
        {},
        {"use_ssl": False, "key": "", "cert": "", "ca": ""}
    ),
    (
        {"use_ssl": True},
        {"use_ssl": True, "key": "", "cert": "", "ca": ""}
    ),
    (
        {"use_ssl": True, "key": "key_example"},
        {"use_ssl": True, "key": "key_example", "cert": "", "ca": ""}
    ),
    (
        {"use_ssl": True, "key": "key_example", "cert": "cert_example"},
        {"use_ssl": True, "key": "key_example", "cert": "cert_example", "ca": ""}
    ),
    (
        {"use_ssl": True, "key": "key_example", "cert": "cert_example", "ca": "ca_example"},
        {"use_ssl": True, "key": "key_example", "cert": "cert_example", "ca": "ca_example"}
    )
])
def test_indexer_ssl_config_default_values(init_values, expected):
    """Check the correct initialization of the `IndexerSSLConfig` class."""
    ssl_config = IndexerSSLConfig(**init_values)

    assert ssl_config.use_ssl == expected["use_ssl"]
    assert ssl_config.key == expected["key"]
    assert ssl_config.cert == expected["cert"]
    assert ssl_config.ca == expected["ca"]


@pytest.mark.parametrize("init_values,expected", [
    (
        {"key": "key_example", "cert": "cert_example"},
        {"use_ca": False, "ca": "", "ssl_protocol": SSLProtocol.auto, "ssl_ciphers": ""}
    ),
    (
        {"key": "key_example", "cert": "cert_example", "use_ca": True},
        {"use_ca": True, "ca": "", "ssl_protocol": SSLProtocol.auto, "ssl_ciphers": ""}
    ),
    (
        {"key": "key_example", "cert": "cert_example", "use_ca": True, "ca": "ca_example"},
        {"use_ca": True, "ca": "ca_example", "ssl_protocol": SSLProtocol.auto, "ssl_ciphers": ""}
    ),
    (
        {"key": "key_example", "cert": "cert_example", "use_ca": True, "ca": "ca_example", "ssl_protocol": SSLProtocol.tls},
        {"use_ca": True, "ca": "ca_example", "ssl_protocol": SSLProtocol.tls, "ssl_ciphers": ""}
    ),
    (
        {"key": "key_example", "cert": "cert_example", "use_ca": True, "ca": "ca_example", "ssl_protocol": SSLProtocol.tls, "ssl_ciphers": "cipher_example"},
        {"use_ca": True, "ca": "ca_example", "ssl_protocol": SSLProtocol.tls, "ssl_ciphers": "cipher_example"}
    )
])
def test_api_ssl_config_default_values(init_values, expected):
    """Check the correct initialization of the `APISSLConfig` class."""
    ssl_config = APISSLConfig(**init_values)

    assert ssl_config.use_ca == expected["use_ca"]
    assert ssl_config.ca == expected["ca"]
    assert ssl_config.ssl_protocol == expected["ssl_protocol"]
    assert ssl_config.ssl_ciphers == expected["ssl_ciphers"]


@pytest.mark.parametrize("init_values", [
    {},
    {"key": "key_example"},
    {"cert": "cert_example"}
])
def test_api_ssl_config_fails_without_values(init_values):
    """Check the correct behavior of the `APISSLConfig` class validations."""
    with pytest.raises(ValidationError):
        _ = APISSLConfig(**init_values)
