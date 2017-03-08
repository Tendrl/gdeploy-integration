import pytest
from python_gdeploy.actions import gluster_brick_provision as gbp


class TestGlusterBrickProvison(object):
    def test_gluster_brick_provision(self, monkeypatch):
        disk_detail = {
            "12.23.34.45": {
                "/dev/sdb": {
                    "mount_path": "/mnt/brick1",
                    "brick_path": "/mnt/brick1/b1"
                },
                "/dev/sdc": {
                    "mount_path": "/mnt/brick2",
                    "brick_path": "/mnt/brick2/b2"
                }
            },
            "22.23.34.45": {
                "/dev/sdb": {
                    "mount_path": "/mnt/brick1",
                    "brick_path": "/mnt/brick1/b1"
                },
                "/dev/sdc": {
                    "mount_path": "/mnt/brick2",
                    "brick_path": "/mnt/brick2/b2"
                }
            },

        }

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {
                    'hosts': [
                        '22.23.34.45',
                        '12.23.34.45'
                    ]
                },
                {
                    'backend-setup:22.23.34.45': {
                        'mountpoints': ['/mnt/brick1', '/mnt/brick2'],
                        'brick_dirs': ['/mnt/brick1/b1', '/mnt/brick2/b2'],
                        'devices': ['/dev/sdb', '/dev/sdc']
                    }
                },
                {
                    'backend-setup:12.23.34.45': {
                        'mountpoints': ['/mnt/brick1', '/mnt/brick2'],
                        'brick_dirs': ['/mnt/brick1/b1', '/mnt/brick2/b2'],
                        'devices': ['/dev/sdb', '/dev/sdc']}
                }
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(gbp, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully provisioned"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(gbp, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = gbp.provision_disks(disk_detail)
        assert out == "succefully provisioned"
        assert err == ""
        assert rc == 0

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {
                    'hosts': [
                        '22.23.34.45',
                        '12.23.34.45'
                    ]
                },
                {
                    'backend-setup:22.23.34.45': {
                        'mountpoints': ['/mnt/brick1', '/mnt/brick2'],
                        'brick_dirs': ['/mnt/brick1/b1', '/mnt/brick2/b2'],
                        'devices': ['/dev/sdb', '/dev/sdc']
                    }
                },
                {
                    'backend-setup:12.23.34.45': {
                        'mountpoints': ['/mnt/brick1', '/mnt/brick2'],
                        'brick_dirs': ['/mnt/brick1/b1', '/mnt/brick2/b2'],
                        'devices': ['/dev/sdb', '/dev/sdc']}
                },
                {
                    'disktype': "RAID10"
                },
                {
                    'diskcount': "8"
                },
                {
                    'stripesize': "256"
                }
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(gbp, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        out, err, rc = gbp.provision_disks(disk_detail, "RAID10",
                                          "8", "256")
        assert out == "succefully provisioned"
        assert err == ""
        assert rc == 0

        disk_type = "RAID10"
        pytest.raises(
            ValueError,
            gbp.provision_disks,
            disk_detail,
            disk_type
        )
