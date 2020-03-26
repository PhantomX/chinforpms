#!/usr/bin/bash
#  Name:  snxrun
#  Purpose:  Perform appropriate startup/stop of snx executable.
#
# Copyright (C) 2020 Phantom X
#
#  This file is part of snx rpm package.
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

# 20200323

exec="/usr/sbin/snx"
prog="$(basename ${exec})"
config="${HOME}/.config/${prog}rc"

timeout=5000
notify_title=SNX
conf_msg="No ${config} file!"
stop_msg="The process ${prog} was stopped!"
stopfail_msg="The process ${prog} was not stopped!"
run_msg="The process ${prog} is running, VPN is working!"
runfail_msg="The process ${prog} is not running!"

notifycom="notify-send -t ${timeout} -i applications-internet --hint=int:transient:1 ${notify_title}"

pid="$(/usr/sbin/pidof -o %PPID ${exec})"

retval=0

start(){
  if ! [[ -r "${config}" ]] ;then
    echo "${conf_msg}"
    if [[ -n "${DISPLAY}" ]] ; then
      ${notifycom} -u critical "${conf_msg}"
    fi
    retval=5
    return
  fi
  if [[ -w "${config}" ]] ;then
    chmod 0600 "${config}" 2>/dev/null 1>&2
  fi
  if [[ -z "${pid}" ]] ;then
    if [[ -n "${DISPLAY}" ]] ; then
      /usr/bin/xterm -e "\"${exec}\" -f \"${config}\" ; sleep 5"
    else
      "${exec}" -f "${config}"
    fi
    sleep 2
  fi
  if /usr/sbin/pidof -o %PPID "${exec}" 2>/dev/null 1>&2; then
    echo "${run_msg}"
    if [[ -n "${DISPLAY}" ]] ; then
      ${notifycom} -u normal "${run_msg}"
    fi
    retval=0
  else
    echo "${runfail_msg}"
    if [[ -n "${DISPLAY}" ]] ; then
      ${notifycom} -u critical "${runfail_msg}"
    fi
    retval=1
  fi
}

stop(){
  if [[ -n "${pid}" ]] ;then
    "${exec}" -d 2>/dev/null 1>&2
    sleep 2
    if /usr/sbin/pidof -o %PPID "${exec}" 2>/dev/null 1>&2; then
      echo "${stopfail_msg}"
      if [[ -n "${DISPLAY}" ]] ; then
        ${notifycom} -u critical "${stopfail_msg}"
      fi
      retval=1
    else
      echo "${stop_msg}"
      if [[ -n "${DISPLAY}" ]] ; then
        ${notifycom} -u normal "${stop_msg}"
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
