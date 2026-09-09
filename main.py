import asyncio
import threading
import time
import os

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler

from config import *
from database import *
from dex_scanner import *
from trend_sources import candidates
from matcher import score

# Small HTTP server so Render can run this as a free Web Service.
web = Flask(__name__)

@web.get('/')
def health():
    return {'status': 'ok', 'service': 'silent7s-meme-radar'}, 200

@web.get('/health')
def health2():
    return 'OK', 200

def start_web_server():
    port = int(os.getenv('PORT', '10000'))
    web.run(host='0.0.0.0', port=port, threaded=True, use_reloader=False)

async def start(u, c):
    if u.effective_chat.id == CHAT_ID:
        await u.message.reply_text('🟢 Silent7s Meme Radar online\nSolana scanner: active')

async def status(u, c):
    if u.effective_chat.id == CHAT_ID:
        await u.message.reply_text(
            f'🟢 Online\nSolana only\nPoll: {POLL_SECONDS}s\n'
            f'Max age: {MAX_TOKEN_AGE_MINUTES}m\nMin score: {MIN_SCORE}'
        )

async def scan(app):
    trends = candidates(TREND_FEEDS)
    try:
        ps = latest_solana_profiles()
    except Exception as e:
        print(e)
        return
    now = int(time.time())
    for p in ps[:100]:
        a = p.get('tokenAddress')
        if not a or seen(a):
            continue
        try:
            t = normalize(p)
        except Exception as e:
            print(e)
            continue
        mark_seen(a, now)
        if (
            t['age'] is None
            or t['age'] > MAX_TOKEN_AGE_MINUTES
            or t['liquidity'] < MIN_LIQUIDITY_USD
            or t['volume5m'] < MIN_VOLUME_5M_USD
        ):
            continue
        total, relation, trend = score(t, trends)
        if total < MIN_SCORE or alerted(a):
            continue
        msg = (
            f"🚨 <b>EARLY SOLANA MEMECOIN</b>\n\n"
            f"🪙 <b>{t['name']} (${t['symbol']})</b>\n"
            f"⏱ Age: {t['age']:.1f} min\n"
            f"📊 Score: <b>{total}/100</b>\n"
            f"🔤 Name/Trend match: {relation}%\n"
            f"💧 Liquidity: ${t['liquidity']:,.0f}\n"
            f"📈 5m volume: ${t['volume5m']:,.0f}\n"
            f"🟢 Buys: {t['buys5m']} / 🔴 Sells: {t['sells5m']}\n"
            f"🔥 Candidate: {(trend or {}).get('title','')}\n"
            f"🔗 {t['url'] or ''}\n\n"
            f"⚠️ Very high risk. Screening signal only."
        )
        try:
            await app.bot.send_message(CHAT_ID, msg, parse_mode='HTML')
            mark_alert(a, now)
        except Exception as e:
            print(e)

async def loop(app):
    while True:
        try:
            await scan(app)
        except Exception as e:
            print('scan error:', e)
        await asyncio.sleep(POLL_SECONDS)

async def scan_cmd(u, c):
    if u.effective_chat.id == CHAT_ID:
        await u.message.reply_text('🔎 Scanning...')
        await scan(c.application)
        await u.message.reply_text('✅ Done.')

async def post_init(app):
    asyncio.create_task(loop(app))

def main():
    if not TELEGRAM_TOKEN:
        raise SystemExit('Set TELEGRAM_TOKEN in Render Environment Variables')
    init_db()

    # Render Web Service health endpoint.
    threading.Thread(target=start_web_server, daemon=True).start()

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('status', status))
    app.add_handler(CommandHandler('scan', scan_cmd))
    app.run_polling()

if __name__ == '__main__':
    main()
