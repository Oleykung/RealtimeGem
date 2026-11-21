
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import os, json, datetime, pytz, asyncio
from pathlib import Path
import time as _time

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID") or 0)
TIMEZONE = os.getenv("TIMEZONE") or "Asia/Bangkok"
BASE = Path(__file__).parent
BOSSES_FILE = BASE / "bosses.json"
TIMERS_FILE = BASE / "timers.json"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents, chunk_guilds_at_startup=False, heartbeat_timeout=60.0, max_messages=None)
tz = pytz.timezone(TIMEZONE)

try:
    with open(BOSSES_FILE, encoding="utf-8") as f:
        BOSSES = json.load(f)
except:
    BOSSES = [{"id": "dilos_latem", "name_th": "ดิลอส ลาเท็ม", "name_en": "Dilos Latem", "city": "Reboldoeux", "map": "Al Quelt Moreza (Dungeon) ชั้น 7-17 / ห้องบอสลับ", "type": "Dungeon Boss", "respawn_min": 120, "fixed_times": []}, {"id": "hill_giant", "name_th": "ฮิลล์ ไจแอนท์", "name_en": "Hill Giant", "city": "Reboldoeux", "map": "Rion Prairie / Ferruccio Junction / จุดวาร์ปกลางทุ่ง", "type": "Field Boss", "respawn_min": 120, "fixed_times": []}, {"id": "nest_head_giant", "name_th": "เนสท์-เฮด ไจแอนท์", "name_en": "Nest-Head Giant", "city": "Reboldoeux", "map": "Rion Prairie เหนือ / Forest of Chery / ริมผา", "type": "Field Boss Lv.30", "respawn_min": 180, "fixed_times": []}, {"id": "queen_goblin", "name_th": "ควีน ก็อบลิน", "name_en": "Queen Goblin", "city": "Reboldoeux", "map": "Al Quelt Moreza ทางออก / ชายป่า Reboldoeux", "type": "Field Boss Lv.25", "respawn_min": 90, "fixed_times": []}, {"id": "pappus_alpha", "name_th": "ปาปัส อัลฟ่า", "name_en": "Pappus Alpha", "city": "Reboldoeux", "map": "Ferruccio Underground / Ferruccio Factory", "type": "Field Boss Lv.35", "respawn_min": 150, "fixed_times": []}, {"id": "treasure_golem", "name_th": "เทรเชอร์ โกเล็ม", "name_en": "Treasure Golem", "city": "The Port of Coimbra", "map": "Tetra Ruins / Secret Tetra ชั้น 24-34 / ห้องสมบัติ", "type": "Dungeon Boss", "respawn_min": 180, "fixed_times": []}, {"id": "kraken", "name_th": "คราเคน ยักษ์", "name_en": "Kraken", "city": "The Port of Coimbra", "map": "Tetra Coast / ชายฝั่ง Coimbra / ท่าเรือร้าง", "type": "Field Boss Lv.45", "respawn_min": 180, "fixed_times": []}, {"id": "tetra_commander", "name_th": "เตตร้า คอมมานเดอร์", "name_en": "Tetra Commander", "city": "The Port of Coimbra", "map": "Tetra Ruins Entrance / ทางเข้า Tetra", "type": "Field Boss Lv.40", "respawn_min": 150, "fixed_times": []}, {"id": "naga_queen", "name_th": "นากา ควีน", "name_en": "Naga Queen", "city": "The Port of Coimbra", "map": "Tetra Underground Lake / บ่อน้ำใต้ดิน Tetra", "type": "Field Boss Lv.42", "respawn_min": 120, "fixed_times": []}, {"id": "giant_crab", "name_th": "ไจแอนท์ แครบ", "name_en": "Giant Crab", "city": "The Port of Coimbra", "map": "Coimbra Beach / ชายหาด Coimbra", "type": "Field Boss Lv.38", "respawn_min": 90, "fixed_times": []}, {"id": "chimera", "name_th": "ไคเมร่า", "name_en": "Chimera", "city": "City of Auch", "map": "Chaos Chimera Dungeon / ดันเจี้ยนไคเมร่า", "type": "Dungeon Boss", "respawn_min": 240, "fixed_times": []}, {"id": "dr_torsche", "name_th": "ดร.ทอร์เช่", "name_en": "Dr. Torsche", "city": "City of Auch", "map": "Dr. Torsche's Mansion / Savage Garden / คฤหาสน์ทอร์เช่", "type": "Dungeon Boss", "respawn_min": 240, "fixed_times": []}, {"id": "big_cockatrice", "name_th": "บิ๊ก ค็อกคาไทรซ์", "name_en": "Big Cockatrice", "city": "City of Auch", "map": "El Lago de Tres Hermanas / El Tejado Verde / ริมทะเลสาบ", "type": "Field Boss Lv.69", "respawn_min": 180, "fixed_times": []}, {"id": "captain_scharf", "name_th": "กัปตัน ชาร์ฟเฟนเบอร์เกอร์", "name_en": "Captain Scharffenberger", "city": "City of Auch", "map": "El Tejado Verde / จุดชมวิว Auch / ยอดเขา", "type": "Field Boss Lv.69", "respawn_min": 180, "fixed_times": []}, {"id": "merman_chief", "name_th": "เมอร์แมน ชีฟเทน", "name_en": "Merman Chieftain", "city": "City of Auch", "map": "Thueringen Lakeside / El Lago ฝั่งตะวันตก", "type": "Field Boss Lv.63", "respawn_min": 120, "fixed_times": []}, {"id": "stone_cortes", "name_th": "สโตน คอร์เทส", "name_en": "Stone Cortes", "city": "City of Auch", "map": "Clock Tower 2nd Floor / หอนาฬิกาชั้น 2 (แมพใหม่ Byron)", "type": "Field Boss Lv.75", "respawn_min": 240, "fixed_times": []}, {"id": "pirate_king_el_lago", "name_th": "ไพเรทคิง แห่งเอล ลาโก", "name_en": "Pirate King of El Lago", "city": "City of Auch", "map": "El Lago de Tres Hermanas กลางทะเลสาบ / เกาะโจรสลัด", "type": "Field Boss Lv.65", "respawn_min": 180, "fixed_times": []}, {"id": "chaos_cub", "name_th": "เคออส คับ", "name_en": "Chaos Cub", "city": "City of Auch", "map": "El Tejado Verde Depths / ถ้ำลึก Auch / ป่า Chaos", "type": "Field Boss Lv.70", "respawn_min": 210, "fixed_times": []}, {"id": "witch_bondage", "name_th": "วิทช์ ออฟ บอนเดจ", "name_en": "Witch of Bondage", "city": "World Boss - ทุกเมือง", "map": "World Boss Arena / ลานบอสโลก (วาร์ปจากทุกเมือง)", "type": "World Boss", "respawn_min": 0, "fixed_times": ["12:00", "19:30", "22:00"]}]

