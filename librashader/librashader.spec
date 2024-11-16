%bcond_with check

# Use vendor tarball
%bcond_without vendor

%global soname_ver 1
%global api_ver 1

%global vendor_hash 45b3bbdbc62375ec34e3ebea1e960849

Name:           librashader
Version:        0.5.1
Release:        1%{?dist}
Summary:        RetroArch shaders for all

License:        MPL-2.0 OR GPL-3.0-only%{?with_vendor: AND ((0BSD OR MIT OR Apache-2.0) AND (Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND BSD-2-Clause AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND BSD-3-Clause AND CC0-1.0 AND (CC0-1.0 OR Apache-2.0) AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND ISC AND MIT AND (MIT OR Apache-2.0) AND ((MIT OR Apache-2.0) AND Unicode-DFS-2016) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND (Unlicense OR MIT) AND Zlib AND (Zlib OR Apache-2.0 OR MIT))}
URL:            https://github.com/SnowflakePowered/%{name}
Source0:        %{url}/archive/%{name}-v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# rust2rpm -t fedora -V --no-rpmautospec --ignore-missing-license-files ./Cargo.toml %%{version}
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

Patch0:         0001-RPM-fixes.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  cmake
BuildRequires:  rust-packaging
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  make
BuildRequires:  patchelf
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
Requires:       libglvnd-glx%{?_isa}
Requires:       vulkan-loader%{?_isa}

%if %{with vendor}
# for i in * ;do echo "Provides:       bundled(crate(${i%%-*})) = ${i##*-}";done
Provides:       bundled(crate(ab_glyph)) = 0.2.29
Provides:       bundled(crate(ab_glyph_rasterizer)) = 0.1.8
Provides:       bundled(crate(adler2)) = 2.0.0
Provides:       bundled(crate(ahash)) = 0.7.8
Provides:       bundled(crate(ahash)) = 0.8.11
Provides:       bundled(crate(aho-corasick)) = 1.1.3
Provides:       bundled(crate(allocator-api2)) = 0.2.18
Provides:       bundled(crate(android-activity)) = 0.5.2
Provides:       bundled(crate(android-properties)) = 0.2.2
Provides:       bundled(crate(android_system_properties)) = 0.1.5
Provides:       bundled(crate(anstream)) = 0.3.2
Provides:       bundled(crate(anstyle)) = 1.0.8
Provides:       bundled(crate(anstyle-parse)) = 0.2.5
Provides:       bundled(crate(anstyle-query)) = 1.1.1
Provides:       bundled(crate(anstyle-wincon)) = 1.0.2
Provides:       bundled(crate(anyhow)) = 1.0.89
Provides:       bundled(crate(arc-swap)) = 1.7.1
Provides:       bundled(crate(array-concat)) = 0.5.3
Provides:       bundled(crate(array-init)) = 2.1.0
Provides:       bundled(crate(arrayref)) = 0.3.9
Provides:       bundled(crate(arrayvec)) = 0.7.6
Provides:       bundled(crate(ash)) = 0.38.0+1.3.281
Provides:       bundled(crate(ash-window)) = 0.13.0
Provides:       bundled(crate(as-raw-xcb-connection)) = 1.0.1
Provides:       bundled(crate(async-trait)) = 0.1.83
Provides:       bundled(crate(atomic-waker)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.4.0
Provides:       bundled(crate(auto_ops)) = 0.3.0
Provides:       bundled(crate(base64)) = 0.13.1
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(bincode-2.0.0)) = rc.3
Provides:       bundled(crate(bincode_derive-2.0.0)) = rc.3
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.6.0
Provides:       bundled(crate(bit-set)) = 0.6.0
Provides:       bundled(crate(bit-vec)) = 0.7.0
Provides:       bundled(crate(bitvec)) = 1.0.1
Provides:       bundled(crate(blake3)) = 1.5.4
Provides:       bundled(crate(block)) = 0.1.6
Provides:       bundled(crate(block2)) = 0.3.0
Provides:       bundled(crate(block2)) = 0.5.1
Provides:       bundled(crate(block-buffer)) = 0.10.4
Provides:       bundled(crate(block-sys)) = 0.2.1
Provides:       bundled(crate(build-target)) = 0.4.0
Provides:       bundled(crate(bumpalo)) = 3.16.0
Provides:       bundled(crate(bytecount)) = 0.6.8
Provides:       bundled(crate(bytemuck)) = 1.18.0
Provides:       bundled(crate(bytemuck_derive)) = 1.7.1
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(byteorder-lite)) = 0.1.0
Provides:       bundled(crate(bytes)) = 1.7.2
Provides:       bundled(crate(calloop)) = 0.12.4
Provides:       bundled(crate(calloop-wayland-source)) = 0.2.0
Provides:       bundled(crate(carlog)) = 0.1.0
Provides:       bundled(crate(cbindgen)) = 0.27.0
Provides:       bundled(crate(cc)) = 1.1.28
Provides:       bundled(crate(cesu8)) = 1.1.0
Provides:       bundled(crate(cfg_aliases)) = 0.1.1
Provides:       bundled(crate(cfg-if)) = 1.0.0
Provides:       bundled(crate(clap)) = 4.3.0
Provides:       bundled(crate(clap_builder)) = 4.3.0
Provides:       bundled(crate(clap_derive)) = 4.3.0
Provides:       bundled(crate(clap_lex)) = 0.5.1
Provides:       bundled(crate(cmake)) = 0.1.51
Provides:       bundled(crate(cocoa)) = 0.25.0
Provides:       bundled(crate(cocoa-foundation)) = 0.1.2
Provides:       bundled(crate(codespan-reporting)) = 0.11.1
Provides:       bundled(crate(colorchoice)) = 1.0.2
Provides:       bundled(crate(colored)) = 2.1.0
Provides:       bundled(crate(color_quant)) = 1.1.0
Provides:       bundled(crate(com)) = 0.6.0
Provides:       bundled(crate(combine)) = 4.6.7
Provides:       bundled(crate(com_macros)) = 0.6.0
Provides:       bundled(crate(com_macros_support)) = 0.6.0
Provides:       bundled(crate(concurrent-queue)) = 2.5.0
Provides:       bundled(crate(config)) = 0.13.4
Provides:       bundled(crate(constant_time_eq)) = 0.3.1
Provides:       bundled(crate(core-foundation)) = 0.9.4
Provides:       bundled(crate(core-foundation-sys)) = 0.8.7
Provides:       bundled(crate(core-graphics)) = 0.23.2
Provides:       bundled(crate(core-graphics-types)) = 0.1.3
Provides:       bundled(crate(cpufeatures)) = 0.2.14
Provides:       bundled(crate(crc)) = 3.2.1
Provides:       bundled(crate(crc32fast)) = 1.4.2
Provides:       bundled(crate(crc-catalog)) = 2.4.0
Provides:       bundled(crate(crossbeam-deque)) = 0.8.5
Provides:       bundled(crate(crossbeam-epoch)) = 0.9.18
Provides:       bundled(crate(crossbeam-utils)) = 0.8.20
Provides:       bundled(crate(crunchy)) = 0.2.2
Provides:       bundled(crate(crypto-common)) = 0.1.6
Provides:       bundled(crate(cursor-icon)) = 1.1.0
Provides:       bundled(crate(d3d12)) = 22.0.0
Provides:       bundled(crate(d3d12-descriptor-heap)) = 0.2.0
Provides:       bundled(crate(data-encoding)) = 2.6.0
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(dirs-next)) = 1.0.2
Provides:       bundled(crate(dirs-sys-next)) = 0.1.2
Provides:       bundled(crate(dispatch)) = 0.2.0
Provides:       bundled(crate(dlib)) = 0.5.2
Provides:       bundled(crate(dlv-list)) = 0.3.0
Provides:       bundled(crate(document-features)) = 0.2.10
Provides:       bundled(crate(downcast-rs)) = 1.2.1
Provides:       bundled(crate(either)) = 1.13.0
Provides:       bundled(crate(encoding_rs)) = 0.8.34
Provides:       bundled(crate(env_logger)) = 0.10.2
Provides:       bundled(crate(equivalent)) = 1.0.1
Provides:       bundled(crate(errno)) = 0.3.9
Provides:       bundled(crate(fastrand)) = 2.1.1
Provides:       bundled(crate(fdeflate)) = 0.3.5
Provides:       bundled(crate(fixedbitset)) = 0.4.2
Provides:       bundled(crate(flate2)) = 1.0.34
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foreign-types)) = 0.5.0
Provides:       bundled(crate(foreign-types-macros)) = 0.2.3
Provides:       bundled(crate(foreign-types-shared)) = 0.3.1
Provides:       bundled(crate(fs2)) = 0.4.3
Provides:       bundled(crate(funty)) = 2.0.0
Provides:       bundled(crate(generic-array)) = 0.14.7
Provides:       bundled(crate(gethostname)) = 0.4.3
Provides:       bundled(crate(getrandom)) = 0.2.15
Provides:       bundled(crate(gfx-maths)) = 0.2.9
Provides:       bundled(crate(gif)) = 0.13.1
Provides:       bundled(crate(glfw)) = 0.58.0
Provides:       bundled(crate(glfw-sys)) = 5.0.0+3.3.9
Provides:       bundled(crate(gl_generator)) = 0.14.0
Provides:       bundled(crate(glob)) = 0.3.1
Provides:       bundled(crate(glow)) = 0.13.1
Provides:       bundled(crate(glow)) = 0.14.1
Provides:       bundled(crate(glslang)) = 0.6.0
Provides:       bundled(crate(glslang-sys)) = 0.6.1+46ef757
Provides:       bundled(crate(glutin_wgl_sys)) = 0.6.0
Provides:       bundled(crate(gpu-alloc)) = 0.6.0
Provides:       bundled(crate(gpu-allocator)) = 0.26.0
Provides:       bundled(crate(gpu-allocator)) = 0.27.0
Provides:       bundled(crate(gpu-alloc-types)) = 0.3.0
Provides:       bundled(crate(gpu-descriptor)) = 0.3.0
Provides:       bundled(crate(gpu-descriptor-types)) = 0.2.0
Provides:       bundled(crate(half)) = 2.4.1
Provides:       bundled(crate(halfbrown)) = 0.2.5
Provides:       bundled(crate(hashbrown)) = 0.12.3
Provides:       bundled(crate(hashbrown)) = 0.14.5
Provides:       bundled(crate(hashbrown)) = 0.15.0
Provides:       bundled(crate(hassle-rs)) = 0.11.0
Provides:       bundled(crate(heck)) = 0.4.1
Provides:       bundled(crate(hermit-abi)) = 0.4.0
Provides:       bundled(crate(hexf-parse)) = 0.2.1
Provides:       bundled(crate(humantime)) = 2.1.0
Provides:       bundled(crate(icrate)) = 0.0.4
Provides:       bundled(crate(image)) = 0.25.2
Provides:       bundled(crate(image-compare)) = 0.4.1
Provides:       bundled(crate(image-webp)) = 0.1.3
Provides:       bundled(crate(indexmap)) = 2.6.0
Provides:       bundled(crate(is-terminal)) = 0.4.13
Provides:       bundled(crate(itertools)) = 0.12.1
Provides:       bundled(crate(itoa)) = 1.0.11
Provides:       bundled(crate(jni)) = 0.21.1
Provides:       bundled(crate(jni-sys)) = 0.3.0
Provides:       bundled(crate(jobserver)) = 0.1.32
Provides:       bundled(crate(jpeg-decoder)) = 0.3.1
Provides:       bundled(crate(json5)) = 0.4.1
Provides:       bundled(crate(js-sys)) = 0.3.70
Provides:       bundled(crate(khronos_api)) = 3.1.0
Provides:       bundled(crate(khronos-egl)) = 6.0.0
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(libc)) = 0.2.159
Provides:       bundled(crate(libloading)) = 0.8.5
Provides:       bundled(crate(libm)) = 0.2.8
Provides:       bundled(crate(libredox)) = 0.0.2
Provides:       bundled(crate(libredox)) = 0.1.3
Provides:       bundled(crate(linked-hash-map)) = 0.5.6
Provides:       bundled(crate(linux-raw-sys)) = 0.4.14
Provides:       bundled(crate(litrs)) = 0.4.1
Provides:       bundled(crate(lock_api)) = 0.4.12
Provides:       bundled(crate(log)) = 0.4.22
Provides:       bundled(crate(mach-siegbert-vogt-dxcsa)) = 0.1.3
Provides:       bundled(crate(malloc_buf)) = 0.0.6
Provides:       bundled(crate(memchr)) = 2.7.4
Provides:       bundled(crate(memmap2)) = 0.9.5
Provides:       bundled(crate(metal)) = 0.29.0
Provides:       bundled(crate(minimal-lexical)) = 0.2.1
Provides:       bundled(crate(miniz_oxide)) = 0.8.0
Provides:       bundled(crate(naga)) = 22.1.0
Provides:       bundled(crate(ndk)) = 0.8.0
Provides:       bundled(crate(ndk-context)) = 0.1.1
Provides:       bundled(crate(ndk-sys)) = 0.5.0+25.2.9519653
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(nom_locate)) = 4.2.0
Provides:       bundled(crate(num)) = 0.4.3
Provides:       bundled(crate(num-bigint)) = 0.4.6
Provides:       bundled(crate(num-complex)) = 0.4.6
Provides:       bundled(crate(num-derive)) = 0.4.2
Provides:       bundled(crate(num_enum)) = 0.7.3
Provides:       bundled(crate(num_enum_derive)) = 0.7.3
Provides:       bundled(crate(num-integer)) = 0.1.46
Provides:       bundled(crate(num-iter)) = 0.1.45
Provides:       bundled(crate(num-rational)) = 0.4.2
Provides:       bundled(crate(num-traits)) = 0.2.19
Provides:       bundled(crate(objc)) = 0.2.7
Provides:       bundled(crate(objc2)) = 0.4.1
Provides:       bundled(crate(objc2)) = 0.5.2
Provides:       bundled(crate(objc2-app-kit)) = 0.2.2
Provides:       bundled(crate(objc2-core-data)) = 0.2.2
Provides:       bundled(crate(objc2-core-image)) = 0.2.2
Provides:       bundled(crate(objc2-encode)) = 3.0.0
Provides:       bundled(crate(objc2-encode)) = 4.0.3
Provides:       bundled(crate(objc2-foundation)) = 0.2.2
Provides:       bundled(crate(objc2-metal)) = 0.2.2
Provides:       bundled(crate(objc2-metal-kit)) = 0.2.2
Provides:       bundled(crate(objc2-quartz-core)) = 0.2.2
Provides:       bundled(crate(objc-sys)) = 0.3.5
Provides:       bundled(crate(once_cell)) = 1.20.2
Provides:       bundled(crate(orbclient)) = 0.3.47
Provides:       bundled(crate(ordered-float)) = 4.3.0
Provides:       bundled(crate(ordered-multimap)) = 0.4.3
Provides:       bundled(crate(owned_ttf_parser)) = 0.25.0
Provides:       bundled(crate(parking_lot)) = 0.12.3
Provides:       bundled(crate(parking_lot_core)) = 0.9.10
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(pathdiff)) = 0.2.1
Provides:       bundled(crate(percent-encoding)) = 2.3.1
Provides:       bundled(crate(persy)) = 1.5.1
Provides:       bundled(crate(pest)) = 2.7.13
Provides:       bundled(crate(pest_derive)) = 2.7.13
Provides:       bundled(crate(pest_generator)) = 2.7.13
Provides:       bundled(crate(pest_meta)) = 2.7.13
Provides:       bundled(crate(petgraph)) = 0.6.5
Provides:       bundled(crate(pin-project-lite)) = 0.2.14
Provides:       bundled(crate(pkg-config)) = 0.3.31
Provides:       bundled(crate(platform-dirs)) = 0.3.0
Provides:       bundled(crate(png)) = 0.17.14
Provides:       bundled(crate(polling)) = 3.7.3
Provides:       bundled(crate(pollster)) = 0.3.0
Provides:       bundled(crate(pp-rs)) = 0.2.1
Provides:       bundled(crate(ppv-lite86)) = 0.2.20
Provides:       bundled(crate(presser)) = 0.3.1
Provides:       bundled(crate(proc-macro2)) = 1.0.86
Provides:       bundled(crate(proc-macro-crate)) = 3.2.0
Provides:       bundled(crate(profiling)) = 1.0.15
Provides:       bundled(crate(quick-error)) = 2.0.1
Provides:       bundled(crate(quick-xml)) = 0.36.2
Provides:       bundled(crate(quote)) = 1.0.37
Provides:       bundled(crate(radium)) = 0.7.0
Provides:       bundled(crate(rand)) = 0.8.5
Provides:       bundled(crate(rand_chacha)) = 0.3.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(range-alloc)) = 0.1.3
Provides:       bundled(crate(raw-window-handle)) = 0.6.2
Provides:       bundled(crate(raw-window-metal)) = 0.4.0
Provides:       bundled(crate(rayon)) = 1.10.0
Provides:       bundled(crate(rayon-core)) = 1.12.1
Provides:       bundled(crate(redox_syscall)) = 0.3.5
Provides:       bundled(crate(redox_syscall)) = 0.4.1
Provides:       bundled(crate(redox_syscall)) = 0.5.7
Provides:       bundled(crate(redox_users)) = 0.4.6
Provides:       bundled(crate(regex)) = 1.11.0
Provides:       bundled(crate(regex-automata)) = 0.4.8
Provides:       bundled(crate(regex-syntax)) = 0.8.5
Provides:       bundled(crate(renderdoc-sys)) = 1.1.0
Provides:       bundled(crate(rmp)) = 0.8.14
Provides:       bundled(crate(rmp-serde)) = 1.3.0
Provides:       bundled(crate(ron)) = 0.7.1
Provides:       bundled(crate(rspirv-0.12.0+sdk)) = 1.3.268.0
Provides:       bundled(crate(rustc-hash)) = 1.1.0
Provides:       bundled(crate(rustc-hash)) = 2.0.0
Provides:       bundled(crate(rust-ini)) = 0.18.0
Provides:       bundled(crate(rustix)) = 0.38.37
Provides:       bundled(crate(ryu)) = 1.0.18
Provides:       bundled(crate(same-file)) = 1.0.6
Provides:       bundled(crate(scoped-tls)) = 1.0.1
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(sctk-adwaita)) = 0.8.3
Provides:       bundled(crate(serde)) = 1.0.210
Provides:       bundled(crate(serde_bytes)) = 0.11.15
Provides:       bundled(crate(serde_derive)) = 1.0.210
Provides:       bundled(crate(serde_json)) = 1.0.128
Provides:       bundled(crate(serde_spanned)) = 0.6.8
Provides:       bundled(crate(sha2)) = 0.10.8
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(simd-adler32)) = 0.3.7
Provides:       bundled(crate(slab)) = 0.4.9
Provides:       bundled(crate(slotmap)) = 1.0.7
Provides:       bundled(crate(smallvec)) = 1.13.2
Provides:       bundled(crate(smartstring)) = 1.0.1
Provides:       bundled(crate(smithay-client-toolkit)) = 0.18.1
Provides:       bundled(crate(smol_str)) = 0.2.2
Provides:       bundled(crate(spirq)) = 1.2.2
Provides:       bundled(crate(spirv-0.3.0+sdk)) = 1.3.268.0
Provides:       bundled(crate(spirv-cross2)) = 0.4.6
Provides:       bundled(crate(spirv-cross2-derive)) = 0.1.0
Provides:       bundled(crate(spirv-cross-sys)) = 0.4.2+b28b355
Provides:       bundled(crate(spirv-to-dxil)) = 0.4.7
Provides:       bundled(crate(spirv-to-dxil-sys)) = 0.4.7
Provides:       bundled(crate(spq-core)) = 1.0.5
Provides:       bundled(crate(spq-spvasm)) = 0.1.4
Provides:       bundled(crate(sptr)) = 0.3.2
Provides:       bundled(crate(stable_deref_trait)) = 1.2.0
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(strict-num)) = 0.1.1
Provides:       bundled(crate(strsim)) = 0.10.0
Provides:       bundled(crate(syn)) = 1.0.109
Provides:       bundled(crate(syn)) = 2.0.79
Provides:       bundled(crate(tap)) = 1.0.1
Provides:       bundled(crate(tempfile)) = 3.13.0
Provides:       bundled(crate(termcolor)) = 1.4.1
Provides:       bundled(crate(thiserror)) = 1.0.64
Provides:       bundled(crate(thiserror-impl)) = 1.0.64
Provides:       bundled(crate(tiff)) = 0.9.1
Provides:       bundled(crate(tiny-skia)) = 0.11.4
Provides:       bundled(crate(tiny-skia-path)) = 0.11.4
Provides:       bundled(crate(toml)) = 0.5.11
Provides:       bundled(crate(toml)) = 0.8.19
Provides:       bundled(crate(toml_datetime)) = 0.6.8
Provides:       bundled(crate(toml_edit)) = 0.22.22
Provides:       bundled(crate(tracing)) = 0.1.40
Provides:       bundled(crate(tracing-core)) = 0.1.32
Provides:       bundled(crate(triomphe)) = 0.1.13
Provides:       bundled(crate(ttf-parser)) = 0.25.0
Provides:       bundled(crate(typenum)) = 1.17.0
Provides:       bundled(crate(ucd-trie)) = 0.1.7
Provides:       bundled(crate(unicode-ident)) = 1.0.13
Provides:       bundled(crate(unicode-segmentation)) = 1.12.0
Provides:       bundled(crate(unicode-width)) = 0.1.14
Provides:       bundled(crate(unicode-xid)) = 0.2.6
Provides:       bundled(crate(unsigned-varint)) = 0.8.0
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(vec_extract_if_polyfill)) = 0.1.0
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(virtue)) = 0.0.13
Provides:       bundled(crate(walkdir)) = 2.5.0
Provides:       bundled(crate(wasi-0.11.0+wasi-snapshot)) = preview1
Provides:       bundled(crate(wasm-bindgen)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-backend)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-futures)) = 0.4.43
Provides:       bundled(crate(wasm-bindgen-macro)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 0.2.93
Provides:       bundled(crate(wasm-bindgen-shared)) = 0.2.93
Provides:       bundled(crate(wayland-backend)) = 0.3.7
Provides:       bundled(crate(wayland-client)) = 0.31.6
Provides:       bundled(crate(wayland-csd-frame)) = 0.3.0
Provides:       bundled(crate(wayland-cursor)) = 0.31.6
Provides:       bundled(crate(wayland-protocols)) = 0.31.2
Provides:       bundled(crate(wayland-protocols-plasma)) = 0.2.0
Provides:       bundled(crate(wayland-protocols-wlr)) = 0.2.0
Provides:       bundled(crate(wayland-scanner)) = 0.31.5
Provides:       bundled(crate(wayland-sys)) = 0.31.5
Provides:       bundled(crate(web-sys)) = 0.3.70
Provides:       bundled(crate(web-time)) = 0.2.4
Provides:       bundled(crate(weezl)) = 0.1.8
Provides:       bundled(crate(wgpu)) = 22.1.0
Provides:       bundled(crate(wgpu-core)) = 22.1.0
Provides:       bundled(crate(wgpu-hal)) = 22.0.0
Provides:       bundled(crate(wgpu-types)) = 22.0.0
Provides:       bundled(crate(widestring)) = 1.1.0
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 0.1.9
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows)) = 0.52.0
Provides:       bundled(crate(windows)) = 0.58.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows-core)) = 0.52.0
Provides:       bundled(crate(windows-core)) = 0.58.0
Provides:       bundled(crate(windows_i686_gnu)) = 0.42.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.48.5
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.42.2
Provides:       bundled(crate(windows_i686_msvc)) = 0.48.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows-implement)) = 0.58.0
Provides:       bundled(crate(windows-interface)) = 0.58.0
Provides:       bundled(crate(windows-result)) = 0.2.0
Provides:       bundled(crate(windows-strings)) = 0.1.0
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
Provides:       bundled(crate(winit)) = 0.29.15
Provides:       bundled(crate(winnow)) = 0.6.20
Provides:       bundled(crate(wyz)) = 0.5.1
Provides:       bundled(crate(x11-dl)) = 2.21.0
Provides:       bundled(crate(x11rb)) = 0.13.1
Provides:       bundled(crate(x11rb-protocol)) = 0.13.1
Provides:       bundled(crate(xcursor)) = 0.3.8
Provides:       bundled(crate(xkbcommon-dl)) = 0.4.2
Provides:       bundled(crate(xkeysym)) = 0.2.1
Provides:       bundled(crate(xml-rs)) = 0.8.22
Provides:       bundled(crate(yaml-rust)) = 0.4.5
Provides:       bundled(crate(zerocopy)) = 0.7.35
Provides:       bundled(crate(zerocopy-derive)) = 0.7.35
Provides:       bundled(crate(zigzag)) = 0.1.0
Provides:       bundled(crate(zune-core)) = 0.4.12
Provides:       bundled(crate(zune-jpeg)) = 0.4.13
%endif


