%define gkthemedir %{_datadir}/gkrellm2/themes
%define pkgname GKrellM-Skins

Name:           gkrellm-themes
Version:        0.1
Release:        1%{?dist}
Summary:        Some themes for the GNU Krell Monitor

License:        GPLv2+
URL:            http://www.muhri.net/gkrellm/
Source0:        http://www.muhri.net/gkrellm/%{pkgname}.tar.gz

BuildArch:      noarch

Requires:       gkrellm

%description
This package contains various themes to use with GKrellM.

%prep
%autosetup -n GKrellM-skins

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gkthemedir}

for f in *.tar.gz *.tgz ;do
  tar -xzvf ${f} -C %{buildroot}%{gkthemedir}
done

find %{buildroot}%{gkthemedir} -type d -name .xvpics -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -type d -print0 | xargs -0 chmod 0755
find %{buildroot}%{gkthemedir} -type f -print0 | xargs -0 chmod 0644

find %{buildroot} -type d -name 'CVS' -print0 | xargs -0r rm -rf
find %{buildroot} -name '*~' -print0 | xargs -0r rm -rf
find %{buildroot} -name '.symlinks' -print0 | xargs -0r rm -rf

%files
%{gkthemedir}/*

%changelog
* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.1-1
- First spec.
