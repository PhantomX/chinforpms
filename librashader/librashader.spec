%bcond check 0

# Use vendor tarball
%bcond vendor 1

%global soname_ver 2
%global api_ver 2

%global vendor_hash 357cfe9fa3294298d82fcd1205aa9660

Name:           librashader
Version:        0.8.1
Release:        2%{?dist}
Summary:        RetroArch shaders for all

License:        MPL-2.0 OR GPL-3.0-only%{?with_vendor: AND ((0BSD OR MIT OR Apache-2.0) AND (Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND BSD-2-Clause AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND BSD-3-Clause AND CC0-1.0 AND (CC0-1.0 OR Apache-2.0) AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND ISC AND MIT AND (MIT OR Apache-2.0) AND ((MIT OR Apache-2.0) AND Unicode-DFS-2016) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND (Unlicense OR MIT) AND Zlib AND (Zlib OR Apache-2.0 OR MIT))}
URL:            https://github.com/SnowflakePowered/%{name}
Source0:        %{url}/archive/%{name}-v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# rust2rpm -t fedora -V auto --no-rpmautospec --ignore-missing-license-files --path <path>
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-capi-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-capi-%{version}-vendor.tar.xz
%endif

Patch0:         0001-RPM-fixes.patch
Patch1:         %{name}-9909b6d.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  cmake
BuildRequires:  rust-packaging
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  make
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
Provides:       bundled(crate(ahash)) = 0.8.12
Provides:       bundled(crate(aho)) = 1.1.3
Provides:       bundled(crate(allocator)) = 0.2.21
Provides:       bundled(crate(android)) = 0.5.2
Provides:       bundled(crate(android)) = 0.2.2
Provides:       bundled(crate(anstream)) = 0.3.2
Provides:       bundled(crate(anstyle)) = 1.0.10
Provides:       bundled(crate(anstyle)) = 0.2.6
Provides:       bundled(crate(anstyle)) = 1.1.2
Provides:       bundled(crate(anstyle)) = 1.0.2
Provides:       bundled(crate(anyhow)) = 1.0.98
Provides:       bundled(crate(arc)) = 1.7.1
Provides:       bundled(crate(array)) = 0.5.5
Provides:       bundled(crate(array)) = 2.1.0
Provides:       bundled(crate(arrayref)) = 0.3.9
Provides:       bundled(crate(arrayvec)) = 0.7.6
Provides:       bundled(crate(ash)) = 0.38.0+1.3.281
Provides:       bundled(crate(ash)) = 0.13.0
Provides:       bundled(crate(as)) = 1.0.1
Provides:       bundled(crate(async)) = 0.1.88
Provides:       bundled(crate(atomic)) = 1.1.2
Provides:       bundled(crate(autocfg)) = 1.4.0
Provides:       bundled(crate(auto_ops)) = 0.3.0
Provides:       bundled(crate(base64)) = 0.13.1
Provides:       bundled(crate(base64)) = 0.22.1
Provides:       bundled(crate(bincode)) = 2.0.1
Provides:       bundled(crate(bincode_derive)) = 2.0.1
Provides:       bundled(crate(bitflags)) = 1.3.2
Provides:       bundled(crate(bitflags)) = 2.9.1
Provides:       bundled(crate(bit)) = 0.8.0
Provides:       bundled(crate(bit)) = 0.8.0
Provides:       bundled(crate(bitvec)) = 1.0.1
Provides:       bundled(crate(blake3)) = 1.8.2
Provides:       bundled(crate(block)) = 0.1.6
Provides:       bundled(crate(block2)) = 0.3.0
Provides:       bundled(crate(block2)) = 0.6.1
Provides:       bundled(crate(block)) = 0.10.4
Provides:       bundled(crate(block)) = 0.2.1
Provides:       bundled(crate(build)) = 0.4.0
Provides:       bundled(crate(bumpalo)) = 3.17.0
Provides:       bundled(crate(bytecount)) = 0.6.8
Provides:       bundled(crate(bytemuck)) = 1.23.0
Provides:       bundled(crate(bytemuck_derive)) = 1.9.3
Provides:       bundled(crate(byteorder)) = 1.5.0
Provides:       bundled(crate(byteorder)) = 0.1.0
Provides:       bundled(crate(bytes)) = 1.10.1
Provides:       bundled(crate(calloop)) = 0.12.4
Provides:       bundled(crate(calloop)) = 0.2.0
Provides:       bundled(crate(carlog)) = 0.1.0
Provides:       bundled(crate(cbindgen)) = 0.27.0
Provides:       bundled(crate(cc)) = 1.2.23
Provides:       bundled(crate(cesu8)) = 1.1.0
Provides:       bundled(crate(cfg_aliases)) = 0.1.1
Provides:       bundled(crate(cfg_aliases)) = 0.2.1
Provides:       bundled(crate(cfg)) = 1.0.0
Provides:       bundled(crate(clap)) = 4.3.0
Provides:       bundled(crate(clap_builder)) = 4.3.0
Provides:       bundled(crate(clap_derive)) = 4.3.0
Provides:       bundled(crate(clap_lex)) = 0.5.1
Provides:       bundled(crate(cmake)) = 0.1.54
Provides:       bundled(crate(cocoa)) = 0.25.0
Provides:       bundled(crate(cocoa)) = 0.1.2
Provides:       bundled(crate(codespan)) = 0.12.0
Provides:       bundled(crate(colorchoice)) = 1.0.3
Provides:       bundled(crate(colored)) = 2.2.0
Provides:       bundled(crate(combine)) = 4.6.7
Provides:       bundled(crate(concurrent)) = 2.5.0
Provides:       bundled(crate(config)) = 0.13.4
Provides:       bundled(crate(constant_time_eq)) = 0.3.1
Provides:       bundled(crate(core)) = 0.9.4
Provides:       bundled(crate(core)) = 0.8.7
Provides:       bundled(crate(core)) = 0.23.2
Provides:       bundled(crate(core)) = 0.1.3
Provides:       bundled(crate(cpufeatures)) = 0.2.17
Provides:       bundled(crate(crc32fast)) = 1.4.2
Provides:       bundled(crate(crc)) = 3.3.0
Provides:       bundled(crate(crc)) = 2.4.0
Provides:       bundled(crate(crossbeam)) = 0.8.6
Provides:       bundled(crate(crossbeam)) = 0.9.18
Provides:       bundled(crate(crossbeam)) = 0.8.21
Provides:       bundled(crate(crunchy)) = 0.2.3
Provides:       bundled(crate(crypto)) = 0.1.6
Provides:       bundled(crate(cursor)) = 1.1.0
Provides:       bundled(crate(d3d12)) = 0.2.0
Provides:       bundled(crate(data)) = 2.9.0
Provides:       bundled(crate(digest)) = 0.10.7
Provides:       bundled(crate(dirs)) = 1.0.2
Provides:       bundled(crate(dirs)) = 0.1.2
Provides:       bundled(crate(dispatch)) = 0.2.0
Provides:       bundled(crate(dispatch2)) = 0.3.0
Provides:       bundled(crate(dlib)) = 0.5.2
Provides:       bundled(crate(dlv)) = 0.3.0
Provides:       bundled(crate(document)) = 0.2.11
Provides:       bundled(crate(downcast)) = 1.2.1
Provides:       bundled(crate(either)) = 1.15.0
Provides:       bundled(crate(encoding_rs)) = 0.8.35
Provides:       bundled(crate(env_logger)) = 0.10.2
Provides:       bundled(crate(equivalent)) = 1.0.2
Provides:       bundled(crate(errno)) = 0.3.12
Provides:       bundled(crate(fastrand)) = 2.3.0
Provides:       bundled(crate(fdeflate)) = 0.3.7
Provides:       bundled(crate(fixedbitset)) = 0.5.7
Provides:       bundled(crate(flate2)) = 1.1.1
Provides:       bundled(crate(fnv)) = 1.0.7
Provides:       bundled(crate(foldhash)) = 0.1.5
Provides:       bundled(crate(foreign)) = 0.5.0
Provides:       bundled(crate(foreign)) = 0.2.3
Provides:       bundled(crate(foreign)) = 0.3.1
Provides:       bundled(crate(fs2)) = 0.4.3
Provides:       bundled(crate(funty)) = 2.0.0
Provides:       bundled(crate(generic)) = 0.14.7
Provides:       bundled(crate(gethostname)) = 0.4.3
Provides:       bundled(crate(getrandom)) = 0.2.16
Provides:       bundled(crate(getrandom)) = 0.3.3
Provides:       bundled(crate(gfx)) = 0.2.9
Provides:       bundled(crate(glfw)) = 0.59.0
Provides:       bundled(crate(glfw)) = 5.0.0+3.3.9
Provides:       bundled(crate(glob)) = 0.3.2
Provides:       bundled(crate(glow)) = 0.16.0
Provides:       bundled(crate(glslang)) = 0.6.2
Provides:       bundled(crate(glslang)) = 0.7.0+1062752
Provides:       bundled(crate(gpu)) = 0.27.0
Provides:       bundled(crate(half)) = 2.6.0
Provides:       bundled(crate(halfbrown)) = 0.2.5
Provides:       bundled(crate(hashbrown)) = 0.12.3
Provides:       bundled(crate(hashbrown)) = 0.14.5
Provides:       bundled(crate(hashbrown)) = 0.15.3
Provides:       bundled(crate(heck)) = 0.4.1
Provides:       bundled(crate(heck)) = 0.5.0
Provides:       bundled(crate(hermit)) = 0.4.0
Provides:       bundled(crate(hermit)) = 0.5.1
Provides:       bundled(crate(hexf)) = 0.2.1
Provides:       bundled(crate(humantime)) = 2.2.0
Provides:       bundled(crate(icrate)) = 0.0.4
Provides:       bundled(crate(image)) = 0.25.6
Provides:       bundled(crate(image)) = 0.4.1
Provides:       bundled(crate(indexmap)) = 2.9.0
Provides:       bundled(crate(is)) = 0.4.16
Provides:       bundled(crate(itertools)) = 0.12.1
Provides:       bundled(crate(itoa)) = 1.0.15
Provides:       bundled(crate(jni)) = 0.21.1
Provides:       bundled(crate(jni)) = 0.3.0
Provides:       bundled(crate(jobserver)) = 0.1.33
Provides:       bundled(crate(json5)) = 0.4.1
Provides:       bundled(crate(js)) = 0.3.77
Provides:       bundled(crate(lazy_static)) = 1.5.0
Provides:       bundled(crate(libc)) = 0.2.172
Provides:       bundled(crate(libloading)) = 0.8.7
Provides:       bundled(crate(libm)) = 0.2.15
Provides:       bundled(crate(libredox)) = 0.1.3
Provides:       bundled(crate(linked)) = 0.5.6
Provides:       bundled(crate(linux)) = 0.4.15
Provides:       bundled(crate(linux)) = 0.9.4
Provides:       bundled(crate(litrs)) = 0.4.1
Provides:       bundled(crate(lock_api)) = 0.4.12
Provides:       bundled(crate(log)) = 0.4.27
Provides:       bundled(crate(mach)) = 0.1.3
Provides:       bundled(crate(malloc_buf)) = 0.0.6
Provides:       bundled(crate(memchr)) = 2.7.4
Provides:       bundled(crate(memmap2)) = 0.9.5
Provides:       bundled(crate(metal)) = 0.31.0
Provides:       bundled(crate(minimal)) = 0.2.1
Provides:       bundled(crate(miniz_oxide)) = 0.8.8
Provides:       bundled(crate(naga)) = 25.0.1
Provides:       bundled(crate(ndk)) = 0.8.0
Provides:       bundled(crate(ndk)) = 0.1.1
Provides:       bundled(crate(ndk)) = 0.5.0+25.2.9519653
Provides:       bundled(crate(nom)) = 7.1.3
Provides:       bundled(crate(nom)) = 8.0.0
Provides:       bundled(crate(nom_locate)) = 5.0.0
Provides:       bundled(crate(num)) = 0.4.3
Provides:       bundled(crate(num)) = 0.4.6
Provides:       bundled(crate(num)) = 0.4.6
Provides:       bundled(crate(num)) = 0.4.2
Provides:       bundled(crate(num_enum)) = 0.7.3
Provides:       bundled(crate(num_enum_derive)) = 0.7.3
Provides:       bundled(crate(num)) = 0.1.46
Provides:       bundled(crate(num)) = 0.1.45
Provides:       bundled(crate(num)) = 0.4.2
Provides:       bundled(crate(num)) = 0.2.19
Provides:       bundled(crate(objc)) = 0.2.7
Provides:       bundled(crate(objc2)) = 0.4.1
Provides:       bundled(crate(objc2)) = 0.5.2
Provides:       bundled(crate(objc2)) = 0.6.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 3.0.0
Provides:       bundled(crate(objc2)) = 4.1.0
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc2)) = 0.3.1
Provides:       bundled(crate(objc)) = 0.3.5
Provides:       bundled(crate(once_cell)) = 1.21.3
Provides:       bundled(crate(orbclient)) = 0.3.48
Provides:       bundled(crate(ordered)) = 4.6.0
Provides:       bundled(crate(ordered)) = 0.4.3
Provides:       bundled(crate(owned_ttf_parser)) = 0.25.0
Provides:       bundled(crate(parking_lot)) = 0.12.3
Provides:       bundled(crate(parking_lot_core)) = 0.9.10
Provides:       bundled(crate(paste)) = 1.0.15
Provides:       bundled(crate(pathdiff)) = 0.2.3
Provides:       bundled(crate(percent)) = 2.3.1
Provides:       bundled(crate(persy)) = 1.6.0
Provides:       bundled(crate(pest)) = 2.8.0
Provides:       bundled(crate(pest_derive)) = 2.8.0
Provides:       bundled(crate(pest_generator)) = 2.8.0
Provides:       bundled(crate(pest_meta)) = 2.8.0
Provides:       bundled(crate(petgraph)) = 0.8.1
Provides:       bundled(crate(pin)) = 0.2.16
Provides:       bundled(crate(pkg)) = 0.3.32
Provides:       bundled(crate(platform)) = 0.3.0
Provides:       bundled(crate(png)) = 0.17.16
Provides:       bundled(crate(polling)) = 3.7.4
Provides:       bundled(crate(pollster)) = 0.3.0
Provides:       bundled(crate(pollster)) = 0.4.0
Provides:       bundled(crate(portable)) = 1.11.0
Provides:       bundled(crate(pp)) = 0.2.1
Provides:       bundled(crate(ppv)) = 0.2.21
Provides:       bundled(crate(presser)) = 0.3.1
Provides:       bundled(crate(proc)) = 1.0.95
Provides:       bundled(crate(proc)) = 3.3.0
Provides:       bundled(crate(profiling)) = 1.0.16
Provides:       bundled(crate(quick)) = 0.37.5
Provides:       bundled(crate(quote)) = 1.0.40
Provides:       bundled(crate(radium)) = 0.7.0
Provides:       bundled(crate(rand)) = 0.8.5
Provides:       bundled(crate(rand_chacha)) = 0.3.1
Provides:       bundled(crate(rand_core)) = 0.6.4
Provides:       bundled(crate(range)) = 0.1.4
Provides:       bundled(crate(raw)) = 0.6.2
Provides:       bundled(crate(raw)) = 0.4.0
Provides:       bundled(crate(rayon)) = 1.10.0
Provides:       bundled(crate(rayon)) = 1.12.1
Provides:       bundled(crate(redox_syscall)) = 0.3.5
Provides:       bundled(crate(redox_syscall)) = 0.5.12
Provides:       bundled(crate(redox_users)) = 0.4.6
Provides:       bundled(crate(r)) = 5.2.0
Provides:       bundled(crate(regex)) = 1.11.1
Provides:       bundled(crate(regex)) = 0.4.9
Provides:       bundled(crate(regex)) = 0.8.5
Provides:       bundled(crate(renderdoc)) = 1.1.0
Provides:       bundled(crate(rmp)) = 0.8.14
Provides:       bundled(crate(rmp)) = 1.3.0
Provides:       bundled(crate(ron)) = 0.7.1
Provides:       bundled(crate(rspirv)) = 1.3.268.0
Provides:       bundled(crate(rustc)) = 1.1.0
Provides:       bundled(crate(rustc)) = 2.1.1
Provides:       bundled(crate(rust)) = 0.18.0
Provides:       bundled(crate(rustix)) = 0.38.44
Provides:       bundled(crate(rustix)) = 1.0.7
Provides:       bundled(crate(rustversion)) = 1.0.20
Provides:       bundled(crate(ryu)) = 1.0.20
Provides:       bundled(crate(same)) = 1.0.6
Provides:       bundled(crate(scoped)) = 1.0.1
Provides:       bundled(crate(scopeguard)) = 1.2.0
Provides:       bundled(crate(sctk)) = 0.8.3
Provides:       bundled(crate(serde)) = 1.0.219
Provides:       bundled(crate(serde_bytes)) = 0.11.17
Provides:       bundled(crate(serde_derive)) = 1.0.219
Provides:       bundled(crate(serde_json)) = 1.0.140
Provides:       bundled(crate(serde_spanned)) = 0.6.8
Provides:       bundled(crate(sha2)) = 0.10.9
Provides:       bundled(crate(shlex)) = 1.3.0
Provides:       bundled(crate(simd)) = 0.3.7
Provides:       bundled(crate(slab)) = 0.4.9
Provides:       bundled(crate(slotmap)) = 1.0.7
Provides:       bundled(crate(smallvec)) = 1.15.0
Provides:       bundled(crate(smartstring)) = 1.0.1
Provides:       bundled(crate(smithay)) = 0.18.1
Provides:       bundled(crate(smol_str)) = 0.2.2
Provides:       bundled(crate(spirq)) = 1.2.2
Provides:       bundled(crate(spirv)) = 1.3.268.0
Provides:       bundled(crate(spirv)) = 0.4.6
Provides:       bundled(crate(spirv)) = 0.1.0
Provides:       bundled(crate(spirv)) = 0.4.3+e670b39
Provides:       bundled(crate(spirv)) = 0.4.7
Provides:       bundled(crate(spirv)) = 0.4.7
Provides:       bundled(crate(spq)) = 1.0.6
Provides:       bundled(crate(spq)) = 0.1.4
Provides:       bundled(crate(sptr)) = 0.3.2
Provides:       bundled(crate(stable_deref_trait)) = 1.2.0
Provides:       bundled(crate(static_assertions)) = 1.1.0
Provides:       bundled(crate(strict)) = 0.1.1
Provides:       bundled(crate(strsim)) = 0.10.0
Provides:       bundled(crate(strum)) = 0.26.3
Provides:       bundled(crate(strum_macros)) = 0.26.4
Provides:       bundled(crate(syn)) = 2.0.101
Provides:       bundled(crate(tap)) = 1.0.1
Provides:       bundled(crate(tempfile)) = 3.20.0
Provides:       bundled(crate(termcolor)) = 1.4.1
Provides:       bundled(crate(thiserror)) = 1.0.69
Provides:       bundled(crate(thiserror)) = 2.0.12
Provides:       bundled(crate(thiserror)) = 1.0.69
Provides:       bundled(crate(thiserror)) = 2.0.12
Provides:       bundled(crate(tiny)) = 0.11.4
Provides:       bundled(crate(tiny)) = 0.11.4
Provides:       bundled(crate(toml)) = 0.5.11
Provides:       bundled(crate(toml)) = 0.8.22
Provides:       bundled(crate(toml_datetime)) = 0.6.9
Provides:       bundled(crate(toml_edit)) = 0.22.26
Provides:       bundled(crate(toml_write)) = 0.1.1
Provides:       bundled(crate(tracing)) = 0.1.41
Provides:       bundled(crate(tracing)) = 0.1.33
Provides:       bundled(crate(triomphe)) = 0.1.14
Provides:       bundled(crate(ttf)) = 0.25.1
Provides:       bundled(crate(typenum)) = 1.18.0
Provides:       bundled(crate(ucd)) = 0.1.7
Provides:       bundled(crate(unicode)) = 1.0.18
Provides:       bundled(crate(unicode)) = 1.12.0
Provides:       bundled(crate(unicode)) = 0.2.0
Provides:       bundled(crate(unicode)) = 0.2.6
Provides:       bundled(crate(unsigned)) = 0.8.0
Provides:       bundled(crate(unty)) = 0.0.4
Provides:       bundled(crate(utf8parse)) = 0.2.2
Provides:       bundled(crate(vec_extract_if_polyfill)) = 0.1.0
Provides:       bundled(crate(version_check)) = 0.9.5
Provides:       bundled(crate(virtue)) = 0.0.18
Provides:       bundled(crate(walkdir)) = 2.5.0
Provides:       bundled(crate(wasi)) = preview1
Provides:       bundled(crate(wasi)) = 0.2.4
Provides:       bundled(crate(wasm)) = 0.2.100
Provides:       bundled(crate(wasm)) = 0.2.100
Provides:       bundled(crate(wasm)) = 0.4.50
Provides:       bundled(crate(wasm)) = 0.2.100
Provides:       bundled(crate(wasm)) = 0.2.100
Provides:       bundled(crate(wasm)) = 0.2.100
Provides:       bundled(crate(wayland)) = 0.3.10
Provides:       bundled(crate(wayland)) = 0.31.10
Provides:       bundled(crate(wayland)) = 0.3.0
Provides:       bundled(crate(wayland)) = 0.31.10
Provides:       bundled(crate(wayland)) = 0.31.2
Provides:       bundled(crate(wayland)) = 0.2.0
Provides:       bundled(crate(wayland)) = 0.2.0
Provides:       bundled(crate(wayland)) = 0.31.6
Provides:       bundled(crate(wayland)) = 0.31.6
Provides:       bundled(crate(web)) = 0.3.77
Provides:       bundled(crate(web)) = 0.2.4
Provides:       bundled(crate(wgpu)) = 25.0.0
Provides:       bundled(crate(wgpu)) = 25.0.1
Provides:       bundled(crate(wgpu)) = 25.0.0
Provides:       bundled(crate(wgpu)) = 25.0.0
Provides:       bundled(crate(wgpu)) = 25.0.1
Provides:       bundled(crate(wgpu)) = 25.0.0
Provides:       bundled(crate(widestring)) = 1.2.0
Provides:       bundled(crate(winapi)) = 0.3.9
Provides:       bundled(crate(winapi)) = 0.4.0
Provides:       bundled(crate(winapi)) = 0.1.9
Provides:       bundled(crate(winapi)) = 0.4.0
Provides:       bundled(crate(windows)) = 0.58.0
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_gnullvm)) = 0.53.0
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_aarch64_msvc)) = 0.53.0
Provides:       bundled(crate(windows)) = 0.58.0
Provides:       bundled(crate(windows_i686_gnu)) = 0.42.2
Provides:       bundled(crate(windows_i686_gnu)) = 0.48.5
Provides:       bundled(crate(windows_i686_gnu)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnu)) = 0.53.0
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_i686_gnullvm)) = 0.53.0
Provides:       bundled(crate(windows_i686_msvc)) = 0.42.2
Provides:       bundled(crate(windows_i686_msvc)) = 0.48.5
Provides:       bundled(crate(windows_i686_msvc)) = 0.52.6
Provides:       bundled(crate(windows_i686_msvc)) = 0.53.0
Provides:       bundled(crate(windows)) = 0.58.0
Provides:       bundled(crate(windows)) = 0.58.0
Provides:       bundled(crate(windows)) = 0.2.0
Provides:       bundled(crate(windows)) = 0.1.0
Provides:       bundled(crate(windows)) = 0.45.0
Provides:       bundled(crate(windows)) = 0.48.0
Provides:       bundled(crate(windows)) = 0.59.0
Provides:       bundled(crate(windows)) = 0.42.2
Provides:       bundled(crate(windows)) = 0.48.5
Provides:       bundled(crate(windows)) = 0.52.6
Provides:       bundled(crate(windows)) = 0.53.0
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnu)) = 0.53.0
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_gnullvm)) = 0.53.0
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.42.2
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.48.5
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides:       bundled(crate(windows_x86_64_msvc)) = 0.53.0
Provides:       bundled(crate(winit)) = 0.29.15
Provides:       bundled(crate(winnow)) = 0.7.10
Provides:       bundled(crate(wit)) = 0.39.0
Provides:       bundled(crate(wyz)) = 0.5.1
Provides:       bundled(crate(x11)) = 2.21.0
Provides:       bundled(crate(x11rb)) = 0.13.1
Provides:       bundled(crate(x11rb)) = 0.13.1
Provides:       bundled(crate(xcursor)) = 0.3.8
Provides:       bundled(crate(xkbcommon)) = 0.4.2
Provides:       bundled(crate(xkeysym)) = 0.2.1
Provides:       bundled(crate(yaml)) = 0.4.5
Provides:       bundled(crate(zerocopy)) = 0.8.25
Provides:       bundled(crate(zerocopy)) = 0.8.25
Provides:       bundled(crate(zigzag)) = 0.1.0
Provides:       bundled(crate(zune)) = 0.4.12
Provides:       bundled(crate(zune)) = 0.4.14
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

