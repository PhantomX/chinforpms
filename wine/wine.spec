%global commit d92866863f6b5ca01675254ad315659b40f88ed4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220527
%global with_snapshot 0

# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%undefine _auto_set_build_flags
%undefine _package_note_file

# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%global _lto_cflags %{nil}


%global winearchdir %{nil}
%global winesodir %{nil}
%ifarch %{ix86}
%global winearchdir i386-windows
%global winesodir i386-unix
%endif
%ifarch x86_64
%global winearchdir x86_64-windows
%global winesodir x86_64-unix
%endif
%ifarch arm
%global winearchdir arm-windows
%global winesodir arm-unix
%endif
%ifarch aarch64
%global winearchdir aarch64-windows
%global winesodir aarch64-unix
%global __brp_llvm_compile_lto_elf %nil
%global __brp_strip_lto %nil
%global __brp_strip_static_archive %nil
%endif

%ifarch %{ix86} x86_64
%global wine_mingw 1
# Package mingw files with debuginfo
%global with_debug 0
%endif
%global no64bit   0
%global winefastsync 5.16
%global winegecko 2.47.2
%global winemono  7.3.0
%global winevulkan 1.3.215

%global wineFAudio 22.02
%global winegsm 1.0.19
%global winejpeg 9e
%global winelcms2 2.13.1
%global winempg123 1.29.3
%global winepng 1.6.37
%global winetiff 4.3.0
%global winejxrlib 1.1
%global winevkd3d 1.3
%global winexml2 2.9.14
%global winexslt 1.1.35
%global winezlib 1.2.12

%global _default_patch_fuzz 2

%global libext .so
%global winedlldir %{winesodir}

%if 0%{?wine_mingw}
%undefine _annotated_build
%global libext %{nil}
%global winedlldir %{winearchdir}
%endif

%global wineacm acm%{?libext}
%global wineax ax%{?libext}
%global winecom com%{?libext}
%global winecpl cpl%{?libext}
%global winedll dll%{?libext}
%global winedll16 dll16%{?libext}
%global winedrv drv%{?libext}
%global winedrv16 drv16%{?libext}
%global wineds ds%{?libext}
%global wineexe exe%{?libext}
%global wineexe16 exe16%{?libext}
%global winemod16 mod16%{?libext}
%global wineocx ocx%{?libext}
%global winesys sys%{?libext}
%global winetlb tlb%{?libext}
%global winevxd vxd%{?libext}
%global winemsstyles msstyles%{?libext}

# build with staging-patches, see:  https://wine-staging.com/
# 1 to enable; 0 to disable.
%global wine_staging 1
%global wine_stagingver 7.10
%global wine_stg_url https://github.com/wine-staging/wine-staging
%if 0%(echo %{wine_stagingver} | grep -q \\. ; echo $?) == 0
%global strel v
%global stpkgver %{wine_stagingver}
%else
%global stpkgver %(c=%{wine_stagingver}; echo ${c:0:7})
%endif
%global ge_id a2fbe5ade7a8baf3747ca57b26680fee86fff9f0
%global ge_url https://github.com/GloriousEggroll/proton-ge-custom/raw/%{ge_id}/patches

%global tkg_id 461ec53f0762238eb31e6dbcf4b7376d6cf0987a
%global tkg_url https://github.com/Frogging-Family/wine-tkg-git/raw/%{tkg_id}/wine-tkg-git/wine-tkg-patches
%global tkg_cid 44515b99f88351e444f8b9a5ab8dce8acba4b23c
%global tkg_curl https://github.com/Frogging-Family/community-patches/raw/%{tkg_cid}/wine-tkg-git

%if 0%{?wine_staging}
%global cap_st cap_sys_nice,
%endif

%global perms_pldr %caps(cap_net_raw+eip)
%global perms_srv %caps(%{?cap_st}cap_net_raw+eip)

# childwindow (breaks nine)
%global childwindow 0
# fastsync/winesync
%global fastsync 1
# proton FS hack (wine virtual desktop with DXVK is not working well, breaks nine)
%global fshack 0
%global vulkanup 0

%if 0%{?fshack}
%global wine_staging_opts %{?wine_staging_opts} -W winex11-WM_WINDOWPOSCHANGING -W winex11-_NET_ACTIVE_WINDOW
%endif

%global whq_url  https://source.winehq.org/git/wine.git/patch
%global whq_murl  https://github.com/wine-mirror/wine
%global whqs_url  https://source.winehq.org/patches/data
%global valve_url https://github.com/ValveSoftware/wine

%global staging_banner Chinforpms Staging

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global vermajor %%(echo %%{ver} | cut -d. -f1)
%global verminor %%(echo %%{ver} | cut -d. -f2 | cut -d- -f1)

Name:           wine
# If rc, use "~" instead "-", as ~rc1
Version:        7.10
Release:        100%{?gver}%{?dist}
Summary:        A compatibility layer for windows applications

Epoch:          1

License:        LGPLv2+
URL:            http://www.winehq.org/

%if 0%{?with_snapshot}
Source0:        %{whq_murl}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
%if "%{verminor}" == "0"
%global verx 1
%endif
Source0:        https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz
Source10:       https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz.sign
%endif

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source6:        wine-README-chinforpms
Source7:        wine-README-chinforpms-fshack
Source8:        wine-README-chinforpms-fastsync

Source50:       https://raw.githubusercontent.com/KhronosGroup/Vulkan-Docs/v%{winevulkan}/xml/vk.xml#/vk-%{winevulkan}.xml

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

