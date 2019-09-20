%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global version 6.2.3
%global pkgrel 1

# rcrev predates betarev
%global rcrev 0
%global betarev 0

%if 0%{?rcrev} || 0%{?betarev}
  %if 0%{?rcrev}
    %global pretype rc
    %global prerev %{rcrev}
  %else
    %global pretype beta
    %global prerev %{betarev}
  %endif
  %if %{prerev} != 1
    %global presplit .
  %else
    %undefine prerev
  %endif
  %global prestring %{pretype}%{?presplit}%{?prerev}
  %global pretagtarball _%{prestring}
  %global pretagurl -%{prestring}
%endif

Name:           powershell
Version:        %{version}
Release:        1%{?pretag:.%{prestring}}%{?dist}
Summary:        Automation and configuration management platform

License:        MIT
URL:            https://microsoft.com/powershell
Source0:        https://github.com/PowerShell/PowerShell/releases/download/v%{version}%{?pretagurl}/powershell-%{version}%{?pretagtarball}-%{pkgrel}.rhel.7.%{_arch}.rpm
Source1:        https://github.com/PowerShell/PowerShell/raw/master/LICENSE.txt

ExclusiveArch:  x86_64

BuildRequires:  chrpath
Requires:       compat-openssl10%{?_isa}
Requires:       krb5-libs%{?_isa}
Requires:       libcurl%{?_isa}
Requires:       libstdc++%{?_isa}
Requires:       libunwind%{?_isa}
Requires:       libuuid%{?_isa}
Requires:       lttng-ust%{?_isa}
Requires:       pam%{?_isa}
Requires:       zlib%{?_isa}

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libssl.so.1.0.0
%global __requires_exclude %__requires_exclude|^libcrypto.so.1.0.0
%global __requires_exclude %__requires_exclude|^lib.*.so

%description
PowerShell is an automation and configuration management platform.
It consists of a cross-platform command-line shell and associated
scripting language

%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp %{S:1} .

gunzip usr/local/share/man/man1/*.1.gz

%build

%install
mkdir -p %{buildroot}/%{_libdir}/%{name}
mv opt/microsoft/%{name}/*/* %{buildroot}%{_libdir}/%{name}/

chmod +x %{buildroot}%{_libdir}/%{name}/*.so

chrpath --delete %{buildroot}%{_libdir}/%{name}/pwsh
chrpath --delete %{buildroot}%{_libdir}/%{name}/createdump
chrpath --delete %{buildroot}%{_libdir}/%{name}/libmi.so
chrpath --delete %{buildroot}%{_libdir}/%{name}/libmscordbi.so
chrpath --delete %{buildroot}%{_libdir}/%{name}/libpsrpclient.so
chrpath --delete %{buildroot}%{_libdir}/%{name}/libsosplugin.so
chrpath --delete %{buildroot}%{_libdir}/%{name}/libsos.so

ln -sf ../libcrypto.so.10 %{buildroot}%{_libdir}/%{name}/libcrypto.so.1.0.0
ln -sf ../libssl.so.10 %{buildroot}%{_libdir}/%{name}/libssl.so.1.0.0

rm -f %{buildroot}%{_libdir}/%{name}/DELETE_ME_TO_DISABLE_CONSOLEHOST_TELEMETRY

mkdir -p %{buildroot}/%{_mandir}/man1
mv usr/local/share/man/man1/*.1 %{buildroot}%{_mandir}/man1/

# No point use script to support multilib
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/pwsh <<'EOF'
#!/usr/bin/sh
LD_LIBRARY_PATH="%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{_libdir}/%{name}/pwsh "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/pwsh


%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/pwsh" > %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/pwsh$" %{_sysconfdir}/shells || echo "%{_bindir}/pwsh" >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/pwsh$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/pwsh$!d' %{_sysconfdir}/shells
fi

%files
%license LICENSE.txt
%{_bindir}/pwsh
%{_libdir}/%{name}/
%{_mandir}/man1/*.1*


%changelog
* Thu Sep 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 6.2.3-1
- 6.2.3

* Wed May 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 6.2.1-1
- 6.2.1

* Sat Mar 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 6.2.0-1
- 6.2.0

* Tue Dec 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 6.1.1-1
- 6.1.1

* Thu Sep 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 6.1.0-1
- 6.1.0

* Fri Jul 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 6.0.3-1
- 6.0.3
- Do not add /bin/pwsh to shells file

* Thu Mar 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 6.0.1-1
- 6.0.1
- Fix post scriptlet

* Wed Jan 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 6.0.0-0.1.rc.2
- Initial spec
