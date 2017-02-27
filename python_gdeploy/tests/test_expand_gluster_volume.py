from python_gdeploy.actions import expand_gluster_volume as egv


class TestExpandVolume(object):
    def test_create_volume(self, monkeypatch):
        volume_name = "vol1"
        brick_details = [
            {"12.23.34.45": ["brick1", "brick2"]}
        ]
        replica_count = "2"
        force = False

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.23.34.45"]},
                {
                    "volume": {
                        "volname": "vol1",
                        "action": "add-brick",
                        "bricks": [
                            "12.23.34.45:brick1", "12.23.34.45:brick2"
                        ],
                        "replica_count": "2",
                        "force": "no"
                    }
                }
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(egv, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully expanded"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(egv, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = egv.expand_volume(
            volume_name,
            brick_details,
            replica_count,
            force
        )
        assert out == "succefully expanded"
        assert err == ""
        assert rc == 0
