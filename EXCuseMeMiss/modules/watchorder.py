import requests
from bs4 import BeautifulSoup
from pyrogram import filters

from ShasaBot import BOT_USERNAME, pbot


@pbot.on_message(filters.command("watchorder", f"watchorder@{BOT_USERNAME}"))
def watchorderx(_, message):

    anime = message.text.replace(message.text.split(" ")[0], "")

    res = requests.get(
        f"https://chiaki.site/?/tools/autocomplete_series&term={anime}"
    ).json()

    data = None

    id_ = res[0]["id"]

    res_ = requests.get(f"https://chiaki.site/?/tools/watch_order/id/{id_}").text

    soup = BeautifulSoup(res_, "html.parser")

    anime_names = soup.find_all("span", class_="wo_title")

    for x in anime_names:

        data = f"{data}\n{x.text}" if data else x.text
    message.reply_text(f"Watchorder of {anime}: \n```{data}```")
