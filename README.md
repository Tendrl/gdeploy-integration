# python-gdeploy
Python modules that wrap the gdeploy (https://github.com/gluster/gdeploy) functionality to allow it to be programmatically used. Currently available functionalities are as follows:

    * setup gluster node
    * gluster cluster creation
    * gluster brick provison
    * gluster volume creation
    * volume option configuration
    * snapshot configuration
    * quota configuration
    * gluster volume expansion


Installation from source on CentOS 7:
------------------------------------
1. As a pre-requisite install and setup gdeploy:

   you can refer http://gdeploy.readthedocs.io/en/latest/installation.html to install gdeploy and for setting up gdeploy
   http://gdeploy.readthedocs.io/en/latest/howitworks.html can be used.
   
2. Installing python-gdeploy:

   Clone the python-gdeploy package and install:
       ```
       $ git clone https://github.com/Tendrl/python-gdeploy.git
       
       $ cd python-gdeploy
       
       $ python setup.py install
       ```
       
3. Configure python-gdeploy:

   Copy python-gdeploy located at etc/python-gdeploy/python-gdeploy.conf.sample to /etc/python-gdeploy/python-gdeploy.conf
       ```
       $ mkdir -p /etc/python-gdeploy
       
       $ cp etc/python-gdeploy/python-gdeploy.conf /etc/python-gdeploy/python-gdeploy.conf
       ```
      
   This configuration file has a field called glusterfs_repo, If you want to install glusterfs from any other repo than default, Please modify itaccordingly.

Usage:
------
Usage is very simple, python gdeploy can be loaded as any other python module and the gdeploy functionalities can be invoked

Example:

```
from python_gdeploy.actions import setup_gluster_node

out, err, rc = setup_gluster_node.setup_gluster_node(<host_list>)
```
This will install all glusterfs related packages on the hosts provided in the host list, start the glusterd service and configure the firewalld. Similarly other actions can also be performed.

NOTE:
-----
this package is independent of any other tendrl packages, this package can be independently installed and above mentioned actions can be run by loading the suitable modules.