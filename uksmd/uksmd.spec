%global commit 779017a3dc5f5951811bffdae6f3634e5cba91fa
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230204
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           uksmd
Version:        0
Release:        5%{?dist}

Summary:        Userspace KSM helper daemon
License:        GPL-3.0-only

URL:            https://codeberg.org/pf-kernel/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%endif

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  pkgconfig(libprocps)
BuildRequires:  pkgconfig(libcap-ng)
BuildRequires:  systemd


%description
The daemon goes through the list of userspace tasks (once per 5 seconds)
and hints them to apply MADV_MERGEABLE to anonymous mappings for ksmd
kthread to merge memory pages with the same content. Only long-living
tasks are hinted (those that were launched more than 10 seconds ago).

This requires "/proc/<pid>/ksm" interface, which is available in
pf-kernel (https://gitlab.com/post-factum/pf-kernel/).


%prep
%autosetup -n %{name} -p1


%build
%meson
%meson_build

%install
%meson_install


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service


%changelog
* Fri Mar 31 2023 Phantom X <megaphantomx at hotmail dot com> - 0-5.20230204git779017a
- Bump
- meson
- New URL

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0-4.20211019gite1d4b12
- Bump

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0-3.20210928git4635f7d
- Last snapshot

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0-2.20210508gitb6af35c
- Bump

* Thu Aug 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20190519git42f4ff8
- Initial spec
