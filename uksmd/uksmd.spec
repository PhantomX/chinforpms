%global commit 42f4ff8eb09011bf1a199938aa2afe23040d7faf
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190519
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           uksmd
Version:        0
Release:        1%{?gver}%{?dist}

Summary:        Userspace KSM helper daemon
License:        GPLv3

URL:            https://gitlab.com/post-factum/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/-/archive/%{commit}/%{name}-%{commit}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2
%endif

BuildRequires:  gcc
BuildRequires:  pkgconfig(libprocps)
BuildRequires:  systemd


%description
The daemon goes through the list of userspace tasks (once per 5 seconds)
and hints them to apply MADV_MERGEABLE to anonymous mappings for ksmd
kthread to merge memory pages with the same content. Only long-living
tasks are hinted (those that were launched more than 10 seconds ago).

This requires "/proc/<pid>/ksm" interface, which is available in
pf-kernel (https://gitlab.com/post-factum/pf-kernel/).


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%make_build \
  CFLAGS="%{build_cflags} -fno-plt" \
  LDFLAGS="%{build_ldflags} `pkg-config --libs libprocps`"


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
* Thu Aug 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20190519git42f4ff8
- Initial spec
