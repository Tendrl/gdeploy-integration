from python_gdeploy.actions import stop_volume as sv


class TestStopVolume(object):
    def test_stop_volume(self, monkeypatch):
        volume_name = "vol1"
        host = "12.34.45.56"
        force = False

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.34.45.56"]},
                {
                    "volume": {
                        "volname": "vol1",
                        "action": "stop",
                        "force": "no",
                        "ignore_volume_errors": "no",
                    }
                },
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(sv, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(sv, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = sv.stop_volume(
            volume_name,
            host,
            force
        )
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
