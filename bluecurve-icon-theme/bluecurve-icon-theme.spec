%global src_hash 3a3ecac0922f964bb1c4be617e8dec37

Name:           bluecurve-icon-theme
Summary:        Bluecurve icon theme
Version:        8.0.2
Release:        103%{?dist}

Epoch:          1

License:        GPL-1.0-or-later
# There is no official upstream yet
Source0:        http://src.fedoraproject.org/repo/pkgs/%{name}/%{name}-%{version}.tar.bz2/%{src_hash}/%{name}-%{version}.tar.bz2
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/Bluecurve-classic.tar.bz2/b0a34d7a0af0e0c1786f7d459a94b9ee/Bluecurve-classic.tar.bz2
Source3:        link.png
URL:            http://www.redhat.com

BuildArch:      noarch

Patch0:         bluecurve-icon-theme-8.0.2-kde4.patch

Requires:       system-logos
Requires:       bluecurve-cursor-theme
Requires(post): coreutils

BuildRequires:  gcc
BuildRequires:  make
# we require XML::Parser for our in-tree intltool
BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  ImageMagick

%description
This package contains Bluecurve style icons.

%package -n bluecurve-cursor-theme
Summary: Bluecurve cursor theme

%description -n bluecurve-cursor-theme
This package contains Bluecurve style cursors.

%prep
%autosetup -p0

%build
%configure
make

%install
make install DESTDIR=%{buildroot}

# These are empty
rm -f ChangeLog NEWS README

touch %{buildroot}%{_datadir}/icons/Bluecurve/icon-theme.cache

# Install classic cursors
tar -xvf %{SOURCE1} -C %{buildroot}%{_datadir}/icons/ || exit 1
find %{buildroot}%{_datadir}/icons/ -type d -print0 | xargs -0 chmod 0755
find %{buildroot}%{_datadir}/icons/ -type f -print0 | xargs -0 chmod 0644

rmdir -p %{buildroot}%{_datadir}/locale ||:

rm -vf %{buildroot}%{_datadir}/icons/Bluecurve/*/*/audio.png
ln -s desktop.png %{buildroot}%{_datadir}/icons/Bluecurve/48x48/apps/user-desktop.png