sed -e 's|_RPM_SO_VER_|%{soname_ver}|' -i include/%{name}_ld.h

sed \
  -e '/^\[lib\]/aname = "rashader"' \
  -e 's|, "staticlib"||' \
  -i %{name}-capi/Cargo.toml
sed \
  -e '/main()/a\     println!("cargo:rustc-cdylib-link-arg=-Wl,-soname,%{name}.so.%{soname_ver}");' \
  -i %{name}-capi/build.rs

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
%else
%generate_buildrequires
%cargo_generate_buildrequires
%endif


%build
%cargo_build -- --package %{name}-capi
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%if %{with vendor}
%{cargo_vendor_manifest}
%endif


%install
mkdir -p %{buildroot}/%{_libdir}/pkgconfig
install -m 0755 target/release/%{name}.so \
  %{buildroot}%{_libdir}/%{name}.so.%{soname_ver}.%{api_ver}
ln -s %{name}.so.%{soname_ver}.%{api_ver} %{buildroot}%{_libdir}/%{name}.so.%{soname_ver}
ln -s %{name}.so.%{soname_ver} %{buildroot}%{_libdir}/%{name}.so

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
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sun Jun 15 2025 Phantom X <megaphantomx at hotmail dot com> - 0.8.1-2
- Build a proper versioned library

* Wed Jun 04 2025 Phantom X <megaphantomx at hotmail dot com> - 0.8.1-1
- 0.8.1

* Tue Apr 29 2025 Phantom X <megaphantomx at hotmail dot com> - 0.8.0-1
- 0.8.0

* Wed Feb 05 2025 Phantom X <megaphantomx at hotmail dot com> - 0.6.2-1
- 0.6.2

* Fri Nov 15 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-1
- 0.5.1

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.4.3-1
- 0.4.3

* Tue Apr 02 2024 Phantom X <megaphantomx at bol dot com dot br> - 0.2.7-1
- Initial spec
