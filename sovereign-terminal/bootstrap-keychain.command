#!/bin/zsh
set -euo pipefail
umask 077
SERVICE="khaemenes-333-network-master-key"
ACCOUNT="333-network-terminal"
if /usr/bin/security find-generic-password -s "$SERVICE" -a "$ACCOUNT" >/dev/null 2>&1; then
  echo "333 Network master key: PRESENT"
  exit 0
fi
KEY="$(/usr/bin/openssl rand -base64 32 | tr -d '\n')"
/usr/bin/security add-generic-password -U -s "$SERVICE" -a "$ACCOUNT" -w "$KEY" >/dev/null
unset KEY
echo "333 Network master key: CREATED in macOS Keychain"
