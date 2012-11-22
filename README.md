Netfabb Cloud script
====================

This script automate the process of going to [cloud.netfabb.com](http://cloud.netfabb.com/), uploading the STL file and wait for e-mail with the link to a web page, where you can download a repaired STL.

This script will upload your STL file and check the e-mails. It everything went OK on the netfabb side, this script will download the repaired file.

This script is experimental! Licensed under the terms of ISC license (see COPYING).

Netfabb Cloud
-------------

The netfabb Cloud Services offer a free and easy-to-use solution for anyone with access to an internet connection and a web browser.

The netfabb Cloud Services extend the repair functionalities of the free netfabb Studio Basic software in an easy to use way. 

Usage
-----

Open the script and change the config at the beginning, it should be clear enough. It is recommended to use a dedicated e-mail address just for this, as the password is stored in plaintext. Gmail works perfectly. When configured, run this command to repair a STL file:

    ./netfabb.py file.stl

File will be stored as file_fixed.stl

Warning
-------

Uploading multiple files with the same filename (or the same file) concurrently might (and probably will) cause unexpected results. Be aware of that when using the same mailbox for more people. Note that netfabb only reads ASCI letters, digits and dots, so `filename.stl` and `file_name.stl` will cause the same damage.
