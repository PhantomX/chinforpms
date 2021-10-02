# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global progdir %{_libdir}/%{name}
%global vermajor %%(echo %{version} | cut -d. -f1)

Name:           teamviewer
Version:        15.22.3
Release:        1%{?dist}
Summary:        Remote control and meeting solution

License:        Proprietary; includes Free Software components

URL:            http://www.teamviewer.com
Source0:        https://download.teamviewer.com/download/linux/teamviewer.x86_64.rpm#/%{name}-%{version}.x86_64.rpm
Source1:        tvw_aux
Source2:        tvw_daemon
Source3:        tvw_exec
Source4:        tvw_extra
Source5:        tvw_main
Source6:        tvw_profile
Source7:        %{name}d.te

# Other architectures can be supported, but not by this spec
ExclusiveArch:  x86_64

%{?systemd_requires}
BuildRequires:  systemd
BuildRequires:  desktop-file-utils
BuildRequires:  chrpath
BuildRequires:  checkpolicy
BuildRequires:  policycoreutils
Requires:       hicolor-icon-theme
Requires:       xdg-utils
Requires(post): policycoreutils
Requires(preun): policycoreutils


%description
TeamViewer provides easy, fast and secure remote access and meeting solutions
to Linux, Windows PCs, Apple PCs and various other platforms,
including Android and iPhone.

TeamViewer is free for personal use.
You can use TeamViewer completely free of charge to access your private
computers or to help your friends with their computer problems.

To buy a license for commercial use, please visit http://www.teamviewer.com

This package contains Free Software components.
For details, see %{_licensedir}/%{_name}/license_foss.txt


%prep
%setup -c -T
echo %{vermajor}

RVER="$(rpm -qp --qf %%{version} %{S:0} 2> /dev/null)"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch"
  echo "You have ${RVER} in %{SOURCE0} instead %{version} "
  echo "Edit VERSION variable and try again"
  exit 1
fi

rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp -p %{S:1} %{S:2} %{S:3} %{S:4} %{S:5} %{S:6} %{S:7} .

find opt/%{name}/ -name '*.so*' | xargs chmod +x

chrpath --delete opt/%{name}/tv_bin/TeamViewer

sed \
  -e 's|/var/run|%{_rundir}|g' \
  -e 's|/opt/%{name}/tv_bin|%{progdir}|g' \
  -i opt/%{name}/tv_bin/script/*.{policy,service}

cat > tvw_config <<'EOF'
TV_VERSION='%{version}'
TV_PKGTYPE='RPM'
TV_EDITION='FULL'

TV_USER_CONFIG_SUBPATH='.config/%{name}'
TV_USER_LOCAL_SUBPATH='.local/share/%{name}%{vermajor}'
TV_PROFILE="$HOME/$TV_USER_LOCAL_SUBPATH"
TV_LOG_DIR="$TV_PROFILE/logfiles"
TV_CFG_DIR="$HOME/$TV_USER_CONFIG_SUBPATH"

TV_PIDFILE='%{_rundir}/teamviewerd.pid'
TV_STARTLOG="$TV_LOG_DIR/startup.log"

export PATH=$TV_SCRIPT_DIR:$PATH
export TV_USERHOME=$HOME
EOF


%build
checkmodule -M -m -o %{name}d.mod %{name}d.te
semodule_package -o %{name}d.pp -m %{name}d.mod

%install
mkdir -p %{buildroot}%{progdir}/{resources,script}

for i in TeamViewer* %{name}-config %{name}d ;do
  install -pm0755 opt/%{name}/tv_bin/$i %{buildroot}%{progdir}/
done

install -pm0755 opt/%{name}/tv_bin/resources/*.so \
  %{buildroot}%{progdir}/resources/

for i in config aux daemon exec extra main profile ;do
  install -pm0644 tvw_$i %{buildroot}%{progdir}/script/
done

install -pm0755 opt/%{name}/tv_bin/script/execscript %{buildroot}%{progdir}/script/

install -pm0644 %{name}d.{te,pp} %{buildroot}%{progdir}/script/

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh

TV_BASE_DIR="%{progdir}"
TV_BIN_DIR="${TV_BASE_DIR}"
TV_SCRIPT_DIR="${TV_BIN_DIR}/script"

source "${TV_SCRIPT_DIR}/tvw_main"

Main "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}


mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}%{vermajor}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

ln -sf ../../..%{_sysconfdir}/%{name} %{buildroot}%{progdir}/config
ln -sf ../../..%{_localstatedir}/log/%{name}%{vermajor} %{buildroot}%{progdir}/logfiles

touch %{buildroot}%{_localstatedir}/lib/%{name}/rolloutfile.tv13
ln -sf ../../..%{_localstatedir}/lib/%{name}/rolloutfile.tv13 %{buildroot}%{progdir}/rolloutfile.tv13

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 opt/%{name}/tv_bin/script/%{name}d.service %{buildroot}%{_unitdir}/

mkdir -p %{buildroot}%{_datadir}/dbus-1/services
install -pm0644 opt/%{name}/tv_bin/script/com.%{name}.TeamViewer*.service \
  %{buildroot}%{_datadir}/dbus-1/services/

mkdir -p %{buildroot}%{_datadir}/polkit-1/actions
install -pm0644 opt/%{name}/tv_bin/script/com.%{name}.TeamViewer.policy \
  %{buildroot}%{_datadir}/polkit-1/actions/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key="Encoding" \
  --set-icon="TeamViewer" \
  --set-key="Exec" \
  --set-value="%{name} %U" \
 opt/%{name}/tv_bin/desktop/com.%{name}.TeamViewer.desktop

for res in 16 24 32 48 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 opt/%{name}/tv_bin/desktop/%{name}_${res}.png ${dir}/TeamViewer.png
done


%preun
%systemd_preun %{name}d.service
#/usr/sbin/semodule --remove %%{name}d >/dev/null 2>&1 || :

%post
/usr/sbin/semodule --install %{progdir}/script/%{name}d.pp >/dev/null 2>&1 || :
%systemd_post %{name}d.service

%postun
%systemd_postun %{name}d.service


%files
%license opt/%{name}/doc/*
%{_bindir}/%{name}
%{progdir}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*x*/apps/*.png
%{_unitdir}/%{name}d.service
%dir %{_sysconfdir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_datadir}/polkit-1/actions/*.policy
%dir %{_localstatedir}/log/%{name}%{vermajor}
%ghost %{_localstatedir}/lib/%{name}/rolloutfile.tv13


%changelog
* Sat Oct 02 2021 - 15.22.3-1
- 15.22.3

* Mon Dec 14 2020 Phantom X - 15.12.4-1
- 15.12.4

* Tue Oct 06 2020 - 15.10.5-1
- Initial spec

