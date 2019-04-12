%global with_xpi 1

%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id \{dc572301-7619-498c-a57d-39143191b318\}

%global inst_path %{_waterfox_extdir}/%{extension_id}

%global pkgname tab_mix_plus

Name:           waterfox-tabmixplus
Version:        0.5.7.0
Release:        1%{?dist}
Summary:        Enhances Waterfox tab browsing abilities

License:        MPLv1.1
URL:            http://tabmixplus.org/

%if 0%{?with_xpi}
Source0:        https://bitbucket.org/onemen/tabmixplus/downloads/tab_mix_plus-%{version}-fx.xpi
%else
Source0:        https://bitbucket.org/onemen/tabmixplus/get/%{version}.tar.bz2#/%{pkgname}-%{version}.tar.bz2
%endif
Source1:        license.txt
Source2:        %{name}.metainfo.xml


BuildArch:      noarch

BuildRequires:  libappstream-glib
Requires:       waterfox-filesystem

%description
Tab Mix Plus is a extension for the Waterfox browser that enhances tab
browsing abilities. It includes such features as duplicating tabs,
controlling tab focus, tab clicking options, undo closed tabs and
windows, plus much more. It also includes a Session Manager with crash
recovery that can save and restore combinations of opened tabs and
windows.


%prep
%if 0%{?with_xpi}
%autosetup -c %{pkgname}-%{version}
%else
%autosetup -c %{pkgname}-%{version}

find -type f -name '.*' -delete -print
mv onemen-tabmixplus*/* .
rmdir onemen-tabmixplus*
rm -f update.json
cp -p %{S:1} .

%endif


%build


%install
# install into _waterfox_extdir

mkdir -p %{buildroot}%{inst_path}

for f in $(find . -print | sed -e '/\.\/$/d') ; do
  if [ -d ${f} ] ; then
    install -dm 755 %{buildroot}%{inst_path}/${f}
  else
    install -pm 644 ${f} %{buildroot}%{inst_path}/${f}
  fi
done

# install MetaInfo file for waterfox, etc
install -Dpm644 %{S:2} %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files
%license license.txt
%{inst_path}
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Thu Apr 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.5.7.0-1
- 0.5.7.0

* Tue Feb 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.5.6.0-1
- Initial spec
