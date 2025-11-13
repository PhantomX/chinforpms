%global pkgname ejs
%global modname yt_dlp_ejs

Name:           yt-dlp-%{pkgname}
Version:        0.3.1
Release:        1%{?dist}
Summary:        External JavaScript for yt-dlp supporting many runtimes

License:        Unlicense AND MIT AND ISC
URL:            https://github.com/yt-dlp/ejs

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
Source1:        %{url}/releases/download/%{version}/%{modname}-%{version}-py3-none-any.whl

Patch0:         0001-Offline-build-fixes.patch

BuildArch:      noarch

BuildRequires:  python3-devel >= 3.10
BuildRequires:  %{py3_dist hatchling}
BuildRequires:  %{py3_dist hatch-vcs}
BuildRequires:  unzip


%description
%{pkgname} is an external JavaScript for yt-dlp supporting many runtimes.


%prep
%autosetup -p1 -n %{pkgname}-%{version}

unzip %{S:1} -d temp yt_dlp_ejs/yt/solver/{core,lib}.min.js

mkdir -p dist
for js in core lib ;do
  mv temp/yt_dlp_ejs/yt/solver/${js}.min.js dist/yt.solver.${js}.min.js
done

sed -e 's|_RPM_VERSION_|%{version}|g' -i pyproject.toml

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files %{modname}


%files -f %{pyproject_files}
%doc README.md
%license LICENSE


%changelog
* Wed Nov 12 2025 Phantom X <megaphantomx at hotmail dot com>  - 0.3.1-1
- Initial spec

