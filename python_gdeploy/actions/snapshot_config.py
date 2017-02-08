from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def volume_snapshot_config(volume_name, hostname, action, snapname=""):
    recipe = []
    host_vol = hostname + ":" + volume_name
    recipe.append(
        gf.get_snapshot(
            host_vol,
            action,
            snapname
        )
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
