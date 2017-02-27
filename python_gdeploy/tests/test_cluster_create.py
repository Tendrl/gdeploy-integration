from python_gdeploy.actions import create_cluster as cc


class TestCreateCluster(object):
    def test_create_cluster(self, monkeypatch):
        host_list = ["12.23.34.45", "22.23.34.45"]

        def mock_cook_gdeploy_config(recipe):
            assert recipe == [
                {"hosts": ["12.23.34.45", "22.23.34.45"]},
                {"peer": {"action": "probe", "ignore_peer_errors": "no"}}
            ]
            return ""
        monkeypatch.setattr(cc, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(cc, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = cc.create_cluster(host_list)
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
