# Site maintenance scripts

| Script | Purpose |
|--------|---------|
| `fetch_wiki_textures.py` | Download Minecraft Wiki textures to `static/img/wiki/` |
| `audit_content.py` | Read-only audit of xlsx, Wiki, Blog images and boilerplate |
| `clean_wiki_sources.py` | Batch-remove Wiki auto-gen `<details>` blocks and duplicate headings |
| `export_books_games_txt.py` | Export/import 书籍、游戏 sheets as `data/export/*.txt` (TSV) |

Run from repository root:

```powershell
python scripts/site/fetch_wiki_textures.py
python scripts/site/audit_content.py
python scripts/site/audit_content.py --out reports/content-audit.md
python scripts/site/audit_content.py --suggest
python scripts/site/clean_wiki_sources.py
python scripts/site/clean_wiki_sources.py --write
python scripts/site/export_books_games_txt.py
python scripts/site/export_books_games_txt.py --import-books
python scripts/site/export_books_games_txt.py --import-games
```
