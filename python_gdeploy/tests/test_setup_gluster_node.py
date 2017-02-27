from python_gdeploy.actions import setup_gluster_node as sgn


class TestSetupGlusterNode(object):
    def test_setup_gluster_node(self, monkeypatch):
        host_list = ["12.23.34.45", "22.23.34.45"]
        glusterfs_repo = "https://download.gluster.org/gluster.repo"

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {'hosts': ['12.23.34.45', '22.23.34.45']},
                {'yum': {
                    'action': 'install',
                    'gpgcheck': 'no',
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
                {'service': {
                    'action': 'enable',
                    'service': 'glusterd'}},
                {'service': {
                    'action': 'start',
                    'service': 'glusterd'}},
                {'firewalld': {
                    'action': 'add',
                    'services': 'glusterfs',
                    'permanent': 'true',
                    'ports': [
                        '111/tcp', '2049/tcp',
                        '54321/tcp', '5900/tcp',
                        '5900-6923/tcp', '5666/tcp',
                        '16514/tcp']}}
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(sgn, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully setup"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(sgn, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = sgn.setup_gluster_node(
            host_list,
            glusterfs_repo=glusterfs_repo
        )
        assert out == "succefully setup"
        assert err == ""
        assert rc == 0
