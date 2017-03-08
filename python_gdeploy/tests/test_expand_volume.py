from python_gdeploy.actions import expand_gluster_volume as egv


class TestExpandVolume(object):
    def test_expand_volume(self, monkeypatch):
        volume_name = "vol1"
        brick_details = [
            [
                {"12.23.34.45": "brick2"},
                {"22.23.34.45": "brick2"},
                {"32.23.34.45": "brick2"},
            ],
            [
                {"12.23.34.45": "brick3"},
                {"22.23.34.45": "brick3"},
                {"32.23.34.45": "brick3"},
            ],
        ]
        replica_count = "3"
        force = False

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.23.34.45", "22.23.34.45", "32.23.34.45"]},
                {
                    "volume": {
                        "volname": "vol1",
                        "action": "add-brick",
                        "bricks": [
                            "12.23.34.45:brick2",
                            "22.23.34.45:brick2", "32.23.34.45:brick2",
                            "12.23.34.45:brick3", "22.23.34.45:brick3",
                            "32.23.34.45:brick3"
                        ],
                        "force": "no",
                        "ignore_volume_errors": "no",
                    }
                },
            ]
            assert recipe[1] == expected_recipe[1]
            return ""
        monkeypatch.setattr(egv, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(egv, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = egv.expand_volume(
            volume_name,
            brick_details,
            replica_count=replica_count,
            force=force
        )
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
