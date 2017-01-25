%define gkthemedir %{_datadir}/gkrellm2/themes
%define pkgname GKrellM-Skins

Name:           gkrellm-themes
Version:        0.1
Release:        2%{?dist}
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

find %{buildroot}%{gkthemedir} -type d -name '.xvpics' -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -type d -print0 | xargs -0 chmod 0755
find %{buildroot}%{gkthemedir} -type f -print0 | xargs -0 chmod 0644

find %{buildroot}%{gkthemedir} -type d -name 'CVS' -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -name '*~' -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -name '*.orig' -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -name '*.swp' -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -name '.directory' -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -name '.symlinks' -print0 | xargs -0r rm -rf
find -L %{buildroot}%{gkthemedir} -type l -print0 | xargs -0r rm -rf
find %{buildroot}%{gkthemedir} -type f -size 0 -print0 | xargs -0 rm -f

rm -f %{buildroot}%{gkthemedir}/bk10/gkrellm_convert.txt
rm -f %{buildroot}%{gkthemedir}/twilite/change_colors
rm -f %{buildroot}%{gkthemedir}/LED/Install
rm -f %{buildroot}%{gkthemedir}/BloeStolen/convert

%files
%{gkthemedir}/*

%changelog
* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1-2
- rebuilt

* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.1-1
- First spec.
