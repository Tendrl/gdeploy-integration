from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def start_volume(volume_name, host=None, force=None):
    recipe = []
    if host:
        host_list = [host]
        recipe.append(gf.get_hosts(host_list))

    force = "yes" if force else "no"

    recipe.append(
        gf.get_volume(volume_name, action="start", force=force)
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
