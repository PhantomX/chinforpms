%global __filter_GLIBC_PRIVATE 1

Name:           libstrangle
Version:        0.1.1
Release:        2%{?dist}
Summary:        Frame rate limiter

License:        GPL-3.0-only
URL:            https://gitlab.com/torkel104/%{name}
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2

Patch10:         0001-look-for-libvulkan.so.1.patch
Patch11:         0001-look-for-libdl.so.2.patch
Patch12:         0001-makefile-rpm-packaging.patch
Patch13:         0001-gcc-13-build-fix.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gl)
Recommends:     (libstrangle(x86-32) if glibc(x86-32))


%description
%{summary}.


%prep
%autosetup -p1

%build
%set_build_flags
%make_build libdir=%{_libdir}


%install
%make_install libdir=%{_libdir}

rm -rf %{buildroot}%{_sysconfdir}


%files
%license COPYING
%doc README.md
%{_bindir}/strangle
%{_bindir}/stranglevk
%{_libdir}/%{name}/%{name}.so
%{_libdir}/%{name}/%{name}_nodlsym.so
%{_libdir}/%{name}/%{name}_vk.so
%{_datadir}/vulkan/implicit_layer.d/libstrangle_vk.json


%changelog
* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-2
- gcc 13 build fix

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- 0.1.1

* Thu May 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.0.4-2
- Remove unneeded ld.so.conf file

* Mon Feb 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.0.4-1
- Initial spec
