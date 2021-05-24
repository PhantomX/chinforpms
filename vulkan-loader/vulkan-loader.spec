%global with_sdk 0

Name:           vulkan-loader
Version:        1.2.178
Release:        1%{?dist}
Summary:        Vulkan ICD desktop loader

License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Loader

%if 1%(echo %{version} | cut -d. -f4) != 1
%global with_sdk 1
%endif

%if 0%{?with_sdk}
Source0:        %{url}/archive/sdk-%{version}.tar.gz#/Vulkan-Loader-sdk-%{version}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/Vulkan-Loader-%{version}.tar.gz
%endif


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  vulkan-headers >= %{version}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)

Provides:       vulkan%{?_isa} = %{version}-%{release}
Provides:       vulkan = %{version}-%{release}
Obsoletes:      vulkan < %{version}-%{release}
Provides:       vulkan-filesystem = %{version}-%{release}
Obsoletes:      vulkan-filesystem < %{version}-%{release}

%if 0%{?fedora} <= 27
%ifarch x86_64 i686 
Requires:       mesa-vulkan-drivers%{?_isa}
%endif
%else
Requires:       mesa-vulkan-drivers%{?_isa}
%endif

%description
This project provides the Khronos official Vulkan ICD desktop 
loader for Windows, Linux, and MacOS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       vulkan-headers
Provides:       vulkan-devel%{?_isa} = %{version}-%{release}
Provides:       vulkan-devel = %{version}-%{release}
Obsoletes:      vulkan-devel < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%if 0%{?with_sdk}
%autosetup -p1 -n Vulkan-Loader-sdk-%{version}
%else
%autosetup -p1 -n Vulkan-Loader-%{version}
%endif


%build
%cmake3 \
  -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
%{nil}

%cmake3_build


%install
%cmake3_install

# create the filesystem
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}%{_datadir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}{%{_sysconfdir},%{_datadir}}/vulkan/icd.d


%files
%license LICENSE.txt
%doc README.md CONTRIBUTING.md
%dir %{_sysconfdir}/vulkan/
%dir %{_sysconfdir}/vulkan/explicit_layer.d/
%dir %{_sysconfdir}/vulkan/icd.d/
%dir %{_sysconfdir}/vulkan/implicit_layer.d/
%dir %{_datadir}/vulkan/
%dir %{_datadir}/vulkan/explicit_layer.d/
%dir %{_datadir}/vulkan/icd.d/
%dir %{_datadir}/vulkan/implicit_layer.d/
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/vulkan.pc
%{_libdir}/*.so


%changelog
* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.178-1
- 1.2.178

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.176-1
- 1.2.176

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.174-1
- 1.2.174

* Thu Mar 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.173-1
- 1.2.173

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.172-1
- 1.2.172

* Mon Mar 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.170-1
- 1.2.170

* Sun Feb 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.169-1
- 1.2.169

* Mon Jan 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.166-1
- 1.2.166

* Tue Dec 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.162-2
- Remove @LIB_SUFFIX@ from library

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.162-1
- 1.2.162

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.161-2
- 1.2.162

* Sat Nov 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.161-1
- 1.2.161

* Tue Nov 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.160-1
- 1.2.160

* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.159-1
- 1.2.159

* Tue Nov  3 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.158-1
- 1.2.158

* Tue Oct 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.157-1
- 1.2.157

* Tue Sep 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.154-1
- 1.2.154

* Sun Sep 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.153-2
- Upstream fixes

* Tue Sep 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.153-1
- 1.2.153

* Fri Aug 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.151-1
- 1.2.151

* Wed Jul 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.148-1
- 1.2.148

* Wed Jul 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.147-1
- 1.2.147

* Thu Jul 09 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.146-1
- 1.2.146

* Wed Jul 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.145-1
- 1.2.145

* Sun May 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.141-1
- 1.2.141

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.140-1
- Update to 1.2.140

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.2.135.0-1
- Update to 1.2.135.0

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.2.131.1-1
- Update to 1.2.131.1

* Tue Nov 12 2019 Dave Airlie <airlied@redhat.com> - 1.1.126.0-1
- Update to 1.1.126.0

* Wed Jul 31 2019 Dave Airlie <airlied@redhat.com> - 1.1.114.0-1
- Update to 1.1.114.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.108.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Dave Airlie <airlied@redhat.com> - 1.1.108.0-0
- Update to 1.1.108.0

* Wed Mar 06 2019 Dave Airlie <airlied@redhat.com> - 1.1.101.0-0
- Update to 1.1.101.0

* Wed Feb 13 2019 Dave Airlie <airlied@redhat.com> - 1.1.97.0-0
- Update to 1.1.97.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Dave Airlie <airlied@redhat.com> - 1.1.92.0-1
- Update to 1.1.92.0

* Mon Nov 19 2018 Dave Airlie <airlied@redhat.com> - 1.1.85.0-1
- Update to 1.1.85.0

* Tue Aug 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.82.0-1
- Update to 1.1.82.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.77.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-4
- Fix update path

* Tue Jun 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-3
- Add conditional for mesa-vulkan-drivers requires

* Tue Jun 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-2
- Improve description and summary
- Set release

* Sat Jun 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-1
- Initial package
