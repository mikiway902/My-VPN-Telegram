#!/bin/bash

# Ждём, пока 3x-ui полностью запустится
sleep 10

# Меняем логин и пароль через встроенную CLI 3x-ui
/usr/local/x-ui/x-ui setting -username "${XUI_ADMIN_USER}" -password "${XUI_ADMIN_PASS}"

# Перезапускаем панель, чтобы применить изменения
/usr/local/x-ui/x-ui restart
