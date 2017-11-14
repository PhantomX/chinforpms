#!/bin/bash
#
# This script merges together the hierarchy of CONFIG_* files under generic
# and debug to form the necessary $PACKAGE_NAME<version>-<arch>-<variant>.config
# files for building RHEL kernels, based on the contents of a control file

PACKAGE_NAME="${1:-kernel}" # defines the package name used
KVERREL="${2:-}"
SUBARCH="${3:-}" # defines a specific arch for use with rh-configs-arch-prep target
SCRIPT="$(readlink -f $0)"
OUTPUT_DIR="$PWD"
SCRIPT_DIR="$(dirname $SCRIPT)"

# to handle this script being a symlink
cd $SCRIPT_DIR

set errexit
set nounset

control_file="config_generation"

cleanup()
{
	rm -f config-*
}

die()
{
	echo "$1"
	cleanup
	exit 1
}

function combine_config_layer()
{
	dir=$1
	file="config-$(echo $dir | sed -e 's|/|-|g')"

	if [ $(ls $dir/ | grep -c "^CONFIG_") -eq 0 ]; then
		touch $file
		return
	fi

	cat $dir/CONFIG_* > $file
}

function merge_configs()
{
	archvar=$1
	arch=$(echo "$archvar" | cut -f1 -d"-")
	configs=$2
	name=$OUTPUT_DIR/$PACKAGE_NAME-$archvar.config
	echo -n "Building $name ... "
	touch config-merging config-merged

	# apply base first
	for config in $(echo $configs | sed -e 's/:/ /g')
	do
		perl merge.pl config-base-$config config-merging > config-merged
		if [ ! $? -eq 0 ]; then
			die "Failed to merge base"
		fi
		mv config-merged config-merging
	done
	for config in $(echo $configs | sed -e 's/:/ /g')
	do
		# not all override files exist
		test -e config-$config || continue

		perl merge.pl config-$config config-merging > config-merged
		if [ ! $? -eq 0 ]; then
			die "Failed to merge configs"
		fi
		mv config-merged config-merging
	done
	if [ "x$arch" == "xaarch64" ]; then
		echo "# arm64" > $name
	elif [ "x$arch" == "xppc64" ]; then
		echo "# powerpc" > $name
	elif [ "x$arch" == "xppc64le" ]; then
		echo "# powerpc" > $name
	elif [ "x$arch" == "xs390x" ]; then
		echo "# s390" > $name
	elif [ "x$arch" == "xarmv7hl" ]; then
		echo "# arm" > $name
	elif [ "x$arch" == "xi686" ]; then
		echo "# i386" > $name
	else
		echo "# $arch" > $name
	fi
	sort config-merging >> $name
	rm -f config-merged config-merging
	echo "done"
}

glist=$(find base-generic -type d)
dlist=$(find base-debug -type d)
gllist=$(test -d generic && find generic -type d)
dllist=$(test -d debug && find debug -type d)

for d in $glist $dlist $gllist $dllist
do
	combine_config_layer $d
done

while read line
do
	if [ $(echo "$line" | grep -c "^#") -ne 0 ]; then
		continue
	elif [ $(echo "$line" | grep -c "^$") -ne 0 ]; then
		continue
	else
		arch=$(echo "$line" | cut -f1 -d"=")
		configs=$(echo "$line" | cut -f2 -d"=")

		if [ -n "$SUBARCH" -a "$SUBARCH" != "$arch" ]; then
			continue
		fi

		merge_configs $arch $configs
	fi
done < $control_file

# A passed in kernel version implies copy to final location
# otherwise defer to another script
if test -n "$KVERREL"
then
	for i in kernel-*.config
	do
		NEW="$(echo $i | sed "s/$PACKAGE_NAME-$SUBARCH/$PACKAGE_NAME-$KVERREL-$SUBARCH/")"
		mv $i $NEW
	done
fi

cleanup
