from python_gdeploy.actions import remove_host as rh


class TestRemoveHost(object):
    def test_remove_host(self, monkeypatch):
        host_list = ["12.34.45.56", "22.34.45.56"]
        force = False

        def mock_cook_gdeploy_config(recipe):
            expected_recipe = [
                {"hosts": ["12.34.45.56", "22.34.45.56"]},
                {
                    "peer": {
                        "action": "detach",
                        "force": "no",
                        "ignore_peer_errors": "no",
                    }
                },
            ]
            assert recipe == expected_recipe
            return ""
        monkeypatch.setattr(rh, 'cook_gdeploy_config',
                            mock_cook_gdeploy_config)

        def mock_invoke_gdeploy(config):
            out = "succefully created"
            err = ""
            rc = 0
            return out, err, rc
        monkeypatch.setattr(rh, 'invoke_gdeploy',
                            mock_invoke_gdeploy)

        out, err, rc = rh.remove_host(
            host_list,
            force
        )
        assert out == "succefully created"
        assert err == ""
        assert rc == 0
