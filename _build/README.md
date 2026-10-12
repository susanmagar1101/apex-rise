# Site generator for the Apex Rise website

The pages of this site (`index.html`, `services.html`, `work.html`, `about.html`, `contact.html`, `404.html` and every case study page in `work/`) are plain HTML files made by `build.py`. The script also writes `sitemap.xml` and `vercel.json`, so the project list, the sitemap and the Vercel address rules always match.

This folder is not published: `.vercelignore` in the site folder tells Vercel to skip `_build/`.

## What you need

Python 3. No extra packages are needed.

## Rebuild the site

From the site folder (or from anywhere, the script finds its own folder):

```
python _build/build.py
```

The script prints each file it writes. Check the changes with `git diff`, test the pages, then commit and push. Vercel publishes the new version after the push.

## Add a project to Our Work

1. Save the screenshots for the project in `assets/work/` as compressed `.jpg` files (about 1200 pixels wide). Note the width and height of each picture.
2. Open `_build/projects.json` and copy the existing project entry inside the `projects` list. Paste it after the last entry (add a comma between entries).
3. Change every value in the copy:
   * `slug`: the end of the page address, in lower case with hyphens, for example `online-booking-system`. The page will be at `/work/online-booking-system`.
   * `name`, `client`, `sector` and `summary`: what the project card shows. Keep the summary to one sentence.
   * `card_image` and `hero.image`: the picture file names, their width and height in pixels, and a short description for the `alt` text.
   * `page_title` and `page_description`: the browser tab title and the search engine description for the case study page.
   * `hero`: the heading (`title_html`), the one-line introduction and, if the client allows it, `live_url` (leave it out if there is no public link).
   * `facts`, `brief`, `delivered`, `how_we_worked` and `cta`: the case study content. `delivered.items` can hold as many parts as the project needs.
4. Run `python _build/build.py`. The new card appears on `/work`, the case study page is written to `work/<slug>.html`, and `sitemap.xml` and `vercel.json` are updated.
5. Test the new page on a laptop and a phone, then commit and push.

Projects appear on the Our Work page in the order they are listed in `projects.json`. Only add real, finished projects, and only include facts and results we can show. Text in `projects.json` is used as HTML, so write `&amp;` for an ampersand.

## Changing other content

Text for the other pages, the top bar and the footer is in `build.py`. Change it there and rebuild; editing the HTML files directly would be overwritten by the next build.
