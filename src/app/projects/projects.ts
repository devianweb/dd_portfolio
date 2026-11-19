export interface Project {
  name: string;
  url: string;
  description: string;
  /** Extra small-print shown under the description, e.g. a fan-project disclaimer. */
  note?: string;
  image: string;
  imageAlt: string;
  logo?: string;
  tags: string[];
}

/** Projects shown as cards, in display order. Add new ones here. */
export const PROJECTS: Project[] = [
  {
    name: 'SkirmishLab',
    url: 'https://skirmishlab.duskwood.design',
    description:
      "A browser-based 3D tabletop skirmish simulator for One Page Rules' Grimdark Future: Firefight. Two players share an invite code and play head-to-head, peer to peer, on low-poly battlefields.",
    note: 'An unofficial fan project, not affiliated with or endorsed by One Page Rules.',
    image: 'assets/projects/skirmishlab-hero.jpg',
    imageAlt:
      'Low-poly miniatures exchanging fire across a ruined battlefield in SkirmishLab',
    logo: 'assets/projects/skirmishlab-logo.svg',
    tags: [
      'TypeScript',
      'Three.js',
      'WebRTC',
      'Node.js',
      'WebSockets',
      'Vite',
      'Vitest',
      'Azure',
    ],
  },
];
