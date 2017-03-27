from python_gdeploy.actions import install_gluster as ig


class TestInstallGluster(object):
    def test_install_gluster(self, monkeypatch):
        host_list = ["12.23.34.45", "22.23.34.45"]
        glusterfs_repo = "https://download.gluster.org/gluster.repo"

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {'hosts': ['12.23.34.45', '22.23.34.45']},
                {'yum': {
                    'action': 'install',
                    'gpgcheck': 'no',
                    'ignore_yum_errors': 'no',
                    'repos': 'https://download.gluster.org/gluster.repo',
                    'packages': [
                        'glusterfs',
                        'glusterfs-server',
                        'glusterfs-cli',
                        'glusterfs-libs',
                        'glusterfs-client-xlators',
                        'glusterfs-api',
                        'glusterfs-fuse'
                    ],
                    'update': 'no'}},
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(ig, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully setup"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(ig, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = ig.install_gluster_packages(
            host_list,
            glusterfs_repo=glusterfs_repo
        )
        assert out == "succefully setup"
        assert err == ""
        assert rc == 0
