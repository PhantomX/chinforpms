%global with_sdk 0

Name:           vulkan-tools
Version:        1.2.197
Release:        1%{?dist}
Summary:        Vulkan tools

License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Tools

%if 0%{?with_sdk}
Source0:        %{url}/archive/sdk-%{version}.tar.gz#/Vulkan-Tools-sdk-%{version}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/Vulkan-Tools-%{version}.tar.gz
%endif


BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  glslang
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  vulkan-loader-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcb)

Provides:       vulkan-demos%{?_isa} = %{version}-%{release}
Obsoletes:      vulkan-demos < %{version}-%{release}

%description
Vulkan tools

%prep
%if 0%{?with_sdk}
%autosetup -n Vulkan-Tools-sdk-%{version}
%else
%autosetup -n Vulkan-Tools-%{version}
%endif


%build
%cmake3 \
  -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
  -DGLSLANG_INSTALL_DIR=%{_prefix} \
%{nil}

%cmake3_build


%install
%cmake3_install

for bin in vkcube vkcubepp vulkaninfo ;do
  mv %{buildroot}%{_bindir}/${bin}{,%{__isa_bits}}

cat >> %{buildroot}%{_bindir}/${bin} <<EOF
#!/usr/bin/sh
host=\$(uname -m)
case "\$host" in
  alpha*|ia64*|ppc64*|powerpc64*|s390x*|x86_64*|aarch64*)
    exec %{_bindir}/${bin}64 "\$@"
    ;;
  *)
    exec %{_bindir}/${bin}32 "\$@"
    ;;
esac
EOF
  chmod 0755 %{buildroot}%{_bindir}/${bin}

done


%files
%license LICENSE.txt
%doc README.md CONTRIBUTING.md
%{_bindir}/*

%changelog
* Thu Nov 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.197-1
- 1.2.197

* Sat Oct 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.196-1
- 1.2.196

* Wed Oct 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.195-1
- 1.2.195

* Tue Sep 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.194-1
- 1.2.194

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.192-1
- 1.2.192

* Fri Sep 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.191-1
- 1.2.191

* Mon Aug 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.190-1
- 1.2.190

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.188-1
- 1.2.188

* Sun Aug 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.187-1
- 1.2.187

* Thu Jul 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.185-1
- 1.2.185

* Sun Jul 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.184-1
- 1.8.184

* Tue Jul 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.183-1
- 1.2.183

* Tue Jun 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.182-1
- 1.2.182

* Tue Jun 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.180-1
- 1.2.180

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.178-1
- 1.2.178

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.176-2
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

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.166-1
- 1.2.166

* Mon Jan 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.165-1
- 1.2.165

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.162-1
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

* Tue Sep 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.152-1
- 1.2.152

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

* Tue May 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.140-1
- Update to 1.2.140
- Multilib wrappers

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.2.135.0-1
- Update to 1.2.135.0

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.2.131.1-1
- Update to 1.2.131.1

* Thu Nov 14 2019 Dave Airlie <airlied@redhat.com> - 1.1.126.0-1
- Update to 1.1.126.0

* Wed Jul 31 2019 Dave Airlie <airlied@redhat.com> - 1.1.114.0-1
- Update to 1.1.114.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.108.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Dave Airlie <airlied@redhat.com> - 1.1.108.0-1
- Update to 1.1.108.0

* Thu Mar 07 2019 Dave Airlie <airlied@redhat.com> - 1.1.101.0-1
- Update to 1.1.101.0

* Wed Feb 13 2019 Dave Airlie <airlied@redhat.com> - 1.1.97.0-1
- Update to 1.1.97.0

* Tue Feb 12 2019 Dave Airlie <airlied@redhat.com> - 1.1.92.0-1
- Update to 1.1.92.0
- don't rename anymore, upstream changed cube app name

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.82.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.82.0-1
- Update to 1.1.82.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.77.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-1
- Initial package
