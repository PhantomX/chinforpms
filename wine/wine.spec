%global commit 1a0470443d12f6fc4c241a93af5bc34aa03b34b3
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200910
%global with_snapshot 0

# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%ifarch %{ix86} x86_64
%global wine_mingw 1
# Package mingw files with debuginfo
%global with_debug 0
%endif
%global no64bit   0
%global winegecko 2.47.1
%global winemono  5.1.0
%global _default_patch_fuzz 2

%global libext .so
%if 0%{?wine_mingw}
%undefine _annotated_build
%global libext %{nil}
%endif

%global wineacm acm%{?libext}
%global wineax ax%{?libext}
%global winecom com%{?libext}
%global winecpl cpl%{?libext}
%global winedll dll%{?libext}
%global winedll16 dll16%{?libext}
%global winedrv drv%{?libext}
%global winedrv16 drv16%{?libext}
%global wineexe exe%{?libext}
%global wineexe16 exe16%{?libext}
%global winemod16 mod16%{?libext}
%global wineocx ocx%{?libext}
%global winesys sys%{?libext}
%global winetlb tlb%{?libext}
%global winevxd vxd%{?libext}

# build with staging-patches, see:  https://wine-staging.com/
# 1 to enable; 0 to disable.
%global wine_staging 1
%global wine_stagingver 5.17
%if 0%(echo %{wine_stagingver} | grep -q \\. ; echo $?) == 0
%global strel v
%global stpkgver %{wine_stagingver}
%else
%global stpkgver %(c=%{wine_stagingver}; echo ${c:0:7})
%endif
%global ge_id ae15b580525714b76de074c2aee30f535e15a349
%global ge_url https://github.com/GloriousEggroll/proton-ge-custom/raw/%{ge_id}/patches

%global tkg_id 2e2d1ad4c821ca63f6eaea7e6dfa6a51d71bac6b
%global tkg_url https://github.com/Frogging-Family/wine-tkg-git/raw/%{tkg_id}/wine-tkg-git/wine-tkg-patches
%global tkg_cid 253417450e507f49790cbea17f077d497c1e45a0
%global tkg_curl https://github.com/Frogging-Family/community-patches/raw/%{tkg_cid}/wine-tkg-git

%global gtk3 0
# proton FS hack (wine virtual desktop with DXVK is not working well)
%global fshack 0
%global mfplatwip 0
%global vulkanup 1
# Broken
%global pba 0

%global fsync_spincounts 1

%global wine_staging_opts %{?wine_staging_opts} -W ntdll-SystemRoot_Symlink
%if 0%{?fshack}
%global wine_staging_opts %{?wine_staging_opts} -W winex11-WM_WINDOWPOSCHANGING -W winex11-_NET_ACTIVE_WINDOW
%global wine_staging_opts %{?wine_staging_opts} -W winex11.drv-mouse-coorrds -W winex11-MWM_Decorations
%global wine_staging_opts %{?wine_staging_opts} -W user32-rawinput-mouse -W user32-rawinput-mouse-experimental -W user32-rawinput-hid
%endif
%if 0%{?mfplatwip}
%global wine_staging_opts %{?wine_staging_opts} -W mfplat-streaming-support
%endif

%global whq_url  https://source.winehq.org/git/wine.git/patch
%global whqs_url  https://source.winehq.org/patches/data
%global valve_url https://github.com/ValveSoftware/wine

%global staging_banner Chinforpms Staging

# binfmt macros for RHEL
%if 0%{?rhel} == 7
%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt  %{?*} >/dev/null 2>&1 || : \
%{nil}
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global vermajor %(echo %{ver} | cut -d. -f1)
%if "%(echo %{ver} | cut -d. -f2 | cut -d- -f1 )" == "0"
%global verx 1
%endif

Name:           wine
# If rc, use "~" instead "-", as ~rc1
Version:        5.17
Release:        100%{?gver}%{?dist}
Summary:        A compatibility layer for windows applications

Epoch:          1

License:        LGPLv2+
URL:            http://www.winehq.org/

%if 0%{?with_snapshot}
Source0:        https://github.com/wine-mirror/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz
Source10:       https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz.sign
%endif

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source4:        wine-32.conf
Source5:        wine-64.conf
Source6:        wine-README-chinforpms
Source7:        wine-README-chinforpms-fshack

# desktop files
Source100:      wine-notepad.desktop
Source101:      wine-regedit.desktop
Source102:      wine-uninstaller.desktop
Source103:      wine-winecfg.desktop
Source104:      wine-winefile.desktop
Source105:      wine-winemine.desktop
Source106:      wine-winhelp.desktop
Source107:      wine-wineboot.desktop
Source108:      wine-wordpad.desktop
Source109:      wine-oleview.desktop
Source110:      wine-iexplore.desktop
Source111:      wine-inetcpl.desktop
Source112:      wine-joycpl.desktop
Source113:      wine-taskmgr.desktop

# AppData files
Source150:      wine.appdata.xml

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

# mime types
Source300:      wine-mime-msi.desktop


# smooth tahoma (#693180)
# disable embedded bitmaps
Source501:      wine-tahoma.conf
# and provide a readme
Source502:      wine-README-tahoma

Patch511:       wine-cjk.patch
Patch599:       0003-winemenubuilder-silence-an-err.patch

# build fixes

# wine bugs/upstream/reverts
#Patch???:      %%{whq_url}/commit#/%%{name}-whq-commit.patch
Patch101:       %{whqs_url}/190297#/%{name}-whq-patch190297.patch

