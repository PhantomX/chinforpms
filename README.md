# chinforpms

Personal Fedora RPM specs. Has specs to build RPMs nonexistent in Fedora or
RPMFusion and existent packages updated with extra changes.

> Most packages can be found in this [COPR repository](https://copr.fedorainfracloud.org/coprs/phantomx/chinforpms), except for those not allowed.

> Builds are tested with current stable Fedora release. Rawhide have very limited support and older releases don't have none. 

> *Epoch* is used without regard, running **dnf distro-sync** is recommended sometimes.

>_Before use, remember that **YOU ARE AT YOUR OWN RISK**! Don't blame me if your
>system explodes or suffer any other bad things._

>Study the licenses carefully.

## Requirements

 * [RPM Fusion](https://rpmfusion.org)

## Differences from Fedora and RPM Fusion

 * **adwaita-qt** - Remove some paddings
 * **belle-sip, linphone, ortp** - Updated version
 * **bluecurve-icon-theme** - Extra symbolic links for cursors, more hardcoded icon sizes
 * **claws-mail** - Can't wait Fedora releases
 * **easytag** - Tests
 * **engrampa** - Split caja extension
 * **FAudio** - Tests
 * **firejail** - suid bit enabled and "firejail" group to use it
 * **gamemode** - System inih and launch script
 * **gnome-themes-extra** - Remove some paddings from Adwaita
 * **gstreamer1** - Added suffix -32/-64 to gst-plugin-scanner, so it can build
                    correct multilib plugins registry, as
                    _~/.cache/gstreamer-1.0/registry.i686.bin_ on x86_64
 * **gtk3** - Revert some features ditched in 3.10 release, some _Debian_,
              _Ubuntu_ and [_gtk3-mushrooms_](https://github.com/TomaszGasior/gtk3-mushrooms) patches
 * **keepassxc** - Post script and cosmetic fixes
 * **kernel** - _blk-mq_ and BFQ enabled by default, [CPU optimizations](https://github.com/graysky2/kernel_gcc_patch) and some
                [_openSUSE_ kernel](http://kernel.opensuse.org/cgit/kernel-source) and [_pf-kernel_](https://gitlab.com/post-factum/pf-kernel/wikis/README) patches
                (kernel-local must be edited to modify gcc optimizations)
 * **krename** - Updated, KF5
 * **libtgvoip** - No unresolved symbols
 * **lutris** - Personal changes
 * **manaplus** - Updated, SDL2
 * **mednafen** - No Haswell optimizations
 * **mesa** - Can't wait Fedora releases
 * **ppsspp** - Build options, no Qt frontend
 * **quiterss** - Updated, Qt5
 * **rust** - Fixed version for Waterfox build
 * **skrooge** - Can't wait Fedora releases
 * **smtube** - Patched to silence players output
 * **steam** - Patch reordering, personal fixes on desktop file and launcher script
 * **taglib** - Tests
 * **telegram-desktop** - Personal fixes
 * ~~**VirtualBox** - Extra patches, a boot logo, no update checking, **VirtualBox-extpack-oracle**
                    and **VirtualBox-guest-additions-iso** support.~~
 * **vkd3d** - Can't wait Fedora releases
 * **xboxdrv** - Tests
 * **wine** - Personal fixes and extra patches, like [_Esync_](https://github.com/zfigura/wine), [_FAudio_](https://github.com/FNA-XNA/FAudio), [_PBA_](https://github.com/acomminos/wine-pba) and
              more gathered from [_TK-Glitch_](https://github.com/Tk-Glitch/PKGBUILDS/tree/master/wine-tkg-git), some of them not always enabled.

## Credits (Patches, install procedures and other files)
* [Arch](https://www.archlinux.org)
* [BFQ](http://algo.ing.unimo.it/people/paolo/disk_sched)
* [Debian](https://www.debian.org)
* [Fedora](https://fedoraproject.org)
* [Gentoo](https://www.gentoo.org)
* [openSUSE](https://www.opensuse.org)
* [pf-kernel](https://gitlab.com/post-factum/pf-kernel)
* [Tk-Glitch](https://github.com/Tk-Glitch)
* [Ubuntu](https://www.ubuntu.com)
