#!/bin/bash
#
# Copyright (c) 2018 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Boyang Xue <bxue@redhat.com>

PACKAGE=kernel

. /usr/share/beakerlib/beakerlib.sh

rlJournalStart

WDIR=/tmp/TC_freeze-protection-bypass.tmp.workdir
ODIR=/tmp/TC_freeze-protection-bypass.tmp.oldmnt
NDIR=/tmp/TC_freeze-protection-bypass.tmp.newmnt
mkdir $ODIR $NDIR $WDIR

cd $WDIR
fallocate -l 64M 64M.img
mkfs.ext4 -qF 64M.img
TDEV=$(losetup -f --show 64M.img)

TRID=$RANDOM

rlPhaseStartSetup

	# The following patch for this bug is integrated in kernel v4.18
	#
	# vfs: add the sb_start_intwrite_trylock() helper
	# ext4: factor out helper ext4_sample_last_mounted()
	# ext4: do not update s_last_mounted of a frozen fs
	KNVR=$(uname -r | cut -d '-' -f1)
	rlCmpVersion $KNVR 4.18.0 >/dev/null
	if [[ $? -eq 2 ]]; then
	        ISFIXED=0
		rlPass "Kernel version < 4.18, indicating it's vulnerable to this bug. Test skipped as pass."
		exit 0
	else
	        ISFIXED=1
	fi

	rlRun "mount $TDEV $ODIR"
	rlRun "echo TC_freeze-protection-bypass > $ODIR/TC_freeze-protection-bypass"
	rlRun "umount $ODIR"
rlPhaseEnd

rlPhaseStartTest
	rlRun "echo \"run TC_freeze-protection-bypass#${TRID}\" >/dev/kmsg"
	rlRun "mount $TDEV $NDIR"
	rlLog "Run 'fsfreeze -f $NDIR &'"
	fsfreeze -f $NDIR &
	wait $!
	rlRun "grep TC_freeze-protection-bypass $NDIR/TC_freeze-protection-bypass"
	rlRun "! dmesg | tac | sed -ne \"0,\#run TC_freeze-protection-bypass\#${TRID}#p\" | tac | grep -E \"ext4_journal_check_start|ext4_journal_start_sb\""
	if [[ $? -eq 0 ]]; then
		rlPass "The kernel warning isn't triggered. Test passes."
	else
		rlFail "The kernel warning is triggered. Test fails."
	fi
rlPhaseEnd

rlPhaseStartCleanup
	rlRun "fsfreeze -u $NDIR"
	rlRun "umount $TDEV"
	rlRun "losetup -d $TDEV"
	rlRun "rm -f 64M.img"
	rlRun "rm -rf $NDIR"
	rlRun "rm -rf $ODIR"
	rlRun "rm -rf $WDIR"
rlPhaseEnd

rlJournalPrintText
rlJournalEnd
