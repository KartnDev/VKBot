import asyncio

from Src.Controllers.ControllerActioner import ControllerAction
from Src.Controllers.TwitchController.TwitchIsAliveController import TwitchIsAliveController

from collections import deque


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

        is_stream_deq = deque(self._handle_channels)
        down_to_alive = []

        while True:
            for item in range(len(is_stream_deq)):
                now_channel = is_stream_deq.popleft()
                if self._twitch_action.is_channel_online(now_channel):
                    await self._twitch_controller.invoke_when_channel_is_online(now_channel)
                    down_to_alive.append(now_channel)
                else:
                    is_stream_deq.append(now_channel)

                for channel in down_to_alive:
                    if not self._twitch_action.is_channel_online(channel):
                        is_stream_deq.append(channel)
                        down_to_alive.remove(channel)
            await asyncio.sleep(time_sleep)

