from pystacker.utils.common import envsubst, deep_update
import pytest


def test_envsubst():
    text = "abc${TEXT}"
    assert envsubst(text, TEXT='def') == 'abcdef'
    assert envsubst(text) == text

    text = "abc${TEXT:-some_default}"
    assert envsubst(text, TEXT='def') == 'abcdef'


def test_envsubst_default():
    text = "abc${TEXT:-some_default}"
    assert envsubst(text,) == 'abcsome_default'


def test_envsubst_multiline():
    text = "abc${TEXT}\nabc${TEXT}"
    assert envsubst(text, TEXT='def') == 'abcdef\nabcdef'


def test_envsubst_not_str():
    text = "abc${TEXT}"
    assert envsubst(text, TEXT=None) == 'abc'


def test_deep_update():
    d1 = {'a':{'b': {'c':'d'}}}
    d2 = {'a':{'b': {'e': 'f'}}, 'g':'h'}
    deep_update(d1, d2)
    assert d1 == {'a': {'b': {'c': 'd', 'e': 'f'}}, 'g': 'h'}

    d3 = {'a':{'b': 2}}
    with pytest.raises(ValueError):
        deep_update(d1, d3, strict=True)


