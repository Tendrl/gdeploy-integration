from python_gdeploy.actions import create_gluster_volume as cgv


class TestCreateVolume(object):
    def test_create_volume(self, monkeypatch):
        volume_name = "vol1"
        brick_details = [
            {"12.23.34.45": ["brick1", "brick2"]},
            {"22.23.34.45": ["brick3", "brick4"]},
            {"32.23.34.45": ["brick5", "brick6"]},
        ]
        transport = "rdma"
        replica_count = "2"
        force = False

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.23.34.45", "22.23.34.45", "32.23.34.45"]},
                {
                    "volume": {
                        "volname": "vol1",
                        "action": "create",
                        "brick_dirs": [
                            "12.23.34.45:brick1", "12.23.34.45:brick2",
                            "22.23.34.45:brick3", "22.23.34.45:brick4",
                            "32.23.34.45:brick5", "32.23.34.45:brick6"
                        ],
                        "transport": "rdma",
                        "replica_count": "2",
                        "force": "no",
                        "ignore_volume_errors": "no",
                    }
                }
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(cgv, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(cgv, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = cgv.create_volume(
            volume_name,
            brick_details,
            transport,
            replica_count,
            force
        )
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
