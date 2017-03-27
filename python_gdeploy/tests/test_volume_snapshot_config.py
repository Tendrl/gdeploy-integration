from python_gdeploy.actions import snapshot_config as vsc


class TestVolumeSnapshotConfig(object):
    def test_volume_snapshot_config(self, monkeypatch):
        volume_name = "vol1"
        hostname = "12.23.34.45"
        action = "create"
        snapname = "snap1"

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {
                    'snapshot': {
                        'action': 'create',
                        'volname': '12.23.34.45:vol1',
                        'snap_name': 'snap1'
                    }
                }
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(vsc, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(vsc, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = vsc.volume_snapshot_config(
            volume_name,
            hostname,
            action,
            snapname
        )

        assert out == "succefully created"
        assert err == ""
        assert rc == 0