TIMERS_CACHE = {}
LAST_LOAD = 0
ALERT_CHANNEL_CACHE = None
WS_CLIENTS = set()  # realtime websocket clients

def load_timers():
    global TIMERS_CACHE, LAST_LOAD
    now = _time.time()
    if TIMERS_CACHE and (now - LAST_LOAD < 10):
        return TIMERS_CACHE.copy()
    if not TIMERS_FILE.exists():
        return {}
    try:
        with open(TIMERS_FILE, encoding="utf-8") as f:
            TIMERS_CACHE = json.load(f)
            LAST_LOAD = now
            return TIMERS_CACHE.copy()
    except:
        return TIMERS_CACHE.copy() if TIMERS_CACHE else {}

def save_timers(data):
    global TIMERS_CACHE, LAST_LOAD
    TIMERS_CACHE = data.copy()
    LAST_LOAD = _time.time()
    with open(TIMERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Realtime broadcast
    if WS_CLIENTS:
        asyncio.create_task(broadcast_ws({"type":"timers","data":data}))

def load_bosses_file():
    try:
        with open(BOSSES_FILE, encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_bosses_file(bosses):
    global BOSSES
    with open(BOSSES_FILE, "w", encoding="utf-8") as f:
        json.dump(bosses, f, ensure_ascii=False, indent=2)
    BOSSES = bosses
    if WS_CLIENTS:
        asyncio.create_task(broadcast_ws({"type":"bosses","data":bosses}))

def find_boss(q):
    if not q: return None
    q = q.lower()
    for b in BOSSES:
        if q in b["id"] or q in b["name_th"].lower() or q in b["name_en"].lower():
            return b
    return None

def now_th(): return datetime.datetime.now(tz)

# ===== REALTIME WEBSOCKET BROADCAST =====
async def broadcast_ws(message):
    if not WS_CLIENTS:
        return
    dead = set()
    for ws in WS_CLIENTS:
        try:
            await ws.send_json(message)
        except:
            dead.add(ws)
    WS_CLIENTS.difference_update(dead)

# ===== AUTOCOMPLETE FOR DYNAMIC BOSS LIST (Realtime) =====
async def autocomplete_boss(interaction: discord.Interaction, current: str):
    current = current.lower()
    choices = []
    for b in BOSSES:
        name = f"{b['name_th']} ({b['name_en']}) | {b['city']}"
        if current in b['name_th'].lower() or current in b['name_en'].lower() or current in b['id'].lower() or current in b['city'].lower() or not current:
            choices.append(app_commands.Choice(name=name[:100], value=b['id']))
        if len(choices) >= 25:
            break
    return choices

async def autocomplete_boss_reset(interaction: discord.Interaction, current: str):
    current = current.lower()
    choices = []
    if not current or "all" in current or "ทั้งหมด" in current or "reset" in current:
        choices.append(app_commands.Choice(name="♻️ รีเซ็ตบอสทั้งหมด (Reset All)", value="all"))
    for b in BOSSES:
        name = f"{b['name_th']} ({b['name_en']}) | {b['city']}"
        if current in b['name_th'].lower() or current in b['name_en'].lower() or current in b['id'].lower() or not current:
            choices.append(app_commands.Choice(name=name[:100], value=b['id']))
        if len(choices) >= 24:
            break
    return choices

@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์: {bot.user} | {TIMEZONE} | บอส {len(BOSSES)} ตัว | Realtime ON")
    check_boss_spawn.start()
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Sync {len(synced)} คำสั่ง (Autocomplete Realtime)")
    except Exception as e:
        print(f"Sync error {e}")

@bot.tree.error
async def on_app_command_error(interaction, error):
    print(f"Slash error: {error}")
    try:
        msg = f"❌ {str(error)[:300]}"
        if not interaction.response.is_done():
            await interaction.response.send_message(msg, ephemeral=True)
        else:
            await interaction.followup.send(msg, ephemeral=True)
    except: pass

@tasks.loop(seconds=30)
async def check_boss_spawn():
    global ALERT_CHANNEL_CACHE
    if ALERT_CHANNEL_ID == 0: return
    if ALERT_CHANNEL_CACHE is None:
        channel = bot.get_channel(ALERT_CHANNEL_ID)
        if not channel:
            try: channel = await bot.fetch_channel(ALERT_CHANNEL_ID)
            except: return
        ALERT_CHANNEL_CACHE = channel
    else:
        channel = ALERT_CHANNEL_CACHE
    timers = load_timers()
    now = now_th()
    for boss in BOSSES:
        bid = boss["id"]
        if boss.get("fixed_times"):
            for t_str in boss["fixed_times"]:
                if not t_str: continue
                h,m = map(int, t_str.split(":"))
                st = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if st < now: continue
                diff = (st - now).total_seconds()/60
                if 9.5 <= diff <= 10.5:
                    key = f"{bid}_{t_str}_{st.date()}_notified"
                    if timers.get(key): continue
                    embed = discord.Embed(title="⏰ บอสจะเกิดใน 10 นาที!", description=f"**{boss['name_th']} / {boss['name_en']}**\nเมือง: {boss['city']}\nแผนที่: {boss['map']}\nเวลา: {t_str} น.", color=0xFF0000)
                    try:
                        await channel.send(content="@everyone", embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
                        timers[key]=True
                        save_timers(timers)
                    except Exception as e: print(e)
                if -0.5 <= diff <= 0.5:
                    key2 = f"{bid}_{t_str}_{st.date()}_spawned"
                    if timers.get(key2): continue
                    embed = discord.Embed(title="🔥 บอสเกิดแล้ว!", description=f"**{boss['name_th']} / {boss['name_en']}** ที่ {boss['map']}", color=0x00FF00)
                    try:
                        await channel.send(content="@everyone บอสเกิดแล้ว!", embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
                        timers[key2]=True
                        save_timers(timers)
                    except Exception as e: print(e)
        else:
            if bid not in timers: continue
            data = timers[bid]
            if "next_spawn" not in data: continue
            try:
                ns = datetime.datetime.fromisoformat(data["next_spawn"])
                if ns.tzinfo is None: ns = tz.localize(ns)
            except: continue
            diff = (ns - now).total_seconds()/60
            if 9.5 <= diff <= 10.5 and not data.get("notified_10m"):
                embed = discord.Embed(title="⏰ บอสใกล้เกิด 10 นาที!", description=f"**{boss['name_th']} / {boss['name_en']}**\nเมือง: {boss['city']}\nแผนที่: {boss['map']}", color=0xFFAA00)
                try:
                    await channel.send(content="@everyone เตรียมตัว!", embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
                    data["notified_10m"]=True
                    timers[bid]=data
                    save_timers(timers)
                except Exception as e: print(e)
            if -0.5 <= diff <= 0.5 and not data.get("notified_spawn"):
                embed = discord.Embed(title="🔥 บอสเกิดแล้ว!", description=f"**{boss['name_th']} / {boss['name_en']}** ที่ {boss['map']} แล้ว!", color=0x00FF00)
                try:
                    await channel.send(content="@everyone", embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
                    data["notified_spawn"]=True
                    timers[bid]=data
                    save_timers(timers)
                except Exception as e: print(e)

@check_boss_spawn.before_loop
async def before_boss_check():
    await bot.wait_until_ready()
    print("⏰ Boss check loop ready (Realtime)")

# ===== SLASH COMMANDS REALTIME AUTOCOMPLETE =====
@bot.tree.command(name="boss", description="ดูรายชื่อบอสทั้งหมด + เวลาเกิดถัดไป")
async def slash_boss(interaction: discord.Interaction):
    await interaction.response.defer()
    timers = load_timers()
    now = now_th()
    embed = discord.Embed(title="📜 Boss Tracker - Granado Espada M TH (Realtime)", description="Reboldoeux / Coimbra / Auch | @everyone ก่อน 10 นาที | Sync Realtime", color=0x0099FF)
    for city in ["Reboldoeux", "The Port of Coimbra", "City of Auch"]:
        blist = [b for b in BOSSES if city in b["city"]]
        if not blist: continue
        txt = "\n".join([f"• {b['name_th']} ({b['name_en']}) - {b['map']}" for b in blist[:6]])
        embed.add_field(name=f"🏰 {city}", value=txt, inline=False)
    upcoming=[]
    for boss in BOSSES:
        if boss.get("fixed_times"):
            for t in boss["fixed_times"]:
                if not t: continue
                h,m = map(int,t.split(":"))
                st = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if st>now: upcoming.append((st,boss))
        else:
            if boss["id"] in timers and "next_spawn" in timers[boss["id"]]:
                try:
                    ns = datetime.datetime.fromisoformat(timers[boss["id"]]["next_spawn"])
                    if ns.tzinfo is None: ns = tz.localize(ns)
                    if ns>now: upcoming.append((ns,boss))
                except: pass
    upcoming.sort(key=lambda x:x[0])
    if upcoming:
        txt = "\n".join([f"**{b['name_th']}** {dt.strftime('%H:%M')} น. - {b['map']}" for dt,b in upcoming[:5]])
        embed.add_field(name="⏳ จะเกิดถัดไป", value=txt, inline=False)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="bosslist", description="ดูรายชื่อบอสทั้งหมดแยกตามเมือง")
async def slash_bosslist(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="📜 รายชื่อบอส Granado Espada M TH (Realtime)", color=0x0099FF)
    for city in ["Reboldoeux", "The Port of Coimbra", "City of Auch", "World Boss - ทุกเมือง"]:
        blist = [b for b in BOSSES if city in b["city"]]
        if not blist: continue
        txt = "\n".join([f"• {b['name_th']} ({b['name_en']}) - {b['map']}" for b in blist])
        if len(txt)>1024: txt=txt[:1000]+"..."
        embed.add_field(name=city, value=txt, inline=False)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="bossnext", description="ดูบอส 5 ตัวที่จะเกิดถัดไป")
async def slash_bossnext(interaction: discord.Interaction):
    await interaction.response.defer()
    timers = load_timers()
    now = now_th()
    upcoming=[]
    for boss in BOSSES:
        if boss.get("fixed_times"):
            for t in boss.get("fixed_times",[]):
                if not t: continue
                h,m = map(int,t.split(":"))
                st = now.replace(hour=h, minute=m, second=0, microsecond=0)
                if st>now: upcoming.append((st,boss))
        else:
            if boss["id"] in timers and "next_spawn" in timers[boss["id"]]:
                try:
                    ns = datetime.datetime.fromisoformat(timers[boss["id"]]["next_spawn"])
                    if ns.tzinfo is None: ns = tz.localize(ns)
                    if ns>now: upcoming.append((ns,boss))
                except: pass
    upcoming.sort(key=lambda x:x[0])
    if not upcoming:
        await interaction.followup.send("ยังไม่มีตั้งเวลาบอส ใช้ `/bosskill` เลือกจากรายชื่อเพื่อเริ่มนับ")
        return
    embed = discord.Embed(title="⏳ บอสที่จะเกิดถัดไป 5 ตัว (Realtime)", color=0xFFD700)
    for dt,b in upcoming[:5]:
        embed.add_field(name=f"{b['name_th']} ({b['name_en']})", value=f"{b['map']} | {dt.strftime('%H:%M:%S')} น. | {b['city']}", inline=False)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="bosskill", description="แจ้งว่าบอสตายแล้ว - พิมพ์ชื่อบอสได้ (Realtime)")
@app_commands.autocomplete(boss_name=autocomplete_boss)
async def slash_bosskill(interaction: discord.Interaction, boss_name: str):
    await interaction.response.defer()
    boss = find_boss(boss_name)
    if not boss:
        await interaction.followup.send(f"❌ ไม่เจอบอส `{boss_name}` ลองพิมพ์ชื่อไทยหรืออังกฤษ", ephemeral=True)
        return
    if boss.get("fixed_times"):
        await interaction.followup.send(f"ℹ️ **{boss['name_th']}** เป็นบอสเวลาตายตัว {boss['fixed_times']} น. ไม่ต้องแจ้งตาย", ephemeral=True)
        return
    now = now_th()
    next_spawn = now + datetime.timedelta(minutes=boss["respawn_min"])
    timers = load_timers()
    timers[boss["id"]] = {"last_killed": now.isoformat(), "next_spawn": next_spawn.isoformat(), "killed_by": str(interaction.user), "notified_10m": False, "notified_spawn": False}
    save_timers(timers)
    embed = discord.Embed(title="💀 บันทึกบอสตายแล้ว (Realtime Sync)", description=f"**{boss['name_th']} / {boss['name_en']}**\nตายเมื่อ: {now.strftime('%H:%M:%S')} น.\nจะเกิดใหม่: {next_spawn.strftime('%H:%M:%S')} น. (อีก {boss['respawn_min']} นาที)\nแผนที่: {boss['map']}\n\n✅ ส่งไปเว็บแล้ว", color=0x555555)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="bosstime", description="ดูเวลาเกิดของบอส - พิมพ์ชื่อบอสได้ (Realtime)")
@app_commands.autocomplete(boss_name=autocomplete_boss)
async def slash_bosstime(interaction: discord.Interaction, boss_name: str):
    await interaction.response.defer()
    boss = find_boss(boss_name)
    if not boss:
        await interaction.followup.send("❌ ไม่เจอบอส", ephemeral=True)
        return
    timers = load_timers()
    if boss.get("fixed_times"):
        await interaction.followup.send(f"⏰ **{boss['name_th']} / {boss['name_en']}** เกิดเวลาตายตัว: {', '.join(boss['fixed_times'])} น. ที่ {boss['map']}")
    elif boss["id"] in timers:
        ns = timers[boss["id"]].get("next_spawn","ไม่ทราบ")
        try:
            dt = datetime.datetime.fromisoformat(ns)
            await interaction.followup.send(f"⏰ **{boss['name_th']}** จะเกิดที่ {dt.strftime('%H:%M:%S')} น. ที่ {boss['map']} (Realtime)")
        except:
            await interaction.followup.send(f"⏰ **{boss['name_th']}** จะเกิดที่ {ns}")
    else:
        await interaction.followup.send(f"ยังไม่มีเวลาเกิดของ {boss['name_th']} ใช้ /bosskill เลือกบอสเพื่อเริ่มนับ")

@bot.tree.command(name="reset", description="♻️ รีเซ็ตเวลาบอส รายตัว - พิมพ์ชื่อบอสได้ (Realtime)")
@app_commands.autocomplete(boss_name=autocomplete_boss_reset)
async def slash_reset(interaction: discord.Interaction, boss_name: str):
    await interaction.response.defer()
    timers = load_timers()
    if boss_name == "all":
        timers.clear()
        save_timers(timers)
        embed = discord.Embed(title="♻️ รีเซ็ตบอสทั้งหมดแล้ว (Realtime)", description="ล้างเวลาเกิดบอสทั้งหมดเรียบร้อย\n✅ ส่งไปเว็บแล้ว\nใช้ `/bosskill` เพื่อเริ่มนับใหม่", color=0x00FFAA)
        await interaction.followup.send(embed=embed)
        return
    boss = find_boss(boss_name)
    if not boss:
        await interaction.followup.send(f"❌ ไม่เจอบอส `{boss_name}`", ephemeral=True)
        return
    timers.pop(boss["id"], None)
    for k in list(timers.keys()):
        if boss["id"] in k:
            timers.pop(k, None)
    save_timers(timers)
    embed = discord.Embed(title="♻️ รีเซ็ตบอสแล้ว (Realtime)", description=f"**{boss['name_th']} / {boss['name_en']}**\nเมือง: {boss['city']}\nแผนที่: {boss['map']}\n\n✅ ล้างเวลาเกิดเรียบร้อย + ส่งไปเว็บแล้ว", color=0xFFAA00)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="bossreset", description="♻️ รีเซ็ตเวลาบอส รายตัว - ชื่อสำรองของ /reset (Realtime)")
@app_commands.autocomplete(boss_name=autocomplete_boss_reset)
async def slash_bossreset(interaction: discord.Interaction, boss_name: str):
    await slash_reset.callback(interaction, boss_name)

@bot.tree.command(name="setalert", description="ตั้งห้องแจ้งเตือนบอส (Admin)")
async def slash_setalert(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(ephemeral=True)
    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("ต้องเป็น Admin เท่านั้น", ephemeral=True)
        return
    global ALERT_CHANNEL_ID, ALERT_CHANNEL_CACHE
    ALERT_CHANNEL_ID = channel.id
    ALERT_CHANNEL_CACHE = channel
    env_path = BASE / ".env"
    lines = []
    if env_path.exists():
        with open(env_path, encoding="utf-8") as f:
            lines = f.readlines()
    new_lines=[]
    found=False
    for line in lines:
        if line.startswith("ALERT_CHANNEL_ID="):
            new_lines.append(f"ALERT_CHANNEL_ID={channel.id}\n")
            found=True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"ALERT_CHANNEL_ID={channel.id}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    await interaction.followup.send(f"✅ ตั้งห้องแจ้งเตือนเป็น {channel.mention} แล้ว จะแท็ก @everyone ก่อนบอสเกิด 10 นาที", ephemeral=True)

# ===== WEB + REALTIME WEBSOCKET =====
try:
    from aiohttp import web
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False
    print("⚠️ aiohttp ไม่ได้ติดตั้ง - pip install aiohttp")

async def api_get_bosses(request): return web.json_response(load_bosses_file())
async def api_get_timers(request): return web.json_response(load_timers())
async def api_post_timers(request):
    try:
        data = await request.json()
        save_timers(data)
        return web.json_response({"ok": True, "count": len(data)})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

async def api_add_boss(request):
    try:
        data = await request.json()
        bosses = load_bosses_file()
        if any(b["id"]==data["id"] for b in bosses):
            return web.json_response({"error":"id exists"}, status=400)
        bosses.append(data)
        save_bosses_file(bosses)
        return web.json_response({"ok":True, "boss":data})
    except Exception as e:
        return web.json_response({"error":str(e)}, status=500)

async def api_update_boss(request):
    try:
        bid = request.match_info.get("id")
        data = await request.json()
        bosses = load_bosses_file()
        for i,b in enumerate(bosses):
            if b["id"]==bid:
                data["id"]=bid
                bosses[i]=data
                save_bosses_file(bosses)
                return web.json_response({"ok":True, "boss":data})
        return web.json_response({"error":"not found"}, status=404)
    except Exception as e:
        return web.json_response({"error":str(e)}, status=500)

async def api_delete_boss(request):
    try:
        bid = request.match_info.get("id")
        bosses = load_bosses_file()
        new_list = [b for b in bosses if b["id"]!=bid]
        if len(new_list)==len(bosses):
            return web.json_response({"error":"not found"}, status=404)
        save_bosses_file(new_list)
        timers = load_timers()
        timers.pop(bid, None)
        for k in list(timers.keys()):
            if bid in k:
                timers.pop(k, None)
        save_timers(timers)
        return web.json_response({"ok":True})
    except Exception as e:
        return web.json_response({"error":str(e)}, status=500)

async def api_kill(request):
    try:
        data = await request.json()
        bid = data.get("id")
        boss = find_boss(bid)
        if not boss: return web.json_response({"error":"boss not found"}, status=404)
        if boss.get("fixed_times"): return web.json_response({"error":"fixed time boss"}, status=400)
        now = now_th()
        next_spawn = now + datetime.timedelta(minutes=boss["respawn_min"])
        timers = load_timers()
        timers[boss["id"]] = {"last_killed": now.isoformat(), "next_spawn": next_spawn.isoformat(), "killed_by": "web", "notified_10m": False, "notified_spawn": False}
        save_timers(timers)
        return web.json_response({"ok":True, "next_spawn": next_spawn.isoformat()})
    except Exception as e:
        return web.json_response({"error":str(e)}, status=500)

async def api_reset(request):
    try:
        data = await request.json()
        bid = data.get("id")
        timers = load_timers()
        if bid == "all": timers.clear()
        else:
            timers.pop(bid, None)
            for k in list(timers.keys()):
                if bid in k:
                    timers.pop(k, None)
        save_timers(timers)
        return web.json_response({"ok":True})
    except Exception as e:
        return web.json_response({"error":str(e)}, status=500)

async def api_settime(request):
    try:
        data = await request.json()
        bid = data.get("id")
        next_spawn_str = data.get("next_spawn")
        boss = find_boss(bid)
        if not boss: return web.json_response({"error":"boss not found"}, status=404)
        try:
            ns = datetime.datetime.fromisoformat(next_spawn_str)
            if ns.tzinfo is None: ns = tz.localize(ns)
        except:
            return web.json_response({"error":"invalid time"}, status=400)
        timers = load_timers()
        timers[bid] = {"last_killed": now_th().isoformat(), "next_spawn": ns.isoformat(), "killed_by": data.get("by","web-settime"), "notified_10m": False, "notified_spawn": False}
        save_timers(timers)
        return web.json_response({"ok":True, "next_spawn": ns.isoformat()})
    except Exception as e:
        return web.json_response({"error":str(e)}, status=500)

async def api_status(request):
    return web.json_response({"bot": str(bot.user) if bot.user else "starting", "guilds": len(bot.guilds) if hasattr(bot,'guilds') else 0, "timers": len(load_timers()), "bosses": len(load_bosses_file()), "timezone": TIMEZONE, "ws_clients": len(WS_CLIENTS), "realtime": True})

async def handle_index(request):
    try:
        with open(BASE / "index.html", encoding="utf-8") as f:
            return web.Response(text=f.read(), content_type="text/html")
    except:
        return web.Response(text="<h1>Boss Tracker Realtime</h1>", content_type="text/html")

async def handle_ws(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    WS_CLIENTS.add(ws)
    print(f"🔗 Web client connected - total {len(WS_CLIENTS)}")
    try:
        await ws.send_json({"type":"init", "bosses": load_bosses_file(), "timers": load_timers()})
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    if data.get("type") == "ping":
                        await ws.send_json({"type":"pong"})
                except:
                    pass
    except Exception as e:
        print(f"WS error {e}")
    finally:
        WS_CLIENTS.discard(ws)
        print(f"🔌 Web client disconnected - total {len(WS_CLIENTS)}")
    return ws

def create_web_app():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_get('/ws', handle_ws)
    app.router.add_get('/api/bosses', api_get_bosses)
    app.router.add_post('/api/bosses', api_add_boss)
    app.router.add_put('/api/bosses/{id}', api_update_boss)
    app.router.add_delete('/api/bosses/{id}', api_delete_boss)
    app.router.add_get('/api/timers', api_get_timers)
    app.router.add_post('/api/timers', api_post_timers)
    app.router.add_post('/api/kill', api_kill)
    app.router.add_post('/api/reset', api_reset)
    app.router.add_post('/api/settime', api_settime)
    app.router.add_get('/api/status', api_status)
    return app

async def start_web_server():
    if not WEB_AVAILABLE: return
    app = create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print(f"🌐 Web Dashboard + Realtime WS รันแล้วที่ http://localhost:8080")
    print(f"🔴 Realtime WebSocket: ws://localhost:8080/ws")

@bot.event
async def setup_hook():
    if WEB_AVAILABLE:
        bot.loop.create_task(start_web_server())

if not TOKEN:
    print("❌ ไม่พบ DISCORD_TOKEN ในไฟล์ .env")
    exit(1)

bot.run(TOKEN)