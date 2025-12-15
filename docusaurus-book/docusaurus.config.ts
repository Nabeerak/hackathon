import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Bridging the gap between the digital brain and the physical body.',
  favicon: 'img/logo.svg',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://Nabeerak.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/hackathon/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Nabeerak', // Usually your GitHub org/user name.
  projectName: 'hackathon', // Usually your repo name.

  onBrokenLinks: 'throw',
  trailingSlash: false,

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/physical-ai-textbook', // Serve docs at the site's root
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/Nabeerak/hackathon/tree/main/docusaurus-book/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: false,
          breadcrumbs: true,
          // Book-like features
          sidebarCollapsible: true,
          sidebarCollapsed: false,
        },
        blog: false, // Disable blog functionality
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
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