# 7000-/8000-/801-806 - Reverts to unbreak esync/fsync
Patch7000:      %{whq_url}/e854ea34cc481658ec61f4603d0438e075608c98#/%{name}-whq-e854ea3.patch
Patch7001:      %{whq_url}/e6e2f2325a0a4eb14f10dd6df319b068761e9600#/%{name}-whq-e6e2f23.patch
Patch7002:      %{whq_url}/8a63b688ac49f19c259066fd100407edf3747f95#/%{name}-whq-8a63b68.patch
Patch7003:      %{whq_url}/1a743c9af39d0224b65ae504ae7e24d9fad56c2b#/%{name}-whq-1a743c9.patch
Patch7004:      %{whq_url}/01150d7f8d27ad5efdb824da938c4a9fa562a036#/%{name}-whq-01150d7.patch
Patch7005:      %{whq_url}/04f41e87a369828a698f62c32cabad34ed34a3e7#/%{name}-whq-04f41e8.patch
Patch7006:      %{whq_url}/704975f58d7947721f530d202022721c16df466a#/%{name}-whq-704975f.patch
Patch7007:      %{whq_url}/3e9f8c87e5a2acaa80f8bbb1d50fa82147942143#/%{name}-whq-3e9f8c8.patch
Patch7008:      %{whq_url}/b925dd78b813decf386139a15aa7bc6863ee7ae5#/%{name}-whq-b925dd7.patch
Patch7009:      %{whq_url}/c0319e0eabbad87a3e153c23f2461c881153b984#/%{name}-whq-c0319e0.patch
Patch7010:      %{whq_url}/87fa906a84621295a76035d73dd6305c9cd2ea4a#/%{name}-whq-87fa906.patch
Patch7011:      %{whq_url}/ac90898f72b02bbc226a95deb40555c1fb8ac3a3#/%{name}-whq-ac90898.patch
Patch7012:      %{whq_url}/7c32b2dd9368137eca3cf0202360bbe0db62efbf#/%{name}-whq-7c32b2d.patch
Patch7013:      %{whq_url}/c96ef78b6d6d9184d8ec4cd18924a3049d388583#/%{name}-whq-c96ef78.patch
Patch7014:      %{whq_url}/9fe61171e515e7c77720675ecbe69731219b549c#/%{name}-whq-9fe6117.patch
Patch7015:      %{whq_url}/be0eb9c92eb7a4fcd9d0d48568c8ed5e8326ef0b#/%{name}-whq-be0eb9c.patch
Patch7016:      %{whq_url}/35b063a404457fdf956d1913738a3c8a66266cb4#/%{name}-whq-35b063a.patch
Patch7017:      %{whq_url}/f1d40d4824b568389cbc328cebb5734430b52e44#/%{name}-whq-f1d40d4.patch
Patch7018:      %{whq_url}/cd0c5988020acc92ff98260e3304967bf31e4e87#/%{name}-whq-cd0c598.patch
Patch7019:      %{whq_url}/4ffe39573b537d638e4b39c9b5990c6566d62b09#/%{name}-whq-4ffe395.patch
Patch7020:      %{whq_url}/a18444984171ee86503d1250094965fb50a198ee#/%{name}-whq-a184449.patch
Patch7021:      %{whq_url}/39915c9bc42f17619b1d2c46e6b3aea485c471a0#/%{name}-whq-39915c9.patch
Patch7022:      %{whq_url}/efd59e378c2ba8cae98fa664ae98521027e96b81#/%{name}-whq-efd59e3.patch
Patch7023:      %{whq_url}/8b87d6b81408e5d6fe34f9e9fda1df2f4f2e5cd0#/%{name}-whq-8b87d6b.patch
Patch7024:      %{whq_url}/65edacf93484faf1dc3d11e555081d69556ccbc3#/%{name}-whq-65edacf.patch
Patch7025:      %{whq_url}/f1276b25ae72e81cf044134bae92db6ef73be3a1#/%{name}-whq-f1276b2.patch
Patch7026:      %{whq_url}/cdfc45859c299aa629482ee06614c9819346b444#/%{name}-whq-cdfc458.patch
Patch7027:      %{whq_url}/ca3ca7b046ae94a152b1367ca982774345887e55#/%{name}-whq-ca3ca7b.patch
Patch7028:      %{whq_url}/39e7f25e0918d23e5b9ef5fc5049948b6f56525e#/%{name}-whq-39e7f25.patch
Patch7029:      %{whq_url}/33c750f50ff8b6f1eae63140e8287c49a5130a60#/%{name}-whq-33c750f.patch
Patch7030:      %{whq_url}/245efd04e1456a71a6962acbb8ebc279481e9ffa#/%{name}-whq-245efd0.patch
Patch7031:      %{whq_url}/8e5d3042786917c04d3065755d81e7f8a751e529#/%{name}-whq-8e5d304.patch
Patch7032:      %{whq_url}/e561ce4b9259071f79d219dddf62f05cdd8dd07b#/%{name}-whq-e561ce4.patch
Patch7033:      %{whq_url}/95e2d05e5d6b92a2f6b28e00f36064b7bf6b249a#/%{name}-whq-95e2d05.patch
Patch7034:      %{whq_url}/7f28a1c521341399da1f3559358f2abf876d34be#/%{name}-whq-7f28a1c.patch
Patch7035:      %{whq_url}/20c91c5e803090bd40fe3045a0d9fea0a68913e4#/%{name}-whq-20c91c5.patch
Patch7036:      %{whq_url}/683583faf2f4b00874f702429393b127aca8eef4#/%{name}-whq-683583f.patch
Patch7037:      %{whq_url}/0c14b1a962573ee125940f2008c646befe597226#/%{name}-whq-0c14b1a.patch
Patch7038:      %{whq_url}/2333099c52566c6cf3d3f981588a26d4ff408155#/%{name}-whq-2333099.patch
Patch7039:      %{whq_url}/4d70266274c1102c385dd00303d312d94453d19b#/%{name}-whq-4d70266.patch
Patch7040:      %{whq_url}/246dedaa091308f140a3cac41845f5e978492e37#/%{name}-whq-246deda.patch
Patch7041:      %{whq_url}/509ad75adbca85d606a3bd8bba727abf0751cebc#/%{name}-whq-509ad75.patch
Patch7042:      %{whq_url}/552bc8aa4703b674747df36c591038da17c0c858#/%{name}-whq-552bc8a.patch
Patch7043:      %{whq_url}/ff19f21913c508f5827df0e7e4c3a351c36711a0#/%{name}-whq-ff19f21.patch
Patch7044:      %{whq_url}/d8d6a6b2e639d2e29e166a3faf988b81388ae191#/%{name}-whq-d8d6a6b.patch
Patch7045:      %{whq_url}/df513b95ec24d279a10fbe358973662ce2c9c385#/%{name}-whq-df513b9.patch
Patch7046:      %{whq_url}/84d25135b3b2f9a30619f741d166fa1daa8298e5#/%{name}-whq-84d2513.patch
Patch7047:      %{whq_url}/a4ce2f652d76d033a79434416ff585cd15356a87#/%{name}-whq-a4ce2f6.patch
Patch7048:      %{whq_url}/ee5c842e5303c70e88a1c68390c46db1f1689f19#/%{name}-whq-ee5c842.patch
Patch7049:      %{whq_url}/b86dc3926bfe5cd92400aa96c89b0255eba1d447#/%{name}-whq-b86dc39.patch
Patch7050:      %{whq_url}/d4c2b61c48cdd35275684e75427d2cf0d8d928de#/%{name}-whq-d4c2b61.patch
Patch7051:      %{whq_url}/412555e0cdcd16439db56f6bd6ea56cedcda0883#/%{name}-whq-412555e.patch
Patch7052:      %{whq_url}/573be7e6023e73d736c341bdca1ee49594f56ee4#/%{name}-whq-573be7e.patch
Patch7053:      %{whq_url}/e0fca9451146908402a8fbc770ff189aba636213#/%{name}-whq-e0fca94.patch
Patch7054:      %{whq_url}/9ed951266244ad75454cfdb63ee0e872ca9ac43b#/%{name}-whq-9ed9512.patch
Patch7055:      %{whq_url}/06fa3d32a73d59c7fec59a8682e3750150f84554#/%{name}-whq-06fa3d3.patch
Patch7056:      %{whq_url}/07248fc5002fb109de8fc8e51e9d05329e0cd8cc#/%{name}-whq-07248fc.patch
Patch7057:      %{whq_url}/c3e2013b615dd449113fe8fce0700319aa082020#/%{name}-whq-c3e2013.patch
Patch7058:      %{whq_url}/98eab245d3c3377af0c3da6880bb8ede80cb0925#/%{name}-whq-98eab24.patch
Patch7059:      %{whq_url}/a20b997b3430bd7dc94ffd587cd299efa467420e#/%{name}-whq-a20b997.patch
Patch7060:      %{whq_url}/c4c3b06e83ce8f7f18e77a101656ba983fb0d0e3#/%{name}-whq-c4c3b06.patch
Patch7061:      %{whq_url}/e9e5c95058df1f409debeb6b05aa222b476d79f6#/%{name}-whq-e9e5c95.patch
Patch7062:      %{whq_url}/888d66a2376f0da076ec312ef5ca2d93fee0e2f9#/%{name}-whq-888d66a.patch
Patch7063:      %{whq_url}/f6bfb4ce00d27c4bc11615a5426065749e72b70a#/%{name}-whq-f6bfb4c.patch
Patch7064:      %{whq_url}/7e9ccbe68fe5215df9bd8e424195e1abf56f7286#/%{name}-whq-7e9ccbe.patch
Patch7065:      %{whq_url}/c1dc5021ac2534ea7bf52246f13c19941b791efa#/%{name}-whq-c1dc502.patch
Patch7066:      %{whq_url}/df5e4764870e8ad1d8b206cb3475a073bc034e48#/%{name}-whq-df5e476.patch
Patch7067:      %{whq_url}/2ec86fc20a49020a52cbec2727aca966642f9fac#/%{name}-whq-2ec86fc.patch
Patch7068:      %{whq_url}/44a230937b6dc320aad8b18828060e3e916eee03#/%{name}-whq-44a2309.patch
Patch7069:      %{whq_url}/e84ec36a620a4922ddcb9cdce9ddabc2573ee1da#/%{name}-whq-e84ec36.patch
Patch7070:      %{whq_url}/2e6a2cf9c65e92db51edfdec6fbace8e49e90c7a#/%{name}-whq-2e6a2cf.patch
Patch7071:      %{whq_url}/a0b7fb9bb2a6f446a0018a89bd8b50f756a0fe1c#/%{name}-whq-a0b7fb9.patch
Patch7072:      %{whq_url}/7e3d265469996efc7e720685be9b2c524eb7434b#/%{name}-whq-7e3d265.patch
Patch7073:      %{whq_url}/78532a0c09c33a24715ae5ff7f446f1de488a24b#/%{name}-whq-78532a0.patch
Patch7074:      %{whq_url}/5f9f827fd4effe08d544964db349b56519952da6#/%{name}-whq-5f9f827.patch
Patch7075:      %{whq_url}/a2c890c1e104140f83209c8d1e8ee298b346e38d#/%{name}-whq-a2c890c.patch
Patch7076:      %{whq_url}/c468a36903aea9ddac12b25c93cc5b65f293d6b9#/%{name}-whq-c468a36.patch
Patch7077:      %{whq_url}/6ff0bb786c43ac3348dec6a977feb36af8bc4bcf#/%{name}-whq-6ff0bb7.patch
Patch7078:      %{whq_url}/251335cdf35d4ff1fcae9c73f77136c9b85e7d96#/%{name}-whq-251335c.patch
Patch7079:      %{whq_url}/9e3893cc29dbcfd53d89abc679d0207cf2492999#/%{name}-whq-9e3893c.patch
Patch7080:      %{whq_url}/67949d96a7c49b95801723e8cfdf327e907822cb#/%{name}-whq-67949d9.patch
Patch7081:      %{whq_url}/537bb7a8aee278d285cb77669fd9258dfaa3222f#/%{name}-whq-537bb7a.patch
Patch7082:      %{whq_url}/b7ccb9d06a897a384b71ccb959b431168ca07e03#/%{name}-whq-b7ccb9d.patch
Patch7083:      %{whq_url}/99649d78927bb911b8a9022c8f362e0a7d9c7ea9#/%{name}-whq-99649d7.patch
Patch7084:      %{whq_url}/31538a79a90653afb8bc7744506989c8811a800d#/%{name}-whq-31538a7.patch
Patch7085:      %{whq_url}/577b3924408cd1ffa7d2559999751a9ced597882#/%{name}-whq-577b392.patch
Patch7086:      %{whq_url}/9b9845e43e08e357588bb6a2ca6bfc15ce2dcd73#/%{name}-whq-9b9845e.patch
Patch7087:      %{whq_url}/01143089f08c662a75f5af47fc2a8a3f8ae2afd6#/%{name}-whq-0114308.patch
Patch7088:      %{whq_url}/36e55720b66743d161330183693949e4f8503cc7#/%{name}-whq-36e5572.patch
Patch7089:      %{whq_url}/438abad27c797ca806938188f725fb0e36aa9fb9#/%{name}-whq-438abad.patch
Patch7090:      %{whq_url}/10dbd1edd19008bc8eaeb55446e1e5fd87a12814#/%{name}-whq-10dbd1e.patch
Patch7091:      %{whq_url}/c031662fd0bf1bc366185fe85a342bf60a9fc0bc#/%{name}-whq-c031662.patch
Patch7092:      %{whq_url}/7161dcd42653452a2373a7595a7020d0a59722f4#/%{name}-whq-7161dcd.patch
Patch7093:      %{whq_url}/13c1f008c0d8beca934ebfd347dc8354f4c9db05#/%{name}-whq-13c1f00.patch
Patch7094:      %{whq_url}/b8dc6b241204f5348563a23f51765234ef19f044#/%{name}-whq-b8dc6b2.patch
Patch7095:      %{whq_url}/e60591919850a79a483ec3c138fce96f8e1edb57#/%{name}-whq-e605919.patch
Patch7096:      %{whq_url}/dde38fda6eacf453cb48f75b7579647ceb75e9fd#/%{name}-whq-dde38fd.patch
Patch7097:      %{whq_url}/6898bdca94cde73bd8d8b88d99153a731f6a7a6b#/%{name}-whq-6898bdc.patch
Patch7098:      %{whq_url}/bededeccc51cc766ed48ce861a2a411ad8d22a87#/%{name}-whq-bededec.patch
Patch7099:      %{whq_url}/52c04e1e390e0008580eca7343f5c04aed3d1323#/%{name}-whq-52c04e1.patch
Patch7100:      %{whq_url}/18f83c12a04f934eda74fed77055073075bc4275#/%{name}-whq-18f83c1.patch
Patch7101:      %{whq_url}/847b93c7400f82225057e8b71938eb8ccd5d23be#/%{name}-whq-847b93c.patch
Patch7102:      %{whq_url}/69e9651c1ae0542e52f5ea924b9e286584446607#/%{name}-whq-69e9651.patch
Patch7103:      %{whq_url}/ed566a87232fddde73481efe2dfcefceca5e49e4#/%{name}-whq-ed566a8.patch
Patch7104:      %{whq_url}/b9f531a0e81ebf7a0dfeac00d557632546b12f56#/%{name}-whq-b9f531a.patch
Patch7105:      %{whq_url}/38c78a968259963d29559096dda575237039c561#/%{name}-whq-38c78a9.patch
Patch7106:      %{whq_url}/716cf7d342466235d3117db5da788704cbf2853d#/%{name}-whq-716cf7d.patch
Patch7107:      %{whq_url}/bc8745851e3005fd98c45fe06fc9d4d92c68fa53#/%{name}-whq-bc87458.patch
Patch7108:      %{whq_url}/067648cd2bdc4776cb69c6554ee9d799e0b201c7#/%{name}-whq-067648c.patch
Patch7109:      %{whq_url}/2334f4e64582a518e4d5a7627472a0d817b147ef#/%{name}-whq-2334f4e.patch
Patch7110:      %{whq_url}/f1ff598e2aca810c3a0540d6a764787d31890741#/%{name}-whq-f1ff598.patch
Patch7111:      %{whq_url}/15c3eaafbb3a376998e9c5eb36cb24816dad5447#/%{name}-whq-15c3eaa.patch
Patch7112:      %{whq_url}/83a4549e9baa252d0fb92d14e5a39119b8583813#/%{name}-whq-83a4549.patch
Patch7113:      %{whq_url}/43be3507c04b56938e985047f2ab55147ed8ddd2#/%{name}-whq-43be350.patch
Patch7114:      %{whq_url}/eef527723f02abcdb301b02cae059b123f277d26#/%{name}-whq-eef5277.patch
Patch7115:      %{whq_url}/e1e34cdc375baf2d1d5a2266ae0faa885987ab37#/%{name}-whq-e1e34cd.patch
Patch7116:      %{whq_url}/64731a8e9fce07a7c34374dc0a6bb6ed8b5f6183#/%{name}-whq-64731a8.patch
Patch7117:      %{whq_url}/4fcf20d1d120985a6056ef8e1861738c2e903660#/%{name}-whq-4fcf20d.patch
Patch7118:      %{whq_url}/f89f7a54c25eb202e70225713ed39687be048e26#/%{name}-whq-f89f7a5.patch
Patch7119:      %{whq_url}/8a169390c9ef4d8a43b604558c4194a052473c0c#/%{name}-whq-8a16939.patch
Patch7120:      %{whq_url}/4478ba258e45559ac97353ab27951e84dd9865c1#/%{name}-whq-4478ba2.patch
Patch7121:      %{whq_url}/cfc9da22f58659e57d20d76c1c45b91da9dca789#/%{name}-whq-cfc9da2.patch
Patch7122:      %{whq_url}/70fceaa2fe581ed41408faa368ff3f6833fd463c#/%{name}-whq-70fceaa.patch
Patch7123:      %{whq_url}/3df16c0b70f734f5260bfde0f68239976d6a5842#/%{name}-whq-3df16c0.patch
Patch7124:      %{whq_url}/d324014d42bc759b6a6faa594bdecce054e294c1#/%{name}-whq-d324014.patch
Patch7125:      %{whq_url}/b6722aa7527abc71cb46ab75e4b875c288408d52#/%{name}-whq-b6722aa.patch
Patch7126:      %{whq_url}/3a9edf9aad43c3e8ba724571da5381f821f1dc56#/%{name}-whq-3a9edf9.patch
Patch7127:      %{whq_url}/acc52bc90ef1d3cdfc3eef97bb3ac84bfc96cb4c#/%{name}-whq-acc52bc.patch
Patch7128:      %{whq_url}/2d5bd21f31e2a608120ba262ba2af245526905d3#/%{name}-whq-2d5bd21.patch
Patch7129:      %{whq_url}/8885a51347a768d8a9125d573963d12ac67d4715#/%{name}-whq-8885a51.patch
Patch7130:      %{whq_url}/520040dc4a287fd62d7d5161c083cee990c3d6e6#/%{name}-whq-520040d.patch
Patch7131:      %{whq_url}/21f1fa82a8c7bd1b077f0289141972ed619c5a5f#/%{name}-whq-21f1fa8.patch
Patch7132:      %{whq_url}/887332f9c7bf0d75f53f88a9739b77b12463d636#/%{name}-whq-887332f.patch
Patch7133:      %{whq_url}/25d6abb951e111fd4da1130fef16749ae6981540#/%{name}-whq-25d6abb.patch
Patch7134:      %{whq_url}/69b6572338396134a3e20189cb35445d68757ebb#/%{name}-whq-69b6572.patch
Patch7135:      %{whq_url}/c02b63fb60458ec750e5991a7491235861c40061#/%{name}-whq-c02b63f.patch
Patch7136:      %{whq_url}/72fc2ceaa6ae472a809b4d5c02be98c44388c1b7#/%{name}-whq-72fc2ce.patch
Patch7137:      %{whq_url}/a07cff77d3bd452c3c4b99bf93503f727bf768cb#/%{name}-whq-a07cff7.patch
Patch7138:      %{whq_url}/e9951dbe37c9fb018e677d872df9f563a0861295#/%{name}-whq-e9951db.patch
Patch7139:      %{whq_url}/b64208df0d8e94259783081084c5a731e0839542#/%{name}-whq-b64208d.patch
Patch7140:      %{whq_url}/695bf7a64532fe9755f2a471ed9e420b9e08539f#/%{name}-whq-695bf7a.patch
Patch7141:      %{whq_url}/086072ca6aa98e1d3107cac828c1d96cba01eeca#/%{name}-whq-086072c.patch
Patch7142:      %{whq_url}/66fb3802d31b34360f87edd11eb6508bca785824#/%{name}-whq-66fb380.patch
Patch7143:      %{whq_url}/5376bc5ee48f4ec3485dd404b32bd2530c24d3f7#/%{name}-whq-5376bc5.patch
Patch7144:      %{whq_url}/e5493e34e4a0c21771200b0ecb72b7c24c484f39#/%{name}-whq-e5493e3.patch
Patch7145:      %{whq_url}/dc672b49ca887c78a3e20854d96e7a56e967c072#/%{name}-whq-dc672b4.patch
Patch7146:      %{whq_url}/4448715cfbd70b214c332ab9fdfdfe3f28508177#/%{name}-whq-4448715.patch
Patch7147:      %{whq_url}/af9a8b1b0890cad21b23279d7f0dae083859e960#/%{name}-whq-af9a8b1.patch
Patch7148:      %{whq_url}/25f7aa52adf126b24c1fa2eaed9bd4b40152aa82#/%{name}-whq-25f7aa5.patch
Patch7149:      %{whq_url}/e3caa9c420bcad90bb850e588845d18f4d99e435#/%{name}-whq-e3caa9c.patch
Patch7150:      %{whq_url}/b116cf848a0816e8d03fad93bba1022baf53a229#/%{name}-whq-b116cf8.patch
Patch7151:      %{whq_url}/031c744a1fb9b94f7a4634eae5f56845b586554d#/%{name}-whq-031c744.patch
Patch7152:      %{whq_url}/a0266339c777eafcda918a253ec8d287372fc84d#/%{name}-whq-a026633.patch
Patch7153:      %{whq_url}/b2d09cbb219e43a203d908199cf0ada1aa344b8e#/%{name}-whq-b2d09cb.patch
Patch7154:      %{whq_url}/dfa48037ec462c279bf314670d07f04696a9a25c#/%{name}-whq-dfa4803.patch
Patch7155:      %{whq_url}/c198390c78acefdfd95ef3474f192a44f8e80b2c#/%{name}-whq-c198390.patch
Patch7156:      %{whq_url}/af3aee8a5a2852951b1fbc6e355e674fed9d4c5c#/%{name}-whq-af3aee8.patch
Patch7157:      %{whq_url}/ec3cdaba4f018a87ef2fdfdb2e47a8b7811402f1#/%{name}-whq-ec3cdab.patch
Patch7158:      %{whq_url}/8622eb326fb8120fc038e27947e61677d4124f15#/%{name}-whq-8622eb3.patch
Patch7160:      %{whq_url}/1ff8fe20bf87f0b60e2b1a185fd3f9ee383fe31c#/%{name}-whq-1ff8fe2.patch
Patch7161:      %{whq_url}/434871fd1b6d1fef8c68e8d35689caec49367e20#/%{name}-whq-434871f.patch
Patch7162:      %{whq_url}/1a43c5de71eea457855f7dcfb7e5811f1c74ebf8#/%{name}-whq-1a43c5d.patch
Patch7163:      %{whq_url}/2d38551dd9012db1361cbd5ff3de6cb5fb90dc60#/%{name}-whq-2d38551.patch
Patch7164:      %{whq_url}/eff42369e9c59f330083e25a23762df084ce6869#/%{name}-whq-eff4236.patch
Patch7165:      %{whq_url}/d04baa29e296599f3736ab9bd7c830451eb3335d#/%{name}-whq-d04baa2.patch
Patch7166:      %{whq_url}/640773aa9ee64201dd4985254bb259b14f7f640b#/%{name}-whq-640773a.patch
Patch7167:      %{whq_url}/a4ab07a653d5bc912e954c1fb970aeabb6daafe1#/%{name}-whq-a4ab07a.patch
Patch7168:      %{whq_url}/8898a6951988c95db3e92146b948a3b2aed08fd2#/%{name}-whq-8898a69.patch
Patch7169:      %{whq_url}/b58a899acc9b6c2c02c78223b74db2822fe1ebb4#/%{name}-whq-b58a899.patch
Patch7170:      %{whq_url}/e0e3b6bc91f7db956e3a66f2938eea45d4055a39#/%{name}-whq-e0e3b6b.patch
Patch7171:      %{whq_url}/d33474fa6bae057b6e7fd6acda76438d90dc66bc#/%{name}-whq-d33474f.patch
Patch7172:      %{whq_url}/829739273425ba3a275aa8b93cde82bdff02975c#/%{name}-whq-8297392.patch
Patch7173:      %{whq_url}/82cd85b07918a4437428497ffaf7f13286b83479#/%{name}-whq-82cd85b.patch
Patch7174:      %{whq_url}/20715ee3fdaa794a7b6ba285cdb72b68991c65af#/%{name}-whq-20715ee.patch
Patch7175:      %{whq_url}/917a206b01c82170a862e8497cbe26b6f1bfade0#/%{name}-whq-917a206.patch
Patch7176:      %{whq_url}/518decf16b8445f49cb8bddfd081e7911ae28212#/%{name}-whq-518decf.patch
Patch7177:      %{whq_url}/f8699c0a71a528d287b84cd0bc5b5bb7cec924f0#/%{name}-whq-f8699c0.patch
Patch7178:      %{whq_url}/49fcd632e4b512421810ec4e35dc455b3f7697d3#/%{name}-whq-49fcd63.patch
Patch7179:      %{whq_url}/1320b15dfc87997e60d7a2af70000e5650b83cba#/%{name}-whq-1320b15.patch
Patch7180:      %{whq_url}/845156cc3dc8c8c6b1b62fcb57bcdfc25c94e100#/%{name}-whq-845156c.patch
Patch7181:      %{whq_url}/a0d325333fb0cba6028a15b924dd115cbbdc0586#/%{name}-whq-a0d3253.patch
Patch7182:      %{whq_url}/378ce9e6bea05fed194d44666eabd7a0d25caffd#/%{name}-whq-378ce9e.patch
Patch7183:      %{whq_url}/340a661723eab4afe2204837716e2b53cc14f5f2#/%{name}-whq-340a661.patch
Patch7184:      %{whq_url}/ca0db956a65f9010983c6723643e50df115ef34a#/%{name}-whq-ca0db95.patch
Patch7185:      %{whq_url}/461fc592ad1462c022bcf1c2cebfaee2bb5cc1de#/%{name}-whq-461fc59.patch
Patch7186:      %{whq_url}/d0a16b7dc99a4040e4e804c04d71a24b3a9d829e#/%{name}-whq-d0a16b7.patch
Patch7187:      %{whq_url}/368e3a93b8da3641c53f260bb4c96d03d00d1080#/%{name}-whq-368e3a9.patch
Patch7188:      %{whq_url}/5ebdeaaa372186b4c3a9098676c76423a1781154#/%{name}-whq-5ebdeaa.patch
Patch7189:      %{whq_url}/6f862a1ad803b1a7037797cedb3624445538afc1#/%{name}-whq-6f862a1.patch
Patch7190:      %{whq_url}/113e9811c473dd73b14964893cecf0c7042502cc#/%{name}-whq-113e981.patch
Patch7191:      %{whq_url}/b14eee69c7240658252bc96b6302e98948f2c62c#/%{name}-whq-b14eee6.patch
Patch7192:      %{whq_url}/829c7595130bb84e131b797e45a84176b169a81c#/%{name}-whq-829c759.patch
Patch7193:      %{whq_url}/7e4ea871a33f226684ecef9ba158cf9cf8efe42d#/%{name}-whq-7e4ea87.patch
Patch7194:      %{whq_url}/b72270cb16bc670bbf46be6fdc8dffc525d82f35#/%{name}-whq-b72270c.patch
Patch7195:      %{whq_url}/e722660114e268179344e2e076a8e10b0f8ab3f3#/%{name}-whq-e722660.patch
Patch7196:      %{whq_url}/095b0f5acc225ab79db2406d42686b8c51b4d887#/%{name}-whq-095b0f5.patch
Patch7197:      %{whq_url}/d8739008bd33dfe2587d4afc524b17ec87f59ddd#/%{name}-whq-d873900.patch
Patch7198:      %{whq_url}/af3320c57576166e0d306c1e4d9d4d3964ad58b1#/%{name}-whq-af3320c.patch
Patch7199:      %{whq_url}/0c3c89b74decfdab8e0227d87e5eecdb3380806c#/%{name}-whq-0c3c89b.patch
Patch7200:      %{whq_url}/2789787f011e1a923dc22b6884433826e9350725#/%{name}-whq-2789787.patch
Patch7201:      %{whq_url}/d25a267978de5949a283c5f76405175316f8f773#/%{name}-whq-d25a267.patch
Patch7202:      %{whq_url}/547855e623c561c23b205f18d017e53d5ee75b7b#/%{name}-whq-547855e.patch
Patch7203:      %{whq_url}/587ca81f8de4fec07217b4e55e370f3fb6095773#/%{name}-whq-587ca81.patch
Patch7204:      %{whq_url}/94c1640bb38edd76bab13b29f1444bce20edcacc#/%{name}-whq-94c1640.patch
Patch7205:      %{whq_url}/56ee3a8ad12b02e2c53a2f3737bcd6ba15fd4737#/%{name}-whq-56ee3a8.patch
Patch7206:      %{whq_url}/0a57d3853bd0b3bfd25b7d171e8c9bddca22f52a#/%{name}-whq-0a57d38.patch
Patch7207:      %{whq_url}/a2e77268f2007f2819c2e3e8bd736a056f309a4c#/%{name}-whq-a2e7726.patch
Patch7208:      %{whq_url}/9ec262ebcc7f14d7373841d4ca082b855ed8090f#/%{name}-whq-9ec262e.patch
Patch7209:      %{whq_url}/eccd21e38735fb08e31a4be1a8897ebe248747b4#/%{name}-whq-eccd21e.patch
Patch7210:      %{whq_url}/4a49af0cbeb1bb5570d92f679c98ad05abc693e6#/%{name}-whq-4a49af0.patch
Patch7211:      %{whq_url}/9ac3f24f744bf76c252fafb2c2e254bbbf38ed1e#/%{name}-whq-9ac3f24.patch
Patch7212:      %{whq_url}/0357d2ca75be92e927bb785a786d3766c94f3c83#/%{name}-whq-0357d2c.patch
Patch7213:      %{whq_url}/bcc3410732c60e32eaf3abd808be7482218f57d7#/%{name}-whq-bcc3410.patch
Patch7214:      %{whq_url}/afb16545671e7420c7a8bbb4ef97333c33001564#/%{name}-whq-afb1654.patch
Patch7215:      %{whq_url}/63b66c9955b243e20b280dac236dea4fdf21c92c#/%{name}-whq-63b66c9.patch
Patch7216:      %{whq_url}/fb8a44f3ee50badd85af4b50fdbc1db28ce76ab0#/%{name}-whq-fb8a44f.patch
Patch7217:      %{whq_url}/674ec0c7f6754c47a5a513ceff80663bb8f5a3e4#/%{name}-whq-674ec0c.patch
Patch7218:      %{whq_url}/86acbd0122ddad629f4ac55595782f2c704d54dc#/%{name}-whq-86acbd0.patch
Patch7219:      %{whq_url}/3b81ea316198e1b128e0e41534da48218f5b641a#/%{name}-whq-3b81ea3.patch
Patch7220:      %{whq_url}/5ff23d2218b6166c78cd587b1f633a2a3540a541#/%{name}-whq-5ff23d2.patch
Patch7221:      %{whq_url}/b21d2e5f58dc5fa713174616de5042e05e13a1fe#/%{name}-whq-b21d2e5.patch
Patch7222:      %{whq_url}/f7a7633aa107003238171c12f52d2f57b93bc3f2#/%{name}-whq-f7a7633.patch
Patch7223:      %{whq_url}/2efb498a7b088a0d1d072754b668fcf752532de7#/%{name}-whq-2efb498.patch
Patch7224:      %{whq_url}/07194e9287eb2e2adbc2d1bdff204b4f8dec3ef0#/%{name}-whq-07194e9.patch
Patch7225:      %{whq_url}/6695ca86a29c4ba3844445480d5591c0dd75a824#/%{name}-whq-6695ca8.patch
Patch7226:      %{whq_url}/9c6d0f6eeab8eb58a9cfc4ba3c1d3c9145b1d8db#/%{name}-whq-9c6d0f6.patch
Patch7227:      %{whq_url}/4d57e8f937fc866d092539ceafb989d740462d2c#/%{name}-whq-4d57e8f.patch
Patch7228:      %{whq_url}/409160bb596e44bcceee24d9ecd4d2629cbd6cb7#/%{name}-whq-409160b.patch
Patch7229:      %{whq_url}/48a23dbd432d8dbeaa884fe656105d902729f8de#/%{name}-whq-48a23db.patch
Patch7230:      %{whq_url}/f5badeac28dc245c4804d4d0a72ddfcea66846ac#/%{name}-whq-f5badea.patch
Patch7231:      %{whq_url}/22f53e6d9dd23a88d75ec8b6e4b3a73a186344d1#/%{name}-whq-22f53e6.patch
Patch7232:      %{whq_url}/7aadafbd505ab61c15bccb7d995cc9f4afc54e3d#/%{name}-whq-7aadafb.patch
Patch7233:      %{whq_url}/0e46dd09e5c71726f0c120362991cd3b2613295b#/%{name}-whq-0e46dd0.patch
Patch7234:      %{whq_url}/c6fea822a99ca4b5c82e5217a0a631434ad52c29#/%{name}-whq-c6fea82.patch
Patch7235:      %{whq_url}/c71da19d24a5d6f01e65b3b3691a9d7dd17a2278#/%{name}-whq-c71da19.patch
Patch7236:      %{whq_url}/fdb09f452376ead1fceeb04dc5407095467418c1#/%{name}-whq-fdb09f4.patch
Patch7237:      %{whq_url}/992bdd77a05755ccbde22bf244a41ab3c50086db#/%{name}-whq-992bdd7.patch
Patch7238:      %{whq_url}/99520e1997b92155b9e389513960b0bdacfab9b2#/%{name}-whq-99520e1.patch
Patch7239:      %{whq_url}/3b745f17b5553f88011a50a7b355f0eb3f5084b9#/%{name}-whq-3b745f1.patch
Patch7240:      %{whq_url}/d7ef680e950431d868e6d52418513472af7edbb3#/%{name}-whq-d7ef680.patch
Patch7241:      %{whq_url}/85db4f7ec28a5d68fecba624f518dc1d2a07e359#/%{name}-whq-85db4f7.patch
Patch7242:      %{whq_url}/052e8dbf5985ffa5875067491b03a523257752f9#/%{name}-whq-052e8db.patch
Patch7243:      %{whq_url}/5498ebd8c0aaa651ce6823cccdf572a3f551deba#/%{name}-whq-5498ebd.patch
Patch7244:      %{whq_url}/fdb3d9ae320363c1bd9fa716b167a7ad313e638b#/%{name}-whq-fdb3d9a.patch
Patch7245:      %{whq_url}/ef01f6ac1338dcb100bc2ff5cd1cf360d7d8520f#/%{name}-whq-ef01f6a.patch
Patch7246:      %{whq_url}/1037bf54bf056090855c3e2dc8c70193f18a243e#/%{name}-whq-1037bf5.patch
Patch7247:      %{whq_url}/9ec5be2cea3af2ca631ef0dce3208965058abb59#/%{name}-whq-9ec5be2.patch
Patch7248:      %{whq_url}/b2d38f15314e39eeb17ec5e02bc6fe78b26420e3#/%{name}-whq-b2d38f1.patch
Patch7249:      %{whq_url}/e9abe3f7395a81dcb6d192b48bd54848dc4f2b5e#/%{name}-whq-e9abe3f.patch
Patch7250:      %{whq_url}/83f9e784e42c404e31172e55a406a8403c8a33de#/%{name}-whq-83f9e78.patch
Patch7251:      %{whq_url}/42a2ad202e6a260dc9e3f04939c7dacf270f7434#/%{name}-whq-42a2ad2.patch
Patch7252:      %{whq_url}/fe7b8d70d5229c693dc16b743ef0ec7f76a1569f#/%{name}-whq-fe7b8d7.patch
Patch7253:      %{whq_url}/242dc8989a993d1b3807f437fbac7b92707b6e28#/%{name}-whq-242dc89.patch
Patch7254:      %{whq_url}/20bc32cddc6ca8b1e2577cbc12050804972ca0ac#/%{name}-whq-20bc32c.patch
Patch7255:      %{whq_url}/a6fb7be678438ab689ac87ad4ed21a9b33a17c2e#/%{name}-whq-a6fb7be.patch
Patch7256:      %{whq_url}/6b96e0e0cbdc28e9dbde3fa3d9bc948b512fd1fb#/%{name}-whq-6b96e0e.patch
Patch7257:      %{whq_url}/bf6a803e04db1c466c9e7b1fd44e17ee10b17381#/%{name}-whq-bf6a803.patch
Patch7258:      %{whq_url}/440e31a73212382362cf64982de8ecf2d579cdb4#/%{name}-whq-440e31a.patch
Patch7259:      %{whq_url}/a07aa965e5d3c2f4a46387ad911ef1c8500e2107#/%{name}-whq-a07aa96.patch
Patch7260:      %{whq_url}/dce5b9add1f9221c176e47c920e247ceeb70632c#/%{name}-whq-dce5b9a.patch
Patch7261:      %{whq_url}/35352575e4e8d9fc753dad583f2b24ed999ec8db#/%{name}-whq-3535257.patch
Patch7262:      %{whq_url}/4617f83fcf0a34fe41b0e38dde1567195395efca#/%{name}-whq-4617f83.patch
Patch7263:      %{whq_url}/e9b3660e729929f4e09f403d526759d532df03e0#/%{name}-whq-e9b3660.patch
Patch7264:      %{whq_url}/99851ca4c2edd4b921c91327540d69dec77c5df7#/%{name}-whq-99851ca.patch
Patch7265:      %{whq_url}/f30ba2cf256054c4aa6b75ff2f282dfe8e2c219a#/%{name}-whq-f30ba2c.patch
Patch7266:      %{whq_url}/5a68254c131290adbf51843aa82f543afe99fe87#/%{name}-whq-5a68254.patch
Patch7267:      %{whq_url}/432d504118f4c00cc33c199946b36448cc6355e1#/%{name}-whq-432d504.patch
Patch7268:      %{whq_url}/f1e4c54104d92f57d0b3699a800c0f09ce4e8320#/%{name}-whq-f1e4c54.patch
Patch7269:      %{whq_url}/9a9fb47e24d3daa57aa24bc5529e33b6271b92bc#/%{name}-whq-9a9fb47.patch
Patch7270:      %{whq_url}/ca45eda758e29261691b27eecf1f4fc78bdfadc5#/%{name}-whq-ca45eda.patch
Patch7271:      %{whq_url}/485c8566f103f05dba3c8c31d3adb18b89eb032a#/%{name}-whq-485c856.patch
Patch7272:      %{whq_url}/1e4865ffcfa4933ff27b1e66405e1498dd9d1781#/%{name}-whq-1e4865f.patch
Patch7273:      %{whq_url}/adb4e74b479d5406454dffa17fe908742306ac6e#/%{name}-whq-adb4e74.patch
Patch7274:      %{whq_url}/ae15a4ca5a1c7270dcfe4f7456ea75fc946ab279#/%{name}-whq-ae15a4c.patch
Patch7275:      %{whq_url}/3889c374a11d92733f6830473ff589f8846a7396#/%{name}-whq-3889c37.patch
Patch7276:      %{whq_url}/7b795324483504e911350a8c0710d4c2fa2b6dee#/%{name}-whq-7b79532.patch
Patch7277:      %{whq_url}/82dc024a35a1a522b088df4e9355fa7752f40821#/%{name}-whq-82dc024.patch
Patch7278:      %{whq_url}/704d0662bef08a980c87c408fa33f50fc60b5cac#/%{name}-whq-704d066.patch
Patch7279:      %{whq_url}/7c4f2d5342a8673af994077ed2e586b0f3410583#/%{name}-whq-7c4f2d5.patch
Patch7280:      %{whq_url}/73fc0a18a693c179d676d38fe8cf0df8f7679ea9#/%{name}-whq-73fc0a1.patch
Patch7281:      %{whq_url}/9ed6d24ed83d20796e2c5190365c26426a0c6a87#/%{name}-whq-9ed6d24.patch
Patch7282:      %{whq_url}/3c1ebfdf82242e28ef697c139e0e94cb5ceb3fcd#/%{name}-whq-3c1ebfd.patch
Patch7283:      %{whq_url}/d2b83336c7b219b3267035bd6ab9af5480184743#/%{name}-whq-d2b8333.patch
Patch7284:      %{whq_url}/6e9d3d2014145930f688f4c5c9043d5112d41b6e#/%{name}-whq-6e9d3d2.patch
Patch7285:      %{whq_url}/4ea42892539d84e6fd5bb864d18ef26d0e2038d4#/%{name}-whq-4ea4289.patch
Patch7286:      %{whq_url}/037b91620c4caafae943e7cd304f0d9df4335d21#/%{name}-whq-037b916.patch
Patch7287:      %{whq_url}/ffa52880f2519c885ce61b89b847c82e0531c032#/%{name}-whq-ffa5288.patch
Patch7288:      %{whq_url}/823c55ad2755c36f55cce1f0cf5f0ee6dcaf9d76#/%{name}-whq-823c55a.patch
Patch7289:      %{whq_url}/42cb7d2ad1caba08de235e6319b9967296b5d554#/%{name}-whq-42cb7d2.patch
Patch7290:      %{whq_url}/14994715e9337821aeac39c0f43b704bdc7ba200#/%{name}-whq-1499471.patch
Patch7291:      %{whq_url}/d1f83537e7f064f0f77ead043617bc213c8c0053#/%{name}-whq-d1f8353.patch
Patch7292:      %{whq_url}/bc2164e07487edccc32bff06691d14ab017a3f47#/%{name}-whq-bc2164e.patch
Patch7293:      %{whq_url}/f4c403d1f2100934c24241b0ed8f4e19cb0ff4dd#/%{name}-whq-f4c403d.patch
Patch7294:      %{whq_url}/3f51cb630497621042c0479d8a604d74a837ba3b#/%{name}-whq-3f51cb6.patch
Patch7295:      %{whq_url}/66e6d87ab86c393f189aa8d409b62b3e028ed17e#/%{name}-whq-66e6d87.patch
Patch7296:      %{whq_url}/aa08e1541510357f3c3865cc959cc1d60a1b86cf#/%{name}-whq-aa08e15.patch
Patch7297:      %{whq_url}/9f8acda1677e90a5f429ef8db739adce700629ca#/%{name}-whq-9f8acda.patch
Patch7298:      %{whq_url}/eb45a75a2e76e9716d08ae35cc2512b02e3bf85d#/%{name}-whq-eb45a75.patch
Patch7299:      %{whq_url}/c5f66fc784d20154f3d5905d25f8243a0fc6a330#/%{name}-whq-c5f66fc.patch
Patch7300:      %{whq_url}/00e7d50f8bd3dccf2c34dac2501937b7d294ab76#/%{name}-whq-00e7d50.patch
Patch7301:      %{whq_url}/635e914bdeca3a148dab8aeabc8037a2e7ac8151#/%{name}-whq-635e914.patch
Patch7302:      %{whq_url}/3b4c2ffb7bcc86165c67def31debfa63ccae7a62#/%{name}-whq-3b4c2ff.patch
Patch7303:      %{whq_url}/e3e477e6a14fbcb153258b47d1905915dc4c1f22#/%{name}-whq-e3e477e.patch
Patch7304:      %{whq_url}/40d403c926e8f96c77d067188c842c12f099f9a9#/%{name}-whq-40d403c.patch
Patch7305:      %{whq_url}/0534beb331ff9f1444db47cfb3c03224c1837aca#/%{name}-whq-0534beb.patch
Patch7306:      %{whq_url}/26c8fb8ce7a09698cdba73576cf924185dffd3a9#/%{name}-whq-26c8fb8.patch
Patch7307:      %{whq_url}/c7032e9222fdfd3b4364d6c729fa5ca6f0b35f69#/%{name}-whq-c7032e9.patch
Patch7308:      %{whq_url}/77e74fb1dbc8a435cefe17998dc73a4e40c3aeed#/%{name}-whq-77e74fb.patch
Patch7309:      %{whq_url}/088ababfc24751b951008570f6160a1e8dca0e0c#/%{name}-whq-088abab.patch
Patch7310:      %{whq_url}/1cf4a1c0880f0f39f6d986db53a3b108a6e5c648#/%{name}-whq-1cf4a1c.patch
Patch7311:      %{whq_url}/3347ad003a1f86b6d1cd83b63a8e8dac1e8e784f#/%{name}-whq-3347ad0.patch
Patch7312:      %{whq_url}/12dba1b2ae50099de4cd857f867ebcaefe6852d8#/%{name}-whq-12dba1b.patch
Patch7313:      %{whq_url}/2aa58e43a0d8589aa37f275147e5beab023b5d42#/%{name}-whq-2aa58e4.patch
Patch7314:      %{whq_url}/5a174dd60446effe39f78ec7b4394e80e2522d98#/%{name}-whq-5a174dd.patch
Patch7315:      %{whq_url}/c4789b08f3bcc879d3a95b1023626a3e2a3a8967#/%{name}-whq-c4789b0.patch
Patch7316:      %{whq_url}/919a94aa954f543b49728f1750ea23aab21cc41c#/%{name}-whq-919a94a.patch
Patch7317:      %{whq_url}/9415667cdfbb4c94cdfe03a1e80a87482bee98c1#/%{name}-whq-9415667.patch
Patch7318:      %{whq_url}/d7e12831b04ed6645558bdeec41e09311200d7f3#/%{name}-whq-d7e1283.patch
Patch7319:      %{whq_url}/5e240cdf50dc10003a8663ec9be51f9d8bb42634#/%{name}-whq-5e240cd.patch
Patch7320:      %{whq_url}/2a539470287005b51e2e72f27026fde26691ba65#/%{name}-whq-2a53947.patch
Patch7321:      %{whq_url}/de1eaee4804ffbeb0917b139638adb19c2106936#/%{name}-whq-de1eaee.patch
Patch7322:      %{whq_url}/7053b7c615b44e7112ab8fb4c056206d32b6f1c9#/%{name}-whq-7053b7c.patch
Patch7323:      %{whq_url}/28bf959c5c342faa956e718823bcabb06a4c4c30#/%{name}-whq-28bf959.patch
Patch7324:      %{whq_url}/76e48978a95deed5eb5fa601486648e3665d21ad#/%{name}-whq-76e4897.patch
Patch7325:      %{whq_url}/0eae5d3abc64e6496df5d7d7b36944e0cfada76e#/%{name}-whq-0eae5d3.patch
Patch7326:      %{whq_url}/398cfe48079ce02f0f13f62273b31f5ee0fd1a4b#/%{name}-whq-398cfe4.patch
Patch7327:      %{whq_url}/e7c60141d616b609b99e59a19375fc9759c3e4fa#/%{name}-whq-e7c6014.patch
Patch7328:      %{whq_url}/e0a2f85b788b5cd764582a71fadaee11f06ab979#/%{name}-whq-e0a2f85.patch
Patch7329:      %{whq_url}/500131b2f5fcdc09eb15bb5db740b6ae5dfd9390#/%{name}-whq-500131b.patch
Patch7330:      %{whq_url}/6039b785947088d379672c709c227b96ce3be1e5#/%{name}-whq-6039b78.patch
Patch7331:      %{whq_url}/b68138a62e849036b75954f7a406c64be5d86e21#/%{name}-whq-b68138a.patch
Patch7332:      %{whq_url}/f4d7d8955098a0255733ae304349415fa373049c#/%{name}-whq-f4d7d89.patch
Patch7333:      %{whq_url}/d2b0c10000ad53dbc0aa717b31f18f9078f35c7f#/%{name}-whq-d2b0c10.patch
Patch7334:      %{whq_url}/180f7cf412c486a4f2f769b44c0ccf1223226ee3#/%{name}-whq-180f7cf.patch
Patch7335:      %{whq_url}/b1af31b47aa96ae5f6a8444ffba7a060f7ef6099#/%{name}-whq-b1af31b.patch
Patch7336:      %{whq_url}/f3ca16379d8c06f3342fc3039f4be926325808b8#/%{name}-whq-f3ca163.patch
Patch7337:      %{whq_url}/8ac77cfbf96689d83463928a9d0bdc5fcd054cb9#/%{name}-whq-8ac77cf.patch
Patch7338:      %{whq_url}/519f86d5aa4f61e47bcbf3a7207354523aa752e2#/%{name}-whq-519f86d.patch
Patch7339:      %{whq_url}/9dd1eaab44ae3677bb93160d4d7d709b26202dac#/%{name}-whq-9dd1eaa.patch
Patch7340:      %{whq_url}/17785690c047d507d8031aced658b716969e8668#/%{name}-whq-1778569.patch
Patch7341:      %{whq_url}/ff9ce43c0127bd23d5aaf9cb6bbb28fcbe729fac#/%{name}-whq-ff9ce43.patch
Patch7342:      %{whq_url}/a47f4daf8f70bc389fb1789e3e90df6138cf0549#/%{name}-whq-a47f4da.patch
Patch7343:      %{whq_url}/dd77ff754b949c21c986b61592cdc91884f2e175#/%{name}-whq-dd77ff7.patch
Patch7344:      %{whq_url}/f298db7254a42b2818083469bba0ed8080be38de#/%{name}-whq-f298db7.patch
Patch7345:      %{whq_url}/0e45f7b4cd8bbf8833737cb2f4f6aedecbe3a7de#/%{name}-whq-0e45f7b.patch
Patch7346:      %{whq_url}/9def213de32a80fcfb05a7474be42f44d7a0c939#/%{name}-whq-9def213.patch
Patch7347:      %{whq_url}/dcd02876ea73f65dc286038f0f70189c4994152f#/%{name}-whq-dcd0287.patch
Patch7348:      %{whq_url}/abe5fda90d918e0efbc0f4e122eee7cf637a2e9c#/%{name}-whq-abe5fda.patch
Patch7349:      %{whq_url}/bd12ec5dfff885a1bd5a5d05b2ec48129e6f4398#/%{name}-whq-bd12ec5.patch
Patch7350:      %{whq_url}/96c5109a0f1a4b203e2a0575764a2577f5270c52#/%{name}-whq-96c5109.patch
Patch7351:      %{whq_url}/2fc11e8952bff715115425346d0ccbaed146bcd5#/%{name}-whq-2fc11e8.patch
Patch7352:      %{whq_url}/fc7dae4ba5edd734bb0ffc7318dcc659d1797f2b#/%{name}-whq-fc7dae4.patch
Patch7353:      %{whq_url}/cb28c2dbb0d92bcddea768bd5d43c5caecba6a0f#/%{name}-whq-cb28c2d.patch
Patch7354:      %{whq_url}/dc1483c179d8e6e8ac1efe1fb54d8f1f2395077d#/%{name}-whq-dc1483c.patch
Patch7355:      %{whq_url}/2e5b8ffcc9ab8ac750e6fb2ac32eadeb6698540d#/%{name}-whq-2e5b8ff.patch
Patch7356:      %{whq_url}/e613d81d815d96a04eca42eea5faec71bdd459d9#/%{name}-whq-e613d81.patch
Patch7357:      %{whq_url}/f8d42a31c624f28f6c9bfd9678fb025bf15e9c12#/%{name}-whq-f8d42a3.patch
Patch7358:      %{whq_url}/688799b1f7b2750b938f8da771480d2c16d1ae1d#/%{name}-whq-688799b.patch
Patch7359:      %{whq_url}/5eefbc6db98985a5b63bec78fde7eef2f7fa02f2#/%{name}-whq-5eefbc6.patch
Patch7360:      %{whq_url}/4752e252ea6ee084b679a9b9551a1c55f8744451#/%{name}-whq-4752e25.patch
Patch7361:      %{whq_url}/78c772e9d802d13522855fa3c8e2257c4933214a#/%{name}-whq-78c772e.patch
Patch7362:      %{whq_url}/d41b1c28c378c531cc9c66639bfa16778972281d#/%{name}-whq-d41b1c2.patch
Patch7363:      %{whq_url}/1372d8fc2cac3466d759500063a50d86f03dc94a#/%{name}-whq-1372d8f.patch
Patch7364:      %{whq_url}/131e53a1fc2cd7156b56402c97d53af8da72399e#/%{name}-whq-131e53a.patch
Patch7365:      %{whq_url}/9018a377355fb2906d06b50008d04761491bbfd9#/%{name}-whq-9018a37.patch
Patch7367:      %{whq_url}/5b795b658d14bd85ba6783131c6f42a37cfcce27#/%{name}-whq-5b795b6.patch
Patch7368:      %{whq_url}/09ab7e8a0c9c96624e4597b6e91cb202a8086ef9#/%{name}-whq-09ab7e8.patch
Patch7369:      %{whq_url}/30453f0acf8bdca4dec5de38d08a776b933256c8#/%{name}-whq-30453f0.patch
Patch7370:      %{whq_url}/db886f09236759141a95183be83c666cac5f9a64#/%{name}-whq-db886f0.patch
Patch7371:      %{whq_url}/98bee7881a30eb01fb3d633f008957919a4aa71b#/%{name}-whq-98bee78.patch
Patch7372:      %{whq_url}/9f3e9d464da8806acd185783f4d2350dd675fd2e#/%{name}-whq-9f3e9d4.patch
Patch7373:      %{whq_url}/0bf52b09f2913b2f718fb32ccd0b1300bdada679#/%{name}-whq-0bf52b0.patch
Patch7374:      %{whq_url}/e3b059b5bad4b7ff23459a6384c866e3da1bdee1#/%{name}-whq-e3b059b.patch
Patch7375:      %{whq_url}/a865a4f61d413d85d6ae4e57d3c14c0657d3a598#/%{name}-whq-a865a4f.patch
Patch7376:      %{whq_url}/d18b5669952bf1639be78fd699310231d4de0259#/%{name}-whq-d18b566.patch
Patch7377:      %{whq_url}/b37371bf20be58ee7bd0b63dbac15b474873bc86#/%{name}-whq-b37371b.patch
Patch7378:      %{whq_url}/928fffee8dac4a9555bbbc141d9f29483422eee1#/%{name}-whq-928fffe.patch
Patch7379:      %{whq_url}/29d5c6c476faa00529fe765150d014607da48f27#/%{name}-whq-29d5c6c.patch
Patch7380:      %{whq_url}/8e3b5183cc79b99ac74e2cb3f665f8e46a076495#/%{name}-whq-8e3b518.patch
Patch7381:      %{whq_url}/9a7c56d9e7f8e49dc98dace53b10d0753f0e27a7#/%{name}-whq-9a7c56d.patch
Patch7382:      %{whq_url}/28e443d9e2a3bfea936b4f6f97bf78f6ccf6a91a#/%{name}-whq-28e443d.patch
Patch7383:      %{whq_url}/15b3584603205b93e6e6a0bace6159438ce22ffb#/%{name}-whq-15b3584.patch
Patch7384:      %{whq_url}/57f419993eb8088ef210e8a56b07acf63509b159#/%{name}-whq-57f4199.patch
Patch7385:      %{whq_url}/d775b9fd93ecfbbd12945f1e167e4bb381612c69#/%{name}-whq-d775b9f.patch
Patch7386:      %{whq_url}/94ca95a6d444e8cd1592bd41f09cba2e1ae49902#/%{name}-whq-94ca95a.patch
Patch7387:      %{whq_url}/8e5c11b964e844696c7f5882d3b8dd7ff70a7869#/%{name}-whq-8e5c11b.patch
Patch7388:      %{whq_url}/06c09fca3127fce9d3a3d1b4714173404ee58629#/%{name}-whq-06c09fc.patch
Patch7389:      %{whq_url}/eee92591bcf4eb7e1f0d91e24c47b5021a9c81fe#/%{name}-whq-eee9259.patch
Patch7390:      %{whq_url}/7a31d401391c9c66173a599cadbbb6946f607927#/%{name}-whq-7a31d40.patch
Patch7391:      %{whq_url}/44052219aa0e6412a0f595f830c0cdf6e82ea70c#/%{name}-whq-4405221.patch
Patch7392:      %{whq_url}/300a01f467e84bb69bf6387e52545ddbc9c456dc#/%{name}-whq-300a01f.patch
Patch7393:      %{whq_url}/5f6bb63800c14a46a4124c5a5e42094cae3a38fc#/%{name}-whq-5f6bb63.patch
Patch7394:      %{whq_url}/f8fa6fd68608b53def2c34a489b5af2416f47cd7#/%{name}-whq-f8fa6fd.patch
Patch7395:      %{whq_url}/f6fb372a045256d84d6e18d4757b9f59e209cf0e#/%{name}-whq-f6fb372.patch
Patch7396:      %{whq_url}/1e5cd8fadcb80b68391de6589304d9f2654dbdd8#/%{name}-whq-1e5cd8f.patch
Patch7397:      %{whq_url}/7ae370a5491b58eeec03961b09dcf5ae5e53e411#/%{name}-whq-7ae370a.patch
Patch7398:      %{whq_url}/3609406308110f93f11c6045da5734f038ef727c#/%{name}-whq-3609406.patch
Patch7399:      %{whq_url}/b6b2667482a14e4cd76da48940ead142ce207b2e#/%{name}-whq-b6b2667.patch
Patch7400:      %{whq_url}/e7c9a0e1511641961a69babe2ab7aca75c636672#/%{name}-whq-e7c9a0e.patch
Patch7401:      %{whq_url}/fef78c4e10422319736f290e44493838e4257a04#/%{name}-whq-fef78c4.patch
Patch7402:      %{whq_url}/ad1f09d57424b26bcf463dd45b5b0acb5bd97029#/%{name}-whq-ad1f09d.patch
Patch7403:      %{whq_url}/1f5a45e63ecff2f83eb927e253007bd75fb36c05#/%{name}-whq-1f5a45e.patch
Patch7404:      %{whq_url}/c37c9bf65a6f6dfd9708f6654227a953504dc158#/%{name}-whq-c37c9bf.patch
Patch7405:      %{whq_url}/305da71c7d8098bf2d2a07584a25be2e5fcc2b91#/%{name}-whq-305da71.patch
Patch7406:      %{whq_url}/3f8d60e2ac5997766f19107aef23e351c7d68a03#/%{name}-whq-3f8d60e.patch
Patch7407:      %{whq_url}/b7e51a1653320d06a9c04f53d0d9e7eda577c31b#/%{name}-whq-b7e51a1.patch
Patch7408:      %{whq_url}/78831ae9d044ffb824e72cb8952f3eb25140c7c9#/%{name}-whq-78831ae.patch
Patch7409:      %{whq_url}/504d6eaa9a0642e6c71aa320cb5ac1e88dc44a01#/%{name}-whq-504d6ea.patch
Patch7410:      %{whq_url}/fa2b372ec02d3755ce892612750238f41b39ad85#/%{name}-whq-fa2b372.patch
Patch7411:      %{whq_url}/e7550069ded02c1f8503a15e155127e1e2c26f6a#/%{name}-whq-e755006.patch
Patch7412:      %{whq_url}/bd54f39766e53f92909bc208e5746497c0dc5d69#/%{name}-whq-bd54f39.patch
Patch7413:      %{whq_url}/53f17314aa97d4aba8d37d76ae878cbae20818bf#/%{name}-whq-53f1731.patch
Patch7414:      %{whq_url}/a09a268faeb29fb6cffd6e422843659793f09ced#/%{name}-whq-a09a268.patch
Patch7415:      %{whq_url}/ed8358393413d52096c56e96b44ee73f15053f91#/%{name}-whq-ed83583.patch
Patch7416:      %{whq_url}/f4e55565470938d31e21f4a35aa14e5a950f81c8#/%{name}-whq-f4e5556.patch
Patch7417:      %{whq_url}/31800a1414a33995eba7c89d65a93d69beee47b3#/%{name}-whq-31800a1.patch
Patch7418:      %{whq_url}/647c54e539c6dcc76c6289bad0fc387274d999eb#/%{name}-whq-647c54e.patch
Patch7419:      %{whq_url}/2c903e9e9bb1254a9fbed60767b56668e675f64e#/%{name}-whq-2c903e9.patch
Patch7420:      %{whq_url}/69f1b12a30bbf28e750206f0ec1ab2c6320abcbd#/%{name}-whq-69f1b12.patch
Patch7421:      %{whq_url}/0720c6cfd0b8c863fd22053c2ca750fd982d49d2#/%{name}-whq-0720c6c.patch
Patch7422:      %{whq_url}/2b76b9f234eb5d4753337d8b080f2c050daae3ff#/%{name}-whq-2b76b9f.patch
Patch7423:      %{whq_url}/1d3e3a1c8d08c75e88734ec00b5a2b412e8d6ca3#/%{name}-whq-1d3e3a1.patch
Patch7424:      %{whq_url}/d29c33a35c56f9a348ca8a8de01b7fe7eb4c4ef4#/%{name}-whq-d29c33a.patch
Patch7425:      %{whq_url}/734a7120b6ca73ac4286fc8efaddf74534b7a513#/%{name}-whq-734a712.patch
Patch7426:      %{whq_url}/f7895ef25a4cb2115ffbe04d28b87bcb6ee3c0b7#/%{name}-whq-f7895ef.patch
Patch7427:      %{whq_url}/93fa2e0ab82a9506fb71bf0f536fa521f58ea88c#/%{name}-whq-93fa2e0.patch
Patch7428:      %{whq_url}/9014dae8fb7b78cdd8a200278a1e2a5caccd533a#/%{name}-whq-9014dae.patch
Patch7429:      %{whq_url}/2a08e0e29025f335acd77f7d899afa7f45240b2b#/%{name}-whq-2a08e0e.patch
Patch7430:      %{whq_url}/7a71f98640bf8fa402d6b0c3ec30b40818710ee7#/%{name}-whq-7a71f98.patch
Patch7431:      %{whq_url}/4f3534fa6f0e4b7ec9e3d446b394afca612e21ba#/%{name}-whq-4f3534f.patch
Patch7432:      %{whq_url}/13abe9e2bd58f636efa2149eee8172f37b5ddef3#/%{name}-whq-13abe9e.patch
Patch7433:      %{whq_url}/1e7e21534e6598782e77c38907573fa0e118e13b#/%{name}-whq-1e7e215.patch
Patch7434:      %{whq_url}/9b7f14f1b49e838f5edc74296fd53b7215a8b52d#/%{name}-whq-9b7f14f.patch
Patch7435:      %{whq_url}/f804d1ac70f0f113ddd0295dcb83707776cdbd2f#/%{name}-whq-f804d1a.patch
Patch7436:      %{whq_url}/94ee27097228ac37f1576565c9f93f6186ff66a3#/%{name}-whq-94ee270.patch
Patch7437:      %{whq_url}/26c078a2a64e515323bfbb4fcbdaf161150942ba#/%{name}-whq-26c078a.patch
Patch7438:      %{whq_url}/dc8085142528305605ef4af621ba56f2aa75da65#/%{name}-whq-dc80851.patch
Patch7439:      %{whq_url}/3d4be8e150bf37607b25dce0db2931384e5cadd7#/%{name}-whq-3d4be8e.patch
Patch7440:      %{whq_url}/5a6341d8c7cbd19308dead261ef67c5c1e5e4f0b#/%{name}-whq-5a6341d.patch
Patch7441:      %{whq_url}/cd8971399e35a8feaa841025ab74857a85bf5678#/%{name}-whq-cd89713.patch
Patch7442:      %{whq_url}/d4052e0d709d7fddcb6a4adc10e98a8e65c8218e#/%{name}-whq-d4052e0.patch
Patch7443:      %{whq_url}/76556bc5885b45f88ca436fb2f04cdf79bc29af0#/%{name}-whq-76556bc.patch
Patch7444:      %{whq_url}/c76dc32feffaeed260bf73499e43012b69bee1b4#/%{name}-whq-c76dc32.patch
Patch7445:      %{whq_url}/ccaaf6957f525f09ba485377a606ce322ab90792#/%{name}-whq-ccaaf69.patch
Patch7446:      %{whq_url}/57a222356cb675beec38268c2736628e0fb3d231#/%{name}-whq-57a2223.patch
Patch7447:      %{whq_url}/06c3e7e44cb40ac2e6e6c55029103d63f47f9e5f#/%{name}-whq-06c3e7e.patch
Patch7448:      %{whq_url}/09ff2436c4b1be1f379aec7e4f0b625c6dbc90e2#/%{name}-whq-09ff243.patch
Patch7449:      %{whq_url}/ac94d8890558bcb34d28ee7c2f276bf994faa8a5#/%{name}-whq-ac94d88.patch
Patch7450:      %{whq_url}/0451e44d957325e9de348b8701058e19ce47dc57#/%{name}-whq-0451e44.patch
Patch7451:      %{whq_url}/43ce429234a568cca6d563e0464acc3cfbbdbd50#/%{name}-whq-43ce429.patch
Patch7452:      %{whq_url}/1d65e474b1a5aa3ea60e6b14c7a49479b35cc7e1#/%{name}-whq-1d65e47.patch
Patch7453:      %{whq_url}/1e7378d80c20fc8f45a246fd043ef4e2911e94f5#/%{name}-whq-1e7378d.patch
Patch7454:      %{whq_url}/225be12999ef8d7e9c8a504d0d26254c9cace568#/%{name}-whq-225be12.patch
Patch7455:      %{whq_url}/81d1c79dcda0eea8fd35b2dcc6dfa3c3a17e2393#/%{name}-whq-81d1c79.patch
Patch7456:      %{whq_url}/447bce4117a58910690a0d2610ebcbdd49ae9127#/%{name}-whq-447bce4.patch
Patch7457:      %{whq_url}/ae07938ba661dc0515673835878710a25c99eec8#/%{name}-whq-ae07938.patch
Patch7458:      %{whq_url}/71090bdc2f5051f181c193ea410e6438b92c9c37#/%{name}-whq-71090bd.patch
Patch7459:      %{whq_url}/00b4a51fcc325fe1a5f2d1dbc7b81dacf4686b4c#/%{name}-whq-00b4a51.patch
Patch7460:      %{whq_url}/4faed406d428a2cec752c2aa1bda8449a1342057#/%{name}-whq-4faed40.patch
Patch7461:      %{whq_url}/3576258402f5e23ad059cf446eafef7fb2c10430#/%{name}-whq-3576258.patch
Patch7462:      %{whq_url}/7444aa42306cd0e091dd46efc2e0be3c7c61b2fa#/%{name}-whq-7444aa4.patch
Patch7463:      %{whq_url}/36fc962f5c0f2fd33cfd09c816017655104c4201#/%{name}-whq-36fc962.patch
Patch7464:      %{whq_url}/f54c7205b6ac387ee394c8877245f0d0f3a3cc7a#/%{name}-whq-f54c720.patch
Patch7465:      %{whq_url}/2306efc3fae152586348a618fce3d8398a883924#/%{name}-whq-2306efc.patch
Patch7466:      %{whq_url}/e8f2c2464a3ce47e84be7786691ba35d25c7e6a8#/%{name}-whq-e8f2c24.patch
Patch7467:      %{whq_url}/c6e0cb6c720c56541ebb45a6b4821d46f0300f36#/%{name}-whq-c6e0cb6.patch
Patch7468:      %{whq_url}/32eb41de8caaa9462406c859c8242df5a6ebf343#/%{name}-whq-32eb41d.patch
Patch7469:      %{whq_url}/6cff65900dd299f596636ca5449b0f99e825cf97#/%{name}-whq-6cff659.patch
Patch7470:      %{whq_url}/2a62242747aa17a1a4ad7443b0ace900f72682c9#/%{name}-whq-2a62242.patch
Patch7471:      %{whq_url}/30596feb03098b392bd5078a1a2d390567681b3c#/%{name}-whq-30596fe.patch
Patch7472:      %{whq_url}/849d08b0aed1b256ac459347cb488ef3db5ce3f9#/%{name}-whq-849d08b.patch
Patch7473:      %{whq_url}/cffd06ea67f34a8f6379c78330c40d55ba83223f#/%{name}-whq-cffd06e.patch
Patch7474:      %{whq_url}/7f8224411c39242fe751524816b1349002066c72#/%{name}-whq-7f82244.patch
Patch7475:      %{whq_url}/8f3bd63b52f03ff05e9d2a00a2e129a0b0092969#/%{name}-whq-8f3bd63.patch
Patch7476:      %{whq_url}/525e7078a83f568d10183327ab3fa6b82d08d41b#/%{name}-whq-525e707.patch
Patch7477:      %{whq_url}/f332f2e4e28e9618e7b4a65e9352915cf9772e93#/%{name}-whq-f332f2e.patch
Patch7478:      %{whq_url}/4a7cd0f492affbc0eb347b97426b8c23f9a4f976#/%{name}-whq-4a7cd0f.patch
Patch7479:      %{whq_url}/53e0bf2f9f0f9876ca89e4c9133d9d5265b3e9dd#/%{name}-whq-53e0bf2.patch
Patch7480:      %{whq_url}/a686759f1d7aee67b5786b72e81a4e4fcf3f3c02#/%{name}-whq-a686759.patch
Patch7481:      %{whq_url}/77fbf3a9fde517ecb4d23e0bc121668206fec2f3#/%{name}-whq-77fbf3a.patch
Patch7482:      %{whq_url}/1721f0ff2759a0dfce166f20653058248f188521#/%{name}-whq-1721f0f.patch
Patch7483:      %{whq_url}/25d4c50db3b2cd5113709b98adfd3de86b6e19ec#/%{name}-whq-25d4c50.patch
Patch7484:      %{whq_url}/de1cb029f6e9bd6b8959695f5d0ae55188d9b723#/%{name}-whq-de1cb02.patch
Patch7485:      %{whq_url}/22f4b6fcf5014b6d98188253636c116e50446c44#/%{name}-whq-22f4b6f.patch
Patch7486:      %{whq_url}/97b5ad7597bf2add39251d7379fc607bf1578478#/%{name}-whq-97b5ad7.patch
Patch7487:      %{whq_url}/a4af2b2b70db96309172b226dc6163e90d565420#/%{name}-whq-a4af2b2.patch
Patch7488:      %{whq_url}/13ea90d80f7275e1ad4f3fc3c1c75b68bdbefbb4#/%{name}-whq-13ea90d.patch
Patch7489:      %{whq_url}/5b3842451ba6c7a37a24e0f16707d8a19020287d#/%{name}-whq-5b38424.patch
Patch7490:      %{whq_url}/7531091f33dcd0dc849cfb5df918e9a331f7a6b8#/%{name}-whq-7531091.patch
Patch7491:      %{whq_url}/0267a04547770fe75147aa025e11045aca5c4ed9#/%{name}-whq-0267a04.patch
Patch7492:      %{whq_url}/5f0d268fffc741171fcf9006012c310128846de5#/%{name}-whq-5f0d268.patch
Patch7493:      %{whq_url}/7ea9f9edeed417a241d607bac282d68bdf5abd36#/%{name}-whq-7ea9f9e.patch
Patch7494:      %{whq_url}/0ec191eb0fd161e3bbd9e92270282d3d81e2cf11#/%{name}-whq-0ec191e.patch
Patch7495:      %{whq_url}/36663d9abd0fc085c1197429a78dfbe86c1dc56a#/%{name}-whq-36663d9.patch
Patch7496:      %{whq_url}/76037ffbeefc7b15b764b4d6079bb6c939176523#/%{name}-whq-76037ff.patch
Patch7497:      %{whq_url}/e24ba09f8f35b146de178e492c8071d1923bfa88#/%{name}-whq-e24ba09.patch
Patch7498:      %{whq_url}/d902c333066e57ba3587ffd72e6a2bf08f9319ca#/%{name}-whq-d902c33.patch
Patch7499:      %{whq_url}/898e121b2e1628e91ebe9dee1c1cf8f959f7cd4c#/%{name}-whq-898e121.patch
Patch7500:      %{whq_url}/8231dbf04961356a74bf026cfd3e359605ddc81e#/%{name}-whq-8231dbf.patch
Patch7501:      %{whq_url}/3c9d10d756746ea21ec83f78de42ede871a0222a#/%{name}-whq-3c9d10d.patch
Patch7502:      %{whq_url}/3f562e0b919083bbb988474d50f70b9c5370e29d#/%{name}-whq-3f562e0.patch
Patch7503:      %{whq_url}/16ed88a95234d844fee9fc19053c5c7f618f92ba#/%{name}-whq-16ed88a.patch
Patch7504:      %{whq_url}/2c3719c7a9b370461d18c4422dd965dda80cb859#/%{name}-whq-2c3719c.patch
Patch7505:      %{whq_url}/9aa885bf37c01df1e8f00852681806ec4c21b040#/%{name}-whq-9aa885b.patch
Patch7506:      %{whq_url}/601175822e9c61ce02e21f20c76daf1b760d6924#/%{name}-whq-6011758.patch
Patch7507:      %{whq_url}/32c618b7c5f5c1891de7833986ad95c9aeec69f9#/%{name}-whq-32c618b.patch
Patch7508:      %{whq_url}/057e7f19407f0291cb4240c23fc391263ba9faa8#/%{name}-whq-057e7f1.patch
Patch7509:      %{whq_url}/8bd95a80f263a8df6873f8e3a8b10fdce4136fc4#/%{name}-whq-8bd95a8.patch
Patch7510:      %{whq_url}/0b3db9dfa2877ff36c10f73b04e97af71ab2f845#/%{name}-whq-0b3db9d.patch
Patch7511:      %{whq_url}/6844ff8a0bda7c0511c3c328f459cc4286bf3c5d#/%{name}-whq-6844ff8.patch
Patch7512:      %{whq_url}/97847eeee8aaaad9b141e14d4468838960ea3093#/%{name}-whq-97847ee.patch
Patch7513:      %{whq_url}/7571fa87df453e404d8b6ca58e2da95340156849#/%{name}-whq-7571fa8.patch
Patch7514:      %{whq_url}/5a151b060a08f36d9a667dec8d0e9fbdbe0851f2#/%{name}-whq-5a151b0.patch
Patch7515:      %{whq_url}/0e939eb969d3bd3caab3d5efea4778db07c00c87#/%{name}-whq-0e939eb.patch
Patch7516:      %{whq_url}/6c7f389c5ee3a1e55835a1c25cfc4160e0f214ea#/%{name}-whq-6c7f389.patch
Patch7517:      %{whq_url}/e40de801b5e757f13e5d699fa22368bf1939d444#/%{name}-whq-e40de80.patch
Patch7518:      %{whq_url}/d2496e2d5c5ea4bde34659ba88cea52e8c27facb#/%{name}-whq-d2496e2.patch
Patch7519:      %{whq_url}/8ea62f2ed13865d866a38b80f24caca02ef72447#/%{name}-whq-8ea62f2.patch
Patch7520:      %{whq_url}/47fe53172971cfd233b30b33cf0d710c6317279c#/%{name}-whq-47fe531.patch
Patch7521:      %{whq_url}/9012096b47d8422a296734ecbedb226188e93501#/%{name}-whq-9012096.patch
Patch7522:      %{whq_url}/aaea13a128b76fa0076b8852187c7d10e5eb5d68#/%{name}-whq-aaea13a.patch
Patch7523:      %{whq_url}/a729af0e9c0027e7f9686df7e3d85ec1ab3cfb37#/%{name}-whq-a729af0.patch
Patch7524:      %{whq_url}/8c0c70dd0f0cccfe1e2c9706f4645e7fce13078c#/%{name}-whq-8c0c70d.patch
Patch7525:      %{whq_url}/41d1fd3229eaaa42f4057fbfa335e0e6d665233e#/%{name}-whq-41d1fd3.patch
Patch7526:      %{whq_url}/bc3284f818f70d2de0bc76beaa69a3352f27fd34#/%{name}-whq-bc3284f.patch
Patch7527:      %{whq_url}/a12e308ebaa226caaaa8e8c932bc2c7687914d21#/%{name}-whq-a12e308.patch
Patch7528:      %{whq_url}/0e7f6e0ed32ffe5fe09ae429037fc28dcbebe6ea#/%{name}-whq-0e7f6e0.patch
Patch7529:      %{whq_url}/4e5811637ad027d01cc5033f76b03e6e8cfdd287#/%{name}-whq-4e58116.patch
Patch7530:      %{whq_url}/482b64effd44a8f601d3327eed84ce6d61432cf3#/%{name}-whq-482b64e.patch
Patch7531:      %{whq_url}/af1a328fa0da4df7a73688528e49a568dcea995e#/%{name}-whq-af1a328.patch
Patch7532:      %{whq_url}/a8ddcf7dfe64b727a0c06d0a008a0ca5b227868c#/%{name}-whq-a8ddcf7.patch
Patch7533:      %{whq_url}/99a6ae5b863b220e72f01abc9ce3ab1c7be9d7f7#/%{name}-whq-99a6ae5.patch
Patch7534:      %{whq_url}/a9639dd6053f1e7de915c29851cc1be45ed537d0#/%{name}-whq-a9639dd.patch
Patch7535:      %{whq_url}/1581fb619b879b58a402bc64ad81bde265b926e8#/%{name}-whq-1581fb6.patch
Patch7536:      %{whq_url}/65c37cee249984884af40d91aa14706d81e128bf#/%{name}-whq-65c37ce.patch
Patch7537:      %{whq_url}/4225ec994e64f365b0b093609a3343c0ae1987f0#/%{name}-whq-4225ec9.patch
Patch7538:      %{whq_url}/b75ae8c31eba2a59e2b32bf8d456ca5756ac6e0d#/%{name}-whq-b75ae8c.patch
Patch7539:      %{whq_url}/e703e2da39a411e1f0aaf6d5ff7a1fa36edb87cd#/%{name}-whq-e703e2d.patch
Patch7540:      %{whq_url}/aef321ec0f9b54cc07071e0757c57b73210f304c#/%{name}-whq-aef321e.patch
Patch7541:      %{whq_url}/75e616d52b452d37cc93f492d47eba641f9741c1#/%{name}-whq-75e616d.patch
Patch7542:      %{whq_url}/3863b243fe5ef4e223a809e93a85e858952dd754#/%{name}-whq-3863b24.patch
Patch7543:      %{whq_url}/8b5e0bdf8b9db3ab19bbabdb2ce591f5fc876ac7#/%{name}-whq-8b5e0bd.patch
Patch7544:      %{whq_url}/15684bd5aa557562072a749ab4782489fcd27546#/%{name}-whq-15684bd.patch
Patch7545:      %{whq_url}/029843176b11404a77384b40ca3e9a99226477fe#/%{name}-whq-0298431.patch
Patch7546:      %{whq_url}/eb293d7645eddbac8e94086a58d460b4407f4b58#/%{name}-whq-eb293d7.patch
Patch7547:      %{whq_url}/e5bd1ba4ad4802c3f589fc91b8953205af52a978#/%{name}-whq-e5bd1ba.patch
Patch7548:      %{whq_url}/21c99970f3c423e2b8b1f92b2b44c5dce7cc28bf#/%{name}-whq-21c9997.patch
Patch7549:      %{whq_url}/7ca68a86313e39d21cc92eac84a00841318143ae#/%{name}-whq-7ca68a8.patch
Patch7550:      %{whq_url}/df8578da8ef4f6e9e480e1c49cd82ebdf8281d38#/%{name}-whq-df8578d.patch
Patch7551:      %{whq_url}/151b42953b49bc0417c53656b0040ef765a8cbef#/%{name}-whq-151b429.patch
Patch7552:      %{whq_url}/01c05387ce56ad99bd0b629a41317d7058a82462#/%{name}-whq-01c0538.patch
Patch7553:      %{whq_url}/f4661f1b38c479bd08baee93d9ddb1f9e93c173d#/%{name}-whq-f4661f1.patch
Patch7554:      %{whq_url}/2b9a0550bcda166afdf852370397e1041c096f5f#/%{name}-whq-2b9a055.patch
Patch7555:      %{whq_url}/58f2326410dd5574e52ab3362b67ab345674c3b1#/%{name}-whq-58f2326.patch
Patch7556:      %{whq_url}/2b40969c58a099f958c58909b666915991a42979#/%{name}-whq-2b40969.patch
Patch7557:      %{whq_url}/2de4f12b33724af2f90607a0626d75e8fbf8e4da#/%{name}-whq-2de4f12.patch
Patch7558:      %{whq_url}/2d544ff8a038ac20c278d0e8f2de4c5478ff6d95#/%{name}-whq-2d544ff.patch
Patch7559:      %{whq_url}/ff88ed8b0652e8fc202893c65258a012e650ebbe#/%{name}-whq-ff88ed8.patch
Patch7560:      %{whq_url}/3803997349efdd2860263d08bd9d71bc0702cd2c#/%{name}-whq-3803997.patch
Patch7561:      %{whq_url}/8aa370e9919f179feeece8dac9782f90f2e2b09c#/%{name}-whq-8aa370e.patch
Patch7562:      %{whq_url}/13e81421b7f1c9cfe1d6a5a7738ac728c662788c#/%{name}-whq-13e8142.patch
Patch7563:      %{whq_url}/c1c61bf2559509b33fc8bdd297032bc57e474229#/%{name}-whq-c1c61bf.patch
Patch7564:      %{whq_url}/2dbf14ee80583e7fa8da74cfaa85700cb82f4f70#/%{name}-whq-2dbf14e.patch
Patch7565:      %{whq_url}/af47236499235349187c00a9be981a713fa5041c#/%{name}-whq-af47236.patch
Patch7566:      %{whq_url}/26e04d52fe466e44eb5ca383c94c2920c5e294ec#/%{name}-whq-26e04d5.patch
Patch7567:      %{whq_url}/518d06404ad70aa9812a77d019a18fe79c16f831#/%{name}-whq-518d064.patch
Patch7568:      %{whq_url}/c0ab7af1b0553e6177fad872d95e4195582e4d94#/%{name}-whq-c0ab7af.patch
Patch7569:      %{whq_url}/541b06747ae4a64d0e39ed010b256b9326490701#/%{name}-whq-541b067.patch
Patch7570:      %{whq_url}/85a33ff731bf82e229a2c6aa386d36fa4a90da65#/%{name}-whq-85a33ff.patch
Patch7571:      %{whq_url}/81a08cea79afccdf4daddda5936c05a30849f83a#/%{name}-whq-81a08ce.patch
Patch7572:      %{whq_url}/1a9558cf9bda654950e389532b400023ecbd81c0#/%{name}-whq-1a9558c.patch
Patch7573:      %{whq_url}/c2c330532e96cc0cf5ba30f784d195fea90a4366#/%{name}-whq-c2c3305.patch
Patch7574:      %{whq_url}/f7e4fd0cf8f5237614474a6e5dcdad24a6a1dcdd#/%{name}-whq-f7e4fd0.patch
Patch7575:      %{whq_url}/9e973954fdfd2f9e22545bb6311053c835861193#/%{name}-whq-9e97395.patch
Patch7576:      %{whq_url}/7d3503d83ece320ed023297e12d766e487383462#/%{name}-whq-7d3503d.patch
Patch7577:      %{whq_url}/f9c89932595c874cf9eb6fc8d3244d89ff55bbf8#/%{name}-whq-f9c8993.patch
Patch7578:      %{whq_url}/82e8fd97f6996a13ecdd0c827336e0681e2216a3#/%{name}-whq-82e8fd9.patch
Patch7579:      %{whq_url}/b23ef1d836bada90df71ce9730f68088e0124226#/%{name}-whq-b23ef1d.patch
Patch7580:      %{whq_url}/9864f9c024ad6e45d2e4369dca7418bc9121d727#/%{name}-whq-9864f9c.patch
Patch7581:      %{whq_url}/00a0e2cd8c4df240371ddd22516e4e3544a142ce#/%{name}-whq-00a0e2c.patch
Patch7582:      %{whq_url}/74dc9aa33502ba89333ab4be3c7c1458015c1d56#/%{name}-whq-74dc9aa.patch
Patch7583:      %{whq_url}/52e9baddbce3f6d8aa768379ec6d7e82b47545c6#/%{name}-whq-52e9bad.patch
Patch7584:      %{whq_url}/f51cd0a1b5383506c5b1a535f702acab42898d08#/%{name}-whq-f51cd0a.patch
Patch7585:      %{whq_url}/4c45348f7808c3a1ea635e196402951f0008ab90#/%{name}-whq-4c45348.patch
Patch7586:      %{whq_url}/7b96e82fd569bc3b261be147abe49a822f14d4e0#/%{name}-whq-7b96e82.patch
Patch7587:      %{whq_url}/5b4b8774888b58ed424c46383d709c8e39345112#/%{name}-whq-5b4b877.patch
Patch7588:      %{whq_url}/1c2b14a5240cdf18576552b1a81c6b7e17ff3a91#/%{name}-whq-1c2b14a.patch
Patch7589:      %{whq_url}/30e5250622f40037a58dd87517267dbab88c5df3#/%{name}-whq-30e5250.patch
Patch7590:      %{whq_url}/61f3b3dcdf759537fe83b86837e2ef341a2c8b66#/%{name}-whq-61f3b3d.patch
Patch7591:      %{whq_url}/74deee7df0abd7e05b433f875e86e26d7e2f447f#/%{name}-whq-74deee7.patch
Patch7592:      %{whq_url}/72b97eeba0d934ed2c8607f45429664130dd8f5f#/%{name}-whq-72b97ee.patch
Patch7593:      %{whq_url}/4e80f2ea5e350168933599ab7ad633254717e93c#/%{name}-whq-4e80f2e.patch
Patch7594:      %{whq_url}/2d91f7def15cb0df65fdb87c19e24a5a6c99839e#/%{name}-whq-2d91f7d.patch
Patch7595:      %{whq_url}/d99a454a6bead9aaa5c55705d4807b416d2855a3#/%{name}-whq-d99a454.patch
Patch7596:      %{whq_url}/5bbd8130adf9f4b0e6b45c5309484c2aaffcd8cd#/%{name}-whq-5bbd813.patch
Patch7597:      %{whq_url}/7fe03dbf21196d40ad533f6acf2e216fb48540d6#/%{name}-whq-7fe03db.patch
Patch7598:      %{whq_url}/4ba7c42370e6a1de17f3a5eb72c87950f9319425#/%{name}-whq-4ba7c42.patch
Patch7599:      %{whq_url}/787df87badf606fe6589d17b9728dfe58cb524b5#/%{name}-whq-787df87.patch
Patch7600:      %{whq_url}/298fa4a7f0fb8f97923a2a86c6e42b6e060e062b#/%{name}-whq-298fa4a.patch
Patch7601:      %{whq_url}/3038674eefd67681c187521d10a28f0460a2fd96#/%{name}-whq-3038674.patch
Patch7602:      %{whq_url}/4100c43576af4953f32b646fddb7987cd019d869#/%{name}-whq-4100c43.patch
Patch7603:      %{whq_url}/cd193e44a58f542a919e3c59a82c64e6d2393b76#/%{name}-whq-cd193e4.patch
Patch7604:      %{whq_url}/f3322891420d4d7c5a1c506a25ef4f99d21b2f8e#/%{name}-whq-f332289.patch
Patch7605:      %{whq_url}/3885b32bc8995bbb171ffdc7af7d402df1b0534e#/%{name}-whq-3885b32.patch
Patch7606:      %{whq_url}/36ebdfc6b647aaaac1298a03269420fab5de5880#/%{name}-whq-36ebdfc.patch
Patch7607:      %{whq_url}/cc9d69b20bda583142288b0cfb0ab472348a2b51#/%{name}-whq-cc9d69b.patch
Patch7608:      %{whq_url}/3395ee3631fe7088d33d5fd53f0e788741157e6a#/%{name}-whq-3395ee3.patch
Patch7609:      %{whq_url}/0c857e92cb424bd7189b76b4035926f1688ab1e9#/%{name}-whq-0c857e9.patch
Patch7610:      %{whq_url}/7ec069d85f5235db98e57291825b9d602ae47ed5#/%{name}-whq-7ec069d.patch
Patch7611:      %{whq_url}/4826900a30a431faa8bcc9e3f0007f794d8d15bb#/%{name}-whq-4826900.patch
Patch7612:      %{whq_url}/a9a08dbc3dd8b595888f6c6b066e6c8fd389771a#/%{name}-whq-a9a08db.patch
Patch7613:      %{whq_url}/595f2846b2064a6ebeb0b02133e2d68851fb1c06#/%{name}-whq-595f284.patch
Patch7614:      %{whq_url}/33be1cf598b0319855bf14ee88a0120636df6032#/%{name}-whq-33be1cf.patch
Patch7615:      %{whq_url}/a8ccb7fa04cae768214e649928e1ee10804f0c41#/%{name}-whq-a8ccb7f.patch
Patch7616:      %{whq_url}/ed64fd72a7ab48f5f48e7dcbd4d666f851365993#/%{name}-whq-ed64fd7.patch
Patch7617:      %{whq_url}/e151e4c8a12281306caee136edfa24cadeabde59#/%{name}-whq-e151e4c.patch
Patch7618:      %{whq_url}/e58ef508a935e69f26c614063346d4ba67667cbe#/%{name}-whq-e58ef50.patch
Patch7619:      %{whq_url}/b07cc3fe0c02ac9ea7be5263657f82a68c76e181#/%{name}-whq-b07cc3f.patch
Patch7620:      %{whq_url}/b211bd7b6449e3a67bb0ecf5c113981eefa0dbb4#/%{name}-whq-b211bd7.patch
Patch7621:      %{whq_url}/a204ad557dd504391e13e1382278472cd86517f4#/%{name}-whq-a204ad5.patch
Patch7622:      %{whq_url}/82acb284bda2fe655ce0ff51b18667f1c9311e30#/%{name}-whq-82acb28.patch
Patch7623:      %{whq_url}/5adb93c654aab78f26f40b83ebca39af0326ba6d#/%{name}-whq-5adb93c.patch
Patch7624:      %{whq_url}/96e5ac876fd48c3692a2b89780e7bb40fe526798#/%{name}-whq-96e5ac8.patch
Patch7625:      %{whq_url}/ec02224941eedf16b8b043964519f6363b5ce21f#/%{name}-whq-ec02224.patch
Patch7626:      %{whq_url}/e9090e1c903578b30118ce9559c1824361abc6da#/%{name}-whq-e9090e1.patch
Patch7627:      %{whq_url}/c487f21b6b95f1fda2f80920135e8481dc86e4a6#/%{name}-whq-c487f21.patch
Patch7628:      %{whq_url}/d0946955ec21e4da57aaec92459f81f131b27a49#/%{name}-whq-d094695.patch
Patch7629:      %{whq_url}/c4ae13e31264616757200cd97700724ffe37e602#/%{name}-whq-c4ae13e.patch
Patch7630:      %{whq_url}/947fe11e02f0cb227f571a26625ef4cbddf93030#/%{name}-whq-947fe11.patch
Patch7631:      %{whq_url}/655ab7a84f1442ebc185a09acd06611cac1a3eb2#/%{name}-whq-655ab7a.patch
Patch7632:      %{whq_url}/53d956700adf17eb14e02292ee520cdcc8e7ba99#/%{name}-whq-53d9567.patch
Patch7633:      %{whq_url}/4935576d4a5cb13bc58eebfca1ca43bc43866ff9#/%{name}-whq-4935576.patch
Patch7634:      %{whq_url}/22628bcc1742273affa85cbafb0e494922f424f7#/%{name}-whq-22628bc.patch
Patch7635:      %{whq_url}/f2d60c16eacb538566e4f750f3476b2ef3b3e2ec#/%{name}-whq-f2d60c1.patch
Patch7636:      %{whq_url}/5ced4a705a544f9a91fd38669b3907559b3a575e#/%{name}-whq-5ced4a7.patch
Patch7637:      %{whq_url}/ab6056d6774310162ef268ca6af5e3ad2e556a4e#/%{name}-whq-ab6056d.patch
Patch7638:      %{whq_url}/5d96c5aac883b343ddcfbe6f6b1b96ad6827a46b#/%{name}-whq-5d96c5a.patch
Patch7639:      %{whq_url}/129149d212e607ff2df8619085d57cb7d7fb09da#/%{name}-whq-129149d.patch
Patch7640:      %{whq_url}/a26bb7b2ef50cf0d1360b35b093b7e4ef11aa6d0#/%{name}-whq-a26bb7b.patch
Patch7641:      %{whq_url}/24021931a88ed917bc2b52c0914c059c2d8d2f30#/%{name}-whq-2402193.patch
Patch7642:      %{whq_url}/820d703c3182de41a175f6dddf339b9f6147734f#/%{name}-whq-820d703.patch

