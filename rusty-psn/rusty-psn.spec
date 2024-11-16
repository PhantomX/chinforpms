%bcond_without bin

%if %{with bin}
%global _build_id_links none
%undefine _debugsource_packages
%else
# Use vendor tarball
%bcond_without vendor
%endif

%global vc_id   2a0afcdd36d6bf73f683d77abf352812177cd1a0
%global vendor_hash 4a99bb94fda35a80951c0bbbfef8c47c

Name:           rusty-psn
Version:        0.5.2
Release:        1%{?dist}
Summary:        Simple tool to grab updates for PS3 games

License:        MIT
URL:            https://github.com/RainbowCookie32/%{name}

%if %{with bin}
Source0:        %{url}/releases/download/v%{version}/rusty-psn-cli-linux.zip#/%{name}-cli-%{version}-linux.zip
Source1:        %{url}/releases/download/v%{version}/rusty-psn-egui-linux.zip#/%{name}-egui-%{version}-linux.zip
Source2:        %{url}/raw/%{vc_id}/LICENSE
Source3:        %{url}/raw/%{vc_id}/README.md
Source4:        %{url}/raw/%{vc_id}/resources/OFL.txt
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# rust2rpm -t fedora -V --no-rpmautospec --ignore-missing-license-files -f cli,egui ./Cargo.toml %%{version}
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif
%endif

%if %{with bin}
ExclusiveArch:  x86_64
%else
ExclusiveArch:  %{rust_arches}
%endif

