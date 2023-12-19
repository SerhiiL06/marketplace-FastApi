class AdvIDNotExists(Exception):
    def __init__(self, obj_id) -> None:
        self.obj_id = obj_id
