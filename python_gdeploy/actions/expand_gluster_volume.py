from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def expand_volume(volume_name, brick_details, replica_count="",
                  force=False):
    """Brick details should be of following form

    [

      {"hostname2": ["brick1","brick2"]},

      {"hostname3": ["brick1","brick2"]},

      {"hostname1": ["brick1","brick2"]},

    ]
    """
    recipe = []
    brick_list = []
    host_list = []
    for host in brick_details:
        host_list.append(host.keys()[0])
        for brick in host.values()[0]:
            brick_list.append(host.keys()[0] + ":" + brick)
    recipe.append(gf.get_hosts(host_list))
    force = "yes" if force else "no"
    recipe.append(
        gf.get_volume(
            volume_name,
            "add-brick",
            brick_dirs=brick_list,
            replica_count=replica_count,
            force=force
        )
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
