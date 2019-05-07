#!/bin/bash
#
# This script takes the merged config files and processes them through oldconfig
# and listnewconfig


die()
{
	echo "$1"
	exit 1
}

# stupid function to find top of tree to do kernel make configs
switch_to_toplevel()
{
	path="$(pwd)"
	while test "$path" != "/"
	do
		test -e $path/MAINTAINERS && \
		test -d $path/drivers && \
		break

		path="$(dirname $path)"
	done

	test "$path" != "/" || die "Can't find toplevel"
	echo "$path"
}

checkoptions()
{
	/usr/bin/awk '

		/is not set/ {
			split ($0, a, "#");
			split(a[2], b);
			if (NR==FNR) {
				configs[b[1]]="is not set";
			} else {
				if (configs[b[1]] != "" && configs[b[1]] != "is not set")
					 print "Found # "b[1] " is not set, after generation, had " b[1] " " configs[b[1]] " in Source tree";
			}
		}

		/=/     {
			split ($0, a, "=");
			if (NR==FNR) {
				configs[a[1]]=a[2];
			} else {
				if (configs[a[1]] != "" && configs[a[1]] != a[2])
					 print "Found "a[1]"="configs[a[1]]" after generation, had " a[1]"="a[2]" in Source tree";
			}
		}
	' $1 $2 > .mismatches

	if test -s .mismatches
	then
		echo "Error: Mismatches found in configuration files"
		cat .mismatches
		exit 1
	fi
}

function process_configs()
{
	# assume we are in $source_tree/configs, need to get to top level
	pushd $(switch_to_toplevel)

	for cfg in $SCRIPT_DIR/${PACKAGE_NAME}${KVERREL}${SUBARCH}*.config
	do
		arch=$(head -1 $cfg | cut -b 3-)
		cfgtmp="${cfg}.tmp"
		cfgorig="${cfg}.orig"
		cat $cfg > $cfgorig

		echo -n "Processing $cfg ... "

		# an empty grep is good but leaves a return value, so use # 'true' to bypass
		make ARCH=$arch KCONFIG_CONFIG=$cfg listnewconfig | grep -E 'CONFIG_' > .newoptions || true
		if test -n "$NEWOPTIONS" && test -s .newoptions
		then
			echo "Found unset config items, please set them to an appropriate value"
			cat .newoptions
			rm .newoptions
			exit 1
		fi
		rm .newoptions

		make ARCH=$arch KCONFIG_CONFIG=$cfg olddefconfig > /dev/null || exit 1
		echo "# $arch" > ${cfgtmp}
		cat "${cfg}" >> ${cfgtmp}
		if test -n "$CHECKOPTIONS"
		then
			checkoptions $cfgtmp $cfgorig
		fi
		mv ${cfgtmp} ${cfg}
		rm ${cfgorig}
		echo "done"
	done
	rm "$SCRIPT_DIR"/*.config.old
	popd > /dev/null

	echo "Processed config files are in $SCRIPT_DIR"
}

NEWOPTIONS=""
CHECKOPTIONS=""

while [[ $# -gt 0 ]]
do
	key="$1"
	case $key in
		-n)
			NEWOPTIONS="x"
			;;
		-c)
			CHECKOPTIONS="x"
			;;
		*)
			break;;
	esac
	shift
done

PACKAGE_NAME="${1:-kernel}" # defines the package name used
KVERREL="$(test -n "$2" && echo "-$2" || echo "")"
SUBARCH="$(test -n "$3" && echo "-$3" || echo "")"
SCRIPT="$(readlink -f $0)"
OUTPUT_DIR="$PWD"
SCRIPT_DIR="$(dirname $SCRIPT)"

# to handle this script being a symlink
cd $SCRIPT_DIR

process_configs
