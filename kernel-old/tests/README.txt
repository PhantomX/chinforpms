Recommended Layout for Kernel Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add tests to enable Fedora CI [1] which are curated using the standard test interface [2]

[1] https://fedoraproject.org/wiki/CI
[2] https://fedoraproject.org/wiki/CI/Standard_Test_Interface

As new pull requests are filed, please link/add your tests in one of the following directories
to better organize the tests. If a new directory is required, which isn't included in the layout
below, please add justification in the pull request. The directories can be created as new tests
are added to dist-git.

acpi
cgroup
cpu
crc32c-self-check
criu
crypto
drivers
filesystem
firmware
ftrace
include
kabi
kmod
kpatch
ksc
kvm
mce
memory
modules
namespace
networking
performance
powermgmt
ptp
scheduler
security
storage
syscalls
time
update build
