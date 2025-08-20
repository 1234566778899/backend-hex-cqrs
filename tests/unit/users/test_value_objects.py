import pytest
from app.contexts.users.domain.value_objects import Email, Name, UserId

def test_email_valido():
    e = Email("user@example.com")
    assert e.value == "user@example.com"

@pytest.mark.parametrize("bad", ["bad", "x@", "@x.com", "x@x", "x x@x.com"])
def test_email_invalido(bad):
    with pytest.raises(ValueError):
        Email(bad)

def test_name_valido():
    n = Name("Ada")
    assert n.value == "Ada"

@pytest.mark.parametrize("bad", ["", " "])
def test_name_invalido(bad):
    with pytest.raises(ValueError):
        Name(bad)

def test_user_id_valido():
    uid = UserId("1234567890")
    assert uid.value == "1234567890"

@pytest.mark.parametrize("bad", ["", "123", None])
def test_user_id_invalido(bad):
    with pytest.raises(Exception):
        UserId(bad) 