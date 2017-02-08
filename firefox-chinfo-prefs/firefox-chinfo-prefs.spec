Name:           firefox-chinfo-prefs
Version:        20170130
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
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/firefox/pref
install -pm0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/firefox/pref/chinfo.js


%files
%config(noreplace) %{_sysconfdir}/firefox/pref/chinfo.js

%changelog
* Tue Feb  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170130-1
- Initial spec
