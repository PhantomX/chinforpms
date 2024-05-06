%if 0%{?fedora} >= 40
%global build_type_safety_c 0
%endif

%global pkgname libvorbis

Name:           %{pkgname}-aotuv
Summary:        The Vorbis General Audio Compression Codec - aoTuV optimized
Version:        1.3.7
Release:        3%{?dist}

License:        BSD-3-Clause

URL:            https://www.xiph.org/
Source0:        https://downloads.xiph.org/releases/vorbis/%{pkgname}-%{version}.tar.xz

# https://ao-yumi.github.io/aotuv_web/index.html
# https://freac.org
Patch10:        https://freac.org/patches/%{pkgname}-1.3.7-aotuv-b6.03.patch
Patch11:        https://freac.org/patches/%{pkgname}-1.3.7-aotuv-b6.03-lancer.patch
Patch12:        0001-sharedbook-Revert-memory-leak-fix-to-please-Lancer-o.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(ogg) >= 1.0

Requires:       %{pkgname}%{?_isa} >= %{version}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*
%global __requires_exclude ^libvorbis\\.so.*$


%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates.

The libvorbis package contains runtime libraries for use in programs
that support Ogg Vorbis.

This release is compiled with aoTuV optimizations patches


%prep
%autosetup -n %{pkgname}-%{version} -p1

sed -i "s|-O20||" configure
sed -i "s|-O3||" configure
sed -i "s/-ffast-math//" configure
sed -i "s/-mcpu=750//" configure


%build
%configure \
  --disable-static \
  --disable-silent-rules \
  --disable-docs \
  --disable-examples \
%{nil}

%make_build


%install
%make_install docdir=%{_pkgdocdir}

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -f %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%license COPYING
%{_libdir}/%{name}/*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Mon May 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.7-3
- Provides and requires tweaks

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.7-2
- build_type_safety_c 1

* Fri Dec 11 2020 Phantom X <megaphantomx at hotmail dot com> - 2:1.3.7-1
- Initial spec