# mfplat things, again (remove when AAC support is added)
Patch210:       %{whq_url}/f51b2ca8f7640dd0770a82c1e2c19caa65286eef#/%{name}-whq-revert-mfplat-f51b2ca.patch
Patch211:       %{whq_url}/4d929972c341bff2da3616606b8cbeadf85dba26#/%{name}-whq-revert-mfplat-4d92997.patch
Patch212:       %{whq_url}/34a55c7b96c97b178ea1ab519eb0e847096f2076#/%{name}-whq-revert-mfplat-34a55c7.patch
Patch213:       %{whq_url}/d84d9054f5466212e122fac70265eae841438764#/%{name}-whq-revert-mfplat-d84d905.patch
Patch214:       %{whq_url}/0052ffbfa0e7672278b3d5fcdb767d604fa0f565#/%{name}-whq-revert-mfplat-0052ffb.patch
Patch215:       %{whq_url}/4dd187b2227767524825e51eddd14f206ffd03dd#/%{name}-whq-revert-mfplat-4dd187b.patch
Patch216:       %{whq_url}/7da1828c4927faec011d1c15d2f3f9bbb43435b7#/%{name}-whq-revert-mfplat-7da1828.patch
Patch217:       %{whq_url}/5144b27661fcd6705353d832e0383085f8afe842#/%{name}-whq-revert-mfplat-5144b27.patch
Patch218:       %{whq_url}/28c9c138d2658a4c3252a94d45a1e8b7ac28be7f#/%{name}-whq-revert-mfplat-28c9c13.patch
Patch219:       %{whq_url}/0c59cfc14e33a5706c1873151780d5b2dcc536ca#/%{name}-whq-revert-mfplat-0c59cfc.patch
Patch220:       %{whq_url}/a4be9e85687f7a8d7476ee3d3ced80eeec720f57#/%{name}-whq-revert-mfplat-a4be9e8.patch
Patch221:       %{whq_url}/d2f653a854ccd17688813d6b7f585acbfb45b9ba#/%{name}-whq-revert-mfplat-d2f653a.patch
Patch222:       %{whq_url}/aa867c6cfba48a63179088ec6381c73488853659#/%{name}-whq-revert-mfplat-aa867c6.patch
Patch223:       %{whq_url}/9196fee58349558593fd7edf4768b189c25f6293#/%{name}-whq-revert-mfplat-9196fee.patch
Patch224:       %{whq_url}/227a1275b14a2ffd71a4d0c621cb655e3576ad02#/%{name}-whq-revert-mfplat-227a127.patch
Patch225:       %{whq_url}/506963aaea8e3c6e4820884b3308da27f435e580#/%{name}-whq-revert-mfplat-506963a.patch
Patch226:       %{name}-revert-mfplat-446bb1e.patch
Patch227:       %{whq_url}/6a7428a0fae887cecf2e97b9cab9de9cf7811446#/%{name}-whq-revert-mfplat-6a7428a.patch
Patch228:       %{name}-revert-mfplat-7a4aafd.patch
Patch229:       %{whq_url}/6860e9ab29f4fbcfe35cb0519cfe94b94f54a36f#/%{name}-whq-revert-mfplat-6860e9a.patch
Patch230:       %{name}-revert-mfplat-24e5467.patch
Patch231:       %{whq_url}/6834fc5c9dd11026261aaa723d9df29d373ebdf5#/%{name}-whq-revert-mfplat-6834fc5.patch
Patch232:       %{whq_url}/2d7c37da495cc25d14f5b2761a5d7e2a2111320a#/%{name}-whq-revert-mfplat-2d7c37d.patch
Patch233:       %{whq_url}/dfce20f34322e4d4087edf0e5f065ae7a2493151#/%{name}-whq-revert-mfplat-dfce20f.patch
Patch234:       %{whq_url}/648ea45b810f54e5da69a239a4198c3f48b4c7e2#/%{name}-whq-revert-mfplat-648ea45.patch
Patch235:       %{whq_url}/3dd1aefc682adff082d2ae267a230f684dc1e9c4#/%{name}-whq-revert-mfplat-3dd1aef.patch
Patch236:       %{whq_url}/f71c51cb19fd694ad9e169ecc37767a93bbe40aa#/%{name}-whq-revert-mfplat-f71c51c.patch
Patch237:       %{whq_url}/651e4002ceeb9a15b11a184b5f47a732e26b7e00#/%{name}-whq-revert-mfplat-651e400.patch
Patch238:       %{whq_url}/e4258d529342cc1dc486a136d0f715520b3dd5da#/%{name}-whq-revert-mfplat-e4258d5.patch
Patch239:       %{whq_url}/aca4537c8645c991745f85ef883b97f84e4ba5cc#/%{name}-whq-revert-mfplat-aca4537.patch
Patch240:       %{whq_url}/962b4325e5b9e97c1594e2ea03cb44659367912b#/%{name}-whq-revert-mfplat-962b432.patch
Patch241:       %{whq_url}/606505e5643d8df2a23a2cc074fa9b6b2ae8b05f#/%{name}-whq-revert-mfplat-606505e.patch
Patch242:       %{whq_url}/f38369416f6487013bf197d70420bd9feef7e485#/%{name}-whq-revert-mfplat-f383694.patch
Patch243:       %{whq_url}/edef14126cbdb64dda218688a51b6e170cb4909b#/%{name}-whq-revert-mfplat-edef141.patch
Patch244:       %{name}-revert-mfplat-7735b48.patch
Patch245:       %{whq_url}/b5d6c5992092fd0c96deacbe892668aba6759f93#/%{name}-whq-revert-mfplat-b5d6c59.patch
Patch246:       %{whq_url}/55282e0d0988b66809ddb58b9f3b7449f8284fc1#/%{name}-whq-revert-mfplat-55282e0.patch
Patch247:       %{whq_url}/ebd2b7d7049e46b37caad7b0235064d1a7ec3104#/%{name}-whq-revert-mfplat-ebd2b7d.patch
Patch248:       %{whq_url}/db41b2ae238da4a8f73060948e94b8bdc64f64bb#/%{name}-whq-revert-mfplat-db41b2a.patch
Patch249:       %{whq_url}/5861379d6df87562753322e251261868943e91ca#/%{name}-whq-revert-mfplat-5861379.patch
Patch250:       %{whq_url}/bcd39c5061768d6d9a822cb8f8effa715ca62972#/%{name}-whq-revert-mfplat-bcd39c5.patch
Patch251:       %{whq_url}/3827f0487db5ad12f1beb7aabb4e6bbc278a8145#/%{name}-whq-revert-mfplat-3827f04.patch
Patch252:       %{whq_url}/bffe90496c904a0f95242e1bbfd3709fb1ff5e5d#/%{name}-whq-revert-mfplat-bffe904.patch
Patch253:       %{whq_url}/3b83fe637e8b1f0e0cbac1d53106718f56b6afdc#/%{name}-whq-revert-mfplat-3b83fe6.patch
Patch254:       %{whq_url}/38b98c653680cd87ecd3060601a57f996c35272e#/%{name}-whq-revert-mfplat-38b98c6.patch
Patch255:       %{whq_url}/8091f3a0b8463d41049ed4ade98c79f82c86ebbc#/%{name}-whq-revert-mfplat-8091f3a.patch
Patch256:       %{whq_url}/90dc7f5b944192da4b7e2f4a3d5e687fe0c9cdd2#/%{name}-whq-revert-mfplat-90dc7f5.patch
Patch257:       %{whq_url}/ed2c300d02acefa2aedd4333ff4a982137c1d4fe#/%{name}-whq-revert-mfplat-ed2c300.patch
Patch258:       %{whq_url}/6f1b3cf975965e1383e5f5c802cebdc0f4956c2a#/%{name}-whq-revert-mfplat-6f1b3cf.patch
Patch259:       %{whq_url}/ce9a42e8bda50fd5eb91c8dee78f310881d2c7e5#/%{name}-whq-revert-mfplat-ce9a42e.patch
Patch260:       %{whq_url}/86e0a2489a7e82bff3eb751094661270a40a2167#/%{name}-whq-revert-mfplat-86e0a24.patch
Patch261:       %{whq_url}/d7c4fa0d5724b7a89f5b80970e8f62efcc457f8c#/%{name}-whq-revert-mfplat-d7c4fa0.patch
Patch262:       %{whq_url}/b52a48b97ecbb8f7aff187a7743647dfab0670ea#/%{name}-whq-revert-mfplat-b52a48b.patch
Patch263:       %{whq_url}/3f1036b61b59e3a99ea6bf1f1d6984a878df6d7b#/%{name}-whq-revert-mfplat-3f1036b.patch
Patch264:       %{whq_url}/a7c60623158b048244701f104ca4daeb739637a4#/%{name}-whq-revert-mfplat-a7c6062.patch
Patch265:       %{whq_url}/e7a3cf7baf41419263ee24690501734602bf1c25#/%{name}-whq-revert-mfplat-e7a3cf7.patch
Patch266:       %{whq_url}/4455f0c3546a07ee2069cda8df50ca9f271070e6#/%{name}-whq-revert-mfplat-4455f0c.patch
Patch267:       %{whq_url}/9cc016ecb925d41f3835c07a02e23a5776a77517#/%{name}-whq-revert-mfplat-9cc016e.patch
Patch268:       %{whq_url}/8c5207f6a7232c20ad12a0d3171185442faa1295#/%{name}-whq-revert-mfplat-8c5207f.patch
Patch269:       %{whq_url}/3aaa953bd6f71c77a3d3ec34ab0f5155f67346db#/%{name}-whq-revert-mfplat-3aaa953.patch
Patch270:       %{whq_url}/2298f04a1d40a008a843ac4b0573d1a3234d5f82#/%{name}-whq-revert-mfplat-2298f04.patch
Patch271:       %{whq_url}/a7a90de929f3a37507a3f4d4231c778f79e5fa94#/%{name}-whq-revert-mfplat-a7a90de.patch
Patch272:       %{whq_url}/64b96eec7d0aea470f897a3ed0ac9e1b3a680cc5#/%{name}-whq-revert-mfplat-64b96ee.patch
Patch273:       %{whq_url}/ab1203999211209da4e737d9fc71581bea9a6bd1#/%{name}-whq-revert-mfplat-ab12039.patch
Patch274:       %{name}-revert-mfplat-77c25c8.patch
Patch275:       %{whq_url}/6e2ac3b6172dca128c83f21e10a89f4477025da0#/%{name}-whq-revert-mfplat-6e2ac3b.patch
Patch276:       %{name}-revert-mfplat-29c67fb.patch
Patch277:       %{whq_url}/1e3ae78a693f3ecb01012b19d06f76da16ee37d2#/%{name}-whq-revert-mfplat-1e3ae78.patch
Patch278:       %{whq_url}/f46618e386dedfae2a95f48cb97a14c86cd2565b#/%{name}-whq-revert-mfplat-f46618e.patch
Patch279:       %{whq_url}/7d28e8ec89254ba0fd4e7612c71f5479e82f9d2a#/%{name}-whq-revert-mfplat-7d28e8e.patch
Patch280:       %{whq_url}/562d8c338dd975706a7611a1a899ab4a8a3a2911#/%{name}-whq-revert-mfplat-562d8c3.patch
Patch281:       %{whq_url}/aacf6bcd0f0cb619906f4199d65a70eaf57ec5a8#/%{name}-whq-revert-mfplat-aacf6bc.patch
Patch282:       %{whq_url}/7c20724b0d29cee02010a3114575315b9fc9d439#/%{name}-whq-revert-mfplat-7c20724.patch
Patch283:       %{whq_url}/1933981760f50e86e91d15baeedd64bbdb5f2109#/%{name}-whq-revert-mfplat-1933981.patch
Patch284:       %{whq_url}/f91f4348356285ede39915f0d10ffae11c4871e5#/%{name}-whq-revert-mfplat-f91f434.patch
Patch285:       %{whq_url}/a4201aa6dec755ec824a0e8bb301ce2154e54ec5#/%{name}-whq-revert-mfplat-a4201aa.patch
Patch286:       %{whq_url}/2cfcdc64625e36edca686d0e9249b38605bb7ede#/%{name}-whq-revert-mfplat-2cfcdc6.patch
Patch287:       %{whq_url}/b1807751219e256867eaac5cc4d8b97a5482978f#/%{name}-whq-revert-mfplat-b180775.patch
Patch288:       %{whq_url}/86bd6924568d47ac9446f3a04859a8960c5d3894#/%{name}-whq-revert-mfplat-86bd692.patch
Patch289:       %{whq_url}/6f49156bbc763179feac35074f61a683ff4c5a7b#/%{name}-whq-revert-mfplat-6f49156.patch
Patch290:       %{name}-revert-mfplat-e21fe9e.patch
Patch291:       %{whq_url}/1a2cc84686b728af8836849cee2237e1390d1311#/%{name}-whq-revert-mfplat-1a2cc84.patch
Patch292:       %{name}-revert-mfplat-573deb1.patch
Patch293:       %{whq_url}/d90627784455bd77addd21e774b816162db2ef12#/%{name}-whq-revert-mfplat-d906277.patch
Patch294:       %{whq_url}/7144bf27b9d1cffb22ab22782114ff2e5057cc20#/%{name}-whq-revert-mfplat-7144bf2.patch
Patch295:       %{whq_url}/915d88e5e60aa08b377eca5c5cbeed6a3d2d4af5#/%{name}-whq-revert-mfplat-915d88e.patch
Patch296:       %{whq_url}/0d956959fa61b770881c1545804fabd7e26edd90#/%{name}-whq-revert-mfplat-0d95695.patch
Patch297:       %{whq_url}/0250e84bf17e287e15517329c01f6d0e346c0710#/%{name}-whq-revert-mfplat-0250e84.patch
Patch298:       %{whq_url}/b18b7260a2fc7543f47febc3f97021f4dd67ba54#/%{name}-whq-revert-mfplat-b18b726.patch
Patch299:       %{whq_url}/89d28156cf561afe0bc8692e611a96631af51433#/%{name}-whq-revert-mfplat-89d2815.patch
Patch300:       %{whq_url}/bf6aa078a709d5afd0c11d1a4e01eb1094c0d09e#/%{name}-whq-revert-mfplat-bf6aa07.patch
Patch301:       %{whq_url}/23fb8a6b49304a0b8ccf5a10e5bbd603691ba7bc#/%{name}-whq-revert-mfplat-23fb8a6.patch
Patch302:       %{whq_url}/6eca6ad68644639ef54706363dcbb2d62962da8f#/%{name}-whq-revert-mfplat-6eca6ad.patch
Patch303:       %{whq_url}/048e21d22e33fb8187532851dad6ce566592156b#/%{name}-whq-revert-mfplat-048e21d.patch
Patch304:       %{whq_url}/1d7d3f58d6666e2a5793a79ea8a28476f961e9c2#/%{name}-whq-revert-mfplat-1d7d3f5.patch
Patch305:       %{whq_url}/ce71f5a05f226b3f68328d4632cd78ac9440d073#/%{name}-whq-revert-mfplat-ce71f5a.patch
Patch306:       %{whq_url}/d686663d22cb027fae7607acf3bae96ab34018f5#/%{name}-whq-revert-mfplat-d686663.patch
Patch307:       %{whq_url}/ca10760d2e7ea4f8718741592fd639f589247e53#/%{name}-whq-revert-mfplat-ca10760.patch
Patch308:       %{whq_url}/529efbb4c91365f2f555b3c09ffda946f3843f5d#/%{name}-whq-revert-mfplat-529efbb.patch
Patch309:       %{whq_url}/fc2128d7fcd869b238932d50f034b8ff3e8be65c#/%{name}-whq-revert-mfplat-fc2128d.patch
Patch310:       %{whq_url}/bd527c1946cc92dfeee072542815e71b2e3d1861#/%{name}-whq-revert-mfplat-bd527c1.patch
Patch311:       %{whq_url}/b7fa00be65363132f1fd8686bfa0a81b394c0dba#/%{name}-whq-revert-mfplat-b7fa00b.patch
Patch312:       %{whq_url}/bae7ac48bce5e0566b30a8dd3a766b343b5617a7#/%{name}-whq-revert-mfplat-bae7ac4.patch
Patch313:       %{whq_url}/faf6f267aead1c2c1f59b051aa7bc12d25dc8941#/%{name}-whq-revert-mfplat-faf6f26.patch
Patch314:       %{whq_url}/5db4b0cff96dae30643613a01d13b75196a00c25#/%{name}-whq-revert-mfplat-5db4b0c.patch
Patch315:       %{whq_url}/2567ff497d40cbc43a1d5d766636b6dd77fc4618#/%{name}-whq-revert-mfplat-2567ff4.patch
Patch316:       %{whq_url}/e3f226fde01d96c5e7799884ed4da5324adceca9#/%{name}-whq-revert-mfplat-e3f226f.patch
Patch317:       %{whq_url}/68fa3f673633c138596b86ad2ed1befcd0cc63c5#/%{name}-whq-revert-mfplat-68fa3f6.patch
Patch318:       %{whq_url}/5b04d18945c547144bf692f6418af5ec25315835#/%{name}-whq-revert-mfplat-5b04d18.patch
Patch319:       %{whq_url}/f14018f7edecdff5784ee98e10f1defa6ee75040#/%{name}-whq-revert-mfplat-f14018f.patch
Patch320:       %{whq_url}/5387718c6fbd36b7a6309122f4af68d475a344e8#/%{name}-whq-revert-mfplat-5387718.patch
Patch321:       %{whq_url}/4c999efdfb6df56e48deec14444442415d8d1ae2#/%{name}-whq-revert-mfplat-4c999ef.patch
Patch322:       %{whq_url}/411ef13e7c2bbc43afcfc8fe1a1e251b79a059be#/%{name}-whq-revert-mfplat-411ef13.patch
Patch323:       %{whq_url}/0c2f1121cc8caa5815ea48ccbe7f891f6891f39e#/%{name}-whq-revert-mfplat-0c2f112.patch
Patch324:       %{whq_url}/0416d2f167dc852fca9a41ecf398b32409665657#/%{name}-whq-revert-mfplat-0416d2f.patch
Patch325:       %{whq_url}/50c20cf8cf7b9fb5caee39f55e339c0ff4a2c0d1#/%{name}-whq-revert-mfplat-50c20cf.patch
Patch326:       %{whq_url}/32a72b3e78b6e258eba4a325d3d750f5311921c9#/%{name}-whq-revert-mfplat-32a72b3.patch
Patch327:       %{whq_url}/16d93a32e3dcf5013dce8d6f2fbade8c8c0a4c53#/%{name}-whq-revert-mfplat-16d93a3.patch
Patch328:       %{whq_url}/ea81a48259804c2ed0aa74d98e1362e5ad7f76ef#/%{name}-whq-revert-mfplat-ea81a48.patch
Patch329:       %{name}-revert-mfplat-031747a.patch
Patch330:       %{whq_url}/71b136384b208e85be362d523cc4cc7be9aff202#/%{name}-whq-revert-mfplat-71b1363.patch
Patch331:       %{whq_url}/fb0f6b4be46032e2e38a804822eaccb772e5d9bb#/%{name}-whq-revert-mfplat-fb0f6b4.patch
Patch332:       %{whq_url}/bee6d2049e2f2c3b87ab5bcc5458ff900ec42850#/%{name}-whq-revert-mfplat-bee6d20.patch
Patch333:       %{whq_url}/e8bf5dcdf8cdbb365e9ca8703debdc2ae5f98279#/%{name}-whq-revert-mfplat-e8bf5dc.patch
Patch334:       %{whq_url}/c39dbe1f31435e715cd10bdf83be864e00346699#/%{name}-whq-revert-mfplat-c39dbe1.patch
Patch335:       %{whq_url}/ee7958bac7a176aa250cdcc23b9bb5c009204015#/%{name}-whq-revert-mfplat-ee7958b.patch
Patch336:       %{whq_url}/21832ac226da7e31944df26bf02ff231d2a1a941#/%{name}-whq-revert-mfplat-21832ac.patch
Patch337:       %{whq_url}/0892b92b56531aa3b1c67948bf0cd06152ed361e#/%{name}-whq-revert-mfplat-0892b92.patch
Patch338:       %{whq_url}/2ae08f035fdb5665eab4cef6333344ace528c61e#/%{name}-whq-revert-mfplat-2ae08f0.patch
Patch339:       %{whq_url}/7adcdb6ff8c6ac321a1f21bfa4123d08c3bc52d5#/%{name}-whq-revert-mfplat-7adcdb6.patch
Patch340:       %{whq_url}/6abd8e23b8be24af194d97c2fa6bd9e9fed4b29a#/%{name}-whq-revert-mfplat-6abd8e2.patch
Patch341:       %{whq_url}/8abbc0096da3b6e836d9b7559eb31a73f113bc2f#/%{name}-whq-revert-mfplat-8abbc00.patch
Patch342:       %{whq_url}/99ce6e87a3b22c5602d7bbedd43bb40627b63321#/%{name}-whq-revert-mfplat-99ce6e8.patch
Patch343:       %{whq_url}/c4c3912bad1c67bb70fd009eee18e0a58cdfe929#/%{name}-whq-revert-mfplat-c4c3912.patch
Patch344:       %{whq_url}/f7ca5cfa27e433530f2725d44045ea5284fd332a#/%{name}-whq-revert-mfplat-f7ca5cf.patch
Patch345:       %{whq_url}/24266121f1396a3b6ef4d40a7b35a0a31931539c#/%{name}-whq-revert-mfplat-2426612.patch
Patch346:       %{whq_url}/9c711ba7488d78a91e133083567e56feb446a7c8#/%{name}-whq-revert-mfplat-9c711ba.patch
Patch347:       %{whq_url}/7a8254fd05a2c7c89783d65cba544f2899611c73#/%{name}-whq-revert-mfplat-7a8254f.patch

