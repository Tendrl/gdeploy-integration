import os
import subprocess
import uuid

GDEPLOY_CONFIG_PATH = "/var/run/python_gdeploy/config_"


def add_section(section):
    return "[" + section + "]\n"


def cook_gdeploy_config(recipe):
    config_str = ""
    for el in recipe:
        k = el.keys()[0]
        v = el.values()[0]
        config_str += add_section(k)
        if type(v) == list:
            for el in v:
                config_str += el + "\n"
        elif type(v) == dict:
            for var, val in v.iteritems():
                if val is None:
                    line = val
                    continue
                line = var + "=" + (
                    str(val) if type(val) != list else ",".join(val))
                config_str += line + "\n"
        config_str += "\n"

    return config_str


def invoke_gdeploy(config):
    conf_file = GDEPLOY_CONFIG_PATH + str(uuid.uuid4()) + ".conf"
    cmd = ["gdeploy", "-c", conf_file]
    try:
        with open(conf_file, 'w') as f:
            f.write(config)
        process = subprocess.Popen(
            args=cmd,
            close_fds=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = process.communicate()
        rc = process.returncode
    except Exception as e:
        rc = -1
        out = ""
        err = "Gdeploy command invocation failed. Error: %s" % str(e)
    finally:
        if os.path.isfile(conf_file):
            os.remove(conf_file)
    return out, err, rc
