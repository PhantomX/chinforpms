%global commit 85ca5537ac2a067d4c0e2fd67dd17ab6bde4359e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20181211
%global with_snapshot 1

%global sdl2_version %(pkg-config --silence-errors --modversion sdl2 2>/dev/null || echo 2.0.10)

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           sdlcl
Version:        1.2.15
Release:        1%{?gver}%{?dist}
Summary:        Compatibility library that allows SDL 1.2 applications to use SDL 2.0

License:        LGPLv2
URL:            https://github.com/MrAlert/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(sdl2)
Requires:       SDL2%{_isa} >= %{sdl2_version}


%description
%{summary}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

sed \
  -e '/^CFLAGS =/s|=.*|+= -fPIC `pkg-config --cflags sdl2` -fvisibility=hidden|g' \
  -e '/^LDFLAGS =/s|=.*|+= -shared -ldl|g' \
  -i Makefile


%build
%set_build_flags
%make_build


%install
mkdir -p %{buildroot}%{_libdir}/%{name}
chmod +x *.so.*
cp -a *.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files
%license COPYING
%doc README.md
%{_libdir}/%{name}/*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.15-1.20181211git85ca553
- Initial spec
