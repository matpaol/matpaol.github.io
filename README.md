# Matteo Paolini — portfolio

Static HTML for GitHub Pages. The current implementation extends the approved Gemini design.

## Update a project

Edit `projects/<project-slug>/project.json`. Every project uses the same fields: overview, constraints, contribution, approach, results, limits, media and links. Set `featured` to select it for the home and `order` to choose its position. Then run:

```sh
python3 build.py
```

Open `index.html` or serve the folder with `python3 -m http.server 8000`.

## Add project material

Each project has its own `index.html` and `project.json`. Put original images in its `media/` folder and reports in `documents/`. Add reports, YouTube videos, notebooks and repositories to the project's `links` list. Relative resource links start from that project's folder. Optional `media` entries place illustrations in the appropriate narrative section:

```json
{"type":"image", "section":"approach", "src":"media/fem.png", "width":1600, "height":900, "alt":"Description of the FEM result", "caption":"Material, loading and measured quantity"}
```

For a YouTube demonstration use `type: "youtube"`, `id`, `title` and `section`. Run the builder after any change. Keep requirements separate from measured results, and describe your own work separately from the team's work.

To add a project, copy one project folder, change its `slug`, `order` and content, then run the builder. Its page and archive card are generated automatically. Generated `index.html` files should be edited through `project.json`, since the next build replaces them.

## Design reference

[Editable Figma desktop, mobile and project layouts](https://www.figma.com/design/JZyWqWKXTIS7Js0dQFFeLH)

The Figma layouts were visually reviewed. The HTML has passed local-reference and structural checks; a live Safari/Chrome responsive check is still required before deployment.

`verified-base.html` preserves the current public source used as the base. `additions.css` holds the design extension; `styles.css` and the HTML pages are generated. `seed_content.py` records the initial import and should not be run after manual content changes.

## Pending material

- Current CV PDF: the button opens a clear availability note instead of a broken download.
- Original project renders, FEM, diagrams and demonstrations from the next uploads.
- Individual contributions for group projects other than Tentacle and HR fairness.
- Final measurements and reports for quantitative claims.

The uploaded material is not automatically copied into this public site. Private repository code and raw respondent data are excluded.
