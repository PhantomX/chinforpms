# prevent library files from being installed
%global cargo_install_lib 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash 377a44a1df9ce598b8bbe07c67adb670

%global appname io.github.umio_yasuno.%{name}

Name:           amdgpu_top
Version:        0.11.0
Release:        1%{?dist}
Summary:        Tool to display AMDGPU usage

License:        MIT
URL:            https://github.com/Umio-Yasuno/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# cargo vendor-filterer --versioned-dirs --platform=x86_64-unknown-linux-gnu && tar --numeric-owner -cvJf ../%%{name}-%%{version}-vendor.tar.xz vendor/
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

Patch0:         0001-Remove-git-requirement.patch

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdrm_amdgpu)

Requires:       hicolor-icon-theme

%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(ab_glyph)) = 0.2.31
Provides:       bundled(crate(ab_glyph_rasterizer)) = 0.1.10
Provides:       bundled(crate(accesskit)) = 0.19.0
Provides:       bundled(crate(adler2)) = 2.0.1
Provides:       bundled(crate(ahash)) = 0.8.12
Provides:       bundled(crate(android-activity)) = 0.6.0
Provides:       bundled(crate(android-properties)) = 0.2.2
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(arboard)) = 3.6.1
Provides:       bundled(crate(arc-swap)) = 1.7.1
Provides:       bundled(crate(arrayvec)) = 0.7.6
Provides:       bundled(crate(ash)) = 0.38.0+1.3.281
Provides:       bundled(crate(as-raw-xcb-connection)) = 1.0.1
Provides:       bundled(crate(atomic-waker)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.5.0
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(basic-toml)) = 0.1.10
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.9.3
Provides:       bundled(crate(bit-set)) = 0.8.0
Provides:       bundled(crate(bit-vec)) = 0.8.0
Provides:       bundled(crate(block2)) = 0.5.1
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(bstr)) = 1.12.0
Provides:       bundled(crate(bumpalo)) = 3.19.0
Provides:       bundled(crate(bytemuck)) = 1.23.2
Provides:       bundled(crate(bytemuck_derive)) = 1.10.1
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(byteorder-lite)) = 0.1.0
Provides:       bundled(crate(bytes)) = 1.10.1
Provides:       bundled(crate(calloop)) = 0.13.0
Provides:       bundled(crate(calloop-wayland-source)) = 0.3.0
Provides:       bundled(crate(castaway)) = 0.2.4
Provides:       bundled(crate(cc)) = 1.2.35
Provides:       bundled(crate(cesu8)) = 1.1.0
Provides:       bundled(crate(cfg_aliases)) = 0.2.1
Provides:       bundled(crate(cfg-if)) = 1.0.3
Provides:       bundled(crate(cgl)) = 0.3.2
Provides:       bundled(crate(clipboard-win)) = 5.4.1
Provides:       bundled(crate(clru)) = 0.6.2
Provides:       bundled(crate(codespan-reporting)) = 0.12.0
Provides:       bundled(crate(combine)) = 4.6.7
Provides:       bundled(crate(compact_str)) = 0.8.1
Provides:       bundled(crate(concurrent-queue)) = 2.5.0
Provides:       bundled(crate(core-foundation)) = 0.10.1
Provides:       bundled(crate(core-foundation)) = 0.9.4
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(core-graphics)) = 0.23.2
Provides:       bundled(crate(core-graphics-types)) = 0.1.3
Provides:       bundled(crate(cpufeatures)) = 0.2.17
Provides:       bundled(crate(crc32fast)) = 1.5.0
Provides:       bundled(crate(crossbeam-channel)) = 0.5.15
Provides:       bundled(crate(crossbeam-utils)) = 0.8.21
Provides:       bundled(crate(crossterm)) = 0.28.1
Provides:       bundled(crate(crossterm_winapi)) = 0.9.1
Provides:       bundled(crate(crunchy)) = 0.2.4
Provides:       bundled(crate(crypto-common)) = 0.1.6
Provides:       bundled(crate(cursive)) = 0.21.1
Provides:       bundled(crate(cursive_core)) = 0.4.6
Provides:       bundled(crate(cursive-macros)) = 0.1.0
Provides:       bundled(crate(cursor-icon)) = 1.2.0
Provides:       bundled(crate(darling)) = 0.21.3
Provides:       bundled(crate(darling_core)) = 0.21.3
Provides:       bundled(crate(darling_macro)) = 0.21.3
Provides:       bundled(crate(deranged)) = 0.5.3
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(dispatch)) = 0.2.0
Provides:       bundled(crate(dispatch2)) = 0.3.0
Provides:       bundled(crate(displaydoc)) = 0.2.5
Provides:       bundled(crate(dlib)) = 0.5.2
Provides:       bundled(crate(document-features)) = 0.2.11
Provides:       bundled(crate(downcast-rs)) = 1.2.1
Provides:       bundled(crate(dpi)) = 0.1.2
Provides:       bundled(crate(dunce)) = 1.0.5
Provides:       bundled(crate(ecolor)) = 0.32.1
Provides:       bundled(crate(eframe)) = 0.32.1
Provides:       bundled(crate(egui)) = 0.32.1
Provides:       bundled(crate(egui_glow)) = 0.32.1
Provides:       bundled(crate(egui_plot)) = 0.33.0
Provides:       bundled(crate(egui-wgpu)) = 0.32.1
Provides:       bundled(crate(egui-winit)) = 0.32.1
Provides:       bundled(crate(emath)) = 0.32.1
Provides:       bundled(crate(enum-map)) = 2.7.3
Provides:       bundled(crate(enum-map-derive)) = 0.17.0
Provides:       bundled(crate(enumn)) = 0.1.14
Provides:       bundled(crate(enumset)) = 1.1.10
Provides:       bundled(crate(enumset_derive)) = 0.14.0
Provides:       bundled(crate(epaint)) = 0.32.1
Provides:       bundled(crate(epaint_default_fonts)) = 0.32.1
Provides:       bundled(crate(equivalent)) = 1.0.2
Provides:       bundled(crate(errno)) = 0.3.13
Provides:       bundled(crate(error-code)) = 3.3.2
Provides:       bundled(crate(faster-hex)) = 0.10.0
Provides:       bundled(crate(fastrand)) = 2.3.0
Provides:       bundled(crate(fax)) = 0.2.6
Provides:       bundled(crate(fax_derive)) = 0.2.0
Provides:       bundled(crate(fdeflate)) = 0.3.7
Provides:       bundled(crate(find-crate)) = 0.6.3
Provides:       bundled(crate(find-msvc-tools)) = 0.1.0
Provides:       bundled(crate(flate2)) = 1.1.2
Provides:       bundled(crate(fluent)) = 0.17.0
Provides:       bundled(crate(fluent-bundle)) = 0.16.0
Provides:       bundled(crate(fluent-langneg)) = 0.13.0
Provides:       bundled(crate(fluent-syntax)) = 0.12.0
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foldhash)) = 0.1.5
Provides:       bundled(crate(foreign-types)) = 0.5.0
Provides:       bundled(crate(foreign-types-macros)) = 0.2.3
Provides:       bundled(crate(foreign-types-shared)) = 0.3.1
Provides:       bundled(crate(form_urlencoded)) = 1.2.2
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(gethostname)) = 1.0.2
Provides:       bundled(crate(getrandom)) = 0.3.3
Provides:       bundled(crate(gix)) = 0.73.0
Provides:       bundled(crate(gix-actor)) = 0.35.4
Provides:       bundled(crate(gix-chunk)) = 0.4.11
Provides:       bundled(crate(gix-command)) = 0.6.2
Provides:       bundled(crate(gix-commitgraph)) = 0.29.0
Provides:       bundled(crate(gix-config)) = 0.46.0
Provides:       bundled(crate(gix-config-value)) = 0.15.1
Provides:       bundled(crate(gix-date)) = 0.10.5
Provides:       bundled(crate(gix-diff)) = 0.53.0
Provides:       bundled(crate(gix-discover)) = 0.41.0
Provides:       bundled(crate(gix-features)) = 0.43.1
Provides:       bundled(crate(gix-fs)) = 0.16.1
Provides:       bundled(crate(gix-glob)) = 0.21.0
Provides:       bundled(crate(gix-hash)) = 0.19.0
Provides:       bundled(crate(gix-hashtable)) = 0.9.0
Provides:       bundled(crate(gix-lock)) = 18.0.0
Provides:       bundled(crate(gix-object)) = 0.50.2
Provides:       bundled(crate(gix-odb)) = 0.70.0
Provides:       bundled(crate(gix-pack)) = 0.60.0
Provides:       bundled(crate(gix-packetline)) = 0.19.1
Provides:       bundled(crate(gix-path)) = 0.10.20
Provides:       bundled(crate(gix-protocol)) = 0.51.0
Provides:       bundled(crate(gix-quote)) = 0.6.0
Provides:       bundled(crate(gix-ref)) = 0.53.1
Provides:       bundled(crate(gix-refspec)) = 0.31.0
Provides:       bundled(crate(gix-revision)) = 0.35.0
Provides:       bundled(crate(gix-revwalk)) = 0.21.0
Provides:       bundled(crate(gix-sec)) = 0.12.0
Provides:       bundled(crate(gix-shallow)) = 0.5.0
Provides:       bundled(crate(gix-tempfile)) = 18.0.0
Provides:       bundled(crate(gix-trace)) = 0.1.13
Provides:       bundled(crate(gix-transport)) = 0.48.0
Provides:       bundled(crate(gix-traverse)) = 0.47.0
Provides:       bundled(crate(gix-url)) = 0.32.0
Provides:       bundled(crate(gix-utils)) = 0.3.0
Provides:       bundled(crate(gix-validate)) = 0.10.0
Provides:       bundled(crate(gl_generator)) = 0.14.0
Provides:       bundled(crate(glow)) = 0.16.0
Provides:       bundled(crate(glutin)) = 0.32.3
Provides:       bundled(crate(glutin_egl_sys)) = 0.7.1
Provides:       bundled(crate(glutin_glx_sys)) = 0.6.1
Provides:       bundled(crate(glutin_wgl_sys)) = 0.6.1
Provides:       bundled(crate(glutin-winit)) = 0.5.0
Provides:       bundled(crate(gpu-alloc)) = 0.6.0
Provides:       bundled(crate(gpu-alloc-types)) = 0.3.0
Provides:       bundled(crate(gpu-descriptor)) = 0.3.2
Provides:       bundled(crate(gpu-descriptor-types)) = 0.2.0
Provides:       bundled(crate(half)) = 2.6.0
Provides:       bundled(crate(hash32)) = 0.3.1
Provides:       bundled(crate(hashbrown)) = 0.15.5
Provides:       bundled(crate(heapless)) = 0.8.0
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit-abi)) = 0.5.2
Provides:       bundled(crate(hexf-parse)) = 0.2.1
Provides:       bundled(crate(home)) = 0.5.11
Provides:       bundled(crate(i18n-config)) = 0.4.8
Provides:       bundled(crate(i18n-embed)) = 0.16.0
Provides:       bundled(crate(i18n-embed-fl)) = 0.10.0
Provides:       bundled(crate(i18n-embed-impl)) = 0.8.4
Provides:       bundled(crate(icu_collections)) = 2.0.0
Provides:       bundled(crate(icu_locale_core)) = 2.0.0
Provides:       bundled(crate(icu_normalizer)) = 2.0.0
Provides:       bundled(crate(icu_normalizer_data)) = 2.0.0
Provides:       bundled(crate(icu_properties)) = 2.0.1
Provides:       bundled(crate(icu_properties_data)) = 2.0.1
Provides:       bundled(crate(icu_provider)) = 2.0.0
Provides:       bundled(crate(ident_case)) = 1.0.1
Provides:       bundled(crate(idna)) = 1.1.0
Provides:       bundled(crate(idna_adapter)) = 1.2.1
Provides:       bundled(crate(image)) = 0.25.7
Provides:       bundled(crate(indexmap)) = 2.11.0
Provides:       bundled(crate(intl-memoizer)) = 0.5.3
Provides:       bundled(crate(intl_pluralrules)) = 7.0.2
Provides:       bundled(crate(itoa)) = 1.0.15
Provides:       bundled(crate(jiff)) = 0.2.15
Provides:       bundled(crate(jiff-static)) = 0.2.15
Provides:       bundled(crate(jiff-tzdb)) = 0.1.4
Provides:       bundled(crate(jiff-tzdb-platform)) = 0.1.3
Provides:       bundled(crate(jni)) = 0.21.1
Provides:       bundled(crate(jni-sys)) = 0.3.0
Provides:       bundled(crate(jobserver)) = 0.1.34
Provides:       bundled(crate(js-sys)) = 0.3.77
Provides:       bundled(crate(khronos_api)) = 3.1.0
Provides:       bundled(crate(khronos-egl)) = 6.0.0
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(libc)) = 0.2.175
Provides:       bundled(crate(libdrm_amdgpu_sys)) = 0.8.8
Provides:       bundled(crate(libloading)) = 0.8.8
Provides:       bundled(crate(libm)) = 0.2.15
Provides:       bundled(crate(libredox)) = 0.1.9
Provides:       bundled(crate(libz-rs-sys)) = 0.5.1
Provides:       bundled(crate(linux-raw-sys)) = 0.4.15
Provides:       bundled(crate(linux-raw-sys)) = 0.9.4
Provides:       bundled(crate(litemap)) = 0.8.0
Provides:       bundled(crate(litrs)) = 0.4.2
Provides:       bundled(crate(lock_api)) = 0.4.13
Provides:       bundled(crate(log)) = 0.4.27
Provides:       bundled(crate(malloc_buf)) = 0.0.6
Provides:       bundled(crate(maybe-async)) = 0.2.10
Provides:       bundled(crate(memchr)) = 2.7.5
Provides:       bundled(crate(memmap2)) = 0.9.8
Provides:       bundled(crate(memoffset)) = 0.9.1
Provides:       bundled(crate(miniz_oxide)) = 0.8.9
Provides:       bundled(crate(mio)) = 1.0.4
Provides:       bundled(crate(moxcms)) = 0.7.5
Provides:       bundled(crate(naga)) = 25.0.1
Provides:       bundled(crate(ndk)) = 0.9.0
Provides:       bundled(crate(ndk-context)) = 0.1.1
Provides:       bundled(crate(ndk-sys)) = 0.5.0+25.2.9519653
Provides:       bundled(crate(ndk-sys)) = 0.6.0+11769913
Provides:       bundled(crate(nix)) = 0.30.1
Provides:       bundled(crate(nohash-hasher)) = 0.2.0
Provides:       bundled(crate(num)) = 0.4.3
Provides:       bundled(crate(num-complex)) = 0.4.6
Provides:       bundled(crate(num-conv)) = 0.1.0
Provides:       bundled(crate(num_enum)) = 0.7.4
Provides:       bundled(crate(num_enum_derive)) = 0.7.4
Provides:       bundled(crate(num-integer)) = 0.1.46
Provides:       bundled(crate(num-iter)) = 0.1.45
Provides:       bundled(crate(num-rational)) = 0.4.2
Provides:       bundled(crate(num_threads)) = 0.1.7
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(objc)) = 0.2.7
Provides:       bundled(crate(objc2)) = 0.5.2
Provides:       bundled(crate(objc2)) = 0.6.2
Provides:       bundled(crate(objc2-app-kit)) = 0.2.2
Provides:       bundled(crate(objc2-app-kit)) = 0.3.1
Provides:       bundled(crate(objc2-cloud-kit)) = 0.2.2
Provides:       bundled(crate(objc2-contacts)) = 0.2.2
Provides:       bundled(crate(objc2-core-data)) = 0.2.2
Provides:       bundled(crate(objc2-core-foundation)) = 0.3.1
Provides:       bundled(crate(objc2-core-graphics)) = 0.3.1
Provides:       bundled(crate(objc2-core-image)) = 0.2.2
Provides:       bundled(crate(objc2-core-location)) = 0.2.2
Provides:       bundled(crate(objc2-encode)) = 4.1.0
Provides:       bundled(crate(objc2-foundation)) = 0.2.2
Provides:       bundled(crate(objc2-foundation)) = 0.3.1
Provides:       bundled(crate(objc2-io-surface)) = 0.3.1
Provides:       bundled(crate(objc2-link-presentation)) = 0.2.2
Provides:       bundled(crate(objc2-metal)) = 0.2.2
Provides:       bundled(crate(objc2-quartz-core)) = 0.2.2
Provides:       bundled(crate(objc2-symbols)) = 0.2.2
Provides:       bundled(crate(objc2-ui-kit)) = 0.2.2
Provides:       bundled(crate(objc2-uniform-type-identifiers)) = 0.2.2
Provides:       bundled(crate(objc2-user-notifications)) = 0.2.2
Provides:       bundled(crate(objc-sys)) = 0.3.5
Provides:       bundled(crate(once_cell)) = 1.21.3
Provides:       bundled(crate(orbclient)) = 0.3.48
Provides:       bundled(crate(ordered-float)) = 4.6.0
Provides:       bundled(crate(owned_ttf_parser)) = 0.25.1
Provides:       bundled(crate(parking_lot)) = 0.12.4
Provides:       bundled(crate(parking_lot_core)) = 0.9.11
Provides:       bundled(crate(percent-encoding)) = 2.3.2
Provides:       bundled(crate(pin-project)) = 1.1.10
Provides:       bundled(crate(pin-project-internal)) = 1.1.10
Provides:       bundled(crate(pin-project-lite)) = 0.2.16
Provides:       bundled(crate(pkg-config)) = 0.3.32
Provides:       bundled(crate(png)) = 0.18.0
Provides:       bundled(crate(polling)) = 3.10.0
Provides:       bundled(crate(pollster)) = 0.4.0
Provides:       bundled(crate(portable-atomic)) = 1.11.1
Provides:       bundled(crate(portable-atomic-util)) = 0.2.4
Provides:       bundled(crate(potential_utf)) = 0.1.3
Provides:       bundled(crate(powerfmt)) = 0.2.0
Provides:       bundled(crate(proc-macro2)) = 1.0.101
Provides:       bundled(crate(proc-macro-crate)) = 3.3.0
Provides:       bundled(crate(proc-macro-error2)) = 2.0.1
Provides:       bundled(crate(proc-macro-error-attr2)) = 2.0.0
Provides:       bundled(crate(prodash)) = 30.0.1
Provides:       bundled(crate(profiling)) = 1.0.17
Provides:       bundled(crate(pxfm)) = 0.1.20
Provides:       bundled(crate(quick-error)) = 2.0.1
Provides:       bundled(crate(quick-xml)) = 0.37.5
Provides:       bundled(crate(quote)) = 1.0.40
Provides:       bundled(crate(raw-window-handle)) = 0.6.2
Provides:       bundled(crate(redox_syscall)) = 0.4.1
Provides:       bundled(crate(redox_syscall)) = 0.5.17
Provides:       bundled(crate(r-efi)) = 5.3.0
Provides:       bundled(crate(regex-automata)) = 0.4.10
Provides:       bundled(crate(renderdoc-sys)) = 1.1.0
Provides:       bundled(crate(ron)) = 0.10.1
Provides:       bundled(crate(rustc-hash)) = 1.1.0
Provides:       bundled(crate(rustc-hash)) = 2.1.1
Provides:       bundled(crate(rust-embed)) = 8.7.2
Provides:       bundled(crate(rust-embed-impl)) = 8.7.2
Provides:       bundled(crate(rust-embed-utils)) = 8.7.2
Provides:       bundled(crate(rustix)) = 0.38.44
Provides:       bundled(crate(rustix)) = 1.0.8
Provides:       bundled(crate(rustversion)) = 1.0.22
Provides:       bundled(crate(ryu)) = 1.0.20
Provides:       bundled(crate(same-file)) = 1.0.6
Provides:       bundled(crate(scoped-tls)) = 1.0.1
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(self_cell)) = 1.2.0
Provides:       bundled(crate(serde)) = 1.0.219
Provides:       bundled(crate(serde_derive)) = 1.0.219
Provides:       bundled(crate(serde_json)) = 1.0.143
Provides:       bundled(crate(sha1)) = 0.10.6
Provides:       bundled(crate(sha1-checked)) = 0.10.0
Provides:       bundled(crate(sha2)) = 0.10.9
Provides:       bundled(crate(shell-words)) = 1.1.0
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(signal-hook)) = 0.3.18
Provides:       bundled(crate(signal-hook-mio)) = 0.2.4
Provides:       bundled(crate(signal-hook-registry)) = 1.4.6
Provides:       bundled(crate(simd-adler32)) = 0.3.7
Provides:       bundled(crate(slab)) = 0.4.11
Provides:       bundled(crate(slotmap)) = 1.0.7
Provides:       bundled(crate(smallvec)) = 1.15.1
Provides:       bundled(crate(smithay-client-toolkit)) = 0.19.2
Provides:       bundled(crate(smithay-clipboard)) = 0.7.2
Provides:       bundled(crate(smol_str)) = 0.2.2
Provides:       bundled(crate(spirv-0.3.0+sdk)) = 1.3.268.0
Provides:       bundled(crate(stable_deref_trait)) = 1.2.0
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(strum)) = 0.26.3
Provides:       bundled(crate(strum_macros)) = 0.26.4
Provides:       bundled(crate(syn)) = 2.0.106
Provides:       bundled(crate(synstructure)) = 0.13.2
Provides:       bundled(crate(sys-locale)) = 0.3.2
Provides:       bundled(crate(tempfile)) = 3.21.0
Provides:       bundled(crate(termcolor)) = 1.4.1
Provides:       bundled(crate(termsize)) = 0.1.9
Provides:       bundled(crate(thiserror)) = 1.0.69
Provides:       bundled(crate(thiserror)) = 2.0.16
Provides:       bundled(crate(thiserror-impl)) = 1.0.69
Provides:       bundled(crate(thiserror-impl)) = 2.0.16
Provides:       bundled(crate(tiff)) = 0.10.3
Provides:       bundled(crate(time)) = 0.3.42
Provides:       bundled(crate(time-core)) = 0.1.5
Provides:       bundled(crate(time-macros)) = 0.2.23
Provides:       bundled(crate(tinystr)) = 0.8.1
Provides:       bundled(crate(tinyvec)) = 1.10.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(toml)) = 0.5.11
Provides:       bundled(crate(toml_datetime)) = 0.6.11
Provides:       bundled(crate(toml_edit)) = 0.22.27
Provides:       bundled(crate(tracing)) = 0.1.41
Provides:       bundled(crate(tracing-core)) = 0.1.34
Provides:       bundled(crate(ttf-parser)) = 0.25.1
Provides:       bundled(crate(type-map)) = 0.5.1
Provides:       bundled(crate(typenum)) = 1.18.0
Provides:       bundled(crate(unic-langid)) = 0.9.6
Provides:       bundled(crate(unic-langid-impl)) = 0.9.6
Provides:       bundled(crate(unicode-bom)) = 2.0.3
Provides:       bundled(crate(unicode-ident)) = 1.0.18
Provides:       bundled(crate(unicode-normalization)) = 0.1.24
Provides:       bundled(crate(unicode-segmentation)) = 1.12.0
Provides:       bundled(crate(unicode-width)) = 0.1.14
Provides:       bundled(crate(unicode-width)) = 0.2.1
Provides:       bundled(crate(url)) = 2.5.7
Provides:       bundled(crate(utf8_iter)) = 1.0.4
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(walkdir)) = 2.5.0
Provides:       bundled(crate(wasi-0.11.1+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasi-0.14.3+wasi)) = 0.2.4
Provides:       bundled(crate(wasm-bindgen)) = 0.2.100
Provides:       bundled(crate(wasm-bindgen-backend)) = 0.2.100
Provides:       bundled(crate(wasm-bindgen-futures)) = 0.4.50
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.100
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.100
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.100
Provides:       bundled(crate(wayland-backend)) = 0.3.11
Provides:       bundled(crate(wayland-client)) = 0.31.11
Provides:       bundled(crate(wayland-csd-frame)) = 0.3.0
Provides:       bundled(crate(wayland-cursor)) = 0.31.11
Provides:       bundled(crate(wayland-protocols)) = 0.32.9
Provides:       bundled(crate(wayland-protocols-plasma)) = 0.3.9
Provides:       bundled(crate(wayland-protocols-wlr)) = 0.3.9
Provides:       bundled(crate(wayland-scanner)) = 0.31.7
Provides:       bundled(crate(wayland-sys)) = 0.31.7
Provides:       bundled(crate(webbrowser)) = 1.0.5
Provides:       bundled(crate(web-sys)) = 0.3.77
Provides:       bundled(crate(web-time)) = 1.1.0
Provides:       bundled(crate(weezl)) = 0.1.10
Provides:       bundled(crate(wgpu)) = 25.0.2
Provides:       bundled(crate(wgpu-core)) = 25.0.2
Provides:       bundled(crate(wgpu-core-deps-emscripten)) = 25.0.0
Provides:       bundled(crate(wgpu-core-deps-windows-linux-android)) = 25.0.0
Provides:       bundled(crate(wgpu-hal)) = 25.0.2
Provides:       bundled(crate(wgpu-types)) = 25.0.0
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.10
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows)) = 0.58.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.53.0
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.53.0
Provides:       bundled(crate(windows-core)) = 0.58.0
Provides:       bundled(crate(windows_i686_gnu)) = 0.42.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnu)) = 0.53.0
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.53.0
Provides:       bundled(crate(windows_i686_msvc)) = 0.42.2
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.53.0
Provides:       bundled(crate(windows-implement)) = 0.58.0
Provides:       bundled(crate(windows-interface)) = 0.58.0
Provides:       bundled(crate(windows-link)) = 0.1.3
Provides:       bundled(crate(windows-result)) = 0.2.0
Provides:       bundled(crate(windows-strings)) = 0.1.0
Provides:       bundled(crate(windows-sys)) = 0.45.0
Provides:       bundled(crate(windows-sys)) = 0.52.0
Provides:       bundled(crate(windows-sys)) = 0.59.0
Provides:       bundled(crate(windows-sys)) = 0.60.2
Provides:       bundled(crate(windows-targets)) = 0.42.2
Provides:       bundled(crate(windows-targets)) = 0.52.6
Provides:       bundled(crate(windows-targets)) = 0.53.3
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.53.0
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.53.0
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.53.0
Provides:       bundled(crate(winit)) = 0.30.12
Provides:       bundled(crate(winnow)) = 0.7.13
Provides:       bundled(crate(wit-bindgen)) = 0.45.0
Provides:       bundled(crate(writeable)) = 0.6.1
Provides:       bundled(crate(x11-dl)) = 2.21.0
Provides:       bundled(crate(x11rb)) = 0.13.2
Provides:       bundled(crate(x11rb-protocol)) = 0.13.2
Provides:       bundled(crate(xcursor)) = 0.3.10
Provides:       bundled(crate(xi-unicode)) = 0.3.0
Provides:       bundled(crate(xkbcommon-dl)) = 0.4.2
Provides:       bundled(crate(xkeysym)) = 0.2.1
Provides:       bundled(crate(xml-rs)) = 0.8.27
Provides:       bundled(crate(yoke)) = 0.8.0
Provides:       bundled(crate(yoke-derive)) = 0.8.0
Provides:       bundled(crate(zerocopy)) = 0.8.26
Provides:       bundled(crate(zerocopy-derive)) = 0.8.26
Provides:       bundled(crate(zerofrom)) = 0.1.6
Provides:       bundled(crate(zerofrom-derive)) = 0.1.6
Provides:       bundled(crate(zerotrie)) = 0.2.2
Provides:       bundled(crate(zerovec)) = 0.11.4
Provides:       bundled(crate(zerovec-derive)) = 0.11.1
Provides:       bundled(crate(zlib-rs)) = 0.5.1
Provides:       bundled(crate(zune-core)) = 0.4.12
Provides:       bundled(crate(zune-jpeg)) = 0.4.20
%endif


%description
%{name} is a tool that displays information gathered from performance
counters (GRBM, GRBM2), sensors, fdinfo, gpu_metrics and AMDGPU driver.


%prep
%autosetup -p1 -n %{name}-%{version} %{?with_vendor:-a1}

sed -e 's|, "git_version"||g' -i Cargo.toml

%if %{with vendor}
%cargo_prep -v vendor
%else
%generate_buildrequires
%cargo_generate_buildrequires
%endif


%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%if %{with vendor}
%{cargo_vendor_manifest}
%endif


%install
%cargo_install

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  assets/%{name}.desktop
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  assets/%{name}-tui.desktop

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 docs/%{name}.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 assets/%{appname}.metainfo.xml %{buildroot}%{_metainfodir}/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-tui.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-tui.desktop
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Thu Dec 04 2025 Phantom X <megaphantomx at hotmail dot com> - 0.11.0-1
- Initial spec
