from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def provison_disks(disk_dictionary):
    """Structure of disk dictionary

    {"host_name_0": {

           "diks_name_0": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>

           },

           "diks_name_1": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>

           },

           "diks_name_2": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>

           }

     },

    "host_name_2": {

           "diks_name_0": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>

           },

           "diks_name_1": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>

           },

           "diks_name_2": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>

           },

     }

    }
    """
    recipe = []
    recipe.append(gf.get_hosts(disk_dictionary.keys()))
    for host, disks in disk_dictionary.iteritems():
        device_list = []
        mount_point_list = []
        brick_path_list = []
        for disk, detail in disks.iteritems():
            device_list.append(disk)
            mount_point_list.append(detail["mount_path"])
            brick_path_list.append(detail["brick_path"])
        recipe.append(
            gf.get_backend_setup(
                device_list,
                mount_points=mount_point_list,
                brick_dirs=brick_path_list,
                target_host=host
            )
        )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
