# chinforpms

Personal Fedora RPM specs. Have specs to build RPMs not existant in Fedora or
RPMFusion and existant packages updated with extra changes (these have .chinfo
release tags).

>_Before use, remember that **YOU ARE AT YOUR OWN RISK**! Don't blame me if your
>system explodes or suffer any other bad things._

>Study the licenses carefully.

## Requirements

 * [RPM Fusion](https://rpmfusion.org)

## Differences from Fedora and RPM Fusion

 * **bluecurve-icon-theme** - Extra symbolic links for cursors, more hardcoded icon sizes
 * **gnome-colors-icon-theme** - Post script and cleanup
 * **gstreamer1** - Change libexecdir on ix86 to libdir (/usr/lib), so gst-plugin-scanner 
                    can build correct multilib plugins registry,
                    _~/.cache/gstreamer-1.0/registry.i686.bin_
 * **gtk3** - Revert some features ditched in 3.10 release, some _Debian_ and
              _Ubuntu_ patches
 * **keepassxc** - Post script and cosmetic fixes
 * **kernel** - [BFQ](http://algo.ing.unimo.it/people/paolo/disk_sched), [CPU optimizations](https://github.com/graysky2/kernel_gcc_patch) and some
                [_openSUSE_ kernel](http://kernel.opensuse.org/cgit/kernel-source) patches
                (kernel-local must be edited to modify gcc optimizations)
 * **nautilus-dropbox** - Optional nautilus support and use system binary **dropboxd**
 * **steam** - Patch reordering, personal fixes on desktop file and launcher script
 * **VirtualBox** - Extra patches, a boot logo, no update checking, **VirtualBox-extpack-oracle**
                    and **VirtualBox-guest-additions-iso** support
 * **wine** - [Gallium Nine](https://github.com/sarnex/wine-d3d9-patches) support,
              extra patches and personal fixes

## Credits (Patches, install procedures and other files)
* [Arch](https://www.archlinux.org)
* [Debian](https://www.debian.org)
* [Fedora](https://fedoraproject.org)
* [Gentoo](https://www.gentoo.org)
* [openSUSE](https://www.opensuse.org)
* [Ubuntu](https://www.ubuntu.com)
