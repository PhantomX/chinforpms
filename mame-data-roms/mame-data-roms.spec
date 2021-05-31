# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

Name:           mame-data-roms
Version:        1
Release:        1%{?dist}
Summary:        Free no-commercial use and non redistributable roms for mame

License:        Free for no-commercial use and non redistributable
URL:            https://www.mamedev.org/roms

# Distributable ROM images (non-commercial use)
Source0:        README.roms
Source1:        %{url}/alienar/alienar.zip
Source2:        %{url}/carpolo/carpolo.zip
Source3:        %{url}/crash/crash.zip
Source4:        %{url}/circus/circus.zip
Source5:        %{url}/fax/fax.zip
Source6:        %{url}/fireone/fireone.zip
Source7:        %{url}/gridlee/gridlee.zip
Source8:        %{url}/hardhat/hardhat.zip
Source9:        %{url}/looping/looping.zip
Source10:       %{url}/ripcord/ripcord.zip
Source11:       %{url}/robby/robby.zip
Source12:       %{url}/robotbwl/robotbwl.zip
Source13:       %{url}/sidetrac/sidetrac.zip
Source14:       %{url}/spectar/spectar.zip
Source15:       %{url}/starfire/starfire.zip
Source16:       %{url}/supertnk/supertnk.zip
Source17:       %{url}/targ/targ.zip
Source18:       %{url}/teetert/teetert.zip
Source19:       %{url}/topgunnr/topgunnr.zip
Source20:       %{url}/victory/victory.zip
%global romfiles %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20}

BuildArch:      noarch

Requires:       mame-data-extras >= 0.232

%description
%{summary}.


%prep
%autosetup -cT

cp -p %{S:0} README

%build


%install
mkdir -p %{buildroot}%{_datadir}/mame/roms
install -pm0644 %{romfiles} \
  %{buildroot}%{_datadir}/mame/roms/

%files
%doc README
%{_datadir}/mame/roms/*.zip


%changelog
* Sat May 29 2021 - 1-1
- Initial spec
