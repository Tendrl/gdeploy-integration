from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def reorder_bricks(brick_list, replica_count):
    """The brick list given as input to this function will be grouped

    host wise, this function makes sure that the list is modified

    in such a way that they are regrouped to have successive bricks

    from different nodes

    """

    new_list = []
    for i in range(len(brick_list) / replica_count):
        for j in range(replica_count):
            new_list.append(
                brick_list[j * (len(brick_list) / replica_count) + i]
            )
    return new_list


def create_volume(volume_name, brick_details, transport=[],
                  replica_count="", force=False):
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

    # In case of distributed replicated volume make sure the replica pairs
    # are placed in different nodes.
    if replica_count:
        if len(brick_list) % int(replica_count) != 0:
            out = "insufficient bricks (count: %d) for replica count" + \
                  ": %s" % (len(brick_list), replica_count)
            err = out
            rc = 1
        elif len(brick_list) / int(replica_count) > 1:
            # this means this is a distributed replicated volume
            brick_list = reorder_bricks(brick_list, int(replica_count))

    force = "yes" if force else "no"
    args = [volume_name, "create", brick_list]
    if transport:
        args.append(transport)
    if replica_count:
        args.append(replica_count)
    recipe.append(
        gf.get_volume(*args, force=force)
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
