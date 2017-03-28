pirc_auto.py: controls sensors and object avoidance. It should run in the background.
pirc_manual.py: called from PHP, runs only when needed by user intervention.

In order to have the required permission:

- add the following to the sudoers (sudo visudo):
www-data ALL = NOPASSWD:  /var/www/html/pirc_nofile/piRC_manual.py, /usr/bin/python3

You may be able to speed up launching the python script by compiling it first:

python3 -m compileall ./

In this case, you need to change the proper line in the index.php file.