class UnconfirmedPostsSerializerMixin:
    """
    Mixin which allows staff users to edit
    some fields of unconfirmed posts.
    """
    staff_edit = False
    staff_fields = []  # fields which staff can edit

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.staff_edit is True:
            read_only_fields = []
            for field in self.Meta.fields:
                if field not in self.staff_fields:
                    read_only_fields.append(field)
            self.Meta.read_only_fields = read_only_fields

            self.Meta.fields.extend(self.staff_fields)
