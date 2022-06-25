import asyncio
import typing
import aiogram
import Constants.messages as messages
from Services.weather_service import WeatherService
from typing import NamedTuple
from typing import List
from Errors.auth_error import AuthError
from Errors.location_not_found import LocationNotFound
from aiogram.utils.exceptions import ValidationError

TelegramAuthData = NamedTuple("TelegramAuthData", [("api_id", int), ("api_hash", str), ("bot_token", str)])
CommandInfo = NamedTuple("CommandInfo", [("command", str), ("function", typing.Callable)])


class BotService:
    def __init__(self, bot_token: str, weather_service: WeatherService):
        try:
            self._api = aiogram.Bot(token=bot_token)
        except ValidationError:
            raise AuthError("Telegram Bot API")
        self._weather_service = weather_service
        self.BOT_COMMANDS = [
            CommandInfo("start", self._on_start_command),
            CommandInfo("show", self._on_show_command)
        ]
        self._dispatcher = aiogram.Dispatcher(self._api)
        self._dispatcher.register_message_handler(self._on_message)
        self._loop = asyncio.get_event_loop()


    def run(self):
        aiogram.executor.start_polling(self._dispatcher, skip_updates=True, loop=self._loop)


    @property
    def loop(self):
        return self._loop


    async def _on_message(self, event: aiogram.types.Message):
        try:
            is_command = "/" in event.text
            if not is_command:
                return
            content = event.text.replace("/", "").split()
            name = content[0]
            content.pop(0)
            args = content
            for command in self.BOT_COMMANDS:
                if name == command.command:
                    await command.function(event, args)
                    break
        except Exception as error:
            await self._api.send_message(event.from_id, messages.REQUEST_ERROR)
            raise error


    async def _on_start_command(self, event: aiogram.types.Message, args: List[str]):
        await self._api.send_message(event.from_id, messages.START)


    async def _on_show_command(self, event: aiogram.types.Message, args: List[str]):
        if len(args) == 0:
            message = messages.NO_CITY
        else:
            city = ""
            for arg in args:
                city += f"{arg} "
            try:
                weather = self._weather_service.get_weather(city)
                message = messages.Formatter.weather(weather)
            except LocationNotFound:
                message = messages.LOCATION_NOT_FOUND
        await self._api.send_message(event.from_id, message)
