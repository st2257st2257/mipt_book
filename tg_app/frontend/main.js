import { Telegraf, Markup } from 'telegraf'
import { message } from 'telegraf/filters'

const token = '7539153786:AAG1DiZ4B9sZPH_1YiMigM2cr06LFiXeUr8'
const webAppUrl = 'https://vk.com/'

const bot = new Telegraf(token)

bot.command('start', (ctx) => {
  ctx.reply(
    'Добро пожаловать! Нажмите на кнопку ниже, чтобы запустить приложение',
    Markup.keyboard([
      Markup.button.webApp('Отправить сообщение', `${webAppUrl}/feedback`),
    ])
  )
})

bot.launch()
