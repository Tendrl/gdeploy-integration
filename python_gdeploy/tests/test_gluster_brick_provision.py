import pytest
from python_gdeploy.actions import gluster_brick_provision as gbp


class TestGlusterBrickProvison(object):
    def test_gluster_brick_provision(self, monkeypatch):
        disk_detail = {
            "12.23.34.45": {
                "/dev/sdb": {
                    "mount_path": "/mnt/brick1",
                    "lv": "brick1_lv",
                    "pv": "brick1_pv",
                    "vg": "brick1_vg",
                    "pool": "brick1_pool",
                    "brick_path": "/mnt/brick1/b1"
                },
                "/dev/sdc": {
                    "mount_path": "/mnt/brick2",
                    "lv": "brick2_lv",
                    "pv": "brick2_pv",
                    "vg": "brick2_vg",
                    "pool": "brick2_pool",
                    "brick_path": "/mnt/brick2/b2"
                }
            },
            "22.23.34.45": {
                "/dev/sdb": {
                    "mount_path": "/mnt/brick1",
                    "lv": "brick1_lv",
                    "pv": "brick1_pv",
                    "vg": "brick1_vg",
                    "pool": "brick1_pool",
                    "brick_path": "/mnt/brick1/b1"
                },
                "/dev/sdc": {
                    "mount_path": "/mnt/brick2",
                    "lv": "brick2_lv",
                    "pv": "brick2_pv",
                    "vg": "brick2_vg",
                    "pool": "brick2_pool",
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
                        'devices': ['/dev/sdb', '/dev/sdc'],
                        'pools': ['brick1_pool', 'brick2_pool'],
                        'lvs': ['brick1_lv', 'brick2_lv'],
                        'pvs': ['brick1_pv', 'brick2_pv'],
                        'vgs': ['brick1_vg', 'brick2_vg'],
                    }
                },
                {
                    'backend-setup:12.23.34.45': {
                        'mountpoints': ['/mnt/brick1', '/mnt/brick2'],
                        'brick_dirs': ['/mnt/brick1/b1', '/mnt/brick2/b2'],
                        'devices': ['/dev/sdb', '/dev/sdc'],
                        'pools': ['brick1_pool', 'brick2_pool'],
                        'lvs': ['brick1_lv', 'brick2_lv'],
                        'pvs': ['brick1_pv', 'brick2_pv'],
                        'vgs': ['brick1_vg', 'brick2_vg'],
                    }
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
                        'devices': ['/dev/sdb', '/dev/sdc'],
                        'pools': ['brick1_pool', 'brick2_pool'],
                        'pvs': ['brick1_pv', 'brick2_pv'],
                        'lvs': ['brick1_lv', 'brick2_lv'],
                        'vgs': ['brick1_vg', 'brick2_vg'],
                    }
                },
                {
                    'backend-setup:12.23.34.45': {
                        'mountpoints': ['/mnt/brick1', '/mnt/brick2'],
                        'brick_dirs': ['/mnt/brick1/b1', '/mnt/brick2/b2'],
                        'devices': ['/dev/sdb', '/dev/sdc'],
                        'pools': ['brick1_pool', 'brick2_pool'],
                        'pvs': ['brick1_pv', 'brick2_pv'],
                        'lvs': ['brick1_lv', 'brick2_lv'],
                        'vgs': ['brick1_vg', 'brick2_vg'],
                    }
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