# Fix cursors
for dir in {,L}Bluecurve{,-inverse} ; do
  ( cd %{buildroot}%{_datadir}/icons/${dir}/cursors
    ln -s hand1 9d800788f1b08800ae810202380a0822
    ln -s hand1 5aca4d189052212118709018842178c0 
    ln -s hand2 e29285e634086352946a0e7090d73106
    ln -s hand2 pointer
    ln -s hand2 pointing_hand
    ln -s cross cell
    ln -s dnd-copy 6407b0e94181790501fd1e167b474872
    ln -s dnd-copy 1081e37283d90000800003c07f3ef6bf
    ln -s dnd-copy 08ffe1cb5fe6fc01f906f1c063814ccf
    ln -s dnd-copy b66166c04f8c3109214a4fbd64a50fc8
    ln -s dnd-copy copy
    ln -s dnd-move 4498f0e0c1937ffe01fd06f973665830
    ln -s dnd-move 9081237383d90e509aa00f00170e968f
    ln -s dnd-link alias
    ln -s dnd-link link
    ln -s dnd-link 0876e1c15ff2fc01f906f1c363074c0f
    ln -s dnd-link 640fb0e74195791501fd1ed57b41487f
    ln -s dnd-link a2a266d0498c3104214a47bd64ab0fc8
    ln -s dnd-move move
    ln -s dnd-none 03b6e0fcb3499374a867c041f52298f0
    ln -s dnd-none fcf21c00b30f7e3f83fe0dfd12e71cff
    ln -s dnd-none closedhand
    ln -s dnd-none forbidden
    ln -s dnd-none no-drop
    ln -s dnd-none not-allowed
    ln -s fleur all-scroll
    ln -s fleur size_all
    ln -s left_ptr default
    ln -s left_ptr_watch 00000000000000020006000e7e9ffc3f
    ln -s left_ptr_watch 3ecb610c1bf2410f44200f48c40d3599
    ln -s left_ptr_watch 0426c94ea35c87780ff01dc239897213
    ln -s left_ptr_watch half-busy
    ln -s left_ptr_watch wait
    ln -s left_ptr_watch 9116a3ea924ed2162ecab71ba103b17f
    ln -s left_ptr_watch progress
    ln -s top_right_corner fcf1c3c7cd4491d801f1e1c78f100000
    ln -s top_right_corner 50585d75b494802d0151028115016902
    ln -s top_right_corner nesw-resize
    ln -s top_right_corner size_bdiag
    #ln -s plus 6407b0e94181790501fd1e167b474872
    ln -s plus 3085a0e285430894940527032f8b26df
    ln -s sb_h_double_arrow 14fef782d02440884392942c11205230
    ln -s sb_h_double_arrow 028006030e0e7ebffc7f7070c0600140
    ln -s sb_h_double_arrow 043a9f68147c53184671403ffa811cc5 
    ln -s sb_h_double_arrow col-resize
    ln -s sb_h_double_arrow ew-resize
    ln -s sb_h_double_arrow e-resize
    ln -s sb_h_double_arrow size_hor
    ln -s sb_h_double_arrow split_h
    ln -s sb_h_double_arrow w-resize
    ln -s top_left_corner c7088f0f3e6c8088236ef8e1e3e70000
    ln -s top_left_corner 38c5dff7c7b8962045400281044508d2
    ln -s top_left_corner nwse-resize
    ln -s top_left_corner size_fdiag
    ln -s sb_up_arrow up_arrow
    ln -s sb_v_double_arrow 2870a09082c103050810ffdffffe0204
    ln -s sb_v_double_arrow c07385c7190e701020ff7ffffd08103c
    ln -s sb_v_double_arrow n-resize
    ln -s sb_v_double_arrow row-resize
    ln -s sb_v_double_arrow size_ver
    ln -s sb_v_double_arrow split_v
    ln -s sb_v_double_arrow v_double_arrow
    ln -s question_arrow d9ce0ab605698f320427677b458ad60b
    ln -s question_arrow help
    ln -s question_arrow whats_this
    ln -s double_arrow 00008160000006810000408080010102
    ln -s double_arrow ns-resize
    ln -s xterm ibeam
    ln -s xterm term
  ) || exit 1
done

for dir in {,L}Bluecurve-inverse ; do
  ( cd %{buildroot}%{_datadir}/icons/${dir}/cursors
    ln -s question_arrow 5c6cd98b3f3ebcb1f9c7f1c204630408
  ) || exit 1
done

install -pm0644 %{SOURCE3} \
  %{buildroot}%{_datadir}/icons/Bluecurve/96x96/filesystems/link.png || exit 1
for s in 16x16 24x24 32x32 36x36 48x48 ; do
  src=%{buildroot}%{_datadir}/icons/Bluecurve/96x96/filesystems/link.png
  dir=%{buildroot}%{_datadir}/icons/Bluecurve/${s}/filesystems
  convert ${src} -filter Lanczos -resize ${s} \
    ${dir}/link.png || exit 1
done

for s in 16x16 24x24 48x48 96x96 ; do
  ( cd %{buildroot}%{_datadir}/icons/Bluecurve/${s}/mimetypes
    ln -s file-vector_art.png drawing.png
    ln -s file-presentation.png presentation.png
    # KOffice icons
    ln -s file-vector_art.png karbon_karbon.png
    ln -s file-presentation.png kpresenter_kpr.png
    ln -s file-wordprocessor.png kword_kwd.png
    ln -s file-spreadsheet.png kspread_ksp.png
  ) || exit 1
done

