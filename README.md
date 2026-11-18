# dd_portfolio

Personal portfolio for Ian Webster / Duskwood Design, served at [duskwood.design](https://duskwood.design) via GitHub Pages.

Built with Angular 14 as a single scrolling page: a home section and a grid of project cards.

## Adding a project

Add an entry to `PROJECTS` in [src/app/projects/projects.ts](src/app/projects/projects.ts) and drop its images in `src/assets/projects/`. Cards render in array order.

## Development

```sh
npm ci
npm start        # dev server at http://localhost:4200
npm test         # Karma unit tests (needs Chrome)
```

## Deploying

GitHub Pages serves the `docs/` folder on `main`.

```sh
npm run build    # production build into docs/, plus CNAME and 404.html
```

Then commit `docs/` and push.
