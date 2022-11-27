import hikari

from torrent_scrap import ScrapSearch, ScrapDownload

bot = hikari.GatewayBot(
    token='...', 
    intents=hikari.Intents.ALL,
)

@bot.listen(hikari.GuildMessageCreateEvent)
async def search(event):

    links = []

    if event.is_bot or not event.content:
        pass

    if event.content.startswith("p."):
        search = event.content.split('.')[1]
        results = ScrapSearch(search)
        for result in results():
            links.append(result[6])
        for result in results():
            await event.message.respond(layout(result))

def layout(event):
    return f'ID: {event[0]}, Nome: {event[1]}, Tipo: {event[2]}, Espaço: {event[3]}, Seeds: {event[4]}, Release: {event[5]}, Link: {ScrapDownload(event[6])}'

bot.run()