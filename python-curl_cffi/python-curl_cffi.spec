%global srcname curl_cffi
%global impersonate_ver 1.5.6

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "%%^", ""); print(ver)}

Name:           python-%{srcname}
Version:        0.15.0
Release:        1%{?dist}
Summary:        Python binding for curl-impersonate fork via cffi

License:        MIT
URL:            https://github.com/lexiforest/%{srcname}

Source0:        %{url}/archive/v%{ver}/%{srcname}-%{ver}.tar.gz

Patch0:         https://gitlab.archlinux.org/archlinux/packaging/packages/%{name}/-/raw/8ee3b5a8a09e4d65eb05cef836c8404cf9cef96f/use-system-curl-impersonate.patch#/%{name}-archlinux-use-system-curl-impersonate.patch

BuildRequires:  python3-devel
BuildRequires:  curl-impersonate-devel = %{impersonate_ver}
BuildRequires:  gcc
BuildRequires:  gcc-g++

%global _description %{expand:
%{summary}.}

%description %_description

%package     -n python3-%{srcname}
Summary:        %{summary}
Provides:       %{srcname} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-%{srcname}
%_description


%prep
%autosetup -n %{srcname}-%{ver} -p1

sed -e '/^before-all/d' -i pyproject.toml
sed \
  -e 's|@CURL_IMPERSONATE_VERSION@|%{impersonate_ver}|' \
  -e '/library_dirs/s|"/usr/lib"|"%{_libdir}"|g' \
  -i scripts/build.py
sed -e '/include/s|"curl/curl.h"|<curl-impersonate/curl.h>|' -i ffi/shim.h

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{srcname}


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/curl-cffi


%changelog
* Sun Jun 14 2026 Phantom X <megaphantomx at hotmail dot com> - 0.15.1^b2-1
- Initial spec

