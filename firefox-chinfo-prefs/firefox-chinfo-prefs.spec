Name:           firefox-chinfo-prefs
Version:        20180419
Release:        1%{?dist}
Summary:        Chinforinfula default preferences for Firefox

License:        Public Domain
URL:            https://github.com/PhantomX
Source0:        %{name}.js

BuildArch:      noarch

%description
%{summary}.

%prep

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/firefox/pref
install -pm0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/firefox/pref/chinfo.js

mkdir -p %{buildroot}%{_sysconfdir}/waterfox/pref
install -pm0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/waterfox/pref/chinfo.js

%files
%config(noreplace) %{_sysconfdir}/firefox/pref/chinfo.js
%config(noreplace) %{_sysconfdir}/waterfox/pref/chinfo.js

%changelog
* Thu Apr 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180419-1
- 20180419

* Thu Mar 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180315-1
- 20180315

* Thu Jan 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180104-1
- 20180104

* Wed Jan 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180103-1
- 20180103

* Mon Dec 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 20171218-1
- 20171218

* Thu Dec 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 20171121-2
- Added waterfox
- Removed R: firefox

* Fri Nov 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 20171117-1
- 20171117

* Sun Aug 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170813-1
- 20170813

* Tue Jun 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170627-1
- 20170627

* Fri Jun 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170623-1
- 20170623

* Fri Apr 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170414-1
- 20170414

* Thu Mar 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170309-1
- media.autoplay.enabled -> false

* Tue Feb  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 20170130-1
- Initial spec
