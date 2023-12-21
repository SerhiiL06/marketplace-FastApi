from database.depends import db_depends
from src.advertisements.models import Advertisements
from fastapi import Request, Response, Cookie
import json
from src.advertisements.exceptions import AdvIDNotExists


class BookmarkSession:
    def add_to_bookmark(self, adv_id, request, response):
        db = db_depends()
        check_adv = (
            db.query(Advertisements).filter(Advertisements.id == adv_id).one_or_none()
        )

        if check_adv is None:
            raise AdvIDNotExists(adv_id)

        bookmark_list = request.cookies.get("bookmark_list")

        if bookmark_list is None:
            bookmark_list = []
        else:
            bookmark_list = json.loads(bookmark_list)

        if adv_id in bookmark_list:
            bookmark_list.remove(adv_id)
            response.set_cookie("bookmark_list", bookmark_list)
        else:
            bookmark_list.append(adv_id)
            response.set_cookie("bookmark_list", bookmark_list)

    def get_bookmark_list(self, request, db):
        list_of_bookmarks = json.loads(request.cookies.get("bookmark_list"))

        if list_of_bookmarks is None:
            return {"list": "None"}

        return (
            db.query(Advertisements)
            .filter((Advertisements.id).in_(list_of_bookmarks))
            .all()
        )
