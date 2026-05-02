# prevent library files from being installed
%global cargo_install_lib 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash 6b0fda357e50b123028c54c4667573ed

%global appname com.mtkennerly.%{name}

Name:           ludusavi
Version:        0.31.0
Release:        1%{?dist}
Summary:        Game save backup tool

License:        MIT
URL:            https://github.com/mtkennerly/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# cargo vendor --versioned-dirs && tar --numeric-owner -cvJf ../%%{name}-%%{version}-vendor.tar.xz vendor/
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

ExclusiveArch:  %{rust_arches}

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  librsvg2-tools
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
Requires:       hicolor-icon-theme

%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(ab_glyph)) = 0.2.29
Provides:       bundled(crate(ab_glyph_rasterizer)) = 0.1.8
Provides:       bundled(crate(addr2line)) = 0.24.2
Provides:       bundled(crate(adler2)) = 2.0.0
Provides:       bundled(crate(aes)) = 0.8.4
Provides:       bundled(crate(ahash)) = 0.7.8
Provides:       bundled(crate(ahash)) = 0.8.11
Provides:       bundled(crate(aho-corasick)) = 1.1.3
Provides:       bundled(crate(aliasable)) = 0.1.3
Provides:       bundled(crate(aligned-vec)) = 0.6.4
Provides:       bundled(crate(android-activity)) = 0.6.0
Provides:       bundled(crate(android-properties)) = 0.2.2
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(android-tzdata)) = 0.1.1
Provides:       bundled(crate(anstream)) = 0.6.15
Provides:       bundled(crate(anstyle)) = 1.0.8
Provides:       bundled(crate(anstyle-parse)) = 0.2.5
Provides:       bundled(crate(anstyle-query)) = 1.1.1
Provides:       bundled(crate(anstyle-wincon)) = 3.0.4
Provides:       bundled(crate(anyhow)) = 1.0.100
Provides:       bundled(crate(arbitrary)) = 1.4.2
Provides:       bundled(crate(arg_enum_proc_macro)) = 0.3.4
Provides:       bundled(crate(arrayref)) = 0.3.9
Provides:       bundled(crate(arrayvec)) = 0.7.6
Provides:       bundled(crate(ash)) = 0.38.0+1.3.281
Provides:       bundled(crate(as-raw-xcb-connection)) = 1.0.1
Provides:       bundled(crate(async-compression)) = 0.4.15
Provides:       bundled(crate(atk-sys)) = 0.18.2
Provides:       bundled(crate(atomic-waker)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.4.0
Provides:       bundled(crate(av1-grain)) = 0.2.5
Provides:       bundled(crate(avif-serialize)) = 0.8.6
Provides:       bundled(crate(backtrace)) = 0.3.74
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(base64ct)) = 1.6.0
Provides:       bundled(crate(bit_field)) = 0.10.3
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.10.0
Provides:       bundled(crate(bit-set)) = 0.8.0
Provides:       bundled(crate(bitstream-io)) = 2.6.0
Provides:       bundled(crate(bit-vec)) = 0.8.0
Provides:       bundled(crate(bitvec)) = 1.0.1
Provides:       bundled(crate(block)) = 0.1.6
Provides:       bundled(crate(block2)) = 0.5.1
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(borsh)) = 1.5.1
Provides:       bundled(crate(borsh-derive)) = 1.5.1
Provides:       bundled(crate(bstr)) = 1.10.0
Provides:       bundled(crate(built)) = 0.7.7
Provides:       bundled(crate(bumpalo)) = 3.16.0
Provides:       bundled(crate(bytecheck)) = 0.6.12
Provides:       bundled(crate(bytecheck_derive)) = 0.6.12
Provides:       bundled(crate(bytemuck)) = 1.24.0
Provides:       bundled(crate(bytemuck_derive)) = 1.10.2
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(byteorder-lite)) = 0.1.0
Provides:       bundled(crate(bytes)) = 1.7.2
Provides:       bundled(crate(byte-unit)) = 5.1.4
Provides:       bundled(crate(bzip2)) = 0.4.4
Provides:       bundled(crate(bzip2-sys)) = 0.1.11+1.0.8
Provides:       bundled(crate(cairo-sys-rs)) = 0.18.2
Provides:       bundled(crate(calloop)) = 0.13.0
Provides:       bundled(crate(calloop-wayland-source)) = 0.3.0
Provides:       bundled(crate(cc)) = 1.2.49
Provides:       bundled(crate(cesu8)) = 1.1.0
Provides:       bundled(crate(cfg_aliases)) = 0.2.1
Provides:       bundled(crate(cfg-expr)) = 0.15.8
Provides:       bundled(crate(cfg-if)) = 1.0.0
Provides:       bundled(crate(chrono)) = 0.4.38
Provides:       bundled(crate(cipher)) = 0.4.4
Provides:       bundled(crate(clap)) = 4.5.20
Provides:       bundled(crate(clap_builder)) = 4.5.20
Provides:       bundled(crate(clap_complete)) = 4.5.33
Provides:       bundled(crate(clap_derive)) = 4.5.18
Provides:       bundled(crate(clap_lex)) = 0.7.2
Provides:       bundled(crate(clipboard_macos)) = 0.1.1
Provides:       bundled(crate(clipboard_wayland)) = 0.2.2
Provides:       bundled(crate(clipboard-win)) = 5.4.0
Provides:       bundled(crate(clipboard_x11)) = 0.4.2
Provides:       bundled(crate(codespan-reporting)) = 0.12.0
Provides:       bundled(crate(colorchoice)) = 1.0.2
Provides:       bundled(crate(color_quant)) = 1.1.0
Provides:       bundled(crate(combine)) = 4.6.7
Provides:       bundled(crate(concurrent-queue)) = 2.5.0
Provides:       bundled(crate(console)) = 0.15.8
Provides:       bundled(crate(constant_time_eq)) = 0.1.5
Provides:       bundled(crate(core-foundation)) = 0.10.0
Provides:       bundled(crate(core-foundation)) = 0.9.4
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(core-graphics)) = 0.23.2
Provides:       bundled(crate(core-graphics)) = 0.24.0
Provides:       bundled(crate(core-graphics-types)) = 0.1.3
Provides:       bundled(crate(core-graphics-types)) = 0.2.0
Provides:       bundled(crate(core_maths)) = 0.1.1
Provides:       bundled(crate(cosmic-text)) = 0.15.0
Provides:       bundled(crate(cpufeatures)) = 0.2.14
Provides:       bundled(crate(crc)) = 3.2.1
Provides:       bundled(crate(crc32fast)) = 1.4.2
Provides:       bundled(crate(crc-catalog)) = 2.4.0
Provides:       bundled(crate(crossbeam-deque)) = 0.8.5
Provides:       bundled(crate(crossbeam-epoch)) = 0.9.18
Provides:       bundled(crate(crossbeam-utils)) = 0.8.20
Provides:       bundled(crate(crunchy)) = 0.2.2
Provides:       bundled(crate(cryoglyph)) = 0.1.0
Provides:       bundled(crate(crypto-common)) = 0.1.6
Provides:       bundled(crate(ctor-lite)) = 0.1.0
Provides:       bundled(crate(cursor-icon)) = 1.1.0
Provides:       bundled(crate(data-url)) = 0.3.2
Provides:       bundled(crate(dbus)) = 0.9.7
Provides:       bundled(crate(deranged)) = 0.3.11
Provides:       bundled(crate(dialoguer)) = 0.11.0
Provides:       bundled(crate(diff)) = 0.1.13
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(dirs)) = 5.0.1
Provides:       bundled(crate(dirs-sys)) = 0.4.1
Provides:       bundled(crate(dispatch)) = 0.2.0
Provides:       bundled(crate(displaydoc)) = 0.2.5
Provides:       bundled(crate(dlib)) = 0.5.2
Provides:       bundled(crate(document-features)) = 0.2.12
Provides:       bundled(crate(downcast-rs)) = 1.2.1
Provides:       bundled(crate(dpi)) = 0.1.1
Provides:       bundled(crate(dyn-clone)) = 1.0.17
Provides:       bundled(crate(either)) = 1.13.0
Provides:       bundled(crate(embed-resource)) = 3.0.6
Provides:       bundled(crate(encode_unicode)) = 0.3.6
Provides:       bundled(crate(equator)) = 0.4.2
Provides:       bundled(crate(equator-macro)) = 0.4.2
Provides:       bundled(crate(equivalent)) = 1.0.1
Provides:       bundled(crate(errno)) = 0.3.9
Provides:       bundled(crate(error-code)) = 3.3.1
Provides:       bundled(crate(etagere)) = 0.2.13
Provides:       bundled(crate(euclid)) = 0.22.11
Provides:       bundled(crate(exr)) = 1.74.0
Provides:       bundled(crate(fallible-iterator)) = 0.3.0
Provides:       bundled(crate(fallible-streaming-iterator)) = 0.1.9
Provides:       bundled(crate(fastrand)) = 2.1.1
Provides:       bundled(crate(fdeflate)) = 0.3.5
Provides:       bundled(crate(filetime)) = 0.2.25
Provides:       bundled(crate(find-msvc-tools)) = 0.1.5
Provides:       bundled(crate(flate2)) = 1.0.34
Provides:       bundled(crate(flexi_logger)) = 0.29.3
Provides:       bundled(crate(float-cmp)) = 0.9.0
Provides:       bundled(crate(fluent)) = 0.16.1
Provides:       bundled(crate(fluent-bundle)) = 0.15.3
Provides:       bundled(crate(fluent-langneg)) = 0.13.0
Provides:       bundled(crate(fluent-syntax)) = 0.11.1
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foldhash)) = 0.1.5
Provides:       bundled(crate(foldhash)) = 0.2.0
Provides:       bundled(crate(fontconfig-parser)) = 0.5.7
Provides:       bundled(crate(fontdb)) = 0.23.0
Provides:       bundled(crate(font-types)) = 0.10.1
Provides:       bundled(crate(foreign-types)) = 0.5.0
Provides:       bundled(crate(foreign-types-macros)) = 0.2.3
Provides:       bundled(crate(foreign-types-shared)) = 0.3.1
Provides:       bundled(crate(form_urlencoded)) = 1.2.1
Provides:       bundled(crate(funty)) = 2.0.0
Provides:       bundled(crate(futures)) = 0.3.31
Provides:       bundled(crate(futures-channel)) = 0.3.31
Provides:       bundled(crate(futures-core)) = 0.3.31
Provides:       bundled(crate(futures-executor)) = 0.3.31
Provides:       bundled(crate(futures-io)) = 0.3.31
Provides:       bundled(crate(futures-macro)) = 0.3.31
Provides:       bundled(crate(futures-sink)) = 0.3.31
Provides:       bundled(crate(futures-task)) = 0.3.31
Provides:       bundled(crate(futures-util)) = 0.3.31
Provides:       bundled(crate(fuzzy-matcher)) = 0.3.7
Provides:       bundled(crate(gdk-pixbuf-sys)) = 0.18.0
Provides:       bundled(crate(gdk-sys)) = 0.18.2
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(gethostname)) = 0.4.3
Provides:       bundled(crate(getrandom)) = 0.2.15
Provides:       bundled(crate(gif)) = 0.13.3
Provides:       bundled(crate(gimli)) = 0.31.1
Provides:       bundled(crate(gio-sys)) = 0.18.1
Provides:       bundled(crate(glam)) = 0.25.0
Provides:       bundled(crate(gl_generator)) = 0.14.0
Provides:       bundled(crate(glib-sys)) = 0.18.1
Provides:       bundled(crate(globetter)) = 0.2.0
Provides:       bundled(crate(globset)) = 0.4.15
Provides:       bundled(crate(glow)) = 0.16.0
Provides:       bundled(crate(glutin_wgl_sys)) = 0.6.1
Provides:       bundled(crate(gobject-sys)) = 0.18.0
Provides:       bundled(crate(gpu-alloc)) = 0.6.0
Provides:       bundled(crate(gpu-allocator)) = 0.27.0
Provides:       bundled(crate(gpu-alloc-types)) = 0.3.0
Provides:       bundled(crate(gpu-descriptor)) = 0.3.2
Provides:       bundled(crate(gpu-descriptor-types)) = 0.2.0
Provides:       bundled(crate(gtk-sys)) = 0.18.2
Provides:       bundled(crate(guillotiere)) = 0.6.2
Provides:       bundled(crate(half)) = 2.7.1
Provides:       bundled(crate(harfrust)) = 0.3.2
Provides:       bundled(crate(hashbrown)) = 0.12.3
Provides:       bundled(crate(hashbrown)) = 0.14.5
Provides:       bundled(crate(hashbrown)) = 0.15.0
Provides:       bundled(crate(hashbrown)) = 0.16.1
Provides:       bundled(crate(hashlink)) = 0.9.1
Provides:       bundled(crate(heck)) = 0.4.1
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit-abi)) = 0.3.9
Provides:       bundled(crate(hermit-abi)) = 0.4.0
Provides:       bundled(crate(hexf-parse)) = 0.2.1
Provides:       bundled(crate(hmac)) = 0.12.1
Provides:       bundled(crate(home)) = 0.5.9
Provides:       bundled(crate(http)) = 1.1.0
Provides:       bundled(crate(httparse)) = 1.9.5
Provides:       bundled(crate(http-body)) = 1.0.1
Provides:       bundled(crate(http-body-util)) = 0.1.2
Provides:       bundled(crate(hyper)) = 1.4.1
Provides:       bundled(crate(hyper-rustls)) = 0.27.3
Provides:       bundled(crate(hyper-util)) = 0.1.9
Provides:       bundled(crate(iana-time-zone)) = 0.1.61
Provides:       bundled(crate(iana-time-zone-haiku)) = 0.1.2
Provides:       bundled(crate(iced)) = 0.14.0
Provides:       bundled(crate(iced_core)) = 0.14.0
Provides:       bundled(crate(iced_debug)) = 0.14.0
Provides:       bundled(crate(iced_futures)) = 0.14.0
Provides:       bundled(crate(iced_graphics)) = 0.14.0
Provides:       bundled(crate(iced_program)) = 0.14.0
Provides:       bundled(crate(iced_renderer)) = 0.14.0
Provides:       bundled(crate(iced_runtime)) = 0.14.0
Provides:       bundled(crate(iced_tiny_skia)) = 0.14.0
Provides:       bundled(crate(iced_wgpu)) = 0.14.0
Provides:       bundled(crate(iced_widget)) = 0.14.2
Provides:       bundled(crate(iced_winit)) = 0.14.0
Provides:       bundled(crate(idna)) = 0.5.0
Provides:       bundled(crate(image)) = 0.25.2
Provides:       bundled(crate(imagesize)) = 0.13.0
Provides:       bundled(crate(image-webp)) = 0.1.3
Provides:       bundled(crate(image-webp)) = 0.2.4
Provides:       bundled(crate(imgref)) = 1.12.0
Provides:       bundled(crate(indexmap)) = 1.9.3
Provides:       bundled(crate(indexmap)) = 2.12.1
Provides:       bundled(crate(indicatif)) = 0.17.8
Provides:       bundled(crate(inout)) = 0.1.3
Provides:       bundled(crate(instant)) = 0.1.13
Provides:       bundled(crate(interpolate_name)) = 0.2.4
Provides:       bundled(crate(intl-memoizer)) = 0.5.2
Provides:       bundled(crate(intl_pluralrules)) = 7.0.2
Provides:       bundled(crate(ipnet)) = 2.10.1
Provides:       bundled(crate(is_terminal_polyfill)) = 1.70.1
Provides:       bundled(crate(itertools)) = 0.12.1
Provides:       bundled(crate(itertools)) = 0.13.0
Provides:       bundled(crate(itoa)) = 1.0.11
Provides:       bundled(crate(jni)) = 0.21.1
Provides:       bundled(crate(jni-sys)) = 0.3.0
Provides:       bundled(crate(jobserver)) = 0.1.32
Provides:       bundled(crate(jpeg-decoder)) = 0.3.2
Provides:       bundled(crate(js-sys)) = 0.3.83
Provides:       bundled(crate(kamadak-exif)) = 0.6.1
Provides:       bundled(crate(keyvalues-parser)) = 0.2.0
Provides:       bundled(crate(keyvalues-serde)) = 0.2.1
Provides:       bundled(crate(khronos_api)) = 3.1.0
Provides:       bundled(crate(khronos-egl)) = 6.0.0
Provides:       bundled(crate(known-folders)) = 1.2.0
Provides:       bundled(crate(kurbo)) = 0.10.4
Provides:       bundled(crate(kurbo)) = 0.11.3
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(lebe)) = 0.5.3
Provides:       bundled(crate(libc)) = 0.2.174
Provides:       bundled(crate(libdbus-sys)) = 0.2.5
Provides:       bundled(crate(libfuzzer-sys)) = 0.4.10
Provides:       bundled(crate(libloading)) = 0.8.5
Provides:       bundled(crate(libm)) = 0.2.8
Provides:       bundled(crate(libredox)) = 0.0.2
Provides:       bundled(crate(libredox)) = 0.1.3
Provides:       bundled(crate(libsqlite3-sys)) = 0.30.1
Provides:       bundled(crate(lilt)) = 0.8.1
Provides:       bundled(crate(linebender_resource_handle)) = 0.1.1
Provides:       bundled(crate(linked-hash-map)) = 0.5.6
Provides:       bundled(crate(linux-raw-sys)) = 0.4.14
Provides:       bundled(crate(litrs)) = 1.0.0
Provides:       bundled(crate(lock_api)) = 0.4.12
Provides:       bundled(crate(log)) = 0.4.22
Provides:       bundled(crate(loop9)) = 0.1.5
Provides:       bundled(crate(lru)) = 0.16.2
Provides:       bundled(crate(malloc_buf)) = 0.0.6
Provides:       bundled(crate(maybe-rayon)) = 0.1.1
Provides:       bundled(crate(memchr)) = 2.7.4
Provides:       bundled(crate(memmap2)) = 0.9.5
Provides:       bundled(crate(metal)) = 0.32.0
Provides:       bundled(crate(mime)) = 0.3.17
Provides:       bundled(crate(minimal-lexical)) = 0.2.1
Provides:       bundled(crate(miniz_oxide)) = 0.8.0
Provides:       bundled(crate(mio)) = 1.0.2
Provides:       bundled(crate(mutate_once)) = 0.1.2
Provides:       bundled(crate(naga)) = 27.0.3
Provides:       bundled(crate(ndk)) = 0.9.0
Provides:       bundled(crate(ndk-context)) = 0.1.1
Provides:       bundled(crate(ndk-sys)) = 0.6.0+11769913
Provides:       bundled(crate(new_debug_unreachable)) = 1.0.6
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(nom)) = 8.0.0
Provides:       bundled(crate(noop_proc_macro)) = 0.3.0
Provides:       bundled(crate(normpath)) = 1.3.0
Provides:       bundled(crate(ntapi)) = 0.4.1
Provides:       bundled(crate(number_prefix)) = 0.4.0
Provides:       bundled(crate(num-bigint)) = 0.4.6
Provides:       bundled(crate(num-conv)) = 0.1.0
Provides:       bundled(crate(num-derive)) = 0.4.2
Provides:       bundled(crate(num_enum)) = 0.7.3
Provides:       bundled(crate(num_enum_derive)) = 0.7.3
Provides:       bundled(crate(num-integer)) = 0.1.46
Provides:       bundled(crate(num-rational)) = 0.4.2
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(objc)) = 0.2.7
Provides:       bundled(crate(objc2)) = 0.5.2
Provides:       bundled(crate(objc2-app-kit)) = 0.2.2
Provides:       bundled(crate(objc2-cloud-kit)) = 0.2.2
Provides:       bundled(crate(objc2-contacts)) = 0.2.2
Provides:       bundled(crate(objc2-core-data)) = 0.2.2
Provides:       bundled(crate(objc2-core-foundation)) = 0.3.1
Provides:       bundled(crate(objc2-core-image)) = 0.2.2
Provides:       bundled(crate(objc2-core-location)) = 0.2.2
Provides:       bundled(crate(objc2-encode)) = 4.0.3
Provides:       bundled(crate(objc2-foundation)) = 0.2.2
Provides:       bundled(crate(objc2-io-kit)) = 0.3.1
Provides:       bundled(crate(objc2-link-presentation)) = 0.2.2
Provides:       bundled(crate(objc2-metal)) = 0.2.2
Provides:       bundled(crate(objc2-quartz-core)) = 0.2.2
Provides:       bundled(crate(objc2-symbols)) = 0.2.2
Provides:       bundled(crate(objc2-ui-kit)) = 0.2.2
Provides:       bundled(crate(objc2-uniform-type-identifiers)) = 0.2.2
Provides:       bundled(crate(objc2-user-notifications)) = 0.2.2
Provides:       bundled(crate(objc-sys)) = 0.3.5
Provides:       bundled(crate(object)) = 0.36.5
Provides:       bundled(crate(once_cell)) = 1.21.3
Provides:       bundled(crate(opener)) = 0.7.2
Provides:       bundled(crate(option-ext)) = 0.2.0
Provides:       bundled(crate(orbclient)) = 0.3.47
Provides:       bundled(crate(ordered-float)) = 5.1.0
Provides:       bundled(crate(ouroboros)) = 0.18.5
Provides:       bundled(crate(ouroboros_macro)) = 0.18.5
Provides:       bundled(crate(owned_ttf_parser)) = 0.25.0
Provides:       bundled(crate(pango-sys)) = 0.18.0
Provides:       bundled(crate(parking_lot)) = 0.12.3
Provides:       bundled(crate(parking_lot_core)) = 0.9.10
Provides:       bundled(crate(password-hash)) = 0.4.2
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(pbkdf2)) = 0.11.0
Provides:       bundled(crate(percent-encoding)) = 2.3.1
Provides:       bundled(crate(pest)) = 2.7.14
Provides:       bundled(crate(pest_derive)) = 2.7.14
Provides:       bundled(crate(pest_generator)) = 2.7.14
Provides:       bundled(crate(pest_meta)) = 2.7.14
Provides:       bundled(crate(pico-args)) = 0.5.0
Provides:       bundled(crate(pin-project)) = 1.1.6
Provides:       bundled(crate(pin-project-internal)) = 1.1.6
Provides:       bundled(crate(pin-project-lite)) = 0.2.14
Provides:       bundled(crate(pin-utils)) = 0.1.0
Provides:       bundled(crate(pkg-config)) = 0.3.31
Provides:       bundled(crate(png)) = 0.17.14
Provides:       bundled(crate(polling)) = 3.7.3
Provides:       bundled(crate(portable-atomic)) = 1.9.0
Provides:       bundled(crate(portable-atomic-util)) = 0.2.4
Provides:       bundled(crate(powerfmt)) = 0.2.0
Provides:       bundled(crate(ppv-lite86)) = 0.2.20
Provides:       bundled(crate(presser)) = 0.3.1
Provides:       bundled(crate(pretty_assertions)) = 1.4.1
Provides:       bundled(crate(proc-macro2)) = 1.0.87
Provides:       bundled(crate(proc-macro2-diagnostics)) = 0.10.1
Provides:       bundled(crate(proc-macro-crate)) = 3.2.0
Provides:       bundled(crate(proc-macro-error)) = 1.0.4
Provides:       bundled(crate(proc-macro-error-attr)) = 1.0.4
Provides:       bundled(crate(profiling)) = 1.0.16
Provides:       bundled(crate(profiling-procmacros)) = 1.0.17
Provides:       bundled(crate(ptr_meta)) = 0.1.4
Provides:       bundled(crate(ptr_meta_derive)) = 0.1.4
Provides:       bundled(crate(qoi)) = 0.4.1
Provides:       bundled(crate(quick-error)) = 2.0.1
Provides:       bundled(crate(quick-xml)) = 0.36.2
Provides:       bundled(crate(quinn)) = 0.11.5
Provides:       bundled(crate(quinn-proto)) = 0.11.8
Provides:       bundled(crate(quinn-udp)) = 0.5.5
Provides:       bundled(crate(quote)) = 1.0.42
Provides:       bundled(crate(radium)) = 0.7.0
Provides:       bundled(crate(rand)) = 0.8.5
Provides:       bundled(crate(rand_chacha)) = 0.3.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(range-alloc)) = 0.1.3
Provides:       bundled(crate(rangemap)) = 1.5.1
Provides:       bundled(crate(rav1e)) = 0.7.1
Provides:       bundled(crate(ravif)) = 0.11.20
Provides:       bundled(crate(raw-window-handle)) = 0.6.2
Provides:       bundled(crate(rayon)) = 1.10.0
Provides:       bundled(crate(rayon-core)) = 1.12.1
Provides:       bundled(crate(read-fonts)) = 0.35.0
Provides:       bundled(crate(redox_syscall)) = 0.4.1
Provides:       bundled(crate(redox_syscall)) = 0.5.7
Provides:       bundled(crate(redox_users)) = 0.4.6
Provides:       bundled(crate(regashii)) = 0.2.0
Provides:       bundled(crate(regex)) = 1.11.0
Provides:       bundled(crate(regex-automata)) = 0.4.8
Provides:       bundled(crate(regex-syntax)) = 0.8.5
Provides:       bundled(crate(rend)) = 0.4.2
Provides:       bundled(crate(renderdoc-sys)) = 1.1.0
Provides:       bundled(crate(reqwest)) = 0.12.8
Provides:       bundled(crate(resvg)) = 0.45.1
Provides:       bundled(crate(rfd)) = 0.15.0
Provides:       bundled(crate(rgb)) = 0.8.52
Provides:       bundled(crate(ring)) = 0.17.8
Provides:       bundled(crate(rkyv)) = 0.7.45
Provides:       bundled(crate(rkyv_derive)) = 0.7.45
Provides:       bundled(crate(roxmltree)) = 0.20.0
Provides:       bundled(crate(rusqlite)) = 0.32.1
Provides:       bundled(crate(rustc-demangle)) = 0.1.24
Provides:       bundled(crate(rustc-hash)) = 1.1.0
Provides:       bundled(crate(rustc-hash)) = 2.0.0
Provides:       bundled(crate(rustc_version)) = 0.4.1
Provides:       bundled(crate(rust_decimal)) = 1.36.0
Provides:       bundled(crate(rustix)) = 0.38.37
Provides:       bundled(crate(rustls)) = 0.23.14
Provides:       bundled(crate(rustls-pemfile)) = 2.2.0
Provides:       bundled(crate(rustls-pki-types)) = 1.10.0
Provides:       bundled(crate(rustls-webpki)) = 0.102.8
Provides:       bundled(crate(rustversion)) = 1.0.22
Provides:       bundled(crate(rustybuzz)) = 0.20.1
Provides:       bundled(crate(ryu)) = 1.0.18
Provides:       bundled(crate(same-file)) = 1.0.6
Provides:       bundled(crate(schemars)) = 0.8.21
Provides:       bundled(crate(schemars_derive)) = 0.8.21
Provides:       bundled(crate(scoped-tls)) = 1.0.1
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(sctk-adwaita)) = 0.10.1
Provides:       bundled(crate(seahash)) = 4.1.0
Provides:       bundled(crate(self_cell)) = 0.10.3
Provides:       bundled(crate(self_cell)) = 1.0.4
Provides:       bundled(crate(semver)) = 1.0.23
Provides:       bundled(crate(serde)) = 1.0.228
Provides:       bundled(crate(serde_core)) = 1.0.228
Provides:       bundled(crate(serde_derive)) = 1.0.228
Provides:       bundled(crate(serde_derive_internals)) = 0.29.1
Provides:       bundled(crate(serde_json)) = 1.0.128
Provides:       bundled(crate(serde_spanned)) = 0.6.8
Provides:       bundled(crate(serde_spanned)) = 1.0.3
Provides:       bundled(crate(serde_urlencoded)) = 0.7.1
Provides:       bundled(crate(serde_yaml)) = 0.8.26
Provides:       bundled(crate(sha1)) = 0.10.6
Provides:       bundled(crate(sha2)) = 0.10.8
Provides:       bundled(crate(shell-words)) = 1.1.0
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(signal-hook)) = 0.3.17
Provides:       bundled(crate(signal-hook-registry)) = 1.4.2
Provides:       bundled(crate(simd-adler32)) = 0.3.7
Provides:       bundled(crate(simd_helpers)) = 0.1.0
Provides:       bundled(crate(simdutf8)) = 0.1.5
Provides:       bundled(crate(simplecss)) = 0.2.2
Provides:       bundled(crate(siphasher)) = 1.0.1
Provides:       bundled(crate(skrifa)) = 0.37.0
Provides:       bundled(crate(slab)) = 0.4.9
Provides:       bundled(crate(slotmap)) = 1.0.7
Provides:       bundled(crate(smallvec)) = 1.15.1
Provides:       bundled(crate(smithay-client-toolkit)) = 0.19.2
Provides:       bundled(crate(smithay-clipboard)) = 0.7.2
Provides:       bundled(crate(smol_str)) = 0.2.2
Provides:       bundled(crate(socket2)) = 0.5.7
Provides:       bundled(crate(softbuffer)) = 0.4.6
Provides:       bundled(crate(spin)) = 0.9.8
Provides:       bundled(crate(spirv-0.3.0+sdk)) = 1.3.268.0
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(steamlocate)) = 2.0.0
Provides:       bundled(crate(strict-num)) = 0.1.1
Provides:       bundled(crate(strsim)) = 0.11.1
Provides:       bundled(crate(subtle)) = 2.6.1
Provides:       bundled(crate(svg_fmt)) = 0.4.3
Provides:       bundled(crate(svgtypes)) = 0.15.3
Provides:       bundled(crate(swash)) = 0.2.6
Provides:       bundled(crate(syn)) = 1.0.109
Provides:       bundled(crate(syn)) = 2.0.87
Provides:       bundled(crate(sync_wrapper)) = 1.0.1
Provides:       bundled(crate(syn_derive)) = 0.1.8
Provides:       bundled(crate(sysinfo)) = 0.36.0
Provides:       bundled(crate(sys-locale)) = 0.3.1
Provides:       bundled(crate(system-deps)) = 6.2.2
Provides:       bundled(crate(tap)) = 1.0.1
Provides:       bundled(crate(target-lexicon)) = 0.12.16
Provides:       bundled(crate(tempfile)) = 3.13.0
Provides:       bundled(crate(termcolor)) = 1.4.1
Provides:       bundled(crate(terminal_size)) = 0.4.0
Provides:       bundled(crate(thiserror)) = 1.0.64
Provides:       bundled(crate(thiserror)) = 2.0.17
Provides:       bundled(crate(thiserror-impl)) = 1.0.64
Provides:       bundled(crate(thiserror-impl)) = 2.0.17
Provides:       bundled(crate(thread_local)) = 1.1.8
Provides:       bundled(crate(tiff)) = 0.9.1
Provides:       bundled(crate(time)) = 0.3.36
Provides:       bundled(crate(time-core)) = 0.1.2
Provides:       bundled(crate(tiny-skia)) = 0.11.4
Provides:       bundled(crate(tiny-skia-path)) = 0.11.4
Provides:       bundled(crate(tinystr)) = 0.7.6
Provides:       bundled(crate(tinyvec)) = 1.8.0
Provides:       bundled(crate(tinyvec_macros)) = 0.1.1
Provides:       bundled(crate(tiny-xlib)) = 0.2.3
Provides:       bundled(crate(tokio)) = 1.40.0
Provides:       bundled(crate(tokio-macros)) = 2.4.0
Provides:       bundled(crate(tokio-rustls)) = 0.26.0
Provides:       bundled(crate(tokio-util)) = 0.7.12
Provides:       bundled(crate(toml)) = 0.8.19
Provides:       bundled(crate(toml)) = 0.9.8
Provides:       bundled(crate(toml_datetime)) = 0.6.8
Provides:       bundled(crate(toml_datetime)) = 0.7.3
Provides:       bundled(crate(toml_edit)) = 0.22.22
Provides:       bundled(crate(toml_parser)) = 1.0.4
Provides:       bundled(crate(toml_writer)) = 1.0.4
Provides:       bundled(crate(tower-service)) = 0.3.3
Provides:       bundled(crate(tracing)) = 0.1.40
Provides:       bundled(crate(tracing-attributes)) = 0.1.27
Provides:       bundled(crate(tracing-core)) = 0.1.32
Provides:       bundled(crate(try-lock)) = 0.2.5
Provides:       bundled(crate(ttf-parser)) = 0.25.0
Provides:       bundled(crate(typed-path)) = 0.9.2
Provides:       bundled(crate(type-map)) = 0.5.0
Provides:       bundled(crate(typenum)) = 1.17.0
Provides:       bundled(crate(ucd-trie)) = 0.1.7
Provides:       bundled(crate(unic-langid)) = 0.9.5
Provides:       bundled(crate(unic-langid-impl)) = 0.9.5
Provides:       bundled(crate(unicode-bidi)) = 0.3.17
Provides:       bundled(crate(unicode-bidi-mirroring)) = 0.4.0
Provides:       bundled(crate(unicode-ccc)) = 0.4.0
Provides:       bundled(crate(unicode-ident)) = 1.0.13
Provides:       bundled(crate(unicode-linebreak)) = 0.1.5
Provides:       bundled(crate(unicode-normalization)) = 0.1.24
Provides:       bundled(crate(unicode-properties)) = 0.1.3
Provides:       bundled(crate(unicode-script)) = 0.5.7
Provides:       bundled(crate(unicode-segmentation)) = 1.12.0
Provides:       bundled(crate(unicode-vo)) = 0.1.0
Provides:       bundled(crate(unicode-width)) = 0.1.14
Provides:       bundled(crate(untrusted)) = 0.9.0
Provides:       bundled(crate(url)) = 2.5.2
Provides:       bundled(crate(usvg)) = 0.45.1
Provides:       bundled(crate(utf16string)) = 0.2.0
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(utf8-width)) = 0.1.7
Provides:       bundled(crate(uuid)) = 1.10.0
Provides:       bundled(crate(vcpkg)) = 0.2.15
Provides:       bundled(crate(velcro)) = 0.5.4
Provides:       bundled(crate(velcro_core)) = 0.5.4
Provides:       bundled(crate(velcro_macros)) = 0.5.4
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(version-compare)) = 0.2.0
Provides:       bundled(crate(v_frame)) = 0.3.9
Provides:       bundled(crate(vswhom)) = 0.1.0
Provides:       bundled(crate(vswhom-sys)) = 0.1.3
Provides:       bundled(crate(walkdir)) = 2.5.0
Provides:       bundled(crate(want)) = 0.3.1
Provides:       bundled(crate(wasi-0.11.0+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasite)) = 0.1.0
Provides:       bundled(crate(wasm-bindgen)) = 0.2.106
Provides:       bundled(crate(wasm-bindgen-futures)) = 0.4.45
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.106
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.106
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.106
Provides:       bundled(crate(wasmtimer)) = 0.4.3
Provides:       bundled(crate(wayland-backend)) = 0.3.7
Provides:       bundled(crate(wayland-client)) = 0.31.6
Provides:       bundled(crate(wayland-csd-frame)) = 0.3.0
Provides:       bundled(crate(wayland-cursor)) = 0.31.6
Provides:       bundled(crate(wayland-protocols)) = 0.32.4
Provides:       bundled(crate(wayland-protocols-plasma)) = 0.3.4
Provides:       bundled(crate(wayland-protocols-wlr)) = 0.3.4
Provides:       bundled(crate(wayland-scanner)) = 0.31.5
Provides:       bundled(crate(wayland-sys)) = 0.31.5
Provides:       bundled(crate(webpki-roots)) = 0.26.6
Provides:       bundled(crate(web-sys)) = 0.3.83
Provides:       bundled(crate(web-time)) = 1.1.0
Provides:       bundled(crate(weezl)) = 0.1.12
Provides:       bundled(crate(wgpu)) = 27.0.1
Provides:       bundled(crate(wgpu-core)) = 27.0.3
Provides:       bundled(crate(wgpu-core-deps-apple)) = 27.0.0
Provides:       bundled(crate(wgpu-core-deps-emscripten)) = 27.0.0
Provides:       bundled(crate(wgpu-core-deps-windows-linux-android)) = 27.0.0
Provides:       bundled(crate(wgpu-hal)) = 27.0.4
Provides:       bundled(crate(wgpu-types)) = 27.0.1
Provides:       bundled(crate(which)) = 6.0.3
Provides:       bundled(crate(whoami)) = 1.5.2
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.9
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(window_clipboard)) = 0.5.1
Provides:       bundled(crate(windows)) = 0.58.0
Provides:       bundled(crate(windows)) = 0.60.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows-collections)) = 0.1.1
Provides:       bundled(crate(windows-core)) = 0.52.0
Provides:       bundled(crate(windows-core)) = 0.58.0
Provides:       bundled(crate(windows-core)) = 0.60.1
Provides:       bundled(crate(windows-future)) = 0.1.1
Provides:       bundled(crate(windows_i686_gnu)) = 0.42.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.48.5
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.42.2
Provides:       bundled(crate(windows_i686_msvc)) = 0.48.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows-implement)) = 0.58.0
Provides:       bundled(crate(windows-implement)) = 0.59.0
Provides:       bundled(crate(windows-interface)) = 0.58.0
Provides:       bundled(crate(windows-interface)) = 0.59.0
Provides:       bundled(crate(windows-link)) = 0.1.0
Provides:       bundled(crate(windows-numerics)) = 0.1.1
Provides:       bundled(crate(windows-registry)) = 0.2.0
Provides:       bundled(crate(windows-result)) = 0.2.0
Provides:       bundled(crate(windows-result)) = 0.3.1
Provides:       bundled(crate(windows-strings)) = 0.1.0
Provides:       bundled(crate(windows-strings)) = 0.3.1
Provides:       bundled(crate(windows-sys)) = 0.45.0
Provides:       bundled(crate(windows-sys)) = 0.48.0
Provides:       bundled(crate(windows-sys)) = 0.52.0
Provides:       bundled(crate(windows-sys)) = 0.59.0
Provides:       bundled(crate(windows-targets)) = 0.42.2
Provides:       bundled(crate(windows-targets)) = 0.48.5
Provides:       bundled(crate(windows-targets)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(winit)) = 0.30.5
Provides:       bundled(crate(winnow)) = 0.6.20
Provides:       bundled(crate(winnow)) = 0.7.14
Provides:       bundled(crate(winreg)) = 0.52.0
Provides:       bundled(crate(winreg)) = 0.55.0
Provides:       bundled(crate(winsafe)) = 0.0.19
Provides:       bundled(crate(wyz)) = 0.5.1
Provides:       bundled(crate(x11-dl)) = 2.21.0
Provides:       bundled(crate(x11rb)) = 0.13.1
Provides:       bundled(crate(x11rb-protocol)) = 0.13.1
Provides:       bundled(crate(xcursor)) = 0.3.8
Provides:       bundled(crate(xkbcommon-dl)) = 0.4.2
Provides:       bundled(crate(xkeysym)) = 0.2.1
Provides:       bundled(crate(xml-rs)) = 0.8.22
Provides:       bundled(crate(xmlwriter)) = 0.1.0
Provides:       bundled(crate(yaml-rust)) = 0.4.5
Provides:       bundled(crate(yansi)) = 1.0.1
Provides:       bundled(crate(yazi)) = 0.2.1
Provides:       bundled(crate(zeno)) = 0.3.3
Provides:       bundled(crate(zerocopy)) = 0.7.35
Provides:       bundled(crate(zerocopy)) = 0.8.31
Provides:       bundled(crate(zerocopy-derive)) = 0.7.35
Provides:       bundled(crate(zerocopy-derive)) = 0.8.31
Provides:       bundled(crate(zeroize)) = 1.8.1
Provides:       bundled(crate(zip)) = 0.6.6
Provides:       bundled(crate(zstd)) = 0.11.2+zstd.1.5.2
Provides:       bundled(crate(zstd-safe)) = 5.0.2+zstd.1.5.2
Provides:       bundled(crate(zstd-sys)) = 2.0.13+zstd.1.5.6
Provides:       bundled(crate(zune-core)) = 0.4.12
Provides:       bundled(crate(zune-inflate)) = 0.2.54
Provides:       bundled(crate(zune-jpeg)) = 0.4.21
%endif