%if %{without bin}
BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  google-noto-sans-fonts
BuildRequires:  google-noto-sans-jp-fonts
BuildRequires:  rust-packaging
%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
%global _vendor_provides %{expand:
Provides:       bundled(crate(ab_glyph)) = 0.2.26
Provides:       bundled(crate(ab_glyph_rasterizer)) = 0.1.8
Provides:       bundled(crate(accesskit)) = 0.12.3
Provides:       bundled(crate(accesskit_consumer)) = 0.16.1
Provides:       bundled(crate(accesskit_macos)) = 0.10.1
Provides:       bundled(crate(accesskit_unix)) = 0.6.2
Provides:       bundled(crate(accesskit_windows)) = 0.15.1
Provides:       bundled(crate(accesskit_winit)) = 0.16.1
Provides:       bundled(crate(addr2line)) = 0.22.0
Provides:       bundled(crate(adler)) = 1.0.2
Provides:       bundled(crate(ahash)) = 0.8.11
Provides:       bundled(crate(aho-corasick)) = 1.1.3
Provides:       bundled(crate(allocator-api2)) = 0.2.18
Provides:       bundled(crate(android-activity)) = 0.5.2
Provides:       bundled(crate(android-properties)) = 0.2.2
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(android-tzdata)) = 0.1.1
Provides:       bundled(crate(anstream)) = 0.6.14
Provides:       bundled(crate(anstyle)) = 1.0.7
Provides:       bundled(crate(anstyle-parse)) = 0.2.4
Provides:       bundled(crate(anstyle-query)) = 1.0.3
Provides:       bundled(crate(anstyle-wincon)) = 3.0.3
Provides:       bundled(crate(arboard)) = 3.4.0
Provides:       bundled(crate(arrayref)) = 0.3.7
Provides:       bundled(crate(arrayvec)) = 0.7.4
Provides:       bundled(crate(ash)) = 0.37.3+1.3.251
Provides:       bundled(crate(ashpd)) = 0.8.1
Provides:       bundled(crate(as-raw-xcb-connection)) = 1.0.1
Provides:       bundled(crate(async-broadcast)) = 0.5.1
Provides:       bundled(crate(async-broadcast)) = 0.7.0
Provides:       bundled(crate(async-channel)) = 2.3.1
Provides:       bundled(crate(async-executor)) = 1.12.0
Provides:       bundled(crate(async-fs)) = 1.6.0
Provides:       bundled(crate(async-fs)) = 2.1.2
Provides:       bundled(crate(async-io)) = 1.13.0
Provides:       bundled(crate(async-io)) = 2.3.2
Provides:       bundled(crate(async-lock)) = 2.8.0
Provides:       bundled(crate(async-lock)) = 3.3.0
Provides:       bundled(crate(async-net)) = 2.0.0
Provides:       bundled(crate(async-once-cell)) = 0.5.3
Provides:       bundled(crate(async-process)) = 1.8.1
Provides:       bundled(crate(async-process)) = 2.2.2
Provides:       bundled(crate(async-recursion)) = 1.1.1
Provides:       bundled(crate(async-signal)) = 0.2.6
Provides:       bundled(crate(async-task)) = 4.7.1
Provides:       bundled(crate(async-trait)) = 0.1.80
Provides:       bundled(crate(atomic-waker)) = 1.1.2
Provides:       bundled(crate(atspi)) = 0.19.0
Provides:       bundled(crate(atspi-common)) = 0.3.0
Provides:       bundled(crate(atspi-connection)) = 0.3.0
Provides:       bundled(crate(atspi-proxies)) = 0.3.0
Provides:       bundled(crate(autocfg)) = 1.3.0
Provides:       bundled(crate(backtrace)) = 0.3.72
Provides:       bundled(crate(base64)) = 0.21.7
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.5.0
Provides:       bundled(crate(bit-set)) = 0.5.3
Provides:       bundled(crate(bit-vec)) = 0.6.3
Provides:       bundled(crate(block)) = 0.1.6
Provides:       bundled(crate(block2-0.2.0)) = alpha.6
Provides:       bundled(crate(block2)) = 0.3.0
Provides:       bundled(crate(block2)) = 0.5.1
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(blocking)) = 1.6.1
Provides:       bundled(crate(block-sys-0.1.0)) = beta.1
Provides:       bundled(crate(block-sys)) = 0.2.1
Provides:       bundled(crate(bumpalo)) = 3.16.0
Provides:       bundled(crate(bytemuck)) = 1.16.0
Provides:       bundled(crate(bytemuck_derive)) = 1.7.0
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(byteorder-lite)) = 0.1.0
Provides:       bundled(crate(bytes)) = 1.6.0
Provides:       bundled(crate(bytesize)) = 1.3.0
Provides:       bundled(crate(calloop)) = 0.12.4
Provides:       bundled(crate(calloop-wayland-source)) = 0.2.0
Provides:       bundled(crate(cc)) = 1.0.98
Provides:       bundled(crate(cesu8)) = 1.1.0
Provides:       bundled(crate(cfg_aliases)) = 0.1.1
Provides:       bundled(crate(cfg-if)) = 1.0.0
Provides:       bundled(crate(cgl)) = 0.3.2
Provides:       bundled(crate(chrono)) = 0.4.38
Provides:       bundled(crate(clap)) = 4.5.13
Provides:       bundled(crate(clap_builder)) = 4.5.13
Provides:       bundled(crate(clap_derive)) = 4.5.13
Provides:       bundled(crate(clap_lex)) = 0.7.0
Provides:       bundled(crate(clipboard-win)) = 3.1.1
Provides:       bundled(crate(clipboard-win)) = 5.3.1
Provides:       bundled(crate(codespan-reporting)) = 0.11.1
Provides:       bundled(crate(colorchoice)) = 1.0.1
Provides:       bundled(crate(com)) = 0.6.0
Provides:       bundled(crate(combine)) = 4.6.7
Provides:       bundled(crate(com_macros)) = 0.6.0
Provides:       bundled(crate(com_macros_support)) = 0.6.0
Provides:       bundled(crate(concurrent-queue)) = 2.5.0
Provides:       bundled(crate(copypasta)) = 0.10.1
Provides:       bundled(crate(core-foundation)) = 0.9.4
Provides:       bundled(crate(core-foundation-sys)) = 0.8.6
Provides:       bundled(crate(core-graphics)) = 0.23.2
Provides:       bundled(crate(core-graphics-types)) = 0.1.3
Provides:       bundled(crate(cpufeatures)) = 0.2.12
Provides:       bundled(crate(crc32fast)) = 1.4.2
Provides:       bundled(crate(crossbeam-utils)) = 0.8.20
Provides:       bundled(crate(crypto-common)) = 0.1.6
Provides:       bundled(crate(cursor-icon)) = 1.1.0
Provides:       bundled(crate(deranged)) = 0.3.11
Provides:       bundled(crate(derivative)) = 2.2.0
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(directories)) = 5.0.1
Provides:       bundled(crate(dirs-next)) = 2.0.0
Provides:       bundled(crate(dirs-sys)) = 0.4.1
Provides:       bundled(crate(dirs-sys-next)) = 0.1.2
Provides:       bundled(crate(dispatch)) = 0.2.0
Provides:       bundled(crate(dlib)) = 0.5.2
Provides:       bundled(crate(document-features)) = 0.2.8
Provides:       bundled(crate(downcast-rs)) = 1.2.1
Provides:       bundled(crate(eframe)) = 0.28.1
Provides:       bundled(crate(emath)) = 0.28.1
Provides:       bundled(crate(endi)) = 1.1.0
Provides:       bundled(crate(enumflags2)) = 0.7.9
Provides:       bundled(crate(enumflags2_derive)) = 0.7.9
Provides:       bundled(crate(enumn)) = 0.1.13
Provides:       bundled(crate(equivalent)) = 1.0.1
Provides:       bundled(crate(errno)) = 0.3.9
Provides:       bundled(crate(error-code)) = 3.2.0
Provides:       bundled(crate(event-listener)) = 2.5.3
Provides:       bundled(crate(event-listener)) = 3.1.0
Provides:       bundled(crate(event-listener)) = 4.0.3
Provides:       bundled(crate(event-listener)) = 5.3.0
Provides:       bundled(crate(event-listener-strategy)) = 0.4.0
Provides:       bundled(crate(event-listener-strategy)) = 0.5.2
Provides:       bundled(crate(fastrand)) = 1.9.0
Provides:       bundled(crate(fastrand)) = 2.1.0
Provides:       bundled(crate(fdeflate)) = 0.3.4
Provides:       bundled(crate(flate2)) = 1.0.30
Provides:       bundled(crate(flexi_logger)) = 0.29.4
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foreign-types)) = 0.5.0
Provides:       bundled(crate(foreign-types-macros)) = 0.2.3
Provides:       bundled(crate(foreign-types-shared)) = 0.3.1
Provides:       bundled(crate(form_urlencoded)) = 1.2.1
Provides:       bundled(crate(futures-channel)) = 0.3.30
Provides:       bundled(crate(futures-core)) = 0.3.30
Provides:       bundled(crate(futures-io)) = 0.3.30
Provides:       bundled(crate(futures-lite)) = 1.13.0
Provides:       bundled(crate(futures-lite)) = 2.3.0
Provides:       bundled(crate(futures-macro)) = 0.3.30
Provides:       bundled(crate(futures-sink)) = 0.3.30
Provides:       bundled(crate(futures-task)) = 0.3.30
Provides:       bundled(crate(futures-util)) = 0.3.30
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(gethostname)) = 0.4.3
Provides:       bundled(crate(getrandom)) = 0.2.15
Provides:       bundled(crate(gimli)) = 0.29.0
Provides:       bundled(crate(gl_generator)) = 0.14.0
Provides:       bundled(crate(glow)) = 0.13.1
Provides:       bundled(crate(glutin)) = 0.31.3
Provides:       bundled(crate(glutin_egl_sys)) = 0.6.0
Provides:       bundled(crate(glutin_glx_sys)) = 0.5.0
Provides:       bundled(crate(glutin_wgl_sys)) = 0.5.0
Provides:       bundled(crate(glutin-winit)) = 0.4.2
Provides:       bundled(crate(gpu-alloc)) = 0.6.0
Provides:       bundled(crate(gpu-allocator)) = 0.25.0
Provides:       bundled(crate(gpu-alloc-types)) = 0.3.0
Provides:       bundled(crate(gpu-descriptor)) = 0.3.0
Provides:       bundled(crate(gpu-descriptor-types)) = 0.2.0
Provides:       bundled(crate(hashbrown)) = 0.14.5
Provides:       bundled(crate(hassle-rs)) = 0.11.0
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit-abi)) = 0.3.9
Provides:       bundled(crate(hex)) = 0.4.3
Provides:       bundled(crate(hexf-parse)) = 0.2.1
Provides:       bundled(crate(hmac)) = 0.12.1
Provides:       bundled(crate(home)) = 0.5.9
Provides:       bundled(crate(http)) = 1.1.0
Provides:       bundled(crate(httparse)) = 1.8.0
Provides:       bundled(crate(http-body)) = 1.0.0
Provides:       bundled(crate(http-body-util)) = 0.1.1
Provides:       bundled(crate(hyper)) = 1.3.1
Provides:       bundled(crate(hyper-rustls)) = 0.27.2
Provides:       bundled(crate(hyper-util)) = 0.1.5
Provides:       bundled(crate(iana-time-zone)) = 0.1.60
Provides:       bundled(crate(iana-time-zone-haiku)) = 0.1.2
Provides:       bundled(crate(icrate)) = 0.0.4
Provides:       bundled(crate(idna)) = 0.5.0
Provides:       bundled(crate(image)) = 0.25.2
Provides:       bundled(crate(indexmap)) = 2.2.6
Provides:       bundled(crate(instant)) = 0.1.13
Provides:       bundled(crate(io-lifetimes)) = 1.0.11
Provides:       bundled(crate(ipnet)) = 2.9.0
Provides:       bundled(crate(is_terminal_polyfill)) = 1.70.0
Provides:       bundled(crate(itoa)) = 1.0.11
Provides:       bundled(crate(jni)) = 0.21.1
Provides:       bundled(crate(jni-sys)) = 0.3.0
Provides:       bundled(crate(jobserver)) = 0.1.31
Provides:       bundled(crate(js-sys)) = 0.3.69
Provides:       bundled(crate(khronos_api)) = 3.1.0
Provides:       bundled(crate(khronos-egl)) = 6.0.0
Provides:       bundled(crate(lazy-bytes-cast)) = 5.0.1
Provides:       bundled(crate(libc)) = 0.2.155
Provides:       bundled(crate(libloading)) = 0.7.4
Provides:       bundled(crate(libloading)) = 0.8.3
Provides:       bundled(crate(libredox)) = 0.0.2
Provides:       bundled(crate(libredox)) = 0.1.3
Provides:       bundled(crate(linux-raw-sys)) = 0.3.8
Provides:       bundled(crate(linux-raw-sys)) = 0.4.14
Provides:       bundled(crate(litrs)) = 0.4.1
Provides:       bundled(crate(lock_api)) = 0.4.12
Provides:       bundled(crate(log)) = 0.4.22
Provides:       bundled(crate(mac-notification-sys)) = 0.6.1
Provides:       bundled(crate(malloc_buf)) = 0.0.6
Provides:       bundled(crate(memchr)) = 2.7.2
Provides:       bundled(crate(memmap2)) = 0.9.4
Provides:       bundled(crate(memoffset)) = 0.7.1
Provides:       bundled(crate(memoffset)) = 0.9.1
Provides:       bundled(crate(metal)) = 0.28.0
Provides:       bundled(crate(mime)) = 0.3.17
Provides:       bundled(crate(miniz_oxide)) = 0.7.3
Provides:       bundled(crate(mio)) = 1.0.1
Provides:       bundled(crate(naga)) = 0.20.0
Provides:       bundled(crate(ndk)) = 0.8.0
Provides:       bundled(crate(ndk-context)) = 0.1.1
Provides:       bundled(crate(ndk-sys)) = 0.5.0+25.2.9519653
Provides:       bundled(crate(nix)) = 0.26.4
Provides:       bundled(crate(nix)) = 0.28.0
Provides:       bundled(crate(nohash-hasher)) = 0.2.0
Provides:       bundled(crate(nu-ansi-term)) = 0.50.1
Provides:       bundled(crate(num-conv)) = 0.1.0
Provides:       bundled(crate(num_enum)) = 0.7.2
Provides:       bundled(crate(num_enum_derive)) = 0.7.2
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(objc)) = 0.2.7
Provides:       bundled(crate(objc2-0.3.0-beta.3.patch)) = leaks.3
Provides:       bundled(crate(objc2)) = 0.4.1
Provides:       bundled(crate(objc2)) = 0.5.2
Provides:       bundled(crate(objc2-app-kit)) = 0.2.2
Provides:       bundled(crate(objc2-core-data)) = 0.2.2
Provides:       bundled(crate(objc2-core-image)) = 0.2.2
Provides:       bundled(crate(objc2-encode-2.0.0)) = pre.2
Provides:       bundled(crate(objc2-encode)) = 3.0.0
Provides:       bundled(crate(objc2-encode)) = 4.0.3
Provides:       bundled(crate(objc2-foundation)) = 0.2.2
Provides:       bundled(crate(objc2-metal)) = 0.2.2
Provides:       bundled(crate(objc2-quartz-core)) = 0.2.2
Provides:       bundled(crate(objc-foundation)) = 0.1.1
Provides:       bundled(crate(objc_id)) = 0.1.1
Provides:       bundled(crate(objc-sys-0.2.0)) = beta.2
Provides:       bundled(crate(objc-sys)) = 0.3.5
Provides:       bundled(crate(object)) = 0.35.0
Provides:       bundled(crate(once_cell)) = 1.19.0
Provides:       bundled(crate(option-ext)) = 0.2.0
Provides:       bundled(crate(orbclient)) = 0.3.47
Provides:       bundled(crate(ordered-stream)) = 0.2.0
Provides:       bundled(crate(owned_ttf_parser)) = 0.21.0
Provides:       bundled(crate(parking)) = 2.2.0
Provides:       bundled(crate(parking_lot)) = 0.12.3
Provides:       bundled(crate(parking_lot_core)) = 0.9.10
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(percent-encoding)) = 2.3.1
Provides:       bundled(crate(pin-project)) = 1.1.5
Provides:       bundled(crate(pin-project-internal)) = 1.1.5
Provides:       bundled(crate(pin-project-lite)) = 0.2.14
Provides:       bundled(crate(pin-utils)) = 0.1.0
Provides:       bundled(crate(piper)) = 0.2.2
Provides:       bundled(crate(pkg-config)) = 0.3.30
Provides:       bundled(crate(png)) = 0.17.13
Provides:       bundled(crate(polling)) = 2.8.0
Provides:       bundled(crate(polling)) = 3.7.0
Provides:       bundled(crate(poll-promise)) = 0.3.0
Provides:       bundled(crate(pollster)) = 0.3.0
Provides:       bundled(crate(powerfmt)) = 0.2.0
Provides:       bundled(crate(ppv-lite86)) = 0.2.17
Provides:       bundled(crate(presser)) = 0.3.1
Provides:       bundled(crate(proc-macro2)) = 1.0.84
Provides:       bundled(crate(proc-macro-crate)) = 1.3.1
Provides:       bundled(crate(proc-macro-crate)) = 3.1.0
Provides:       bundled(crate(profiling)) = 1.0.15
Provides:       bundled(crate(quick-xml)) = 0.31.0
Provides:       bundled(crate(quick-xml)) = 0.36.1
Provides:       bundled(crate(quinn)) = 0.11.2
Provides:       bundled(crate(quinn-proto)) = 0.11.8
Provides:       bundled(crate(quinn-udp)) = 0.5.4
Provides:       bundled(crate(quote)) = 1.0.36
Provides:       bundled(crate(rand)) = 0.8.5
Provides:       bundled(crate(rand_chacha)) = 0.3.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(raw-window-handle)) = 0.5.2
Provides:       bundled(crate(raw-window-handle)) = 0.6.2
Provides:       bundled(crate(redox_syscall)) = 0.3.5
Provides:       bundled(crate(redox_syscall)) = 0.4.1
Provides:       bundled(crate(redox_syscall)) = 0.5.1
Provides:       bundled(crate(redox_users)) = 0.4.5
Provides:       bundled(crate(regex)) = 1.10.4
Provides:       bundled(crate(regex-automata)) = 0.4.6
Provides:       bundled(crate(regex-syntax)) = 0.8.3
Provides:       bundled(crate(renderdoc-sys)) = 1.1.0
Provides:       bundled(crate(reqwest)) = 0.12.5
Provides:       bundled(crate(ring)) = 0.17.8
Provides:       bundled(crate(ron)) = 0.8.1
Provides:       bundled(crate(rustc-demangle)) = 0.1.24
Provides:       bundled(crate(rustc-hash)) = 1.1.0
Provides:       bundled(crate(rustc-hash)) = 2.0.0
Provides:       bundled(crate(rustix)) = 0.37.27
Provides:       bundled(crate(rustix)) = 0.38.34
Provides:       bundled(crate(rustls)) = 0.23.12
Provides:       bundled(crate(rustls-pemfile)) = 2.1.2
Provides:       bundled(crate(rustls-pki-types)) = 1.7.0
Provides:       bundled(crate(rustls-webpki)) = 0.102.6
Provides:       bundled(crate(ryu)) = 1.0.18
Provides:       bundled(crate(same-file)) = 1.0.6
Provides:       bundled(crate(scoped-tls)) = 1.0.1
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(sctk-adwaita)) = 0.8.1
Provides:       bundled(crate(serde)) = 1.0.214
Provides:       bundled(crate(serde_derive)) = 1.0.214
Provides:       bundled(crate(serde_json)) = 1.0.128
Provides:       bundled(crate(serde_repr)) = 0.1.19
Provides:       bundled(crate(serde_urlencoded)) = 0.7.1
Provides:       bundled(crate(sha1)) = 0.10.6
Provides:       bundled(crate(sha1_smol)) = 1.0.1
Provides:       bundled(crate(sha2)) = 0.10.8
Provides:       bundled(crate(signal-hook)) = 0.3.17
Provides:       bundled(crate(signal-hook-mio)) = 0.2.4
Provides:       bundled(crate(signal-hook-registry)) = 1.4.2
Provides:       bundled(crate(simd-adler32)) = 0.3.7
Provides:       bundled(crate(slab)) = 0.4.9
Provides:       bundled(crate(slotmap)) = 1.0.7
Provides:       bundled(crate(smallvec)) = 1.13.2
Provides:       bundled(crate(smithay-client-toolkit)) = 0.18.1
Provides:       bundled(crate(smithay-clipboard)) = 0.7.1
Provides:       bundled(crate(smol_str)) = 0.2.2
Provides:       bundled(crate(socket2)) = 0.4.10
Provides:       bundled(crate(socket2)) = 0.5.7
Provides:       bundled(crate(spin)) = 0.9.8
Provides:       bundled(crate(spirv-0.3.0+sdk)) = 1.3.268.0
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(strict-num)) = 0.1.1
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(subtle)) = 2.5.0
Provides:       bundled(crate(syn)) = 1.0.109
Provides:       bundled(crate(syn)) = 2.0.85
Provides:       bundled(crate(sync_wrapper)) = 1.0.1
Provides:       bundled(crate(tauri-winrt-notification)) = 0.2.1
Provides:       bundled(crate(tempfile)) = 3.10.1
Provides:       bundled(crate(termcolor)) = 1.4.1
Provides:       bundled(crate(thiserror)) = 1.0.61
Provides:       bundled(crate(thiserror-impl)) = 1.0.61
Provides:       bundled(crate(time)) = 0.3.36
Provides:       bundled(crate(time-core)) = 0.1.2
Provides:       bundled(crate(tiny-skia)) = 0.11.4
Provides:       bundled(crate(tiny-skia-path)) = 0.11.4
Provides:       bundled(crate(tinyvec)) = 1.6.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(tokio)) = 1.41.0
Provides:       bundled(crate(tokio-macros)) = 2.4.0
Provides:       bundled(crate(tokio-rustls)) = 0.26.0
Provides:       bundled(crate(toml_datetime)) = 0.6.6
Provides:       bundled(crate(toml_edit)) = 0.19.15
Provides:       bundled(crate(toml_edit)) = 0.21.1
Provides:       bundled(crate(tower)) = 0.4.13
Provides:       bundled(crate(tower-layer)) = 0.3.2
Provides:       bundled(crate(tower-service)) = 0.3.2
Provides:       bundled(crate(tracing)) = 0.1.40
Provides:       bundled(crate(tracing-attributes)) = 0.1.27
Provides:       bundled(crate(tracing-core)) = 0.1.32
Provides:       bundled(crate(try-lock)) = 0.2.5
Provides:       bundled(crate(ttf-parser)) = 0.21.1
Provides:       bundled(crate(type-map)) = 0.5.0
Provides:       bundled(crate(typenum)) = 1.17.0
Provides:       bundled(crate(uds_windows)) = 1.1.0
Provides:       bundled(crate(unicode-bidi)) = 0.3.15
Provides:       bundled(crate(unicode-ident)) = 1.0.12
Provides:       bundled(crate(unicode-normalization)) = 0.1.23
Provides:       bundled(crate(unicode-segmentation)) = 1.11.0
Provides:       bundled(crate(unicode-width)) = 0.1.12
Provides:       bundled(crate(unicode-xid)) = 0.2.4
Provides:       bundled(crate(untrusted)) = 0.9.0
Provides:       bundled(crate(url)) = 2.5.0
Provides:       bundled(crate(urlencoding)) = 2.1.3
Provides:       bundled(crate(utf8parse)) = 0.2.1
Provides:       bundled(crate(version_check)) = 0.9.4
Provides:       bundled(crate(waker-fn)) = 1.2.0
Provides:       bundled(crate(walkdir)) = 2.5.0
Provides:       bundled(crate(want)) = 0.3.1
Provides:       bundled(crate(wasi-0.11.0+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasm-bindgen)) = 0.2.92
Provides:       bundled(crate(wasm-bindgen-backend)) = 0.2.92
Provides:       bundled(crate(wasm-bindgen-futures)) = 0.4.42
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.92
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.92
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.92
Provides:       bundled(crate(webbrowser)) = 1.0.1
Provides:       bundled(crate(webpki-roots)) = 0.26.1
Provides:       bundled(crate(web-sys)) = 0.3.69
Provides:       bundled(crate(web-time)) = 0.2.4
Provides:       bundled(crate(wgpu)) = 0.20.1
Provides:       bundled(crate(wgpu-core)) = 0.21.1
Provides:       bundled(crate(wgpu-hal)) = 0.21.1
Provides:       bundled(crate(wgpu-types)) = 0.20.0
Provides:       bundled(crate(widestring)) = 1.1.0
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.8
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows)) = 0.48.0
Provides:       bundled(crate(windows)) = 0.52.0
Provides:       bundled(crate(windows)) = 0.56.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.5
Provides:       bundled(crate(windows-core)) = 0.52.0
Provides:       bundled(crate(windows-core)) = 0.56.0
Provides:       bundled(crate(windows_i686_gnu)) = 0.42.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.48.5
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.5
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.42.2
Provides:       bundled(crate(windows_i686_msvc)) = 0.48.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.5
Provides:       bundled(crate(windows-implement)) = 0.48.0
Provides:       bundled(crate(windows-implement)) = 0.56.0
Provides:       bundled(crate(windows-interface)) = 0.48.0
Provides:       bundled(crate(windows-interface)) = 0.56.0
Provides:       bundled(crate(windows-result)) = 0.1.1
Provides:       bundled(crate(windows-sys)) = 0.45.0
Provides:       bundled(crate(windows-sys)) = 0.48.0
Provides:       bundled(crate(windows-sys)) = 0.52.0
Provides:       bundled(crate(windows-targets)) = 0.42.2
Provides:       bundled(crate(windows-targets)) = 0.48.5
Provides:       bundled(crate(windows-targets)) = 0.52.5
Provides:       bundled(crate(windows-version)) = 0.1.1
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.5
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.5
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.5
Provides:       bundled(crate(winit)) = 0.29.15
Provides:       bundled(crate(winnow)) = 0.5.40
Provides:       bundled(crate(winreg)) = 0.52.0
Provides:       bundled(crate(xml-rs)) = 0.8.20
Provides:       bundled(crate(zbus)) = 3.15.2
Provides:       bundled(crate(zbus)) = 4.2.2
Provides:       bundled(crate(zbus_macros)) = 3.15.2
Provides:       bundled(crate(zbus_macros)) = 4.2.2
Provides:       bundled(crate(zbus_names)) = 2.6.1
Provides:       bundled(crate(zbus_names)) = 3.0.0
Provides:       bundled(crate(zerocopy)) = 0.7.34
Provides:       bundled(crate(zerocopy-derive)) = 0.7.34
Provides:       bundled(crate(zeroize)) = 1.8.1
Provides:       bundled(crate(zvariant)) = 3.15.2
Provides:       bundled(crate(zvariant)) = 4.1.1
Provides:       bundled(crate(zvariant_derive)) = 3.15.2
Provides:       bundled(crate(zvariant_derive)) = 4.1.1
Provides:       bundled(crate(zvariant_utils)) = 1.0.1
Provides:       bundled(crate(zvariant_utils)) = 2.0.0
}
%_vendor_provides
Provides:       bundled(crate(crossterm)) = 0.28.1
Provides:       bundled(crate(crossterm_winapi)) = 0.9.1
%endif
%endif


