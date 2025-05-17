import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _, I18n
from aiogram.utils.i18n import lazy_gettext as __
from Librarybot.states import StepByStepStates
from database import Orders
from dotenv import load_dotenv
from database import Session, engine

load_dotenv()
TOKEN = getenv("TOKEN")
dp = Dispatcher()
i18n = I18n(path="locales", default_locale="en", domain="messages")

def make_inline_buttons(btns, sizes):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=text, callback_data=text) for text in btns])
    ikb.adjust(*sizes)
    return ikb.as_markup(resize_keyboard=True)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text=_("Kitoblar katalogi"), callback_data=_("kitoblar katalogi")),
        InlineKeyboardButton(text=_("Buyurtmalarim"), callback_data=_("buyurtmalarim")),
        InlineKeyboardButton(text=_("Aloqa"), callback_data=_("aloqa"))
    )
    ikb.adjust(*[2,1])
    await message.answer(_(f"Hello, {html.bold(message.from_user.full_name)}! Asosiy menuga xush kelibsiz!"), reply_markup=ikb.as_markup())




# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")

@dp.callback_query(F.data == __("aloqa"))
async def aloqa_handler(callback : CallbackQuery):
    await callback.message.answer(text="https://t.me/Akhmadalief")

@dp.callback_query(F.data == __("buyurtmalarim"))
async def order_handler(callback : CallbackQuery):
    await callback.message.answer(text=_("Hech qanday buyurtma mavjud emas"))

@dp.callback_query(F.data == __("kitoblar katalogi"))
async def book_category_handler(callback:CallbackQuery):
    btns = [__("Badiiy adabiyot"), __("Ilmiy-ommabop"), __("Biznes va rivojlanish"), __("Orqaga")]
    sizes = [3, 1]
    markup = make_inline_buttons(btns, sizes)
    await callback.message.answer(_("Iltimos kitob turini tanlang!"), reply_markup=markup)


@dp.callback_query(F.data == __("Badiiy adabiyot"))
async def documentary_book_handler(callback:CallbackQuery):
    btns = ["Mehrobdan Chayon - Cho'lpon", "O'tkan kunlar - Abdulla Qodiriy", "Orqaga"]
    sizes = [2, 1]
    markup = make_inline_buttons(btns, sizes)
    await callback.message.answer("Iltimos kitob tanlang!", reply_markup=markup)

@dp.callback_query(F.data == "Mehrobdan Chayon - Cho'lpon")
async def book_saver_handler(callback:CallbackQuery, state :FSMContext):
    order = Orders(name="Mehrobdan Chayon", category="Badiiy adabiyot", author="Cho'lpon", price=30000)
    Session().add(order)
    Session().commit()
    await callback.message.answer("Kitob buyurtmalar savatiga tushdi!")

@dp.callback_query(F.data == "O'tkan kunlar - Abdulla Qodiriy")
async def book_saver_handler(callback:CallbackQuery, state :FSMContext):
    order = Orders(name="O'tkan kunlar", category="Badiiy adabiyot", author="Abdulla Qodiriy", price=50000)
    Session().add(order)
    Session().commit()
    await callback.message.answer("Kitob buyurtmalar savatiga tushdi!")


@dp.callback_query(F.data == "Ilmiy-ommabop")
async def scientific_book_handler(callback:CallbackQuery):
    btns = ["Tibbiyot mo'jizalari - David Agus", "Qiziqarli fizika - Perelman", "Orqaga"]
    sizes = [2, 1]
    markup = make_inline_buttons(btns, sizes)
    await callback.message.answer("Iltimos kitob tanlang!", reply_markup=markup)

@dp.callback_query(F.data == "Tibbiyot mo'jizalari - David Agus")
async def book_saver_handler(callback:CallbackQuery, state :FSMContext):
    order = Orders(name="Tibbiyot mo'jizalari", category="Ilmiy-ommabop", author="David Agus", price=100000)
    Session().add(order)
    Session().commit()
    await callback.message.answer("Kitob buyurtmalar savatiga tushdi!")

@dp.callback_query(F.data == "Qiziqarli fizika - Perelman")
async def book_saver_handler(callback:CallbackQuery,  state :FSMContext):
    order = Orders(name="Qiziqarli fizika", category="Ilmiy-ommabop", author="Perelman", price=20000)
    Session().add(order)
    Session().commit()
    await callback.message.answer("Kitob buyurtmalar savatiga tushdi!")

@dp.callback_query(F.data == "Biznes va rivojlanish")
async def business_book_handler(callback:CallbackQuery):
    btns = ["Muvaffaqiyat odatlari - Stephen Covey", "Boy ota, kambag'al ota - Robert Kiyosaki", "Orqaga"]
    sizes = [2, 1]
    markup = make_inline_buttons(btns, sizes)
    await callback.message.answer("Iltimos kitob tanlang!", reply_markup=markup)

@dp.callback_query(F.data == "Muvaffaqiyat odatlari - Stephen Covey")
async def book_saver_handler(callback:CallbackQuery, state :FSMContext):
    order = Orders(name="Muvaffaqiyat odatlari", category="Biznes va rivojlanish", author="Stephen Covey", price=5000)
    Session().add(order)
    Session().commit()
    await callback.message.answer("Kitob buyurtmalar savatiga tushdi!")

@dp.callback_query(F.data == "Boy ota, kambag'al ota - Robert Kiyosaki")
async def book_saver_handler(callback:CallbackQuery,  state :FSMContext):
    order = Orders(name="Boy ota, kambag'al ota", category="Biznes va rivojlanish", author="Robert Kiyosaki", price=5000)
    Session().add(order)
    Session().commit()
    await callback.message.answer("Kitob buyurtmalar savatiga tushdi!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


@dp.callback_query(F.data == 'Orqaga')
async def back_handler(message: Message, state: FSMContext):
    btns = ["kitoblar katalogi", "buyurtmalarim", "aloqa"]
    sizes = [2, 1]
    markup = make_inline_buttons(btns, sizes)
    await state.set_state(StepByStepStates.step1)
    await message.answer("Ortga qaytdingiz. Iltimos, menu tanlang:", reply_markup=markup)