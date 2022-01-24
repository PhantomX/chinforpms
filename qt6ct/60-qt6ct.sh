#!/usr/bin/sh

case "${@}" in
  *kde|*kde1|*kde2|*plasma*|*lxqt)
    if [ "$QT_QPA_PLATFORMTHEME" = "qt5ct" ] || [ "$QT_QPA_PLATFORMTHEME" = "qt6ct" ] ;then
      unset QT_QPA_PLATFORMTHEME
      systemctl --user unset-environment QT_QPA_PLATFORMTHEME
    fi
    ;;
  *)
    if [ -z "$QT_QPA_PLATFORMTHEME" ]; then
      QT_QPA_PLATFORMTHEME='qt6ct'
      export QT_QPA_PLATFORMTHEME
      systemctl --user import-environment QT_QPA_PLATFORMTHEME
    fi
    ;;
esac
