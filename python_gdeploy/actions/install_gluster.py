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


def get_glusterfs_repo():
    config = ConfigParser.SafeConfigParser()
    config.read('/etc/python-gdeploy/python-gdeploy.conf')
    return config.get("python-gdeploy", "glusterfs_repo")


def install_gluster_packages(host_list,
                             glusterfs_packages=None,
                             glusterfs_repo=None,
                             gpgcheck=None):
    recipe = []

    recipe.append(gf.get_hosts(host_list))

    recipe.append(
        gf.get_yum(
            "install",
            glusterfs_packages if glusterfs_packages else GLUSTERFS_PACKAGES,
            glusterfs_repo if glusterfs_repo else get_glusterfs_repo(),
            gpgcheck if gpgcheck else "no"
        )
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
