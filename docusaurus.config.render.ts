import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// RENDER STATIC SITE CONFIGURATION (ROOT DEPLOYMENT)
// For Render: https://your-site.onrender.com/

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Bridging the gap between the digital brain and the physical body.',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // FOR RENDER: Deploy at root (no subpath)
  url: 'https://your-site.onrender.com',  // ⚠️ UPDATE with your Render URL
  baseUrl: '/',                             // ✅ Root deployment

  onBrokenLinks: 'throw',
  trailingSlash: false,

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/physical-ai-textbook',
          sidebarPath: './sidebars.ts',
          showLastUpdateTime: true,
          showLastUpdateAuthor: false,
          breadcrumbs: true,
          sidebarCollapsible: true,
          sidebarCollapsed: false,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics Textbook',
      hideOnScroll: false,
      logo: {
        alt: 'Physical AI Textbook',
        src: 'img/logo.svg',
        width: 32,
        height: 32,
      },
      items: [
        {
          href: 'https://github.com/Nabeerak/hackathon',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Fundamentals',
          items: [
            {
              label: 'Introduction',
              to: '/physical-ai-textbook',
            },
            {
              label: 'Hardware & Infrastructure',
              to: '/physical-ai-textbook/hardware-infrastructure',
            },
            {
              label: 'ROS 2 Fundamentals',
              to: '/physical-ai-textbook/ros2-fundamentals',
            },
            {
              label: 'Digital Twin Simulation',
              to: '/physical-ai-textbook/digital-twin-simulation',
            },
          ],
        },
        {
          title: 'Advanced Topics',
          items: [
            {
              label: 'NVIDIA Isaac Platform',
              to: '/physical-ai-textbook/nvidia-isaac',
            },
            {
              label: 'Vision-Language-Action',
              to: '/physical-ai-textbook/vision-language-action',
            },
            {
              label: 'Humanoid Robotics',
              to: '/physical-ai-textbook/humanoid-robotics',
            },
            {
              label: 'Appendices',
              to: '/physical-ai-textbook/appendices/glossary',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Panaversity',
              href: 'https://panaversity.org',
            },
            {
              label: 'GitHub Repository',
              href: 'https://github.com/Nabeerak/hackathon',
            },
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/humble/',
            },
            {
              label: 'NVIDIA Isaac Sim',
              href: 'https://docs.omniverse.nvidia.com/isaacsim/',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Panaversity. All rights reserved.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
