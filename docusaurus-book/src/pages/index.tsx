import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <Heading as="h1" className={styles.heroTitle}>
              {siteConfig.title}
            </Heading>
            <p className={styles.heroSubtitle}>
              {siteConfig.tagline}
            </p>
            <div className={styles.buttons}>
              <Link
                className={clsx('button button--secondary button--lg', styles.heroButton)}
                to="/physical-ai-textbook">
                Start Reading the Book
              </Link>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

const features = [
  {
    title: 'ROS 2 Mastery',
    icon: '🤖',
    description: 'Master Robot Operating System 2 from fundamentals to advanced topics with hands-on examples.',
  },
  {
    title: 'NVIDIA Isaac Platform',
    icon: '🎮',
    description: 'Explore digital twin simulation, Isaac Sim, and GPU-accelerated robotics development.',
  },
  {
    title: 'Vision-Language-Action',
    icon: '👁️',
    description: 'Learn cutting-edge VLA models that bridge perception, language, and robotic control.',
  },
  {
    title: 'Humanoid Robotics',
    icon: '🦾',
    description: 'Build and program humanoid robots with state-of-the-art AI and control systems.',
  },
];

function FeatureBox({title, icon, description, index}) {
  return (
    <div className={styles.featureBox}>
      <div className={styles.neonBorder}></div>
      <div className={styles.featureContent}>
        <div className={styles.featureIcon}>{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description="Comprehensive textbook on Physical AI & Humanoid Robotics covering ROS 2, NVIDIA Isaac, Vision-Language-Action models, and more">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <h2 className={styles.featuresTitle}>What You'll Learn</h2>
            <div className={styles.featureGrid}>
              {features.map((props, idx) => (
                <FeatureBox key={idx} {...props} index={idx} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
