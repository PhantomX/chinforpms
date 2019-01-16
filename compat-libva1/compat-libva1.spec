%global pkgname libva

Name:           compat-libva1
Version:        1.8.3
Release:        1%{?dist}
Summary:        Video Acceleration (VA) API for Linux - v1

License:  MIT
URL:            https://01.org/linuxmedia

Source0:        https://github.com/01org/libva/archive/%{version}/%{pkgname}-%{version}.tar.gz


BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
%{!?_without_wayland:
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-scanner) >= 1
BuildRequires:  pkgconfig(wayland-server) >= 1
}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
Libva is a library providing the VA API video acceleration API.
This version of libva package contains only the libraries
and is provided for compatibility with STEAM_RUNTIME=0 from steam.


%prep
%autosetup -n %{pkgname}-%{version} -p1
autoreconf -ivf

%build
%configure \
  --libdir=%{_libdir}/libva1 \
  --disable-silent-rules \
  --disable-static \
  --enable-glx \
  --with-drivers-path=%{_libdir}/libva1/dri \
  --disable-va-messaging \
%{?_without_wayland:--disable-wayland}

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install INSTALL="install -p"

# Remove devel files, this is a compat package
rm -f %{buildroot}%{_libdir}/libva1/libva*.{la,so}
rm -rf %{buildroot}%{_libdir}/libva1/pkgconfig
rm -rf %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/libva1" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p %{buildroot}%{_libdir}/libva1/dri

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc NEWS
%license COPYING
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{_libdir}/libva1/libva*.so.*
%dir %{_libdir}/libva1/dri


%changelog
* Tue Jan 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.8.3-1
- Initial spec
