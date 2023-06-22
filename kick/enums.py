from enum import Enum

__all__ = ("ChatroomChatMode",)


class ChatroomChatMode(Enum):
    """
    An enum containing possble chatroom chat mode values.

    Attributes
    -----------
    public: `ChatroomChatMode`
        The public value
    privet: `ChatroomChatMode`
        The privet value
    """

    public = "public"
    privet = "privet"
