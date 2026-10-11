# analytitech.net: PerfectRep website

Static site. No framework, no dependencies beyond Python 3.

```
python3 build.py                      # writes dist/
cd dist && python3 -m http.server     # preview at http://localhost:8000
```

- `site.json`: app name, coach name, prices, emails, store links. Change here, rebuild.
- `templates/`: one file per page (home, partners, support, privacy, terms, 404).
- `partials/`: shared head, header, footer.
- `assets/`: CSS, logo, icons, app screenshots, `og.png` link preview.

When the app is in the stores, put the links in `appStoreUrl` and
`playStoreUrl` and swap the "coming soon" badges in `templates/index.html`.

## Going live (GitHub Pages, free)

1. Create a GitHub repo (e.g. `AnalytiTech/website`) and push this folder.
2. Repo → Settings → Pages → Source: **GitHub Actions**. The included
   workflow builds and deploys on every push to `main`.
3. Repo → Settings → Pages → Custom domain: `analytitech.net`, then tick
   Enforce HTTPS once the certificate is issued.
4. At GoDaddy → DNS for analytitech.net:
   - Replace the `@` A records with GitHub's: `185.199.108.153`,
     `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - `www` CNAME → `analytitech.github.io` (your GitHub org/user name).
   - **Leave the MX and other email records alone** (Google Workspace).
5. Turn off the GoDaddy Website Builder site once the new site loads.

The privacy, terms and support URLs used inside the app
(`analytitech.net/privacy`, `/terms`, `/support`) are built by this site.
