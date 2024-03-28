#!/usr/bin/sh

exec curl -q -H 'Snap-Device-Series: 16' https://api.snapcraft.io/v2/snaps/info/authy
