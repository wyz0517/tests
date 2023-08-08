#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.
import logging
import asyncio  # 引入异步IO库用于延迟操作

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, COPY_LINK = range(4)
recharge, recharge_bsc_usdt = 4, 5


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    # 添加这一段来发送邀请链接
    user_id = update.effective_user.id  # 获取用户ID
    invite_link = f"https://t.me/LanBiZiSGKbot?code={user_id}"
    await context.bot.send_message(chat_id=update.message.chat_id, text=f"您的邀请链接是：{invite_link}")
    keyboard = [
        [
            InlineKeyboardButton("开始查询", callback_data=str(ONE)),
            InlineKeyboardButton("个人中心", callback_data=str(TWO)),
            InlineKeyboardButton("通知频道", url="https://t.me/SGKonlyChannel"),  # 将这里的链接替换为你的频道链接
            InlineKeyboardButton("充值", callback_data=str(recharge)),
            InlineKeyboardButton("帮助", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text(
        "你好，欢迎使用蓝鼻子社工库机器人！\n本社工库支持同名信息、共享ofo，可查询到身份证、手机号、邮箱、家庭住址、外卖信息、QQ绑定、微博绑定、户籍信息、同邮服、群关系等等\n\n通过点击菜单运行对应的指令 从(/start)开始 \n将你要查询的消息，点击 \\start 可以开始查询",
        reply_markup=reply_markup)

    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES

async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons and multiple prompts"""
    query = update.callback_query
    await query.answer()

    # 发送第一个提示
    await context.bot.send_message(chat_id=query.message.chat_id, text="请在上方选择你需要的查询类型。\n 基础查询：通过身份证 手机号 QQ 用户名 密码 查询 \n 猎魔查询：通过地址 或 名字 或 地区出生日期 查询")

    keyboard = [
        [
            InlineKeyboardButton("基础查询", callback_data=str(THREE)),
            InlineKeyboardButton("猎魔查询", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="输入你想查询的类型", reply_markup=reply_markup
    )
    return START_ROUTES


async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("检查我的安全性", callback_data=str(ONE)),
            InlineKeyboardButton("我的积分", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="无权限", reply_markup=reply_markup
    )
    return START_ROUTES


async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    query = update.callback_query
    await query.answer()

    # 发送第一条消息
    await context.bot.send_message(chat_id=query.message.chat_id, text="无权限")

    user_id = update.effective_user.id  # 获取用户ID
    invite_link = f"https://t.me/LanBiZiSGKbot?code={user_id}"
    await context.bot.send_message(chat_id=query.message.chat_id, text=f"您的邀请链接是：{invite_link}")

    # 发送第三条消息
    await context.bot.send_message(chat_id=query.message.chat_id, text="非常抱歉，您暂时没有查询权限！\n\n你可以通过:\n1. 邀请三位好友获得查询权限\n2. 充值10USDT获得查询权限")

    # 发送/start命令
    await context.bot.send_message(chat_id=query.message.chat_id, text="点击 /start 回到主菜单")

    # Transfer to conversation state `SECOND`
    return END_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

# 邀请链接
async def copy_invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send an invite link to the user."""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id  # 获取用户ID
    invite_link = f"https://t.me/LanBiZiSGKbot?code={user_id}"

    await context.bot.send_message(chat_id=query.message.chat_id, text=f"您的邀请链接是：{invite_link}")

    return ConversationHandler.END

# 充值
async def recharge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle recharge request."""
    query = update.callback_query
    await query.answer()

    # 发送充值信息
    await context.bot.send_message(chat_id=query.message.chat_id,
                                   text="目前仅支持币安Bep20和波场Trc20链，USDT充值，请确保与你使用的链接相符")

    # 提供选择充值金额的内联键盘
    keyboard = [
        [InlineKeyboardButton("10USDT/49次", callback_data="recharge_bsc_usdt"),
         InlineKeyboardButton("50USDT/299次", callback_data="recharge_bsc_usdt")],
        [InlineKeyboardButton("100USDT/699次", callback_data="recharge_bsc_usdt"),
         InlineKeyboardButton("500USDT/4999次", callback_data="recharge_bsc_usdt")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=query.message.chat_id,
                                   text="请选择充值金额，充值越多约优惠：",
                                   reply_markup=reply_markup)

    return START_ROUTES


async def recharge_bsc_usdt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle recharge request."""
    query = update.callback_query
    await query.answer()

    # 仅发送“正在生成.........”的消息
    await context.bot.send_message(chat_id=query.message.chat_id, text="正在生成.........")

    # 等待两秒
    await asyncio.sleep(2)

    # 发送另一条消息
    await context.bot.send_message(chat_id=query.message.chat_id, text="您的充值链接已生成，请在三十分钟内完成充值：\n\n币安BEP20链：0x12F9E97b84aE85df7d7Ce12dCe01Ac35e9396481 \n波场Trc20链：TLbt8jfF8TMCDCJzzoKhvPTW6Zvsz3n3Cz")

    return START_ROUTES



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6345017304:AAEuOldZ6sDfZ6FzTNilaE6vYM-Ngwa8TP8").build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(recharge, pattern="^" + str(recharge) + "$"),
                CallbackQueryHandler(recharge_bsc_usdt, pattern="^recharge_bsc_usdt$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(copy_invite_link, pattern="^" + str(COPY_LINK) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
            ],

        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