# Reverts to unbreak fshack
Patch8000:       %{whq_url}/2538b0100fbbe1223e7c18a52bade5cfe5f8d3e3#/%{name}-whq-2538b01.patch
Patch8001:       %{whq_url}/fd6f50c0d3e96947846ca82ed0c9bd79fd8e5b80#/%{name}-whq-fd6f50c.patch
Patch8002:       %{whq_url}/26b26a2e0efcb776e7b0115f15580d2507b10400#/%{name}-whq-26b26a2.patch
Patch8003:       %{whq_url}/8cd6245b7633abccd68f73928544ae4de6f76d52#/%{name}-whq-8cd6245.patch
Patch8004:       %{whq_url}/707fcb99a60015fcbb20c83e9031bc5be7a58618#/%{name}-whq-707fcb9.patch
Patch8005:       %{whq_url}/e3eb89d5ebb759e975698b97ed8b547a9de3853f#/%{name}-whq-e3eb89d.patch
Patch8006:       %{whq_url}/145cfce1135a7e59cc4c89cd05b572403f188161#/%{name}-whq-145cfce.patch
Patch8007:       %{whq_url}/6f9d20806e821ab07c8adf81ae6630fae94b00ef#/%{name}-whq-6f9d208.patch
Patch8008:       %{whq_url}/3a3c7cbd209e23cc6ee88299b3ba877ab20a767f#/%{name}-whq-3a3c7cb.patch
Patch8009:       %{whq_url}/0b0ac41981006514616abdd4c4b6922cf66be7b6#/%{name}-whq-0b0ac41.patch
Patch8010:       %{whq_url}/679ff720902b8e5d5d750b980084bdcdc9a051ed#/%{name}-whq-679ff72.patch
Patch8011:       %{whq_url}/6f305dd881e16f77f9eb183684d04b0b8746b769#/%{name}-whq-6f305dd.patch
Patch8012:       %{whq_url}/2a6de8d7f7d6f5ac018d8e330cfa580fc0c3b9e5#/%{name}-whq-2a6de8d.patch
Patch8013:       %{whq_url}/a8b4cf7f2d3d1fbd79308a106a84e753cdac69e8#/%{name}-whq-a8b4cf7.patch
Patch8014:       %{whq_url}/f5e6c086f91749e9e302c1abf858807535bc9775#/%{name}-whq-f5e6c08.patch
Patch8015:       %{whq_url}/45d991d54138523e5278db5618eb458100982294#/%{name}-whq-45d991d.patch
Patch8016:       %{whq_url}/9905a5a81d6baf59e992c5b2a8ea92ee4054e5d6#/%{name}-whq-9905a5a.patch
Patch8017:       %{whq_url}/7dd52f6d24f372f08ab71f0acbb0a2b028d390ba#/%{name}-whq-7dd52f6.patch
Patch8018:       %{whq_url}/0d42388095e4fd5c7702a61824b01ce0f9fc4d74#/%{name}-whq-0d42388.patch
Patch8019:       %{whq_url}/4a2481631331e2743476ea4e1b0005f8f5024242#/%{name}-whq-4a24816.patch
Patch8020:       %{whq_url}/d13b61b7385a6a380fb91720c511b194926fa0ca#/%{name}-whq-d13b61b.patch
Patch8021:       %{whq_url}/5491e939bc22f0ab479aec6b8a525be9c5ff5e35#/%{name}-whq-5491e93.patch
Patch8022:       %{whq_url}/2116b49717f26802b51e2904de8d74651da33545#/%{name}-whq-2116b49.patch
Patch8023:       %{whq_url}/9c99d9bceba34559a32f1e5906a6fcbcf91b0004#/%{name}-whq-9c99d9b.patch
Patch8024:       %{whq_url}/b45c04f4c352ef81df5312684008839f4eeee03d#/%{name}-whq-b45c04f.patch
Patch8025:       %{whq_url}/440fab3870b3c9ea778031ec51db69f8c3a687f5#/%{name}-whq-440fab3.patch
Patch8026:       %{whq_url}/2b484b1ac7a5510be54cb5341143d89dc1924b37#/%{name}-whq-2b484b1.patch
Patch8027:       %{whq_url}/fd29fe4ea73d87e39bd3d0ddd791c14f536508b7#/%{name}-whq-fd29fe4.patch
Patch8028:       %{whq_url}/1aa7c9af90c340f45e03c6b94525704ad19eb657#/%{name}-whq-1aa7c9a.patch
Patch8029:       %{whq_url}/f04360cfbec574dc37675df141ef8fc14e1302ba#/%{name}-whq-f04360c.patch
Patch8030:       %{whq_url}/715a04daabdab616b530ef5a937827df7c2523c3#/%{name}-whq-715a04d.patch
Patch8031:       %{whq_url}/d9625e5a01a52496d1fb7f1a9a691fd3ec8332db#/%{name}-whq-d9625e5.patch
Patch8032:       %{whq_url}/586f68f414924b1e41fec10a72b1aacced068885#/%{name}-whq-586f68f.patch

