%global commit f95c3b3761ee1b1903f54ae69b526ed6f0edc3b9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210623
%global gver .%{date}git%{shortcommit}

%global pkgname SPIRV-Headers

Name:           spirv-headers
Version:        1.5.4
Release:        109%{?gver}%{?dist}
Summary:        Header files from the SPIR-V registry

License:        MIT
URL:            https://github.com/KhronosGroup
Source0:        %{url}/%{name}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

BuildArch:      noarch

%description
%{summary}

This includes:

* Header files for various languages.
* JSON files describing the grammar for the SPIR-V core instruction
  set, and for the GLSL.std.450 extended instruction set.
* The XML registry file

%package        devel
Summary:        Development files for %{name}

%description    devel
%{summary}

This includes:

* Header files for various languages.
* JSON files describing the grammar for the SPIR-V core instruction
  set, and for the GLSL.std.450 extended instruction set.
* The XML registry fil

%prep
%autosetup -n %{pkgname}-%{commit}
chmod a-x include/spirv/1.2/spirv.py

sed -e '/^project/s|1.5.1|%{version}|' -i CMakeLists.txt


%build


%install
mkdir -p %{buildroot}%{_includedir}/
mv include/* %{buildroot}%{_includedir}/

%files devel
%license LICENSE
%doc README.md
%{_includedir}/spirv/

%changelog
* Fri Jun 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-109.20210623gitf95c3b3
- Last snapshot

* Fri Jun 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-108.20210609gitf5417a4
- Update

* Mon May 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-107.20210429git85b7e00
- Bump

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-106.20210414gitdafead1
- Update

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-105.20210331gitf88a1f9
- Bump

* Fri Feb 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-104.20210219gita3fdfe8
- Update

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-103.20210120git8bb2420
- Latest snapshot

* Fri Dec 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-102.20201127gitf027d53
- Update

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-101.20201123git104ecc3
- Bump

* Fri Oct 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1.5.4-100.20201023git7845730
- 1.5.4

* Sat Oct  3 2020 Phantom X <megaphantomx at hotmail dot com> - 1.5.1-101.20200927gitd4e76fb
- Bump

* Mon Sep 14 2020 Phantom X <megaphantomx at hotmail dot com> - 1.5.3-100.20200910git060627f
- New snapshot

* Tue Aug 04 2020 Dave Airlie <airlied@redhat.com> - 1.5.1-5.20200803.git3fdabd0
- Update to latest spirv headers

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4.20200414.git2ad0492
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.5.1-3
- Update to latest spirv headers

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.5.1-2
- Update to latest spirv headers

* Tue Nov 12 2019 Dave Airlie <airlied@redhat.com> - 1.5.1-1
- Latest git snapshot building vulkan

* Thu Aug 01 2019 Dave Airlie <airlied@redhat.com> - 1.4.2-0.1
- Latest git snapshot for building vulkan.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 03:08:22 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 1.4.1-1
- Release 1.4.1

* Thu Mar 07 2019 Dave Airlie <airlied@redhat.com> - 1.2-0.12.20190307.git03a0815
- Update to latest version

* Mon Feb 04 2019 Dave Airlie <airlied@redhat.com> - 1.2-0.11.20190125.git8bea0a2
- Update to latest version

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.10.20180703.gitff684ff
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.9.20180703.gitff684ff
- Revert last commit

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.8.20180919.gitd5b2e12
- Update for SPIRV-Tools-2018.5

* Mon Jul 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.7.20180703.gitff684ff
- Update for SPIRV-Tools-2018.4

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.6.20180405.git12f8de9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.5.20180405.git12f8de9
- Update for vulkan 1.0.73.0

* Fri Feb 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.4.20180201.gitce30920
- Update for vulkan 1.0.68.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.3.20171015.git0610978
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.2.20171015.git0610978
- fix rpmlint error

* Thu Jul 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.2-0.1.20171015.git0610978
- First build

