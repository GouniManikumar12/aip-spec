# GitHub Pages Setup Guide

This guide explains how to configure GitHub Pages for the AIP Specification repository.

## Repository Information

- **Repository URL**: https://github.com/GouniManikumar12/aip-spec
- **GitHub Pages URL**: https://gounimanikumar12.github.io/aip-spec/

## Setup Steps

### 1. Enable GitHub Pages

1. Go to your repository: https://github.com/GouniManikumar12/aip-spec
2. Click on **Settings** (top navigation)
3. Scroll down to **Pages** in the left sidebar
4. Under **Build and deployment**:
   - **Source**: Select "GitHub Actions"
   - This will use the workflow file at `.github/workflows/pages.yml`

### 2. Configure Repository Permissions

1. In **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Check **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

### 3. Verify Deployment

1. Go to **Actions** tab in your repository
2. You should see the "Deploy GitHub Pages" workflow running
3. Wait for it to complete (green checkmark)
4. Visit https://gounimanikumar12.github.io/aip-spec/

## What's Deployed

The GitHub Pages site includes:

- **Main Documentation**: README.md as the homepage
- **Specification Docs**: All files in `/docs/` directory
  - Overview, Roles, Transport & Auth, Auction, Events, etc.
- **Schemas**: JSON schemas in `/schemas/` directory
- **Examples**: Example payloads in `/examples/` directory
- **Governance**: CONFORMANCE.md, GOVERNANCE.md, SECURITY.md, etc.

## Site Structure

```
https://gounimanikumar12.github.io/aip-spec/
├── README.md (homepage)
├── docs/
│   ├── index.md
│   ├── 01-overview.md
│   ├── 02-roles.md
│   ├── 03-transport-and-auth.md
│   ├── 04-auction.md
│   ├── 05-events-and-states.md
│   ├── 06-wallets-and-payouts.md
│   ├── 07-security-and-fraud.md
│   ├── 08-observability.md
│   ├── 09-compliance.md
│   └── 10-versioning-and-conformance.md
├── CONFORMANCE.md
├── GOVERNANCE.md
├── SECURITY.md
├── VERSIONING.md
└── PRD.md
```

## Theme Configuration

The site uses the **Cayman** theme configured in `_config.yml`:

```yaml
theme: jekyll-theme-cayman
title: AIP Specification
description: Agentic Intent Protocol - Open protocol for intent monetization in AI and agentic environments
```

## Automatic Deployment

Every push to the `main` branch automatically triggers a deployment:

1. GitHub Actions workflow runs (`.github/workflows/pages.yml`)
2. Site is built using Jekyll
3. Deployed to GitHub Pages
4. Available at https://gounimanikumar12.github.io/aip-spec/

## Custom Domain (Optional)

To use a custom domain like `specs.admesh.dev`:

1. Add a `CNAME` file to the repository root:
   ```
   specs.admesh.dev
   ```

2. Configure DNS records:
   - Add a CNAME record pointing to `gounimanikumar12.github.io`

3. In GitHub Settings → Pages:
   - Enter your custom domain
   - Enable "Enforce HTTPS"

## Troubleshooting

### Pages Not Showing Up

1. Check **Actions** tab for deployment errors
2. Verify **Settings** → **Pages** shows "Your site is live at..."
3. Clear browser cache and try again

### 404 Errors

- Ensure file paths are correct (case-sensitive)
- Check that files are committed and pushed to `main` branch
- Wait a few minutes for deployment to complete

### Workflow Failures

1. Check **Actions** tab for error details
2. Verify workflow permissions are set correctly
3. Ensure `_config.yml` is valid YAML

## Updating Content

To update the documentation:

1. Edit files locally in the `aip-spec` directory
2. Commit changes:
   ```bash
   git add .
   git commit -m "Update documentation"
   ```
3. Push to GitHub:
   ```bash
   git push origin main
   ```
4. GitHub Actions will automatically rebuild and deploy

## Links

- **Repository**: https://github.com/GouniManikumar12/aip-spec
- **GitHub Pages**: https://gounimanikumar12.github.io/aip-spec/
- **Actions**: https://github.com/GouniManikumar12/aip-spec/actions
- **Settings**: https://github.com/GouniManikumar12/aip-spec/settings/pages

## Next Steps

1. ✅ Repository created and code pushed
2. ⏳ Enable GitHub Pages in repository settings
3. ⏳ Wait for first deployment to complete
4. ⏳ Verify site is accessible
5. 🎯 (Optional) Configure custom domain

---

**Note**: The GitHub Pages workflow is already configured and will run automatically once you enable Pages in the repository settings.

