%bcond_without check

# https://github.com/dim13/otpauth

%global commit 948f0dbb5b7191fc9825c657d6aadc4176b08531
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240706
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global goipath         github.com/dim13/otpauth
Version:                0.5.2

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
Release:        2%{?dist}
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
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.2-1.20240314git36a9db9
- 0.5.2

* Mon Dec 11 2023 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-2.20231208git6a02ca0
- Initial spec
