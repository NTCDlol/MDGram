import asyncio
import os
from telethon import types
from telethon import events
from telethon import TelegramClient, functions
from getpass import getpass
from colorama import init, Fore, Back, Style
import sys
import aioconsole
# Инициализация colorama (автоматический сброс цвета)
init(autoreset=True)
commands = """
    В чате:
    !Ответ (ID сообщения) (Ответ) — ответ на сообщение
    !Удалить (ID сообщения) — удалить сообщение
    !Изменить (ID сообщения) (Текст) — изменить сообщение
    !Переслать (ID сообщения) (Номер чата) — переслать сообщение
    !Копировать (ID сообщения) — скопировать сообщение
    !Отпр (текст) — отправить сообщение
    !Выход — выход в выбор чатов
    !Поиск (текст) — поиск сообщений
    !Вверх — старые сообщения
    !Вниз — новые сообщения

    В выборе чатов:
    !Меню — открыть меню
    !Выход — выйти из MDGram
    !ВыйтиИзГруппы (Номер чата) — выйти из группы
    !Архив — просмотр архива
    !Архивиров (Номер чата) — архивировать чат
    !Разархивиров (Номер чата) — разархивировать чат
    !Далее — листать чаты вперед
    !Назад — листать чаты назад
    !Поиск (текст или юз) — поиск чатов
    
    В главном меню:
    !помощь    - Все команды MDGram
    !чаты      - Показать список чатов
    !профиль   - Изменение профиля (в разработке)
    !темы      - Выбор темы (в разработке)
    !группы    - Создание групп (в разработке)
    !каналы    - Создание каналов (в разработке)
    !настройки - Настройки клиента (в разработке)
    !выход     - Выход из MDGram
    """

print(f"""
        {Fore.CYAN}@@@@@@                                 {Fore.WHITE}Представляю вам {Fore.RED}MDGram
       {Fore.CYAN}*===--=*@                               {Fore.WHITE}Телеграм в интерфейсе командной строки здесь!
      {Fore.CYAN}@======--=*@  
       {Fore.CYAN}*=======--=*@                           {Fore.WHITE}Для помощи во всех командах — {Fore.YELLOW}!помощь  
        {Fore.CYAN}@*======---=@@                         
          {Fore.CYAN}@+======---*@                        {Fore.WHITE}Если есть какие то вопросы, пишите в тг:  
           {Fore.CYAN}@*======-:=@  
       {Fore.CYAN}@*+======---*@                          {Fore.MAGENTA}@NTheCuteDrone  
      {Fore.CYAN}@*+======--=+@@  
     {Fore.BLUE}@=======--=+@@      @*************+*@     {Fore.WHITE}Этот проект с {Fore.GREEN}открытым кодом  
     {Fore.BLUE}*=====--=+@        +-============----@  
      {Fore.BLUE}*+====*@           @++++++++++++==*@     {Fore.WHITE}Как и обычный тг
""")


def load_theme(filename):
    """
    Загружает тему из текстового файла, где каждая строка имеет вид:
      key="VALUE"
    Если файла нет, используется тема по умолчанию.
    """
    theme = {}
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    value = value.strip().strip('"').strip("'")
                    theme[key.strip()] = value
    else:
        theme = {
            "theme_name": "Defalut Theme",
            "theme_type": "Black",
            "you_in_chat": "GREEN",
            "friend_in_chat": "CYAN",
            "id": "CYAN",
            "login": "CYAN",
            "error": "RED",
            "cancel": "YELLOW",
            "messages_from": "MAGENTA",
            "chats": "MAGENTA",
            "ls": "GREEN",
            "group": "MAGENTA",
            "channel": "YELLOW",
            "default_text": "WHITE",
            "background": "BLACK"
        }
    return theme

# Загружаем тему из файла "theme.txt"
THEME = load_theme("theme.txt")

