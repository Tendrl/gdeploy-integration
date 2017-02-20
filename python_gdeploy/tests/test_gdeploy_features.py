import pytest
from python_gdeploy.wrapper import gdeploy_features as gf


class TestGdeployFeatures(object):
    def test_get_hosts(self):
        host_list = ["12.34.45.56","23.56.78.43","45,67,43,12"] 
        host = gf.get_hosts(host_list)
        expected_host_dict = {
            "hosts": ["12.34.45.56","23.56.78.43","45,67,43,12"]
        }
        assert host == expected_host_dict

    def test_get_peer(self):
        action = "probe"
        peer = gf.get_peer(action)
        expected_peer_dict = {
            "peer": {
                "action": "probe"
            }
        }
        assert peer == expected_peer_dict
        
        action = "invalid_option"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_peer,
            action
        )

    def test_get_yum(self):
        action = "install"
        packages = ["glusterfs", "glusterfs-cli", "glusterfs-api"]
        repos = ["https://asda.asds.asd/dsfsd/sdfsdf.repo"]
        gpgcheck = "yes"
        update = "yes"
        target_host = "12.34.45.56"

        yum = gf.get_yum(
            action,
            packages,
            repos,
            gpgcheck,
            update,
            target_host
        )
    
        expected_yum = {
            "yum:12.34.45.56" : {
                "action": "install",
                "packages": ["glusterfs", "glusterfs-cli", "glusterfs-api"],
                "gpgcheck": "yes",
                "update": "yes",
                "repos": ["https://asda.asds.asd/dsfsd/sdfsdf.repo"]
            }
        }
        assert yum == expected_yum

        action = "invalid_action"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_yum,
            action,
            packages
        )

        gpgcheck = "invalid_gpgcheck_value"
        action = "install"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_yum,
            action,
            packages,
            gpgcheck=gpgcheck
        )

        update = "invalid_update_value"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_yum,
            action,
            packages,
            update=update
        )

    def test_get_firewall(self):
        action = "add"
        ports=["12","45","456"]
        services=["glusterd","collectd"]
        zone = "public"
        permanent = "true"

        firewall = gf.get_firewall(
            action,
            ports,
            services,
            zone,
            permanent
        )
        expected_firewall = {
            "firewalld" : {
                "action": "add",
                "ports": ["12","45","456"],
                "services": ["glusterd","collectd"],
                "zone": "public",
                "permanent": "true"
            }
        }
        assert firewall == expected_firewall

        action = "unsupported_action"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_firewall,
            action,
            ports,
            services
        )

        action = "add"
        permanent = "unsupported_value"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_firewall,
            action,
            ports,
            services,
            permanent=permanent
        )

    def test_get_service(self):
        action = "start"
        services = ["glusterd", "collectd"]
        target_host = "12.34.45.56"

        service = gf.get_service(
            action,
            services,
            target_host
        )
    
        expected_service = {
            "service:12.34.45.56" : {
                "action": "start",
                "service": ["glusterd", "collectd"]
            }
        }
        assert service == expected_service

        action = "invalid_action"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_service,
            action,
            services
        )

    def test_get_backend_setup(self):
        devices = ["/dev/sda", "/dev/sdb"]
        vgs = ["vg1","vg2","vg3"]
        pools = ["pool1","pool2","pool3"]
        lvs = ["lv1","lv2","lv3"]
        mountpoints = ["/mnt/data1","/mnt/data2","/mnt/data3"]
        brick_dirs = ["/mnt/data1/1","/mnt/data2/2","/mnt/data3/2"]
        target_host = "12.34.45.56"
        lv_size="5MB"

        backend_setup = gf.get_backend_setup(
            devices,
            vgs,
            pools,
            lvs,
            lv_size,
            mountpoints,
            brick_dirs,
            target_host
        )
        
        expected_backend_setup = {
            "backend-setup:12.34.45.56": {
                "devices": ["/dev/sda", "/dev/sdb"],
                "vgs": ["vg1","vg2","vg3"],
                "lvs": ["lv1","lv2","lv3"],
                "pools": ["pool1","pool2","pool3"],
                "size": "5MB",
                "mountpoints": ["/mnt/data1","/mnt/data2","/mnt/data3"],
                "brick_dirs": ["/mnt/data1/1","/mnt/data2/2","/mnt/data3/2"]
            }
        }

        assert backend_setup == expected_backend_setup

    def test_get_snapshot(self):
        vol_name = "vol1"
        action = "create"
        snap_name = "snap1"
        target_host = "12.23.34.45"

        snapshot = gf.get_snapshot(
            vol_name,
            action,
            snap_name,
            target_host
        )

        expected_snapshot = {
            "snapshot:12.23.34.45" : {
                "action": "create",
                "volname": "vol1",
                "snap_name": "snap1"
            }
        }
        
        assert snapshot == expected_snapshot

        action = "unsupported_action"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_snapshot,
            vol_name,
            action,
            snap_name
        )

    def test_get_quota(self):
        vol_name = "vol1"
        action = "limit-objects"
        path = "/mnt/brick1/dir1"
        number = "1000"
        target_host = "12.34.45.56"

        quota = gf.get_quota(
            vol_name,
            action,
            path=path,
            number=number,
            target_host=target_host
        )

        expected_quota = {
            "quota:12.34.45.56" : {
                "action": "limit-objects",
                "volname": "vol1",
                "path": "/mnt/brick1/dir1",
                "number": "1000"
            }
        }
        
        assert quota == expected_quota

        action = "limit-usage"
        size="5GB"
        quota = gf.get_quota(
            vol_name,
            action,
            path,
            size=size,
            target_host=target_host
        )

        expected_quota = {
            "quota:12.34.45.56" : {
                "action": "limit-usage",
                "volname": "vol1",
                "path": "/mnt/brick1/dir1",
                "size": "5GB"
            }
        }
        
        assert quota == expected_quota

        action = "unsupported_action"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_quota,
            vol_name,
            action
        )

        action = "limit-usage"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_quota,
            vol_name,
            action
        )

        action = "limit-objects"
        pytest.raises(
            gf.UnsupportedOptionError,
            gf.get_quota,
            vol_name,
            action
        )
