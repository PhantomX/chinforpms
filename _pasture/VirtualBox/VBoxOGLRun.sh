#!/bin/sh

if VBoxClient --check3d; then
    export LD_LIBRARY_PATH=/usr/lib64/VBoxGuestAdditions:/usr/lib/VBoxGuestAdditions
else
    echo "Error 3D pass-through not enabled in VM settings." 1>&2
    exit 1
fi

exec "$@"