%description
%{name} is a simple tool to grab updates for PS3 games.


%package egui
Summary:        Simple GUI tool to grab updates for PS3 games
Requires:       gnome-icon-theme
%if %{with vendor}
%_vendor_provides
Provides:       bundled(crate(ecolor)) = 0.28.1
Provides:       bundled(crate(egui)) = 0.28.1
Provides:       bundled(crate(egui_glow)) = 0.28.1
Provides:       bundled(crate(egui-notify)) = 0.15.0
Provides:       bundled(crate(egui-wgpu)) = 0.28.1
Provides:       bundled(crate(egui-winit)) = 0.28.1
Provides:       bundled(crate(epaint)) = 0.28.1
Provides:       bundled(crate(notify-rust)) = 4.11.3
Provides:       bundled(crate(rfd)) = 0.14.1
Provides:       bundled(crate(wayland-backend)) = 0.3.3
Provides:       bundled(crate(wayland-client)) = 0.31.2
Provides:       bundled(crate(wayland-csd-frame)) = 0.3.0
Provides:       bundled(crate(wayland-cursor)) = 0.31.1
Provides:       bundled(crate(wayland-protocols)) = 0.31.2
Provides:       bundled(crate(wayland-protocols-plasma)) = 0.2.0
Provides:       bundled(crate(wayland-protocols-wlr)) = 0.2.0
Provides:       bundled(crate(wayland-scanner)) = 0.31.1
Provides:       bundled(crate(wayland-sys)) = 0.31.1
Provides:       bundled(crate(x11-clipboard)) = 0.9.2
Provides:       bundled(crate(x11-dl)) = 2.21.0
Provides:       bundled(crate(x11rb)) = 0.13.1
Provides:       bundled(crate(x11rb-protocol)) = 0.13.1
Provides:       bundled(crate(xcursor)) = 0.3.5
Provides:       bundled(crate(xdg-home)) = 1.1.0
Provides:       bundled(crate(xkbcommon-dl)) = 0.4.2
Provides:       bundled(crate(xkeysym)) = 0.2.0
%endif

