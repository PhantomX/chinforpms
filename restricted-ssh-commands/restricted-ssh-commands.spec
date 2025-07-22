%bcond check 1

Name:           restricted-ssh-commands
Version:        0.4
Release:        1%{?dist}
Summary:        Restrict SSH users to a predefined set of commands

License:        MIT
URL:            https://github.com/bdrung/restricted-ssh-commands

Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  perl-podlators
%if %{with check}
BuildRequires:  shunit2
%endif


%description
%{name} is intended to be called by SSH to restrict a user to only run
specific commands. A list of allowed regular expressions can be
configured in F</etc/restricted-ssh-commands/>. The requested command
has to match at least one regular expression. Otherwise it will be
rejected.


%prep
%autosetup

sed \
  -e 's|$(PREFIX)/lib/|%{_libexecdir}/|' \
  -e 's|$(PREFIX)/share/man/|%{_mandir}/|' \
  -i Makefile

sed -e 's|shunit2|%{_datadir}/shunit2/shunit2|' -i test-%{name}


%build
%make_build


%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/%{name}


%check
%if %{with check}
make check
%endif


%files
%license LICENSE
%doc NEWS
%{_libexecdir}/%{name}
%{_mandir}/man1/%{name}.1*
%dir %{_sysconfdir}/%{name}


%changelog
* Wed Nov 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4-1
- Initial spec
