%global debug_package %{nil}

%ifarch x86_64
%global mark64 ()(64bit)
%else
%global mark64 %{nil}
%endif

Name:           vmware-common
Version:        1
Release:        1%{?dist}
Summary:        Shared files for VMware services

License:        VMware

URL:            https://support.broadcom.com/
Source0:        usbarb.rules
Source1:        https://docs.broadcom.com/doc/end-user-agreement-english#/end-user-agreement-english.pdf

%description
%{summary}.


%prep
%autosetup -c -T

cp %{S:0} .
cp %{S:1} .

cat > bootstrap <<EOF
PREFIX="%{_prefix}"
BINDIR="%{_bindir}"
SBINDIR="%{_sbindir}"
LIBDIR="%{_libdir}"
DATADIR="%{_datadir}"
SYSCONFDIR="%{_sysconfdir}"
DOCDIR="%{_docdir}"
MANDIR="%{_mandir}"
INCLUDEDIR="%{_includedir}"
EOF


cat > config <<'EOF'
.encoding = "UTF-8"
installerDefaults.autoSoftwareUpdateEnabled = "no"
installerDefaults.dataCollectionEnabled = "no"
installerDefaults.componentDownloadEnabled = "no"
installerDefaults.transferVersion = "1"
libdir = "%{_libdir}/vmware"
bindir = "%{_bindir}"
gksu.rootMethod = "sudo"
EOF


%build


%install
mkdir -p %{buildroot}%{_sysconfdir}/vmware
install -pm0644 bootstrap %{buildroot}%{_sysconfdir}/vmware/
install -pm0644 config %{buildroot}%{_sysconfdir}/vmware/

install -pm0644 usbarb.rules %{buildroot}%{_sysconfdir}/vmware/


%files
%license end-user-agreement-english.pdf
%dir %{_sysconfdir}/vmware
%config %{_sysconfdir}/vmware/bootstrap
%config %{_sysconfdir}/vmware/config
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/vmware/usbarb.rules


%changelog
* Tue Oct 01 2024 - 1-1
- Initial spec
