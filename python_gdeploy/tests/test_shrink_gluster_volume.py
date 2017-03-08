from python_gdeploy.actions import shrink_gluster_volume as sgv


class TestshrinkVolume(object):
    def test_shrink_volume(self, monkeypatch):
        volume_name = "vol1"
        brick_details = [
            [
                {"12.23.34.45": "brick3"},
                {"22.23.34.45": "brick3"},
                {"32.23.34.45": "brick3"},
            ],
        ]
        replica_count = "3"
        action = "start"

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.23.34.45", "22.23.34.45", "32.23.34.45"]},
                {
                    "volume": {
                        "volname": "vol1",
                        "action": "remove-brick",
                        "bricks": [
                            "12.23.34.45:brick3", "22.23.34.45:brick3",
                            "32.23.34.45:brick3"
                        ],
                        "state": "start",
                        "ignore_volume_errors": "no",
                    }
                },
            ]
            assert recipe[1] == expected_recipe[1]
            return ""
        monkeypatch.setattr(sgv, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(sgv, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = sgv.shrink_gluster_volume(
            volume_name,
            brick_details,
            replica_count=replica_count,
            action=action
        )
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
