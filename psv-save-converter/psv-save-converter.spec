%if 0%{?fedora} >= 40
%global build_type_safety_c 0
%endif

%global commit af0b92e8758f1ed2ce14870c4446b60ac0f65f71
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211011

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           psv-save-converter
Version:        0
Release:        2%{?dist}
Summary:        PS3 PSV save tool

License:        GPL-3.0-or-later
URL:            https://github.com/bucanero/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

Provides:       bundled(sha1-reid)


%description
This tool converts and resigns PS1 and PS2 savegame files to PlayStation 3 .PSV
save format.
The tool can also export .PSV PS3 files back to PS1 (.mcs) and PS2 (.psu) save
formats.


%prep
%autosetup -n %{name}-%{commit} -p1

sed \
  -e '/^CPPFLAGS/s| -s -static | |g' \
  -i Makefile


%build
%make_build TARGET_EXEC=%{name}

%install
mkdir -p %{buildroot}%{_bindir}

install -pm0755 build/%{name} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0-2.20211011gitaf0b92e
- build_type_safety_c 0

* Sun Oct 08 2023 Phantom X <megaphantomx at hotmail dot com> - 0-1.20211011gitaf0b92e
- Initial spec

