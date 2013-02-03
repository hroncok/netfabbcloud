Netfabb Cloud script
====================

This script automate the process of going to [cloud.netfabb.com](http://cloud.netfabb.com/), uploading the STL file and waiting for e-mail with the link to a web page, where you can download a repaired STL.

This script will upload your STL file and check the e-mails. If everything went OK on the netfabb side, this script will download the repaired file.

This script is experimental! Licensed under the terms of ISC license (see COPYING).

Netfabb Cloud
-------------

The netfabb Cloud Services offer a free and easy-to-use solution for anyone with access to an internet connection and a web browser.

The netfabb Cloud Services extend the repair functionalities of the free netfabb Studio Basic software in an easy to use way. 

Pre-install
-----------

You'll need some Python stuff to run this. You can get this by `easy_install` (as root):

    easy_install IMAPClient
    easy_install MultipartPostHandler

Note that `MultipartPostHandler` is available in Ubuntu 12.04+ and Debian Wheezy+ in `python-multipartposthandler` package. Other stuff should be isntalled in your distro, if not, use your distro packages system first, `easy_install` is the second option.

You might need to run this first (if installation of `IMAPClient` fails):

    easy_install -U distribute

Usage
-----

Open the script and change the config at the beginning, it should be clear enough. It is recommended to use a dedicated e-mail address just for this, as the password is stored in plaintext. Gmail works perfectly. When configured, run this command to repair a STL file:

    ./netfabb.py file.stl

File will be stored as file_fixed.stl

Warning
-------

Uploading multiple files with the same filename (or the same file) concurrently might (and probably will) cause unexpected results. Be aware of that when using the same mailbox for more people. Note that netfabb only reads ASCI letters, digits and dots, so `filename.stl` and `file_name.stl` will cause the same damage.

Xfce integration
----------------

You can integrate this script to Thunar (file manager for Xfce), by creating a [Custom action](http://thunar.xfce.org/pwiki/documentation/custom_actions). Go **Edit | Configure custom actions...** and click **Add a new custom action** icon on the right side. Select a suitable **Name**, **Description** and **Icon** and use `%f` as the only argument of `netfabbcloud` command in the **Command** field.

![Screenshot of the first tab in Add a new custom action dialog](https://raw.github.com/hroncok/netfabbcloud/master/img/thunar-ca1.png) 

On the second tab (**Appereance Conditions**), be sure to add `*.stl` and `*.STL` (separated by a semi-colon) in the **File Pattern** field and select both **Text Files** and **Other Files** to cover both ASCII and binary STLs.

![Screenshot of the second tab in Add a new custom action dialog](https://raw.github.com/hroncok/netfabbcloud/master/img/thunar-ca2.png) 

Now you can find **Netfabb Cloud** in the context menu of STL files.
