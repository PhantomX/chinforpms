%global commit a3ff06d9228294b8cc9fef5a87afe37820e34a30
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180711

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           pkgrip
Version:        1.1
Release:        1.a%{?dist}
Summary:        Fast linux alternative for decrypting PS3/PSP pkgs

License:        GPL-3.0-only
URL:            https://github.com/qwikrazor87/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

Patch0:         %{url}/pull/4.patch#/%{name}-gh-pr4.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(zlib)

Provides:       bundle(libkirk)


%description
%{name} is a PC app to decrypt PSP/PS3 pkgs. It has support for extracting PS1
KEYS.BIN and decrypting PTF themes.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

sed \
  -e 's|CFLAGS = -Wall -Wextra -Werror|CFLAGS+=|g' \
  -e '/^CFLAGS+=-O2/d' \
  -e 's|-L ./libkirk |$(LDFLAGS) \0|g' \
  -i src/Makefile

%build
%make_build -C src libkirk/libkirk.a
%make_build -C src pkgrip


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 src/%{name} %{buildroot}%{_bindir}


%files
%license gpl-3.0.txt
%doc README.md
%{_bindir}/%{name}


%changelog
* Fri Jul 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1-1.a.20180711gita3ff06d
- Initial spec
