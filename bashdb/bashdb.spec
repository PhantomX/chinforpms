%bcond_with tests

Name:           bashdb
Summary:        BASH debugger, the BASH symbolic debugger
Version:        4.4_0.94
Release:        2%{?dist}
License:        GPLv2+
URL:            http://bashdb.sourceforge.net/

%global rversion %(c=%{version}; echo ${c//_/-})
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{rversion}.tar.bz2

BuildArch:      noarch

BuildRequires:  bash >= 4.4
BuildRequires:  gcc
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires:       bash >= 4.4

Obsoletes:      emacs-bashdb < %{version}
Obsoletes:      emacs-bashdb-el < %{version}

%description
The Bash Debugger Project is a source-code debugger for bash,
which follows the gdb command syntax. 
The purpose of the BASH debugger is to check
what is going on “inside” a bash script, while it executes:
    * Start a script, specifying conditions that might affect its behavior.
    * Stop a script at certain conditions (break points).
    * Examine the state of a script.
    * Experiment, by changing variable values on the fly.
The 4.0 series is a complete rewrite of the previous series.
Bashdb can be used with ddd: ddd --debugger %{_bindir}/%{name} <script-name>.

%prep
%setup -q -n %{name}-%{rversion}

%build
%configure
%make_build

%install
%make_install INSTALL="install -p"

rm -f "%{buildroot}%{_infodir}/dir"

%if %{with tests}
%check
make check
%endif

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%postun
if [ "$1" = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files
%license COPYING
%doc doc/*.html AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_infodir}/%{name}.info*

%changelog
* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.4_0.94-2
- BR: gcc

* Mon Oct 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 4.4_0.94-1
- 4.4-0.94

* Thu Mar 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 4.4_0.92-1
- 4.4-0.92

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3_0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3_0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Oct 18 2014 Paulo Roma <roma@lcg.ufrj.br> - 4.3_0.9-1
- Rebuilt for bash 4.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2_0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2_0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2_0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Paulo Roma <roma@lcg.ufrj.br> 4.2_0.8-1
- Updated to 4.2-0.8

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2_0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 29 2011 Paulo Roma <roma@lcg.ufrj.br> 4.2_0.7-1
- Updated to 4.2-0.7

* Sun Mar 06 2011 Paulo Roma <roma@lcg.ufrj.br> 4.2_0.6-1
- Updated to 4.2-0.6
- Emacs lisp code has been removed upstream.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1_0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 Paulo Roma <roma@lcg.ufrj.br> 4.1_0.4-1
- Updated to 4.1-0.4

* Sun Mar 14 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.0_0.4-3
- Update package to comply with emacs add-on packaging guidelines
- Split out separate Elisp source file package

* Sun Dec 27 2009 Paulo Roma <roma@lcg.ufrj.br> 4.0_0.4-2
- Updated to 4.0-0.4

* Fri Apr 10 2009 Paulo Roma <roma@lcg.ufrj.br> 4.0_0.3-2
- Updated to 4.0-0.3 for supporting bash 4.0
- Added building option "with tests".

* Wed Feb 25 2009 Paulo Roma <roma@lcg.ufrj.br> 4.0_0.2-1
- Completely rewritten for Fedora.

* Tue Nov 18 2008 Manfred Tremmel <Manfred.Tremmel@iiv.de>
- update to 4.0-0.2

