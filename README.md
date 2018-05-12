# chinforpms

Personal Fedora RPM specs. Have specs to build RPMs not existant in Fedora or
RPMFusion and existant packages updated with extra changes (these have .chinfo
release tags).

> Most packages can be found in this [COPR repository](https://copr.fedorainfracloud.org/coprs/phantomx/chinforpms), except for those not allowed.

>_Before use, remember that **YOU ARE AT YOUR OWN RISK**! Don't blame me if your
>system explodes or suffer any other bad things._

>Study the licenses carefully.

## Requirements

 * [RPM Fusion](https://rpmfusion.org)

## Differences from Fedora and RPM Fusion

 * **belle-sip, linphone, ortp** - Updated version
 * **bluecurve-icon-theme** - Extra symbolic links for cursors, more hardcoded icon sizes
 * **easytag** - Tests
 * **gnome-colors-icon-theme** - Post script and cleanup
 * **gstreamer1** - Added suffix -32/-64 to gst-plugin-scanner, so it can build
                    correct multilib plugins registry, as
                    _~/.cache/gstreamer-1.0/registry.i686.bin_ on x86_64
 * **gtk3** - Revert some features ditched in 3.10 release, some _Debian_,
              _Ubuntu_ and [_gtk3-mushrooms_](https://github.com/TomaszGasior/gtk3-mushrooms) patches
 * **keepassxc** - Post script and cosmetic fixes
 * **kernel** - _blk-mq_ enabled by default, [CPU optimizations](https://github.com/graysky2/kernel_gcc_patch) and some
                [_openSUSE_ kernel](http://kernel.opensuse.org/cgit/kernel-source) patches
                (kernel-local must be edited to modify gcc optimizations)
 * **libogg** - Tests
 * **mesa** - Tests
 * **nautilus-dropbox** - Optional nautilus support and use system binary **dropboxd**
 * **psi** - Updated
 * **quiterss** - Updated, Qt5
 * **steam** - Patch reordering, personal fixes on desktop file and launcher script
 * **VirtualBox** - Extra patches, a boot logo, no update checking, **VirtualBox-extpack-oracle**
                    and **VirtualBox-guest-additions-iso** support
 * **xboxdrv** - Tests
 * **xfwm4** - -DMONITOR_ROOT_PIXMAP
 * **xorg-x11-server** - Tests
 * **wine** - Extra patches and personal fixes

## Credits (Patches, install procedures and other files)
* [Arch](https://www.archlinux.org)
* [Debian](https://www.debian.org)
* [Fedora](https://fedoraproject.org)
* [Gentoo](https://www.gentoo.org)
* [openSUSE](https://www.opensuse.org)
* [Ubuntu](https://www.ubuntu.com)
