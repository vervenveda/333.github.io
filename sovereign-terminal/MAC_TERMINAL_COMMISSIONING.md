# 333 Network Sovereign Mac Terminal · Commissioning

Repository root: 333.github.io

## 1. Bootstrap the Keychain key

```zsh
cd "$HOME/333.github.io"
chmod 700 sovereign-terminal/bootstrap-keychain.command sovereign-terminal/Start-333-Network.command
./sovereign-terminal/bootstrap-keychain.command
```

Expected:
```
333 Network master key: CREATED in macOS Keychain
```
or
```
333 Network master key: PRESENT
```

## 2. Start the terminal

```zsh
./sovereign-terminal/Start-333-Network.command
```

Expected:
- bind 127.0.0.1:18733
- owner pairing code printed only in Terminal
- namespaces listed
- Network authority: NONE
- Public publishing: NONE
- STOS authority: NONE

## 3. Health check

In a second Terminal:
```zsh
curl -s http://127.0.0.1:18733/health | python3 -m json.tool
```

## 4. Pair manually

```zsh
curl -s -X POST http://127.0.0.1:18733/pair \
  -H 'content-type: application/json' \
  --data '{"code":"PASTE_THE_TERMINAL_CODE"}'
```

Do not paste the returned session token into chat, files, repositories or screenshots.

## 5. HOLD conditions

WITHHOLD and stop if:
- source integrity mismatch
- Keychain key is missing or not exactly 32 bytes after base64 decoding
- port 18733 binds to anything other than loopback
- pairing succeeds with a wrong code
- snapshot revision conflicts are silently overwritten
- any route exposes shell/file/repository/network authority not listed in the architecture document
