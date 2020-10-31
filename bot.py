from os import getenv
from discord.ext import commands

settings = {
    'token': getenv("BOT_TOKEN"),
    'bot': 'IS_queue_bot',
    'id': int(getenv("BOT_ID")),
    'prefix': '/'
}

bot = commands.Bot(command_prefix=settings['prefix'])

admins = [
    "danila_charushin"
]

queue = []
working = True
current = None


@bot.command()
async def run(ctx):
    global working
    if not working:
        working = True
        await ctx.send("Пошла жара")
    else:
        await ctx.send("Бот уже запущен")


@bot.command()
async def stop(ctx):
    global working
    if working:
        working = False
        await ctx.send("Покеда")
    else:
        await ctx.send("Бот спит, не буди")


@bot.command()
async def show(ctx):
    if working:
        if len(queue) == 0:
            await ctx.send("Очередь пуста, будь первым и всё такое")
        else:
            msg = "Текущая очередь:\n"
            for i, person in enumerate(queue):
                msg += "{}. {}\n".format(i + 1, str(person.nick))
            await ctx.send(msg)


@bot.command()
async def clear(ctx):
    if working:
        if ctx.message.author.name in admins or ctx.message.author.nick in admins:
            queue.clear()
            await ctx.send(f'Очередь очищена')
        else:
            await ctx.send(f'Ты не можешь очистить очередь :)')


@bot.command()
async def take(ctx):
    global current
    if working:
        if ctx.message.author.name in admins or ctx.message.author.nick in admins:
            current = queue.pop(0)
            await ctx.send(f'Вы достали {current.nick} на защиту')
        else:
            await ctx.send(f'Не имеешь права :(')


@bot.command()
async def flush(ctx):
    global current
    if working:
        if ctx.message.author.name in admins or ctx.message.author.nick in admins:
            if current:
                msg = f'Вы сняли {current.nick} с защиты'
                current = None
                await ctx.send(msg)
            else:
                await ctx.send("На защите ещё никого нет")
        else:
            await ctx.send(f'Не имеешь права :(')


@bot.command()
async def get(ctx):
    if working:
        if current:
            await ctx.send("Сейчас на защите: {}".format(current.nick))
        else:
            await ctx.send("Никто не защищается")


@bot.command()
async def pop(ctx):
    global queue
    if working:
        queue = list(filter(lambda p: p != ctx.message.author, queue))
        await ctx.send(f'Ты удалён из очереди :)')


@bot.command()
async def push(ctx):
    if working:
        author = ctx.message.author
        if author in queue:
            await ctx.send(f'Ты уже добавлен в очередь')
        else:
            queue.append(author)
            await ctx.send("Ты добавлен в очередь, твой номер: {}".format(len(queue)))


@bot.command()
async def ping(ctx):
    if working:
        author = ctx.message.author
        await ctx.send(f'Pong, {author.nick}!')


bot.run(settings['token'])
