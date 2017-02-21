import pytest
from python_gdeploy.actions import volume_quota_config as vqc


class TestVolumeSnapshotConfig(object):
    def test_volume_snapshot_config(self, monkeypatch):
        volume_name = "vol1"
        hostname = "12.23.34.45"
        action = "limit-usage"
        dir_details = [
            {"dir1": "5MB"},
            {"dir2": "6MB"},
            {"dir3": "7MB"}
        ]
        
        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {'quota': {
                    'action': 'limit-usage',
                    'volname': '12.23.34.45:vol1',
                    'size': ['5MB', '6MB', '7MB'],
                    'path': ['dir1', 'dir2', 'dir3']
                }}
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(vqc, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(vqc, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = vqc.volume_quota_config(
            volume_name,
            hostname,
            action,
            dir_details
        )

        assert out == "succefully created"
        assert err == ""
        assert rc == 0
