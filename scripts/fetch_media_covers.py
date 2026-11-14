#!/usr/bin/env python3
"""Fetch cover art for browse hubs (anime / games / books / movies) into static/img/media.

Sources (verified reachable from this Windows host via curl.exe):
  - anime  → Anilist GraphQL (type ANIME); Bangumi skipped (timeouts)
  - games  → Steam Store search API (+ Steam CDN covers)
  - books  → Apple iTunes Search (ebook), Anilist MANGA fallback
              Open Library / Google Books kept as optional soft tries
  - movies → Douban subject_suggest (when not rate-limited), IMDb suggestion
              posters (+ CN→EN translate), Anilist fallback for anime films
              iTunes movie / Wikipedia skipped (empty or timeouts here)

HTTP transport prefers curl.exe (urllib SSL/timeouts are unreliable here).
Resume-safe: skips titles already present in data/media_meta/*.json with a local cover.
Run from repo root (Windows PowerShell)::

    Set-Location F:\\commercial\\atelier
    python scripts\\fetch_media_covers.py
    python scripts\\fetch_media_covers.py --only movies
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "zhita_settings.xlsx"
META_DIR = ROOT / "data" / "media_meta"
IMG_ROOT = ROOT / "static" / "img" / "media"
PLACEHOLDER = "/static/img/wiki/bookshelf.png"

UA = "zhk0567/atelier/1.0 (https://zhkun.xyz; personal media cover fetch)"
ANILIST_URL = "https://graphql.anilist.co"
BANGUMI_SEARCH = "https://api.bgm.tv/search/subject/"
STEAM_SEARCH = "https://store.steampowered.com/api/storesearch/"
OPENLIB_SEARCH = "https://openlibrary.org/search.json"
GOOGLE_BOOKS = "https://www.googleapis.com/books/v1/volumes"
ITUNES_SEARCH = "https://itunes.apple.com/search"
MYMEMORY_URL = "https://api.mymemory.translated.net/get"
KITSU_ANIME = "https://kitsu.io/api/edge/anime"
TRANSLATE_CACHE_PATH = META_DIR / "translate_cache.json"
# Manual CN→Steam store titles when free MT invents a wrong English name.
STEAM_TITLE_ALIASES: dict[str, str] = {
    "地狱边境": "LIMBO",
    "侠盗猎车手Ⅴ": "Grand Theft Auto V",
    "侠盗猎车手Ⅴ增强版": "Grand Theft Auto V",
    "100%鲜橙汁": "100% Orange Juice",
    "人类一败涂地": "Human Fall Flat",
    "内心的过去": "The Past Within",
    "双人成行": "It Takes Two",
    "去月球": "To the Moon",
    "原子之心": "Atomic Heart",
    "孤帆远航": "FAR: Lone Sails",
    "异星装置博物馆": "Machinika Museum",
    "我们也在这里": "We Were Here",
    "我们一起在这里": "We Were Here Together",
    "扣押：豪华版": "DISTRAINT Deluxe Edition",
    "泰坦陨落2": "Titanfall 2",
    "狂野西部：生死同盟": "Call of Juarez Bound in Blood",
    "看门狗2": "Watch Dogs 2",
    "精灵与萤火意志": "Ori and the Will of the Wisps",
    "耻辱": "Dishonored",
    "脑叶公司 | 模拟怪物管理": "Lobotomy Corporation",
    "蝙蝠侠：阿卡姆之城年度版": "Batman Arkham City Game of the Year Edition",
    "蝙蝠侠：阿卡姆疯人院年度版": "Batman Arkham Asylum Game of the Year Edition",
    "蝙蝠侠：阿卡姆骑士": "Batman Arkham Knight",
    "无人愿死": "Nobody Wants to Die",
    "黑暗侦探：黑暗中的摸索": "Shadows of Doubt",
    "死亡细胞": "Dead Cells",
    "荒野大镖客：救赎2": "Red Dead Redemption 2",
    "死亡搁浅：导演剪辑版": "DEATH STRANDING DIRECTOR'S CUT",
    "死亡搁浅2：冥滩之上": "Death Stranding 2",
    "艾迪芬奇的记忆": "What Remains of Edith Finch",
    "耻辱2": "Dishonored 2",
    "战地风云5": "Battlefield V",
    "扣押2": "DISTRAINT 2",
    "拉娜的星球": "Planet of Lana",
    "旁观者2": "Beholder 2",
    "最后的篝火": "The Last Campfire",
    "纪念碑谷：全景版": "Monument Valley",
    "纪念碑谷2：全景版": "Monument Valley 2",
    "幽灵行者": "Ghostrunner",
    "战锤40K：格雷迪厄斯-遗迹之战": "Warhammer 40,000 Gladius",
    "僵尸世界大战：劫后余生": "World War Z Aftermath",
    "逃出方块：收藏版": "The Room",
    "逃离方块：收藏版": "The Room",
    "逃生：试炼": "The Outlast Trials",
    "逃离后室": "Escape the Backrooms",
    "不巷歌": "Don't Disturb",
    "地铁繁花": "Underground Blossom",
    "多重花园": "Manifold Garden",
    "夺蛋骑兵": "Egg Raiders",
    "影子工厂": "Impostor Factory",
    "我是僵尸": "I, Zombie",
    "海浪物语": "Wavetale",
    "甜甜圈都市": "Donut County",
    "白门": "The White Door",
    "盛夏盛开的花": "Flowers Blooming at the End of Summer",
    "绣湖：天堂岛": "Rusty Lake Paradise",
    "绣湖：旅馆": "Rusty Lake Hotel",
    "绣湖：根源": "Rusty Lake Roots",
    "诡计穿越僵尸末日": "Scheming Through Zombie Apocalypse",
    "彩虹小马格斗": "Fighting is Magic",
}

# Hard AppIDs when storesearch scoring flaps on ® / punctuation.
STEAM_APP_IDS: dict[str, int] = {
    "泰坦陨落2": 1237970,
    "狂野西部：生死同盟": 21980,
    "看门狗2": 447040,
    "蝙蝠侠：阿卡姆之城年度版": 200260,
    "蝙蝠侠：阿卡姆疯人院年度版": 35140,
    "蝙蝠侠：阿卡姆骑士": 208650,
    "孤帆远航": 609320,
    "异星装置博物馆": 1507190,
    "扣押：豪华版": 395170,
    "扣押2": 560350,
    "精灵与萤火意志": 1057090,
    "耻辱": 205100,
    "耻辱2": 403640,
    "脑叶公司 | 模拟怪物管理": 568220,
    "我们也在这里": 582500,
    "我们一起在这里": 865360,
    "无人愿死": 1939970,
    "黑暗侦探：黑暗中的摸索": 986130,
    "死亡细胞": 588650,
    "荒野大镖客：救赎2": 1174180,
    "死亡搁浅：导演剪辑版": 1850570,
    "艾迪芬奇的记忆": 501300,
    "战地风云5": 1238810,
    "拉娜的星球": 1608230,
    "旁观者2": 761620,
    "最后的篝火": 926140,
    "幽灵行者": 1139900,
    "战锤40K：格雷迪厄斯-遗迹之战": 489630,
    "僵尸世界大战：劫后余生": 699130,
    "逃生：试炼": 1304930,
    "逃离后室": 1946010,
    "不巷歌": 501840,
    "地铁繁花": 2291850,
    "多重花园": 473950,
    "夺蛋骑兵": 3253440,
    "影子工厂": 1182620,
    "白门": 1145960,
    "盛夏盛开的花": 1173010,
    "绣湖：天堂岛": 744190,
    "绣湖：旅馆": 435120,
    "绣湖：根源": 532110,
    "甜甜圈都市": 702670,
    "诡计穿越僵尸末日": 813540,
    "我是僵尸": 307230,
    "海浪物语": 1823930,
}

# Manual CN → Anilist/Kitsu search strings — free MT is often unusable.
ANIME_TITLE_ALIASES: dict[str, str] = {
    "3月的狮子": "3-gatsu no Lion",
    "一个人的○○小日子": "Hitoribocchi no Marumaru Seikatsu",
    "一起一起这里那里": "Acchi Kocchi",
    "三坪房间的侵略者！": "Invaders of the Rokujouma",
    "冰属性男子和酷酷女同事": "Ice Guy and Cool Female Colleague",
    "品酒要在成为夫妻后": "Sake wa Fuufu ni Natte kara",
    "这个美术社大有问题！": "Kono Bijutsubu ni wa Mondai ga Aru",
    "邻桌的怪同学": "Tonari no Seki-kun",
    "酷爱电影的庞波小姐": "Eiga Daisuki Pompo-san",
    "青春之旅": "Ao Haru Ride",
    "青春猪头少年不会梦到红书包女孩": "Rascal Does Not Dream of a Knapsack Kid",
    "Re：从零开始的异世界生活 Memory Snow(雪之会议)": "Re:Zero Starting Life in Another World Memory Snow",
    "间谍过家家": "SPY×FAMILY",
    "迷宫饭": "Dungeon Meshi",
    "阳光中的青时雨": "Hinata no Aoshigure",
    "鬼灭之刃": "Kimetsu no Yaiba",
    "五等分的新娘": "Gotoubun no Hanayome",
    "孤独摇滚": "Bocchi the Rock",
    "天气之子": "Tenki no Ko",
    "声之形": "Koe no Katachi",
    "秒速五厘米": "Byousoku 5 Centimeter",
    "中二病也要谈恋爱！": "Chuunibyou demo Koi ga Shitai",
    "伪恋": "Nisekoi",
    "四月是你的谎言": "Shigatsu wa Kimi no Uso",
    "小林家的龙女仆": "Kobayashi-san Chi no Maid Dragon",
    "干物妹！小埋": "Himouto Umaru-chan",
    "干物妹！小埋R": "Himouto! Umaru-chan R",
    "辉夜大小姐想让我告白～天才们的恋爱头脑战争～ 第一季": "Kaguya-sama wa Kokurasetai",
    "阿宅的恋爱真难": "Wotaku ni Koi wa Muzukashii",
    "超脱": "Detachment",
    "不知情的转学生硬要凑上来": "Jijou wo Shiranai Tenkousei ga Guigui Kuru",
    "会长是女仆大人！": "Kaichou wa Maid-sama!",
    "不动声色的柏田与喜形于色的太田": "Kashiwada-san to Oota-kun",
    "全员恶玉": "Akudama Drive",
    "告白实行委员会": "Kokuhaku Jikkou Iinkai",
    "幻界战线": "Blood Blockade Battlefront",
    "幻界战线 & BEYOND": "Blood Blockade Battlefront & Beyond",
    "欢迎来到实力之上主义的教室": "ようこそ実力至上主義の教室へ",
    "欢迎来到实力之上主义的教室 第二季": "ようこそ実力至上主義の教室へ 2nd Season",
    "欢迎来到实力之上主义的教室 第三季": "ようこそ実力至上主義の教室へ 3rd Season",
    "欢迎来到实力之上主义的教室 第四季": "ようこそ実力至上主義の教室へ 4th Season",
    "电影版 境界的彼方过去篇": "Beyond the Boundary -I'LL BE HERE- Past",
    "百变的七仓同学": "Giji Harem",
    "碧蓝之海 第二季": "Grand Blue Dreaming Season 2",
    "继母的拖油瓶是我前女友": "Mamahaha no Tsurego ga Motokano datta",
    "胆大党 第二季": "Dandadan Season 2",
    "赤发白雪姬 OVA 不值一提的宝物、这一页": "Akagami no Shirayuki-hime OVA",
    "跃动青春": "Skip and Loafer",
    "关于完全听不懂老公在说什么的事 第一季": "Danna ga Nani wo Itteiru ka Wakaranai Ken",
    "紫罗兰永恒花园外传：永远与自动手记人偶": "Violet Evergarden: Eternity and the Auto Memory Doll",
    "致不灭的你": "To Your Eternity",
    "致不灭的你 第二季": "To Your Eternity Season 2",
    "敦君与女朋友": "Akkun to Kanojo",
    "捡到退婚大小姐的我，教她幸福的事": "Hirotta Kekkon Haki Reijou wo Shiawase ni Suru",
    "你与我最后的战场，亦或是世界起始的圣战": "Our Last Crusade or the Rise of a New World",
    "公司的小小前辈": "My Tiny Senpai",
    "关于前辈很烦人的事": "Senpai ga Uzai Kouhai no Hanashi",
    "别当欧尼酱了！": "Oniichan wa Oshimai!",
    "变态王子与不笑猫": "Hentai Ouji to Warawanai Neko",
    "只要贝尔哲布布大小姐喜欢就好": "As Miss Beelzebub Likes",
    "因为是反派大小姐所以养了魔王": "I'm the Villainess, So I'm Taming the Final Boss",
    "在下坂本，有何贵干？": "Sakamoto desu ga?",
    "大叔与棉花糖": "Ojisan and Marshmallow",
    "天使降临到我身边": "Watashi ni Tenshi ga Maiorita!",
    "奇幻世界舅舅": "Isekai Ojisan",
    "女孩的钓鱼慢活": "Slow Loop",
    "如果能写小说就好了": "Imouto sae Ireba Ii",
    "宇崎学妹想要玩！第二季": "Uzaki-chan wa Asobitai! Season 2",
    "小桃小栗 Love Love物语": "Momokuri",
    "小森同学拒绝不了！": "Komori-san wa Kotowarenai!",
    "尽管如此世界依然美丽": "Soredemo Sekai wa Utsukushii",
    "川柳少女": "Senryuu Shoujo",
    "异度入侵": "ID:INVADED",
    "彻夜之歌 第二季": "Call of the Night Season 2",
    "徒然喜欢你": "Tsuredure Children",
    "心灵想要大声呼喊": "The Anthem of the Heart",
    "总之就是非常可爱 第二季": "Tonikaku Kawaii Season 2",
    "我们大家的河合庄": "Bokura wa Minna Kawaisou",
    "我们无法一起学习": "We Never Learn",
    "我女友与青梅竹马的惨烈修罗场": "Oreshura",
    "我心里危险的东西 第二季": "The Dangers in My Heart Season 2",
    "我的妹妹不可能那么可爱 第一季": "Oreimo",
    "我被逐出队伍后过上慢生活": "Banished from the Hero's Party",
    "擅长捉弄的高木同学 剧场版": "Teasing Master Takagi-san Movie",
    "无能力者娜娜": "Talentless Nana",
    "明日酱的水手服": "Akebi's Sailor Uniform",
    "更衣人偶坠入爱河": "My Dress-Up Darling",
    "更衣人偶坠入爱河 第二季": "My Dress-Up Darling Season 2",
    "月色真美": "Tsuki ga Kirei",
    "未确认进行式": "Engaged to the Unidentified",
    "林家的天使同学": "The Angel Next Door Spoils Me Rotten",
    "邻家的天使同学": "The Angel Next Door Spoils Me Rotten",
    "欢迎来到实力之上主义的教室 第四季": "ようこそ実力至上主義の教室へ 4th Season",
    "正相反的你与我": "You and I Are Polar Opposites",
    "武装少女": "Armed Girl's Machiavellism",
    "死神少爷与黑女仆": "The Duke of Death and His Maid",
    "测不准的阿波连同学": "Aharen-san wa Hakarenai",
    "测不准的阿波连同学 第二季": "Aharen-san wa Hakarenai Season 2",
    "温暖的印记": "Honobono Log",
    "熏香花朵凛然绽放": "The Fragrant Flower Blooms with Dignity",
    "电影版 境界的彼方未来篇": "Beyond the Boundary Future",
    "知晓天空之蓝的人啊": "Her Blue Sky",
    "碧蓝之海": "Grand Blue",
    "笨女孩": "Aho Girl",
    "线上游戏的队友不可能是女生？": "And You Thought There Is Never a Girl Online?",
    "老夫老妻重返青春": "Jiisan Baasan Wakagaeru",
    "胆大党": "Dandadan",
    "莉可丽丝": "Lycoris Recoil",
    "虫师": "Mushishi",
    "被神捡到的男人": "By the Grace of the Gods",
    "见面5秒开始战斗": "Battle Game in 5 Seconds",
    "记录的地平线": "Log Horizon",
    "赤发白雪姬 第二季": "Snow White with the Red Hair Season 2",
    "超人高中生们即便在异世界也能从容生存！": "Choujin Koukousei-tachi wa Isekai demo Yoyuu de Ikinuku you desu!",
}

BOOK_TITLE_ALIASES: dict[str, str] = {
    "下一站,天国": "Wandering in the Garden Wandering Clouds Wandering Life",
    "不要挑战人性": "不要挑战人性",
    "世界上最神奇的60个经典定律": "世界上最神奇的60个经典定律",
    "云边有个小卖部": "云边有个小卖部 张嘉佳",
    "克苏鲁神话Ⅱ 疯狂山脉": "At the Mountains of Madness",
    "地球无应答": "地球无应答 王诺诺",
    "夏天、烟火和我的尸体": "Summer, Fireworks, and My Corpse",
    "天才在左疯子在右：心理疾病漫谈": "天才在左疯子在右",
    "斯坦福高效睡眠法": "斯坦福高效睡眠法",
    "白金数据": "プラチナデータ",
    "窄门": "Strait is the Gate",
    "自学大全": "自学大全",
    "诡秘之主": "Lord of Mysteries",
    "道诡异仙": "道诡异仙",
    "霍乱时期的爱情": "Love in the Time of Cholera",
    "不正常人类症候群": "不正常人类症候群",
    "异草奇花": "异草奇花",
    "胭脂盆地": "胭脂盆地",
    "HMI专业催眠师教程": "Professional Hypnotism Manual",
    "女儿红": "女儿红",
    "倾城之恋": "倾城之恋 张爱玲",
    "某某": "某某 木瓜黄",
    "完美人设": "完美人设",
    "悟空传": "悟空传 今何在",
}

ANILIST_QUERY = """
query ($search: String) {
  Page(page: 1, perPage: 5) {
    media(search: $search, type: ANIME, sort: SEARCH_MATCH) {
      id
      title { romaji native english }
      coverImage { large medium }
      averageScore
      episodes
      seasonYear
      genres
      format
      startDate { year month day }
    }
  }
}
"""

ANILIST_MANGA_QUERY = """
query ($search: String) {
  Page(page: 1, perPage: 5) {
    media(search: $search, type: MANGA, sort: SEARCH_MATCH) {
      id
      title { romaji native english }
      coverImage { large medium }
      averageScore
      genres
      format
      startDate { year month day }
    }
  }
}
"""


def _slug(title: str) -> str:
    digest = hashlib.md5(title.encode("utf-8")).hexdigest()[:10]
    safe = re.sub(r"[^\w\-]+", "_", title, flags=re.UNICODE).strip("_")
    safe = (safe[:48] or "item").strip("_")
    return f"{safe}_{digest}"


def _curl_available() -> bool:
    try:
        subprocess.run(
            ["curl.exe", "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return True
    except (OSError, subprocess.TimeoutExpired):
        return False


_USE_CURL = _curl_available()

# Skip flaky sources for the rest of a run after the first hard network failure.
_SOURCE_SKIP: set[str] = set()


def _http_json(
    url: str,
    *,
    data: bytes | None = None,
    headers: dict | None = None,
    timeout: int = 12,
    retries: int = 1,
) -> dict | list | None:
    """Return parsed JSON, or None on soft miss. Raises TimeoutError/URLError on hard network fail after retries."""
    req_headers = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    last_exc: Exception | None = None
    for attempt in range(max(1, retries)):
        try:
            # Prefer curl.exe for BOTH GET and POST — urllib SSL handshakes often
            # time out on this Windows host while curl succeeds for Anilist/Steam/iTunes.
            if _USE_CURL:
                body, code = _curl_bytes(url, data=data, headers=req_headers, timeout=timeout)
                if code in {400, 404}:
                    return None
                if code == 429:
                    time.sleep(1.2 * (attempt + 1))
                    last_exc = TimeoutError("HTTP 429")
                    continue
                if code == 0 or code >= 500:
                    last_exc = TimeoutError(f"curl http={code} for {url}")
                    time.sleep(0.35 * (attempt + 1))
                    continue
                if code >= 400:
                    last_exc = urllib.error.HTTPError(url, code, f"HTTP {code}", hdrs=None, fp=None)  # type: ignore[arg-type]
                    time.sleep(0.25 * (attempt + 1))
                    continue
                text = body.decode("utf-8", errors="replace")
                if not text.strip():
                    raise TimeoutError(f"empty body for {url}")
                return json.loads(text)
            req = urllib.request.Request(url, data=data, headers=req_headers, method="POST" if data else "GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            text = raw.decode("utf-8", errors="replace")
            if not text.strip():
                raise TimeoutError(f"empty body for {url}")
            return json.loads(text)
        except urllib.error.HTTPError as exc:
            # 404 / 400 are soft misses (e.g. wiki page missing).
            if exc.code in {400, 404}:
                return None
            last_exc = exc
            time.sleep(0.25 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError, subprocess.TimeoutExpired) as exc:
            last_exc = exc
            time.sleep(0.25 * (attempt + 1))
    print(f"  ! http fail: {last_exc}")
    # Propagate hard failures so callers can avoid marking checked=true.
    if isinstance(last_exc, TimeoutError):
        raise last_exc
    if isinstance(last_exc, urllib.error.URLError):
        raise last_exc
    if last_exc is not None:
        raise TimeoutError(str(last_exc))
    return None


def _curl_bytes(
    url: str,
    *,
    data: bytes | None = None,
    headers: dict | None = None,
    timeout: int = 12,
) -> tuple[bytes, int]:
    """GET/POST via curl.exe; returns (body, http_code). code 0 means transport failure.

    Body is written to a temp file (not mixed with -w stdout) to avoid truncated JSON.
    """
    out_path = None
    body_path = None
    try:
        fd_out, out_path = tempfile.mkstemp(prefix="atelier_http_out_", suffix=".bin")
        os.close(fd_out)
        cmd = [
            "curl.exe",
            "-sS",
            "-L",
            "--max-time",
            str(max(3, int(timeout))),
            "-A",
            UA,
            "-o",
            out_path,
            "-w",
            "%{http_code}",
        ]
        for key, value in (headers or {}).items():
            if key.lower() == "user-agent":
                continue
            cmd.extend(["-H", f"{key}: {value}"])
        if data is not None:
            fd, body_path = tempfile.mkstemp(prefix="atelier_http_in_", suffix=".bin")
            os.close(fd)
            Path(body_path).write_bytes(data)
            cmd.extend(["--data-binary", f"@{body_path}"])
        cmd.append(url)
        completed = subprocess.run(cmd, check=False, capture_output=True, timeout=timeout + 5)
        try:
            code = int((completed.stdout or b"0").decode("ascii", errors="ignore").strip() or "0")
        except ValueError:
            code = 0
        body = Path(out_path).read_bytes() if Path(out_path).is_file() else b""
        return body, code
    finally:
        for path in (out_path, body_path):
            if path:
                try:
                    os.unlink(path)
                except OSError:
                    pass


def _find_existing_cover(img_dir: Path, title: str) -> Path | None:
    slug = _slug(title)
    matches = sorted(img_dir.glob(f"{slug}.*"))
    for path in matches:
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"} and path.stat().st_size >= 800:
            return path
    return None


def _has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def _fold_title(text: str) -> str:
    text = (text or "").casefold().strip()
    text = (
        text.replace("·", "")
        .replace("：", ":")
        .replace("！", "!")
        .replace("？", "?")
        .replace("～", "~")
        .replace("—", "-")
        .replace("／", "/")
        .replace("的", "の")
        .replace("与", "と")
    )
    # Fullwidth Latin/digits → ASCII.
    fw = str.maketrans(
        {
            **{ord("０") + i: ord("0") + i for i in range(10)},
            **{ord("Ａ") + i: ord("A") + i for i in range(26)},
            **{ord("ａ") + i: ord("a") + i for i in range(26)},
        }
    )
    text = text.translate(fw)
    text = re.sub(r"[\s\-_/\\\[\]()（）【】『』「」<>]+", "", text)
    return text


def _latin_tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]{2,}", (text or "").casefold()) if t not in {"the", "and", "of", "season", "ova", "oad", "movie", "part"}}


def _cjk_chars(text: str) -> set[str]:
    return set(re.findall(r"[\u4e00-\u9fff]", text or ""))


def _title_match_score(query: str, *candidates: str) -> int:
    """Score how well any candidate title matches the query. 0–100."""
    q = _fold_title(query)
    if not q:
        return 0
    q_latin = _latin_tokens(query)
    q_cjk = _cjk_chars(query)
    best = 0
    for raw in candidates:
        if not raw:
            continue
        c = _fold_title(raw)
        if not c:
            continue
        score = 0
        if c == q:
            score = 100
        elif q in c or c in q:
            score = 86
        else:
            c_latin = _latin_tokens(raw)
            c_cjk = _cjk_chars(raw)
            if q_latin and c_latin:
                inter = q_latin & c_latin
                if inter:
                    score = max(score, int(70 * len(inter) / max(len(q_latin), 1)) + 20)
            if q_cjk and c_cjk:
                inter_c = q_cjk & c_cjk
                if len(inter_c) >= 2:
                    score = max(score, int(75 * len(inter_c) / max(len(q_cjk), 1)) + 15)
                elif len(inter_c) == 1 and len(q_cjk) <= 3:
                    score = max(score, 45)
            # Character bigrams for JP/CN near-matches.
            if len(q) >= 4 and len(c) >= 4:
                qb = {q[i : i + 2] for i in range(len(q) - 1)}
                cb = {c[i : i + 2] for i in range(len(c) - 1)}
                if qb and cb:
                    ratio = len(qb & cb) / max(len(qb), 1)
                    if ratio >= 0.35:
                        score = max(score, int(55 + 40 * ratio))
        best = max(best, score)
    return best


def _titles_compatible(query: str, *candidates: str, minimum: int = 55) -> bool:
    for alias_map_name in ("ANIME_TITLE_ALIASES", "STEAM_TITLE_ALIASES", "MOVIE_TITLE_ALIASES"):
        alias_map = globals().get(alias_map_name) or {}
        alias = alias_map.get(query)
        if alias and _title_match_score(alias, *candidates) >= minimum:
            return True
    return _title_match_score(query, *candidates) >= minimum


def _download(url: str, dest: Path, timeout: int = 18) -> bool:
    if not url or url.startswith("data:"):
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    extra_headers = {"Accept": "image/*,*/*"}
    if "doubanio.com" in url or "douban.com" in url:
        extra_headers["Referer"] = "https://movie.douban.com/"
    try:
        body = b""
        ctype = ""
        if _USE_CURL:
            fd, tmp_path = tempfile.mkstemp(prefix="atelier_img_", suffix=".bin")
            os.close(fd)
            try:
                cmd = [
                    "curl.exe",
                    "-sS",
                    "-L",
                    "--fail",
                    "--max-time",
                    str(max(3, int(timeout))),
                    "-A",
                    UA,
                    "-o",
                    tmp_path,
                    "-w",
                    "%{content_type}",
                ]
                for key, value in extra_headers.items():
                    cmd.extend(["-H", f"{key}: {value}"])
                cmd.append(url)
                completed = subprocess.run(cmd, check=False, capture_output=True, timeout=timeout + 5)
                if completed.returncode != 0:
                    return False
                ctype = (completed.stdout or b"").decode("latin-1", errors="ignore").lower()
                body = Path(tmp_path).read_bytes()
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
        else:
            req = urllib.request.Request(url, headers={"User-Agent": UA, **extra_headers})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                ctype = (resp.headers.get("Content-Type") or "").lower()
        if len(body) < 800:
            return False
        if "html" in ctype or body[:15].lstrip().lower().startswith(b"<!doctype"):
            return False
        # Sniff image magic if content-type missing.
        if body[:8] == b"\x89PNG\r\n\x1a\n":
            dest = dest.with_suffix(".png")
        elif body[:2] == b"\xff\xd8":
            dest = dest.with_suffix(".jpg")
        elif body[:4] == b"RIFF" and body[8:12] == b"WEBP":
            dest = dest.with_suffix(".webp")
        elif "png" in ctype:
            dest = dest.with_suffix(".png")
        elif "webp" in ctype:
            dest = dest.with_suffix(".webp")
        elif "jpeg" in ctype or "jpg" in ctype:
            dest = dest.with_suffix(".jpg")
        elif dest.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            dest = dest.with_suffix(".jpg")
        dest.write_bytes(body)
        return True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"  ! download fail: {exc}")
        return False


def _load_sheet(sheet: str) -> list[tuple]:
    import openpyxl

    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    return rows


def _cell(v) -> str:
    if v is None:
        return ""
    return str(v).strip()


def load_anime() -> list[dict]:
    rows = _load_sheet("番剧")
    items = []
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        name = _cell(row[0])
        if not name or name == "名称":
            continue
        items.append({"key": name, "title": name, "series": _cell(row[1]) if len(row) > 1 else ""})
    return items


def load_games() -> list[dict]:
    rows = _load_sheet("游戏")
    items = []
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        name = _cell(row[0])
        if not name or name == "名称":
            continue
        items.append(
            {
                "key": name,
                "title": name,
                "series": _cell(row[1]) if len(row) > 1 else "",
                "platform": _cell(row[2]) if len(row) > 2 else "",
            }
        )
    return items


def load_movies() -> list[dict]:
    rows = _load_sheet("电影")
    items = []
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        name = _cell(row[0])
        if not name or name == "名称":
            continue
        items.append({"key": name, "title": name, "series": _cell(row[1]) if len(row) > 1 else ""})
    return items


def load_books() -> list[dict]:
    rows = _load_sheet("书籍")
    items = []
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        title = _cell(row[0])
        if not title or title in {"书名", "名称"}:
            continue
        items.append(
            {
                "key": title,
                "title": title,
                "author": _cell(row[1]) if len(row) > 1 else "",
                "category": _cell(row[2]) if len(row) > 2 else "",
            }
        )
    return items


def _load_meta(kind: str) -> dict:
    path = META_DIR / f"{kind}.json"
    if not path.is_file():
        return {"items": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {"items": {}}


def _cover_exists(rec: dict) -> bool:
    cover = (rec.get("cover_path") or "").strip()
    if not cover.startswith("/static/"):
        return False
    return (ROOT / cover.lstrip("/")).is_file()


def _record_richness(rec: dict) -> tuple:
    cover = 1 if _cover_exists(rec) else 0
    matched = 1 if rec.get("matched") and cover else 0
    checked = 1 if rec.get("checked") else 0
    extras = sum(1 for k in ("subtitle", "score", "year", "source", "source_id") if rec.get(k) not in (None, ""))
    return (cover, matched, checked, extras)


def _merge_meta_items(primary: dict, secondary: dict) -> dict:
    """Merge meta records without dropping real on-disk covers.

    - A record whose cover_path file exists beats one without a real file.
    - Otherwise the primary (caller/in-memory) wins so clears/resets stick.
    """
    out = dict(secondary)
    for key, rec in primary.items():
        if not isinstance(rec, dict):
            continue
        prev = out.get(key)
        if not isinstance(prev, dict):
            out[key] = rec
            continue
        rec_cover = 1 if _cover_exists(rec) else 0
        prev_cover = 1 if _cover_exists(prev) else 0
        if rec_cover and not prev_cover:
            out[key] = rec
        elif prev_cover and not rec_cover:
            out[key] = prev
        elif rec_cover and prev_cover:
            out[key] = rec if _record_richness(rec) >= _record_richness(prev) else prev
        else:
            # Neither has a real cover file — prefer primary so clears stick.
            out[key] = rec
    return out


def _save_meta(kind: str, meta: dict) -> None:
    META_DIR.mkdir(parents=True, exist_ok=True)
    path = META_DIR / f"{kind}.json"
    # Merge with on-disk items before write so we never shrink cover coverage.
    # Mutate the existing items dict in place — callers keep a `bucket` reference.
    disk = _load_meta(kind)
    disk_items = disk.get("items") if isinstance(disk.get("items"), dict) else {}
    bucket = meta.setdefault("items", {})
    if not isinstance(bucket, dict):
        bucket = {}
        meta["items"] = bucket
    merged = _merge_meta_items(bucket, disk_items)
    if bucket is not merged:
        bucket.clear()
        bucket.update(merged)
    meta["items"] = bucket
    meta["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    # utf-8 without BOM; atomic replace avoids readers seeing truncated JSON.
    payload = json.dumps(meta, ensure_ascii=False, indent=2)
    tmp = path.with_name(f"{path.stem}.{os.getpid()}.tmp")
    tmp.write_text(payload, encoding="utf-8")
    os.replace(tmp, path)


def _pick_anilist(media_list: list, query: str, *extra_queries: str) -> dict | None:
    """Pick Anilist row only when title similarity clears the bar — never first-result fallback."""
    if not media_list:
        return None
    queries = [query, *[q for q in extra_queries if q]]
    alias = ANIME_TITLE_ALIASES.get(query)
    if alias:
        queries.append(alias)
    best = None
    best_score = -1
    for m in media_list:
        titles = m.get("title") or {}
        candidates = [titles.get("native") or "", titles.get("romaji") or "", titles.get("english") or ""]
        score = 0
        for q in queries:
            score = max(score, _title_match_score(q, *candidates))
        if score > best_score:
            best_score = score
            best = m
    # Require a real match — returning media_list[0] caused mass wrong covers.
    return best if best_score >= 55 else None


_TRANSLATE_CACHE: dict[str, str] | None = None


def _load_translate_cache() -> dict[str, str]:
    global _TRANSLATE_CACHE
    if _TRANSLATE_CACHE is not None:
        return _TRANSLATE_CACHE
    if TRANSLATE_CACHE_PATH.is_file():
        try:
            payload = json.loads(TRANSLATE_CACHE_PATH.read_text(encoding="utf-8-sig"))
            if isinstance(payload, dict):
                _TRANSLATE_CACHE = {str(k): str(v) for k, v in payload.items() if v}
                return _TRANSLATE_CACHE
        except (OSError, json.JSONDecodeError, TypeError):
            pass
    _TRANSLATE_CACHE = {}
    return _TRANSLATE_CACHE


def _save_translate_cache() -> None:
    if _TRANSLATE_CACHE is None:
        return
    META_DIR.mkdir(parents=True, exist_ok=True)
    TRANSLATE_CACHE_PATH.write_text(
        json.dumps(_TRANSLATE_CACHE, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def translate_zh_en(text: str) -> str | None:
    """MyMemory free MT — helps Anilist/Kitsu match Chinese titles."""
    text = text.strip()
    if not text or not _has_cjk(text):
        return None
    cache = _load_translate_cache()
    if text in cache:
        return cache[text] or None
    qs = urllib.parse.urlencode({"q": text, "langpair": "zh-CN|en"})
    try:
        data = _http_json(f"{MYMEMORY_URL}?{qs}", timeout=12, retries=1)
    except (urllib.error.URLError, TimeoutError):
        return None
    if not isinstance(data, dict):
        return None
    translated = ((data.get("responseData") or {}).get("translatedText") or "").strip()
    if not translated or translated.casefold() == text.casefold():
        cache[text] = ""
        _save_translate_cache()
        return None
    cache[text] = translated
    _save_translate_cache()
    return translated


def _anime_query_variants(title: str) -> list[str]:
    queries: list[str] = []

    def add(value: str) -> None:
        value = value.strip()
        if value and value not in queries:
            queries.append(value)

    # Manual aliases first — much more reliable than free MT.
    alias = ANIME_TITLE_ALIASES.get(title.strip())
    if alias:
        add(alias)
    add(title)
    # Common Chinese → Japanese particle guesses help Anilist search.
    add(title.replace("的", "の").replace("与", "と"))
    add(title.replace("月的", "月の"))
    # Fullwidth digits often used in JP titles (３月のライオン).
    trans = str.maketrans("0123456789", "０１２３４５６７８９")
    add(title.translate(trans).replace("的", "の"))
    for sep in (" 第", "第", "（", "(", "：", ":", "～", "~", " "):
        if sep in title:
            add(title.split(sep, 1)[0])
    # CN → EN only as last resort (MyMemory often invents garbage).
    if _has_cjk(title) and title.strip() not in ANIME_TITLE_ALIASES:
        en = translate_zh_en(title)
        if en and len(en) < 80:
            add(en)
            shortened = re.sub(r"\b(the|a|an|of|and)\b", " ", en, flags=re.I)
            shortened = re.sub(r"\s+", " ", shortened).strip()
            if shortened and len(shortened) < 60:
                add(shortened)
    return queries


def search_bangumi_anime(title: str) -> dict | None:
    """Bangumi search — strongest for Chinese titles."""
    url = BANGUMI_SEARCH + urllib.parse.quote(title) + "?type=2&responseGroup=small"
    try:
        data = _http_json(url, timeout=10, retries=1)
    except (urllib.error.URLError, TimeoutError):
        raise
    if not isinstance(data, dict):
        return None
    # API may return list at top level or under "list"
    rows = data.get("list") if isinstance(data.get("list"), list) else None
    if rows is None and isinstance(data, list):
        rows = data
    if not rows:
        return None
    q = title.casefold().replace(" ", "")
    pick = rows[0]
    best = -1
    for row in rows[:8]:
        if not isinstance(row, dict):
            continue
        names = [
            str(row.get("name") or ""),
            str(row.get("name_cn") or ""),
        ]
        score = 0
        for name in names:
            n = name.casefold().replace(" ", "")
            if not n:
                continue
            if n == q:
                score = 100
            elif q in n or n in q:
                score = max(score, 80)
        if score > best:
            best = score
            pick = row
    images = pick.get("images") if isinstance(pick.get("images"), dict) else {}
    cover = images.get("large") or images.get("common") or images.get("medium") or ""
    if not cover:
        return None
    rating = pick.get("rating") if isinstance(pick.get("rating"), dict) else {}
    score_val = rating.get("score")
    return {
        "source": "bangumi",
        "source_id": pick.get("id") or "",
        "subtitle": pick.get("name_cn") or pick.get("name") or "",
        "cover_url": cover,
        "score": round(float(score_val), 1) if isinstance(score_val, (int, float)) and score_val else None,
        "episodes": pick.get("eps") or pick.get("eps_count"),
        "year": None,
        "date": (pick.get("air_date") or "")[:10],
        "tags": [],
        "format": str(pick.get("type") or ""),
    }


def search_anilist_anime(title: str) -> dict | None:
    media: list = []
    used_query = title
    network_error = False
    variants = _anime_query_variants(title)[:6]
    hit: dict | None = None
    for q in variants:
        payload = json.dumps(
            {"query": ANILIST_QUERY, "variables": {"search": q}},
            ensure_ascii=False,
        ).encode("utf-8")
        try:
            data = _http_json(
                ANILIST_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                timeout=12,
                retries=1,
            )
        except (urllib.error.URLError, TimeoutError):
            network_error = True
            continue
        if not isinstance(data, dict):
            continue
        if data.get("errors"):
            print(f"  ! anilist errors: {data.get('errors')[:1]}")
            time.sleep(1.0)
            continue
        page_media = (((data.get("data") or {}).get("Page") or {}).get("media")) or []
        if page_media:
            used_query = q
            media = page_media
            hit = _pick_anilist(page_media, title, used_query, *variants[:4])
            if hit:
                break
        time.sleep(0.15)
    if not hit:
        hit = _pick_anilist(media, title, used_query, *variants[:4])
    if not hit:
        if network_error and not media:
            raise TimeoutError("anilist unreachable")
        return None
    titles = hit.get("title") or {}
    cover = (hit.get("coverImage") or {}).get("large") or (hit.get("coverImage") or {}).get("medium") or ""
    genres = hit.get("genres") or []
    date = hit.get("startDate") or {}
    date_str = ""
    if date.get("year"):
        parts = [str(date["year"])]
        if date.get("month"):
            parts.append(f"{int(date['month']):02d}")
        if date.get("day"):
            parts.append(f"{int(date['day']):02d}")
        date_str = "-".join(parts)
    score = hit.get("averageScore")
    return {
        "source": "anilist",
        "source_id": hit.get("id"),
        "subtitle": titles.get("native") or titles.get("romaji") or titles.get("english") or "",
        "cover_url": cover,
        "score": round(score / 10, 1) if isinstance(score, (int, float)) and score else None,
        "episodes": hit.get("episodes"),
        "year": hit.get("seasonYear") or date.get("year"),
        "date": date_str,
        "tags": genres[:5],
        "format": hit.get("format") or "",
        "matched_query": used_query,
    }


def search_kitsu_anime(title: str) -> dict | None:
    """Kitsu anime search — good English/romaji coverage; scored, never first-hit."""
    queries: list[str] = []
    alias = ANIME_TITLE_ALIASES.get(title.strip())
    if alias:
        queries.append(alias)
    queries.append(title)
    if _has_cjk(title) and title.strip() not in ANIME_TITLE_ALIASES:
        en = translate_zh_en(title)
        if en:
            queries.append(en)
    network_error = False
    for q in queries[:4]:
        qs = urllib.parse.urlencode({"filter[text]": q, "page[limit]": 5})
        try:
            data = _http_json(
                f"{KITSU_ANIME}?{qs}",
                headers={
                    "Accept": "application/vnd.api+json",
                    "Content-Type": "application/vnd.api+json",
                },
                timeout=12,
                retries=1,
            )
        except (urllib.error.URLError, TimeoutError):
            network_error = True
            continue
        if not isinstance(data, dict):
            continue
        rows = data.get("data") or []
        if not rows:
            continue
        best = None
        best_score = -1
        best_attrs = None
        for row in rows:
            attrs = row.get("attributes") or {}
            titles = attrs.get("titles") or {}
            candidates = [
                titles.get("ja_jp") or "",
                titles.get("en_jp") or "",
                titles.get("en") or "",
                attrs.get("canonicalTitle") or "",
            ]
            score = max(_title_match_score(title, *candidates), _title_match_score(q, *candidates))
            if alias:
                score = max(score, _title_match_score(alias, *candidates))
            if score > best_score:
                best_score = score
                best = row
                best_attrs = attrs
        if not best or best_score < 55 or not best_attrs:
            continue
        poster = best_attrs.get("posterImage") or {}
        cover = poster.get("large") or poster.get("medium") or poster.get("original") or ""
        if not cover:
            continue
        titles = best_attrs.get("titles") or {}
        subtitle = (
            titles.get("ja_jp")
            or titles.get("en_jp")
            or titles.get("en")
            or best_attrs.get("canonicalTitle")
            or ""
        )
        rating = best_attrs.get("averageRating")
        return {
            "source": "kitsu",
            "source_id": best.get("id") or "",
            "subtitle": subtitle,
            "cover_url": cover,
            "score": round(float(rating) / 10, 1) if rating not in (None, "") else None,
            "episodes": best_attrs.get("episodeCount"),
            "year": (best_attrs.get("startDate") or "")[:4] or None,
            "date": best_attrs.get("startDate") or "",
            "tags": [],
            "format": best_attrs.get("subtype") or "",
            "matched_query": q,
        }
    if network_error:
        raise TimeoutError("kitsu unreachable")
    return None


def search_wikipedia_title(title: str, *, kind_hint: str = "", pages: list[str] | None = None) -> dict | None:
    # Keep candidate set tiny — each miss can cost multi-second timeouts.
    candidates: list[str] = []
    for p in pages or []:
        if p and p not in candidates:
            candidates.append(p)
    if title and title not in candidates:
        candidates.append(title)
    if kind_hint == "anime":
        candidates.append(f"{title} (动画)")
    elif kind_hint == "game":
        candidates.append(f"{title} (video game)")
    elif kind_hint == "movie":
        alias = MOVIE_TITLE_ALIASES.get(title.strip(), "")
        if alias:
            candidates.extend([alias, f"{alias} (film)", f"{alias} (movie)"])
    bases = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/",
        "https://zh.wikipedia.org/api/rest_v1/page/summary/",
    )
    network_error = False
    for cand in candidates[:6]:
        # Page titles may already use underscores; also try spaced form.
        variants = [cand]
        if "_" in cand:
            variants.append(cand.replace("_", " "))
        for variant in variants:
            for base in bases:
                url = base + urllib.parse.quote(variant, safe="")
                try:
                    data = _http_json(url, timeout=8, retries=1)
                except (urllib.error.URLError, TimeoutError):
                    network_error = True
                    continue
                if not isinstance(data, dict):
                    continue
                if data.get("type") in {"disambiguation", "https://mediawiki.org/wiki/HyperSwitch/errors/not_found"}:
                    continue
                if data.get("title") and "does not exist" in str(data.get("detail") or "").lower():
                    continue
                thumb = (data.get("thumbnail") or {}).get("source") or ""
                original = (data.get("originalimage") or {}).get("source") or ""
                cover = original or thumb
                if not cover:
                    continue
                # Strip tracking query params from upload.wikimedia.org URLs.
                cover = cover.split("?", 1)[0]
                desc = data.get("description") or ""
                return {
                    "source": "wikipedia",
                    "source_id": data.get("pageid") or data.get("title") or "",
                    "subtitle": data.get("title") or title,
                    "cover_url": cover,
                    "score": None,
                    "episodes": None,
                    "year": None,
                    "date": "",
                    "tags": [desc] if desc else [],
                    "format": kind_hint or "",
                }
    if network_error:
        raise TimeoutError("wikipedia unreachable")
    return None


def search_wikipedia_movie(title: str) -> dict | None:
    pages: list[str] = []
    wiki = MOVIE_WIKI_PAGES.get(title.strip())
    if wiki:
        pages.append(wiki)
    alias = MOVIE_TITLE_ALIASES.get(title.strip())
    if alias:
        pages.extend([alias, f"{alias} (film)"])
    return search_wikipedia_title(title, kind_hint="movie", pages=pages)


def _steam_title_variants(title: str) -> list[str]:
    """Normalize CJK punctuation / fullwidth Latin so Steam storesearch hits better."""
    out: list[str] = []

    def add(value: str) -> None:
        value = value.strip()
        if value and value not in out:
            out.append(value)

    add(title)
    # Fullwidth Latin / digits / common roman numerals → ASCII.
    fw = str.maketrans(
        {
            **{ord("０") + i: ord("0") + i for i in range(10)},
            **{ord("Ａ") + i: ord("A") + i for i in range(26)},
            **{ord("ａ") + i: ord("a") + i for i in range(26)},
            ord("："): ord(":"),
            ord("／"): ord("/"),
            ord("－"): ord("-"),
            ord("—"): ord("-"),
            ord("～"): ord("~"),
            ord("Ⅰ"): ord("I"),
            ord("Ⅱ"): "II",
            ord("Ⅲ"): "III",
            ord("Ⅳ"): "IV",
            ord("Ⅴ"): "V",
            ord("Ⅵ"): "VI",
            ord("Ⅶ"): "VII",
            ord("Ⅷ"): "VIII",
            ord("Ⅸ"): "IX",
            ord("Ⅹ"): "X",
        }
    )
    add(title.translate(fw))
    return out


def _steam_fold(text: str) -> str:
    """Fold Steam titles for comparison — strip ® ™ : _ - and spaces."""
    text = (text or "").casefold()
    for ch in ("®", "™", "©", ":", "_", "-", "–", "—", ".", ",", "'", '"', "!", "?"):
        text = text.replace(ch, " ")
    return re.sub(r"\s+", " ", text).strip()


def search_steam_game(title: str) -> dict | None:
    network_error = False
    # Known AppID short-circuit — avoids storesearch punctuation/® mismatches.
    known_id = STEAM_APP_IDS.get(title.strip())
    if known_id:
        cover = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{known_id}/library_600x900.jpg"
        return {
            "source": "steam",
            "source_id": known_id,
            "subtitle": STEAM_TITLE_ALIASES.get(title.strip(), title),
            "cover_url": cover,
            "cover_url_fallback": f"https://cdn.cloudflare.steamstatic.com/steam/apps/{known_id}/header.jpg",
            "score": None,
            "episodes": None,
            "year": None,
            "date": "",
            "tags": [],
            "format": "",
            "meta_extra": "",
        }
    terms = _steam_title_variants(title)
    alias = STEAM_TITLE_ALIASES.get(title.strip())
    if alias:
        terms = [alias] + [t for t in terms if t != alias]
    if _has_cjk(title):
        en = translate_zh_en(title)
        if en and en not in terms:
            terms.append(en)
    # Cap attempts — when Steam is unreachable, fall through to iTunes quickly.
    attempts = 0
    for term in terms[:3]:
        for lang, cc in (("english", "us"), ("schinese", "cn")):
            if attempts >= 3 and network_error:
                break
            attempts += 1
            qs = urllib.parse.urlencode({"term": term, "l": lang, "cc": cc})
            try:
                data = _http_json(f"{STEAM_SEARCH}?{qs}", timeout=8, retries=1)
            except (urllib.error.URLError, TimeoutError):
                network_error = True
                time.sleep(0.2)
                continue
            if not isinstance(data, dict):
                continue
            items = data.get("items") or []
            if not items:
                continue
            # Prefer apps over soundtracks/DLC; exact title beats substring.
            q = _steam_fold(term)
            best = None
            best_score = -1
            for it in items:
                if (it.get("type") or "app") != "app":
                    continue
                name = _steam_fold(it.get("name") or "")
                if not name:
                    continue
                score = 0
                if name == q:
                    score = 100
                elif name.startswith(q + " ") or q.startswith(name + " "):
                    score = 70
                elif q in name or name in q:
                    score = 55
                # Penalize soundtrack / OST noise.
                if any(tok in name for tok in ("soundtrack", "ost", "demo", "trailer")):
                    score -= 30
                if score > best_score:
                    best_score = score
                    best = it
            if not best or best_score < 50:
                continue
            pick = best
            appid = pick.get("id")
            if not appid:
                continue
            cover = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/library_600x900.jpg"
            tiny = pick.get("tiny_image") or ""
            price = pick.get("price") or {}
            return {
                "source": "steam",
                "source_id": appid,
                "subtitle": pick.get("name") or "",
                "cover_url": cover,
                "cover_url_fallback": tiny,
                "score": None,
                "episodes": None,
                "year": None,
                "date": "",
                "tags": [],
                "format": "",
                "meta_extra": price.get("final_formatted") if isinstance(price, dict) else "",
            }
        if network_error and attempts >= 3:
            break
    # Soft-miss when Steam flaps — caller can try iTunes without treating as hard defer.
    if network_error:
        print("  · steam unreachable; trying fallback", flush=True)
    return None


def search_itunes_game(title: str) -> dict | None:
    """iTunes software search — reliable fallback when Steam storesearch flaps."""
    terms = _steam_title_variants(title)
    alias = STEAM_TITLE_ALIASES.get(title.strip())
    if alias:
        terms = [alias] + [t for t in terms if t != alias]
    if _has_cjk(title):
        en = translate_zh_en(title)
        if en and en not in terms:
            terms.append(en)
    # CJK CN titles rarely exist as iOS software under the same name — require a
    # strong EN alias hit so we don't accept "Subway®" for 地铁繁花 etc.
    min_score = 78 if _has_cjk(title) else 55
    network_error = False
    for term in terms[:4]:
        for country in ("us", "cn", "jp"):
            qs = urllib.parse.urlencode(
                {"term": term, "entity": "software", "media": "software", "limit": 5, "country": country}
            )
            try:
                data = _http_json(f"{ITUNES_SEARCH}?{qs}", timeout=10, retries=1)
            except (urllib.error.URLError, TimeoutError):
                network_error = True
                continue
            if not isinstance(data, dict):
                continue
            results = data.get("results") or []
            if not results:
                continue
            pick = None
            best = -1
            for row in results:
                name = str(row.get("trackName") or row.get("trackCensoredName") or "")
                score = max(_title_match_score(title, name), _title_match_score(term, name))
                if alias:
                    score = max(score, _title_match_score(alias, name))
                genres = [str(g).casefold() for g in (row.get("genres") or [])]
                if any("game" in g for g in genres):
                    score += 8
                if score > best:
                    best = score
                    pick = row
            if not pick or best < min_score:
                continue
            cover = (
                pick.get("artworkUrl512")
                or _itunes_artwork(pick.get("artworkUrl100") or pick.get("artworkUrl60") or "")
            )
            if not cover:
                continue
            return {
                "source": "itunes_software",
                "source_id": pick.get("trackId") or "",
                "subtitle": pick.get("trackName") or pick.get("trackCensoredName") or "",
                "cover_url": cover,
                "score": None,
                "episodes": None,
                "year": (pick.get("releaseDate") or "")[:4] or None,
                "date": (pick.get("releaseDate") or "")[:10],
                "tags": [str(g) for g in (pick.get("genres") or [])[:4]],
                "format": "software",
            }
    if network_error:
        raise TimeoutError("itunes games unreachable")
    return None


def search_wikipedia_game(title: str) -> dict | None:
    return search_wikipedia_title(title, kind_hint="game")


def search_open_library(title: str, author: str = "") -> dict | None:
    params = {"title": title, "limit": 5}
    if author and author not in {"专业教材", "作者"}:
        params["author"] = author
    qs = urllib.parse.urlencode(params)
    try:
        data = _http_json(f"{OPENLIB_SEARCH}?{qs}", timeout=12, retries=1)
    except (urllib.error.URLError, TimeoutError):
        raise
    if not isinstance(data, dict):
        return None
    docs = data.get("docs") or []
    if not docs:
        params.pop("author", None)
        qs = urllib.parse.urlencode(params)
        try:
            data = _http_json(f"{OPENLIB_SEARCH}?{qs}", timeout=12, retries=1)
        except (urllib.error.URLError, TimeoutError):
            raise
        docs = (data or {}).get("docs") if isinstance(data, dict) else []
        docs = docs or []
    if not docs:
        return None
    doc = docs[0]
    cover_i = doc.get("cover_i")
    cover = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg" if cover_i else ""
    authors = doc.get("author_name") or []
    subjects = doc.get("subject") or []
    return {
        "source": "openlibrary",
        "source_id": doc.get("key") or "",
        "subtitle": ", ".join(authors[:2]) if authors else author,
        "cover_url": cover,
        "score": None,
        "episodes": None,
        "year": (doc.get("first_publish_year") or None),
        "date": str(doc.get("first_publish_year") or ""),
        "tags": [str(s) for s in subjects[:4] if s],
        "format": "",
    }


def search_google_books(title: str, author: str = "") -> dict | None:
    q_parts = [f"intitle:{title}"]
    if author and author not in {"专业教材", "作者"}:
        q_parts.append(f"inauthor:{author}")
    qs = urllib.parse.urlencode({"q": " ".join(q_parts), "maxResults": 5, "printType": "books", "langRestrict": "zh"})
    try:
        data = _http_json(f"{GOOGLE_BOOKS}?{qs}", timeout=8, retries=1)
    except (urllib.error.URLError, TimeoutError):
        raise
    if not isinstance(data, dict) or not data.get("items"):
        qs2 = urllib.parse.urlencode({"q": title, "maxResults": 5, "printType": "books"})
        try:
            data = _http_json(f"{GOOGLE_BOOKS}?{qs2}", timeout=8, retries=1)
        except (urllib.error.URLError, TimeoutError):
            raise
    if not isinstance(data, dict):
        return None
    items = data.get("items") or []
    if not items:
        return None
    info = (items[0].get("volumeInfo") or {})
    images = info.get("imageLinks") or {}
    cover = images.get("thumbnail") or images.get("smallThumbnail") or ""
    cover = cover.replace("http://", "https://")
    if cover:
        cover = re.sub(r"zoom=\d", "zoom=2", cover)
    authors = info.get("authors") or []
    cats = info.get("categories") or []
    return {
        "source": "google_books",
        "source_id": items[0].get("id") or "",
        "subtitle": ", ".join(authors[:2]) if authors else author,
        "cover_url": cover,
        "score": None,
        "episodes": None,
        "year": (info.get("publishedDate") or "")[:4] or None,
        "date": info.get("publishedDate") or "",
        "tags": cats[:4],
        "format": "",
    }


def _itunes_artwork(url: str) -> str:
    """Upscale iTunes artwork thumbnails to a usable cover size."""
    if not url:
        return ""
    return re.sub(r"/\d+x\d+bb\.", "/600x600bb.", url)


def search_itunes_book(title: str, author: str = "") -> dict | None:
    """Apple iTunes Search API — reliable on this host for ebook covers."""
    queries: list[str] = []

    def add(q: str) -> None:
        q = q.strip()
        if q and q not in queries:
            queries.append(q)

    add(f"{title} {author}".strip() if author and author not in {"专业教材", "作者"} else title)
    add(title)
    book_alias = BOOK_TITLE_ALIASES.get(title.strip(), "")
    if book_alias:
        add(book_alias)
        if author and author not in {"专业教材", "作者"}:
            add(f"{book_alias} {author}".strip())
    network_error = False
    # Prefer CN store for CJK list titles — US ebook search invents unrelated authors.
    countries = ("cn", "jp", "us") if _has_cjk(title) else ("us", "cn", "jp")
    min_score = 72 if _has_cjk(title) else 55
    for q in queries:
        for country in countries:
            qs = urllib.parse.urlencode(
                {"term": q, "entity": "ebook", "media": "ebook", "limit": 5, "country": country}
            )
            try:
                data = _http_json(f"{ITUNES_SEARCH}?{qs}", timeout=10, retries=1)
            except (urllib.error.URLError, TimeoutError):
                network_error = True
                continue
            if not isinstance(data, dict):
                continue
            results = data.get("results") or []
            if not results:
                continue
            pick = None
            best = -1
            for row in results:
                name = str(row.get("trackName") or row.get("collectionName") or "")
                score = max(_title_match_score(title, name), _title_match_score(q, name))
                artist = str(row.get("artistName") or "")
                if author and author not in {"专业教材", "作者"} and author.casefold() in artist.casefold():
                    score += 15
                # CJK list title must share CJK with the store title — blocks Dickens/etc.
                if _has_cjk(title) and _has_cjk(name):
                    if not any(ch in name for ch in title if "\u4e00" <= ch <= "\u9fff"):
                        score -= 40
                elif _has_cjk(title) and not _has_cjk(name):
                    score -= 25
                if score > best:
                    best = score
                    pick = row
            if not pick or best < min_score:
                continue
            cover = _itunes_artwork(
                pick.get("artworkUrl100") or pick.get("artworkUrl60") or pick.get("artworkUrl600") or ""
            )
            if not cover:
                continue
            year = (pick.get("releaseDate") or "")[:4] or None
            genres = pick.get("genres") or []
            return {
                "source": "itunes",
                "source_id": pick.get("trackId") or pick.get("collectionId") or "",
                "subtitle": pick.get("artistName") or author,
                "cover_url": cover,
                "score": None,
                "episodes": None,
                "year": int(year) if year and str(year).isdigit() else None,
                "date": (pick.get("releaseDate") or "")[:10],
                "tags": [str(g) for g in genres[:4] if g and str(g) != "Books"],
                "format": "ebook",
            }
    if network_error:
        raise TimeoutError("itunes unreachable")
    return None


def _douban_poster_url(url: str) -> str:
    """Prefer large Douban poster variants when the suggest API returns a small thumb."""
    if not url:
        return ""
    upgraded = url
    for small, large in (
        ("/s_ratio_poster/", "/l_ratio_poster/"),
        ("/m_ratio_poster/", "/l_ratio_poster/"),
        ("/s_ratio/", "/l_ratio_poster/"),
    ):
        if small in upgraded:
            upgraded = upgraded.replace(small, large)
            break
    return upgraded


def search_douban_movie(title: str) -> dict | None:
    """Douban movie subject_suggest — good when not rate-limited (empty list)."""
    if "douban" in _SOURCE_SKIP:
        return None
    queries: list[str] = []

    def add(q: str) -> None:
        q = q.strip()
        if q and q not in queries:
            queries.append(q)

    add(title)
    soft = re.sub(r"[（(].*?[）)]", "", title).strip()
    add(soft)
    if _has_cjk(title):
        en = translate_zh_en(title)
        if en:
            add(en)

    network_error = False
    empty_streak = 0
    best: dict | None = None
    best_score = -1
    q_fold = title.casefold().replace(" ", "").replace("·", "").replace("：", ":").replace("！", "!")
    for q in queries[:4]:
        qs = urllib.parse.urlencode({"q": q})
        url = f"https://movie.douban.com/j/subject_suggest?{qs}"
        try:
            data = _http_json(
                url,
                headers={"Referer": "https://movie.douban.com/", "Accept": "application/json"},
                timeout=10,
                retries=1,
            )
        except (urllib.error.URLError, TimeoutError):
            network_error = True
            continue
        if not isinstance(data, list):
            continue
        if not data:
            empty_streak += 1
            continue
        empty_streak = 0
        for row in data:
            if not isinstance(row, dict):
                continue
            name = str(row.get("title") or "").strip()
            if not name:
                continue
            sub = str(row.get("sub_title") or row.get("year") or "")
            typ = str(row.get("type") or "")
            img = _douban_poster_url(str(row.get("img") or ""))
            if not img:
                continue
            name_fold = name.casefold().replace(" ", "").replace("·", "").replace("：", ":").replace("！", "!")
            score = 0
            if name_fold == q_fold:
                score = 100
            elif q_fold and (q_fold in name_fold or name_fold in q_fold):
                score = 80
            elif soft and soft.casefold().replace(" ", "") in name_fold:
                score = 60
            else:
                score = 20
            if typ and typ.lower() in {"movie", "影视"}:
                score += 8
            if sub.isdigit():
                score += 2
            if score > best_score:
                best_score = score
                year = int(sub) if sub.isdigit() else None
                best = {
                    "source": "douban",
                    "source_id": str(row.get("id") or ""),
                    "subtitle": name if name != title else (sub or ""),
                    "cover_url": img,
                    "cover_url_fallback": str(row.get("img") or ""),
                    "score": None,
                    "episodes": None,
                    "year": year,
                    "date": str(year or ""),
                    "tags": [],
                    "format": "movie",
                }
        if best_score >= 80:
            break
    if best:
        return best
    # Douban often returns [] when rate-limited. Soft-skip after a streak so we
    # still try Anilist/IMDb, then a later slow run can clear the skip.
    if empty_streak >= 4 and "douban" not in _SOURCE_SKIP:
        _SOURCE_SKIP.add("douban")
        print("  · soft-skip douban for rest of run (empty suggest streak)", flush=True)
    if network_error:
        raise TimeoutError("douban unreachable")
    return None


# Manual CN→EN when free MT invents a wrong English title for IMDb/Douban.
MOVIE_TITLE_ALIASES: dict[str, str] = {
    "机器人总动员": "WALL-E",
    "飞屋环游记": "Up",
    "疯狂动物城": "Zootopia",
    "疯狂动物城2": "Zootopia 2",
    "疯狂原始人": "The Croods",
    "疯狂原始人2": "The Croods: A New Age",
    "秒速五厘米": "5 Centimeters per Second",
    "天气之子": "Weathering with You",
    "声之形": "A Silent Voice",
    "大鱼海棠": "Big Fish & Begonia",
    "摔跤吧！爸爸": "Dangal",
    "一个叫欧维的男人决定去死": "A Man Called Ove",
    "肖申克的救赎": "The Shawshank Redemption",
    "当幸福来敲门": "The Pursuit of Happyness",
    "怦然心动": "Flipped",
    "情书": "Love Letter",
    "波西米亚狂想曲": "Bohemian Rhapsody",
    "猫鼠游戏": "Catch Me If You Can",
    "白日梦想家": "The Secret Life of Walter Mitty",
    "绿皮书": "Green Book",
    "罗马假日": "Roman Holiday",
    "让子弹飞": "Let the Bullets Fly",
    "魂断蓝桥": "Waterloo Bridge",
    "少年派的奇幻漂流": "Life of Pi",
    "神探夏洛克：可恶的新娘": "Sherlock: The Abominable Bride",
    "哈利·波特与魔法石": "Harry Potter and the Philosopher's Stone",
    "哈利·波特与密室": "Harry Potter and the Chamber of Secrets",
    "哈利·波特与阿兹卡班的囚徒": "Harry Potter and the Prisoner of Azkaban",
    "哈利·波特与火焰杯": "Harry Potter and the Goblet of Fire",
    "哈利·波特与凤凰社": "Harry Potter and the Order of the Phoenix",
    "哈利·波特与混血王子": "Harry Potter and the Half-Blood Prince",
    "哈利·波特与死亡圣器(上)": "Harry Potter and the Deathly Hallows – Part 1",
    "哈利·波特与死亡圣器(下)": "Harry Potter and the Deathly Hallows – Part 2",
    "阿甘正传": "Forrest Gump",
    "泰坦尼克号": "Titanic",
    "楚门的世界": "The Truman Show",
    "教父": "The Godfather",
    "教父2": "The Godfather Part II",
    "教父3": "The Godfather Part III",
    "奥本海默": "Oppenheimer",
    "流浪地球": "The Wandering Earth",
    "飞驰人生": "Pegasus",
    "了不起的盖兹比": "The Great Gatsby",
    "超脱": "Detachment",
    "一直游到海水变蓝": "Swimming Out Till the Sea Turns Blue",
    "上升：我们一起飞上3万米高空": "Ascending",
    "与玛格丽特的午后": "My Afternoon with Margueritte",
    "心灵捕手": "Good Will Hunting",
    "我是谁": "Who Am I 1998",
    "星际穿越": "Interstellar",
    "海蒂和爷爷": "Heidi 2015",
    "神奇动物在哪里": "Fantastic Beasts and Where to Find Them",
    "遗愿清单": "The Bucket List",
    "钢琴家": "The Pianist",
}

# Exact en/zh Wikipedia page titles (REST summary) when free search is noisy.
MOVIE_WIKI_PAGES: dict[str, str] = {
    "肖申克的救赎": "The_Shawshank_Redemption",
    "机器人总动员": "WALL-E",
    "飞屋环游记": "Up_(2009_film)",
    "疯狂动物城": "Zootopia",
    "疯狂动物城2": "Zootopia_2",
    "疯狂原始人": "The_Croods",
    "疯狂原始人2": "The_Croods:_A_New_Age",
    "阿甘正传": "Forrest_Gump",
    "泰坦尼克号": "Titanic_(1997_film)",
    "楚门的世界": "The_Truman_Show",
    "教父": "The_Godfather",
    "教父2": "The_Godfather_Part_II",
    "教父3": "The_Godfather_Part_III",
    "奥本海默": "Oppenheimer_(film)",
    "流浪地球": "The_Wandering_Earth",
    "飞驰人生": "飞驰人生",
    "了不起的盖兹比": "The_Great_Gatsby_(2013_film)",
    "超脱": "Detachment_(film)",
    "当幸福来敲门": "The_Pursuit_of_Happyness",
    "怦然心动": "Flipped_(2010_film)",
    "摔跤吧！爸爸": "Dangal_(film)",
    "一个叫欧维的男人决定去死": "A_Man_Called_Ove_(film)",
    "猫鼠游戏": "Catch_Me_If_You_Can",
    "白日梦想家": "The_Secret_Life_of_Walter_Mitty_(2013_film)",
    "让子弹飞": "Let_the_Bullets_Fly",
    "魂断蓝桥": "Waterloo_Bridge_(1940_film)",
    "一直游到海水变蓝": "一直游到海水变蓝",
    "与玛格丽特的午后": "My_Afternoon_with_Margueritte",
    "上升：我们一起飞上3万米高空": "上升：我们一起飞上3万米高空",
    "哈利·波特与魔法石": "Harry_Potter_and_the_Philosopher's_Stone_(film)",
    "哈利·波特与密室": "Harry_Potter_and_the_Chamber_of_Secrets_(film)",
    "哈利·波特与阿兹卡班的囚徒": "Harry_Potter_and_the_Prisoner_of_Azkaban_(film)",
    "哈利·波特与火焰杯": "Harry_Potter_and_the_Goblet_of_Fire_(film)",
    "哈利·波特与凤凰社": "Harry_Potter_and_the_Order_of_the_Phoenix_(film)",
    "哈利·波特与混血王子": "Harry_Potter_and_the_Half-Blood_Prince_(film)",
    "哈利·波特与死亡圣器(上)": "Harry_Potter_and_the_Deathly_Hallows_–_Part_1",
    "哈利·波特与死亡圣器(下)": "Harry_Potter_and_the_Deathly_Hallows_–_Part_2",
    "少年派的奇幻漂流": "Life_of_Pi_(film)",
    "心灵捕手": "Good_Will_Hunting",
    "我是谁": "Who_Am_I?_(1998_film)",
    "星际穿越": "Interstellar_(film)",
    "海蒂和爷爷": "Heidi_(2015_film)",
    "神奇动物在哪里": "Fantastic_Beasts_and_Where_to_Find_Them_(film)",
    "神探夏洛克：可恶的新娘": "The_Abominable_Bride",
    "绿皮书": "Green_Book_(film)",
    "罗马假日": "Roman_Holiday",
    "遗愿清单": "The_Bucket_List",
    "钢琴家": "The_Pianist_(2002_film)",
    "波西米亚狂想曲": "Bohemian_Rhapsody_(film)",
}


def _imdb_poster_url(url: str) -> str:
    if not url:
        return ""
    # Strip size suffix so Amazon serves a larger master, then request ~600px.
    cleaned = re.sub(r"\._V1_.*?(?=\.(?:jpg|jpeg|png|webp)$)", "", url, flags=re.IGNORECASE)
    if cleaned.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        return re.sub(r"\.(jpg|jpeg|png|webp)$", r"._V1_SX600.\1", cleaned, count=1, flags=re.IGNORECASE)
    return url


def search_imdb_movie(title: str) -> dict | None:
    """IMDb v2 suggestion API — strong for EN titles; use after CN→EN translate."""
    queries: list[str] = []

    def add(q: str) -> None:
        q = (q or "").strip()
        if q and q not in queries:
            queries.append(q)

    add(MOVIE_TITLE_ALIASES.get(title, ""))
    add(title)
    soft = re.sub(r"[（(].*?[）)]", "", title).strip()
    add(soft)
    if _has_cjk(title):
        en = translate_zh_en(title)
        if en:
            add(en)

    network_error = False
    best: dict | None = None
    best_score = -1
    for q in queries[:5]:
        # Suggestion endpoint wants a lowercase first character path segment.
        first = q[0].lower()
        if not ("a" <= first <= "z" or first.isdigit()):
            # Skip pure-CJK queries — IMDb suggestion needs Latin/digit stem.
            continue
        path_q = urllib.parse.quote(q)
        url = f"https://v2.sg.media-imdb.com/suggestion/{first}/{path_q}.json"
        try:
            data = _http_json(url, timeout=10, retries=1)
        except (urllib.error.URLError, TimeoutError):
            network_error = True
            continue
        if not isinstance(data, dict):
            continue
        rows = data.get("d") or []
        if not isinstance(rows, list):
            continue
        q_fold = q.casefold().replace(" ", "")
        for row in rows:
            if not isinstance(row, dict):
                continue
            name = str(row.get("l") or "").strip()
            if not name:
                continue
            qid = str(row.get("qid") or row.get("q") or "").lower()
            img_meta = row.get("i") if isinstance(row.get("i"), dict) else {}
            img = _imdb_poster_url(str(img_meta.get("imageUrl") or ""))
            if not img:
                continue
            name_fold = name.casefold().replace(" ", "")
            score = 0
            if name_fold == q_fold:
                score = 100
            elif q_fold and (q_fold in name_fold or name_fold in q_fold):
                score = 78
            else:
                # token overlap
                qt = set(q.casefold().replace(":", " ").split())
                nt = set(name.casefold().replace(":", " ").split())
                if qt and nt and len(qt & nt) >= max(1, len(qt) - 1):
                    score = 55
                else:
                    score = 15
            if qid in {"movie", "feature"}:
                score += 12
            elif qid in {"tvseries", "tvepisode", "videogame", "name"}:
                score -= 25
            year = row.get("y")
            if isinstance(year, int):
                score += 1
            if score > best_score:
                best_score = score
                best = {
                    "source": "imdb",
                    "source_id": str(row.get("id") or ""),
                    "subtitle": name if name != title else "",
                    "cover_url": img,
                    "cover_url_fallback": str(img_meta.get("imageUrl") or ""),
                    "score": None,
                    "episodes": None,
                    "year": year if isinstance(year, int) else None,
                    "date": str(year or ""),
                    "tags": [],
                    "format": "movie",
                }
        if best_score >= 90:
            break
    if best and best_score >= 40:
        return best
    if network_error:
        raise TimeoutError("imdb unreachable")
    return None


def search_anilist_manga(title: str) -> dict | None:
    """Anilist MANGA — useful for light novels / manga-adjacent book titles."""
    payload = json.dumps(
        {"query": ANILIST_MANGA_QUERY, "variables": {"search": title}},
        ensure_ascii=False,
    ).encode("utf-8")
    try:
        data = _http_json(
            ANILIST_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            timeout=12,
            retries=1,
        )
    except (urllib.error.URLError, TimeoutError):
        raise
    if not isinstance(data, dict):
        return None
    media = (((data.get("data") or {}).get("Page") or {}).get("media")) or []
    hit = _pick_anilist(media, title)
    if not hit:
        return None
    titles = hit.get("title") or {}
    cover = (hit.get("coverImage") or {}).get("large") or (hit.get("coverImage") or {}).get("medium") or ""
    if not cover:
        return None
    genres = hit.get("genres") or []
    date = hit.get("startDate") or {}
    score = hit.get("averageScore")
    return {
        "source": "anilist_manga",
        "source_id": hit.get("id"),
        "subtitle": titles.get("native") or titles.get("romaji") or titles.get("english") or "",
        "cover_url": cover,
        "score": round(score / 10, 1) if isinstance(score, (int, float)) and score else None,
        "episodes": None,
        "year": date.get("year"),
        "date": str(date.get("year") or ""),
        "tags": genres[:5],
        "format": hit.get("format") or "",
    }


def _relative_cover(path: Path) -> str:
    rel = path.relative_to(ROOT / "static").as_posix()
    return f"/static/{rel}"


def _reclaim_local_covers(kind: str, items: list[dict], bucket: dict, img_dir: Path) -> int:
    """Wire orphaned static/img/media files back into meta by title slug."""
    reclaimed = 0
    for row in items:
        key = row["key"]
        existing = bucket.get(key) or {}
        cover_path = existing.get("cover_path") or ""
        local_file = ROOT / cover_path.lstrip("/") if cover_path.startswith("/static/") else None
        if cover_path and local_file and local_file.is_file():
            continue
        found = _find_existing_cover(img_dir, key)
        if not found:
            continue
        record = {
            "title": key,
            "series": row.get("series") or existing.get("series") or "",
            "author": row.get("author") or existing.get("author") or "",
            "category": row.get("category") or existing.get("category") or "",
            "platform": row.get("platform") or existing.get("platform") or "",
            "matched": True,
            "checked": True,
            "cover_path": _relative_cover(found),
            "subtitle": existing.get("subtitle") or "",
            "score": existing.get("score"),
            "episodes": existing.get("episodes"),
            "year": existing.get("year"),
            "date": existing.get("date") or "",
            "tags": existing.get("tags") or [],
            "source": existing.get("source") or "local",
            "source_id": existing.get("source_id") or "",
            "format": existing.get("format") or "",
        }
        bucket[key] = record
        reclaimed += 1
    return reclaimed


def process_kind(kind: str, delay: float, force: bool) -> tuple[int, int, int]:
    loaders = {"anime": load_anime, "games": load_games, "books": load_books, "movies": load_movies}
    items = loaders[kind]()
    meta = _load_meta(kind)
    bucket = meta.setdefault("items", {})
    img_dir = IMG_ROOT / kind
    img_dir.mkdir(parents=True, exist_ok=True)

    reclaimed = _reclaim_local_covers(kind, items, bucket, img_dir)
    if reclaimed:
        print(f"  · reclaimed {reclaimed} local covers into meta", flush=True)
        _save_meta(kind, meta)

    # Retry rows whose cover file vanished — wipe stale path so merge cannot resurrect it.
    cleared = 0
    for key, rec in list(bucket.items()):
        if not isinstance(rec, dict):
            continue
        cover_path = rec.get("cover_path") or ""
        local_file = ROOT / cover_path.lstrip("/") if cover_path.startswith("/static/") else None
        has_cover = bool(cover_path and local_file and local_file.is_file())
        if cover_path and not has_cover:
            rec["checked"] = False
            rec["matched"] = False
            rec["cover_path"] = ""
            cleared += 1
    if cleared:
        print(f"  · cleared {cleared} missing-file cover paths for retry", flush=True)
        _save_meta(kind, meta)

    ok = miss = skip = 0
    total = len(items)
    for idx, row in enumerate(items, 1):
        key = row["key"]
        existing = bucket.get(key) or {}
        cover_path = existing.get("cover_path") or ""
        local_file = ROOT / cover_path.lstrip("/") if cover_path.startswith("/static/") else None
        if not force and cover_path and local_file and local_file.is_file():
            skip += 1
            continue
        # Orphaned file on disk (meta wiped earlier).
        found = None if force else _find_existing_cover(img_dir, key)
        if found:
            existing = dict(existing)
            existing.update(
                {
                    "title": key,
                    "matched": True,
                    "checked": True,
                    "cover_path": _relative_cover(found),
                    "source": existing.get("source") or "local",
                }
            )
            bucket[key] = existing
            _save_meta(kind, meta)
            skip += 1
            ok += 1
            print(f"[{kind} {idx}/{total}] {key} (local)", flush=True)
            continue
        # Resume-friendly: skip titles already checked without a cover.
        if not force and existing.get("checked") and not (
            cover_path and local_file and local_file.is_file()
        ):
            skip += 1
            continue

        print(f"[{kind} {idx}/{total}] {key}", flush=True)
        hit: dict | None = None
        try:
            if kind == "anime":
                # Anilist (+ CN→EN translate variants); Kitsu fallback. Bangumi/Wiki skip.
                try:
                    hit = search_anilist_anime(key)
                except (urllib.error.URLError, TimeoutError):
                    hit = None
                if not hit or not hit.get("cover_url"):
                    hit = search_kitsu_anime(key) or hit
            elif kind == "games":
                # Steam first; iTunes software fallback when storesearch flaps.
                try:
                    hit = search_steam_game(key)
                except (urllib.error.URLError, TimeoutError):
                    hit = None
                if not hit or not hit.get("cover_url"):
                    hit = search_itunes_game(key) or hit
            elif kind == "movies":
                # Wikipedia first for live-action posters. Anilist only as soft
                # fallback (often mismatches live-action to unrelated anime).
                # Douban often times out — soft-skip after hard fail.
                # IMDb Amazon CDN TLS fails: use IMDb only for EN title hints.
                try:
                    hit = search_wikipedia_movie(key)
                except (urllib.error.URLError, TimeoutError):
                    hit = None
                if not hit or not hit.get("cover_url"):
                    try:
                        hit = search_anilist_anime(key) or hit
                    except (urllib.error.URLError, TimeoutError):
                        pass
                if (not hit or not hit.get("cover_url")) and "douban" not in _SOURCE_SKIP:
                    try:
                        hit = search_douban_movie(key) or hit
                    except (urllib.error.URLError, TimeoutError):
                        _SOURCE_SKIP.add("douban")
                        print("  · skip douban for rest of run (unreachable)", flush=True)
                if not hit or not hit.get("cover_url"):
                    imdb_hit = None
                    try:
                        imdb_hit = search_imdb_movie(key)
                    except (urllib.error.URLError, TimeoutError):
                        imdb_hit = None
                    en_name = (imdb_hit or {}).get("subtitle") or MOVIE_TITLE_ALIASES.get(key) or ""
                    if en_name:
                        try:
                            hit = search_anilist_anime(en_name) or hit
                        except (urllib.error.URLError, TimeoutError):
                            pass
                        if not hit or not hit.get("cover_url"):
                            try:
                                hit = search_wikipedia_title(
                                    en_name,
                                    kind_hint="movie",
                                    pages=[en_name, f"{en_name} (film)"],
                                ) or hit
                            except (urllib.error.URLError, TimeoutError):
                                pass
                    if (not hit or not hit.get("cover_url")) and en_name and "douban" not in _SOURCE_SKIP:
                        try:
                            hit = search_douban_movie(en_name) or hit
                        except (urllib.error.URLError, TimeoutError):
                            _SOURCE_SKIP.add("douban")
                            print("  · skip douban for rest of run (unreachable)", flush=True)
            else:
                # iTunes ebook first (reachable); Anilist MANGA / Wikipedia soft fallbacks.
                hit = search_itunes_book(key, row.get("author", ""))
                if (not hit or not hit.get("cover_url")) and "anilist_manga" not in _SOURCE_SKIP:
                    try:
                        manga_q = BOOK_TITLE_ALIASES.get(key, key)
                        hit = search_anilist_manga(manga_q) or search_anilist_manga(key) or hit
                    except (urllib.error.URLError, TimeoutError):
                        _SOURCE_SKIP.add("anilist_manga")
                        print("  · skip anilist_manga for rest of run (network)", flush=True)
                if not hit or not hit.get("cover_url"):
                    try:
                        book_pages = [BOOK_TITLE_ALIASES.get(key, ""), key]
                        hit = search_wikipedia_title(
                            key,
                            kind_hint="book",
                            pages=[p for p in book_pages if p],
                        ) or hit
                    except (urllib.error.URLError, TimeoutError):
                        pass
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"  · defer (network): {exc}", flush=True)
            # Do NOT mark checked — resume will retry later.
            time.sleep(max(delay, 0.8))
            continue

        record = {
            "title": key,
            "series": row.get("series") or "",
            "author": row.get("author") or "",
            "category": row.get("category") or "",
            "platform": row.get("platform") or "",
            "matched": False,
            "checked": True,
            "cover_path": "",
            "subtitle": "",
            "score": None,
            "episodes": None,
            "year": None,
            "date": "",
            "tags": [],
            "source": "",
            "source_id": "",
        }

        if hit:
            record.update(
                {
                    "matched": True,
                    "subtitle": hit.get("subtitle") or "",
                    "score": hit.get("score"),
                    "episodes": hit.get("episodes"),
                    "year": hit.get("year"),
                    "date": hit.get("date") or "",
                    "tags": hit.get("tags") or [],
                    "source": hit.get("source") or "",
                    "source_id": hit.get("source_id") or "",
                    "format": hit.get("format") or "",
                }
            )
            slug = _slug(key)
            dest = img_dir / f"{slug}.jpg"
            urls = [hit.get("cover_url") or ""]
            if hit.get("cover_url_fallback"):
                urls.append(hit["cover_url_fallback"])
            saved = False
            for url in urls:
                if url and _download(url, dest):
                    # dest suffix may change inside _download
                    saved_path = next(
                        (p for p in sorted(img_dir.glob(f"{slug}.*"), key=lambda p: p.stat().st_mtime, reverse=True) if p.is_file()),
                        dest,
                    )
                    record["cover_path"] = _relative_cover(saved_path)
                    saved = True
                    break
            if not saved and kind == "games" and hit.get("source_id"):
                # capsule fallback
                appid = hit["source_id"]
                for alt in (
                    f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/library_600x900_2x.jpg",
                    f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg",
                    f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/library_600x900.jpg",
                ):
                    if _download(alt, dest):
                        saved_path = next(
                            (p for p in sorted(img_dir.glob(f"{slug}.*"), key=lambda p: p.stat().st_mtime, reverse=True) if p.is_file()),
                            dest,
                        )
                        record["cover_path"] = _relative_cover(saved_path)
                        saved = True
                        break
            if saved:
                ok += 1
            else:
                miss += 1
                # Keep metadata for next try but do not mark checked — cover CDN may flap.
                record["matched"] = False
                record["checked"] = False
                record["cover_path"] = ""
                print("  · meta ok, cover missing (will retry)")
        else:
            miss += 1
            print("  · no match")

        bucket[key] = record
        # Persist every item so detached runs can resume after kill/timeout.
        _save_meta(kind, meta)
        time.sleep(delay)

    _save_meta(kind, meta)
    return ok, miss, skip


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch browse media covers into static/img/media")
    parser.add_argument("--only", choices=["anime", "games", "books", "movies", "all"], default="all")
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    parser.add_argument("--force", action="store_true", help="re-fetch even if cover exists")
    args = parser.parse_args()

    kinds = ["anime", "games", "books", "movies"] if args.only == "all" else [args.only]
    # Host-verified unreachable sources — avoid burning ~12s timeouts per title.
    # bangumi / google_books / openlibrary still burn long timeouts on this host.
    # Wikipedia is used selectively for movies/books via dedicated helpers.
    _SOURCE_SKIP.update({"bangumi", "google_books", "openlibrary"})
    print(f"ROOT={ROOT} curl={_USE_CURL} skip={sorted(_SOURCE_SKIP)}")
    for kind in kinds:
        print(f"\n=== {kind} ===")
        ok, miss, skip = process_kind(kind, delay=args.delay, force=args.force)
        print(f"done {kind}: covers={ok} miss={miss} skipped={skip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
