from asyncio import subprocess
import logging
import os
import sys
import asyncio
import webbrowser
from tkinter import Label, Tk, filedialog
import cv2
import psutil
import pyautogui
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from PIL import ImageGrab
import pygetwindow as gw

API_TOKEN = '7848221838:AAHEGV7HqoFVu18Uv2jcpZmnVjQ2Sj4TcVU' #Вставьте токен
Bot = Bot(token=API_TOKEN)
dp = Dispatcher()

awaiting_file = False

class Form(StatesGroup):
    input_variable = State()

exit = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад ⬅️')]],
    resize_keyboard=True
)

failss = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Открыть файл 📤', callback_data="files1")],
    [InlineKeyboardButton(text='Получить файл 📥', callback_data="files2")]]
)

def open_file_explorer():
    root = Tk()
    root.withdraw()  # Скрыть основное окно tkinter
    root.attributes('-topmost', True)  # Открыть проводник поверх других окон
    file_path = filedialog.askopenfilename()  # Диалог выбора файла
    return file_path

zero = ReplyKeyboardMarkup(keyboard=[])

startkalava = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Запустить', callback_data="starty"),
    InlineKeyboardButton(text='Помощь', callback_data="help", url="https://t.me/Vandallov2")]
])

pover1 = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Да ✔️', callback_data="yes1"),
    InlineKeyboardButton(text='Нет ❌', callback_data="not")]
])

pover2 = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Да ✔️', callback_data="yes2"),
    InlineKeyboardButton(text='Нет ❌', callback_data="not")]
])

pover3 = InlineKeyboardMarkup (inline_keyboard=[
    [InlineKeyboardButton(text='Да ✔️', callback_data="yes3"),
    InlineKeyboardButton(text='Нет ❌', callback_data="not")]
])

pover_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Сон 🌙')],
        [KeyboardButton(text= 'Завершение работы 📴')],
        [KeyboardButton(text='Перезагрузка 🔃')],
        [KeyboardButton(text='Назад ⬅️')]],
        resize_keyboard=True,
        input_field_placeholder='Управление питанием...')



main_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Скриншот 🖥️'),
        KeyboardButton(text='Фото 📷')],
        [KeyboardButton(text='Браузер 🌐'),
        KeyboardButton(text='Сайты 📱')],
        [KeyboardButton(text='Заряд 🔋'),
        KeyboardButton(text='Файлы 📁')],
        [KeyboardButton(text='Питание 💻')],
        [KeyboardButton(text='Текст на экран ✏️')],
        [KeyboardButton(text= 'Меню ⚙')]],
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...')

class LinkInput(StatesGroup):
    waiting_for_link = State() 
    
class ScreenTextState(StatesGroup):
    waiting_for_text = State()

class TextDisplayState(StatesGroup):
    waiting_for_text = State()

# Обработчик команды для вывода текста на экран
@dp.message(F.text == "Текст на экран ✏️")
async def request_screen_text(message: Message, state: FSMContext):
    # Спрашиваем у пользователя текст для отображения
    await message.answer("Введите текст, который нужно отобразить на экране ✏️")
    # Устанавливаем состояние для ожидания ввода текста
    await state.set_state(TextDisplayState.waiting_for_text)

@dp.message(TextDisplayState.waiting_for_text)
async def display_screen_text(message: Message, state: FSMContext):
    # Проверяем, что сообщение содержит текст
    if not message.text:
        # Если сообщение не текстовое, сообщаем об ошибке
        await message.answer("Ошибка: пожалуйста, отправьте текст, чтобы он отобразился на экране❌")
        return  # Прекращаем выполнение функции

    user_text = message.text  # Получаем введенный текст

    # Функция для отображения текста с помощью tkinter
    def show_text_on_screen(text):
        root = Tk()
        root.title("Текст на экран ✏️")

        # Настраиваем окно, чтобы оно отображалось поверх всех окон
        root.attributes("-topmost", True)

        # Получаем размер экрана и вычисляем центр
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width, window_height = 400, 100
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Настраиваем текстовый лейбл
        label = Label(root, text=text, font=("Arial", 16), wraplength=380, justify="center")
        label.pack(expand=True, fill="both")

        # Окно останется открытым, пока пользователь не закроет его вручную
        root.mainloop()

    # Запускаем функцию отображения текста в фоновом режиме
    asyncio.create_task(asyncio.to_thread(show_text_on_screen, user_text))
    
    # Сообщаем пользователю, что текст отображается
    await message.answer("Текст отображается на экране ✅")

    # Сбрасываем состояние, чтобы функция сработала только один раз после команды
    await state.clear()

