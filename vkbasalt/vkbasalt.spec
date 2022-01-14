%global commit d416bcb9ca3ab49eec07f93993caae4f72e3df4a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210719
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname vkBasalt

Name:           vkbasalt
Version:        0.3.2.4
Release:        3%{?gver}%{?dist}
Summary:        A vulkan post processing layer

License:        zlib
URL:            https://github.com/DadSchoorse/vkBasalt

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  spirv-headers-devel
BuildRequires:  vulkan-headers
BuildRequires:  pkgconfig(x11)
Requires:       vulkan-loader%{?_isa}

Provides:       %{pkgname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
vkBasalt is a Vulkan post processing layer to enhance the visual graphics of
games.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1


%build
%meson \
  -Dappend_libdir_vkbasalt=true \
%{nil}

%meson_build


%install
%meson_install

mkdir -p %{buildroot}%{_datadir}/%{pkgname}


%files
%license LICENSE
%doc README.md config/vkBasalt.conf
%{_libdir}/%{name}/lib%{name}.so
%dir %{_datadir}/%{pkgname}
%{_datadir}/vulkan/implicit_layer.d/%{pkgname}.json


%changelog
* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.4-3.20210719gitd416bcb
- Bump

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.4-2.20210305gitb929505
- Snapshot

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.4-1.20210218git111b0e8
- 0.3.2.4

* Sat Jan 09 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.3-1.20210108gitce647da
- 0.3.2.3

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.2-1.20201001gitca921c8
- Initial spec
