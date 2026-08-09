# Competitor feed - deploy (droplet)

1) TOKEN (one time, ~5 min): developers.facebook.com -> Graph API Explorer -> your lead-ads app
   - Permissions: instagram_basic, pages_show_list, business_management, instagram_manage_insights
   - Generate token -> GET /me/accounts -> note your Page id -> GET /{page-id}?fields=instagram_business_account -> that id = IG_BUSINESS_ID
   - Exchange for long-lived token (Access Token Debugger -> Extend). Lives ~60 days; renew task will remind.
2) On droplet:
   sudo mkdir -p /opt/competitor-feed && cd /opt/competitor-feed
   curl -sO https://raw.githubusercontent.com/calum7macleod/dashboards/main/tools/competitor-feed/fetch.py
   curl -sO https://raw.githubusercontent.com/calum7macleod/dashboards/main/tools/competitor-feed/config.json
   sudo nano /etc/competitor-feed.env   # IG_TOKEN=... IG_BUSINESS_ID=... GH_TOKEN=...  (chmod 600)
   (crontab -l; echo "0 5 * * 1 . /etc/competitor-feed.env && python3 /opt/competitor-feed/fetch.py >> /var/log/competitor-feed.log 2>&1") | crontab -
3) Test once: . /etc/competitor-feed.env && python3 fetch.py
Output lands at data/competitor-feed.json in dashboards repo. Max analyzes baselines/breakouts in Monday brief.
Tokens NEVER go in chat or repo.
