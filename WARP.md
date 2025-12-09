# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a personal GitHub Pages blog built using Jekyll Now, a simplified Jekyll setup that requires minimal configuration. The blog focuses on data analysis, computational molecular simulations, machine learning, and Python development topics.

**Repository URL**: christophergaughan.github.io (GitHub Pages hosted)

## Key Technologies

- **Jekyll**: Static site generator (v1.2.0 - Jekyll Now)
- **Kramdown**: Markdown processor with GitHub Flavored Markdown support
- **Rouge**: Syntax highlighter
- **MathJax**: Mathematical equation rendering (LaTeX support)
- **Plotly**: Interactive data visualizations
- **Sass/SCSS**: CSS preprocessing

## Development Commands

### Local Development

```bash
# Install Jekyll and GitHub Pages dependencies (if not already installed)
gem install github-pages

# Serve site locally with live reload
jekyll serve

# View site at: http://127.0.0.1:4000/
```

**Note**: Jekyll is not currently installed on this system. Install via `gem install github-pages` before local development.

### Content Management

```bash
# Create new blog post (filename format is critical)
# Format: YYYY-MM-DD-title-with-hyphens.md
touch _posts/$(date +%Y-%m-%d)-your-post-title.md

# View all posts
ls _posts/
```

## Repository Structure

### Core Directories

- **`_posts/`**: Blog post content in Markdown format
  - Must follow naming convention: `YYYY-MM-DD-title.md`
  - Front matter required: `layout`, `title`, optional `author`, `date`
  - Support for LaTeX equations using MathJax (inline: `$$equation$$`)
  - Can include Jupyter notebooks (converted to markdown/HTML)

- **`_layouts/`**: Page templates
  - `default.html`: Base template with header, footer, navigation
  - `post.html`: Blog post template (extends default.html)
  
- **`_includes/`**: Reusable HTML components
  - `analytics.html`: Google Analytics integration
  - `disqus.html`: Comment system
  - `meta.html`: SEO meta tags
  - `svg-icons.html`: Social media icons
  
- **`_sass/`**: SCSS stylesheets (compiled by Jekyll)
  - `_reset.scss`: CSS reset
  - `_variables.scss`: Design system variables
  - `_highlights.scss`: Syntax highlighting styles
  - `_svg-icons.scss`: SVG icon styles
  
- **`images/`**: Static image assets

### Key Files

- **`_config.yml`**: Jekyll configuration
  - Site metadata (name, description, avatar)
  - Social media links
  - Plugin configuration
  - Permalink structure
  
- **`style.scss`**: Main stylesheet (imports all Sass partials)
- **`index.html`**: Homepage listing all blog posts
- **`about.md`**: About page content
- **`404.md`**: Custom 404 error page

## Architecture Patterns

### Jekyll Liquid Templating

This site uses Jekyll's Liquid templating engine:

- **Variables**: `{{ site.name }}`, `{{ page.title }}`, `{{ content }}`
- **Loops**: `{% for post in site.posts %}...{% endfor %}`
- **Includes**: `{% include meta.html %}`
- **Conditionals**: `{% if page.title %}...{% endif %}`

### Front Matter Structure

All posts and pages require YAML front matter:

```yaml
---
layout: post
title: "Your Post Title"
author: "Christopher L. Gaughan, Ph.D."
date: YYYY-MM-DD
---
```

### Math Equation Support

LaTeX equations are rendered via MathJax (included in `default.html`):

- Inline math: `$$E = mc^2$$`
- Display math: Use double `$$` on separate lines
- MathJax CDN: `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js`

### Styling System

The site uses Sass with a modular structure:

- Variables defined in `_sass/_variables.scss` (colors, fonts, breakpoints)
- Mobile-first responsive design with `@include mobile` mixins
- Base font size: 18px, Helvetica/Helvetica Neue font stack
- Container max-width: 740px

### Third-Party Integrations

- **Plotly.js**: Loaded via CDN in default layout for interactive visualizations
- **Bootstrap CSS**: Version 3.3.7 (loaded for specific components)
- **JiffyReader**: Speed reading enhancement bookmarklet embedded in navigation

## Development Guidelines

### Creating Blog Posts

1. **File naming**: Use `YYYY-MM-DD-descriptive-title.md` format
2. **Front matter**: Always include `layout: post` and `title`
3. **LaTeX**: Use MathJax syntax for mathematical content
4. **Code blocks**: Use triple backticks with language specifier for syntax highlighting
5. **Images**: Store in `/images/` directory, reference with `/images/filename.png`

### Style Modifications

- Edit `style.scss` for global styles
- Edit individual Sass partials in `_sass/` for specific components
- Jekyll automatically compiles SCSS to CSS on build
- Changes require Jekyll restart in local development

### GitHub Pages Deployment

This site uses GitHub Pages' automatic deployment:

- Push to `master` branch triggers automatic rebuild
- Changes typically appear within seconds to minutes
- No manual build/deploy commands needed
- Site available at: https://christophergaughan.github.io

### Excluded Files

The following are excluded from the built site (see `_config.yml`):

- `Gemfile`, `Gemfile.lock`
- `LICENSE`, `README.md`, `CNAME`
- `_site/` (build output)
- `.jekyll-*` (cache files)
- `node_modules/`, `vendor/`

## Important Notes

### Blog Post Content

- This blog features technical content including physics (Einstein field equations, general relativity), data science, and machine learning
- Posts may include complex mathematical notation requiring proper LaTeX rendering
- Some posts include embedded Jupyter notebooks or converted notebook content

### No Automated Testing

There are no test scripts or CI/CD pipelines in this repository. Content validation is manual.

### GitHub Pages Limitations

- Only specific Jekyll plugins are supported (listed in `_config.yml`)
- Custom plugins require pre-building site locally and pushing to `gh-pages` branch
- Ruby dependencies managed via `github-pages` gem

## Common Tasks

### Add a new blog post

```bash
# Create post file with proper naming
touch _posts/$(date +%Y-%m-%d)-new-post-title.md

# Add front matter and content
# Edit in your preferred editor
# Commit and push to GitHub
git add _posts/$(date +%Y-%m-%d)-new-post-title.md
git commit -m "Add new blog post"
git push origin master
```

### Preview changes locally

```bash
# Serve site (auto-regenerates on file changes)
jekyll serve

# Or with drafts visible
jekyll serve --drafts

# With future-dated posts visible
jekyll serve --future
```

### Update site configuration

1. Edit `_config.yml`
2. Restart Jekyll server (config changes not auto-reloaded)
3. Commit and push changes

### Modify styles

1. Edit `style.scss` or files in `_sass/`
2. Changes auto-reload with Jekyll serve
3. Test thoroughly before pushing to production
