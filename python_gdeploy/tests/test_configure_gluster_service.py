from python_gdeploy.actions import configure_gluster_service as cgs


class TestConfigureGlusterService(object):
    def test_configure_gluster_service(self, monkeypatch):
        host_list = ["12.23.34.45", "22.23.34.45"]

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {'hosts': ['12.23.34.45', '22.23.34.45']},
                {'service': {
                    'action': 'enable',
                    'ignore_service_errors': 'no',
                    'service': 'glusterd'}},
                {'service': {
                    'action': 'start',
                    'ignore_service_errors': 'no',
                    'service': 'glusterd'}},
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(cgs, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully setup"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(cgs, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = cgs.configure_gluster_service(
            host_list
        )
        assert out == "succefully setup"
        assert err == ""
        assert rc == 0