%description
%{name} is a preprocessor, compiler, and runtime for RetroArch 'slang'
shaders, rewritten in pure Rust.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{name}-v%{version} -p1 %{?with_vendor:-a1}

sed -e 's|_RPM_SO_VER_|%{soname_ver}|' -i include/librashader_ld.h

cat > %{name}.pc <<'EOF'
prefix=%{_prefix}
exec_prefix=%{_exec_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}
 
Name: %{name}
Description: RetroArch shaders for all
Version: %{version}
Libs: -L${libdir} -lrashader
Cflags: -I${includedir}
EOF

%if %{with vendor}
%cargo_prep -v vendor
%endif

%generate_buildrequires
%if %{with vendor}
%cargo_vendor_manifest
%else
%cargo_generate_buildrequires
%endif

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

patchelf --set-soname librashader.so.%{soname_ver} target/release/liblibrashader_capi.so

%install
mkdir -p %{buildroot}/%{_libdir}/pkgconfig
install -m 0755 target/release/liblibrashader_capi.so \
  %{buildroot}%{_libdir}/librashader.so.%{soname_ver}.%{api_ver}
ln -s librashader.so.%{soname_ver}.%{api_ver} %{buildroot}%{_libdir}/librashader.so.%{soname_ver}
ln -s librashader.so.%{soname_ver} %{buildroot}%{_libdir}/librashader.so

install -pm0644 %{name}.pc %{buildroot}/%{_libdir}/pkgconfig/

mkdir -p %{buildroot}%{_includedir}/%{name}
install -pm0644 include/*.h %{buildroot}%{_includedir}/%{name}/ 


%if %{with check}
%check
%cargo_test
%endif


%files
%license LICENSE-GPL.md
%license LICENSE.md
%license LICENSE.dependencies
%doc BROKEN_SHADERS.md
%doc README.md
%{_libdir}/librashader.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/librashader.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Nov 15 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-1
- 0.5.1

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.4.3-1
- 0.4.3

* Tue Apr 02 2024 Phantom X <megaphantomx at bol dot com dot br> - 0.2.7-1
- Initial spec
