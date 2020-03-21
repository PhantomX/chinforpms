#!/usr/bin/bash
#  Name:  snxvpnrun
#  Purpose:  Perform appropriate startup/stop of snxconnect executable.
#
# Copyright (C) 2020 Phantom X
#
#  This file is part of snxconnect rpm package.
#
#  snxrun is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  snxrun is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this script.  If not, see <http://www.gnu.org/licenses/>.
#

exec="/usr/sbin/snx"
prog="$(basename ${exec})"
vpnexec="/usr/bin/snxconnect"
vpnprog="$(basename ${vpnexec})"
config="${HOME}/.config/snxrc"

urgency=normal
timeout=5000
notify_title=SNX
conf_msg="No ${config} file!"
display_msg='This needs to run in a graphical environment!'
stop_msg="The process ${prog} was stopped!"
stopfail_msg="The process ${prog} was not stopped!"
run_msg="The process ${prog} is running, VPN is working!"
runfail_msg="The process ${prog} is not running!"

notifycom="notify-send -u ${urgency} -t ${timeout} -i applications-internet --hint=int:transient:1 ${notify_title}"

pid="$(/usr/sbin/pidof -o %PPID ${exec})"

retval=0

start(){
  if ! [ -r "${config}" ] ;then
    if [[ -n "${DISPLAY}" ]] ; then
      ${notifycom} "${conf_msg}"
    else
      echo "${conf_msg}"
    fi
    retval=5
    return
  fi
  if [[ -z "${DISPLAY}" ]] ; then
    echo "${display_msg}"
    retval=6
    return
  fi
  if [[ -z "${pid}" ]] ;then
    "${vpnexec}" &
    sleep 5
  fi
  if /usr/sbin/pidof -o %PPID "${exec}" 2>/dev/null 1>&2; then
    ${notifycom} "${run_msg}"
    retval=0
  else
    ${notifycom} "${runfail_msg}"
    retval=1
  fi
}

stop(){
  if [[ -n "${pid}" ]] ;then
    "${exec}" -d 2>/dev/null 1>&2
    sleep 2
    if /usr/sbin/pidof -o %PPID "${exec}" 2>/dev/null 1>&2; then
      if [[ -n "${DISPLAY}" ]] ; then
        ${notifycom} "${stopfail_msg}"
      else
        echo "${stopfail_msg}"
      fi
      retval=1
    else
      if [[ -n "${DISPLAY}" ]] ; then
        ${notifycom} "${stop_msg}"
      else
        echo "${stop_msg}"
      fi
      retval=0
    fi
  fi
}


restart() {
  stop
  unset PID
  start
}

toggle(){
  if [[ -n "${pid}" ]] ;then
    stop
  else
    start
  fi
}

case "$1" in
  start|stop|toggle)
    $1
    ;;
  force-reload|restart|reload)
    restart
    ;;
  status)
    if [[ -n "${pid}" ]] ;then
      echo "${prog} is running in pid ${pid}."
    else
      echo "${prog} is not running."
    fi
    ;;
  help)
    echo "Usage: $0 {start|stop|toggle|status|restart|condrestart|reload|force-reload}"
    exit 2
    ;;
  *)
    toggle
    ;;
esac

exit ${retval}
