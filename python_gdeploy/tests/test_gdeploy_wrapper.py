import pytest
from python_gdeploy.wrapper import gdeploy_wrapper as gw
import subprocess
import uuid

expected_config = """[hosts]
12.23.34.45
23.34.45.56
34.45.56.67

[backend-setup]
devices=vda,vdb

"""

class process(object):
    def __init__(self):
        self.returncode = 0

    def communicate(self):
        out = "dummy output string"
        err = "dummy err string"
        return out, err


class TestGdeployWrapper(object):
    def test_add_section(self):
        section = "volume"
        header = gw.add_section(section)
        expected_header = "[volume]\n"

        assert header == expected_header

    def test_cook_gdeploy_config(self):
        recipe1 = [
            {"hosts": ["12.23.34.45","23.34.45.56","34.45.56.67"]},
            {
                "backend-setup": {
                    "devices" : ["vda","vdb"]
                }
            }
        ]
        config = gw.cook_gdeploy_config(recipe1)
        assert config == expected_config

    def test_invoke_gdeploy(self, monkeypatch):
        monkeypatch.setattr(gw, "GDEPLOY_CONFIG_PATH", "/tmp/config_")

        def mock_uuid():
            return "87edcddd-f61b-4699-951f-187e6e022dc9"
        monkeypatch.setattr(uuid, 'uuid4', mock_uuid)

        def mock_subprocess_popen(args=None, stdout=None, stderr=None):
            assert args == [
                "gdeploy",
                "-c",
                "/tmp/config_87edcddd-f61b-4699-951f-187e6e022dc9.conf"
            ]
            assert stdout == subprocess.PIPE
            assert stderr == subprocess.PIPE
            return process()
        monkeypatch.setattr(subprocess, "Popen", mock_subprocess_popen)
        
        out, err, rc = gw.invoke_gdeploy("")
        assert out == "dummy output string"
        assert err == "dummy err string"
        assert rc == 0
