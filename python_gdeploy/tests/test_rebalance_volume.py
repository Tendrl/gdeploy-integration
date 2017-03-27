from python_gdeploy.actions import rebalance_volume as rv


class TestStartVolume(object):
    def test_start_volume(self, monkeypatch):
        volume_name = "vol1"
        host = "12.34.45.56"
        force = False
        action = "start"

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.34.45.56"]},
                {
                    "volume": {
                        "volname": "vol1",
                        "action": "rebalance",
                        "force": "no",
                        "state": "start",
                        "ignore_volume_errors": "no",
                    }
                },
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(rv, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(rv, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = rv.rebalance_volume(
            volume_name,
            action,
            host,
            force
        )
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
