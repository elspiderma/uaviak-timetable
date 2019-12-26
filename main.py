import json

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll

from command.group_timetable import TimetableGroupCommand
from command.teacher_timetable import TimetableTeacherCommand
from command.not_found import NotFoundCommand
import config

HANDLERS = [TimetableGroupCommand, TimetableTeacherCommand, NotFoundCommand]

def proc_event(vk_api, event):
    if event is None:
        return None

    for i in HANDLERS:
        handler = i(vk_api) 
        if handler.check(event):
            handler.run(event)
            break

def long_poll():
    vk = VkApi(token=config.TOKEN, api_version='5.103')
    vk_api = vk.get_api()

    vk_long_poll = VkBotLongPoll(vk=vk, group_id=config.GROUP_ID, wait=90)
    for event in vk_long_poll.listen():
        event_obj = event.obj
        try:
            proc_event(vk_api, event_obj)
        except Exception as e:
            print(e)
        
if __name__ == '__main__':
    long_poll()