# wine staging patches for wine-staging
Source900:       %{wine_stg_url}/archive/%{?strel}%{wine_stagingver}/wine-staging-%{stpkgver}.tar.gz

Patch900:        0001-staging-restore-mfplat-streaming-patchset.patch
Patch901:        0001-Fix-staging-windows.networking.connectivity.dll.patch

# https://github.com/Tk-Glitch/PKGBUILDS/wine-tkg-git/wine-tkg-patches
Patch1000:       %{tkg_url}/proton/use_clock_monotonic/use_clock_monotonic.patch#/%{name}-tkg-use_clock_monotonic.patch
Patch1002:       %{tkg_url}/proton/valve_proton_fullscreen_hack/FS_bypass_compositor.patch#/%{name}-tkg-FS_bypass_compositor.patch
Patch1003:       %{tkg_url}/misc/childwindow/childwindow-proton.patch#/%{name}-tkg-childwindow-proton.patch
Patch1004:       %{tkg_url}/misc/steam/steam.patch#/%{name}-tkg-steam.patch
Patch1005:       %{tkg_url}/misc/CSMT-toggle/CSMT-toggle.patch#/%{name}-tkg-CSMT-toggle.patch
Patch1006:       %{tkg_url}/hotfixes/syscall_emu/protonify_stg_syscall_emu-009.mystagingpatch#/%{name}-tkg-protonify_stg_syscall_emu-009.patch
Patch1007:       %{tkg_url}/hotfixes/08cccb5/a608ef1.mypatch#/%{name}-tkg-a608ef1.patch

# fsync
Patch1020:       %{tkg_url}/proton/fsync/fsync-unix-staging.patch#/%{name}-tkg-fsync-unix-staging.patch
Patch1021:       %{tkg_url}/proton/fsync/server_Abort_waiting_on_a_completion_port_when_closing_it.patch#/%{name}-tkg-server_Abort_waiting_on_a_completion_port_when_closing_it.patch
Patch1022:       %{tkg_url}/proton/fsync/fsync_futex_waitv.patch#/%{name}-tkg-fsync_futex_waitv.patch
# FS Hack
Patch1023:       %{tkg_url}/proton/valve_proton_fullscreen_hack/valve_proton_fullscreen_hack-staging.patch#/%{name}-tkg-valve_proton_fullscreen_hack-staging.patch
Patch1024:       %{tkg_url}/proton/LAA/LAA-unix-staging.patch#/%{name}-tkg-LAA-unix-staging.patch
Patch1025:       %{tkg_url}/proton-tkg-specific/proton-tkg/staging/proton-tkg-staging.patch#/%{name}-tkg-proton-tkg-staging.patch
Patch1026:       %{tkg_url}/hotfixes/proton_fs_hack_staging/remove_hooks_that_time_out.mypatch#/%{name}-tkg-remove_hooks_that_time_out.patch
Patch1027:       %{tkg_url}/proton/proton-winevulkan/proton-winevulkan.patch#/%{name}-tkg-proton-winevulkan.patch
Patch1028:       %{tkg_url}/proton/proton-winevulkan/proton-winevulkan-nofshack.patch#/%{name}-tkg-proton-winevulkan-nofshack.patch
Patch1029:       %{tkg_url}/hotfixes/syscall_emu/rdr2.patch#/%{name}-tkg-rdr2.patch
Patch1031:       %{tkg_url}/proton-tkg-specific/proton-cpu-topology-overrides/proton-cpu-topology-overrides.patch#/%{name}-tkg-proton-cpu-topology-overrides.patch
Patch1032:       %{tkg_url}/proton/proton-win10-default/proton-win10-default-staging.patch#/%{name}-tkg-proton-win10-default-staging.patch
Patch1034:       %{tkg_url}/hotfixes/GetMappedFileName/Return_nt_filename_and_resolve_DOS_drive_path.mypatch#/%{name}-tkg-Return_nt_filename_and_resolve_DOS_drive_path.patch
Patch1035:       %{tkg_url}/hotfixes/rdr2/ef6e33f.mypatch#/%{name}-tkg-ef6e33f.patch
Patch1036:       %{tkg_url}/hotfixes/rdr2/0001-proton-bcrypt_rdr2_fixes4.mypatch#/%{name}-tkg-0001-proton-bcrypt_rdr2_fixes4.patch
Patch1037:       %{tkg_url}/hotfixes/rdr2/0002-bcrypt-Add-support-for-calculating-secret-ecc-keys.mypatch#/%{name}-tkg-0002-bcrypt-Add-support-for-calculating-secret-ecc-keys.patch
Patch1038:       %{tkg_url}/hotfixes/proton_fs_hack_staging/win32u.implement_rudimentary_EnableMouseInPointer_support3.mypatch#/%{name}-tkg-win32u.implement_rudimentary_EnableMouseInPointer_support3.patch
Patch1039:       %{tkg_url}/hotfixes/proton_fs_hack_staging/winex11.drv_Add_a_GPU_for_each_Vulkan_device_that_was_not_tied_to_an_XRandR_provider.mypatch#/%{name}-tkg-winex11.drv_Add_a_GPU_for_each_Vulkan_device_that_was_not_tied_to_an_XRandR_provider.patch
Patch1040:       %{tkg_url}/hotfixes/proton_fs_hack_staging/winex11.drv_Ignore_ClipCursor_if_desktop_window_is_foreground.mypatch#/%{name}-tkg-winex11.drv_Ignore_ClipCursor_if_desktop_window_is_foreground.patch

Patch1050:       %{tkg_url}/misc/fastsync/fastsync-staging-protonify.patch#/%{name}-tkg-fastsync-staging-protonify.patch
Patch1051:       %{tkg_url}/misc/fastsync/fastsync-clock_monotonic-fixup.patch#/%{name}-tkg-fastsync-clock_monotonic-fixup.patch

Patch1089:       %{tkg_curl}/0001-ntdll-Use-kernel-soft-dirty-flags-for-write-watches-.mypatch#/%{name}-tkg-0001-ntdll-Use-kernel-soft-dirty-flags-for-write-watches.patch
Patch1090:       0001-fshack-revert-grab-fullscreen.patch
Patch1091:       %{valve_url}/commit/8d5fed7770aca31075c29bd5b8306339798a8742.patch#/%{name}-valve-8d5fed7.patch
Patch1092:       %{valve_url}/commit/3b176c060227854a40333c0ec5c634a2e9d39fd4.patch#/%{name}-valve-3b176c0.patch

Patch1300:       nier.patch
Patch1301:       0001-FAudio-Disable-reverb.patch
Patch1302:       0001-proton-tkg-staging-update-to-NtUserGetDesktopWindow.patch
Patch1304:       0001-winegstreamer-remove-last-WG_PARSER_EVENT_SEGMENT.patch
Patch1305:       0001-mfplat-custom-fixes-from-proton.patch

# Patch the patch
Patch5000:      0001-chinforpms-message.patch

# END of staging patches

%if !0%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 aarch64
%else
ExclusiveArch:  %{ix86}
%endif

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
%ifarch aarch64
BuildRequires:  clang >= 5.0
BuildRequires:  lld
%else
BuildRequires:  gcc
%endif
%if 0%{?wine_mingw}
%ifarch %{ix86} x86_64
# mingw-binutils 2.35 or patched 2.34 is needed to prevent crashes
BuildRequires:  mingw32-binutils >= 2.34-100
BuildRequires:  mingw64-binutils >= 2.34-100
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
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(glut)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  fontpackages-devel
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gmp)
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
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  librsvg2
BuildRequires:  librsvg2-tools
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libv4l2)
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
BuildRequires:  pkgconfig(xfixes)
# childwindow.patch
#BuildRequires:  pkgconfig(xpresent)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xxf86dga)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  libappstream-glib

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(libva)
%if 0%{?fastsync}
BuildRequires:  winesync-devel >= %{winefastsync}
%endif
%endif

