# Site maintenance scripts

| Script | Purpose |
|--------|---------|
| `fetch_cert_images.py` | Sync certificate images from xlsx to `static/uploads/events/` |
| `fetch_wiki_textures.py` | Download Minecraft Wiki textures to `static/img/wiki/` |

Run from repository root:

```powershell
python scripts/site/fetch_cert_images.py
python scripts/site/fetch_wiki_textures.py
```
