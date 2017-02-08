from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def volume_quota_config(volume_name, hostname, action, dir_details={}):
    """dir_details should be of following form

    [

      {"dir2": "size2"},

      {"dir1": "size1"},

      {"dir3": "size3"},

    ]
    """
    recipe = []
    host_vol = hostname + ":" + volume_name
    if dir_details:
        dir_list = []
        size_list = []
        for directory in dir_details:
            dir_list.append(directory.keys()[0])
            size_list.append(directory.values()[0])
        recipe.append(
            gf.get_quota(
                host_vol,
                action,
                path=dir_list,
                size=size_list
            )
        )
    else:
        recipe.append(
            gf.get_quota(
                host_vol,
                action
            )
        )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
