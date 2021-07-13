import datetime
from db.structures import Departaments, Timetable


class TestTimetable:
    def test_from_record(self):
        id_ = 1
        additional_info = 'TestInfo'
        date = datetime.date(2020, 2, 2)
        departament = Departaments.FILL_TIME

        timetable = Timetable.from_record({
            'id': id_,
            'additional_info': additional_info,
            'date': date,
            'departament': departament.value
        })

        assert timetable.id == id_
        assert timetable.additional_info == additional_info
        assert timetable.date == date
        assert timetable.departament == departament