@dp.message(CommandStart())
@dp.message(F.text == 'Меню ⚙')
async def start(message: Message):
    await message.answer(text='👋 Добро пожаловать в TG Link!\nЭтот бот — ваш личный помощник для дистанционного управления компьютером через Telegram.\n\nВозможности TG Link:\n📸Захват скриншотов и фото с веб-камеры\n🌐 Открытие сайтов и браузеров\n🔋 Мониторинг состояния батареи\n📂 Доступ к файлам и управление открытыми окнами\n⭐И еще много всего интересного\n\nПросто выберите команду из меню, и TG Link выполнит задачу на вашем компьютере!', reply_markup=startkalava)

@dp.callback_query(F.data == "starty")
async def start(callback: CallbackQuery):
    # Отправляем сообщение в ответ на нажатие кнопки
    await callback.message.answer("Добро пожаловать👾\nВыберите пункт из меню ⬇️",reply_markup=main_keyboard)

@dp.message(F.text == 'Файлы 📁')
async def handle_files(message: Message):
    await message.answer(
        'Способ взаимодействия с файлами:',reply_markup=failss)
@dp.message(F.text == 'Питание 💻')
async def pover(message: Message):
    await message.answer('Выберите пункт:', reply_markup=pover_keyboard)

@dp.message(F.text == 'Сон 🌙')
async def sleep_mode(message: Message):
    await message.answer(text="Вы точно хотите отправить компьютер в сон? 🌙",reply_markup=pover1)

@dp.message(F.text == 'Перезагрузка 🔃')
async def sleep_mode(message: Message):
    await message.answer(text="Вы точно хотите запустить перезагрузку? 🔃",reply_markup=pover3)


@dp.message(F.text == 'Завершение работы 📴')
async def off_mode(message: Message):
    await message.answer(text="Вы точно хотите выключить компьютер? 📴",reply_markup=pover2)

@dp.callback_query(F.data == "yes1")
async def request_file(callback: CallbackQuery):
     await callback.message.answer("Компьютер уходит в сон 🌙",reply_markup=main_keyboard)
     os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

@dp.callback_query(F.data == "yes3")
async def request_file(callback: CallbackQuery):
     await callback.message.answer("Переагрузка 🔃",reply_markup=main_keyboard)
     os.system("shutdown /r /t 0")


@dp.callback_query(F.data == "yes2")
async def request_file(callback: CallbackQuery):
    await callback.message.answer("Выключение компьютера 📴",reply_markup=main_keyboard)
    os.system("shutdown /s /t 0")
@dp.callback_query(F.data == "not")
async def request_file(callback: CallbackQuery):
         await callback.message.answer("Действие отменено ❌", reply_markup=main_keyboard)



@dp.callback_query(F.data == "files1")
async def request_file(callback: CallbackQuery):
    global awaiting_file
    awaiting_file = True  # Устанавливаем флаг ожидания файла
    await callback.message.answer("Отправьте файл, который вы хотите открыть на ПК 💾")

# Обработчик получения различных типов файлов от пользователя
@dp.message(F.content_type.in_({'document', 'photo', 'video', 'video_note', 'audio'}))
async def receive_file(message: types.Message):
    global awaiting_file
    if awaiting_file:
        if message.document:
            file_id = message.document.file_id
            file_name = message.document.file_name
            extension = os.path.splitext(file_name)[1]
        elif message.photo:
            file_id = message.photo[-1].file_id  # Берем последнюю версию фото (самую большую)
            file_name = "photo.jpg"
            extension = ".jpg"
        elif message.video:
            file_id = message.video.file_id
            file_name = "video.mp4"
            extension = ".mp4"
        elif message.video_note:
            file_id = message.video_note.file_id
            file_name = "video_note.mp4"
            extension = ".mp4"
        elif message.audio:
            file_id = message.audio.file_id
            file_name = message.audio.file_name or "audio.mp3"
            extension = os.path.splitext(file_name)[1] if file_name else ".mp3"

        # Загрузка и сохранение файла
        file = await Bot.get_file(file_id)
        file_path = f"downloaded_file{extension}"
        await Bot.download_file(file.file_path, destination=file_path)

        # Открываем файл на компьютере

        os.startfile(file_path)
        await message.answer(f"Файл '{file_name}' получен и открыт ✅")

        # Сбрасываем флаг ожидания файла
        awaiting_file = False


