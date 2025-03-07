Name:           firefox-chinfo-prefs
Version:        20250226
Release:        1%{?dist}
Summary:        Chinforinfula default preferences for Firefox

License:        LicenseRef-Fedora-Public-Domain
URL:            https://github.com/PhantomX
Source0:        %{name}.js

BuildArch:      noarch

Requires:       firefox


%description
%{summary}.


%prep

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/firefox/defaults/pref
install -pm0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/firefox/defaults/pref/chinfo.js


%files
%config(noreplace) %{_sysconfdir}/firefox/defaults/pref/chinfo.js


%changelog
* Wed Feb 26 2025 Phantom X <megaphantomx at hotmail dot com> - 20250226-1
- 20250226

* Wed Jan 08 2025 Phantom X <megaphantomx at hotmail dot com> - 20250108-1
- 20250108

* Fri Oct 04 2024 Phantom X <megaphantomx at hotmail dot com> - 20241004-1
- 20241004

* Mon Jul 15 2024 Phantom X <megaphantomx at hotmail dot com> - 20240715-1
- 20240715

* Mon Dec 11 2023 Phantom X <megaphantomx at hotmail dot com> - 20231210-1
- 20231210

* Fri May 26 2023 Phantom X <megaphantomx at hotmail dot com> - 20230526-1
- 20230526

* Wed Mar 22 2023 Phantom X <megaphantomx at hotmail dot com> - 20221207-2
- Move to new directory

* Wed Dec 07 2022 Phantom X <megaphantomx at hotmail dot com> - 20221207-1
- 20221207
- Removed waterfox

* Fri Oct 21 2022 Phantom X <megaphantomx at hotmail dot com> - 20221021-1
- 20221021

* Mon Jun 13 2022 Phantom X <megaphantomx at hotmail dot com> - 20220613-1
- 20220613

* Wed May 04 2022 Phantom X <megaphantomx at hotmail dot com> - 20220504-1
- 20220504

* Sat Nov 06 2021 Phantom X <megaphantomx at hotmail dot com> - 20211104-1
- 20211104

* Fri Jul 16 2021 Phantom X <megaphantomx at hotmail dot com> - 20210716-1
- 20210716

* Thu Jun 10 2021 Phantom X <megaphantomx at hotmail dot com> - 20210610-1
- 20210610

* Tue Mar 16 2021 Phantom X <megaphantomx at hotmail dot com> - 20210315-1
- 20210315

* Sat Jan 30 2021 Phantom X <megaphantomx at hotmail dot com> - 20210129-1
- 20210129

* Thu Oct 22 2020 Phantom X <megaphantomx at hotmail dot com> - 20201022-1
- 20201022

* Mon Jul 06 2020 Phantom X <megaphantomx at hotmail dot com> - 20200706-1
- 20200706

* Sat Apr 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 20200411-1
- 20200411

* Thu Mar 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 20200326-1
- 20200326

* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 20191216-1
- 20191216

* Mon Dec 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 20191209-1
- 20191209

* Wed Dec 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 20191204-1
- 20191204

* Mon Nov 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 20191118-1
- 20191118

* Thu Nov 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 20191114-1
- 20191114

* Tue Nov 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 20191112-1
- 20191112

* Mon Oct 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 20191013-1
- 20191013

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190522-1
- 20190522

* Wed Jan 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 20190116-1
- 20190116

* Thu Dec 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 20181213-1
- 20181213

* Tue Nov 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 20181106-1
- 20181106

* Thu Sep 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180906-1
- 20180906

* Wed Jun 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180620-1
- 20180620
- Provides: waterfox-chinfo-prefs

* Wed May 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180516-1
- 20180516

* Mon May 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 20180514-1
- 20180514

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
