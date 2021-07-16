import pytest


def inputs(num):
    return num + 411


def test_para_testar_os_dados_para_registro():
    assert inputs(41) == 452


def test_soma_411_palavra():
    with pytest.raises(TypeError):
        inputs("mateus")
