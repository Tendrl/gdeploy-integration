class UnsupportedOptionError(Exception):
    def __init__(self, message):
        self.message = message


def get_hosts(host_list):
    host = {
        "hosts": host_list
    }
    return host


def get_tuned_profile(tuned_profile):
    if tuned_profile not in [
            "rhgs-sequential-io",
            "rhgs-random-io"]:
        msg = "profile %s is unsupported tuned-profile" % (tuned_profile)
        raise UnsupportedOptionError(msg)
    tp = {
        "tune-profile": tuned_profile
    }
    return tp


def get_peer(action, force=None):
    if action not in ["probe", "detach"]:
        msg = "Action %s is unsupported action for peer feature" % (action)
        raise UnsupportedOptionError(msg)

    peer = {
        "action": action,
        "ignore_peer_errors": "no"
    }

    if force:
        peer.update({"force": force})

    return {"peer": peer}


def get_yum(action, packages, repos=None,
            gpgcheck="yes", update="no", target_host=""):
    if action not in ["install", "remove"]:
        msg = "Action %s is unsupported action for yum feature" % (action)
        raise UnsupportedOptionError(msg)

    if gpgcheck not in ["yes", "no"]:
        msg = "Value {} is unsupported option for " + \
              "attribute gpgcheck in yum feature".format(gpgcheck)
        raise UnsupportedOptionError(msg)

    if update not in ["yes", "no"]:
        msg = "Value {} is unsupported option for " + \
              "attribute update in yum feature".format(update)
        raise UnsupportedOptionError(msg)

    yum = {
        "action": action,
        "packages": packages,
        "ignore_yum_errors": "no"
    }

    if action == "install":
        yum.update(
            {
                "gpgcheck": gpgcheck,
                "update": update
            }
        )
        if repos:
            yum.update(
                {"repos": repos}
            )
    section_header = "yum"
    if target_host:
        section_header += ":" + target_host
    return {section_header: yum}


def get_firewall(action, ports, services="", zone="",
                 permanent=""):
    if action not in ["add", "delete"]:
        msg = "Action %s is unsupported action for firewall feature" % (action)
        raise UnsupportedOptionError(msg)

    firewall = {
        "action": action,
        "ports": ports,
    }

    if services:
        firewall.update(
            {
                "services": services,
            }
        )
    if zone:
        firewall.update(
            {
                "zone": zone,
            }
        )
    if permanent:
        if permanent not in ["true", "false"]:
            msg = "Value {} is unsupported value for attribute permanent" + \
                  "in firewall feature".format(action)
            raise UnsupportedOptionError(msg)

        firewall.update(
            {
                "permanent": permanent,
            }
        )

    section_header = "firewalld"
    return {section_header: firewall}


def get_service(action, services, target_host=""):
    if action not in ["start", "stop", "restart",
                      "reload", "enable", "disable"]:
        msg = "Action %s is unsupported action for service feature" % (action)
        raise UnsupportedOptionError(msg)

    service = {
        "action": action,
        "service": services,
        "ignore_service_errors": "no"
    }

    section_header = "service"
    if target_host:
        section_header += ":" + target_host
    return {section_header: service}


def get_backend_setup(devices, vgs=None, pools=None, lvs=None,
                      lv_size=None, mount_points=None,
                      brick_dirs=None, target_host=""):
    backend_setup = {
        "devices": devices
    }
    if vgs:
        backend_setup.update(
            {"vgs": vgs}
        )
    if lvs:
        backend_setup.update(
            {"lvs": lvs}
        )
    if pools:
        backend_setup.update(
            {"pools": pools}
        )
    if lv_size:
        backend_setup.update(
            {"size": lv_size}
        )
    if mount_points:
        backend_setup.update(
            {"mountpoints": mount_points}
        )
    if brick_dirs:
        backend_setup.update(
            {"brick_dirs": brick_dirs}
        )
    section_header = "backend-setup"
    if target_host:
        section_header += ":" + target_host
    return {section_header: backend_setup}