Patch801:       %{tkg_url}/hotfixes/01150d7f/06877e55b1100cc49d3726e9a70f31c4dfbe66f8-92.mystagingpatch#/%{name}-tkg-06877e5_revert-92.patch
Patch802:       %{tkg_url}/hotfixes/01150d7f/934a09585a15e8491e422b43624ffe632b02bd3c-3.mystagingpatch#/%{name}-tkg-934a095_revert-3.patch
Patch803:       %{tkg_url}/hotfixes/01150d7f/ntdll-ForceBottomUpAlloc-97fbe3f.mystagingpatch#/%{name}-tkg-ntdll-ForceBottomUpAlloc-97fbe3f.patch
Patch804:       %{tkg_url}/hotfixes/01150d7f/staging-rawinput-esync-nofshack-fix-2.mystagingpatch#/%{name}-tkg-staging-rawinput-esync-nofshack-fix-2.patch
Patch805:       %{tkg_url}/hotfixes/01150d7f/001-3a9edf9aad43c3e8ba724571da5381f821f1dc56.myearlypatch#/%{name}-tkg-001-3a9edf9_early.patch
Patch806:       %{tkg_url}/hotfixes/01150d7f/002-e0e3b6bc91f7db956e3a66f2938eea45d4055a39.myearlypatch#/%{name}-tkg-002-e0e3b6b_early.patch
Patch807:       %{tkg_url}/hotfixes/01150d7f/003-1e7378d8-447bce41.myearlypatch#/%{name}-tkg-003-1e7378d8-447bce41_early.patch

%if 0%{?wine_staging}
# wine staging patches for wine-staging
Source900:       https://github.com/wine-staging/wine-staging/archive/%{?strel}%{wine_stagingver}/wine-staging-%{stpkgver}.tar.gz

# https://github.com/Tk-Glitch/PKGBUILDS/wine-tkg-git/wine-tkg-patches
Patch1000:       %{tkg_url}/proton/use_clock_monotonic.patch#/%{name}-tkg-use_clock_monotonic.patch
Patch1002:       %{tkg_url}/proton/FS_bypass_compositor.patch#/%{name}-tkg-FS_bypass_compositor.patch
Patch1003:       %{tkg_url}/misc/childwindow.patch#/%{name}-tkg-childwindow.patch
Patch1004:       %{tkg_url}/misc/steam.patch#/%{name}-tkg-steam.patch
Patch1005:       %{tkg_url}/misc/CSMT-toggle.patch#/%{name}-tkg-CSMT-toggle.patch
Patch1006:       %{tkg_url}/misc/d3d12-fixes.patch#/%{name}-tkg-d3d12-fixes.patch

# fsync
Patch1020:       %{tkg_url}/proton/fsync-staging.patch#/%{name}-tkg-fsync-staging.patch
Patch1022:       %{tkg_url}/proton/fsync-spincounts.patch#/%{name}-tkg-fsync-spincounts.patch
# FS Hack
Patch1023:       %{tkg_url}/proton/valve_proton_fullscreen_hack-staging.patch#/%{name}-tkg-valve_proton_fullscreen_hack-staging.patch
Patch1024:       %{tkg_url}/proton/proton-rawinput.patch#/%{name}-tkg-proton-rawinput.patch
Patch1025:       %{tkg_url}/proton/proton_mf_hacks.patch#/%{name}-tkg-proton_mf_hacks.patch
Patch1026:       %{tkg_url}/proton/LAA-staging.patch#/%{name}-tkg-LAA-staging.patch
Patch1027:       %{tkg_url}/proton-tkg-specific/proton-staging_winex11-MWM_Decorations.patch#/%{name}-tkg-proton-staging_winex11-MWM_Decorations.patch
Patch1028:       %{valve_url}/commit/a1e5640b60439f0df83fc24c8a69629cef2c6c67.patch#/%{name}-valve-a1e5640.patch
Patch1029:       %{tkg_url}/proton-tkg-specific/proton-tkg-staging.patch#/%{name}-tkg-proton-tkg-staging.patch
Patch1030:       %{tkg_url}/proton-tkg-specific/proton-pa-staging.patch#/%{name}-tkg-proton-pa-staging.patch
Patch1031:       %{tkg_url}/proton-tkg-specific/proton-vk-bits-4.5.patch#/%{name}-tkg-proton-vk-bits-4.5.patch
Patch1032:       %{tkg_url}/proton/proton_fs_hack_integer_scaling.patch#/%{name}-tkg-proton_fs_hack_integer_scaling.patch
Patch1033:       %{tkg_url}/proton/proton-winevulkan.patch#/%{name}-tkg-proton-winevulkan.patch
Patch1034:       %{tkg_url}/proton/proton-winevulkan-nofshack.patch#/%{name}-tkg-proton-winevulkan-nofshack.patch
Patch1035:       %{tkg_url}/proton/proton-win10-default-staging.patch#/%{name}-tkg-proton-win10-default-staging.patch