# Определяем цвета на основе темы с помощью colorama
LOGIN_COLOR          = getattr(Fore, THEME.get("login", "CYAN").upper(), Fore.CYAN)
ERROR_COLOR          = getattr(Fore, THEME.get("error", "RED").upper(), Fore.RED)
CANCEL_COLOR         = getattr(Fore, THEME.get("cancel", "YELLOW").upper(), Fore.YELLOW)
MESSAGES_FROM_COLOR  = getattr(Fore, THEME.get("messages_from", "MAGENTA").upper(), Fore.MAGENTA)
CHATS_COLOR          = getattr(Fore, THEME.get("chats", "MAGENTA").upper(), Fore.MAGENTA)
LS_COLOR             = getattr(Fore, THEME.get("ls", "GREEN").upper(), Fore.GREEN)
GROUP_COLOR          = getattr(Fore, THEME.get("group", "MAGENTA").upper(), Fore.MAGENTA)
CHANNEL_COLOR        = getattr(Fore, THEME.get("channel", "YELLOW").upper(), Fore.YELLOW)
DEFAULT_TEXT_COLOR   = getattr(Fore, THEME.get("default_text", "WHITE").upper(), Fore.WHITE)
YOU_IN_CHAT_COLOR    = getattr(Fore, THEME.get("you_in_chat", "GREEN").upper(), Fore.GREEN)
FRIEND_IN_CHAT_COLOR = getattr(Fore, THEME.get("friend_in_chat", "CYAN").upper(), Fore.CYAN)
ID_COLOR             = getattr(Fore, THEME.get("id", "CYAN").upper(), Fore.CYAN)

BACKGROUND_COLOR     = getattr(Back, THEME.get("background", "BLACK").upper(), Back.BLACK)

# Данные API (замените на свои, если необходимо)
api_id = 20099121
api_hash = "b83debb0bceee57863dbd19954b97e0e"

