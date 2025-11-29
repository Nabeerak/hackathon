# Physical AI & Humanoid Robotics Textbook Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator. It hosts the Physical AI & Humanoid Robotics textbook content with built-in search functionality.

## Prerequisites

- Node.js >= 20.0
- npm (comes with Node.js)

## Installation

```bash
npm install
```

This will install all required dependencies including Docusaurus core and the local search plugin.

## Local Development

```bash
npm start
```

This command starts a local development server and opens up a browser window at `http://localhost:3000`. Most changes are reflected live without having to restart the server.

## Build

```bash
npm run build
```

This command generates static content into the `build` directory. The build process includes:
- Compiling all markdown documentation
- Building the search index for local search functionality
- Optimizing assets for production

## Test Build Locally

```bash
npm run serve
```

This command serves the built website locally to test the production build before deployment.

## Deployment to GitHub Pages

This project is configured to deploy to GitHub Pages at: `https://Nabeerak.github.io/hackathon/`

### Prerequisites for Deployment
- Git repository must have a `gh-pages` branch enabled in GitHub Pages settings
- You need write access to the repository

### Deploy Command

```bash
npm run deploy
```

This command:
1. Builds the production-ready site
2. Pushes the build output to the `gh-pages` branch
3. GitHub Pages will automatically serve the updated site

### Manual Deployment (Alternative)

If the deploy script doesn't work, you can manually deploy:

```bash
npm run build
cd build
git init
git add -A
git commit -m "Deploy to GitHub Pages"
git push -f git@github.com:Nabeerak/hackathon.git main:gh-pages
```

## Project Structure

```
docusaurus-book/
├── docs/               # Documentation markdown files
│   ├── constitution.md # Project constitution
│   ├── module1.md      # Sample module 1
│   └── module2.md      # Sample module 2
├── blog/               # Blog posts (optional)
├── src/                # Custom React components and pages
│   ├── components/     # Reusable components
│   ├── css/           # Custom CSS
│   └── pages/         # Custom pages
├── static/            # Static assets (images, etc.)
├── docusaurus.config.ts  # Docusaurus configuration
├── sidebars.ts        # Sidebar configuration
└── package.json       # Dependencies and scripts
```

## Features

- **Documentation**: Organized textbook content with sidebar navigation
- **Search**: Local search functionality that indexes all documentation and blog content
- **Dark Mode**: Automatic dark mode support based on system preferences
- **Mobile Responsive**: Optimized for all device sizes
- **Edit on GitHub**: Links to edit pages directly on GitHub

## Configuration

The site configuration is in `docusaurus.config.ts`. Key settings:

- **URL**: `https://Nabeerak.github.io`
- **Base URL**: `/hackathon/`
- **Organization**: `Nabeerak`
- **Repository**: `hackathon`

## Search Configuration

The site uses `@easyops-cn/docusaurus-search-local` for local search functionality. The search indexes:
- All documentation pages
- Blog posts
- Custom pages

Search is configured in the `themes` section of `docusaurus.config.ts`.

## Troubleshooting

### Build Fails
```bash
npm run clear
npm run build
```

### Search Not Working
- Ensure you've run `npm run build` to generate the search index
- The search index is only generated during the build process, not in development mode

### Deployment Issues
- Verify GitHub Pages is enabled in repository settings
- Check that the `gh-pages` branch exists
- Ensure you have push permissions to the repository

## Contributing

1. Make changes to documentation in the `docs/` directory
2. Test locally with `npm start`
3. Build and verify with `npm run build && npm run serve`
4. Commit and push changes
5. Deploy with `npm run deploy`

## Resources

- [Docusaurus Documentation](https://docusaurus.io/)
- [Markdown Features](https://docusaurus.io/docs/markdown-features)
- [Deployment Guide](https://docusaurus.io/docs/deployment)