Patch1090:       revert-grab-fullscreen.patch
Patch1091:       %{valve_url}/commit/a09b82021c8d5b167a7c9773a6b488d708232b6c.patch#/%{name}-valve-a09b820.patch
Patch1092:       %{valve_url}/commit/35ff7c5c657d143a96c419346ef516e50815cdfb.patch#/%{name}-valve-35ff7c5.patch
Patch1093:       %{tkg_url}/hotfixes/01150d7f/d8d6a6b2e639d2e29e166a3faf988b81388ae191.mypatch#/%{name}-tkg-d8d6a6b.patch
Patch1094:       %{tkg_url}/hotfixes/01150d7f/origin_3078f10d_fix.mypatch#/%{name}-tkg-origin_3078f10d_fix.patch
Patch1095:       %{tkg_url}/hotfixes/01150d7f/001-SMBIOS-0720c6cf.mypatch#/%{name}-tkg-001-SMBIOS-0720c6c.patch
Patch1096:       %{tkg_url}/hotfixes/01150d7f/002-SMBIOS-d29c33a3.mypatch#/%{name}-tkg-002-SMBIOS-d29c33a3.patch
Patch1097:       %{tkg_url}/hotfixes/01150d7f/001-8622eb326fb8120fc038e27947e61677d4124f15-staging.mypatch#/%{name}-tkg-001-8622eb3-staging.patch
Patch1098:       0001-hotfix-rebased-f2d60c1.patch

# https://bugs.winehq.org/show_bug.cgi?id=48032
Patch1200:       %{tkg_curl}/origin_downloads_e4ca5dbe_revert.mypatch#/%{name}-tkg-origin_downloads_e4ca5dbe_revert.patch
Patch1201:       %{tkg_curl}/guy1524_mfplat_WIP.mypatch#/%{name}-tkg-guy1524_mfplat_WIP.patch

Patch1300:       %{ge_url}/game-patches/nier.patch#/%{name}-ge-nier.patch
Patch1301:       nier-nofshack.patch

%if 0%{?pba}
# acomminos PBA patches
Source3001:     wine-README-pba
Patch3000:      %{tkg_url}/PBA/PBA317+.patch#/%{name}-tkg-PBA317+.patch
%endif

# Patch the patch
Patch5000:      0001-chinforpms-message.patch
# Fix vulkan crash with x86
Patch5001:      wine-fix-i686-gcc10.patch

%endif

%if !0%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%else
ExclusiveArch:  %{ix86} %{arm}
%endif

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
BuildRequires:  automake
%ifarch aarch64
BuildRequires:  clang >= 5.0
%else
BuildRequires:  gcc
%endif
%if 0%{?wine_mingw}
%ifarch %{ix86} x86_64
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
%endif
%endif
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  fontforge
BuildRequires:  icoutils
BuildRequires:  patchutils
BuildRequires:  perl-generators
BuildRequires:  python3
BuildRequires:  pkgconfig(alsa)
BuildRequires:  cups-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(faudio)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glut)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  fontpackages-devel
BuildRequires:  gettext-devel
BuildRequires:  giflib-devel
BuildRequires:  gsm-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  libieee1284-devel
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libmpg123)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  librsvg2
BuildRequires:  librsvg2-tools
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libvkd3d)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(netapi)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  pkgconfig(odbc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  opencl-headers
BuildRequires:  openldap-devel
BuildRequires:  pkgconfig(osmesa)
BuildRequires:  pkgconfig(sane-backends)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xxf86dga)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libappstream-glib

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
%if 0%{?gtk3}
BuildRequires:  pkgconfig(gtk+-3.0)
%endif
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(libva)
%endif

