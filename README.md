github-webhook-daemon
=====================

Calls a shell command when a webhook notification is received

Installation
------------

### Dependencies
Python 3

###Installing as a service

```sh
ln -s /path/to/github-webhook-daemon/github-webhook-daemon.py /usr/local/bin/
cp /path/to/github-webhook-daemon/config.json.example /etc/github-webhook-daemon.conf
```
edit `/etc/github-webhook-daemon.conf`

**Debian**:
```sh
ln -s /path/to/github-webhook-daemon/init_scripts/sysvinit/github-webhook-daemon /etc/init.d/
update-rc.d github-webhook-daemon defaults
update-rc.d github-webhook-daemon start
```
