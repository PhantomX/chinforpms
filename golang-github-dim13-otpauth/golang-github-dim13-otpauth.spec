%bcond check 1

# https://github.com/dim13/otpauth

%bcond snapshot 0

%if %{with snapshot}
%global commit 62ea28997756a49c34dade271df5beb2a9ccd2fb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250418

%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global goipath         github.com/dim13/otpauth
Version:                0.6.0

%gometa

%global common_description %{expand:
Convert Google Authenticator otpauth-migration://offline?data=... transfer links
to plain otpauth links.}

%global golicenses    LICENSE
%global godocs        *.md

%global godevelheader %{expand:
# The devel package will usually benefit from corresponding project binaries.
Requires:  %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
}

Name:           %{goname}
Release:        1%{?dist}
Summary:        Google Authenticator migration decoder 
License:        ISC
URL:            %{gourl}
Source:         %{gosource}

%description
%{common_description}

%gopkg

%prep
%goprep

%generate_buildrequires
%go_generate_buildrequires

%build
%gobuild -o %{gobuilddir}/bin/otpauth %{goipath}


%install
%gopkginstall
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/


%if %{with check}
%check
%gocheck
%endif

%files
%license %{golicenses}
%doc %{godocs}
%{_bindir}/*

%gopkgfiles

%changelog
* Fri Aug 01 2025 Phantom X <megaphantomx at hotmail dot com> - 0.6.0-1
- 0.6.0

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 0.5.4-1
- 0.5.4

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.2-1.20240314git36a9db9
- 0.5.2

* Mon Dec 11 2023 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-2.20231208git6a02ca0
- Initial spec