missresize() {
  basedir=$1
  newdir=$2
  if [ -d ${basedir}/stock ] ;then
    mkdir -p ${basedir}/actions
    echo "Copying ${basedir}/stock to ${basedir}/actions"
    for file in ${basedir}/stock/*.png ;do
      file2="${basedir}/actions/$(basename ${file})"
      if [ ! -f ${file2} ] ;then
        if [ -L ${file} ] ;then
          cp -a ${file} ${file2} || return $?
        else
          ln -s ../stock/$(basename ${file}) ${file2} || return $?
        fi
      fi
    done
  fi
  [ "${newdir}" = "none" ] && return 0
  for dir in ${basedir}/*/ ;do
    dir2=$(basename ${dir})
    for newres in ${newdir} ;do
      mkdir -p ${newres}/${dir2}
      if [ -d ${newres}/${dir2} ] ;then
        echo "Converting ${basedir}/${dir2} to ${newres}/${dir2}"
        for file in ${dir}/*.png ;do
          file2="${newres}/${dir2}/$(basename ${file})"
          if [ ! -f ${file2} ] ;then
            if [ -L ${file} ] ;then
              ln -s $(echo $(readlink ${file}) | sed -e "s|${basedir}|${newres}|g") ${file2} || return $?
            else
              convert ${file} -filter Lanczos -resize ${newres} ${file2} || return $?
            fi
          fi
        done
      fi
    done
  done
}

( cd %{buildroot}%{_datadir}/icons/Bluecurve
  missresize 96x96 "64x64 48x48 36x36 32x32 24x24 22x22 20x20 16x16"
  missresize 64x64 "48x48 36x36 32x32 24x24 22x22 20x20 16x16"
  missresize 48x48 "36x36 32x32 24x24 22x22 20x20 16x16"
  missresize 36x36 "32x32 24x24 22x22 20x20 16x16"
  missresize 32x32 "24x24 22x22 20x20 16x16"
  missresize 24x24 "22x22 20x20 16x16"
  missresize 22x22 "20x20 16x16"
  missresize 16x16 "none"
)

# The upstream packages may gain po files at some point in the near future
# %find_lang %{name} || touch %{name}.lang

%files
%doc AUTHORS COPYING
%{_datadir}/icons/Bluecurve/index.theme
%{_datadir}/icons/Bluecurve/16x16
%{_datadir}/icons/Bluecurve/20x20
%{_datadir}/icons/Bluecurve/22x22
%{_datadir}/icons/Bluecurve/24x24
%{_datadir}/icons/Bluecurve/32x32
%{_datadir}/icons/Bluecurve/36x36
%{_datadir}/icons/Bluecurve/48x48
%{_datadir}/icons/Bluecurve/64x64
%{_datadir}/icons/Bluecurve/96x96
%ghost %{_datadir}/icons/Bluecurve/icon-theme.cache

%files -n bluecurve-cursor-theme
%dir %{_datadir}/icons/Bluecurve
%{_datadir}/icons/Bluecurve/Bluecurve.cursortheme
%{_datadir}/icons/Bluecurve/cursors
%{_datadir}/icons/Bluecurve-inverse
%{_datadir}/icons/LBluecurve
%{_datadir}/icons/LBluecurve-inverse
%{_datadir}/icons/Bluecurve-classic
%{_datadir}/icons/Bluecurve-classic-inverse

%changelog
* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 8.0.2-103.chinfo
- BR: gcc

* Mon Mar 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 8.0.2-102.chinfo
- Remove obsolete scriptlets

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 8.0.2-101.chinfo
- Source0 url

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 8.0.2-100.chinfo
- Bump release

* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 8.0.2-15
- Added classic icons.
- Fixed cursors links.

* Sun Nov 06 2016 Filipe Rosset <rosset.filipe@gmail.com> - 8.0.2-14
- Fix FTBFS in rawhide rhbz #1307353 plus spec cleanup

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Ray Strode <rstrode@redhat.com> - 8.0.2-4
- Require coreutils for touch in post (bug 507581)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 24 2008 Matthias Clasen <mclasen@redhat.com> - 8.0.2-2
- Split off cursor theme as a separate package

* Mon Apr  7 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 8.0.2-1
- Add some symlinks to make Bluecurve work well with KDE 4 (#408151)

* Fri Feb  1 2008 Matthias Clasen <mclasen@redhat.com> - 8.0.1-1
- Fix some lrt <-> ltr typos
- Flip some redo icons

* Fri Oct 12 2007 Ray Strode <rstrode@redhat.com> - 8.0.0-1
- Add a lot of missing icons back (bug 328391)
- redo Bluecurve Makefile to scale better to all the new icons
- bump version to 8.0.0

* Tue Sep 25 2007 Ray Strode <rstrode@redhat.com> - 1.0.0-1
- Initial import, version 1.0.0
