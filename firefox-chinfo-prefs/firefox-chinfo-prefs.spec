Name:           firefox-chinfo-prefs
Version:        20170414
Release:        1%{?dist}
Summary:        Chinforinfula default preferences for Firefox

License:        Public Domain
URL:            https://github.com/PhantomX
Source0:        %{name}.js

BuildArch:      noarch

Requires:       firefox

%description
%{summary}.

%prep

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/firefox/pref
install -pm0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/firefox/pref/chinfo.js


%files
%config(noreplace) %{_sysconfdir}/firefox/pref/chinfo.js

%changelog
* Fri Apr 14 2017 Phantom X - 20170414-1
- 20170414

* Thu Mar 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170309-1
- media.autoplay.enabled -> false

* Tue Feb  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170130-1
- Initial spec
