from python_gdeploy.actions import set_volume_options as svo


class TestSetupVolumeOptions(object):
    def test_setup_volume_options(self, monkeypatch):
        hostname = "12.23.34.45"
        volume_name = "vol1"
        options = [
            {"option1": "value1"},
            {"option2": "value2"},
            {"option3": "value3"},
        ]

        def mock_cook_gdeploy_config(recipe):
            assert recipe == [
                {
                    "volume": {
                        "action": "set",
                        "volname": "12.23.34.45:vol1",
                        "key": ["option1", "option2", "option3"],
                        "value": ["value1", "value2", "value3"],
                    }
                }
            ]
            return ""
        monkeypatch.setattr(svo, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully set"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(svo, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = svo.set_volume_options(
            volume_name,
            hostname,
            options
        )
        assert out == "succefully set"
        assert err == ""
        assert rc == 0
