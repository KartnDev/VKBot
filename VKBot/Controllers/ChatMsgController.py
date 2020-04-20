from BotFramework.SDK import HandleMessage, RequiredLvl


class ChatMsgController:

    def __init__(self, VkAction):


    @RequiredLvl(lvl=10)
    @HandleMessage(msg="!arbuz")
    def handle_name(self, VkActioner):
        VkActioner.sendMessage("Hyi")


