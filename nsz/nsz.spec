%global commit 4ee7c8cd02da02476e79526237174dfb3c7986be
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240306
%bcond_with snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           nsz
Version:        4.6.1
Release:        1%{?dist}
Summary:        Homebrew compatible NSP/XCI compressor/decompressor

License:        MIT
URL:            https://github.com/nicoboss/nsz

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Use-pycryptodomex-instead-pycryptodome.patch
Patch1:         0001-Disable-GUI-support.patch
Patch2:         0001-Prevent-escape-warning.patch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist enlighten}
BuildRequires:  %{py3_dist pycryptodomex}
BuildRequires:  %{py3_dist zstandard}


%description
NSZ is a NX homebrew compatible NSP/XCI compressor/decompressor.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -N -p1

sed 's/\r//' -i *.txt

%autopatch -p1

rm -rf requirements-gui.txt nsz/gui

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files %{name}


%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Tue Apr 09 2024 Phantom X <megaphantomx at hotmail dot com> - 4.6.1-1
- Initial spec

