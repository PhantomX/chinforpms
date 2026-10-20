#!/bin/sh

# Adjusts the configuration options to build the variants correctly

test -n "$RHTEST" && exit 0

if [ -z "$FLAVOR" ]; then
	FLAVOR=rhel
fi

if [ "$FLAVOR" = "fedora" ]; then
	SECONDARY=rhel
else
	SECONDARY=fedora
fi

# The +1 is to remove the - at the end of the SPECPACKAGE_NAME string
specpackage_name_len=$((${#SPECPACKAGE_NAME} + 1))
for i in "${SPECPACKAGE_NAME}"*-"$FLAVOR".config; do
	# shellcheck disable=SC3057
	NEW=${SPECPACKAGE_NAME}-"$SPECRPMVERSION"-$(echo "${i:$specpackage_name_len}" | sed s/-"$FLAVOR"//)
	mv "$i" "$NEW"
done

rm -f kernel-*-"$SECONDARY".config
