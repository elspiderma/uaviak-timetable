from db.structures import Teacher


class TestTeacher:
    def test_from_record(self):
        id_ = 1
        short_name = 'Антропова О.А.'
        full_name = 'Антропова Ольга Александровна'

        teacher = Teacher.from_record({
            'id': id_,
            'short_name': short_name,
            'full_name': full_name
        })

        assert teacher.id == id_
        assert teacher.short_name == short_name
        assert teacher.full_name == full_name
