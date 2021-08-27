from db.structures import Group


class TestGroup:
    def test_from_record(self):
        id_ = 1
        number = '19ис-1'

        group = Group.from_record({
            'id': id_,
            'number': number
        })

        assert group.id == id_
        assert group.number == number
