from python_gdeploy.actions import delete_volume as dv


class TestDeleteVolume(object):
    def test_delete_volume(self, monkeypatch):
        volume_name = "vol1"
        host = "12.34.45.56"
        force = False

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.34.45.56"]},
                {
                    "volume": {
                        "volname": "vol1",
                        "action": "delete",
                        "force": "no",
                        "ignore_volume_errors": "no",
                    }
                },
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(dv, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(dv, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = dv.delete_volume(
            volume_name,
            host,
            force
        )
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
