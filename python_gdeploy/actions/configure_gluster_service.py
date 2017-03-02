from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def configure_gluster_service(host_list):
    """sample host list:

    ["12.34.45.65","34.23.67.34", "12.76.77.88"]

    """

    recipe = []

    recipe.append(gf.get_hosts(host_list))

    recipe.append(
        gf.get_service(
            "enable",
            "glusterd"
        )
    )

    recipe.append(
        gf.get_service(
            "start",
            "glusterd"
        )
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
