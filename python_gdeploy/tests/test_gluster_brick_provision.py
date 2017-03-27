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
            },
        }

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {
                    'hosts': [
                        '12.23.34.45'
                    ]
                },
                {
                    'backend-setup:12.23.34.45': {
                        'mountpoints': ['/mnt/brick1'],
                        'brick_dirs': ['/mnt/brick1/b1'],
                        'devices': ['/dev/sdb'],
                        'pools': ['brick1_pool'],
                        'lvs': ['brick1_lv'],
                        'pvs': ['brick1_pv'],
                        'vgs': ['brick1_vg'],
                    }
                }
            ]
            print "RECIPE1"
            print recipe
            print expected_recipe
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
                        '12.23.34.45'
                    ]
                },
                {
                    'backend-setup:12.23.34.45': {
                        'mountpoints': ['/mnt/brick1'],
                        'brick_dirs': ['/mnt/brick1/b1'],
                        'devices': ['/dev/sdb'],
                        'pools': ['brick1_pool'],
                        'pvs': ['brick1_pv'],
                        'lvs': ['brick1_lv'],
                        'vgs': ['brick1_vg'],
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
            print "RECIPE1"
            print recipe
            print expected_recipe

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