Requires:       wine-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-desktop = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
Requires:       wine-core(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
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
Recommends:     wine-dxvk(x86-32)
Recommends:     dosbox-staging
Recommends:     isdn4k-utils(x86-32)
%if 0%{?fastsync}
Recommends:     winesync >= %{winefastsync}
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
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
Recommends:     wine-dxvk(x86-64)
Recommends:     dosbox-staging
Recommends:     isdn4k-utils(x86-64)

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
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
Requires:       gmp(x86-32)
Requires:       gnutls(x86-32)
Requires:       gstreamer1-plugins-good(x86-32)
Requires:       libgcrypt(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXfixes(x86-32)
Requires:       libXi(x86-32)
Requires:       libXinerama(x86-32)
#Requires:       libXpresent(x86-32)
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
Requires:       libXxf86vm(x86-32)
Requires:       libpcap(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       samba-libs(x86-32)
Requires:       unixODBC(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
Requires:       libva(x86-32)
Recommends:     gstreamer1-plugins-ugly(x86-32)
%endif
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       nss-mdns(x86-64)
Requires:       gmp(x86-64)
Requires:       gnutls(x86-64)
Requires:       gstreamer1-plugins-good(x86-64)
Requires:       libgcrypt(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXfixes(x86-64)
Requires:       libXi(x86-64)
Requires:       libXinerama(x86-64)
#Requires:       libXpresent(x86-64)
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
Requires:       libXxf86vm(x86-64)
Requires:       libpcap(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       samba-libs(x86-64)
Requires:       unixODBC(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
Requires:       libva(x86-64)
Recommends:     gstreamer1-plugins-ugly(x86-64)
%endif
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gmp
Requires:       gnutls
Requires:       gstreamer1-plugins-good
Requires:       libgcrypt
Requires:       libXcursor
Requires:       libXfixes
#Requires:       libXpresent
Requires:       libXrender
Requires:       libpcap
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan-loader
%if 0%{?wine_staging}
Requires:       libva
Recommends:     gstreamer1-plugins-ugly
%endif
%endif

Provides:       gsm = %{winegsm}
Provides:       libFAudio = %{wineFAudio}
Provides:       libjpeg = %{winejpeg}
Provides:       lcms2 = %{winelcms2}
Provides:       mpg123 = %{winempg123}
Provides:       libpng = %{winepng}
Provides:       libtiff = %{winetiff}
Provides:       jxrlib = %{winejxrlib}
Provides:       libxml2 = %{winexml2}
Provides:       libxslt = %{winexslt}
Provides:       libvkd3d = %{winevkd3d}
Provides:       zlib = %{winezlib}

# removed as of 1.7.35
Obsoletes:      wine-wow < 1.7.35
Provides:       wine-wow = %{?epoch:%{epoch}:}%{version}-%{release}

# removed as of 6.21
Obsoletes:      wine-capi < %{?epoch:%{epoch}:}6.20-101
Provides:       wine-capi = %{?epoch:%{epoch}:}%{version}-%{release}

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
%setup -q -n %{name}-%{?gver:%{commit}}%{!?gver:%{ver}}

patch_command='patch -F%{_default_patch_fuzz} %{_default_patch_flags}'

%patch511 -p1 -b.cjk
%patch599 -p1

%patch347 -p1 -R
%patch346 -p1 -R
%patch345 -p1 -R
%patch344 -p1 -R
%patch343 -p1 -R
%patch342 -p1 -R
%patch341 -p1 -R
%patch340 -p1 -R
%patch339 -p1 -R
%patch338 -p1 -R
%patch337 -p1 -R
%patch336 -p1 -R
%patch335 -p1 -R
%patch334 -p1 -R
%patch333 -p1 -R
%patch332 -p1 -R
%patch331 -p1 -R
%patch330 -p1 -R
%patch329 -p1 -R
rm -f dlls/qasf/tests/test.wmv
rm -f dlls/qasf/tests/resource.rc
%patch328 -p1 -R
%patch327 -p1 -R
%patch326 -p1 -R
%patch325 -p1 -R
%patch324 -p1 -R
%patch323 -p1 -R
%patch322 -p1 -R
%patch321 -p1 -R
%patch320 -p1 -R
%patch319 -p1 -R
%patch318 -p1 -R
%patch317 -p1 -R
%patch316 -p1 -R
%patch315 -p1 -R
%patch314 -p1 -R
%patch313 -p1 -R
%patch312 -p1 -R
%patch311 -p1 -R
%patch310 -p1 -R
%patch309 -p1 -R
%patch308 -p1 -R
%patch307 -p1 -R
%patch306 -p1 -R
%patch305 -p1 -R
%patch304 -p1 -R
%patch303 -p1 -R
%patch302 -p1 -R
%patch301 -p1 -R
%patch300 -p1 -R
%patch299 -p1 -R
%patch298 -p1 -R
%patch297 -p1 -R
%patch296 -p1 -R
%patch295 -p1 -R
%patch294 -p1 -R
%patch293 -p1 -R
%patch292 -p1 -R
%patch291 -p1 -R
%patch290 -p1 -R
rm -f dlls/mf/tests/rgb32frame.bin
%patch289 -p1 -R
%patch288 -p1 -R
%patch287 -p1 -R
%patch286 -p1 -R
%patch285 -p1 -R
%patch284 -p1 -R
%patch283 -p1 -R
%patch282 -p1 -R
%patch281 -p1 -R
%patch280 -p1 -R
%patch279 -p1 -R
%patch278 -p1 -R
%patch277 -p1 -R
%patch276 -p1 -R
%patch275 -p1 -R
%patch274 -p1 -R
rm -f dlls/mf/tests/audiodata.bin
mv dlls/mf/tests/wmadecdata.bin dlls/mf/tests/wmadata.bin
rm -f dlls/mf/tests/wmaencdata.bin
%patch273 -p1 -R
%patch272 -p1 -R
%patch271 -p1 -R
%patch270 -p1 -R
%patch269 -p1 -R
%patch268 -p1 -R
%patch267 -p1 -R
%patch266 -p1 -R
%patch265 -p1 -R
%patch264 -p1 -R
%patch263 -p1 -R
%patch262 -p1 -R
%patch261 -p1 -R
%patch260 -p1 -R
%patch259 -p1 -R
%patch258 -p1 -R
%patch257 -p1 -R
%patch256 -p1 -R
%patch255 -p1 -R
%patch254 -p1 -R
%patch253 -p1 -R
%patch252 -p1 -R
%patch251 -p1 -R
%patch250 -p1 -R
%patch249 -p1 -R
%patch248 -p1 -R
%patch247 -p1 -R
%patch246 -p1 -R
%patch245 -p1 -R
%patch244 -p1 -R
%patch243 -p1 -R
%patch242 -p1 -R
%patch241 -p1 -R
%patch240 -p1 -R
%patch239 -p1 -R
%patch238 -p1 -R
%patch237 -p1 -R
%patch236 -p1 -R
%patch235 -p1 -R
%patch234 -p1 -R
%patch233 -p1 -R
%patch232 -p1 -R
%patch231 -p1 -R
%patch230 -p1 -R
rm -f dlls/winegstreamer/h264_decoder.c
%patch229 -p1 -R
%patch228 -p1 -R
%patch227 -p1 -R
rm -f dlls/mf/tests/nv12frame.bin
%patch226 -p1 -R
%patch225 -p1 -R
%patch224 -p1 -R
%patch223 -p1 -R
%patch222 -p1 -R
%patch221 -p1 -R
%patch220 -p1 -R
%patch219 -p1 -R
%patch218 -p1 -R
%patch217 -p1 -R
%patch216 -p1 -R
%patch215 -p1 -R
%patch214 -p1 -R
%patch213 -p1 -R
%patch212 -p1 -R
%patch211 -p1 -R
%patch210 -p1 -R

# setup and apply wine-staging patches
%if 0%{?wine_staging}

gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

%patch900 -p1
%patch901 -p1

%patch1006 -p1
%patch1000 -p1
%if !0%{?fshack}
%patch1002 -p1
%if 0%{?childwindow}
%patch1003 -p1
%endif
%endif
%patch1004 -p1
%patch1005 -p1
%patch1007 -p1

%patch5000 -p1

sed -e 's|autoreconf -f|true|g' -i ./patches/patchinstall.sh
./patches/patchinstall.sh DESTDIR="`pwd`" --all %{?wine_staging_opts}

%patch1020 -p1
%patch1021 -p1
%patch1022 -p1
%if 0%{?fshack}
%patch1023 -p1
%endif
%patch1024 -p1
%patch1025 -p1
%patch1026 -p1
%patch1038 -p1
%if 0%{?childwindow}
%patch1039 -p1
%endif
%patch1040 -p1
%if 0%{?fshack}
%if 0%{?vulkanup}
%patch1027 -p1
%endif
%patch1090 -p1
%else
%if 0%{?vulkanup}
%patch1028 -p1
%endif
%endif
%patch1029 -p1
%patch1031 -p1
%if 0%{?fastsync}
%patch1050 -p1
%patch1051 -p1
%endif
%patch1032 -p1
%dnl #FIXME breaks something %patch1034 -p1
%dnl #FIXME needs rebase %patch1035 -p1
%dnl #FIXME needs rebase %patch1036 -p1
%dnl #FIXME needs rebase %patch1037 -p1

%patch1089 -p1
%patch1091 -p1 -R
%patch1092 -p1

%patch1300 -p1
%patch1301 -p1
%patch1302 -p1
%patch1304 -p1
%patch1305 -p1

sed \
  -e "s/ (Staging)/ (%{staging_banner})/g" \
  -i configure*

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

WINEVULKAN_VER="$(grep '^VK_XML_VERSION' dlls/winevulkan/make_vulkan | awk '{print $3}' | tr -d \")"
if [ "${WINEVULKAN_VER}" != "%{winevulkan}" ] ;then
  echo "winevulkan version mismatch. Edit %%global winevulkan to ${WINEVULKAN_VER}."
  exit 1
fi

cp -p %{SOURCE3} README.FEDORA
cp -p %{SOURCE6} README.chinforpms
%if 0%{?fshack}
cat README.chinforpms %{SOURCE7} >> README.chinforpms.fshack
touch -r README.chinforpms README.chinforpms.fshack
mv -f README.chinforpms.fshack README.chinforpms
%endif
%if 0%{?fastsync}
cat README.chinforpms %{SOURCE8} >> README.chinforpms.fastsync
touch -r README.chinforpms README.chinforpms.fastsync
mv -f README.chinforpms.fastsync README.chinforpms
%endif

cp -p %{SOURCE502} README.tahoma

sed -e '/winemenubuilder\.exe/s|-a ||g' -i loader/wine.inf.in

cp -p %{SOURCE50} ./dlls/winevulkan/vk-%{winevulkan}.xml

./dlls/winevulkan/make_vulkan
./tools/make_requests
./tools/make_specfiles
autoreconf -f


%build
# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo %{build_cflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

export CFLAGS="$CFLAGS -ftree-vectorize -mno-avx -mno-avx2"

%ifarch aarch64
%global toolchain clang
%endif

# Remove this flags by upstream recommendation (see configure.ac)
export CFLAGS="`echo $CFLAGS | sed \
  -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//' \
  -e 's/-fstack-protector-strong//' \
  -e 's/-fstack-clash-protection//' \
  -e 's/-fcf-protection//' \
  `"

export LDFLAGS="-Wl,-O1,--sort-common %{build_ldflags}"

# https://bugs.winehq.org/show_bug.cgi?id=43530
export LDFLAGS="`echo $LDFLAGS | sed \
  -e 's/-Wl,-z,now//' \
  -e 's/-Wl,-z,relro//' \
  `"

%if 0%{?wine_mingw}
# mingw compiler do not support plugins and some flags are crashing it
export CROSSCFLAGS="`echo $CFLAGS | sed \
  -e 's/-grecord-gcc-switches//' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-cc1,,' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,' \
  -e 's/-fasynchronous-unwind-tables//' \
  `"

# mingw linker do not support -z,relro and now
export CROSSLDFLAGS="`echo $LDFLAGS | sed \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-ld,,' \
  -e 's,-Wl,--build-id=sha1,,' \
  `"

mkdir bin
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

# required so that both Linux and Windows development files can be found
unset PKG_CONFIG_PATH 

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --with-dbus \
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
%endif
 --disable-tests \
 --without-oss \
%{nil}

%make_build TARGETFLAGS="" depend
%make_build TARGETFLAGS=""

%install
%if 0%{?wine_mingw}
export PATH="$(pwd)/bin:$PATH"
%endif

%make_install \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
# do not ship typelibs in 32-bit packages
# https://www.winehq.org/pipermail/wine-devel/2020-June/167283.html
rm -f %{buildroot}%{_includedir}/wine/windows/*.tlb 
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
echo "%{_libdir}/wine/%{winesodir}" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/wine-%{_arch}.conf

# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s \
  $(realpath -m --relative-to=%{_fontconfig_confdir} %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf) \
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
%doc README.FEDORA
%doc README.chinforpms
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%if 0%{?wine_staging}
%doc README.esync
%endif
%{_bindir}/msidb
%{_bindir}/winedump
%{_libdir}/wine/%{winedlldir}/explorer.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cabarc.%{wineexe}
%{_libdir}/wine/%{winedlldir}/control.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cmd.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dxdiag.%{wineexe}
%{_libdir}/wine/%{winedlldir}/notepad.%{wineexe}
%{_libdir}/wine/%{winedlldir}/plugplay.%{wineexe}
%{_libdir}/wine/%{winedlldir}/progman.%{wineexe}
%{_libdir}/wine/%{winedlldir}/taskmgr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winedbg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winefile.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winemine.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winemsibuilder.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winepath.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winmgmt.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winver.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wordpad.%{wineexe}
%{_libdir}/wine/%{winedlldir}/write.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wusa.%{wineexe}

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%ifnarch %{arm}
%{perms_pldr} %{_bindir}/wine32-preloader
%endif
%{perms_srv} %{_bindir}/wineserver32
%config %{_sysconfdir}/ld.so.conf.d/wine-%{_arch}.conf
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{perms_srv} %{_bindir}/wineserver64
%config %{_sysconfdir}/ld.so.conf.d/wine-%{_arch}.conf
%endif
%ifarch x86_64 aarch64
%{perms_pldr} %{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ifnarch %{arm}
%ghost %{_bindir}/wine-preloader
%endif
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine
%dir %{_libdir}/wine/%{winearchdir}
%dir %{_libdir}/wine/%{winesodir}
%if !0%{?wine_mingw}
%{_libdir}/wine/%{winearchdir}/*
%endif

%{_libdir}/wine/%{winedlldir}/attrib.%{wineexe}
%{_libdir}/wine/%{winedlldir}/arp.%{wineexe}
%{_libdir}/wine/%{winedlldir}/aspnet_regiis.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cacls.%{wineexe}
%{_libdir}/wine/%{winedlldir}/conhost.%{wineexe}
%{_libdir}/wine/%{winedlldir}/cscript.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dism.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dllhost.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dpnsvr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/eject.%{wineexe}
%{_libdir}/wine/%{winedlldir}/expand.%{wineexe}
%{_libdir}/wine/%{winedlldir}/extrac32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/fc.%{wineexe}
%{_libdir}/wine/%{winedlldir}/find.%{wineexe}
%{_libdir}/wine/%{winedlldir}/findstr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/fsutil.%{wineexe}
%{_libdir}/wine/%{winedlldir}/hostname.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ipconfig.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winhlp32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/mshta.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winedlldir}/msidb.%{wineexe}
%endif
%{_libdir}/wine/%{winedlldir}/msiexec.%{wineexe}
%{_libdir}/wine/%{winedlldir}/net.%{wineexe}
%{_libdir}/wine/%{winedlldir}/netstat.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ngen.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ntoskrnl.%{wineexe}
%{_libdir}/wine/%{winedlldir}/oleview.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ping.%{wineexe}
%{_libdir}/wine/%{winedlldir}/powershell.%{wineexe}
%{_libdir}/wine/%{winedlldir}/reg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regasm.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regedit.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regini.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regsvcs.%{wineexe}
%{_libdir}/wine/%{winedlldir}/regsvr32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/rpcss.%{wineexe}
%{_libdir}/wine/%{winedlldir}/rundll32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/schtasks.%{wineexe}
%{_libdir}/wine/%{winedlldir}/sdbinst.%{wineexe}
%{_libdir}/wine/%{winedlldir}/secedit.%{wineexe}
%{_libdir}/wine/%{winedlldir}/servicemodelreg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/services.%{wineexe}
%{_libdir}/wine/%{winedlldir}/start.%{wineexe}
%{_libdir}/wine/%{winedlldir}/tasklist.%{wineexe}
%{_libdir}/wine/%{winedlldir}/termsv.%{wineexe}
%{_libdir}/wine/%{winedlldir}/view.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wevtutil.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wineboot.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winebrowser.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wineconsole.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winecfg.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winemenubuilder.%{wineexe}
%{_libdir}/wine/%{winedlldir}/winedevice.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wmplayer.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wscript.%{wineexe}
%{_libdir}/wine/%{winedlldir}/uninstaller.%{wineexe}

%{_libdir}/wine/%{winesodir}/libwine.so.1*

%{_libdir}/wine/%{winedlldir}/acledit.%{winedll}
%{_libdir}/wine/%{winedlldir}/aclui.%{winedll}
%{_libdir}/wine/%{winedlldir}/activeds.%{winedll}
%{_libdir}/wine/%{winedlldir}/activeds.%{winetlb}
%{_libdir}/wine/%{winedlldir}/actxprxy.%{winedll}
%{_libdir}/wine/%{winedlldir}/adsldp.%{winedll}
%{_libdir}/wine/%{winedlldir}/adsldpc.%{winedll}
%{_libdir}/wine/%{winedlldir}/advapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/advpack.%{winedll}
%{_libdir}/wine/%{winedlldir}/amsi.%{winedll}
%{_libdir}/wine/%{winedlldir}/amstream.%{winedll}
%{_libdir}/wine/%{winedlldir}/apisetschema.%{winedll}
%{_libdir}/wine/%{winedlldir}/apphelp.%{winedll}
%{_libdir}/wine/%{winedlldir}/appwiz.%{winecpl}
%{_libdir}/wine/%{winedlldir}/atl.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl80.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl90.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl100.%{winedll}
%{_libdir}/wine/%{winedlldir}/atl110.%{winedll}
%{_libdir}/wine/%{winedlldir}/atlthunk.%{winedll}
%{_libdir}/wine/%{winedlldir}/atmlib.%{winedll}
%{_libdir}/wine/%{winedlldir}/authz.%{winedll}
%{_libdir}/wine/%{winesodir}/avicap32.so
%{_libdir}/wine/%{winedlldir}/avicap32.%{winedll}
%{_libdir}/wine/%{winedlldir}/avifil32.%{winedll}
%{_libdir}/wine/%{winedlldir}/avrt.%{winedll}
%{_libdir}/wine/%{winesodir}/bcrypt.so
%{_libdir}/wine/%{winedlldir}/bcrypt.%{winedll}
%{_libdir}/wine/%{winedlldir}/bluetoothapis.%{winedll}
%{_libdir}/wine/%{winedlldir}/browseui.%{winedll}
%{_libdir}/wine/%{winedlldir}/bthprops.%{winecpl}
%{_libdir}/wine/%{winedlldir}/cabinet.%{winedll}
%{_libdir}/wine/%{winedlldir}/cards.%{winedll}
%{_libdir}/wine/%{winedlldir}/cdosys.%{winedll}
%{_libdir}/wine/%{winedlldir}/cfgmgr32.%{winedll}
%{_libdir}/wine/%{winedlldir}/chcp.%{winecom}
%{_libdir}/wine/%{winedlldir}/clock.%{wineexe}
%{_libdir}/wine/%{winedlldir}/clusapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/cng.%{winesys}
%{_libdir}/wine/%{winedlldir}/combase.%{winedll}
%{_libdir}/wine/%{winedlldir}/comcat.%{winedll}
%{_libdir}/wine/%{winedlldir}/comctl32.%{winedll}
%{_libdir}/wine/%{winedlldir}/comdlg32.%{winedll}
%{_libdir}/wine/%{winedlldir}/compstui.%{winedll}
%{_libdir}/wine/%{winedlldir}/comsvcs.%{winedll}
%{_libdir}/wine/%{winedlldir}/concrt140.%{winedll}
%{_libdir}/wine/%{winedlldir}/connect.%{winedll}
%{_libdir}/wine/%{winedlldir}/credui.%{winedll}
%{_libdir}/wine/%{winedlldir}/crtdll.%{winedll}
%{_libdir}/wine/%{winesodir}/crypt32.so
%{_libdir}/wine/%{winedlldir}/crypt32.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptdlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptdll.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptext.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptnet.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptsp.%{winedll}
%{_libdir}/wine/%{winedlldir}/cryptui.%{winedll}
%{_libdir}/wine/%{winesodir}/ctapi32.so
%{_libdir}/wine/%{winedlldir}/ctapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/ctl3d32.%{winedll}
%{_libdir}/wine/%{winedlldir}/d2d1.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d10.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d10_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d10core.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d11.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d12.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dcompiler_*.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dim.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dim700.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3drm.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx9_*.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx10_*.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx11_42.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dx11_43.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3dxof.%{winedll}
%{_libdir}/wine/%{winedlldir}/davclnt.%{winedll}
%{_libdir}/wine/%{winedlldir}/dbgeng.%{winedll}
%{_libdir}/wine/%{winedlldir}/dbghelp.%{winedll}
%{_libdir}/wine/%{winedlldir}/dciman32.%{winedll}
%{_libdir}/wine/%{winedlldir}/dcomp.%{winedll}
%{_libdir}/wine/%{winedlldir}/ddraw.%{winedll}
%{_libdir}/wine/%{winedlldir}/ddrawex.%{winedll}
%{_libdir}/wine/%{winedlldir}/devenum.%{winedll}
%{_libdir}/wine/%{winedlldir}/dhcpcsvc.%{winedll}
%{_libdir}/wine/%{winedlldir}/dhcpcsvc6.%{winedll}
%{_libdir}/wine/%{winedlldir}/dhtmled.%{wineocx}
%{_libdir}/wine/%{winedlldir}/diasymreader.%{winedll}
%{_libdir}/wine/%{winedlldir}/difxapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/dinput.%{winedll}
%{_libdir}/wine/%{winedlldir}/dinput8.%{winedll}
%{_libdir}/wine/%{winedlldir}/directmanipulation.%{winedll}
%{_libdir}/wine/%{winedlldir}/dispex.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmband.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmcompos.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmime.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmloader.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmscript.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmstyle.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmsynth.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmusic.%{winedll}
%{_libdir}/wine/%{winedlldir}/dmusic32.%{winedll}
%{_libdir}/wine/%{winedlldir}/dotnetfx35.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dplay.%{winedll}
%{_libdir}/wine/%{winedlldir}/dplaysvr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dplayx.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnaddr.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnet.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnhpast.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnhupnp.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpnlobby.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpvoice.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpwsockx.%{winedll}
%{_libdir}/wine/%{winedlldir}/drmclien.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsdmo.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsound.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsquery.%{winedll}
%{_libdir}/wine/%{winedlldir}/dssenh.%{winedll}
%{_libdir}/wine/%{winedlldir}/dswave.%{winedll}
%{_libdir}/wine/%{winedlldir}/dsuiext.%{winedll}
%{_libdir}/wine/%{winedlldir}/dpvsetup.%{wineexe}
%{_libdir}/wine/%{winedlldir}/dwmapi.%{winedll}
%{_libdir}/wine/%{winesodir}/dwrite.so
%{_libdir}/wine/%{winedlldir}/dwrite.%{winedll}
%{_libdir}/wine/%{winedlldir}/dx8vb.%{winedll}
%{_libdir}/wine/%{winedlldir}/dxdiagn.%{winedll}
%{_libdir}/wine/%{winedlldir}/dxgi.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winedlldir}/dxgkrnl.%{winesys}
%{_libdir}/wine/%{winedlldir}/dxgmms1.%{winesys}
%endif
%{_libdir}/wine/%{winedlldir}/dxtrans.%{winedll}
%{_libdir}/wine/%{winedlldir}/dxva2.%{winedll}
%{_libdir}/wine/%{winedlldir}/esent.%{winedll}
%{_libdir}/wine/%{winedlldir}/evr.%{winedll}
%{_libdir}/wine/%{winedlldir}/explorerframe.%{winedll}
%{_libdir}/wine/%{winedlldir}/faultrep.%{winedll}
%{_libdir}/wine/%{winedlldir}/feclient.%{winedll}
%{_libdir}/wine/%{winedlldir}/fltlib.%{winedll}
%{_libdir}/wine/%{winedlldir}/fltmgr.%{winesys}
%{_libdir}/wine/%{winedlldir}/fntcache.%{winedll}
%{_libdir}/wine/%{winedlldir}/fontsub.%{winedll}
%{_libdir}/wine/%{winedlldir}/fusion.%{winedll}
%{_libdir}/wine/%{winedlldir}/fwpuclnt.%{winedll}
%{_libdir}/wine/%{winedlldir}/gameux.%{winedll}
%{_libdir}/wine/%{winedlldir}/gamingtcui.%{winedll}
%{_libdir}/wine/%{winedlldir}/gdi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/gdiplus.%{winedll}
%{_libdir}/wine/%{winedlldir}/glu32.%{winedll}
%{_libdir}/wine/%{winesodir}/gphoto2.so
%{_libdir}/wine/%{winedlldir}/gphoto2.%{wineds}
%{_libdir}/wine/%{winedlldir}/gpkcsp.%{winedll}
%{_libdir}/wine/%{winedlldir}/hal.%{winedll}
%{_libdir}/wine/%{winedlldir}/hh.%{wineexe}
%{_libdir}/wine/%{winedlldir}/hhctrl.%{wineocx}
%{_libdir}/wine/%{winedlldir}/hid.%{winedll}
%{_libdir}/wine/%{winedlldir}/hidclass.%{winesys}
%{_libdir}/wine/%{winedlldir}/hidparse.%{winesys}
%{_libdir}/wine/%{winedlldir}/hlink.%{winedll}
%{_libdir}/wine/%{winedlldir}/hnetcfg.%{winedll}
%{_libdir}/wine/%{winedlldir}/http.%{winesys}
%{_libdir}/wine/%{winedlldir}/httpapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/icacls.%{wineexe}
%{_libdir}/wine/%{winedlldir}/iccvid.%{winedll}
%{_libdir}/wine/%{winedlldir}/icinfo.%{wineexe}
%{_libdir}/wine/%{winedlldir}/icmp.%{winedll}
%{_libdir}/wine/%{winedlldir}/ieframe.%{winedll}
%{_libdir}/wine/%{winedlldir}/ieproxy.%{winedll}
%{_libdir}/wine/%{winedlldir}/imaadp32.%{wineacm}
%{_libdir}/wine/%{winedlldir}/imagehlp.%{winedll}
%{_libdir}/wine/%{winedlldir}/imm32.%{winedll}
%{_libdir}/wine/%{winedlldir}/inetcomm.%{winedll}
%{_libdir}/wine/%{winedlldir}/inetcpl.%{winecpl}
%{_libdir}/wine/%{winedlldir}/inetmib1.%{winedll}
%{_libdir}/wine/%{winedlldir}/infosoft.%{winedll}
%{_libdir}/wine/%{winedlldir}/initpki.%{winedll}
%{_libdir}/wine/%{winedlldir}/inkobj.%{winedll}
%{_libdir}/wine/%{winedlldir}/inseng.%{winedll}
%{_libdir}/wine/%{winedlldir}/iphlpapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/iprop.%{winedll}
%{_libdir}/wine/%{winedlldir}/irprops.%{winecpl}
%{_libdir}/wine/%{winedlldir}/itircl.%{winedll}
%{_libdir}/wine/%{winedlldir}/itss.%{winedll}
%{_libdir}/wine/%{winedlldir}/joy.%{winecpl}
%{_libdir}/wine/%{winedlldir}/jscript.%{winedll}
%{_libdir}/wine/%{winedlldir}/jsproxy.%{winedll}
%{_libdir}/wine/%{winesodir}/kerberos.so
%{_libdir}/wine/%{winedlldir}/kerberos.%{winedll}
%{_libdir}/wine/%{winedlldir}/kernel32.%{winedll}
%{_libdir}/wine/%{winedlldir}/kernelbase.%{winedll}
%{_libdir}/wine/%{winedlldir}/ksecdd.%{winesys}
%{_libdir}/wine/%{winedlldir}/ksproxy.%{wineax}
%{_libdir}/wine/%{winedlldir}/ksuser.%{winedll}
%{_libdir}/wine/%{winedlldir}/ktmw32.%{winedll}
%{_libdir}/wine/%{winedlldir}/l3codeca.%{wineacm}
%{_libdir}/wine/%{winedlldir}/light.%{winemsstyles}
%{_libdir}/wine/%{winedlldir}/loadperf.%{winedll}
%{_libdir}/wine/%{winedlldir}/localspl.%{winedll}
%{_libdir}/wine/%{winedlldir}/localui.%{winedll}
%{_libdir}/wine/%{winedlldir}/lodctr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/lz32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mapistub.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciavi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mcicda.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciqtz32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciseq.%{winedll}
%{_libdir}/wine/%{winedlldir}/mciwave.%{winedll}
%{_libdir}/wine/%{winedlldir}/mf.%{winedll}
%{_libdir}/wine/%{winedlldir}/mf3216.%{winedll}
%{_libdir}/wine/%{winedlldir}/mferror.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfmediaengine.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfplat.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfplay.%{winedll}
%{_libdir}/wine/%{winedlldir}/mfreadwrite.%{winedll}
%{_libdir}/wine/%{winedlldir}/mgmtapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/midimap.%{winedll}
%{_libdir}/wine/%{winedlldir}/mlang.%{winedll}
%{_libdir}/wine/%{winedlldir}/mmcndmgr.%{winedll}
%{_libdir}/wine/%{winedlldir}/mmdevapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/mofcomp.%{wineexe}
%{_libdir}/wine/%{winesodir}/mountmgr.so
%{_libdir}/wine/%{winedlldir}/mountmgr.%{winesys}
%{_libdir}/wine/%{winedlldir}/mp3dmod.%{winedll}
%{_libdir}/wine/%{winedlldir}/mpr.%{winedll}
%{_libdir}/wine/%{winedlldir}/mprapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/msacm32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msacm32.%{winedrv}
%{_libdir}/wine/%{winedlldir}/msado15.%{winedll}
%{_libdir}/wine/%{winedlldir}/msadp32.%{wineacm}
%{_libdir}/wine/%{winedlldir}/msasn1.%{winedll}
%{_libdir}/wine/%{winedlldir}/mscat32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mscoree.%{winedll}
%{_libdir}/wine/%{winedlldir}/mscorwks.%{winedll}
%{_libdir}/wine/%{winedlldir}/msctf.%{winedll}
%{_libdir}/wine/%{winedlldir}/msctfmonitor.%{winedll}
%{_libdir}/wine/%{winedlldir}/msctfp.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdaps.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdasql.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdelta.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdmo.%{winedll}
%{_libdir}/wine/%{winedlldir}/msdrm.%{winedll}
%{_libdir}/wine/%{winedlldir}/msftedit.%{winedll}
%{_libdir}/wine/%{winedlldir}/msg711.%{wineacm}
%{_libdir}/wine/%{winedlldir}/msgsm32.%{wineacm}
%{_libdir}/wine/%{winedlldir}/mshtml.%{winedll}
%{_libdir}/wine/%{winedlldir}/mshtml.%{winetlb}
%{_libdir}/wine/%{winedlldir}/msi.%{winedll}
%{_libdir}/wine/%{winedlldir}/msident.%{winedll}
%{_libdir}/wine/%{winedlldir}/msimtf.%{winedll}
%{_libdir}/wine/%{winedlldir}/msimg32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msimsg.%{winedll}
%{_libdir}/wine/%{winedlldir}/msinfo32.%{wineexe}
%{_libdir}/wine/%{winedlldir}/msisip.%{winedll}
%{_libdir}/wine/%{winedlldir}/msisys.%{wineocx}
%{_libdir}/wine/%{winedlldir}/msls31.%{winedll}
%{_libdir}/wine/%{winedlldir}/msnet32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mspatcha.%{winedll}
%{_libdir}/wine/%{winedlldir}/msports.%{winedll}
%{_libdir}/wine/%{winedlldir}/msscript.%{wineocx}
%{_libdir}/wine/%{winedlldir}/mssign32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mssip32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msrle32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mstask.%{winedll}
%{_libdir}/wine/%{winesodir}/msv1_0.so
%{_libdir}/wine/%{winedlldir}/msv1_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcirt.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp_win.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcm80.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcm90.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp60.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp70.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp71.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp80.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp90.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp100.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp110.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp120.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp120_app.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp140.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp140_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcp140_atomic_wait.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr70.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr71.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr80.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr90.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr100.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr110.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr120.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcr120_app.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrt.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrt20.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrt40.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvcrtd.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvfw32.%{winedll}
%{_libdir}/wine/%{winedlldir}/msvidc32.%{winedll}
%{_libdir}/wine/%{winedlldir}/mswsock.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml2.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml3.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml4.%{winedll}
%{_libdir}/wine/%{winedlldir}/msxml6.%{winedll}
%{_libdir}/wine/%{winedlldir}/mtxdm.%{winedll}
%{_libdir}/wine/%{winedlldir}/nddeapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/ncrypt.%{winedll}
%{_libdir}/wine/%{winedlldir}/ndis.%{winesys}
%{_libdir}/wine/%{winesodir}/netapi32.so
%{_libdir}/wine/%{winedlldir}/netapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/netcfgx.%{winedll}
%{_libdir}/wine/%{winedlldir}/netio.%{winesys}
%{_libdir}/wine/%{winedlldir}/netprofm.%{winedll}
%{_libdir}/wine/%{winedlldir}/netsh.%{wineexe}
%{_libdir}/wine/%{winedlldir}/netutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/newdev.%{winedll}
%{_libdir}/wine/%{winedlldir}/ninput.%{winedll}
%{_libdir}/wine/%{winedlldir}/normaliz.%{winedll}
%{_libdir}/wine/%{winedlldir}/npmshtml.%{winedll}
%{_libdir}/wine/%{winedlldir}/npptools.%{winedll}
%{_libdir}/wine/%{winedlldir}/nsi.%{winedll}
%{_libdir}/wine/%{winesodir}/nsiproxy.so
%{_libdir}/wine/%{winedlldir}/nsiproxy.%{winesys}
%{_libdir}/wine/%{winesodir}/ntdll.so
%{_libdir}/wine/%{winedlldir}/ntdll.%{winedll}
%{_libdir}/wine/%{winedlldir}/ntdsapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/ntprint.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winesodir}/nvcuda.dll.so
%{_libdir}/wine/%{winesodir}/nvcuvid.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/nvcuda.dll
%{_libdir}/wine/%{winedlldir}/nvcuvid.dll
%endif
%endif
%{_libdir}/wine/%{winedlldir}/objsel.%{winedll}
%{_libdir}/wine/%{winesodir}/odbc32.so
%{_libdir}/wine/%{winedlldir}/odbc32.%{winedll}
%{_libdir}/wine/%{winedlldir}/odbcbcp.%{winedll}
%{_libdir}/wine/%{winedlldir}/odbccp32.%{winedll}
%{_libdir}/wine/%{winedlldir}/odbccu32.%{winedll}
%{_libdir}/wine/%{winedlldir}/ole32.%{winedll}
%{_libdir}/wine/%{winedlldir}/oleacc.%{winedll}
%{_libdir}/wine/%{winedlldir}/oleaut32.%{winedll}
%{_libdir}/wine/%{winedlldir}/olecli32.%{winedll}
%{_libdir}/wine/%{winedlldir}/oledb32.%{winedll}
%{_libdir}/wine/%{winedlldir}/oledlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/olepro32.%{winedll}
%{_libdir}/wine/%{winedlldir}/olesvr32.%{winedll}
%{_libdir}/wine/%{winedlldir}/olethk32.%{winedll}
%{_libdir}/wine/%{winedlldir}/opcservices.%{winedll}
%{_libdir}/wine/%{winedlldir}/packager.%{winedll}
%{_libdir}/wine/%{winedlldir}/pdh.%{winedll}
%{_libdir}/wine/%{winedlldir}/photometadatahandler.%{winedll}
%{_libdir}/wine/%{winedlldir}/pidgen.%{winedll}
%{_libdir}/wine/%{winedlldir}/powrprof.%{winedll}
%{_libdir}/wine/%{winedlldir}/presentationfontcache.%{wineexe}
%{_libdir}/wine/%{winedlldir}/printui.%{winedll}
%{_libdir}/wine/%{winedlldir}/prntvpt.%{winedll}
%{_libdir}/wine/%{winedlldir}/propsys.%{winedll}
%{_libdir}/wine/%{winedlldir}/psapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/pstorec.%{winedll}
%{_libdir}/wine/%{winedlldir}/pwrshplugin.%{winedll}
%{_libdir}/wine/%{winedlldir}/qasf.%{winedll}
%{_libdir}/wine/%{winesodir}/qcap.so
%{_libdir}/wine/%{winedlldir}/qcap.%{winedll}
%{_libdir}/wine/%{winedlldir}/qedit.%{winedll}
%{_libdir}/wine/%{winedlldir}/qdvd.%{winedll}
%{_libdir}/wine/%{winedlldir}/qmgr.%{winedll}
%{_libdir}/wine/%{winedlldir}/qmgrprxy.%{winedll}
%{_libdir}/wine/%{winedlldir}/quartz.%{winedll}
%{_libdir}/wine/%{winedlldir}/query.%{winedll}
%{_libdir}/wine/%{winedlldir}/qwave.%{winedll}
%{_libdir}/wine/%{winedlldir}/rasapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/rasdlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/regapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/resutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/riched20.%{winedll}
%{_libdir}/wine/%{winedlldir}/riched32.%{winedll}
%{_libdir}/wine/%{winedlldir}/rpcrt4.%{winedll}
%{_libdir}/wine/%{winedlldir}/robocopy.%{wineexe}
%{_libdir}/wine/%{winedlldir}/rsabase.%{winedll}
%{_libdir}/wine/%{winedlldir}/rsaenh.%{winedll}
%{_libdir}/wine/%{winedlldir}/rstrtmgr.%{winedll}
%{_libdir}/wine/%{winedlldir}/rtutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/rtworkq.%{winedll}
%{_libdir}/wine/%{winedlldir}/samlib.%{winedll}
%{_libdir}/wine/%{winedlldir}/sapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/sas.%{winedll}
%{_libdir}/wine/%{winedlldir}/sc.%{wineexe}
%{_libdir}/wine/%{winedlldir}/scarddlg.%{winedll}
%{_libdir}/wine/%{winedlldir}/sccbase.%{winedll}
%{_libdir}/wine/%{winedlldir}/schannel.%{winedll}
%{_libdir}/wine/%{winedlldir}/scrobj.%{winedll}
%{_libdir}/wine/%{winedlldir}/scrrun.%{winedll}
%{_libdir}/wine/%{winedlldir}/scsiport.%{winesys}
%{_libdir}/wine/%{winedlldir}/sechost.%{winedll}
%{_libdir}/wine/%{winesodir}/secur32.so
%{_libdir}/wine/%{winedlldir}/secur32.%{winedll}
%{_libdir}/wine/%{winedlldir}/sensapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/serialui.%{winedll}
%{_libdir}/wine/%{winedlldir}/setupapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/sfc_os.%{winedll}
%{_libdir}/wine/%{winedlldir}/shcore.%{winedll}
%{_libdir}/wine/%{winedlldir}/shdoclc.%{winedll}
%{_libdir}/wine/%{winedlldir}/shdocvw.%{winedll}
%{_libdir}/wine/%{winedlldir}/schedsvc.%{winedll}
%{_libdir}/wine/%{winedlldir}/shell32.%{winedll}
%{_libdir}/wine/%{winedlldir}/shfolder.%{winedll}
%{_libdir}/wine/%{winedlldir}/shlwapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/shutdown.%{wineexe}
%{_libdir}/wine/%{winedlldir}/slbcsp.%{winedll}
%{_libdir}/wine/%{winedlldir}/slc.%{winedll}
%{_libdir}/wine/%{winedlldir}/snmpapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/softpub.%{winedll}
%{_libdir}/wine/%{winedlldir}/spoolsv.%{wineexe}
%{_libdir}/wine/%{winedlldir}/sppc.%{winedll}
%{_libdir}/wine/%{winedlldir}/srclient.%{winedll}
%{_libdir}/wine/%{winedlldir}/srvcli.%{winedll}
%{_libdir}/wine/%{winedlldir}/sspicli.%{winedll}
%{_libdir}/wine/%{winedlldir}/stdole2.%{winetlb}
%{_libdir}/wine/%{winedlldir}/stdole32.%{winetlb}
%{_libdir}/wine/%{winedlldir}/sti.%{winedll}
%{_libdir}/wine/%{winedlldir}/strmdll.%{winedll}
%{_libdir}/wine/%{winedlldir}/subst.%{wineexe}
%{_libdir}/wine/%{winedlldir}/svchost.%{wineexe}
%{_libdir}/wine/%{winedlldir}/svrapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/sxs.%{winedll}
%{_libdir}/wine/%{winedlldir}/systeminfo.%{wineexe}
%{_libdir}/wine/%{winedlldir}/t2embed.%{winedll}
%{_libdir}/wine/%{winedlldir}/tapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/taskkill.%{wineexe}
%{_libdir}/wine/%{winedlldir}/taskschd.%{winedll}
%{_libdir}/wine/%{winedlldir}/tbs.%{winedll}
%{_libdir}/wine/%{winedlldir}/tdh.%{winedll}
%{_libdir}/wine/%{winedlldir}/tdi.%{winesys}
%{_libdir}/wine/%{winedlldir}/traffic.%{winedll}
%{_libdir}/wine/%{winedlldir}/tzres.%{winedll}
%{_libdir}/wine/%{winedlldir}/ucrtbase.%{winedll}
%{_libdir}/wine/%{winedlldir}/uianimation.%{winedll}
%{_libdir}/wine/%{winedlldir}/uiautomationcore.%{winedll}
%{_libdir}/wine/%{winedlldir}/uiribbon.%{winedll}
%{_libdir}/wine/%{winedlldir}/unicows.%{winedll}
%{_libdir}/wine/%{winedlldir}/unlodctr.%{wineexe}
%{_libdir}/wine/%{winedlldir}/updspapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/url.%{winedll}
%{_libdir}/wine/%{winedlldir}/urlmon.%{winedll}
%{_libdir}/wine/%{winedlldir}/usbd.%{winesys}
%{_libdir}/wine/%{winedlldir}/user32.%{winedll}
%{_libdir}/wine/%{winedlldir}/usp10.%{winedll}
%{_libdir}/wine/%{winedlldir}/utildll.%{winedll}
%{_libdir}/wine/%{winedlldir}/uxtheme.%{winedll}
%{_libdir}/wine/%{winedlldir}/userenv.%{winedll}
%{_libdir}/wine/%{winedlldir}/vbscript.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp90.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp100.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp110.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp120.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcomp140.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcruntime140.%{winedll}
%{_libdir}/wine/%{winedlldir}/vcruntime140_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/vdmdbg.%{winedll}
%{_libdir}/wine/%{winedlldir}/vga.%{winedll}
%{_libdir}/wine/%{winedlldir}/version.%{winedll}
%{_libdir}/wine/%{winedlldir}/virtdisk.%{winedll}
%{_libdir}/wine/%{winedlldir}/vssapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/vulkan-1.%{winedll}
%{_libdir}/wine/%{winedlldir}/wbemdisp.%{winedll}
%{_libdir}/wine/%{winedlldir}/wbemprox.%{winedll}
%{_libdir}/wine/%{winedlldir}/wdscore.%{winedll}
%{_libdir}/wine/%{winedlldir}/webservices.%{winedll}
%{_libdir}/wine/%{winedlldir}/websocket.%{winedll}
%{_libdir}/wine/%{winedlldir}/wer.%{winedll}
%{_libdir}/wine/%{winedlldir}/wevtapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wevtsvc.%{winedll}
%{_libdir}/wine/%{winedlldir}/where.%{wineexe}
%{_libdir}/wine/%{winedlldir}/whoami.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wiaservc.%{winedll}
%{_libdir}/wine/%{winedlldir}/wimgapi.%{winedll}
%{_libdir}/wine/%{winesodir}/win32u.so
%{_libdir}/wine/%{winedlldir}/win32u.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.devices.enumeration.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.gaming.input.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.globalization.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.media.devices.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.media.speech.%{winedll}
%{_libdir}/wine/%{winedlldir}/windows.networking.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winedlldir}/win32k.%{winesys}
%{_libdir}/wine/%{winedlldir}/windows.networking.connectivity.%{winedll}
%endif
%{_libdir}/wine/%{winedlldir}/windowscodecs.%{winedll}
%{_libdir}/wine/%{winedlldir}/windowscodecsext.%{winedll}
%{_libdir}/wine/%{winesodir}/winebus.so
%{_libdir}/wine/%{winedlldir}/winebus.%{winesys}
%{_libdir}/wine/%{winesodir}/winegstreamer.so
%{_libdir}/wine/%{winedlldir}/winegstreamer.%{winedll}
%{_libdir}/wine/%{winedlldir}/winehid.%{winesys}
%{_libdir}/wine/%{winedlldir}/winemapi.%{winedll}
%{_libdir}/wine/%{winesodir}/winevulkan.so
%if 0%{?fshack}
%{_libdir}/wine/%{winesodir}/winevulkan.dll.so
%else
%{_libdir}/wine/%{winedlldir}/winevulkan.%{winedll}
%endif
%{_libdir}/wine/%{winesodir}/wineusb.sys.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/wineusb.sys
%endif
%{_libdir}/wine/%{winesodir}/winex11.so
%{_libdir}/wine/%{winedlldir}/winex11.%{winedrv}
%{_libdir}/wine/%{winedlldir}/wing32.%{winedll}
%{_libdir}/wine/%{winedlldir}/winhttp.%{winedll}
%{_libdir}/wine/%{winedlldir}/wininet.%{winedll}
%{_libdir}/wine/%{winedlldir}/winmm.%{winedll}
%{_libdir}/wine/%{winedlldir}/winnls32.%{winedll}
%{_libdir}/wine/%{winesodir}/winspool.so
%{_libdir}/wine/%{winedlldir}/winspool.%{winedrv}
%{_libdir}/wine/%{winedlldir}/winsta.%{winedll}
%{_libdir}/wine/%{winedlldir}/wintypes.%{winedll}
%{_libdir}/wine/%{winedlldir}/wlanui.%{winedll}
# FIXME - remove when mfplat reverts are unneeded
%{_libdir}/wine/%{winedlldir}/wmadmod.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmasf.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmic.%{wineexe}
%{_libdir}/wine/%{winedlldir}/wmiutils.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmp.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmvcore.%{winedll}
%{_libdir}/wine/%{winedlldir}/spoolss.%{winedll}
%{_libdir}/wine/%{winedlldir}/winscard.%{winedll}
%{_libdir}/wine/%{winedlldir}/wintab32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wintrust.%{winedll}
%{_libdir}/wine/%{winedlldir}/winusb.%{winedll}
%{_libdir}/wine/%{winedlldir}/wlanapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wmphoto.%{winedll}
%{_libdir}/wine/%{winedlldir}/wnaspi32.%{winedll}
%ifarch x86_64
%{_libdir}/wine/%{winedlldir}/wow64.%{winedll}
%{_libdir}/wine/%{winedlldir}/wow64cpu.%{winedll}
%{_libdir}/wine/%{winedlldir}/wow64win.%{winedll}
%endif
%{_libdir}/wine/%{winedlldir}/wpc.%{winedll}
%{_libdir}/wine/%{winesodir}/wpcap.so
%{_libdir}/wine/%{winedlldir}/wpcap.%{winedll}
%{_libdir}/wine/%{winesodir}/ws2_32.so
%{_libdir}/wine/%{winedlldir}/ws2_32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wsdapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wshom.%{wineocx}
%{_libdir}/wine/%{winedlldir}/wsnmp32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wsock32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wtsapi32.%{winedll}
%{_libdir}/wine/%{winedlldir}/wuapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/wuaueng.%{winedll}
%{_libdir}/wine/%{winedlldir}/wuauserv.%{wineexe}
%{_libdir}/wine/%{winedlldir}/security.%{winedll}
%{_libdir}/wine/%{winedlldir}/sfc.%{winedll}
%{_libdir}/wine/%{winedlldir}/wineps.%{winedrv}
%{_libdir}/wine/%{winedlldir}/d3d8.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d8thk.%{winedll}
%{_libdir}/wine/%{winedlldir}/d3d9.%{winedll}
%{_libdir}/wine/%{winesodir}/opengl32.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/opengl32.dll
%endif
%{_libdir}/wine/%{winedlldir}/wined3d.%{winedll}
%{_libdir}/wine/%{winedlldir}/winexinput.%{winesys}
%{_libdir}/wine/%{winesodir}/dnsapi.so
%{_libdir}/wine/%{winedlldir}/dnsapi.%{winedll}
%{_libdir}/wine/%{winedlldir}/iexplore.%{wineexe}
%{_libdir}/wine/%{winedlldir}/xactengine2_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine2_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine2_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine2_9.%{winedll}
%if 0%{?wine_staging}
#{_libdir}/wine/%%{winesodir}/xactengine2_1.dll.so
#{_libdir}/wine/%%{winesodir}/xactengine2_2.dll.so
#{_libdir}/wine/%%{winesodir}/xactengine2_3.dll.so
#{_libdir}/wine/%%{winesodir}/xactengine2_5.dll.so
#{_libdir}/wine/%%{winesodir}/xactengine2_6.dll.so
#{_libdir}/wine/%%{winesodir}/xactengine2_8.dll.so
#{_libdir}/wine/%%{winesodir}/xactengine2_10.dll.so
%endif
%{_libdir}/wine/%{winedlldir}/xactengine3_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_6.%{winedll}
%{_libdir}/wine/%{winedlldir}/xactengine3_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_6.%{winedll}
%{_libdir}/wine/%{winedlldir}/x3daudio1_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xapofx1_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_5.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_6.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_7.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_8.%{winedll}
%{_libdir}/wine/%{winedlldir}/xaudio2_9.%{winedll}
%{_libdir}/wine/%{winedlldir}/xcopy.%{wineexe}
%{_libdir}/wine/%{winedlldir}/xinput1_1.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput1_2.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput1_3.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput1_4.%{winedll}
%{_libdir}/wine/%{winedlldir}/xinput9_1_0.%{winedll}
%{_libdir}/wine/%{winedlldir}/xmllite.%{winedll}
%{_libdir}/wine/%{winedlldir}/xolehlp.%{winedll}
%{_libdir}/wine/%{winedlldir}/xpsprint.%{winedll}
%{_libdir}/wine/%{winedlldir}/xpssvcs.%{winedll}

%if 0%{?wine_staging}
%ifarch x86_64 aarch64
%{_libdir}/wine/%{winedlldir}/nvapi64.%{winedll}
%{_libdir}/wine/%{winesodir}/nvencodeapi64.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/nvencodeapi64.dll
%endif
%else
%{_libdir}/wine/%{winedlldir}/nvapi.%{winedll}
%{_libdir}/wine/%{winesodir}/nvencodeapi.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/nvencodeapi.dll
%endif
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/%{winedlldir}/winevdm.%{wineexe}
%{_libdir}/wine/%{winedlldir}/ifsmgr.%{winevxd}
%{_libdir}/wine/%{winedlldir}/mmdevldr.%{winevxd}
%{_libdir}/wine/%{winedlldir}/monodebg.%{winevxd}
%{_libdir}/wine/%{winedlldir}/rundll.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/vdhcp.%{winevxd}
%{_libdir}/wine/%{winedlldir}/user.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/vmm.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vnbt.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vnetbios.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vtdapi.%{winevxd}
%{_libdir}/wine/%{winedlldir}/vwin32.%{winevxd}
%{_libdir}/wine/%{winedlldir}/w32skrnl.%{winedll}
%{_libdir}/wine/%{winedlldir}/avifile.%{winedll16}
%{_libdir}/wine/%{winedlldir}/comm.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/commdlg.%{winedll16}
%{_libdir}/wine/%{winedlldir}/compobj.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ctl3d.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ctl3dv2.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ddeml.%{winedll16}
%{_libdir}/wine/%{winedlldir}/dispdib.%{winedll16}
%{_libdir}/wine/%{winedlldir}/display.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/gdi.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/imm.%{winedll16}
%{_libdir}/wine/%{winedlldir}/krnl386.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/keyboard.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/lzexpand.%{winedll16}
%{_libdir}/wine/%{winedlldir}/mmsystem.%{winedll16}
%{_libdir}/wine/%{winedlldir}/mouse.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/msacm.%{winedll16}
%{_libdir}/wine/%{winedlldir}/msvideo.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2conv.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2disp.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2nls.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2prox.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ole2thk.%{winedll16}
%{_libdir}/wine/%{winedlldir}/olecli.%{winedll16}
%{_libdir}/wine/%{winedlldir}/olesvr.%{winedll16}
%{_libdir}/wine/%{winedlldir}/rasapi16.%{winedll16}
%{_libdir}/wine/%{winedlldir}/setupx.%{winedll16}
%{_libdir}/wine/%{winedlldir}/shell.%{winedll16}
%{_libdir}/wine/%{winedlldir}/sound.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/storage.%{winedll16}
%{_libdir}/wine/%{winedlldir}/stress.%{winedll16}
%{_libdir}/wine/%{winedlldir}/system.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/toolhelp.%{winedll16}
%{_libdir}/wine/%{winedlldir}/twain.%{winedll16}
%{_libdir}/wine/%{winedlldir}/typelib.%{winedll16}
%{_libdir}/wine/%{winedlldir}/ver.%{winedll16}
%{_libdir}/wine/%{winedlldir}/w32sys.%{winedll16}
%{_libdir}/wine/%{winedlldir}/win32s16.%{winedll16}
%{_libdir}/wine/%{winedlldir}/win87em.%{winedll16}
%{_libdir}/wine/%{winedlldir}/winaspi.%{winedll16}
%{_libdir}/wine/%{winedlldir}/windebug.%{winedll16}
%{_libdir}/wine/%{winedlldir}/wineps16.%{winedrv16}
%{_libdir}/wine/%{winedlldir}/wing.%{winedll16}
%{_libdir}/wine/%{winedlldir}/winhelp.%{wineexe16}
%{_libdir}/wine/%{winedlldir}/winnls.%{winedll16}
%{_libdir}/wine/%{winedlldir}/winoldap.%{winemod16}
%{_libdir}/wine/%{winedlldir}/winsock.%{winedll16}
%{_libdir}/wine/%{winedlldir}/wintab.%{winedll16}
%{_libdir}/wine/%{winedlldir}/wow32.%{winedll}
%endif

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
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
%{_datadir}/wine/nls/c_20949.nls
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
%{_datadir}/wine/nls/c_708.nls
%{_datadir}/wine/nls/c_737.nls
%{_datadir}/wine/nls/c_720.nls
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
%{_datadir}/wine/nls/locale.nls
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
%doc README.tahoma
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

# ldap subpackage
%files ldap
%{_libdir}/wine/%{winesodir}/wldap32.so
%{_libdir}/wine/%{winedlldir}/wldap32.%{winedll}

# cms subpackage
%files cms
%{_libdir}/wine/%{winedlldir}/mscms.%{winedll}

# twain subpackage
%files twain
%{_libdir}/wine/%{winedlldir}/twain_32.%{winedll}
%{_libdir}/wine/%{winesodir}/sane.so
%{_libdir}/wine/%{winedlldir}/sane.%{wineds}

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
%{_libdir}/wine/%{winesodir}/*.a
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/*.a
%endif

%files pulseaudio
%{_libdir}/wine/%{winesodir}/winepulse.so
%{_libdir}/wine/%{winedlldir}/winepulse.%{winedrv}

%files alsa
%{_libdir}/wine/%{winesodir}/winealsa.so
%{_libdir}/wine/%{winedlldir}/winealsa.%{winedrv}

%files openal
%{_libdir}/wine/%{winesodir}/openal32.dll.so
%if 0%{?wine_mingw}
%{_libdir}/wine/%{winedlldir}/openal32.dll
%endif

%files opencl
%{_libdir}/wine/%{winesodir}/opencl.so
%{_libdir}/wine/%{winedlldir}/opencl.%{winedll}


%changelog
* Sat Jun 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.10-100
- 7.10

* Mon May 30 2022 Phantom X - 1:7.9-102.20220527gitd928668
- Forgotten last snapshot

* Sat May 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.9-101.20220526gitd3378c1
- Snapshot

* Sun May 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.8-101.20220513git5aa9340
- Snapshot

* Sat May 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.8-100
- 7.8

* Tue May 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.7-102.20220502gitf91f434
- fastsync

* Sat Apr 30 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.7-101.20220428git64b96ee
- Snapshot

* Sat Apr 23 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.7-100
- 7.7

* Sat Apr 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.6-102.20220415gite254680
- Bump

* Tue Apr 12 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.6-101.20220411git02faaea
- Snapshot

* Sat Apr 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.6-100
- 7.6

* Mon Apr 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.5-101.20220401git0de8d01
- Snapshot

* Sat Mar 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.5-100
- 7.5

* Mon Mar 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-103.20220318git47b02e8
- Weekend bump

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-102.20220315git670a1e8
- tkg updates

* Tue Mar 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-101.20220314git8a52d3e
- Snapshot

* Sun Mar 13 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.4-100
- 7.4

* Sat Mar 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-103.20220304git18230d2
- Bump

* Wed Mar 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-102.20220301git89a8b32
- Snapshot

* Sun Feb 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-101
- Update tkg patches

* Sat Feb 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.3-100
- 7.3

* Tue Feb 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.2-102.20220221git53cb28e
- Bump to get staging restored mfplat streaming support

* Mon Feb 21 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.2-101.20220218gitbf42dca
- Snapshot
- Use mfplat patch from Proton-GE, cleaning all reverts

* Mon Feb 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.2-100
- 7.2
- Disable fastsync for the time

* Tue Feb 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.1-102.20220207git54b8c8c
- Bump
- wine-mono 7.1.2
- mfplat streaming restoring optional support

* Sun Feb 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.1-101.20220204git4364ff8
- Snapshot

* Sat Jan 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.1-100
- 7.1

* Sat Jan 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0-101.20220121gitc09a5da
- Snapshot

* Tue Jan 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0-100
- 7.0

* Sat Jan 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc6-100
- 7.0-rc6

* Sat Jan 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc5-100
- 7.0-rc5

* Mon Jan 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc4-100
- 7.0-rc4

* Fri Dec 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc3-101.20211230gitb6dc839
- Snapshot

* Mon Dec 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc3-100
- 7.0-rc3

* Sat Dec 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-103.20211223git7555573
- Bump

* Tue Dec 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-102.20211220git656d7f5
- Snapshot

* Mon Dec 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-101
- Add some pending hotfixes

* Sat Dec 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc2-100
- 7.0-rc2

* Sat Dec 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:7.0~rc1-100
- 7.0-rc1
- fastsync optional support

* Sun Dec 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.23-100
- 6.23

* Sat Nov 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.22-102.20211126gitf03933f
- Snapshot

* Tue Nov 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.22-101
- Disable extfaudio

* Sat Nov 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.22-100
- 6.22

* Wed Nov 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-103.20211116gitb65ef71
- Bump

* Sat Nov 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-102.20211112gitbe0684d
- Bump

* Wed Nov 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-101.20211109git6a072b9
- Snapshot

* Sat Nov 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.21-100
- 6.21

* Tue Nov 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.20-102.20211101git0b79e2c
- futex_waitv support

* Sat Oct 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.20-101.20211029git5f93c68
- Snapshot
- Obsoletes wine-capi packages

* Mon Oct 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.20-100
- 6.20
- Add reverts for external FAudio and mfplat

* Wed Oct 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.19-101.20211012git50f889f
- Snapshot

* Sat Oct 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.19-100
- 6.19

* Wed Oct 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-104.20211005gited38d12
- Bump

* Mon Oct 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-103.20211004git5a8dcb0
- Bump

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-102.20211001gita87abdb
- Snapshot

* Sat Sep 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-101
- Add some fixes in review

* Sat Sep 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.18-100
- 6.18

* Mon Sep 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.17-101.20210917git16e73be
- Snapshot

* Sat Sep 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.17-100
- 6.17

* Sat Sep 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.16-101.20210903git8b9f1e1
- Snapshot

* Sat Aug 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.16-100
- 6.16

* Sat Aug 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.15-101.20210820git7d60044
- Snapshot

* Sat Aug 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.15-100
- 6.15

* Tue Aug 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.14-102.20210809gitcaf5ab5
- Bump

* Sat Aug 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.14-101.20210806git2cc98b7
- Snapshot

* Sat Jul 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.14-100
- 6.14

* Tue Jul 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.13-102.20210726gitf1023b4
- Bump

* Fri Jul 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.13-101.20210722gitc518a53
- Snapshot

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.13-100
- 6.13

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-105.20210719gitd60c450
- Bump

* Sat Jul 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-104.20210709git49cde09
- Weekend snapshot

* Fri Jul 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-103.20210708gitd10887b
- Bump

* Tue Jul 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-102.20210705git14f03e8
- Snapshot with some server fixes

* Sat Jul 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-101
- Staging update

* Fri Jul 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.12-100
- 6.12

* Sun Jun 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.11-102.20210625git542175a
- Snapshot
- Add dosbox alternate binary patch

* Sun Jun 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.11-101
- tkg update

* Sat Jun 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.11-100
- 6.11
- Add offline vk.xml for make_vulkan

* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-104.20210611gitf5bd0be
- Bump

* Thu Jun 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-103.20210609git2a505ef
- Snapshot

* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-102
- Add some fixes from Proton GE

* Sun Jun 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-101
- Revert commits breaking joystick

* Sat Jun 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.10-100
- 6.10
- Add rt prio and net raw capabilitiess

* Sat May 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-103.20210528git35180d3
- Bump

* Wed May 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-102.20210525git8ddff3f
- Staging update again

* Tue May 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-101.20210524git94eb8d3
- Snapshot

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.9-100
- 6.9

* Sat May 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.8-100
- 6.8
- Disable childwindow patch, since nine crashes with it

* Tue May 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-105.20210503git3ba4412
- Update

* Sun May 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-104.20210430git2deb8c2
- Staging update
- tkg update

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-103.20210430git2deb8c2
- Update
- More architecture-specific updates

* Wed Apr 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-102.20210427git4ccf749
- Bump

* Tue Apr 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-101.20210426gitd7feceb
- Snapshot
- Architecture-specific updates

* Sat Apr 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.7-100
- 6.7
- BR: gmp (wine-tkg-proton-bcrypt)

* Sat Apr 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.6-101.20210416git749f8c2
- Snapshot

* Mon Apr 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.6-100
- 6.6
- Patchsets review, fshack can be enabled now

* Mon Apr 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.5-102.20210402git2fcc1d0
- Bug#50914 fix

* Sat Apr 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.5-101.20210402git2fcc1d0
- Snapshot
- wine-mono 6.1.1

* Sun Mar 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.5-100
- 6.5

* Wed Mar 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.4-102.20210323gitf69c8f0
- Bump

* Sat Mar 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.4-101.20210319git41df83c
- Snapshot

* Sun Mar 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.4-100
- 6.4

* Sat Mar 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.3-101.20210305git5bccf6f
- Snapshot

* Sat Feb 27 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.3-100
- 6.3

* Sat Feb 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.2-101.20210219git4de079b
- Snapshot

* Sat Feb 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.2-100
- 6.2

* Sat Feb 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.1-102.20210205git4f1b297
- Snapshot

* Mon Feb 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.1-101
- mfplat fix

* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.1-100
- 6.1

* Fri Jan 29 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-106.20210128gitf72ef20
- Update

* Tue Jan 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-105.20210125git2d6462c
- Bump
- BR: libudev

* Tue Jan 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-104.20210118git88220e0
- tkg update

* Mon Jan 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-103.20210115git00401d2
- Pass -fno-tree-dce only to affected objects

* Mon Jan 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-102.20210115git00401d2
- Disable ntdll-NtAlertThreadByThreadId

* Mon Jan 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-101.20210115git00401d2
- Snapshot

* Fri Jan 15 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0-100
- 6.0

* Sat Jan 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc6-100
- 6.0-rc6

* Mon Jan 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc5-101
- Revert some staging patches

* Sun Jan 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc5-100
- 6.0-rc5

* Sat Dec 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc4-100
- 6.0-rc4

* Thu Dec 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc3-101.20201224git9d7a710
- Snapshot

* Sat Dec 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc3-100
- 6.0-rc3

* Thu Dec 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:6.0~rc2-101.20201217gitef876fc
- Snapshot and staging fixes

* Sun Dec 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc2-100
- 6.0-rc2

* Wed Dec 09 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc1-101.20201209git3100197
- Snapshot

* Sat Dec 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:6.0~rc1-100
- 6.0-rc1

* Thu Dec 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.22-102.20201202gite4fbae8
- New snapshot

* Sat Nov 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.22-101.20201127gitcbca9f8
- Snapshot

* Sat Nov 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.22-100
- 5.22

* Sun Nov 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.21-101.20201113gitcf49617
- Snapshot
- Remove glu BR

* Sat Nov 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.21-100
- 5.21

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.20-101.20201030git03eaa2c
- Snapshot

* Sat Oct 24 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.20-100
- 5.20

* Tue Oct 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-103.20201016git0c249e6
- tkg updates. fsync reverts unneeded

* Fri Oct 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-102.20201016git0c249e6
- Snapshot

* Mon Oct 12 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-101
- tkg sync

* Sat Oct 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.19-100
- 5.19

* Wed Oct 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-103.20201006gitc29f9e6
- Bump

* Sun Oct 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-102.20201002gitcce4f36
- Snapshot

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-101
- Staging update

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.18-100
- 5.18

* Wed Sep 16 2020 Phantom X <megaphantomx at hotmail dot com> - 1:5.17-101.20200915git26eedec
- Snapshot

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
