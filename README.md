# How to Rock Climb! — wiki site

Quartz v4 site for the LLM wiki built from John Long's *How to Rock Climb!*
(source wiki: `~/Documents/org-notes/llm-wiki/other/how-to-rock-climb/wiki`).

## Update content

```sh
python3 sync-wiki.py   # regenerates content/ from the wiki
npx quartz build --serve   # preview at http://localhost:8080
git add -A && git commit -m "Sync wiki" && git push
```

Pushing to `v4` deploys to GitHub Pages via `.github/workflows/deploy.yml`.

Built with [Quartz](https://quartz.jzhao.xyz/).