Requires:       wine-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-desktop = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
Requires:       wine-core(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       mesa-dri-drivers(x86-64)
%endif

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mesa-dri-drivers
Requires:       samba-winbind-clients
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       mesa-dri-drivers(aarch-64)
%endif

%description
Wine as a compatibility layer for UNIX to run Windows applications. This
package includes a program loader, which allows unmodified Windows
3.x/9x/NT binaries to run on x86 and x86_64 Unixes. Wine can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the
wine-* sub packages.

%package core
Summary:        Wine core package
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives

# require -filesystem
Requires:       wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch %{ix86}
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-32)
Requires:       freetype(x86-32)
Requires:       nss-mdns(x86-32)
Requires:       gnutls(x86-32)
Requires:       gstreamer1-plugins-good(x86-32)
Requires:       libgcrypt(x86-32)
Requires:       libxslt(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXinerama(x86-32)
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libjpeg(x86-32)
Requires:       libpng(x86-32)
Requires:       libpcap(x86-32)
Requires:       libtiff(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       samba-libs(x86-32)
Requires:       unixODBC(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
%if 0%{?gtk3}
Requires:       gtk3(x86-32)
%endif
Requires:       libva(x86-32)
%endif
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       nss-mdns(x86-64)
Requires:       gnutls(x86-64)
Requires:       gstreamer1-plugins-good(x86-64)
Requires:       libgcrypt(x86-64)
Requires:       libxslt(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXinerama(x86-64)
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libjpeg(x86-64)
Requires:       libpng(x86-64)
Requires:       libpcap(x86-64)
Requires:       libtiff(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       samba-libs(x86-64)
Requires:       unixODBC(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
%if 0%{?gtk3}
Requires:       gtk3(x86-64)
%endif
Requires:       libva(x86-64)
%endif
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gnutls
Requires:       gstreamer1-plugins-good
Requires:       libgcrypt
Requires:       libXrender
Requires:       libXcursor
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libjpeg
Requires:       libpng
Requires:       libpcap
Requires:       libtiff
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan-loader
%if 0%{?wine_staging}
%if 0%{?gtk3}
Requires:       gtk3
%endif
Requires:       libva
%endif
%endif

# removed as of 1.7.35
Obsoletes:      wine-wow < 1.7.35
Provides:       wine-wow = %{version}-%{release}

%description core
Wine core package includes the basic wine stuff needed by all other packages.

%package systemd
Summary:        Systemd config for the wine binfmt handler
Requires:       systemd >= 23
BuildArch:      noarch
Requires(post):  systemd
Requires(postun): systemd
Obsoletes:      wine-sysvinit < %{version}-%{release}

%description systemd
Register the wine binary handler for windows executables via systemd binfmt
handling. See man binfmt.d for further information.

%package filesystem
Summary:        Filesystem directories for wine
BuildArch:      noarch

%description filesystem
Filesystem directories and basic configuration for wine.

%package common
Summary:        Common files
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description common
Common wine files and scripts.

%package desktop
Summary:        Desktop integration features for wine
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-systemd = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package fonts
Summary:       Wine font files
BuildArch:     noarch
# arial-fonts are available with staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-arial-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Obsoletes:     wine-arial-fonts <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:      wine-courier-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-fixedsys-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-small-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-system-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-marlett-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-tahoma-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
# times-new-roman-fonts are available with staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-times-new-roman-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Obsoletes:     wine-times-new-roman-fonts <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:      wine-symbol-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-webdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-wingdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
Requires:      liberation-narrow-fonts

%description fonts
%{summary}

%if 0%{?wine_staging}
%package arial-fonts
Summary:       Wine Arial font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description arial-fonts
%{summary}
%endif

%package courier-fonts
Summary:       Wine Courier font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description courier-fonts
%{summary}

%package fixedsys-fonts
Summary:       Wine Fixedsys font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description fixedsys-fonts
%{summary}

%package small-fonts
Summary:       Wine Small font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description small-fonts
%{summary}

%package system-fonts
Summary:       Wine System font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description system-fonts
%{summary}


%package marlett-fonts
Summary:       Wine Marlett font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description marlett-fonts
%{summary}


%package ms-sans-serif-fonts
Summary:       Wine MS Sans Serif font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description ms-sans-serif-fonts
%{summary}

# rhbz#693180
# http://lists.fedoraproject.org/pipermail/devel/2012-June/168153.html
%package tahoma-fonts
Summary:       Wine Tahoma font family
BuildArch:     noarch
Requires:      wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%description tahoma-fonts
%{summary}
Please note: If you want system integration for wine tahoma fonts install the
wine-tahoma-fonts-system package.

%package tahoma-fonts-system
Summary:       Wine Tahoma font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-tahoma-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description tahoma-fonts-system
%{summary}

%if 0%{?wine_staging}
%package times-new-roman-fonts
Summary:       Wine Times New Roman font family
BuildArch:     noarch
Requires:      wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%description times-new-roman-fonts
%{summary}
Please note: If you want system integration for wine times new roman fonts install the
wine-times-new-roman-fonts-system package.

%package times-new-roman-fonts-system
Summary:       Wine Times New Roman font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-times-new-roman-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description times-new-roman-fonts-system
%{summary}
%endif

%package symbol-fonts
Summary:       Wine Symbol font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description symbol-fonts
%{summary}

%package webdings-fonts
Summary:       Wine Webdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description webdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-webdings-fonts-system package.

%package webdings-fonts-system
Summary:       Wine Webdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-webdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description webdings-fonts-system
%{summary}

%package wingdings-fonts
Summary:       Wine Wingdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description wingdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-wingdings-fonts-system package.

%package wingdings-fonts-system
Summary:       Wine Wingdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-wingdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description wingdings-fonts-system
%{summary}


%package ldap
Summary: LDAP support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description ldap
LDAP support for wine

%package cms
Summary: Color Management for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description cms
Color Management for wine

%package twain
Summary: Twain support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
%ifarch %{ix86}
Requires: sane-backends-libs(x86-32)
%endif
%ifarch x86_64
Requires: sane-backends-libs(x86-64)
%endif
%ifarch %{arm} aarch64
Requires: sane-backends-libs
%endif

%description twain
Twain support for wine

%package capi
Summary: ISDN support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description capi
ISDN support for wine

%package devel
Summary: Wine development environment
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package pulseaudio
Summary: Pulseaudio support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
# midi output
Requires: wine-alsa%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description pulseaudio
This package adds a pulseaudio driver for wine.

%package alsa
Summary: Alsa support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description alsa
This package adds an alsa driver for wine.

%package openal
Summary: Openal support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description openal
This package adds an openal driver for wine.

%package opencl
Summary: OpenCL support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%Description opencl
This package adds the opencl driver for wine.

%prep
%if 0%{?with_snapshot}
%setup -q -n %{name}-%{commit}
%else
%setup -q -n %{name}-%{ver}
%endif

%patch511 -p1 -b.cjk
%patch599 -p1

%patch101 -p1

%if 0%{?wine_staging}
%patch7642 -p1 -R
%patch7641 -p1 -R
%patch7640 -p1 -R
%patch7639 -p1 -R
%patch7638 -p1 -R
%patch7637 -p1 -R
%patch7636 -p1 -R
%patch7635 -p1 -R
%patch7634 -p1 -R
%patch7633 -p1 -R
%patch7632 -p1 -R
%patch7631 -p1 -R
%patch7630 -p1 -R
%patch7629 -p1 -R
%patch7628 -p1 -R
%patch7627 -p1 -R
%patch7626 -p1 -R
%patch7625 -p1 -R
%patch7624 -p1 -R
%patch7623 -p1 -R
%patch7622 -p1 -R
%patch7621 -p1 -R
%patch7620 -p1 -R
%patch7619 -p1 -R
%patch7618 -p1 -R
%patch7617 -p1 -R
%patch7616 -p1 -R
%patch7615 -p1 -R
%patch7614 -p1 -R
%patch7613 -p1 -R
%patch7612 -p1 -R
%patch7611 -p1 -R
%patch7610 -p1 -R
%patch7609 -p1 -R
%patch7608 -p1 -R
%patch7607 -p1 -R
%patch7606 -p1 -R
%patch7605 -p1 -R
%patch7604 -p1 -R
%patch7603 -p1 -R
%patch7602 -p1 -R
%patch7601 -p1 -R
%patch7600 -p1 -R
%patch7599 -p1 -R
%patch7598 -p1 -R
%patch7597 -p1 -R
%patch7596 -p1 -R
%patch7595 -p1 -R
%patch7594 -p1 -R
%patch7593 -p1 -R
%patch7592 -p1 -R
%patch7591 -p1 -R
%patch7590 -p1 -R
%patch7589 -p1 -R
%patch7588 -p1 -R
%patch7587 -p1 -R
%patch7586 -p1 -R
%patch7585 -p1 -R
%patch7584 -p1 -R
%patch7583 -p1 -R
%patch7582 -p1 -R
%patch7581 -p1 -R
%patch7580 -p1 -R
%patch7579 -p1 -R
%patch7578 -p1 -R
%patch7577 -p1 -R
%patch7576 -p1 -R
%patch7575 -p1 -R
%patch7574 -p1 -R
%patch7573 -p1 -R
%patch7572 -p1 -R
%patch7571 -p1 -R
%patch7570 -p1 -R
%patch7569 -p1 -R
%patch7568 -p1 -R
%patch7567 -p1 -R
%patch7566 -p1 -R
%patch7565 -p1 -R
%patch7564 -p1 -R
%patch7563 -p1 -R
%patch7562 -p1 -R
%patch7561 -p1 -R
%patch7560 -p1 -R
%patch7559 -p1 -R
%patch7558 -p1 -R
%patch7557 -p1 -R
%patch7556 -p1 -R
%patch7555 -p1 -R
%patch7554 -p1 -R
%patch7553 -p1 -R
%patch7552 -p1 -R
%patch7551 -p1 -R
%patch7550 -p1 -R
%patch7549 -p1 -R
%patch7548 -p1 -R
%patch7547 -p1 -R
%patch7546 -p1 -R
%patch7545 -p1 -R
%patch7544 -p1 -R
%patch7543 -p1 -R
%patch7542 -p1 -R
%patch7541 -p1 -R
%patch7540 -p1 -R
%patch7539 -p1 -R
%patch7538 -p1 -R
%patch7537 -p1 -R
%patch7536 -p1 -R
%patch7535 -p1 -R
%patch7534 -p1 -R
%patch7533 -p1 -R
%patch7532 -p1 -R
%patch7531 -p1 -R
%patch7530 -p1 -R
%patch7529 -p1 -R
%patch7528 -p1 -R
%patch7527 -p1 -R
%patch7526 -p1 -R
%patch7525 -p1 -R
%patch7524 -p1 -R
%patch7523 -p1 -R
%patch7522 -p1 -R
%patch7521 -p1 -R
%patch7520 -p1 -R
%patch7519 -p1 -R
%patch7518 -p1 -R
%patch7517 -p1 -R
%patch7516 -p1 -R
%patch7515 -p1 -R
%patch7514 -p1 -R
%patch7513 -p1 -R
%patch7512 -p1 -R
%patch7511 -p1 -R
%patch7510 -p1 -R
%patch7509 -p1 -R
%patch7508 -p1 -R
%patch7507 -p1 -R
%patch7506 -p1 -R
%patch7505 -p1 -R
%patch7504 -p1 -R
%patch7503 -p1 -R
%patch7502 -p1 -R
%patch7501 -p1 -R
%patch7500 -p1 -R
%patch7499 -p1 -R
%patch7498 -p1 -R
%patch7497 -p1 -R
%patch7496 -p1 -R
%patch7495 -p1 -R
%patch7494 -p1 -R
%patch7493 -p1 -R
%patch7492 -p1 -R
%patch7491 -p1 -R
%patch7490 -p1 -R
%patch7489 -p1 -R
%patch7488 -p1 -R
%patch7487 -p1 -R
%patch7486 -p1 -R
%patch7485 -p1 -R
%patch7484 -p1 -R
%patch7483 -p1 -R
%patch7482 -p1 -R
%patch7481 -p1 -R
%patch7480 -p1 -R
%patch7479 -p1 -R
%patch7478 -p1 -R
%patch7477 -p1 -R
%patch7476 -p1 -R
%patch7475 -p1 -R
%patch7474 -p1 -R
%patch7473 -p1 -R
%patch7472 -p1 -R
%patch7471 -p1 -R
%patch7470 -p1 -R
%patch7469 -p1 -R
%patch7468 -p1 -R
%patch7467 -p1 -R
%patch7466 -p1 -R
%patch7465 -p1 -R
%patch7464 -p1 -R
%patch7463 -p1 -R
%patch7462 -p1 -R
%patch7461 -p1 -R
%patch7460 -p1 -R
%patch7459 -p1 -R
%patch7458 -p1 -R
%patch7457 -p1 -R
%patch7456 -p1 -R
%patch7455 -p1 -R
%patch7454 -p1 -R
%patch7453 -p1 -R
%patch7452 -p1 -R
%patch7451 -p1 -R
%patch7450 -p1 -R
%patch7449 -p1 -R
%patch7448 -p1 -R
%patch7447 -p1 -R
%patch7446 -p1 -R
%patch7445 -p1 -R
%patch7444 -p1 -R
%patch7443 -p1 -R
%patch7442 -p1 -R
%patch7441 -p1 -R
%patch7440 -p1 -R
%patch7439 -p1 -R
%patch7438 -p1 -R
%patch7437 -p1 -R
%patch7436 -p1 -R
%patch7435 -p1 -R
%patch7434 -p1 -R
%patch7433 -p1 -R
%patch7432 -p1 -R
%patch7431 -p1 -R
%patch7430 -p1 -R
%patch7429 -p1 -R
%patch7428 -p1 -R
%patch7427 -p1 -R
%patch7426 -p1 -R
%patch7425 -p1 -R
%patch7424 -p1 -R
%patch7423 -p1 -R
%patch7422 -p1 -R
%patch7421 -p1 -R
%patch7420 -p1 -R
%patch7419 -p1 -R
%patch7418 -p1 -R
%patch7417 -p1 -R
%patch7416 -p1 -R
%patch7415 -p1 -R
%patch7414 -p1 -R
%patch7413 -p1 -R
%patch7412 -p1 -R
%patch7411 -p1 -R
%patch7410 -p1 -R
%patch7409 -p1 -R
%patch7408 -p1 -R
%patch7407 -p1 -R
%patch7406 -p1 -R
%patch7405 -p1 -R
%patch7404 -p1 -R
%patch7403 -p1 -R
%patch7402 -p1 -R
%patch7401 -p1 -R
%patch7400 -p1 -R
%patch7399 -p1 -R
%patch7398 -p1 -R
%patch7397 -p1 -R
%patch7396 -p1 -R
%patch7395 -p1 -R
%patch7394 -p1 -R
%patch7393 -p1 -R
%patch7392 -p1 -R
%patch7391 -p1 -R
%patch7390 -p1 -R
%patch7389 -p1 -R
%patch7388 -p1 -R
%patch7387 -p1 -R
%patch7386 -p1 -R
%patch7385 -p1 -R
%patch7384 -p1 -R
%patch7383 -p1 -R
%patch7382 -p1 -R
%patch7381 -p1 -R
%patch7380 -p1 -R
%patch7379 -p1 -R
%patch7378 -p1 -R
%patch7377 -p1 -R
%patch7376 -p1 -R
%patch7375 -p1 -R
%patch7374 -p1 -R
%patch7373 -p1 -R
%patch7372 -p1 -R
%patch7371 -p1 -R
%patch7370 -p1 -R
%patch7369 -p1 -R
%patch7368 -p1 -R
%patch7367 -p1 -R
%patch7365 -p1 -R
%patch7364 -p1 -R
%patch7363 -p1 -R
%patch7362 -p1 -R
%patch7361 -p1 -R
%patch7360 -p1 -R
%patch7359 -p1 -R
%patch7358 -p1 -R
%patch7357 -p1 -R
%patch7356 -p1 -R
%patch7355 -p1 -R
%patch7354 -p1 -R
%patch7353 -p1 -R
%patch7352 -p1 -R
%patch7351 -p1 -R
%patch7350 -p1 -R
%patch7349 -p1 -R
%patch7348 -p1 -R
%patch7347 -p1 -R
%patch7346 -p1 -R
%patch7345 -p1 -R
%patch7344 -p1 -R
%patch7343 -p1 -R
%patch7342 -p1 -R
%patch7341 -p1 -R
%patch7340 -p1 -R
%patch7339 -p1 -R
%patch7338 -p1 -R
%patch7337 -p1 -R
%patch7336 -p1 -R
%patch7335 -p1 -R
%patch7334 -p1 -R
%patch7333 -p1 -R
%patch7332 -p1 -R
%patch7331 -p1 -R
%patch7330 -p1 -R
%patch7329 -p1 -R
%patch7328 -p1 -R
%patch7327 -p1 -R
%patch7326 -p1 -R
%patch7325 -p1 -R
%patch7324 -p1 -R
%patch7323 -p1 -R
%patch7322 -p1 -R
%patch7321 -p1 -R
%patch7320 -p1 -R
%patch7319 -p1 -R
%patch7318 -p1 -R
%patch7317 -p1 -R
%patch7316 -p1 -R
%patch7315 -p1 -R
%patch7314 -p1 -R
%patch7313 -p1 -R
%patch7312 -p1 -R
%patch7311 -p1 -R
%patch7310 -p1 -R
%patch7309 -p1 -R
%patch7308 -p1 -R
%patch7307 -p1 -R
%patch7306 -p1 -R
%patch7305 -p1 -R
%patch7304 -p1 -R
%patch7303 -p1 -R
%patch7302 -p1 -R
%patch7301 -p1 -R
%patch7300 -p1 -R
%patch7299 -p1 -R
%patch7298 -p1 -R
%patch7297 -p1 -R
%patch7296 -p1 -R
%patch7295 -p1 -R
%patch7294 -p1 -R
%patch7293 -p1 -R
%patch7292 -p1 -R
%patch7291 -p1 -R
%patch7290 -p1 -R
%patch7289 -p1 -R
%patch7288 -p1 -R
%patch7287 -p1 -R
%patch7286 -p1 -R
%patch7285 -p1 -R
%patch7284 -p1 -R
%patch7283 -p1 -R
%patch7282 -p1 -R
%patch7281 -p1 -R
%patch7280 -p1 -R
%patch7279 -p1 -R
%patch7278 -p1 -R
%patch7277 -p1 -R
%patch7276 -p1 -R
%patch7275 -p1 -R
%patch7274 -p1 -R
%patch7273 -p1 -R
%patch7272 -p1 -R
%patch7271 -p1 -R
%patch7270 -p1 -R
%patch7269 -p1 -R
%patch7268 -p1 -R
%patch7267 -p1 -R
%patch7266 -p1 -R
%patch7265 -p1 -R
%patch7264 -p1 -R
%patch7263 -p1 -R
%patch7262 -p1 -R
%patch7261 -p1 -R
%patch7260 -p1 -R
%patch7259 -p1 -R
%patch7258 -p1 -R
%patch7257 -p1 -R
%patch7256 -p1 -R
%patch7255 -p1 -R
%patch7254 -p1 -R
%patch7253 -p1 -R
%patch7252 -p1 -R
%patch7251 -p1 -R
%patch7250 -p1 -R
%patch7249 -p1 -R
%patch7248 -p1 -R
%patch7247 -p1 -R
%patch7246 -p1 -R
%patch7245 -p1 -R
%patch7244 -p1 -R
%patch7243 -p1 -R
%patch7242 -p1 -R
%patch7241 -p1 -R
%patch7240 -p1 -R
%patch7239 -p1 -R
%patch7238 -p1 -R
%patch7237 -p1 -R
%patch7236 -p1 -R
%patch7235 -p1 -R
%patch7234 -p1 -R
%patch7233 -p1 -R
%patch7232 -p1 -R
%patch7231 -p1 -R
%patch7230 -p1 -R
%patch7229 -p1 -R
%patch7228 -p1 -R
%patch7227 -p1 -R
%patch7226 -p1 -R
%patch7225 -p1 -R
%patch7224 -p1 -R
%patch7223 -p1 -R
%patch7222 -p1 -R
%patch7221 -p1 -R
%patch7220 -p1 -R
%patch7219 -p1 -R
%patch7218 -p1 -R
%patch7217 -p1 -R
%patch7216 -p1 -R
%patch7215 -p1 -R
%patch7214 -p1 -R
%patch7213 -p1 -R
%patch7212 -p1 -R
%patch7211 -p1 -R
%patch7210 -p1 -R
%patch7209 -p1 -R
%patch7208 -p1 -R
%patch7207 -p1 -R
%patch7206 -p1 -R
%patch7205 -p1 -R
%patch7204 -p1 -R
%patch7203 -p1 -R
%patch7202 -p1 -R
%patch7201 -p1 -R
%patch7200 -p1 -R
%patch7199 -p1 -R
%patch7198 -p1 -R
%patch7197 -p1 -R
%patch7196 -p1 -R
%patch7195 -p1 -R
%patch7194 -p1 -R
%patch7193 -p1 -R
%patch7192 -p1 -R
%patch7191 -p1 -R
%patch7190 -p1 -R
%patch7189 -p1 -R
%patch7188 -p1 -R
%patch7187 -p1 -R
%patch7186 -p1 -R
%patch7185 -p1 -R
%patch7184 -p1 -R
%patch7183 -p1 -R
%patch7182 -p1 -R
%patch7181 -p1 -R
%patch7180 -p1 -R
%patch7179 -p1 -R
%patch7178 -p1 -R
%patch7177 -p1 -R
%patch7176 -p1 -R
%patch7175 -p1 -R
%patch7174 -p1 -R
%patch7173 -p1 -R
%patch7172 -p1 -R
%patch7171 -p1 -R
%patch7170 -p1 -R
%patch7169 -p1 -R
%patch7168 -p1 -R
%patch7167 -p1 -R
%patch7166 -p1 -R
%patch7165 -p1 -R
%patch7164 -p1 -R
%patch7163 -p1 -R
%patch7162 -p1 -R
%patch7161 -p1 -R
%patch7160 -p1 -R
%patch7158 -p1 -R
%patch7157 -p1 -R
%patch7156 -p1 -R
%patch7155 -p1 -R
%patch7154 -p1 -R
%patch7153 -p1 -R
%patch7152 -p1 -R
%patch7151 -p1 -R
%patch7150 -p1 -R
%patch7149 -p1 -R
%patch7148 -p1 -R
%patch7147 -p1 -R
%patch7146 -p1 -R
%patch7145 -p1 -R
%patch7144 -p1 -R
%patch7143 -p1 -R
%patch7142 -p1 -R
%patch7141 -p1 -R
%patch7140 -p1 -R
%patch7139 -p1 -R
%patch7138 -p1 -R
%patch7137 -p1 -R
%patch7136 -p1 -R
%patch7135 -p1 -R
%patch7134 -p1 -R
%patch7133 -p1 -R
%patch7132 -p1 -R
%patch7131 -p1 -R
%patch7130 -p1 -R
%patch7129 -p1 -R
%patch7128 -p1 -R
%patch7127 -p1 -R
%patch7126 -p1 -R
%patch7125 -p1 -R
%patch7124 -p1 -R
%patch7123 -p1 -R
%patch7122 -p1 -R
%patch7121 -p1 -R
%patch7120 -p1 -R
%patch7119 -p1 -R
%patch7118 -p1 -R
%patch7117 -p1 -R
%patch7116 -p1 -R
%patch7115 -p1 -R
%patch7114 -p1 -R
%patch7113 -p1 -R
%patch7112 -p1 -R
%patch7111 -p1 -R
%patch7110 -p1 -R
%patch7109 -p1 -R
%patch7108 -p1 -R
%patch7107 -p1 -R
%patch7106 -p1 -R
%patch7105 -p1 -R
%patch7104 -p1 -R
%patch7103 -p1 -R
%patch7102 -p1 -R
%patch7101 -p1 -R
%patch7100 -p1 -R
%patch7099 -p1 -R
%patch7098 -p1 -R
%patch7097 -p1 -R
%patch7096 -p1 -R
%patch7095 -p1 -R
%patch7094 -p1 -R
%patch7093 -p1 -R
%patch7092 -p1 -R
%patch7091 -p1 -R
%patch7090 -p1 -R
%patch7089 -p1 -R
%patch7088 -p1 -R
%patch7087 -p1 -R
%patch7086 -p1 -R
%patch7085 -p1 -R
%patch7084 -p1 -R
%patch7083 -p1 -R
%patch7082 -p1 -R
%patch7081 -p1 -R
%patch7080 -p1 -R
%patch7079 -p1 -R
%patch7078 -p1 -R
%patch7077 -p1 -R
%patch7076 -p1 -R
%patch7075 -p1 -R
%patch7074 -p1 -R
%patch7073 -p1 -R
%patch7072 -p1 -R
%patch7071 -p1 -R
%patch7070 -p1 -R
%patch7069 -p1 -R
%patch7068 -p1 -R
%patch7067 -p1 -R
%patch7066 -p1 -R
%patch7065 -p1 -R
%patch7064 -p1 -R
%patch7063 -p1 -R
%patch7062 -p1 -R
%patch7061 -p1 -R
%patch7060 -p1 -R
%patch7059 -p1 -R
%patch7058 -p1 -R
%patch7057 -p1 -R
%patch7056 -p1 -R
%patch7055 -p1 -R
%patch7054 -p1 -R
%patch7053 -p1 -R
%patch7052 -p1 -R
%patch7051 -p1 -R
%patch7050 -p1 -R
%patch7049 -p1 -R
%patch7048 -p1 -R
%patch7047 -p1 -R
%patch7046 -p1 -R
%patch7045 -p1 -R
%patch7044 -p1 -R
%patch7043 -p1 -R
%patch7042 -p1 -R
%patch7041 -p1 -R
%patch7040 -p1 -R
%patch7039 -p1 -R
%patch7038 -p1 -R
%patch7037 -p1 -R
%patch7036 -p1 -R
%patch7035 -p1 -R
%patch7034 -p1 -R
%patch7033 -p1 -R
%patch7032 -p1 -R
%patch7031 -p1 -R
%patch7030 -p1 -R
%patch7029 -p1 -R
%patch7028 -p1 -R
%patch7027 -p1 -R
%patch7026 -p1 -R
%patch7025 -p1 -R
%patch7024 -p1 -R
%patch7023 -p1 -R
%patch7022 -p1 -R
%patch7021 -p1 -R
%patch7020 -p1 -R
%patch7019 -p1 -R
%patch7018 -p1 -R
%patch7017 -p1 -R
%patch7016 -p1 -R
%patch7015 -p1 -R
%patch7014 -p1 -R
%patch7013 -p1 -R
%patch7012 -p1 -R
%patch7011 -p1 -R
%patch7010 -p1 -R
%patch7009 -p1 -R
%patch7008 -p1 -R
filterdiff -p1 --clean \
  -x 'dlls/ntdll/unix/signal_arm.c' -x 'dlls/ntdll/unix/signal_arm64.c' \
  %{P:7007} > %{name}-whq-3e9f8c8.patch
patch -p1 -R -i %{name}-whq-3e9f8c8.patch
rm -f dlls/ntdll/unix/signal_arm{,64}.c
%patch7006 -p1 -R
%patch7005 -p1 -R
%patch7004 -p1 -R
%patch7003 -p1 -R
%patch7002 -p1 -R
%patch7001 -p1 -R
%patch7000 -p1 -R

%if 0%{?fshack}
%patch8032 -p1 -R
%patch8031 -p1 -R
%patch8030 -p1 -R
%patch8029 -p1 -R
%patch8028 -p1 -R
%patch8027 -p1 -R
%patch8026 -p1 -R
%patch8025 -p1 -R
%patch8024 -p1 -R
%patch8023 -p1 -R
%patch8022 -p1 -R
%patch8021 -p1 -R
%patch8020 -p1 -R
%patch8019 -p1 -R
%patch8018 -p1 -R
%patch8017 -p1 -R
%patch8016 -p1 -R
%patch8015 -p1 -R
%patch8014 -p1 -R
%patch8013 -p1 -R
%patch8012 -p1 -R
%patch8011 -p1 -R
%patch8010 -p1 -R
%patch8009 -p1 -R
%patch8008 -p1 -R
%patch8007 -p1 -R
%patch8006 -p1 -R
%patch8005 -p1 -R
%patch8004 -p1 -R
%patch8003 -p1 -R
%patch8002 -p1 -R
%patch8001 -p1 -R
%patch8000 -p1 -R
%endif
%endif

# setup and apply wine-staging patches
%if 0%{?wine_staging}

gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

%patch801 -p1
%patch802 -p1
%patch803 -p1
%if !0%{?fshack}
%patch804 -p1
%patch805 -p1
%patch806 -p1
%patch807 -p1
%endif
%patch1000 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1

%patch5000 -p1
%patch5001 -p1

sed -e 's|autoreconf -f|true|g' -i ./patches/patchinstall.sh
./patches/patchinstall.sh DESTDIR="`pwd`" --all %{?wine_staging_opts}

sed \
  -e "s/ (Staging)/ (%{staging_banner})/g" \
  -i libs/wine/Makefile.in programs/winecfg/about.c

%if 0%{?pba}
cp -p %{S:3001} README-pba-pkg

%patch3000 -p1
%endif

%patch1020 -p1
%if 0%{?fsync_spincounts}
%patch1022 -p1
%patch1092 -p1
%endif
%if 0%{?fshack}
%patch1023 -p1
%patch1024 -p1
%endif
%if !0%{?mfplatwip}
%patch1025 -p1
%endif
%patch1026 -p1
%if 0%{?fshack}
%patch1027 -p1
%patch1028 -p1 -R
%endif
%patch1029 -p1
%patch1030 -p1
%if 0%{?fshack}
%patch1031 -p1
%patch1032 -p1
%if 0%{?vulkanup}
%patch1033 -p1
%endif
%patch1090 -p1 -R
%else
%if 0%{?vulkanup}
%patch1034 -p1
%endif
%endif
%patch1035 -p1
%patch1091 -p1 -R

%patch1093 -p1
%patch1094 -p1
%patch1095 -p1
%patch1096 -p1
%patch1097 -p1
%patch1098 -p1
%patch1200 -p1
%if 0%{?mfplatwip}
%patch1201 -p1
%endif
%if 0%{?fshack}
%patch1300 -p1
%else
%patch1301 -p1
%endif

# fix parallelized build
sed -i -e 's!^loader server: libs/port libs/wine tools.*!& include!' Makefile.in

%else

rm -rf patches/

%endif

# Verify gecko and mono versions
GECKO_VER="$(grep '^#define' dlls/appwiz.cpl/addons.c | grep ' GECKO_VERSION ' | awk '{print $3}' | tr -d \")"
GECKO_VER2="$(grep '#define' dlls/mshtml/nsiface.idl | grep ' GECKO_VERSION ' | awk '{print $3}' | sed -e 's,\\",,g' -e 's,"),,')"
if [ "${GECKO_VER}" != "%{winegecko}" ] || [ "${GECKO_VER2}" != "%{winegecko}" ] ;then
  echo "winegecko version mismatch. Edit %%global winegecko to ${GECKO_VER}."
  exit 1
fi
MONO_VER="$(grep '^#define' dlls/appwiz.cpl/addons.c | grep ' MONO_VERSION ' | awk '{print $3}' | tr -d \")"
MONO_VER2="$(grep '^#define' dlls/mscoree/mscoree_private.h | grep ' WINE_MONO_VERSION ' | awk '{print $3}' | tr -d \")"
if [ "${MONO_VER}" != "%{winemono}" ] || [ "${MONO_VER2}" != "%{winemono}" ];then
  echo "winemono version mismatch. Edit %%global winemono to ${MONO_VER}."
  exit 1
fi

cp -p %{SOURCE3} README-FEDORA
cp -p %{SOURCE6} README-chinforpms
%if 0%{?fshack}
cat %{SOURCE7} >> README-chinforpms
%endif

cp -p %{SOURCE502} README-tahoma

sed -e '/winemenubuilder\.exe/s|-a ||g' -i loader/wine.inf.in

sed -i \
  -e 's|-lncurses |-lncursesw |g' \
  -e 's|"-lncurses"|"-lncursesw"|g' \
  -e 's|OpenCL/opencl.h|CL/opencl.h|g' \
  configure

./dlls/winevulkan/make_vulkan
./tools/make_requests
./tools/make_specfiles
autoreconf -f


%build

# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%define _lto_cflags %{nil}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo %{build_cflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

export CFLAGS="$CFLAGS -ftree-vectorize -mno-avx"

%ifarch aarch64
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
# Fedora's default compiler flags now conflict with what clang supports
# https://bugzilla.redhat.com/show_bug.cgi?id=1658311
export CFLAGS="`echo $CFLAGS | sed -e 's/-fstack-clash-protection//'`"
%endif

# Remove this flags by upstream recommendation (see configure.ac)
export CFLAGS="`echo $CFLAGS | sed \
  -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//' \
  -e 's/-fstack-protector-strong//' \
  -e 's/-fstack-clash-protection//' \
  -e 's/-fcf-protection//' \
  `"

export LDFLAGS="-Wl,-O1,--sort-common %{build_ldflags}"

%if 0%{?wine_mingw}
# mingw compiler do not support plugins and some flags are crashing it
export CROSSCFLAGS="`echo $CFLAGS | sed \
  -e 's/-grecord-gcc-switches//' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-cc1,,' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,' \
  -e 's/-fasynchronous-unwind-tables//' \
  ` --param=ssp-buffer-size=4"
# mingw linker do not support -z,relro and now
export LDFLAGS="`echo $LDFLAGS | sed \
  -e 's/-Wl,-z,relro//' \
  -e 's/-Wl,-z,now//' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-ld,,' \
  `"

# Put them again on gcc
mkdir bin
cat > bin/gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/gcc %{build_ldflags} "$@"
EOF
if [ -x %{_bindir}/g++ ] ;then
cat > bin/g++ <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/g++ %{build_ldflags} "$@"
EOF
chmod 0755 bin/*g++
fi
%if !0%{?with_debug}
# -Wl -S to build working stripped PEs
cat > bin/x86_64-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/x86_64-w64-mingw32-gcc -Wl,-S "$@"
EOF
cat > bin/i686-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/i686-w64-mingw32-gcc -Wl,-S "$@"
EOF
%endif
chmod 0755 bin/*gcc
export PATH="$(pwd)/bin:$PATH"
%endif

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --without-hal --with-dbus \
 --with-x \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
%if 0%{?wine_mingw}
 --with-mingw \
%else
 --without-mingw \
%endif
%if 0%{?wine_staging}
 --with-xattr \
%if !0%{?gtk3}
 --without-gtk3 \
%endif
%endif
 --disable-tests \
%{nil}

%make_build TARGETFLAGS="" depend
%make_build TARGETFLAGS="" __builddeps__
%make_build TARGETFLAGS=""

%install
%if 0%{?wine_mingw}
export PATH="$(pwd)/bin:$PATH"
%endif

%makeinstall \
        includedir=%{buildroot}%{_includedir} \
        sysconfdir=%{buildroot}%{_sysconfdir}/wine \
        dlldir=%{buildroot}%{_libdir}/wine \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
%endif
%ifnarch %{arm} aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
%ifnarch %{arm}
touch %{buildroot}%{_bindir}/wine-preloader
%endif
touch %{buildroot}%{_bindir}/wineserver

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
%ifarch x86_64 aarch64
chrpath --delete %{buildroot}%{_bindir}/wine64
chrpath --delete %{buildroot}%{_bindir}/wineserver64
%else
chrpath --delete %{buildroot}%{_bindir}/wine32
chrpath --delete %{buildroot}%{_bindir}/wineserver32
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf

# add wine dir to desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -p -m 644 %{SOURCE200} \
%{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
mkdir -p %{buildroot}%{_datadir}/desktop-directories
install -p -m 644 %{SOURCE201} \
%{buildroot}%{_datadir}/desktop-directories/Wine.directory

# add gecko dir
mkdir -p %{buildroot}%{_datadir}/wine/gecko

# add mono dir
mkdir -p %{buildroot}%{_datadir}/wine/mono

# extract and install icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# This replacement masks a composite program icon .SVG down
# so that only its full-size scalable icon is visible
PROGRAM_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="368"\n'\
'   y="8"\n'\
'   viewBox="368, 8, 256, 256"/;'

MAIN_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="8"\n'\
'   y="8"\n'\
'   viewBox="8, 8, 256, 256"/;'

# This icon file is still in the legacy format
install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e "$MAIN_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

# The rest come from programs/, and contain larger scalable icons
# with a new layout that requires the PROGRAM_ICONFIX sed adjustment
install -p -m 644 programs/notepad/notepad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg

install -p -m 644 programs/regedit/regedit.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg

install -p -m 644 programs/msiexec/msiexec.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg

install -p -m 644 programs/winecfg/winecfg.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg

install -p -m 644 programs/winefile/winefile.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg

install -p -m 644 programs/winemine/winemine.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg

install -p -m 644 programs/winhlp32/winhelp.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg

install -p -m 644 programs/wordpad/wordpad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg

install -p -m 644 programs/iexplore/iexplore.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/iexplore.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/iexplore.svg

install -p -m 644 dlls/joy.cpl/joy.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg

install -p -m 644 programs/taskmgr/taskmgr.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/taskmgr.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/taskmgr.svg

for file in %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/*.svg ;do
  basefile=$(basename ${file} .svg)
  for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
    dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
    mkdir -p ${dir}
    rsvg-convert -w ${res} -h ${res} ${file} \
      -o ${dir}/${basefile}.png
  done
done

# install desktop files
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE100}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE101}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE102}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE103}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE104}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE105}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE106}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE107}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE108}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE109}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE110}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE111}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE112}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE113}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/wine.desktop

#mime-types
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE300}

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%ifarch %{ix86} %{arm}
install -p -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif

%ifarch x86_64 aarch64
install -p -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif


# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s \
  $(realpath --relative-to=%{_fontconfig_confdir} %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf) \
  %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

%if 0%{?wine_staging}
# install Times New Roman font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
ln -s ../../wine/fonts/times.ttf times.ttf
popd
%endif

# install Webdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-webdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-webdings-fonts
ln -s ../../wine/fonts/webdings.ttf webdings.ttf
popd

# install Wingdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
ln -s ../../wine/fonts/wingding.ttf wingding.ttf
popd

# clean readme files
pushd documentation
for lang in it hu sv es pt pt_br;
do iconv -f iso8859-1 -t utf-8 README.$lang > \
 README.$lang.conv && mv -f README.$lang.conv README.$lang
done;
popd

rm -f %{buildroot}%{_initrddir}/wine

# wine makefiles are currently broken and don't install the wine man page
install -p -m 0644 loader/wine.man %{buildroot}%{_mandir}/man1/wine.1
install -p -m 0644 loader/wine.de.UTF-8.man %{buildroot}%{_mandir}/de.UTF-8/man1/wine.1
install -p -m 0644 loader/wine.fr.UTF-8.man %{buildroot}%{_mandir}/fr.UTF-8/man1/wine.1
mkdir -p %{buildroot}%{_mandir}/pl.UTF-8/man1
install -p -m 0644 loader/wine.pl.UTF-8.man %{buildroot}%{_mandir}/pl.UTF-8/man1/wine.1

# install and validate AppData file
mkdir -p %{buildroot}/%{_metainfodir}/
install -p -m 0644 %{SOURCE150} %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml

%if 0%{?rhel} == 6
%post sysvinit
if [ $1 -eq 1 ]; then
/sbin/chkconfig --add wine
/sbin/chkconfig --level 2345 wine on
/sbin/service wine start &>/dev/null || :
fi

%preun sysvinit
if [ $1 -eq 0 ]; then
/sbin/service wine stop >/dev/null 2>&1
/sbin/chkconfig --del wine
fi
%endif

%post systemd
%binfmt_apply wine.conf

%postun systemd
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi

%posttrans core
%ifarch x86_64 aarch64
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine64 10 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine64-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver64 20
%else
%ifnarch %{arm}
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine32-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%else
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%endif
%endif

%postun core
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
fi

%files
# meta package

%files core
%license COPYING.LIB
%license LICENSE
%license LICENSE.OLD
%doc ANNOUNCE
%doc AUTHORS
%doc README-FEDORA
%doc README-chinforpms
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%if 0%{?wine_staging}
%doc README.esync
%if 0%{?pba}
%license LICENSE_pba.md
%doc README_pba.md
%doc README-pba-pkg
%endif
%{_bindir}/msidb
%{_libdir}/wine/runas.%{wineexe}
%endif
%{_bindir}/winedump
%{_libdir}/wine/explorer.%{wineexe}
%{_libdir}/wine/cabarc.%{wineexe}
%{_libdir}/wine/control.%{wineexe}
%{_libdir}/wine/cmd.%{wineexe}
%{_libdir}/wine/dxdiag.%{wineexe}
%{_libdir}/wine/notepad.%{wineexe}
%{_libdir}/wine/plugplay.%{wineexe}
%{_libdir}/wine/progman.%{wineexe}
%{_libdir}/wine/taskmgr.%{wineexe}
%{_libdir}/wine/winedbg.exe.so
%{_libdir}/wine/winefile.%{wineexe}
%{_libdir}/wine/winemine.%{wineexe}
%{_libdir}/wine/winemsibuilder.%{wineexe}
%{_libdir}/wine/winepath.%{wineexe}
%{_libdir}/wine/winmgmt.%{wineexe}
%{_libdir}/wine/winver.%{wineexe}
%{_libdir}/wine/wordpad.%{wineexe}
%{_libdir}/wine/write.%{wineexe}
%{_libdir}/wine/wusa.%{wineexe}

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%ifnarch %{arm}
%{_bindir}/wine32-preloader
%endif
%{_bindir}/wineserver32
%config %{_sysconfdir}/ld.so.conf.d/wine-32.conf
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{_bindir}/wineserver64
%config %{_sysconfdir}/ld.so.conf.d/wine-64.conf
%endif
%ifarch x86_64 aarch64
%{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ifnarch %{arm}
%ghost %{_bindir}/wine-preloader
%endif
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine
%dir %{_libdir}/wine/fakedlls
%{_libdir}/wine/fakedlls/*

%{_libdir}/wine/attrib.%{wineexe}
%{_libdir}/wine/arp.%{wineexe}
%{_libdir}/wine/aspnet_regiis.%{wineexe}
%{_libdir}/wine/cacls.%{wineexe}
%{_libdir}/wine/conhost.%{wineexe}
%{_libdir}/wine/cscript.%{wineexe}
%{_libdir}/wine/dism.%{wineexe}
%{_libdir}/wine/dpnsvr.%{wineexe}
%{_libdir}/wine/eject.%{wineexe}
%{_libdir}/wine/expand.%{wineexe}
%{_libdir}/wine/extrac32.%{wineexe}
%{_libdir}/wine/fc.%{wineexe}
%{_libdir}/wine/find.%{wineexe}
%{_libdir}/wine/findstr.%{wineexe}
%{_libdir}/wine/fsutil.%{wineexe}
%{_libdir}/wine/hostname.%{wineexe}
%{_libdir}/wine/ipconfig.%{wineexe}
%{_libdir}/wine/winhlp32.%{wineexe}
%{_libdir}/wine/mshta.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/msidb.%{wineexe}
%endif
%{_libdir}/wine/msiexec.%{wineexe}
%{_libdir}/wine/net.%{wineexe}
%{_libdir}/wine/netstat.%{wineexe}
%{_libdir}/wine/ngen.%{wineexe}
%{_libdir}/wine/ntoskrnl.%{wineexe}
%{_libdir}/wine/oleview.%{wineexe}
%{_libdir}/wine/ping.%{wineexe}
%{_libdir}/wine/powershell.%{wineexe}
%{_libdir}/wine/reg.%{wineexe}
%{_libdir}/wine/regasm.%{wineexe}
%{_libdir}/wine/regedit.%{wineexe}
%{_libdir}/wine/regini.%{wineexe}
%{_libdir}/wine/regsvcs.%{wineexe}
%{_libdir}/wine/regsvr32.%{wineexe}
%{_libdir}/wine/rpcss.%{wineexe}
%{_libdir}/wine/rundll32.%{wineexe}
%{_libdir}/wine/schtasks.%{wineexe}
%{_libdir}/wine/sdbinst.%{wineexe}
%{_libdir}/wine/secedit.%{wineexe}
%{_libdir}/wine/servicemodelreg.%{wineexe}
%{_libdir}/wine/services.%{wineexe}
%{_libdir}/wine/start.%{wineexe}
%{_libdir}/wine/tasklist.%{wineexe}
%{_libdir}/wine/termsv.%{wineexe}
%{_libdir}/wine/view.%{wineexe}
%{_libdir}/wine/wevtutil.%{wineexe}
%{_libdir}/wine/wineboot.%{wineexe}
%{_libdir}/wine/winebrowser.exe.so
%{_libdir}/wine/wineconsole.exe.so
%{_libdir}/wine/winemenubuilder.exe.so
%{_libdir}/wine/winecfg.exe.so
%{_libdir}/wine/winedevice.%{wineexe}
%{_libdir}/wine/wmplayer.%{wineexe}
%{_libdir}/wine/wscript.%{wineexe}
%{_libdir}/wine/uninstaller.%{wineexe}

%{_libdir}/libwine.so.1*

%{_libdir}/wine/acledit.%{winedll}
%{_libdir}/wine/aclui.%{winedll}
%{_libdir}/wine/activeds.%{winedll}
%{_libdir}/wine/activeds.%{winetlb}
%{_libdir}/wine/actxprxy.%{winedll}
%{_libdir}/wine/adsldp.%{winedll}
%{_libdir}/wine/adsldpc.%{winedll}
%{_libdir}/wine/advapi32.dll.so
%{_libdir}/wine/advpack.%{winedll}
%{_libdir}/wine/amsi.%{winedll}
%{_libdir}/wine/amstream.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-identity-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-apiquery-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-appcompat-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-appinit-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-atoms-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-bem-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-comm-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-console-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-console-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-crt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-crt-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-debug-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-debug-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-ansi-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-fromapp-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-handle-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-interlocked-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-interlocked-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-io-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-io-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-job-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-job-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-largeinteger-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-2-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-3-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localregistry-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-4.%{winedll}
%{_libdir}/wine/api-ms-win-core-misc-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namedpipe-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namespace-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-normalization-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-path-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-privateprofile-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-core-processtopology-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-profile-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-quirks-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-realtime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registry-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registry-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registry-l2-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registryuserspecific-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shutdown-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sidebyside-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-stringansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-stringloader-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-systemtopology-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-timezone-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-toolhelp-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-url-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-util-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-versionansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-windowserrorreporting-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-errorprivate-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-registration-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-roparameterizediid-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-string-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-xstate-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-xstate-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-conio-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-convert-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-environment-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-filesystem-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-heap-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-locale-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-math-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-multibyte-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-process-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-runtime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-stdio-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-time-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-utility-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-devices-config-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-devices-config-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-devices-query-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-kernel32-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-normaliz-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-ole32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shell32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-user32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-version-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-dx-d3dkmt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-classicprovider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-consumer-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-controller-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-provider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventlog-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-gdi-dpiinfo-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-joystick-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-misc-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-mm-mme-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-time-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-rectangle-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-perf-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-power-base-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-power-setting-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-4.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-winevent-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-security-activedirectoryclient-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-audit-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-credentials-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-cryptoapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-grouppolicy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsapolicy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-provider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-sddl-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-systemfunctions-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-core-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-core-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-service-management-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-management-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-service-winsvc-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-winsvc-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-scaling-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-stream-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-thread-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shell-shellcom-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shell-shellfolders-l1-1-0.%{winedll}
%{_libdir}/wine/apphelp.%{winedll}
%{_libdir}/wine/appwiz.%{winecpl}
%{_libdir}/wine/atl.%{winedll}
%{_libdir}/wine/atl80.%{winedll}
%{_libdir}/wine/atl90.%{winedll}
%{_libdir}/wine/atl100.%{winedll}
%{_libdir}/wine/atl110.%{winedll}
%{_libdir}/wine/atlthunk.%{winedll}
%{_libdir}/wine/atmlib.%{winedll}
%{_libdir}/wine/authz.%{winedll}
%{_libdir}/wine/avicap32.dll.so
%{_libdir}/wine/avifil32.%{winedll}
%{_libdir}/wine/avrt.%{winedll}
%{_libdir}/wine/bcrypt.dll.so
%{_libdir}/wine/bluetoothapis.%{winedll}
%{_libdir}/wine/browseui.%{winedll}
%{_libdir}/wine/bthprops.%{winecpl}
%{_libdir}/wine/cabinet.%{winedll}
%{_libdir}/wine/cards.%{winedll}
%{_libdir}/wine/cdosys.%{winedll}
%{_libdir}/wine/cfgmgr32.%{winedll}
%{_libdir}/wine/chcp.%{winecom}
%{_libdir}/wine/clock.%{wineexe}
%{_libdir}/wine/clusapi.%{winedll}
%{_libdir}/wine/combase.%{winedll}
%{_libdir}/wine/comcat.%{winedll}
%{_libdir}/wine/comctl32.%{winedll}
%{_libdir}/wine/comdlg32.%{winedll}
%{_libdir}/wine/compstui.%{winedll}
%{_libdir}/wine/comsvcs.%{winedll}
%{_libdir}/wine/concrt140.%{winedll}
%{_libdir}/wine/connect.%{winedll}
%{_libdir}/wine/credui.%{winedll}
%{_libdir}/wine/crtdll.dll.so
%{_libdir}/wine/crypt32.dll.so
%{_libdir}/wine/cryptdlg.%{winedll}
%{_libdir}/wine/cryptdll.%{winedll}
%{_libdir}/wine/cryptext.%{winedll}
%{_libdir}/wine/cryptnet.%{winedll}
%{_libdir}/wine/cryptui.%{winedll}
%{_libdir}/wine/ctapi32.dll.so
%{_libdir}/wine/ctl3d32.%{winedll}
%{_libdir}/wine/d2d1.%{winedll}
%{_libdir}/wine/d3d10.%{winedll}
%{_libdir}/wine/d3d10_1.%{winedll}
%{_libdir}/wine/d3d10core.%{winedll}
%{_libdir}/wine/d3d11.%{winedll}
%{_libdir}/wine/d3d12.dll.so
%{_libdir}/wine/d3dcompiler_*.%{winedll}
%{_libdir}/wine/d3dim.%{winedll}
%{_libdir}/wine/d3drm.%{winedll}
%{_libdir}/wine/d3dx9_*.%{winedll}
%{_libdir}/wine/d3dx10_*.%{winedll}
%{_libdir}/wine/d3dx11_42.%{winedll}
%{_libdir}/wine/d3dx11_43.%{winedll}
%{_libdir}/wine/d3dxof.%{winedll}
%{_libdir}/wine/davclnt.%{winedll}
%{_libdir}/wine/dbgeng.%{winedll}
%{_libdir}/wine/dbghelp.%{winedll}
%{_libdir}/wine/dciman32.%{winedll}
%{_libdir}/wine/ddraw.%{winedll}
%{_libdir}/wine/ddrawex.%{winedll}
%{_libdir}/wine/devenum.%{winedll}
%{_libdir}/wine/dhcpcsvc.%{winedll}
%{_libdir}/wine/dhtmled.%{wineocx}
%{_libdir}/wine/difxapi.%{winedll}
%{_libdir}/wine/dinput.dll.so
%{_libdir}/wine/dinput8.dll.so
%{_libdir}/wine/directmanipulation.%{winedll}
%{_libdir}/wine/dispex.%{winedll}
%{_libdir}/wine/dmband.%{winedll}
%{_libdir}/wine/dmcompos.%{winedll}
%{_libdir}/wine/dmime.%{winedll}
%{_libdir}/wine/dmloader.%{winedll}
%{_libdir}/wine/dmscript.%{winedll}
%{_libdir}/wine/dmstyle.%{winedll}
%{_libdir}/wine/dmsynth.%{winedll}
%{_libdir}/wine/dmusic.%{winedll}
%{_libdir}/wine/dmusic32.%{winedll}
%{_libdir}/wine/dplay.%{winedll}
%{_libdir}/wine/dplayx.%{winedll}
%{_libdir}/wine/dpnaddr.%{winedll}
%{_libdir}/wine/dpnet.%{winedll}
%{_libdir}/wine/dpnhpast.%{winedll}
%{_libdir}/wine/dpnlobby.%{winedll}
%{_libdir}/wine/dpvoice.%{winedll}
%{_libdir}/wine/dpwsockx.%{winedll}
%{_libdir}/wine/drmclien.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/dsdmo.%{winedll}
%endif
%{_libdir}/wine/dsound.%{winedll}
%{_libdir}/wine/dsquery.%{winedll}
%{_libdir}/wine/dssenh.%{winedll}
%{_libdir}/wine/dswave.%{winedll}
%{_libdir}/wine/dsuiext.%{winedll}
%{_libdir}/wine/dwmapi.%{winedll}
%{_libdir}/wine/dwrite.dll.so
%{_libdir}/wine/dx8vb.%{winedll}
%{_libdir}/wine/dxdiagn.%{winedll}
%{_libdir}/wine/dxgi.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/dxgkrnl.%{winesys}
%{_libdir}/wine/dxgmms1.%{winesys}
%endif
%{_libdir}/wine/dxva2.%{winedll}
%{_libdir}/wine/esent.%{winedll}
%{_libdir}/wine/evr.%{winedll}
%{_libdir}/wine/explorerframe.%{winedll}
%{_libdir}/wine/ext-ms-win-authz-context-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-domainjoin-netjoin-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-dwmapi-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-create-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-create-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-draw-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-draw-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-font-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-font-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-render-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-kernel32-package-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-kernel32-package-current-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-dialogbox-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-gui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-gui-l1-3-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-keyboard-l1-3-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-5-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-message-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-message-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-mouse-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-3-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-rectangle-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-uicontext-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-4.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-windowclass-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-windowclass-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-oleacc-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ras-rasapi32-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-object-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-rgn-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-cursor-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-rawinput-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-syscolors-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-security-credui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-security-cryptui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-comctl32-init-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-comdlg32-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-shell32-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-uxtheme-themes-l1-1-0.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/ext-ms-win-appmodel-usercontext-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-xaml-pal-l1-1-0.dll.so
%endif
%{_libdir}/wine/faultrep.%{winedll}
%{_libdir}/wine/feclient.%{winedll}
%{_libdir}/wine/fltlib.%{winedll}
%{_libdir}/wine/fltmgr.%{winesys}
%{_libdir}/wine/fntcache.%{winedll}
%{_libdir}/wine/fontsub.%{winedll}
%{_libdir}/wine/fusion.%{winedll}
%{_libdir}/wine/fwpuclnt.%{winedll}
%{_libdir}/wine/gameux.%{winedll}
%{_libdir}/wine/gdi32.dll.so
%{_libdir}/wine/gdiplus.%{winedll}
%{_libdir}/wine/glu32.dll.so
%{_libdir}/wine/gphoto2.ds.so
%{_libdir}/wine/gpkcsp.%{winedll}
%{_libdir}/wine/hal.%{winedll}
%{_libdir}/wine/hh.%{wineexe}
%{_libdir}/wine/hhctrl.%{wineocx}
%{_libdir}/wine/hid.%{winedll}
%{_libdir}/wine/hidclass.%{winesys}
%{_libdir}/wine/hlink.%{winedll}
%{_libdir}/wine/hnetcfg.%{winedll}
%{_libdir}/wine/http.%{winesys}
%{_libdir}/wine/httpapi.%{winedll}
%{_libdir}/wine/icacls.%{wineexe}
%{_libdir}/wine/iccvid.%{winedll}
%{_libdir}/wine/icinfo.%{wineexe}
%{_libdir}/wine/icmp.%{winedll}
%{_libdir}/wine/ieframe.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/iertutil.dll.so
%endif
%{_libdir}/wine/ieproxy.%{winedll}
%{_libdir}/wine/imaadp32.%{wineacm}
%{_libdir}/wine/imagehlp.%{winedll}
%{_libdir}/wine/imm32.%{winedll}
%{_libdir}/wine/inetcomm.%{winedll}
%{_libdir}/wine/inetcpl.%{winecpl}
%{_libdir}/wine/inetmib1.%{winedll}
%{_libdir}/wine/infosoft.%{winedll}
%{_libdir}/wine/initpki.%{winedll}
%{_libdir}/wine/inkobj.%{winedll}
%{_libdir}/wine/inseng.%{winedll}
%{_libdir}/wine/iphlpapi.dll.so
%{_libdir}/wine/iprop.%{winedll}
%{_libdir}/wine/irprops.%{winecpl}
%{_libdir}/wine/itircl.%{winedll}
%{_libdir}/wine/itss.%{winedll}
%{_libdir}/wine/joy.%{winecpl}
%{_libdir}/wine/jscript.%{winedll}
%{_libdir}/wine/jsproxy.%{winedll}
%{_libdir}/wine/kerberos.dll.so
%{_libdir}/wine/kernel32.dll.so
%{_libdir}/wine/kernelbase.%{winedll}
%{_libdir}/wine/ksecdd.%{winesys}
%{_libdir}/wine/ksproxy.%{wineax}
%{_libdir}/wine/ksuser.%{winedll}
%{_libdir}/wine/ktmw32.%{winedll}
%{_libdir}/wine/l3codeca.acm.so
%{_libdir}/wine/loadperf.%{winedll}
%{_libdir}/wine/localspl.%{winedll}
%{_libdir}/wine/localui.%{winedll}
%{_libdir}/wine/lodctr.%{wineexe}
%{_libdir}/wine/lz32.%{winedll}
%{_libdir}/wine/mapi32.%{winedll}
%{_libdir}/wine/mapistub.%{winedll}
%{_libdir}/wine/mciavi32.%{winedll}
%{_libdir}/wine/mcicda.%{winedll}
%{_libdir}/wine/mciqtz32.%{winedll}
%{_libdir}/wine/mciseq.%{winedll}
%{_libdir}/wine/mciwave.%{winedll}
%{_libdir}/wine/mf.%{winedll}
%{_libdir}/wine/mf3216.%{winedll}
%{_libdir}/wine/mferror.%{winedll}
%{_libdir}/wine/mfmediaengine.%{winedll}
%{_libdir}/wine/mfplat.%{winedll}
%{_libdir}/wine/mfplay.%{winedll}
%{_libdir}/wine/mfreadwrite.%{winedll}
%{_libdir}/wine/mgmtapi.%{winedll}
%{_libdir}/wine/midimap.%{winedll}
%{_libdir}/wine/mlang.%{winedll}
%{_libdir}/wine/mmcndmgr.%{winedll}
%{_libdir}/wine/mmdevapi.%{winedll}
%{_libdir}/wine/mofcomp.%{wineexe}
%{_libdir}/wine/mountmgr.sys.so
%{_libdir}/wine/mp3dmod.dll.so
%{_libdir}/wine/mpr.%{winedll}
%{_libdir}/wine/mprapi.%{winedll}
%{_libdir}/wine/msacm32.%{winedll}
%{_libdir}/wine/msacm32.%{winedrv}
%{_libdir}/wine/msado15.%{winedll}
%{_libdir}/wine/msadp32.%{wineacm}
%{_libdir}/wine/msasn1.%{winedll}
%{_libdir}/wine/mscat32.%{winedll}
%{_libdir}/wine/mscoree.%{winedll}
%{_libdir}/wine/mscorwks.%{winedll}
%{_libdir}/wine/msctf.%{winedll}
%{_libdir}/wine/msctfp.%{winedll}
%{_libdir}/wine/msdaps.%{winedll}
%{_libdir}/wine/msdelta.%{winedll}
%{_libdir}/wine/msdmo.%{winedll}
%{_libdir}/wine/msdrm.%{winedll}
%{_libdir}/wine/msftedit.%{winedll}
%{_libdir}/wine/msg711.%{wineacm}
%{_libdir}/wine/msgsm32.acm.so
%{_libdir}/wine/mshtml.%{winedll}
%{_libdir}/wine/mshtml.%{winetlb}
%{_libdir}/wine/msi.%{winedll}
%{_libdir}/wine/msident.%{winedll}
%{_libdir}/wine/msimtf.%{winedll}
%{_libdir}/wine/msimg32.%{winedll}
%{_libdir}/wine/msimsg.%{winedll}
%{_libdir}/wine/msinfo32.%{wineexe}
%{_libdir}/wine/msisip.%{winedll}
%{_libdir}/wine/msisys.%{wineocx}
%{_libdir}/wine/msls31.%{winedll}
%{_libdir}/wine/msnet32.%{winedll}
%{_libdir}/wine/mspatcha.%{winedll}
%{_libdir}/wine/msports.%{winedll}
%{_libdir}/wine/msscript.%{wineocx}
%{_libdir}/wine/mssign32.%{winedll}
%{_libdir}/wine/mssip32.%{winedll}
%{_libdir}/wine/msrle32.%{winedll}
%{_libdir}/wine/mstask.%{winedll}
%{_libdir}/wine/msvcirt.%{winedll}
%{_libdir}/wine/msvcm80.%{winedll}
%{_libdir}/wine/msvcm90.%{winedll}
%{_libdir}/wine/msvcp60.%{winedll}
%{_libdir}/wine/msvcp70.%{winedll}
%{_libdir}/wine/msvcp71.%{winedll}
%{_libdir}/wine/msvcp80.%{winedll}
%{_libdir}/wine/msvcp90.%{winedll}
%{_libdir}/wine/msvcp100.%{winedll}
%{_libdir}/wine/msvcp110.%{winedll}
%{_libdir}/wine/msvcp120.%{winedll}
%{_libdir}/wine/msvcp120_app.%{winedll}
%{_libdir}/wine/msvcp140.%{winedll}
%{_libdir}/wine/msvcp140_1.%{winedll}
%{_libdir}/wine/msvcr70.dll.so
%{_libdir}/wine/msvcr71.dll.so
%{_libdir}/wine/msvcr80.dll.so
%{_libdir}/wine/msvcr90.dll.so
%{_libdir}/wine/msvcr100.dll.so
%{_libdir}/wine/msvcr110.dll.so
%{_libdir}/wine/msvcr120.dll.so
%{_libdir}/wine/msvcr120_app.%{winedll}
%{_libdir}/wine/msvcrt.dll.so
%{_libdir}/wine/msvcrt20.%{winedll}
%{_libdir}/wine/msvcrt40.%{winedll}
%{_libdir}/wine/msvcrtd.dll.so
%{_libdir}/wine/msvfw32.%{winedll}
%{_libdir}/wine/msvidc32.%{winedll}
%{_libdir}/wine/mswsock.%{winedll}
%{_libdir}/wine/msxml.%{winedll}
%{_libdir}/wine/msxml2.%{winedll}
%{_libdir}/wine/msxml3.dll.so
%{_libdir}/wine/msxml4.%{winedll}
%{_libdir}/wine/msxml6.%{winedll}
%{_libdir}/wine/mtxdm.%{winedll}
%{_libdir}/wine/nddeapi.%{winedll}
%{_libdir}/wine/ncrypt.%{winedll}
%{_libdir}/wine/ndis.%{winesys}
%{_libdir}/wine/netapi32.dll.so
%{_libdir}/wine/netcfgx.%{winedll}
%{_libdir}/wine/netio.%{winesys}
%{_libdir}/wine/netprofm.%{winedll}
%{_libdir}/wine/netsh.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/netutils.%{winedll}
%endif
%{_libdir}/wine/newdev.%{winedll}
%{_libdir}/wine/ninput.%{winedll}
%{_libdir}/wine/normaliz.%{winedll}
%{_libdir}/wine/npmshtml.%{winedll}
%{_libdir}/wine/npptools.%{winedll}
%{_libdir}/wine/ntdll.so
%{_libdir}/wine/ntdll.dll.so
%{_libdir}/wine/ntdsapi.%{winedll}
%{_libdir}/wine/ntprint.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/nvcuda.dll.so
%{_libdir}/wine/nvcuvid.dll.so
%endif
%{_libdir}/wine/objsel.%{winedll}
%{_libdir}/wine/odbc32.dll.so
%{_libdir}/wine/odbcbcp.%{winedll}
%{_libdir}/wine/odbccp32.%{winedll}
%{_libdir}/wine/odbccu32.%{winedll}
%{_libdir}/wine/ole32.%{winedll}
%{_libdir}/wine/oleacc.%{winedll}
%{_libdir}/wine/oleaut32.%{winedll}
%{_libdir}/wine/olecli32.%{winedll}
%{_libdir}/wine/oledb32.%{winedll}
%{_libdir}/wine/oledlg.%{winedll}
%{_libdir}/wine/olepro32.%{winedll}
%{_libdir}/wine/olesvr32.%{winedll}
%{_libdir}/wine/olethk32.%{winedll}
%{_libdir}/wine/opcservices.%{winedll}
%{_libdir}/wine/packager.%{winedll}
%{_libdir}/wine/pdh.%{winedll}
%{_libdir}/wine/photometadatahandler.%{winedll}
%{_libdir}/wine/pidgen.%{winedll}
%{_libdir}/wine/powrprof.%{winedll}
%{_libdir}/wine/presentationfontcache.%{wineexe}
%{_libdir}/wine/printui.%{winedll}
%{_libdir}/wine/prntvpt.%{winedll}
%{_libdir}/wine/propsys.%{winedll}
%{_libdir}/wine/psapi.%{winedll}
%{_libdir}/wine/pstorec.%{winedll}
%{_libdir}/wine/pwrshplugin.%{winedll}
%{_libdir}/wine/qasf.%{winedll}
%{_libdir}/wine/qcap.dll.so
%{_libdir}/wine/qedit.%{winedll}
%{_libdir}/wine/qdvd.%{winedll}
%{_libdir}/wine/qmgr.%{winedll}
%{_libdir}/wine/qmgrprxy.%{winedll}
%{_libdir}/wine/quartz.%{winedll}
%{_libdir}/wine/query.%{winedll}
%{_libdir}/wine/qwave.%{winedll}
%{_libdir}/wine/rasapi32.%{winedll}
%{_libdir}/wine/rasdlg.%{winedll}
%{_libdir}/wine/regapi.%{winedll}
%{_libdir}/wine/resutils.%{winedll}
%{_libdir}/wine/riched20.%{winedll}
%{_libdir}/wine/riched32.%{winedll}
%{_libdir}/wine/rpcrt4.%{winedll}
%{_libdir}/wine/rsabase.%{winedll}
%{_libdir}/wine/rsaenh.%{winedll}
%{_libdir}/wine/rstrtmgr.%{winedll}
%{_libdir}/wine/rtutils.%{winedll}
%{_libdir}/wine/rtworkq.%{winedll}
%{_libdir}/wine/samlib.%{winedll}
%{_libdir}/wine/sapi.%{winedll}
%{_libdir}/wine/sas.%{winedll}
%{_libdir}/wine/sc.%{wineexe}
%{_libdir}/wine/scarddlg.%{winedll}
%{_libdir}/wine/sccbase.%{winedll}
%{_libdir}/wine/schannel.%{winedll}
%{_libdir}/wine/scrobj.%{winedll}
%{_libdir}/wine/scrrun.%{winedll}
%{_libdir}/wine/scsiport.%{winesys}
%{_libdir}/wine/sechost.%{winedll}
%{_libdir}/wine/secur32.dll.so
%{_libdir}/wine/sensapi.%{winedll}
%{_libdir}/wine/serialui.%{winedll}
%{_libdir}/wine/setupapi.%{winedll}
%{_libdir}/wine/sfc_os.%{winedll}
%{_libdir}/wine/shcore.%{winedll}
%{_libdir}/wine/shdoclc.%{winedll}
%{_libdir}/wine/shdocvw.%{winedll}
%{_libdir}/wine/schedsvc.%{winedll}
%{_libdir}/wine/shell32.dll.so
%{_libdir}/wine/shfolder.%{winedll}
%{_libdir}/wine/shlwapi.%{winedll}
%{_libdir}/wine/shutdown.%{wineexe}
%{_libdir}/wine/slbcsp.%{winedll}
%{_libdir}/wine/slc.%{winedll}
%{_libdir}/wine/snmpapi.%{winedll}
%{_libdir}/wine/softpub.%{winedll}
%{_libdir}/wine/spoolsv.%{wineexe}
%{_libdir}/wine/srclient.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/srvcli.%{winedll}
%endif
%{_libdir}/wine/sspicli.%{winedll}
%{_libdir}/wine/stdole2.%{winetlb}
%{_libdir}/wine/stdole32.%{winetlb}
%{_libdir}/wine/sti.%{winedll}
%{_libdir}/wine/strmdll.%{winedll}
%{_libdir}/wine/subst.%{wineexe}
%{_libdir}/wine/svchost.%{wineexe}
%{_libdir}/wine/svrapi.%{winedll}
%{_libdir}/wine/sxs.%{winedll}
%{_libdir}/wine/systeminfo.%{wineexe}
%{_libdir}/wine/t2embed.%{winedll}
%{_libdir}/wine/tapi32.%{winedll}
%{_libdir}/wine/taskkill.%{wineexe}
%{_libdir}/wine/taskschd.%{winedll}
%{_libdir}/wine/tdh.%{winedll}
%{_libdir}/wine/tdi.%{winesys}
%{_libdir}/wine/traffic.%{winedll}
%{_libdir}/wine/tzres.%{winedll}
%{_libdir}/wine/ucrtbase.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/uianimation.%{winedll}
%endif
%{_libdir}/wine/uiautomationcore.%{winedll}
%{_libdir}/wine/uiribbon.%{winedll}
%{_libdir}/wine/unicows.%{winedll}
%{_libdir}/wine/unlodctr.%{wineexe}
%{_libdir}/wine/updspapi.%{winedll}
%{_libdir}/wine/url.%{winedll}
%{_libdir}/wine/urlmon.%{winedll}
%{_libdir}/wine/usbd.%{winesys}
%{_libdir}/wine/user32.dll.so
%{_libdir}/wine/usp10.%{winedll}
%{_libdir}/wine/utildll.%{winedll}
%{_libdir}/wine/uxtheme.dll.so
%{_libdir}/wine/userenv.%{winedll}
%{_libdir}/wine/vbscript.%{winedll}
%{_libdir}/wine/vcomp.%{winedll}
%{_libdir}/wine/vcomp90.%{winedll}
%{_libdir}/wine/vcomp100.%{winedll}
%{_libdir}/wine/vcomp110.%{winedll}
%{_libdir}/wine/vcomp120.%{winedll}
%{_libdir}/wine/vcomp140.%{winedll}
%{_libdir}/wine/vcruntime140.%{winedll}
%{_libdir}/wine/vcruntime140_1.%{winedll}
%{_libdir}/wine/vdmdbg.%{winedll}
%{_libdir}/wine/vga.%{winedll}
%{_libdir}/wine/version.%{winedll}
%{_libdir}/wine/virtdisk.%{winedll}
%{_libdir}/wine/vssapi.%{winedll}
%{_libdir}/wine/vulkan-1.%{winedll}
%{_libdir}/wine/wbemdisp.%{winedll}
%{_libdir}/wine/wbemprox.%{winedll}
%{_libdir}/wine/wdscore.%{winedll}
%{_libdir}/wine/webservices.%{winedll}
%{_libdir}/wine/wer.%{winedll}
%{_libdir}/wine/wevtapi.%{winedll}
%{_libdir}/wine/where.%{wineexe}
%{_libdir}/wine/whoami.%{wineexe}
%{_libdir}/wine/wiaservc.%{winedll}
%{_libdir}/wine/wimgapi.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/win32k.%{winesys}
%{_libdir}/wine/windows.gaming.input.%{winedll}
%{_libdir}/wine/windows.media.speech.%{winedll}
%endif
%{_libdir}/wine/windowscodecs.dll.so
%{_libdir}/wine/windowscodecsext.%{winedll}
%{_libdir}/wine/winebus.sys.so
%{_libdir}/wine/winegstreamer.dll.so
%{_libdir}/wine/winehid.%{winesys}
%{_libdir}/wine/winejoystick.drv.so
%{_libdir}/wine/winemapi.%{winedll}
%{_libdir}/wine/winevulkan.dll.so
%{_libdir}/wine/wineusb.sys.so
%{_libdir}/wine/winex11.drv.so
%{_libdir}/wine/wing32.%{winedll}
%{_libdir}/wine/winhttp.%{winedll}
%{_libdir}/wine/wininet.%{winedll}
%{_libdir}/wine/winmm.%{winedll}
%{_libdir}/wine/winnls32.%{winedll}
%{_libdir}/wine/winspool.drv.so
%{_libdir}/wine/winsta.%{winedll}
%{_libdir}/wine/wlanui.%{winedll}
%{_libdir}/wine/wmasf.%{winedll}
%{_libdir}/wine/wmi.%{winedll}
%{_libdir}/wine/wmic.%{wineexe}
%{_libdir}/wine/wmiutils.%{winedll}
%{_libdir}/wine/wmp.%{winedll}
%{_libdir}/wine/wmvcore.%{winedll}
%{_libdir}/wine/spoolss.%{winedll}
%{_libdir}/wine/winscard.%{winedll}
%{_libdir}/wine/wintab32.%{winedll}
%{_libdir}/wine/wintrust.%{winedll}
%{_libdir}/wine/winusb.%{winedll}
%{_libdir}/wine/wlanapi.%{winedll}
%{_libdir}/wine/wmphoto.%{winedll}
%{_libdir}/wine/wnaspi32.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/wow64cpu.dll.so
%endif
%{_libdir}/wine/wpc.%{winedll}
%{_libdir}/wine/wpcap.dll.so
%{_libdir}/wine/ws2_32.dll.so
%{_libdir}/wine/wsdapi.%{winedll}
%{_libdir}/wine/wshom.%{wineocx}
%{_libdir}/wine/wsnmp32.%{winedll}
%{_libdir}/wine/wsock32.%{winedll}
%{_libdir}/wine/wtsapi32.%{winedll}
%{_libdir}/wine/wuapi.%{winedll}
%{_libdir}/wine/wuaueng.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/wuauserv.%{wineexe}
%endif
%{_libdir}/wine/security.%{winedll}
%{_libdir}/wine/sfc.%{winedll}
%{_libdir}/wine/wineps.%{winedrv}
%{_libdir}/wine/d3d8.%{winedll}
%{_libdir}/wine/d3d9.%{winedll}
%{_libdir}/wine/opengl32.dll.so
%{_libdir}/wine/wined3d.dll.so
%{_libdir}/wine/dnsapi.dll.so
%{_libdir}/wine/iexplore.%{wineexe}
%{_libdir}/wine/xactengine3_0.dll.so
%{_libdir}/wine/xactengine3_1.dll.so
%{_libdir}/wine/xactengine3_2.dll.so
%{_libdir}/wine/xactengine3_3.dll.so
%{_libdir}/wine/xactengine3_4.dll.so
%{_libdir}/wine/xactengine3_5.dll.so
%{_libdir}/wine/xactengine3_6.dll.so
%{_libdir}/wine/xactengine3_7.dll.so
%{_libdir}/wine/x3daudio1_0.dll.so
%{_libdir}/wine/x3daudio1_1.dll.so
%{_libdir}/wine/x3daudio1_2.dll.so
%{_libdir}/wine/x3daudio1_3.dll.so
%{_libdir}/wine/x3daudio1_4.dll.so
%{_libdir}/wine/x3daudio1_5.dll.so
%{_libdir}/wine/x3daudio1_6.dll.so
%{_libdir}/wine/x3daudio1_7.dll.so
%{_libdir}/wine/xapofx1_1.dll.so
%{_libdir}/wine/xapofx1_2.dll.so
%{_libdir}/wine/xapofx1_3.dll.so
%{_libdir}/wine/xapofx1_4.dll.so
%{_libdir}/wine/xapofx1_5.dll.so
%{_libdir}/wine/xaudio2_0.dll.so
%{_libdir}/wine/xaudio2_1.dll.so
%{_libdir}/wine/xaudio2_2.dll.so
%{_libdir}/wine/xaudio2_3.dll.so
%{_libdir}/wine/xaudio2_4.dll.so
%{_libdir}/wine/xaudio2_5.dll.so
%{_libdir}/wine/xaudio2_6.dll.so
%{_libdir}/wine/xaudio2_7.dll.so
%{_libdir}/wine/xaudio2_8.dll.so
%{_libdir}/wine/xaudio2_9.dll.so
%{_libdir}/wine/xcopy.%{wineexe}
%{_libdir}/wine/xinput1_1.%{winedll}
%{_libdir}/wine/xinput1_2.%{winedll}
%{_libdir}/wine/xinput1_3.%{winedll}
%{_libdir}/wine/xinput1_4.%{winedll}
%{_libdir}/wine/xinput9_1_0.%{winedll}
%{_libdir}/wine/xmllite.%{winedll}
%{_libdir}/wine/xolehlp.%{winedll}
%{_libdir}/wine/xpsprint.%{winedll}
%{_libdir}/wine/xpssvcs.%{winedll}

%if 0%{?wine_staging}
%ifarch x86_64 aarch64
%{_libdir}/wine/nvapi64.dll.so
%{_libdir}/wine/nvencodeapi64.dll.so
%else
%{_libdir}/wine/nvapi.dll.so
%{_libdir}/wine/nvencodeapi.dll.so
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/winevdm.exe.so
%{_libdir}/wine/ifsmgr.%{winevxd}
%{_libdir}/wine/mmdevldr.%{winevxd}
%{_libdir}/wine/monodebg.%{winevxd}
%{_libdir}/wine/rundll.%{wineexe16}
%{_libdir}/wine/vdhcp.%{winevxd}
%{_libdir}/wine/user.%{wineexe16}
%{_libdir}/wine/vmm.%{winevxd}
%{_libdir}/wine/vnbt.%{winevxd}
%{_libdir}/wine/vnetbios.%{winevxd}
%{_libdir}/wine/vtdapi.%{winevxd}
%{_libdir}/wine/vwin32.%{winevxd}
%{_libdir}/wine/w32skrnl.%{winedll}
%{_libdir}/wine/avifile.%{winedll16}
%{_libdir}/wine/comm.%{winedrv16}
%{_libdir}/wine/commdlg.%{winedll16}
%{_libdir}/wine/compobj.%{winedll16}
%{_libdir}/wine/ctl3d.%{winedll16}
%{_libdir}/wine/ctl3dv2.%{winedll16}
%{_libdir}/wine/ddeml.%{winedll16}
%{_libdir}/wine/dispdib.%{winedll16}
%{_libdir}/wine/display.%{winedrv16}
%{_libdir}/wine/gdi.%{wineexe16}
%{_libdir}/wine/imm.%{winedll16}
%{_libdir}/wine/krnl386.%{wineexe16}
%{_libdir}/wine/keyboard.%{winedrv16}
%{_libdir}/wine/lzexpand.%{winedll16}
%{_libdir}/wine/mmsystem.%{winedll16}
%{_libdir}/wine/mouse.%{winedrv16}
%{_libdir}/wine/msacm.%{winedll16}
%{_libdir}/wine/msvideo.%{winedll16}
%{_libdir}/wine/ole2.%{winedll16}
%{_libdir}/wine/ole2conv.%{winedll16}
%{_libdir}/wine/ole2disp.%{winedll16}
%{_libdir}/wine/ole2nls.%{winedll16}
%{_libdir}/wine/ole2prox.%{winedll16}
%{_libdir}/wine/ole2thk.%{winedll16}
%{_libdir}/wine/olecli.%{winedll16}
%{_libdir}/wine/olesvr.%{winedll16}
%{_libdir}/wine/rasapi16.%{winedll16}
%{_libdir}/wine/setupx.%{winedll16}
%{_libdir}/wine/shell.%{winedll16}
%{_libdir}/wine/sound.%{winedrv16}
%{_libdir}/wine/storage.%{winedll16}
%{_libdir}/wine/stress.%{winedll16}
%{_libdir}/wine/system.%{winedrv16}
%{_libdir}/wine/toolhelp.%{winedll16}
%{_libdir}/wine/twain.%{winedll16}
%{_libdir}/wine/typelib.%{winedll16}
%{_libdir}/wine/ver.%{winedll16}
%{_libdir}/wine/w32sys.%{winedll16}
%{_libdir}/wine/win32s16.%{winedll16}
%{_libdir}/wine/win87em.%{winedll16}
%{_libdir}/wine/winaspi.%{winedll16}
%{_libdir}/wine/windebug.%{winedll16}
%{_libdir}/wine/wineps16.%{winedrv16}
%{_libdir}/wine/wing.%{winedll16}
%{_libdir}/wine/winhelp.%{wineexe16}
%{_libdir}/wine/winnls.%{winedll16}
%{_libdir}/wine/winoldap.%{winemod16}
%{_libdir}/wine/winsock.%{winedll16}
%{_libdir}/wine/wintab.%{winedll16}
%{_libdir}/wine/wow32.%{winedll}
%endif

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/winebus.inf
%{_datadir}/wine/winehid.inf
%{_datadir}/wine/wineusb.inf
%{_datadir}/wine/nls/c_037.nls
%{_datadir}/wine/nls/c_10000.nls
%{_datadir}/wine/nls/c_10001.nls
%{_datadir}/wine/nls/c_10002.nls
%{_datadir}/wine/nls/c_10003.nls
%{_datadir}/wine/nls/c_10004.nls
%{_datadir}/wine/nls/c_10005.nls
%{_datadir}/wine/nls/c_10006.nls
%{_datadir}/wine/nls/c_10007.nls
%{_datadir}/wine/nls/c_10008.nls
%{_datadir}/wine/nls/c_10010.nls
%{_datadir}/wine/nls/c_10017.nls
%{_datadir}/wine/nls/c_10021.nls
%{_datadir}/wine/nls/c_10029.nls
%{_datadir}/wine/nls/c_10079.nls
%{_datadir}/wine/nls/c_10081.nls
%{_datadir}/wine/nls/c_10082.nls
%{_datadir}/wine/nls/c_1026.nls
%{_datadir}/wine/nls/c_1250.nls
%{_datadir}/wine/nls/c_1251.nls
%{_datadir}/wine/nls/c_1252.nls
%{_datadir}/wine/nls/c_1253.nls
%{_datadir}/wine/nls/c_1254.nls
%{_datadir}/wine/nls/c_1255.nls
%{_datadir}/wine/nls/c_1256.nls
%{_datadir}/wine/nls/c_1257.nls
%{_datadir}/wine/nls/c_1258.nls
%{_datadir}/wine/nls/c_1361.nls
%{_datadir}/wine/nls/c_20127.nls
%{_datadir}/wine/nls/c_20866.nls
%{_datadir}/wine/nls/c_20932.nls
%{_datadir}/wine/nls/c_21866.nls
%{_datadir}/wine/nls/c_28591.nls
%{_datadir}/wine/nls/c_28592.nls
%{_datadir}/wine/nls/c_28593.nls
%{_datadir}/wine/nls/c_28594.nls
%{_datadir}/wine/nls/c_28595.nls
%{_datadir}/wine/nls/c_28596.nls
%{_datadir}/wine/nls/c_28597.nls
%{_datadir}/wine/nls/c_28598.nls
%{_datadir}/wine/nls/c_28599.nls
%{_datadir}/wine/nls/c_28603.nls
%{_datadir}/wine/nls/c_28605.nls
%{_datadir}/wine/nls/c_437.nls
%{_datadir}/wine/nls/c_500.nls
%{_datadir}/wine/nls/c_737.nls
%{_datadir}/wine/nls/c_775.nls
%{_datadir}/wine/nls/c_850.nls
%{_datadir}/wine/nls/c_852.nls
%{_datadir}/wine/nls/c_855.nls
%{_datadir}/wine/nls/c_857.nls
%{_datadir}/wine/nls/c_860.nls
%{_datadir}/wine/nls/c_861.nls
%{_datadir}/wine/nls/c_862.nls
%{_datadir}/wine/nls/c_863.nls
%{_datadir}/wine/nls/c_864.nls
%{_datadir}/wine/nls/c_865.nls
%{_datadir}/wine/nls/c_866.nls
%{_datadir}/wine/nls/c_869.nls
%{_datadir}/wine/nls/c_874.nls
%{_datadir}/wine/nls/c_875.nls
%{_datadir}/wine/nls/c_932.nls
%{_datadir}/wine/nls/c_936.nls
%{_datadir}/wine/nls/c_949.nls
%{_datadir}/wine/nls/c_950.nls
%{_datadir}/wine/nls/l_intl.nls
%{_datadir}/wine/nls/normidna.nls
%{_datadir}/wine/nls/normnfc.nls
%{_datadir}/wine/nls/normnfd.nls
%{_datadir}/wine/nls/normnfkc.nls
%{_datadir}/wine/nls/normnfkd.nls
%{_datadir}/wine/nls/sortdefault.nls

%files common
%{_bindir}/notepad
%{_bindir}/winedbg
%{_bindir}/winefile
%{_bindir}/winemine
%{_bindir}/winemaker
%{_bindir}/winepath
%{_bindir}/msiexec
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/wineboot
%{_bindir}/wineconsole
%{_bindir}/winecfg
%{_mandir}/man1/wine.1*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*

%files fonts
# meta package

%if 0%{?wine_staging}
%files arial-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/arial*
%endif

%files courier-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cou*

%files fixedsys-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/*vgafix.fon

%files system-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cvgasys.fon
%{_datadir}/wine/fonts/hvgasys.fon
%{_datadir}/wine/fonts/jvgasys.fon
%{_datadir}/wine/fonts/svgasys.fon
%{_datadir}/wine/fonts/vgas1255.fon
%{_datadir}/wine/fonts/vgas1256.fon
%{_datadir}/wine/fonts/vgas1257.fon
%{_datadir}/wine/fonts/vgas874.fon
%{_datadir}/wine/fonts/vgasys.fon
%{_datadir}/wine/fonts/vgasyse.fon
%{_datadir}/wine/fonts/vgasysg.fon
%{_datadir}/wine/fonts/vgasysr.fon
%{_datadir}/wine/fonts/vgasyst.fon

%files small-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sma*
%{_datadir}/wine/fonts/jsma*

%files marlett-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/marlett.ttf

%files ms-sans-serif-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sse*
%if 0%{?wine_staging}
%{_datadir}/wine/fonts/msyh.ttf
%endif

%files tahoma-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/tahoma*ttf

%files tahoma-fonts-system
%doc README-tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%if 0%{?wine_staging}
%files times-new-roman-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/times.ttf

%files times-new-roman-fonts-system
%{_datadir}/fonts/wine-times-new-roman-fonts
%endif

%files symbol-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/symbol.ttf

%files webdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/webdings.ttf

%files webdings-fonts-system
%{_datadir}/fonts/wine-webdings-fonts

%files wingdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/wingding.ttf

%files wingdings-fonts-system
%{_datadir}/fonts/wine-wingdings-fonts

%files desktop
%{_datadir}/applications/wine-iexplore.desktop
%{_datadir}/applications/wine-inetcpl.desktop
%{_datadir}/applications/wine-joycpl.desktop
%{_datadir}/applications/wine-taskmgr.desktop
%{_datadir}/applications/wine-notepad.desktop
%{_datadir}/applications/wine-winefile.desktop
%{_datadir}/applications/wine-winemine.desktop
%{_datadir}/applications/wine-mime-msi.desktop
%{_datadir}/applications/wine.desktop
%{_datadir}/applications/wine-regedit.desktop
%{_datadir}/applications/wine-uninstaller.desktop
%{_datadir}/applications/wine-winecfg.desktop
%{_datadir}/applications/wine-wineboot.desktop
%{_datadir}/applications/wine-winhelp.desktop
%{_datadir}/applications/wine-wordpad.desktop
%{_datadir}/applications/wine-oleview.desktop
%{_datadir}/desktop-directories/Wine.directory
%config %{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/*png
%{_datadir}/icons/hicolor/scalable/apps/*svg

%files systemd
%config %{_binfmtdir}/wine.conf

%if 0%{?rhel} == 6
%files sysvinit
%{_initrddir}/wine
%endif

# ldap subpackage
%files ldap
%{_libdir}/wine/wldap32.dll.so

# cms subpackage
%files cms
%{_libdir}/wine/mscms.dll.so

# twain subpackage
%files twain
%{_libdir}/wine/twain_32.%{winedll}
%{_libdir}/wine/sane.ds.so

# capi subpackage
%files capi
%{_libdir}/wine/capi2032.dll.so

%files devel
%{_bindir}/function_grep.pl
%{_bindir}/widl
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winedump
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/wmc
%{_bindir}/wrc
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/winemaker.1*
%attr(0755, root, root) %dir %{_includedir}/wine
%{_includedir}/wine/*
%{_libdir}/*.so
%{_libdir}/wine/*.a
%{_libdir}/wine/*.def

%files pulseaudio
%{_libdir}/wine/winepulse.drv.so

%files alsa
%{_libdir}/wine/winealsa.drv.so

%files openal
%{_libdir}/wine/openal32.dll.so

%files opencl
%{_libdir}/wine/opencl.dll.so


%changelog
* Sat Sep 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.17-100
- 5.17
- tkg updates

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.16-101.20200904git432858b
- Snapshot

* Sun Aug 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.16-100
- 5.16

* Thu Aug 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-104.20200826git666f614
- New snapshot

* Sat Aug 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-103.20200821gitab94abb
- Bump

* Wed Aug 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-102.20200818git8f3bd63
- Snapshot

* Mon Aug 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-101
- Staging update

* Sun Aug 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.15-100
- 5.15

* Sat Aug 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-103.20200807git1ec8bf9
- New snapshot

* Thu Aug 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-102.20200806git8cbbb4f
- Bump

* Wed Aug 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-101.20200804git2b76b9f
- Snapshot

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.14-100
- 5.14
- New Webdings font

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.13-102.20200724git0d42388
- nofshack fixes

* Sat Jul 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.13-101.20200724git0d42388
- Snapshot

* Sun Jul 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.13-100
- 5.13

* Wed Jul 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-103.20200714git54b2a10
- Bump

* Mon Jul 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-102.20200713gitcaa41d4
- Snapshot

* Mon Jul 06 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-101
- Staging update

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.12-100
- 5.12

* Thu Jul 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-103.20200701git10b1793
- Bump

* Sat Jun 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-102.20200626git13b2587
- New snapshot and more fsync reverts

* Mon Jun 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-101
- tkg and ge minor updates

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.11-100
- 5.11

* Tue Jun 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.10-106.20200615git634cb77
- New snapshot

* Sun Jun 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-105.20200612git948a6a4
- Bump

* Thu Jun 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-104.20200610git3430431
- New snapshot

* Wed Jun 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-103.20200609gitbf454cc
- Bump

* Tue Jun 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-102.20200608git1752958
- Snapshot
- wine-mono 5.1.0

* Mon Jun 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-101
- Staging update

* Sat Jun 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.10-100
- 5.10

* Thu Jun 04 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.9-102.20200603gitaba27fd
- Bump

* Wed Jun 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.9-101.20200602git48020f4
- Snapshot and tkg reverts

* Sat May 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.9-100
- 5.9

* Wed May 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-105.20200515git4358ddc
- Fix wine-mono patch

* Tue May 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-104.20200515git3bb824f
- New snapshot
- wine-mono 5.0.1

* Sat May 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-103.20200515git9e26bc8
- Bump

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-102.20200513gitdebe646
- Snapshot

* Mon May 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-101
- Bug#49109/49128 better fix

* Sat May 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.8-100
- 5.8

* Thu May 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-108.20200506git148fc1a
- Bump
- Revert some upstream patches to fix 64 bit Unity3D games

* Tue May 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-107.20200504git4e2ad33
- New snapshot

* Sat May 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-106.20200501gitd1f858e
- Disable fshack again, not good yet
- Bump

* Fri May 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-105.20200430git0c27d24
- New snapshot
- Patchsets review
- Reenable fshack

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-104.20200428git7ccc45f
- Bump and tkg reverts

* Tue Apr 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-103.20200427git28ec279
- Again

* Tue Apr 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-102.20200427git28ec279
- Snapshot

* Sun Apr 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-101
- Bug 49011 fix

* Sat Apr 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.7-100
- 5.7

* Thu Apr 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-104.20200422gitf52b33c
- Bump

* Tue Apr 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-103.20200420gitf31a29b
- New snapshot
- winemono 5.0.0

* Sun Apr 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-102.20200417git59987bc
- Bump

* Wed Apr 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-101.20200415gitf6c131f
- Snapshot

* Sat Apr 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.6-100
- 5.6

* Fri Apr 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.5-102.20200402git3047385
- Snapshot

* Mon Mar 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.5-101
- Staging fixes
- Revert server timeout disabled by proton-tkg-staging patch

* Sun Mar 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.5-100
- 5.5
- New tkg links

* Wed Mar 25 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.4-102.20200324git9c190f8
- Bump

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.4-101.20200320git3ddf3a7
- Snapshot
- Disable some compilation flags

* Sat Mar 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.4-100
- 5.4

* Wed Mar 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-103.20200310git4dfd5f2
- Bump

* Sat Mar 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-102.20200306giteb63713
- Bump

* Thu Mar 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-101.20200304git0eea1b0
- Snapshot

* Sat Feb 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.3-100
- 5.3

* Fri Feb 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.2-102.20200227gitc6b852e
- Bump
- BR: libgcrypt

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.2-101.20200221gitb253bd6
- Snapshot

* Sun Feb 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.2-100
- 5.2

* Tue Feb 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.1-102.20200210git0df9cce
- New snapshot
- tkg sync
- FS hack switch, disabled for the time

* Sun Feb 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.1-101.20200207gitf909d18
- New snapshot

* Sun Feb 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.1-100
- 5.1

* Tue Jan 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0-100
- 5.0

* Sat Jan 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc6-100
- 5.0-rc6

* Wed Jan 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc5-101.20200114git9f8935d
- New snapshot

* Sat Jan 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc5-100
- 5.0-rc5

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc4-100
- 5.0-rc4

* Wed Jan 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc3-100.20191230git5034d10
- 5.0-rc3

* Sat Dec 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc2-100
- 5.0-rc2

* Sat Dec 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:5.0~rc1-100
- 5.0-rc1

* Thu Dec 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.21-102.20191211git750d382
- New snapshot
- wine-gecko 2.47.1
- Fix gtk3 requires when disabled

* Fri Dec 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.21-101.20191205git7ca1c49
- Snapshot

* Sat Nov 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.21-100
- 4.21

* Thu Nov 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.20-102.20191127git4ccdf3e
- Snapshot

* Thu Nov 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.20-101.20191120gitaa3d01e
- Snapshot

* Sat Nov 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.20-100
- 4.20

* Tue Nov 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-105.20191112git292b728
- New snapshot, again

* Thu Nov 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-104
- Revert to release

* Thu Nov 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-103.20191106gitf205838
- Try to fix last one

* Wed Nov 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-102.20191105git7f469b6
- New snapshot
- Patchsets review. All extra patches applied only with staging

* Mon Nov 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-101
- Update revert list

* Sat Nov 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-100
- 4.19

* Sat Oct 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.18-100
- 4.18

* Mon Oct 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-103.20191009git71e96bd
- New snapshot
- R: gstreamer1-plugins-good

* Thu Oct 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-102.20191002git5e8eb5f
- Snapshot

* Sun Sep 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-101
- tkg updates and some reverts

* Sat Sep 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-100
- 4.17
- Retire deprecated isdn4k-utils support

* Wed Sep 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-102
- tkg updates

* Sun Sep 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-101
- tkg updates

* Sat Sep 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-100
- 4.16
- raw-input switch

* Sun Sep 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.15-101
- Disable raw-input

* Sat Aug 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.15-100
- 4.15

* Tue Aug 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-103
- tkg updates

* Fri Aug 23 2019 Phantom X <megaphantomx at bol dot com dot br>  - 1:4.14-102
- tkg updates

* Mon Aug 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-101
- Missing patch
- Deprecate old unmaintained patches

* Sat Aug 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-100
- 4.14

* Fri Aug 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.13-101
- Upstream and tkg updates
- Mono update

* Sat Aug 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.13-100
- 4.13

* Tue Jul 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-105
- Staging and tkg updates

* Fri Jul 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-104
- Try again

* Thu Jul 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-103
- Something broke

* Wed Jul 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-102
- Update staging patchset
- Raw input fix by Guy1524

* Sun Jul 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-101
- mingw build
- gtk3 switch, disabled by default

* Sun Jul 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-100
- 4.12.1

* Sat Jul 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12-100
- 4.12
- f30 sync

* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.11-100
- 4.11

* Sat Jun 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.10-101
- Monotonic patch update from tkg

* Mon Jun 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.10-100
- 4.10

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.9-101
- Some fixes from bugzilla

* Sat May 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.9-100
- 4.9

* Tue May 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-102
- Trim down reverts
- Update staging
- chinforpms experimental message and README
- Trim changelog

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-101
- Revert some upstream patches to fix joystick issues
- Revert staging patch to fix symlink issues

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-100
- 4.8

* Thu May 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.7-101
- no-PIC flags patches from upstream

* Mon Apr 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.7-100
- 4.7

* Thu Apr 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.6-101
- wine-mono 4.8.2

* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.6-100
- 4.6
- esync merged with staging

* Sat Mar 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.5-100
- 4.5

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-103
- Revert xaudio2_7 application name patch, new one fail

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-102
- Replace xaudio2_7 application name with pulseaudio patch

* Mon Mar 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-101
- Some FAudio updates from Valve git

* Sun Mar 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-100
- 4.4

* Mon Mar 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.3-101
- Upstream fixes for whq#42982 and whq#43071

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.3-100
- 4.3
- pkgconfig style BRs
- Upstream FAudio support

* Mon Feb 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.2-101
- faudio update from tkg

* Sun Feb 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.2-100
- 4.2
- Add -ftree-vectorize -ftree-slp-vectorize to CFLAGS

* Mon Feb 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.1-100
- 4.1

* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0-101
- Optional enabled FAudio support. Obsoletes wine-xaudio and wine-freeworld
- Remove old Fedora and RH conditionals, only current Fedora is supported

* Tue Jan 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0-100
- 4.0

* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc7-101
- Patch to fix wine-dxup build

* Sat Jan 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc7-100
- 4.0-rc7

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc6-100
- 4.0-rc6
- Revert -O1 optimizations, seems good now
- Disable mime type registering

* Mon Jan 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc5-101
- Fix includedir

* Sat Jan 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc5-100
- 4.0-rc5

* Sun Dec 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc4-100
- 4.0-rc4

* Sat Dec 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc3-100
- 4.0-rc3

* Tue Dec 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc2-101
- Some Tk-Glitch patches, including optional esync

* Mon Dec 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc2-100
- 4.0-rc2

* Sat Dec 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc1-100
- 4.0-rc1

* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.21-100
- 3.21
- Disable broken wine-pba
- Change rc versioning to "~" system

* Fri Nov 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.20-100.chinfo
- 3.20

* Mon Oct 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.19-100.chinfo
- 3.19

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.18-100.chinfo
- 3.18

* Sun Sep 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.17-100.chinfo
- 3.17

* Thu Sep 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.16-100.chinfo
- 3.16

* Thu Sep 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-104.chinfo
- More upstream fixes
- Change compiler optimizations to -O1 to fix whq#45199

* Sat Sep 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-103.chinfo
- Try again again

* Fri Sep 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-102.chinfo
- Try again

* Thu Sep 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-101.chinfo
- Random upstream patches

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-100.chinfo
- 3.15

* Mon Aug 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-103.chinfo
- Revert pulseaudio fixes

* Mon Aug 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-102.chinfo
- wine-pba patches
- Try new pulseaudio fixes
- license macros

* Fri Aug 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-101.chinfo
- Virtual desktop fix

* Mon Aug 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-100.chinfo
- 3.14

* Sun Aug 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-102.chinfo
- Staging update

* Sun Jul 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-101.chinfo
- Revert to old staging winepulse patches

* Sat Jul 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-100.chinfo
- 3.13
- Clean xaudio2 package, only xaudio2_7.dll.so is needed

* Tue Jul 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.12-100.chinfo
- 3.12
- Split xaudio2, for freeworld packages support

* Sun Jun 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.11-100.chinfo
- 3.11

* Mon Jun 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.10-100.chinfo
- 3.10

* Sat May 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.9-100.chinfo
- 3.9
- BR: vkd3d-devel
- f28 sync

* Sat May 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.8-100.chinfo
- 3.8

* Sat Apr 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.7-100.chinfo
- 3.7

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-102.chinfo
- Revert ARMv7 fix.

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-101.chinfo
- f28 sync

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-100.chinfo
- 3.6

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.5-100.chinfo
- 3.5

* Fri Mar 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.4-100.chinfo
- 3.4

* Sun Mar 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.3-100.chinfo
- 3.3
- Updated URLs
- New wine-staging URL
- s/compholio/staging/
- BR: samba-devel
- BR: SDL2-devel
- BR: vulkan-devel
- R: samba-libs

* Tue Nov 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.21-100.chinfo
- 2.21
- Drop nine, it have proper separated wine-nine package now
- Drop laino package, only one patch is needed
- Update patch list from AUR

* Mon Nov 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.20-100.chinfo
- 2.20
- Rearrange files that are already in default wine from %%{?compholios} sections

* Mon Oct 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.19-101.chinfo
- wine-d3d9 2.19

* Sat Oct 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.19-100.chinfo
- 2.19

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.18-101.chinfo
- BR: mesa-libEGL-devel with nine, fixes Fedora 27 build

* Thu Oct 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.18-100.chinfo
- 2.18

* Wed Sep 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.17-100.chinfo
- 2.17

* Thu Sep 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.16-100.chinfo
- 2.16

* Wed Aug 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.15-100.chinfo
- 2.15

* Thu Aug 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.14-101.chinfo
- nine 2.14

* Tue Aug 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.14-100.chinfo
- 2.14

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.13-100.chinfo
- 2.13
- Disable laino patches

* Wed Jul 12 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.12-100.chinfo
- 2.12

* Tue Jun 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.11-100.chinfo
- 2.11

* Tue Jun 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.10-100.chinfo
- 2.10
- laino patches

* Mon May 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.9-100.chinfo
- 2.9

* Tue May 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.8-100.chinfo
- 2.8

* Tue May 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.7-100.chinfo
- 2.7

* Wed Apr 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.6-100.chinfo
- 2.6

* Sun Apr 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.5-100.chinfo
- 2.5

* Sun Mar 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.4-101.chinfo
- Fix wine-mono version

* Tue Mar 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.4-100.chinfo
- 2.4

* Mon Mar 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.3-100.chinfo
- 2.3

* Wed Feb 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.2-100.chinfo
- 2.2

* Thu Feb 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-100.chinfo
- 2.1

* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-100.chinfo
- 2.0 final

* Mon Jan 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.7.rc7.chinfo
- 2.0-rc6

* Mon Jan 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.6.rc5.chinfo
- 2.0-rc5

* Mon Jan 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.5.rc4.chinfo
- 2.0-rc4

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.4.rc3.nine
- rebuilt

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.3.rc3.nine
- Drop epoch.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.2.rc3.nine
- nine patches
- extra patches
- joy.cpl desktop file

* Tue Dec 27 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc3
- version update

* Wed Dec 21 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc2
- version update

* Thu Dec 15 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc1
- version update

* Wed Nov 23 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-2
- drop sysvinit on Fedora, again

* Wed Nov 16 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-1
- version update
- remove old cruft in spec
- add hard cups-libs dependency (rhbz#1367537)
- include mp3 support (rhbz#1395711)

* Thu Nov 03 2016 Michael Cronenworth <mike@cchtml.com> 1.9.22-1
- version update

* Mon Oct 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.21-1
- version update

* Sun Oct 02 2016 Michael Cronenworth <mike@cchtml.com> 1.9.20-1
- version update

* Mon Sep 19 2016 Michael Cronenworth <mike@cchtml.com> 1.9.19-1
- version update

* Thu Sep 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.18-2
- fix aarch64 definition

* Wed Sep 07 2016 Michael Cronenworth <mike@cchtml.com> 1.9.18-1
- version update

* Sun Aug 28 2016 Michael Cronenworth <mike@cchtml.com> 1.9.17-1
- version update

* Sat Aug 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.16-2
- build on aarch64

* Tue Aug 09 2016 Michael Cronenworth <mike@cchtml.com> 1.9.16-1
- version update
