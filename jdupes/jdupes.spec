Name:           jdupes
Version:        1.13.2
Release:        1%{?dist}
Summary:        A powerful duplicate file finder

License:        MIT

URL:            https://github.com/jbruchon/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:         0001-Use-system-xxhash.patch

BuildRequires:  gcc
BuildRequires:  xxhash-devel


%description
%{name} is a program for identifying and taking actions upon duplicate files.

%prep
%autosetup -p1

rm -f xxhash.*

%build
%make_build \
  COMPILER_OPTIONS="%{build_cflags} -DSMA_MAX_FREE=11" \
  LDFLAGS="%{build_ldflags}" \
  CFLAGS_EXTRA="-DENABLE_BTRFS" \
%{nil}


%install
%make_install \
  INSTALL="%{__install} -p" \
  PREFIX=%{_prefix} \
  BIN_DIR=%{_bindir} \
  MAN_BASE_DIR=%{_mandir}


%check
./%{name} testdir
./%{name} --omitfirst testdir
./%{name} --recurse testdir
./%{name} --size testdir


%files
%license LICENSE
%doc README.md
%doc %{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}


%changelog
* Sat Nov 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.13.2-1
- Initial spec