%description
Ludusavi is a tool for backing up your PC video game save data.


%prep
%autosetup -p1 %{?with_vendor:-a1}

find -name '*.rs' -exec chmod -x {} ';'

%if %{with vendor}
# Dirty fix shebang error
sed -e'1i //placeholder' -i vendor/typed-path-*/src/lib.rs
typedpath_hash="$(sha256sum vendor/typed-path-*/src/lib.rs 2>&1 |cut -d" " -f1)"
sed \
  -e 's|"src/lib.rs":"[^"]*"|"src/lib.rs":"'${typedpath_hash}'"|' \
  -i vendor/typed-path-*/.cargo-checksum.json

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
  --remove-key=Encoding \
  assets/linux/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm0644 assets/icon.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appname}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert assets/icon.svg -h ${res} -w ${res} \
    -o ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 assets/linux/%{appname}.metainfo.xml %{buildroot}%{_metainfodir}/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/*/%{appname}*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Fri May 01 2026 Phantom X <megaphantomx at hotmail dot com> - 0.31.0-1
- 0.31.0

* Tue Nov 25 2025 Phantom X <megaphantomx at hotmail dot com> - 0.30.0-1
- 0.30.0

* Wed Jun 04 2025 Phantom X <megaphantomx at hotmail dot com> - 0.29.1-1
- Initial spec
