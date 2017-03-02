from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def configure_gluster_firewall(host_list):
    """sample host list:

    ["12.34.45.65","34.23.67.34", "12.76.77.88"]

    """

    recipe = []

    recipe.append(gf.get_hosts(host_list))

    glusterfs_ports = [
        "111/tcp",
        "2049/tcp",
        "54321/tcp",
        "5900/tcp",
        "5900-6923/tcp",
        "5666/tcp",
        "16514/tcp"
    ]

    recipe.append(
        gf.get_firewall(
            "add",
            glusterfs_ports,
            "glusterfs",
            permanent="true"
        )
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
