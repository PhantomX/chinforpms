Name:           vkd3d
Version:        1.0
Release:        100.chinfo%{?dist}
Summary:        Direct3D 12 to Vulkan translation library

License:        LGPLv2
URL:            http://www.winehq.org/
Source0:        https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz
Source10:       https://dl.winehq.org/%{name}/source/%{name}-%{version}.tar.xz.sign

BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(xcb-event)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(SPIRV-Tools-shared)
BuildRequires:  spirv-headers-devel

Provides:       lib%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Vkd3d is a 3D graphics library built on top of Vulkan. It has an API very
similar, but not identical, to Direct3D 12.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       lib%{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup


%build
%configure \
  --disable-static \
  --disable-silent-rules \
  --with-spirv-tools
%make_build


%install
%make_install

find %{buildroot} -name '*.la' -exec rm -f {} ';'


%files
%license LICENSE
%doc AUTHORS COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Sat May 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0-100.chinfo
- Initial spec
