%global commit c2f0f3eaf4ae95e55a1876b808d3c0b49fa61dbe
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250102
%bcond_without snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname SDL_GameControllerDB

Name:           sdl_gamecontrollerdb
Version:        1473
Release:        1%{?dist}
Summary:        A database of game controller mappings

License:        Zlib AND MIT
URL:            https://github.com/gabomdq/%{pkgname}
%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-Add-Xbox-360-Controller-for-Windows-GUID.patch

BuildRequires:  python3-devel

Provides:       %{pkgname} = %{version}-%{release}


%description
SDL_GameControllerDB is a community source database of game controller mappings
to be used with SDL2 Game Controller functionality.

%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

%py3_shebang_fix duplicates.py

%build

%install
mkdir -p %{buildroot}%{_datadir}/%{pkgname}
install -pm0644 gamecontrollerdb.txt %{buildroot}%{_datadir}/%{pkgname}/


%files
%license LICENSE
%doc README.md duplicates.py
%{_datadir}/%{pkgname}/gamecontrollerdb.txt


%changelog
* Sat Nov 23 2024 Phantom X <megaphantomx at hotmail dot com> - 1458-1.20241122gitf3a69a9
- Use commit number as version

* Mon Feb 12 2024 Phantom X <megaphantomx at hotmail dot com> - 0-63.20240210gitae51c99
- Add another extra GUID

* Fri Dec 23 2022 Phantom X <megaphantomx at hotmail dot com> - 0-51.20221221gitb717695
- Add extra GUID patch

* Wed Jul 06 2022 Phantom X <megaphantomx at hotmail dot com> - 0-47.20220706git23501da
- Last database

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 0-46.20220425git82de4c7
- Bump

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0-45.20220329git2ab959b
- Bump

* Tue Mar 08 2022 Phantom X <megaphantomx at hotmail dot com> - 0-44.20220305git4607c62
- Last update

* Tue Feb 15 2022 Phantom X <megaphantomx at hotmail dot com> - 0-43.20220215gite30a56f
- Last snapshot

* Sun Nov 14 2021 Phantom X <megaphantomx at hotmail dot com> - 0-42.20211112git1fb968e
- 20211112git1fb968e

* Fri Sep 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0-41.20210917gita920ab8
- Bump

* Thu Sep 02 2021 Phantom X <megaphantomx at hotmail dot com> - 0-40.20210902gitcb4efbb
- Bump

* Sat Aug 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0-39.20210817git538413d
- Update

* Mon Aug 02 2021 Phantom X <megaphantomx at hotmail dot com> - 0-38.20210731git2927014
- Bump

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 0-37.20210709git241fed0
- Last one

* Sat Jul 03 2021 Phantom X <megaphantomx at hotmail dot com> - 0-36.20210702gitf500243
- Last update

* Tue May 25 2021 Phantom X <megaphantomx at hotmail dot com> - 0-35.20210519gitfbf672e
- Update

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0-34.20210418git74e31d7
- Bump

* Thu Apr 08 2021 Phantom X <megaphantomx at hotmail dot com> - 0-33.20210406git01dce71
- Bump

* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 0-32.20210323gite6cf731
- Update

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0-31.20210311git8ce603d
- Latest

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0-30.20210228git160dfcf
- Bump

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0-29.20210208git9de9aef
- Update

* Thu Feb 04 2021 Phantom X <megaphantomx at hotmail dot com> - 0-28.20210203git9107014
- Bump

* Sat Jan 16 2021 Phantom X <megaphantomx at hotmail dot com> - 0-27.20210113gita4b85ef
- Bump

* Thu Jan 07 2021 Phantom X <megaphantomx at hotmail dot com> - 0-26.20210104git70817aa
- Bump

* Sun Nov 29 2020 Phantom X <megaphantomx at hotmail dot com> - 0-25.20201126gitf12a0da
- Bump

* Fri Nov 13 2020 Phantom X <megaphantomx at hotmail dot com> - 0-24.20201103git418d293
- Bump

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 0-23.20201027gitae28d29
- New snapshot

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0-22.20201021gita0fbff6
- Update

* Sat Sep 12 2020 Phantom X <megaphantomx at hotmail dot com> - 0-21.20200911gitbdd8118
- Bump

* Mon Aug 31 2020 Phantom X <megaphantomx at hotmail dot com> - 0-20.20200812git9e4cff6
- New snapshot

* Sun Jul 12 2020 Phantom X <megaphantomx at hotmail dot com> - 0-19.20200703git29e8f04
- Bump

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 0-18.20200619git4350670
- New snapshot

* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-17.20200516git15998df
- Bump

* Mon Apr 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-16.20200408gitd2bb9a5
- New snapshot

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-15.20200315gitca01c94
- New snapshot from new clone

* Wed Feb 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-14.20200219gitb01222f
- Bump

* Sun Feb 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-13.20200118gitfed28b1
- New snapshot

* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-12.20191015git8ff133d
- New snapshot

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-11.20190802gitef8542c
- New snapshot

* Sun Jul 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-10.20190719gitdca1a62
- New snapshot

* Sun Jun 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-9.20190514gitd57f564
- New snapshot

* Mon May 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-8.20190501git935f886
- New snapshot

* Thu Apr 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-7.20190402gite411d95
- New snapshot

* Sat Mar 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-6.20190307git3182bfa
- New snapshot

* Fri Feb 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-5.20190131git40e3a34
- New snapshot

* Wed Dec 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-4.20181201git04ebce5
- New snapshot
- Install check script

* Thu Nov 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20181120git89224d5
- New snapshot

* Thu Sep 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20180925git2c1b295
- New snapshot

* Fri Sep 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20180818git276431b
- Initial spec
