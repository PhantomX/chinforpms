%bcond_with check

# Use vendor tarball
%bcond_without vendor

%global soname_ver 1

%global vendor_hash d7667270d7faefdb0280319f10d05a3a

Name:           librashader
Version:        0.2.7
Release:        1%{?dist}
Summary:        RetroArch shaders for all

License:        MPL-2.0 OR GPL-3.0-only%{?with_vendor: AND ((0BSD OR MIT OR Apache-2.0) AND (Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND BSD-2-Clause AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND BSD-3-Clause AND CC0-1.0 AND (CC0-1.0 OR Apache-2.0) AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND ISC AND MIT AND (MIT OR Apache-2.0) AND ((MIT OR Apache-2.0) AND Unicode-DFS-2016) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND (Unlicense OR MIT) AND Zlib AND (Zlib OR Apache-2.0 OR MIT))}
URL:            https://github.com/SnowflakePowered/%{name}
Source0:        %{url}/archive/%{name}-v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

Patch0:         0001-RPM-fixes.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  rust-packaging
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  patchelf
Requires:       libglvnd-glx%{?_isa}
Requires:       vulkan-loader%{?_isa}

%if %{with vendor}
Provides:       bundled(crate(ab_glyph)) = 32.2.0
Provides:       bundled(crate(ab_glyph_rasterizer)) = 8.1.0
Provides:       bundled(crate(adler)) = 2.0.1
Provides:       bundled(crate(ahash)) = 8.7.0
Provides:       bundled(crate(ahash)) = 11.8.0
Provides:       bundled(crate(aho-corasick)) = 3.1.1
Provides:       bundled(crate(allocator-api2)) = 61.2.0
Provides:       bundled(crate(android-activity)) = 2.5.0
Provides:       bundled(crate(android-properties)) = 2.2.0
Provides:       bundled(crate(android_system_properties)) = 5.1.0
Provides:       bundled(crate(array-concat)) = 2.5.0
Provides:       bundled(crate(array-init)) = 0.1.2
Provides:       bundled(crate(arrayref)) = 7.3.0
Provides:       bundled(crate(arrayvec)) = 4.7.0
Provides:       bundled(crate(ash)) = 152.3.1+3.73.0
Provides:       bundled(crate(ash-window)) = 0.21.0
Provides:       bundled(crate(as-raw-xcb-connection)) = 1.0.1
Provides:       bundled(crate(async-trait)) = 97.1.0
Provides:       bundled(crate(atomic-waker)) = 2.1.1
Provides:       bundled(crate(atty)) = 41.2.0
Provides:       bundled(crate(autocfg)) = 0.2.1
Provides:       bundled(crate(auto_ops)) = 0.3.0
Provides:       bundled(crate(base64)) = 1.31.0
Provides:       bundled(crate(bincode-2.0.0)) = 3.cr
Provides:       bundled(crate(bincode_derive-2.0.0)) = 3.cr
Provides:       bundled(crate(bit_field)) = 2.01.0
Provides:       bundled(crate(bitflags)) = 2.3.1
Provides:       bundled(crate(bitflags)) = 0.5.2
Provides:       bundled(crate(bit-set)) = 3.5.0
Provides:       bundled(crate(bit-vec)) = 3.6.0
Provides:       bundled(crate(bitvec)) = 1.0.1
Provides:       bundled(crate(blake3)) = 1.5.1
Provides:       bundled(crate(block)) = 6.1.0
Provides:       bundled(crate(block2)) = 0.3.0
Provides:       bundled(crate(block2)) = 0.4.0
Provides:       bundled(crate(block-buffer)) = 4.01.0
Provides:       bundled(crate(block-sys)) = 1.2.0
Provides:       bundled(crate(build-target)) = 0.4.0
Provides:       bundled(crate(bumpalo)) = 4.51.3
Provides:       bundled(crate(bytecount)) = 7.6.0
Provides:       bundled(crate(bytemuck)) = 0.51.1
Provides:       bundled(crate(bytemuck_derive)) = 0.6.1
Provides:       bundled(crate(byteorder)) = 0.5.1
Provides:       bundled(crate(bytes)) = 0.6.1
Provides:       bundled(crate(calloop)) = 4.21.0
Provides:       bundled(crate(calloop-wayland-source)) = 0.2.0
Provides:       bundled(crate(cbindgen)) = 0.62.0
Provides:       bundled(crate(cc)) = 09.0.1
Provides:       bundled(crate(cesu8)) = 0.1.1
Provides:       bundled(crate(cfg_aliases)) = 1.1.0
Provides:       bundled(crate(cfg-if)) = 0.0.1
Provides:       bundled(crate(clap)) = 52.2.3
Provides:       bundled(crate(clap)) = 0.1.4
Provides:       bundled(crate(clap_derive)) = 0.1.4
Provides:       bundled(crate(clap_lex)) = 4.2.0
Provides:       bundled(crate(clap_lex)) = 3.3.0
Provides:       bundled(crate(cmake)) = 05.1.0
Provides:       bundled(crate(cocoa)) = 0.52.0
Provides:       bundled(crate(cocoa-foundation)) = 2.1.0
Provides:       bundled(crate(codespan-reporting)) = 1.11.0
Provides:       bundled(crate(color_quant)) = 0.1.1
Provides:       bundled(crate(com)) = 0.6.0
Provides:       bundled(crate(combine)) = 6.6.4
Provides:       bundled(crate(com_macros)) = 0.6.0
Provides:       bundled(crate(com_macros_support)) = 0.6.0
Provides:       bundled(crate(concurrent-queue)) = 0.4.2
Provides:       bundled(crate(config)) = 4.31.0
Provides:       bundled(crate(constant_time_eq)) = 0.3.0
Provides:       bundled(crate(core-foundation)) = 4.9.0
Provides:       bundled(crate(core-foundation-sys)) = 6.8.0
Provides:       bundled(crate(core-graphics)) = 1.32.0
Provides:       bundled(crate(core-graphics-types)) = 3.1.0
Provides:       bundled(crate(cpufeatures)) = 21.2.0
Provides:       bundled(crate(crc)) = 1.0.3
Provides:       bundled(crate(crc32fast)) = 0.4.1
Provides:       bundled(crate(crc-catalog)) = 0.4.2
Provides:       bundled(crate(crossbeam-deque)) = 5.8.0
Provides:       bundled(crate(crossbeam-epoch)) = 81.9.0
Provides:       bundled(crate(crossbeam-utils)) = 91.8.0
Provides:       bundled(crate(crunchy)) = 2.2.0
Provides:       bundled(crate(crypto-common)) = 6.1.0
Provides:       bundled(crate(cty)) = 2.2.0
Provides:       bundled(crate(cursor-icon)) = 0.1.1
Provides:       bundled(crate(d3d12)) = 0.91.0
Provides:       bundled(crate(data-encoding)) = 0.5.2
Provides:       bundled(crate(digest)) = 7.01.0
Provides:       bundled(crate(dirs-next)) = 2.0.1
Provides:       bundled(crate(dirs-sys-next)) = 2.1.0
Provides:       bundled(crate(dispatch)) = 0.2.0
Provides:       bundled(crate(dlib)) = 2.5.0
Provides:       bundled(crate(dlv-list)) = 0.3.0
Provides:       bundled(crate(downcast-rs)) = 0.2.1
Provides:       bundled(crate(either)) = 0.01.1
Provides:       bundled(crate(encoding_rs)) = 33.8.0
Provides:       bundled(crate(env_logger)) = 2.01.0
Provides:       bundled(crate(equivalent)) = 1.0.1
Provides:       bundled(crate(errno)) = 8.3.0
Provides:       bundled(crate(exr)) = 0.27.1
Provides:       bundled(crate(fastrand)) = 2.0.2
Provides:       bundled(crate(fdeflate)) = 4.3.0
Provides:       bundled(crate(fixedbitset)) = 2.4.0
Provides:       bundled(crate(flate2)) = 82.0.1
Provides:       bundled(crate(flume)) = 0.11.0
Provides:       bundled(crate(foreign-types)) = 0.5.0
Provides:       bundled(crate(foreign-types-macros)) = 3.2.0
Provides:       bundled(crate(foreign-types-shared)) = 1.3.0
Provides:       bundled(crate(fs2)) = 3.4.0
Provides:       bundled(crate(funty)) = 0.0.2
Provides:       bundled(crate(generic-array)) = 7.41.0
Provides:       bundled(crate(gethostname)) = 3.4.0
Provides:       bundled(crate(getrandom)) = 21.2.0
Provides:       bundled(crate(gfx-maths)) = 9.2.0
Provides:       bundled(crate(gif)) = 1.31.0
Provides:       bundled(crate(gl)) = 0.41.0
Provides:       bundled(crate(glfw)) = 0.74.0
Provides:       bundled(crate(glfw)) = 1.94.0
Provides:       bundled(crate(glfw-sys)) = 5.3.3+0.0.4
Provides:       bundled(crate(gl_generator)) = 0.41.0
Provides:       bundled(crate(glob)) = 1.3.0
Provides:       bundled(crate(glow)) = 1.31.0
Provides:       bundled(crate(glslang)) = 2.3.0
Provides:       bundled(crate(glslang-sys)) = 2.3.0
Provides:       bundled(crate(glutin_wgl_sys)) = 0.5.0
Provides:       bundled(crate(gpu-alloc)) = 0.6.0
Provides:       bundled(crate(gpu-allocator)) = 0.52.0
Provides:       bundled(crate(gpu-alloc-types)) = 0.3.0
Provides:       bundled(crate(gpu-descriptor)) = 4.2.0
Provides:       bundled(crate(gpu-descriptor-types)) = 2.1.0
Provides:       bundled(crate(half)) = 0.4.2
Provides:       bundled(crate(halfbrown)) = 5.2.0
Provides:       bundled(crate(hashbrown)) = 3.21.0
Provides:       bundled(crate(hashbrown)) = 3.41.0
Provides:       bundled(crate(hassle-rs)) = 0.11.0
Provides:       bundled(crate(heck)) = 1.4.0
Provides:       bundled(crate(hermit-abi)) = 91.1.0
Provides:       bundled(crate(hermit-abi)) = 9.3.0
Provides:       bundled(crate(hexf-parse)) = 1.2.0
Provides:       bundled(crate(humantime)) = 0.1.2
Provides:       bundled(crate(icrate)) = 4.0.0
Provides:       bundled(crate(icrate)) = 0.1.0
Provides:       bundled(crate(image)) = 9.42.0
Provides:       bundled(crate(indexmap)) = 3.9.1
Provides:       bundled(crate(indexmap)) = 6.2.2
Provides:       bundled(crate(is-terminal)) = 21.4.0
Provides:       bundled(crate(itoa)) = 11.0.1
Provides:       bundled(crate(jni)) = 1.12.0
Provides:       bundled(crate(jni-sys)) = 0.3.0
Provides:       bundled(crate(jobserver)) = 82.1.0
Provides:       bundled(crate(jpeg-decoder)) = 1.3.0
Provides:       bundled(crate(json5)) = 1.4.0
Provides:       bundled(crate(js-sys)) = 96.3.0
Provides:       bundled(crate(khronos_api)) = 0.1.3
Provides:       bundled(crate(khronos-egl)) = 0.0.6
Provides:       bundled(crate(lazy_static)) = 0.4.1
Provides:       bundled(crate(lebe)) = 2.5.0
Provides:       bundled(crate(libc)) = 351.2.0
Provides:       bundled(crate(libloading)) = 4.7.0
Provides:       bundled(crate(libloading)) = 3.8.0
Provides:       bundled(crate(librashader-spirv-cross)) = 1.52.0
Provides:       bundled(crate(libredox)) = 2.0.0
Provides:       bundled(crate(libredox)) = 3.1.0
Provides:       bundled(crate(linked-hash-map)) = 6.5.0
Provides:       bundled(crate(linux-raw-sys)) = 31.4.0
Provides:       bundled(crate(lock_api)) = 11.4.0
Provides:       bundled(crate(log)) = 12.4.0
Provides:       bundled(crate(mach-siegbert-vogt-dxcsa)) = 3.1.0
Provides:       bundled(crate(malloc_buf)) = 6.0.0
Provides:       bundled(crate(matches)) = 01.1.0
Provides:       bundled(crate(memchr)) = 2.7.2
Provides:       bundled(crate(memmap2)) = 4.9.0
Provides:       bundled(crate(metal)) = 0.72.0
Provides:       bundled(crate(minimal-lexical)) = 1.2.0
Provides:       bundled(crate(miniz_oxide)) = 2.7.0
Provides:       bundled(crate(naga)) = 2.91.0
Provides:       bundled(crate(ndk)) = 0.8.0
Provides:       bundled(crate(ndk-context)) = 1.1.0
Provides:       bundled(crate(ndk-sys)) = 3569159.2.52+0.5.0
Provides:       bundled(crate(nom)) = 3.1.7
Provides:       bundled(crate(nom_locate)) = 0.2.4
Provides:       bundled(crate(num)) = 1.4.0
Provides:       bundled(crate(num-bigint)) = 4.4.0
Provides:       bundled(crate(num-complex)) = 5.4.0
Provides:       bundled(crate(num_enum)) = 2.7.0
Provides:       bundled(crate(num_enum_derive)) = 2.7.0
Provides:       bundled(crate(num-integer)) = 64.1.0
Provides:       bundled(crate(num-iter)) = 44.1.0
Provides:       bundled(crate(num-rational)) = 1.4.0
Provides:       bundled(crate(num-traits)) = 81.2.0
Provides:       bundled(crate(objc)) = 7.2.0
Provides:       bundled(crate(objc2)) = 1.4.0
Provides:       bundled(crate(objc2)) = 0.5.0
Provides:       bundled(crate(objc2-encode)) = 0.0.3
Provides:       bundled(crate(objc2-encode)) = 0.0.4
Provides:       bundled(crate(objc_exception)) = 2.1.0
Provides:       bundled(crate(objc-sys)) = 2.3.0
Provides:       bundled(crate(once_cell)) = 0.91.1
Provides:       bundled(crate(orbclient)) = 74.3.0
Provides:       bundled(crate(ordered-multimap)) = 3.4.0
Provides:       bundled(crate(os_str_bytes)) = 1.6.6
Provides:       bundled(crate(owned_ttf_parser)) = 0.02.0
Provides:       bundled(crate(parking_lot)) = 1.21.0
Provides:       bundled(crate(parking_lot_core)) = 9.9.0
Provides:       bundled(crate(paste)) = 41.0.1
Provides:       bundled(crate(pathdiff)) = 1.2.0
Provides:       bundled(crate(percent-encoding)) = 1.3.2
Provides:       bundled(crate(persy)) = 0.5.1
Provides:       bundled(crate(pest)) = 9.7.2
Provides:       bundled(crate(pest_derive)) = 9.7.2
Provides:       bundled(crate(pest_generator)) = 9.7.2
Provides:       bundled(crate(pest_meta)) = 9.7.2
Provides:       bundled(crate(petgraph)) = 4.6.0
Provides:       bundled(crate(pin-project-lite)) = 41.2.0
Provides:       bundled(crate(pkg-config)) = 03.3.0
Provides:       bundled(crate(platform-dirs)) = 0.3.0
Provides:       bundled(crate(png)) = 31.71.0
Provides:       bundled(crate(polling)) = 0.6.3
Provides:       bundled(crate(pollster)) = 0.3.0
Provides:       bundled(crate(ppv-lite86)) = 71.2.0
Provides:       bundled(crate(presser)) = 1.3.0
Provides:       bundled(crate(proc-macro2)) = 97.0.1
Provides:       bundled(crate(proc-macro-crate)) = 0.1.3
Provides:       bundled(crate(proc-macro-error)) = 4.0.1
Provides:       bundled(crate(proc-macro-error-attr)) = 4.0.1
Provides:       bundled(crate(profiling)) = 51.0.1
Provides:       bundled(crate(qoi)) = 1.4.0
Provides:       bundled(crate(quick-xml)) = 0.13.0
Provides:       bundled(crate(quote)) = 53.0.1
Provides:       bundled(crate(radium)) = 0.7.0
Provides:       bundled(crate(rand)) = 5.8.0
Provides:       bundled(crate(rand_chacha)) = 1.3.0
Provides:       bundled(crate(rand_core)) = 4.6.0
Provides:       bundled(crate(range-alloc)) = 3.1.0
Provides:       bundled(crate(raw-window-handle)) = 3.4.0
Provides:       bundled(crate(raw-window-handle)) = 2.5.0
Provides:       bundled(crate(raw-window-handle)) = 0.6.0
Provides:       bundled(crate(raw-window-metal)) = 2.3.0
Provides:       bundled(crate(rayon)) = 0.01.1
Provides:       bundled(crate(rayon-core)) = 1.21.1
Provides:       bundled(crate(redox_syscall)) = 5.3.0
Provides:       bundled(crate(redox_syscall)) = 1.4.0
Provides:       bundled(crate(redox_users)) = 5.4.0
Provides:       bundled(crate(regex)) = 4.01.1
Provides:       bundled(crate(regex-automata)) = 6.4.0
Provides:       bundled(crate(regex-syntax)) = 3.8.0
Provides:       bundled(crate(renderdoc-sys)) = 0.1.1
Provides:       bundled(crate(ron)) = 1.7.0
Provides:       bundled(crate(rspirv-0.12.0+sdk)) = 0.862.3.1
Provides:       bundled(crate(rustc-hash)) = 0.1.1
Provides:       bundled(crate(rust-ini)) = 0.81.0
Provides:       bundled(crate(rustix)) = 23.83.0
Provides:       bundled(crate(rustversion)) = 41.0.1
Provides:       bundled(crate(ryu)) = 71.0.1
Provides:       bundled(crate(same-file)) = 6.0.1
Provides:       bundled(crate(scoped-tls)) = 1.0.1
Provides:       bundled(crate(scopeguard)) = 0.2.1
Provides:       bundled(crate(sctk-adwaita)) = 1.8.0
Provides:       bundled(crate(serde)) = 791.0.1
Provides:       bundled(crate(serde_derive)) = 791.0.1
Provides:       bundled(crate(serde_json)) = 511.0.1
Provides:       bundled(crate(sha2)) = 8.01.0
Provides:       bundled(crate(simd-adler32)) = 7.3.0
Provides:       bundled(crate(slab)) = 9.4.0
Provides:       bundled(crate(slotmap)) = 7.0.1
Provides:       bundled(crate(smallvec)) = 2.31.1
Provides:       bundled(crate(smithay-client-toolkit)) = 1.81.0
Provides:       bundled(crate(smol_str)) = 1.2.0
Provides:       bundled(crate(spin)) = 8.9.0
Provides:       bundled(crate(spirv-0.3.0+sdk)) = 0.862.3.1
Provides:       bundled(crate(spirv-to-dxil)) = 7.4.0
Provides:       bundled(crate(spirv-to-dxil-sys)) = 7.4.0
Provides:       bundled(crate(sptr)) = 2.3.0
Provides:       bundled(crate(static_assertions)) = 0.1.1
Provides:       bundled(crate(strict-num)) = 1.1.0
Provides:       bundled(crate(strsim)) = 0.01.0
Provides:       bundled(crate(syn)) = 901.0.1
Provides:       bundled(crate(syn)) = 75.0.2
Provides:       bundled(crate(tap)) = 1.0.1
Provides:       bundled(crate(tempfile)) = 1.01.3
Provides:       bundled(crate(termcolor)) = 1.4.1
Provides:       bundled(crate(textwrap)) = 1.61.0
Provides:       bundled(crate(thiserror)) = 85.0.1
Provides:       bundled(crate(thiserror-impl)) = 85.0.1
Provides:       bundled(crate(tiff)) = 1.9.0
Provides:       bundled(crate(tinymap)) = 0.4.0
Provides:       bundled(crate(tiny-skia)) = 4.11.0
Provides:       bundled(crate(tiny-skia-path)) = 4.11.0
Provides:       bundled(crate(tinyvec)) = 0.6.1
Provides:       bundled(crate(toml)) = 11.5.0
Provides:       bundled(crate(toml_datetime)) = 5.6.0
Provides:       bundled(crate(toml_edit)) = 1.12.0
Provides:       bundled(crate(tracing)) = 04.1.0
Provides:       bundled(crate(tracing-core)) = 23.1.0
Provides:       bundled(crate(ttf-parser)) = 0.02.0
Provides:       bundled(crate(typenum)) = 0.71.1
Provides:       bundled(crate(ucd-trie)) = 6.1.0
Provides:       bundled(crate(unicode-ident)) = 21.0.1
Provides:       bundled(crate(unicode-segmentation)) = 0.11.1
Provides:       bundled(crate(unicode-width)) = 11.1.0
Provides:       bundled(crate(unicode-xid)) = 4.2.0
Provides:       bundled(crate(unsigned-varint)) = 0.8.0
Provides:       bundled(crate(version_check)) = 4.9.0
Provides:       bundled(crate(virtue)) = 31.0.0
Provides:       bundled(crate(walkdir)) = 0.5.2
Provides:       bundled(crate(wasi-0.11.0+wasi-snapshot)) = 1weiverp
Provides:       bundled(crate(wasm-bindgen)) = 29.2.0
Provides:       bundled(crate(wasm-bindgen-backend)) = 29.2.0
Provides:       bundled(crate(wasm-bindgen-futures)) = 24.4.0
Provides:       bundled(crate(wasm-bindgen-macro)) = 29.2.0
Provides:       bundled(crate(wasm-bindgen-macro-support)) = 29.2.0
Provides:       bundled(crate(wasm-bindgen-shared)) = 29.2.0
Provides:       bundled(crate(wayland-backend)) = 3.3.0
Provides:       bundled(crate(wayland-client)) = 2.13.0
Provides:       bundled(crate(wayland-csd-frame)) = 0.3.0
Provides:       bundled(crate(wayland-cursor)) = 1.13.0
Provides:       bundled(crate(wayland-protocols)) = 2.13.0
Provides:       bundled(crate(wayland-protocols-plasma)) = 0.2.0
Provides:       bundled(crate(wayland-protocols-wlr)) = 0.2.0
Provides:       bundled(crate(wayland-scanner)) = 1.13.0
Provides:       bundled(crate(wayland-sys)) = 1.13.0
Provides:       bundled(crate(web-sys)) = 96.3.0
Provides:       bundled(crate(web-time)) = 4.2.0
Provides:       bundled(crate(weezl)) = 8.1.0
Provides:       bundled(crate(wgpu)) = 3.91.0
Provides:       bundled(crate(wgpu-core)) = 3.91.0
Provides:       bundled(crate(wgpu-hal)) = 3.91.0
Provides:       bundled(crate(wgpu-types)) = 2.91.0
Provides:       bundled(crate(widestring)) = 2.0.1
Provides:       bundled(crate(winapi)) = 9.3.0
Provides:       bundled(crate(winapi-i686-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(winapi-util)) = 6.1.0
Provides:       bundled(crate(winapi-x86_64-pc-windows-gnu)) = 0.4.0
Provides:       bundled(crate(windows)) = 0.25.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 2.24.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 5.84.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 4.25.0
Provides:       bundled(crate(windows_aarch64_msvc)) = 2.24.0
Provides:       bundled(crate(windows_aarch64_msvc)) = 5.84.0
Provides:       bundled(crate(windows_aarch64_msvc)) = 4.25.0
Provides:       bundled(crate(windows-core)) = 0.25.0
Provides:       bundled(crate(windows_i686_gnu)) = 2.24.0
Provides:       bundled(crate(windows_i686_gnu)) = 5.84.0
Provides:       bundled(crate(windows_i686_gnu)) = 4.25.0
Provides:       bundled(crate(windows_i686_msvc)) = 2.24.0
Provides:       bundled(crate(windows_i686_msvc)) = 5.84.0
Provides:       bundled(crate(windows_i686_msvc)) = 4.25.0
Provides:       bundled(crate(windows-sys)) = 0.54.0
Provides:       bundled(crate(windows-sys)) = 0.84.0
Provides:       bundled(crate(windows-sys)) = 0.25.0
Provides:       bundled(crate(windows-targets)) = 2.24.0
Provides:       bundled(crate(windows-targets)) = 5.84.0
Provides:       bundled(crate(windows-targets)) = 4.25.0
Provides:       bundled(crate(windows_x86_64_gnu)) = 2.24.0
Provides:       bundled(crate(windows_x86_64_gnu)) = 5.84.0
Provides:       bundled(crate(windows_x86_64_gnu)) = 4.25.0
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 2.24.0
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 5.84.0
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 4.25.0
Provides:       bundled(crate(windows_x86_64_msvc)) = 2.24.0
Provides:       bundled(crate(windows_x86_64_msvc)) = 5.84.0
Provides:       bundled(crate(windows_x86_64_msvc)) = 4.25.0
Provides:       bundled(crate(winit)) = 51.92.0
Provides:       bundled(crate(winnow)) = 04.5.0
Provides:       bundled(crate(wyz)) = 1.5.0
Provides:       bundled(crate(x11-dl)) = 0.12.2
Provides:       bundled(crate(x11rb)) = 0.31.0
Provides:       bundled(crate(x11rb-protocol)) = 0.31.0
Provides:       bundled(crate(xcursor)) = 5.3.0
Provides:       bundled(crate(xkbcommon-dl)) = 2.4.0
Provides:       bundled(crate(xkeysym)) = 0.2.0
Provides:       bundled(crate(xml-rs)) = 02.8.0
Provides:       bundled(crate(yaml-rust)) = 5.4.0
Provides:       bundled(crate(zerocopy)) = 23.7.0
Provides:       bundled(crate(zerocopy-derive)) = 23.7.0
Provides:       bundled(crate(zigzag)) = 0.1.0
Provides:       bundled(crate(zune-inflate)) = 45.2.0
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
sed -e '/halfbrown/s|0.2.4|0.2.5|' -i %{name}/Cargo.toml
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
  %{buildroot}%{_libdir}/librashader.so.%{soname_ver}
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
%{_libdir}/librashader.so.%{soname_ver}

%files devel
%{_includedir}/%{name}
%{_libdir}/librashader.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Apr 02 2024 Phantom X <megaphantomx at bol dot com dot br> - 0.2.7-1
- Initial spec
