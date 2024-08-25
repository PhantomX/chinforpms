%global pkgname vbrfix
%global debpatchver 1

Name:           vbrfixc
Version:        0.24
Release:        1%{?dist}
Summary:        Fixes MP3s and re-constructs VBR headers

License:        GPL-2.0-only
URL:            https://deb.debian.org/debian/pool/main/v/%{pkgname}

Source0:        https://deb.debian.org/debian/pool/main/v/%{debname}/%{pkgname}_%{version}+dfsg.orig.tar.xz
Source1:        https://deb.debian.org/debian/pool/main/v/%{debname}/%{pkgname}_%{version}+dfsg-%{debpatchver}.debian.tar.xz
Source2:        Makefile.%{name}

Patch0:         0001-format-security.patch

BuildRequires:  gcc-g++
BuildRequires:  make


%description
Vbrfix reconstructs MP3 files removing unwanted data, recreates VBR Tag with
seek information if it is VBR, can remove ID3v1/ID3v2/FHG/VBRI tags, can keep
the LAME part of the VBR tag while replacing the seek/bitrate info. 


%prep
%autosetup -p1 -a 1
for i in $(<debian/patches/series);do
  %{__scm_apply_patch -p1 -q} -i debian/patches/$i
done

# Remove old autoconf and replace with single Makefile
rm -rf %{name}/Makefile*
cp -a %{S:2} %{name}/

chmod -x %{name}/*.{h,cpp}


%build
%make_build -C %{name} -f Makefile.%{name}

%install
%make_install -C %{name} -f Makefile.%{name}

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 debian/%{pkgname}.1 %{buildroot}%{_mandir}/man1/


%files
%license COPYING
%doc README
%{_bindir}/%{pkgname}
%{_mandir}/man1/%{pkgname}.1.*


%changelog
* Sat Apr 08 2023 Phantom X <megaphantomx at hotmail dot com> - 0.24-1
- Initial spec