def get_disktype(disk_type):
    if disk_type not in ["RAID10", "RAID6", "JBOD"]:
        msg = "disk_type %s is unsupported type for disk" % (disk_type)
        raise UnsupportedOptionError(msg)
    return {
        "disktype": disk_type
    }


def get_diskcount(disk_count):
    return {
        "diskcount": str(disk_count)
    }


def get_stripesize(stripe_size):
    return {
        "stripesize": str(stripe_size)
    }


def get_volume(volume_name, action, brick_dirs=None, transport=None,
               replica_count=None, disperse=None, disperse_count=None,
               redundancy_count=None, force="", target_host="", state="",
               option_keys=[], option_values=[]):
    if action not in ["start", "stop", "create",
                      "delete", "rebalance", "remove-brick",
                      "add-brick", "set"]:
        msg = "Action %s is unsupported action for volume feature" % (action)
        raise UnsupportedOptionError(msg)

    if action == "set":
        if not option_keys or not option_values:
            msg = "key/value attribute(s) missing. these are mandatory" + \
                  "if action is set"
            raise UnsupportedOptionError(msg)

    if action == "add-brick" or action == "remove-brick":
        if not brick_dirs:
            msg = "bricks attribute missing. it is mandatory" + \
                  "for action {}".format(action)
            raise UnsupportedOptionError(msg)

    volume = {
        "volname": volume_name,
        "action": action,
        "ignore_volume_errors": "no"
    }

    if action == "rebalance" or action == "remove-brick":
        if not state:
            msg = "state attribute missing. it is mandatory" + \
                  "for action {}".format(action)
            raise UnsupportedOptionError(msg)
        volume.update({"state": state})

    if brick_dirs:
        if action == "add-brick" or action == "remove-brick":
            volume.update({"bricks": brick_dirs})
        else:
            volume.update({"brick_dirs": brick_dirs})
    if transport:
        volume.update({"transport": transport})
    if replica_count:
        volume.update({"replica_count": str(replica_count)})
    if disperse_count:
        volume.update({"disperse_count": str(disperse_count)})
    if disperse:
        volume.update({"disperse": disperse})
    if redundancy_count:
        volume.update({"redundancy_count": str(redundancy_count)})
    if force:
        if force not in ["yes", "no"]:
            msg = "Value {} is unsupported option for " + \
                  "attribute force in volume feature".format(force)
            raise UnsupportedOptionError(msg)
        volume.update({"force": force})

    if option_keys:
        volume.update({"key": option_keys})
    if option_values:
        volume.update({"value": option_values})

    section_header = "volume"
    if target_host:
        section_header += ":" + target_host
    return {section_header: volume}


def get_snapshot(volume_name, action, snap_name, target_host=""):
    if action not in ["create", "delete", "clone"]:
        msg = "Action %s is unsupported action for snapshot feature" % (action)
        raise UnsupportedOptionError(msg)

    snapshot = {
        "action": action,
        "volname": volume_name,
        "snap_name": snap_name
    }

    section_header = "snapshot"
    if target_host:
        section_header += ":" + target_host
    return {section_header: snapshot}


def get_quota(volume_name, action, path=[], size=[],
              number=[], target_host=""):
    if action not in ["limit-usage", "limit-objects"]:
        msg = "Action %s is unsupported action for quota feature" % (action)
        raise UnsupportedOptionError(msg)

    quota = {
        "volname": volume_name,
        "action": action
    }

    if action == "limit-usage":
        if path and size:
            quota.update(
                {
                    "path": path,
                    "size": size
                }
            )
        else:
            msg = "path/size attribute(s) missing. these are mandatory" + \
                  "if action is limit-usage"
            raise UnsupportedOptionError(msg)
    elif action == "limit-objects":
        if path and number:
            quota.update(
                {
                    "path": path,
                    "number": number
                }
            )
        else:
            msg = "path/number attribute(s) missing. these are mandatory" + \
                  "if action is limit-objects"
            raise UnsupportedOptionError(msg)

    section_header = "quota"
    if target_host:
        section_header += ":" + target_host
    return {section_header: quota}
