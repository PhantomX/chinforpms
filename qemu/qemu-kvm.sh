#!/bin/sh

# Libvirt introspects the binary using -M none. In that case, don't try
# to init KVM, which will fail and be noisy if the host has kvm disabled
opts="-machine accel=kvm"
if echo "$@" | grep -q " -M none "; then
    opts=
fi

exec /usr/bin/qemu-system-x86_64 $opts "$@"
