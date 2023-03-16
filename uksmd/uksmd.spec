%global commit e1d4b12d22fd710f0155d75585940f0d439f1544
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211019
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           uksmd
Version:        0
Release:        4%{?gver}%{?dist}

Summary:        Userspace KSM helper daemon
License:        GPL-3.0-only

URL:            https://gitlab.com/post-factum/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/-/archive/%{commit}/%{name}-%{commit}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2
%endif

BuildRequires:  make
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
%autosetup %{?gver:-n %{name}-%{commit}} -p1


%build
%set_build_flags
%make_build \
  CFLAGS="$CFLAGS -fno-plt" \
  LDFLAGS="$LDFLAGS $(pkg-config --libs libprocps libcap-ng)"


%install
%make_install PREFIX=%{_prefix}

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 distro/%{name}.service %{buildroot}%{_unitdir}/


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
* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0-4.20211019gite1d4b12
- Bump

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0-3.20210928git4635f7d
- Last snapshot

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0-2.20210508gitb6af35c
- Bump

* Thu Aug 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20190519git42f4ff8
- Initial spec