@dp.message(lambda message: message.text == 'Фото 📷')
async def send_photo(message: Message):
    await message.answer("Загрузка...")
    try:
        # Открываем доступ к камере
        camera = cv2.VideoCapture(0)
        # Захватываем изображение с камеры
        ret, frame = camera.read()
        # Путь для сохранения фотографии
        photo_path = os.path.join(os.getcwd(), "photo.jpg")
        # Сохраняем изображение в файл
        cv2.imwrite(photo_path, frame)
        file_path = "photo.jpg"
        file = FSInputFile(file_path)
        await message.answer_document(document=file)
        # Закрываем камеру (на всякий случай)
        camera.release()
    except Exception as e:
        await message.answer(f'Отсутствует доступ к камере❌\n\n1.Пожалуйста, проверьте подключение камеры и убедитесь, что доступ к ней разрешен в настройках устройства.\n2.Возможно, камера занята другим приложением, либо отсутствуют необходимые разрешения для её использования.\nОшибка:{e}')

class Form(StatesGroup):
    input_variable = State()

@dp.message(F.text == 'Сайты 📱')
async def handle_screenshot(message: types.Message):
    maen_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='YouTube 📼')],
        [KeyboardButton(text='Telegram ✈️')],
        [KeyboardButton(text='ChatGPT 🤖')],
        [KeyboardButton(text='Gmail 📩')],
        [KeyboardButton(text='Своя ссылка 👤')],
        [KeyboardButton(text='Назад ⬅️')]],
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...')
    await message.answer('Выберите пункт:', reply_markup=maen_keyboard)

@dp.message(F.text == "YouTube 📼")
async def youtube(message: types.Message):
    webbrowser.open('https://www.youtube.com/')
    await message.answer('Сайт открыт ✅')

@dp.message(F.text == "Telegram ✈️")
async def youtube(message: types.Message):
    webbrowser.open('https://web.telegram.org/a/')
    await message.answer('Сайт открыт ✅')

@dp.message(F.text == "ChatGPT 🤖")
async def youtube(message: types.Message):
    webbrowser.open('https://chatgpt.com/')
    await message.answer('Сайт открыт ✅')

@dp.message(F.text == "Gmail 📩")
async def youtube(message: types.Message):
    webbrowser.open('https://mail.google.com/mail/')
    await message.answer('Сайт открыт ✅')

@dp.message(F.text == "Назад ⬅️")
async def youtube(message: types.Message):
    await message.answer('Выберите пункт:',reply_markup=main_keyboard)

@dp.message(F.text == "Своя ссылка 👤")
async def start_input(message: Message, state: FSMContext):
    # Переводим в состояние ожидания ссылки
    await state.set_state(LinkInput.waiting_for_link)
    await message.answer("Введите ссылку", reply_markup=types.ReplyKeyboardRemove())

# Обработка ввода ссылки
@dp.message(LinkInput.waiting_for_link)
async def open_link(message: Message, state: FSMContext):
    link = message.text  # Получаем текст, введенный пользователем
    webbrowser.open(link)  # Открываем ссылку в браузере
    await message.answer('Сайт открыт ✅', reply_markup=main_keyboard)

    # Завершаем состояние, чтобы для открытия новой ссылки нужно было снова нажать "Своя ссылка 👤"
    await state.clear()

@dp.message(lambda message: message.text == "Заряд 🔋")
async def send_battery_status(message: types.Message):
    try:
        import psutil  # Убедись, что библиотека psutil установлена
        battery = psutil.sensors_battery()
        percent = battery.percent
        is_plugged = battery.power_plugged
        status = "Подключено к зарядке" if is_plugged else "Не подключено к зарядке"
        await message.answer(f"Заряд батареи: {percent}%\nСтатус: {status}")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@dp.callback_query(lambda message: message.data == 'files2')
async def handle_choose_file(callback: CallbackQuery):
    await callback.message.answer("Открываю проводник для выбора файла...")
    
    # Открытие проводника и выбор файла
    file_path = open_file_explorer()
    
    if file_path:
        try:
            # Отправка выбранного файла пользователю
            file = FSInputFile(file_path)
            await callback.message.answer_document(file)
        except Exception as e:
            # Обработка любой ошибки и отправка сообщения пользователю
            await callback.message.answer(f"Файл слишком большой ❌")
    else:
        await callback.message.answer("Файл не выбран ❌")

@dp.message(F.text == 'Скриншот 🖥️')
async def handle_screenshot(message: types.Message):
    await message.answer("Загрузка...")
    try:
        screenshot = ImageGrab.grab() 
        save_path = r'screen.jpg'  # Укажите доступный путь для сохранения
        screenshot.save(save_path)
        file_path = "screen.jpg"  # Замените на ваш путь
        file = FSInputFile(file_path)  # Создаем объект файла
        await message.answer_document(document=file)
    except Exception as e:  # Ловим исключение и сохраняем текст ошибки в переменную e
        await message.answer(f"Ошибка: {e}")

@dp.message(F.text == 'Браузер 🌐')
async def google(message: Message):
    webbrowser.open("https://")
    await message.answer('Браузер открыт ✅')


async def main():
    await dp.start_polling(Bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print ('Бот выключен')
            