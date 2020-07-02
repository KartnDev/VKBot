from Src.Controllers.ControllerActioner import ControllerAction


class TwitchIsAliveController:
    def __init__(self, action: ControllerAction):
        self.action = action

    async def invoke_when_channel_is_online(self, channel: str):
        pass