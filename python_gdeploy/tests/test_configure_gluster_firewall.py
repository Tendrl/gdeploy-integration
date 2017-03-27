from python_gdeploy.actions import configure_gluster_firewall as cgf


class TestConfigureGlusterFirewall(object):
    def test_configure_gluster_firewall(self, monkeypatch):
        host_list = ["12.23.34.45", "22.23.34.45"]

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {'hosts': ['12.23.34.45', '22.23.34.45']},
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
        monkeypatch.setattr(cgf, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully setup"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(cgf, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = cgf.configure_gluster_firewall(
            host_list
        )
        assert out == "succefully setup"
        assert err == ""
        assert rc == 0
