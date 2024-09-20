Name:           glibc-langpack-pt_BR_iso8601
Version:        2.40
Release:        1%{?dist}
Summary:        Locale data for Brazilian Portuguese, with iso8601 dates

# From locale file header:
# This file is part of the GNU C Library and contains locale data.
# The Free Software Foundation does not claim any copyright interest
# in the locale data contained in this file.  The foregoing does not
# affect the license of the GNU C Library as a whole.  It does not
# exempt you from the conditions of the license if your use would
# otherwise be governed by that license.
License:        LicenseRef-Fedora-Public-Domain
URL:            https://github.com/PhantomX/chinforpms

Source0:        README

Patch0:         0001-pt_BR-use-iso8601-date-format.patch

BuildArch:      noarch

BuildRequires:  glibc-locale-source >= %{version}
Requires:       glibc-langpack-pt >= %{version}


%description
The glibc-langpack-pt_BR_iso8601 package includes the basic information required
to support the Brazilian Portuguese language with iso8601 dates in your
applications. This is an addition to the original language.


%prep
%setup -c -T
cp -p %{_datadir}/i18n/locales/pt_BR .

%patch -P 0 -p1

cp -p %{S:0} .


%build


%install
mkdir -p %{buildroot}%{_prefix}/lib/locale
LC_ALL=en_US.UTF-8 localedef --prefix=%{buildroot} \
  -c -i "pt_BR" -f ISO-8859-1 --no-archive 'pt_BR@iso8601'
LC_ALL=en_US.UTF-8 localedef --prefix=%{buildroot} \
  -c -i "pt_BR" -f UTF-8 --no-archive 'pt_BR.utf8@iso8601'


%files
%doc README
%{_prefix}/lib/locale/pt_BR*iso8601


%changelog
* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 2.40-1
- 2.40

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 2.39-1
- 2.39

* Wed Jun 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.31-1
- Initial spec
