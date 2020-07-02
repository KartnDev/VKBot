import asyncio

from Src.Controllers.ControllerActioner import ControllerAction
from Src.Controllers.TwitchController.TwitchIsAliveController import TwitchIsAliveController


class TwitchEventScheduler:

    def __init__(self, action: ControllerAction, handle_channels: list[str]):
        self._handle_channels = handle_channels
        self._action = action
        self._twitch_action = self._action.twitch_action
        self._twitch_controller = TwitchIsAliveController(action)

    async def twitch_annotate_all(self, time_sleep: int):
        """

        Args:
            time_sleep (sec): time to get new request to check is channel alive
        """
        while True:
            for item in self._handle_channels:
                if self._twitch_action.is_channel_online(item):
                    self._twitch_controller.invoke_when_channel_is_online(item)
            await asyncio.sleep(time_sleep)
