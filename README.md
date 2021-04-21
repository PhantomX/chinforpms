# chinforpms

Personal Fedora RPM specs. Has specs to build RPMs nonexistent in Fedora or RPMFusion and existent packages updated with extra changes, or snapshots, or only backports from Rawhide.

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
 * **bluecurve-icon-theme** - Extra symbolic links for cursors, more hardcoded icon sizes
 * **claws-mail** - Can't wait Fedora releases. Tests
 * **deluge** - Updated, no GConf support
 * **devedeng** - Boolean dependencies for video players and disc burners
 * **easytag** - Tests
 * **engrampa** - Split caja extension
 * **FAudio** - Tests
 * **fdk-aac** - For i686 mock build
 * **firejail** - suid bit enabled and "firejail" group to use it
 * **gamemode** - System inih and launch script
 * **gnome-themes-extra** - Remove some paddings from Adwaita
 * **gstreamer1** - Added suffix -32/-64 to gst-plugin-scanner, so it can build
                    correct multilib plugins registry, as
                    _~/.cache/gstreamer-1.0/registry.i686.bin_ on x86_64
 * **gstreamer1-plugins-base** - preroll buffer fix from Guy1524
 * **gstreamer1-plugins-ugly** - asfdemux fixes from Guy1524
 * **gtk3** - Revert some features ditched in 3.10 release, some _Debian_,
              _Ubuntu_ and [_gtk3-classic](https://github.com/lah7/gtk3-classic) patches
 * **keepassxc** - Post script and cosmetic fixes
 * **kernel** - _blk-mq_ and BFQ enabled by default, [CPU optimizations](https://github.com/graysky2/kernel_gcc_patch) and some
                [_openSUSE_ kernel](http://kernel.opensuse.org/cgit/kernel-source) and [_pf-kernel_](https://gitlab.com/post-factum/pf-kernel/wikis/README) patches
                (kernel-local must be edited to modify gcc optimizations)
 * **krename** - Updated, KF5
 * **libmirage** - Can't wait Fedora releases and better matching with cdemu builds from here
 * **libvirt, qemu, virt-manager** - Updated
 * **lutris** - Personal changes
 * **manaplus** - Updated, SDL2
 * **mednafen** - No Haswell optimizations
 * **mesa** - Can't wait Fedora releases. iXit patches
 * **mupen64plus** - Build options and packaging structure
 * **pcsxr** - CHD support
 * **ppsspp** - Build options, no Qt frontend
 * **qmc2** - Qt5, no game-menus
 * **skrooge** - Can't wait Fedora releases
 * **speedtest-cli** - Can't wait Fedora releases
 * **smtube** - Patched to silence players output
 * **steam** - Patch reordering, personal fixes on desktop file and launcher script
 * **taglib** - Tests
 * **telegram-desktop** - Personal fixes
 * **vkd3d** - Can't wait Fedora releases
 * **vulkan-headers, vulkan-loader, vulkan-tools** - Can't wait Fedora releases. No sdk releases too
 * **xboxdrv** - Experimental fork and personal changes
 * **xfce4-notes-plugin** - No automatic autostart settings
 * **wine** - Personal fixes and extra patches, like [_PBA_](https://github.com/acomminos/wine-pba) and
              more gathered from [_TK-Glitch_](https://github.com/Tk-Glitch/PKGBUILDS/tree/master/wine-tkg-git), some of them not always enabled.
              No alternatives support
 * **wine-dxvk** - mingw build and no alternatives support, enabled by script
 * **yabause** - CHD support
 * More not listed here

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