%description egui
%{name}-egui is a GUI simple tool to grab updates for PS3 games.


%prep
%if %{with bin}
%autosetup -c -T
unzip -d cli %{S:0}
unzip -d egui %{S:1}

cp -p %{S:2} %{S:3} %{S:4} .
%else
%autosetup -p1 %{?with_vendor:-a1}

%if %{with vendor}
%cargo_prep -v vendor
%endif

mv resources/OFL.txt .
rm -rf resources
sed \
  -e '/NotoSansJP-Regular.otf/s|../../resources/|%{_datadir}/fonts/google-noto-sans-jp-fonts/|g' \
  -e '/NotoSans-Regular.ttf/s|../../resources/|%{_datadir}/fonts/google-noto/|g' \
  -i  src/egui/mod.rs

%generate_buildrequires
%if %{with vendor}
%cargo_vendor_manifest
%else
%cargo_generate_buildrequires
%endif
%endif

cat > %{name}.desktop <<'EOF'
[Desktop Entry]
Name=%{name}-egui
Comment=Grab updates for PS3 games
Exec=%{name}-egui
Icon=applications-games
Terminal=false
Type=Application
Categories=Network;
EOF


%build
%if %{without bin}
mkdir cli egui
%cargo_build -f cli
mv target/release/%{name} cli/
rm -rf target/release/*
%cargo_build -f egui
mv target/release/%{name} egui/
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%endif


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 cli/%{name} %{buildroot}%{_bindir}/%{name}
install -pm0755 egui/%{name} %{buildroot}%{_bindir}/%{name}-egui

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%files egui
%license LICENSE OFL.txt
%doc README.md
%{_bindir}/%{name}-egui
%{_datadir}/applications/%{name}.desktop


%changelog
* Fri Nov 15 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.2-1
- 0.5.2
- Source support, with vendored tarball switch

* Fri Sep 20 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.0-1
- 0.5.0

* Sun May 05 2024 Phantom X <megaphantomx at hotmail dot com> - 0.3.7-1
- 0.3.7

* Mon May 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.5-1
- 0.3.5

* Tue May 02 2023 Phantom X <megaphantomx at hotmail dot com> - 0.3.4-1
- 0.3.4

* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2.2-1
- 0.2.2

* Thu Mar 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1.1-1
- Initial spec

