# Docusaurus Deployment Guide

## Asset Path 404 Fix Summary

Your site was experiencing 404 errors for JS/CSS assets because you have **dual deployments** configured with different path requirements.

---

## Platform 1: GitHub Pages ✅ ACTIVE & WORKING

**URL:** `https://Nabeerak.github.io/hackathon/`
**Status:** Deployed and configured correctly

### Configuration (Current `docusaurus.config.ts`)

```typescript
url: 'https://Nabeerak.github.io',
baseUrl: '/hackathon/',              // Subpath deployment
trailingSlash: false,
organizationName: 'Nabeerak',
projectName: 'hackathon',
```

### Asset Paths
✅ `/hackathon/assets/js/runtime~main.*.js`
✅ `/hackathon/assets/js/main.*.js`
✅ `/hackathon/assets/css/styles.*.css`
✅ `/hackathon/img/favicon.ico`

### Deployment Commands

```bash
cd docusaurus-book
npm run build                        # Test build locally
npm run serve                        # Preview at localhost:3000
GIT_USER=Nabeerak npm run deploy    # Deploy to GitHub Pages
```

### Verify Deployment

1. **Clear browser cache** (Ctrl+Shift+Delete or use Incognito)
2. **Visit:** https://Nabeerak.github.io/hackathon/
3. **Open DevTools** (F12) → Network tab
4. **Check all assets return HTTP 200:**
   - JS files: `application/javascript`
   - CSS files: `text/css`
   - Images: `image/svg+xml`, `image/x-icon`

---

## Platform 2: Render Static Site ⚠️ REQUIRES CONFIG CHANGE

**Current Status:** Configured in `render.yaml` but needs ROOT deployment config

### To Deploy on Render:

**Step 1: Switch to Render config**

```bash
# Temporarily rename configs
mv docusaurus-book/docusaurus.config.ts docusaurus-book/docusaurus.config.github.ts
mv docusaurus-book/docusaurus.config.render.ts docusaurus-book/docusaurus.config.ts
```

**Step 2: Update URL in config**

Edit `docusaurus.config.ts` line 17:
```typescript
url: 'https://your-site.onrender.com',  // Replace with your Render URL
baseUrl: '/',                            // Root deployment
```

**Step 3: Build and commit**

```bash
cd docusaurus-book
npm run build
git add -A
git commit -m "chore: Switch to Render deployment config"
git push origin 001-docusaurus-website
```

**Step 4: Deploy via Render Dashboard**

1. Go to https://dashboard.render.com
2. Connect your GitHub repo: `Nabeerak/hackathon`
3. Select branch: `001-docusaurus-website`
4. Render will auto-detect `render.yaml` settings:
   - **Root Directory:** `docusaurus-book`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `build`
5. Click "Create Static Site"

**Asset paths on Render:**
✅ `/assets/js/runtime~main.*.js` (no `/hackathon/` prefix)
✅ `/assets/js/main.*.js`
✅ `/assets/css/styles.*.css`

---

## Why Different Configs?

| Platform | Deployment Type | baseUrl | Asset Path Example |
|----------|----------------|---------|-------------------|
| **GitHub Pages** | Subpath (`/hackathon/`) | `/hackathon/` | `/hackathon/assets/js/main.js` |
| **Render Static** | Root (`/`) | `/` | `/assets/js/main.js` |
| **Vercel** | Root (`/`) | `/` | `/assets/js/main.js` |
| **Netlify** | Root (`/`) | `/` | `/assets/js/main.js` |

---

## Recommended: Stick with GitHub Pages

✅ **Already configured and deployed**
✅ **Free and reliable**
✅ **Auto-deploys via `npm run deploy`**
✅ **Integrated with GitHub workflow**

Your current setup is **optimal for GitHub Pages**. Only switch to Render if you need:
- Custom domain without CNAME setup
- Server-side features (though Docusaurus is static)
- Different hosting provider preference

---

## Troubleshooting

### Assets still 404 after deployment?

1. **Wait 2-3 minutes** for GitHub Pages CDN to update
2. **Hard refresh:** Ctrl+Shift+R (Chrome/Edge) or Cmd+Shift+R (Mac)
3. **Clear browser cache** completely
4. **Try incognito/private browsing**
5. **Check GitHub Pages settings:**
   - Go to: https://github.com/Nabeerak/hackathon/settings/pages
   - Source: `gh-pages` branch
   - Custom domain: (none)

### Build fails?

```bash
cd docusaurus-book
npm run clear            # Clear Docusaurus cache
rm -rf node_modules      # Remove node_modules
npm install              # Reinstall dependencies
npm run build            # Test build
```

### Wrong base URL?

Check which URL you're viewing:
- GitHub Pages: needs `baseUrl: '/hackathon/'`
- Render/Vercel/Netlify: needs `baseUrl: '/'`

---

## Current Branch Structure

- **`001-docusaurus-website`** - Main frontend branch (GitHub Pages config)
- **`backend-deploy`** - Backend deployment (separate Render service)
- **`gh-pages`** - Auto-generated GitHub Pages deployment branch

---

## Summary

✅ **GitHub Pages is LIVE and working:** https://Nabeerak.github.io/hackathon/

**Configuration files:**
- `docusaurus.config.ts` - Current (GitHub Pages config)
- `docusaurus.config.render.ts` - Render config (if needed)
- `render.yaml` - Render deployment config

**Deployment status:**
- GitHub Pages: ✅ Deployed (commit: `a83e1812`)
- Render Static: ⚠️ Not deployed (config ready)
