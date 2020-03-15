from vk_bot.types.vk_base_object import VKBaseObject
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from vk_bot.vk_bot import VKBot


class Message(VKBaseObject):
    def __init__(self,
                 id: int = None,
                 date: int = None,
                 peer_id: int = None,
                 from_id: int = None,
                 text: str = None,
                 random_id: int = None,
                 ref: str = None,
                 ref_source: str = None,
                 attachments: List[object] = None,
                 important: bool = None,
                 geo: object = None,
                 payload: str = None,
                 keyboard: object = None,
                 fwd_messages: List['Message'] = None,
                 reply_message: 'Message' = None,
                 action: object = None,
                 out: int = None,
                 conversation_message_id: int = None,
                 is_hidden: bool = None,
                 client: 'VKBot' = None):
        self.id = id
        self.date = date
        self.peer_id = peer_id
        self.from_id = from_id
        self.text = text
        self.random_id = random_id
        self.ref = ref
        self.ref_source = ref_source
        self.attachments = attachments
        self.important = important
        self.geo = geo
        self.payload = payload
        self.keyboard = keyboard
        self.fwd_messages = fwd_messages
        self.reply_message = reply_message
        self.action = action
        self.out = out
        self.conversation_message_id = conversation_message_id

        self.client = client

    @classmethod
    def de_dict(cls, data: dict, client: 'VKBot' = None):
        if not data:
            return None

        # TODO: attachments
        # TODO: geo
        # TODO: keyboard
        data['fwd_messages'] = Message.de_list(data.get('fwd_messages'), client)
        data['reply_message'] = Message.de_dict(data.get('reply_message'), client)
        # TODO: action

        return cls(**data, client=client)

    def reply(self, *args, **kwargs):
        return self.client.messages_send(reply_to=self.id, peer_id=self.peer_id, *args, **kwargs)
