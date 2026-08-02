# WA->CRM BRIDGE - SETUP (20 minutes, one time)

## 1. Get a VPS (~£4/mo)
Hetzner (hetzner.com/cloud) or DigitalOcean. Smallest Ubuntu 24 droplet/server. Note its IP + root password.

## 2. On the VPS (paste line by line into the console/SSH)
```
apt update && apt install -y nodejs npm chromium-browser
mkdir bridge && cd bridge
npm init -y && npm install whatsapp-web.js qrcode-terminal
# upload wa-bridge.js into this folder (or nano wa-bridge.js and paste it)
export GH_TOKEN="<the same GitHub token Max uses>"
node wa-bridge.js
```

## 3. Link it
A QR code appears in the terminal. Phone: WhatsApp > Settings > Linked devices > Link a device > scan. "Connected, listening" = live.

## 4. Keep it alive forever
```
npm install -g pm2
GH_TOKEN="<token>" pm2 start wa-bridge.js --name wa-bridge
pm2 save && pm2 startup
```

## Rules baked in
- READ-ONLY: the script has no send capability at all.
- Personal chats are filtered OUT before anything leaves the machine (known-CRM numbers + property-keyword gate). Groups skipped.
- Messages batch to data/wa-inbox.json every 15 min; CRM intake rules do the rest.
- If WhatsApp ever emails a device/security warning: `pm2 stop wa-bridge` immediately and tell Max.
