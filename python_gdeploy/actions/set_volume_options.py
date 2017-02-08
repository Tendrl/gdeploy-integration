from python_gdeploy.wrapper import gdeploy_features as gf
from python_gdeploy.wrapper.gdeploy_wrapper import cook_gdeploy_config
from python_gdeploy.wrapper.gdeploy_wrapper import invoke_gdeploy


def set_volume_options(volume_name, hostname, options):
    """options should be of following form

    [

      {"option2": "Value2"},

      {"option3": "Value3"},

      {"option1": "Value1"},

    ]
    """
    recipe = []
    option_key_list = []
    option_value_list = []
    for option in options:
        option_key_list.append(option.keys()[0])
        option_value_list.append(option.values()[0])
    host_vol = hostname + ":" + volume_name
    recipe.append(
        gf.get_volume(
            host_vol,
            "set",
            option_keys=option_key_list,
            option_values=option_value_list
        )
    )

    config_str = cook_gdeploy_config(recipe)

    out, err, rc = invoke_gdeploy(config_str)

    return out, err, rc
