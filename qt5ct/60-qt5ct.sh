#!/usr/bin/sh

if [ -z "$QT_QPA_PLATFORMTHEME" ]; then
  case "${@}" in
    *kde|*kde1|*kde2|*plasma*|*lxqt|*startkde)
      # Ignore
      ;;
    *)
      QT_QPA_PLATFORMTHEME='qt5ct'
      export QT_QPA_PLATFORMTHEME
      ;;
  esac
fi