async def authenticate():
    """
    Авторизация пользователя в Telegram.
    Если сессия уже существует, номер не запрашивается.
    """
    client = TelegramClient("tg_client", api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        phone_number = input(LOGIN_COLOR + "Введите номер телефона (пример: +1234567890): ")
        await client.send_code_request(phone_number)
        code = input(LOGIN_COLOR + "Введите код из Telegram: ")
        try:
            await client.sign_in(phone_number, code)
        except Exception as e:
            if "SESSION_PASSWORD_NEEDED" in str(e):
                password = getpass(CANCEL_COLOR + "Введите пароль (2FA): ")
                await client.sign_in(password=password)
            else:
                print(ERROR_COLOR + "Ошибка авторизации:", e)
                return None
    return client

async def chat_selection_loop(client):
    """
    Меню выбора чата.
    Отображаются чаты по 25 на странице.
    Дополнительные команды в этом меню:
      !архив          — просмотр архивированных чатов
      !архивиров      — архивировать чат (номер чата)
      !разархивиров   — разархивировать чат (номер чата)
      !далее          — следующая страница чатов
      !назад          — предыдущая страница чатов
      !поиск (текст или юз) — поиск чатов по имени или username
      !меню           — возврат в главное меню
    """
    dialogs = await client.get_dialogs()
    chats_list = [d for d in dialogs if not getattr(d, 'archived', False)]
    chat_page_index = 0
    while True:
        start_index = chat_page_index * 25
        end_index = start_index + 25
        current_page = chats_list[start_index:end_index]
        print(CHATS_COLOR + f"\nВаши чаты (страница {chat_page_index + 1}):")
        for idx, chat in enumerate(current_page, start=start_index + 1):
            if chat.is_user:
                chat_type = LS_COLOR + "[ЛС]"
            elif chat.is_group:
                chat_type = GROUP_COLOR + "[Группа]"
            else:
                chat_type = CHANNEL_COLOR + "[Канал]"
            print(f"{Fore.GREEN}{idx}. {chat_type} {DEFAULT_TEXT_COLOR}{chat.name}")
            
        choice = input(DEFAULT_TEXT_COLOR + "mdgram/чаты > ")
        if choice.startswith('!'):
            parts = choice.split()
            command = parts[0].lower()
            if command == "!":
                return "!"
            if command == '!меню':
                # Возврат в главное меню
                return None
            elif command == '!архив':
                try:
                    archived_dialogs = await client.get_dialogs(archived=True)
                    archived_list = list(archived_dialogs)
                    if archived_list:
                        print(CHATS_COLOR + "\nАрхивированные чаты:")
                        for idx, chat in enumerate(archived_list, start=1):
                            print(f"{Fore.GREEN}{idx}. {chat.name}")
                    else:
                        print(CANCEL_COLOR + "Архив пуст.")
                except Exception as e:
                    print(ERROR_COLOR + f"Ошибка при получении архивированных чатов: {e}")
            elif command == '!архивиров':
                if len(parts) < 2:
                    print(ERROR_COLOR + "Укажите номер чата для архивирования.")
                else:
                    try:
                        chat_number = int(parts[1])
                        if 1 <= chat_number <= len(chats_list):
                            chat_to_archive = chats_list[chat_number - 1]
                            try:
                                await client(functions.messages.HideChatRequest(
                                    peer=chat_to_archive.entity,
                                    excluded=False
                                ))
                                print(LS_COLOR + f"Чат {chat_to_archive.name} архивирован.")
                                chats_list.remove(chat_to_archive)
                            except Exception as e:
                                print(ERROR_COLOR + f"Не удалось архивировать чат: {e}")
                        else:
                            print(ERROR_COLOR + "Неверный номер чата!")
                    except ValueError:
                        print(ERROR_COLOR + "Неверный формат номера!")
            elif command == '!разархивиров':
                if len(parts) < 2:
                    print(ERROR_COLOR + "Укажите номер чата для разархивирования.")
                else:
                    try:
                        chat_number = int(parts[1])
                        archived_dialogs = await client.get_dialogs(archived=True)
                        archived_list = list(archived_dialogs)
                        if 1 <= chat_number <= len(archived_list):
                            chat_to_unarchive = archived_list[chat_number - 1]
                            try:
                                await client(functions.messages.HideChatRequest(
                                    peer=chat_to_unarchive.entity,
                                    excluded=True
                                ))
                                print(LS_COLOR + f"Чат {chat_to_unarchive.name} разархивирован.")
                                chats_list.append(chat_to_unarchive)
                            except Exception as e:
                                print(ERROR_COLOR + f"Не удалось разархивировать чат: {e}")
                        else:
                            print(ERROR_COLOR + "Неверный номер чата!")
                    except ValueError:
                        print(ERROR_COLOR + "Неверный формат номера!")
            elif command == '!далее':
                if end_index < len(chats_list):
                    chat_page_index += 1
                else:
                    print(CANCEL_COLOR + "Это последняя страница.")
            elif command == '!назад':
                if chat_page_index > 0:
                    chat_page_index -= 1
                else:
                    print(CANCEL_COLOR + "Это первая страница.")
            elif command == '!поиск':
                if len(parts) < 2:
                    print(ERROR_COLOR + "Использование: !Поиск (текст или юз)")
                else:
                    search_text = " ".join(parts[1:])
                    filtered = [chat for chat in chats_list if 
                                (chat.name and search_text.lower() in chat.name.lower()) or 
                                (hasattr(chat.entity, 'username') and chat.entity.username and search_text.lower() in chat.entity.username.lower())]
                    if filtered:
                        print(CHATS_COLOR + f"\nНайдено {len(filtered)} чатов:")
                        for idx, chat in enumerate(filtered, start=1):
                            if chat.is_user:
                                chat_type = LS_COLOR + "[ЛС]"
                            elif chat.is_group:
                                chat_type = GROUP_COLOR + "[Группа]"
                            else:
                                chat_type = CHANNEL_COLOR + "[Канал]"
                            print(f"{Fore.GREEN}{idx}. {chat_type} {DEFAULT_TEXT_COLOR}{chat.name}")
                        sel = input(DEFAULT_TEXT_COLOR + "Введите номер чата из найденных или нажмите Enter для отмены: ")
                        if sel.isdigit():
                            sel_index = int(sel) - 1
                            if 0 <= sel_index < len(filtered):
                                return filtered[sel_index], chats_list
                            else:
                                print(ERROR_COLOR + "Неверный номер.")
                        else:
                            print(CANCEL_COLOR + "Поиск отменён.")
                    else:
                        print(CANCEL_COLOR + "Чаты не найдены по заданному запросу.")
            else:
                print(ERROR_COLOR + "Неизвестная команда. Если вы хотелт отправить знак '!' попробуйте ещё раз, но только с одним таким знаком")
        else:
            try:
                chat_number = int(choice)
                if 1 <= chat_number <= len(chats_list):
                    return chats_list[chat_number - 1], chats_list
                else:
                    print(ERROR_COLOR + "Неверный номер чата!")
            except ValueError:
                print(ERROR_COLOR + "Ошибка: введите число или команду!")

async def chat_interaction_loop(client, chat, chats_list):
    message_page_stack = [None]  # Хранит историю страниц сообщений
    current_messages = []
    me = await client.get_me()
    partial_input = ""  # Сохраняет ввод, если пользователь не успел дописать

    def redraw_input():
        """Перерисовывает ввод, если пришло новое сообщение."""
        sys.stdout.write("\r" + " " * 100 + "\r")  # Очищаем строку
        sys.stdout.write(DEFAULT_TEXT_COLOR + f"> {partial_input}")  # Выводим ввод заново
        sys.stdout.flush()

    async def on_new_message(event):
        """Обработчик входящих сообщений"""
        if event.chat_id == chat.id:
            sender = await event.get_sender()
            sender_name = sender.title if isinstance(sender, types.Channel) else sender.first_name if sender else "Неизвестный"

            print(f"\n{ID_COLOR}[{event.message.id}] {FRIEND_IN_CHAT_COLOR}{sender_name}: {DEFAULT_TEXT_COLOR}{event.message.text}")
            redraw_input()

    async def on_my_message(event):
        """Обработчик отправленных сообщений"""
        if event.chat_id == chat.id:
            print(f"\n{ID_COLOR}[{event.message.id}] {YOU_IN_CHAT_COLOR}Вы: {DEFAULT_TEXT_COLOR}{event.message.text}")
            redraw_input()

    # Добавляем обработчики
    client.add_event_handler(on_new_message, event=events.NewMessage)
    client.add_event_handler(on_my_message, event=events.NewMessage(outgoing=True))

    try:
        # Загружаем последние 25 сообщений при входе в чат
        messages = await client.get_messages(chat, limit=25)
        if messages:
            current_messages = sorted(messages, key=lambda m: m.id if m.id is not None else -1)
            print(MESSAGES_FROM_COLOR + f"\nСообщения из {chat.name}:")
            for msg in current_messages:
                sender = await msg.get_sender()
                sender_name = sender.title if isinstance(sender, types.Channel) else sender.first_name if sender else "Неизвестный"
                print(f"{ID_COLOR}[{msg.id}] {FRIEND_IN_CHAT_COLOR}{sender_name}:{DEFAULT_TEXT_COLOR} {msg.text}")
        else:
            print(CANCEL_COLOR + "Нет сообщений для отображения.")

        # **Бесконечный цикл для обработки команд и ввода**
        while True:
            try:
               text = await aioconsole.ainput(DEFAULT_TEXT_COLOR + "> ")
               parts = text.split()
               if not parts:
                   continue  # Пропускаем пустой ввод
               command = parts[0].lower()  # Получаем команду
               
               if command == '!отпр':
                    if len(parts) < 2:
                        print(ERROR_COLOR + "Использование: !отпр (текст)")
                    else:
                        msg_text = " ".join(parts[1:]).replace("\\n", "\n")
                    try:
                        sent = await client.send_message(chat, msg_text)
                        current_messages.insert(0, sent)
                        print(f'{YOU_IN_CHAT_COLOR}Готово!')
                        print(f"\n{ID_COLOR}[{sent.id}] {YOU_IN_CHAT_COLOR}{sender_name}: {DEFAULT_TEXT_COLOR}{msg_text}")
                    except Exception as e:
                        print(ERROR_COLOR + f"Ошибка при отправке сообщения: {e}")
                    partial_input = ""  # Очистка буфера ввода
                    redraw_input()  # Перерисовка ввода
               elif command == '!помощь':
                    print(commands)
                    partial_input = ""  # Очистка буфера ввода
                    redraw_input()  # Перерисовка ввода
               elif command == '!выход':
                    client.remove_event_handler(on_new_message, event=events.NewMessage)
                    partial_input = ""  # Очистка буфера ввода
                    redraw_input()  # Перерисовка ввода
                    break
               elif command == '!вверх':
                   if current_messages:
                        oldest_message = current_messages[0]
                        if oldest_message.id is None:
                            print(CANCEL_COLOR + "Невозможно получить ID самого старого сообщения.")
                        else:
                            new_page = await client.get_messages(chat, limit=25, offset_id=oldest_message.id)
                        if new_page:
                            message_page_stack.append(oldest_message.id)
                        else:
                            print(CANCEL_COLOR + "Больше старых сообщений нет.")
                   else:
                        print(CANCEL_COLOR + "Нет сообщений для перелистывания.")
                   partial_input = ""  # Очистка буфера ввода
                   redraw_input()  # Перерисовка ввода
               elif command == '!вниз':
                  if len(message_page_stack) > 1:
                        message_page_stack.pop()
                  else:
                       print(CANCEL_COLOR + "Это самая новая страница.")
                  partial_input = ""  # Очистка буфера ввода
                  redraw_input()  # Перерисовка ввода
               elif command == '!ответ':
                   if len(parts) < 3:
                        print(ERROR_COLOR + "Использование: !ответ (ID сообщения) (текст)")
                   else:
                       try:
                            msg_id = int(parts[1])
                            reply_text = parts[2].replace("/n", "\n")
                            reply = await client.send_message(chat, reply_text, reply_to=msg_id)
                            print(LS_COLOR + f"Ответ отправлен (ID: {reply.id}).")
                       except ValueError:
                            print(ERROR_COLOR + "Неверный ID сообщения.")
                       except Exception as e:
                            print(ERROR_COLOR + f"Ошибка при отправке ответа: {e}")
                       partial_input = ""  # Очистка буфера ввода
                       redraw_input()  # Перерисовка ввода
               elif command == '!удалить':
                   if len(parts) < 2:
                        print(ERROR_COLOR + "Использование: !удалить (ID сообщения)")
                   else:
                       try:
                            msg_id = int(parts[1])
                            await client.delete_messages(chat, msg_id)
                            print(LS_COLOR + "Сообщение удалено.")
                       except ValueError:
                            print(ERROR_COLOR + "Неверный ID сообщения.")
                       except Exception as e:
                            print(ERROR_COLOR + f"Ошибка при удалении сообщения: {e}")
                       partial_input = ""  # Очистка буфера ввода
                       redraw_input()  # Перерисовка ввода
               elif command == '!изменить':
                   if len(parts) < 3:
                        print(ERROR_COLOR + "Использование: !изменить (ID сообщения) (новый текст)")
                   else:
                       try:
                            msg_id = int(parts[1])
                            new_text = parts[2].replace("/n", "\n")
                            edited = await client.edit_message(chat, msg_id, new_text)
                            print(LS_COLOR + f"Сообщение изменено (ID: {edited.id}).")
                       except ValueError:
                            print(ERROR_COLOR + "Неверный ID сообщения.")
                       except Exception as e:
                            print(ERROR_COLOR + f"Ошибка при изменении сообщения: {e}")
                       partial_input = ""  # Очистка буфера ввода
                       redraw_input()  # Перерисовка ввода
               elif command == '!переслать':
                   if len(parts) < 3:
                        print(ERROR_COLOR + "Использование: !переслать (ID сообщения) (номер чата)")
                   else:
                       try:
                            msg_id = int(parts[1])
                            dest_chat_number = int(parts[2])
                            if 1 <= dest_chat_number <= len(chats_list):
                                dest_chat = chats_list[dest_chat_number - 1]
                                await client.forward_messages(dest_chat, msg_id, from_peer=chat)
                                print(LS_COLOR + f"Сообщение переслано в {dest_chat.name}.")
                            else:
                                print(ERROR_COLOR + "Неверный номер чата для пересылки.")
                       except ValueError:
                            print(ERROR_COLOR + "Неверный формат ID или номера чата.")  
                       except Exception as e:
                            print(ERROR_COLOR + f"Ошибка при пересылке сообщения: {e}") 
               elif command == '!копировать':
                   if len(parts) < 2:
                       print(ERROR_COLOR + "Использование: !копировать (ID сообщения)")
                   else:
                       try:
                           msg_id = int(parts[1])
                           target_msg = next((m for m in current_messages if m.id == msg_id), None)
             
                           if target_msg:
                               print(DEFAULT_TEXT_COLOR + f"Содержимое сообщения [{msg_id}]: {target_msg.text}")
                           else:
                               print(ERROR_COLOR + "Сообщение с таким ID не найдено на текущей странице.") 
                       except ValueError:
                           print(ERROR_COLOR + "Неверный ID сообщения.")
               elif command == '!поиск':
                   if len(parts) < 2:
                       print(ERROR_COLOR + "Использование: !поиск (текст)")
                   else:
                       search_text = " ".join(parts[1:])
                       try:
                           search_results = await client.get_messages(chat, search=search_text, limit=25)
                           if search_results:
                                search_results = sorted(search_results, key=lambda m: m.id if m.id is not None else -1)
                                print(MESSAGES_FROM_COLOR + f"\nРезультаты поиска в {chat.name}:")
                                for msg in search_results:
                                    msg_id = msg.id if msg.id is not None else "Нет ID"
                                    sender = await msg.get_sender()
                                    sender_name = sender.first_name if sender and getattr(sender, 'first_name', None) else "Неизвестный"
                                    print(f"{ID_COLOR}[{msg_id}] {DEFAULT_TEXT_COLOR}{sender_name}: {msg.text}")  
                                else:
                                    print(CANCEL_COLOR + "Сообщения, удовлетворяющие поиску, не найдены.")
                            except Exception as e:
                                print(ERROR_COLOR + f"Ошибка при поиске: {e}")
                       else:
                           print(ERROR_COLOR + "Неизвестная команда.")
                   finally:
                       # Удаляем обработчики при выходе
                       client.remove_event_handler(on_new_message, event=events.NewMessage)
                       client.remove_event_handler(on_my_message, event=events.NewMessage(outgoing=True))
async def main_menu_loop(client):
    """
    Главное меню MDGram, которое открывается после входа.
    Здесь доступны команды:
      !чаты      — показать список чатов (переход в меню выбора чатов)
      !профиль   — изменение профиля (в разработке)
      !темы      — выбор темы (в разработке)
      !группы    — создание групп (в разработке)
      !каналы    — создание каналов (в разработке)
      !настройки — настройки клиента (в разработке)
      !выход     — выход из MDGram
    """
    while True:
        cmd = input(DEFAULT_TEXT_COLOR + "mdgram > ")
        if cmd.lower() == '!чаты':
            print(f'{Fore.YELLOW}Загрузка...')
            selection = await chat_selection_loop(client)
            if selection is None:
                print(CANCEL_COLOR + "Возврат в главное меню.")
            else:
                selected_chat, chats_list = selection
                await chat_interaction_loop(client, selected_chat, chats_list)
        elif cmd.lower() == '!помощь':
            print(DEFAULT_TEXT_COLOR + commands)
        elif cmd.lower() == '!профиль':
            print(DEFAULT_TEXT_COLOR + "Функция изменения профиля (в разработке).")
        elif cmd.lower() == '!темы':
            print(DEFAULT_TEXT_COLOR + "Функция выбора темы (в разработке).")
        elif cmd.lower() == '!группы':
            print(DEFAULT_TEXT_COLOR + "Функция создания групп (в разработке).")
        elif cmd.lower() == '!каналы':
            print(DEFAULT_TEXT_COLOR + "Функция создания каналов (в разработке).")
        elif cmd.lower() == '!настройки':
            print(DEFAULT_TEXT_COLOR + "Функция настроек клиента (в разработке).")
        elif cmd.lower() == '!выход':
            confirm = input(CANCEL_COLOR + "Вы уверены, что хотите выйти из MDGram? (да/нет): ")
            if confirm.lower() == 'да':
                break
        else:
            print(ERROR_COLOR + "Неизвестная команда.")

async def main():
    client = await authenticate()
    if not client:
        return
    await main_menu_loop(client)
    print(CANCEL_COLOR + "Выход из MDGram.")

def get_media_url(media_type, media_id):
    try:
        return media[media_type][media_id]
    except KeyError:
        return "Медиа не найдено"

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())