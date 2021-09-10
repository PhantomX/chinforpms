%global __python %{__python3}
Name:           vulkan-headers
Version:        1.2.191
Release:        1%{?dist}
Summary:        Vulkan Header files and API registry

License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Headers

%if 1%(echo %{version} | cut -d. -f4) != 1
%global with_sdk 1
%endif

%if 0%{?with_sdk}
Source0:        %{url}/archive/sdk-%{version}.tar.gz#/Vulkan-Headers-sdk-%{version}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/Vulkan-Headers-%{version}.tar.gz
%endif

BuildRequires:  cmake3
BuildRequires:  make
BuildArch:      noarch

%description
Vulkan Header files and API registry

%prep
%if 0%{?with_sdk}
%autosetup -n Vulkan-Headers-sdk-%{version}
%else
%autosetup -n Vulkan-Headers-%{version}
%endif

%build
%cmake3 \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
%{nil}

%cmake3_build


%install
%cmake3_install


%files
%license LICENSE.txt
%doc README.md
%{_includedir}/vk_video/
%{_includedir}/vulkan/
%dir %{_datadir}/vulkan/
%{_datadir}/vulkan/registry/


%changelog
* Tue Sep 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.191-1
- 1.2.191

* Mon Aug 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.190-1
- 1.2.190

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.188-1
- 1.2.188

* Sun Aug 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.187-1
- 1.2.187

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.185-1
- 1.2.185

* Mon Jul 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.184-1
- 1.2.184

* Mon Jun 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.182-1
- 1.2.182

* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.180-1
- 1.2.180

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.178-1
- 1.2.178

* Mon Apr 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.177-1
- 1.2.177

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.176-1
- 1.2.176

* Tue Apr 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.175-1
- 1.2.175

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.174-1
- 1.2.174

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.173-1
- 1.2.173

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.172-1
- 1.2.172

* Mon Mar 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.171-1
- 1.2.171

* Mon Feb 15 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.170-1
- 1.2.170

* Sun Feb 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.169-1
- 1.2.169

* Mon Jan 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.168-1
- 1.2.168

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.167-1
- 1.2.167

* Mon Jan 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.166-1
- 1.2.166

* Tue Dec 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.165-1
- 1.2.165

* Mon Dec 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.164-1
- 1.2.164

* Sat Dec  5 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.163-1
- 1.2.163

* Mon Nov 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.162-1
- 1.2.162

* Tue Nov 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.161-1
- 1.2.161

* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.160-1
- 1.2.160

* Tue Nov  3 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.159-1
- 1.2.159

* Mon Oct 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.158-1
- 1.2.158

* Tue Oct 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.157-1
- 1.2.157

* Mon Oct  5 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.156-1
- 1.2.156

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.155-1
- 1.2.155

* Tue Sep 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.154-1
- 1.2.154

* Tue Sep 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.153-1
- 1.2.153

* Wed Sep 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.152-1
- 1.2.152

* Fri Aug 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.151-1
- 1.2.151

* Mon Aug 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.149-1
- 1.2.149

* Mon Jul 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.148-1
- 1.2.148

* Wed Jul 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.147-1
- 1.2.147

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.146-1
- 1.2.146

* Sun Jun 21 2020 Phantom X <megaphantomx at hotmail dot com>
- 1.2.145

* Wed Jun 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.143-1
- 1.2.143

* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.141-1
- 1.2.141

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.140-1
- Update to 1.2.140 headers

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.2.135.0-1
- Update to 1.2.135.0 headers

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.2.131.1-1
- Update to 1.2.131.1 headers

* Tue Nov 12 2019 Dave Airlie <airlied@redhat.com> - 1.1.126.0-1
- Update to 1.1.126.0 headers

* Mon Jul 29 2019 Dave Airlie <airlied@redhat.com> - 1.1.114.0-2
- Update to 1.1.114.0 headers

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.108.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Dave Airlie <airlied@redhat.com> - 1.1.108.0-1
- Update to 1.1.108.0 headers

* Thu Apr 18 2019 Dave Airlie <airlied@redhat.com> - 1.1.106.0-1
- Update to 1.1.106.0 headers

* Wed Mar 06 2019 Dave Airlie <airlied@redhat.com> - 1.1.101.0-1
- Update to 1.1.101.0 headers

* Wed Feb 13 2019 Dave Airlie <airlied@redhat.com> - 1.1.97.0-1
- Update to 1.1.97.0 headers

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Dave Airlie <airlied@redhat.com> - 1.1.92.0-1
- Update to 1.1.92.0

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.85.0-1
- Update to 1.1.85.0

* Tue Aug 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.82.0-1
- Update to 1.1.82.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.77.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-1
- Initial package
