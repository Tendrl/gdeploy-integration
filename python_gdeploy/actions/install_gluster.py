import ConfigParser

from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


GLUSTERFS_PACKAGES = [
    "glusterfs",
    "glusterfs-server",
    "glusterfs-cli",
    "glusterfs-libs",
    "glusterfs-client-xlators",
    "glusterfs-api",
    "glusterfs-fuse"
]


def install_gluster_packages(host_list,
                             glusterfs_packages=None,
                             glusterfs_repo=None,
                             gpgcheck=None):
    """sample host list:

    ["12.34.45.65","34.23.67.34", "12.76.77.88"]

    """

    recipe = []

    recipe.append(gf.get_hosts(host_list))

    recipe.append(
        gf.get_yum(
            "install",
            glusterfs_packages if glusterfs_packages else GLUSTERFS_PACKAGES,
            glusterfs_repo,
            gpgcheck if gpgcheck else "no"
        )
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
