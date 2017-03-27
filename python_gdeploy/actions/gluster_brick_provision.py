from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def provision_disks(disk_dictionary, disk_type=None,
                    disk_count=None, stripe_size=None):
    """Structure of disk dictionary

    {"host_name_0": {

           "diks_name_0": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>,

                   "vg": <vg-name>,

                   "lv": <lv-name>,

                   "pv": <pv-name>,

                   "pool": <pool-name>,

           },

           "diks_name_1": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>,

                   "vg": <vg-name>,

                   "lv": <lv-name>,

                   "pv": <pv-name>,

                   "pool": <pool-name>,

           },

           "diks_name_2": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>,

                   "vg": <vg-name>,

                   "lv": <lv-name>,

                   "pv": <pv-name>,

                   "pool": <pool-name>,

           }

     },

    "host_name_2": {

           "diks_name_0": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>,

                   "vg": <vg-name>,

                   "lv": <lv-name>,

                   "pv": <pv-name>,

                   "pool": <pool-name>,

           },

           "diks_name_1": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>,

                   "vg": <vg-name>,

                   "lv": <lv-name>,

                   "pv": <pv-name>,

                   "pool": <pool-name>,

           },

           "diks_name_2": {

                   "mount_path": <actual-mountpath>,

                   "brick_path": <actual-brick-path>,

                   "vg": <vg-name>,

                   "lv": <lv-name>,

                   "pv": <pv-name>,

                   "pool": <pool-name>,

           },

     }

    }
    disk_type = [RAID10|RAID6|JBOD]
    disk_count = is nos of data disks in case of RAID device
    stripe_size = stripe size in KB in case of RAID device
    """
    recipe = []
    recipe.append(gf.get_hosts(disk_dictionary.keys()))
    for host, disks in disk_dictionary.iteritems():
        device_list = []
        mount_point_list = []
        brick_path_list = []
        vg_list = []
        pool_list = []
        lv_list = []
        pv_list = []
        for disk, detail in disks.iteritems():
            device_list.append(disk)
            mount_point_list.append(detail["mount_path"])
            brick_path_list.append(detail["brick_path"])
            lv_list.append(detail["lv"])
            pool_list.append(detail["pool"])
            vg_list.append(detail["vg"])
            pv_list.append(detail["pv"])
        recipe.append(
            gf.get_backend_setup(
                device_list,
                mount_points=mount_point_list,
                brick_dirs=brick_path_list,
                target_host=host,
                lvs=lv_list,
                pools=pool_list,
                vgs=vg_list,
                pvs=pv_list
            )
        )
    if disk_type:
        recipe.append(
            gf.get_disktype(disk_type)
        )
        if disk_type in ["RAID6", "RAID10"]:
            if not stripe_size or not disk_count:
                raise ValueError(
                    "Stripe size and disk count is mandatory" +
                    "for disk of type: %s" % (disk_type)
                )
            else:
                recipe.append(
                    gf.get_diskcount(disk_count)
                )
                recipe.append(
                    gf.get_stripesize(stripe_size)
                )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
