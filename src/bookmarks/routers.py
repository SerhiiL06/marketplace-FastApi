# @users_router.get("/bookmark/add/{adv_id}", tags=["bookmark"])
# async def add_to_bookmark(user: current_user, adv_id: int = Path(gt=0)):
#     return bookmark.add_delete_bookmark(user, adv_id)


# @users_router.get(
#     "/bookmakr/my", tags=["bookmark"], response_model=list[DefaultAdvertisementScheme]
# )
# async def get_bookmarks(db: db_depends, user: current_user):
#     return (
#         db.query(Advertisements)
#         .join(Bookmark, Advertisements.id == Bookmark.adv_id)
#         .filter(Bookmark.user_id == user.get("user_id"))
#         .order_by(desc(Bookmark.created))
#         .all()
#     )


# @users_router.post("/add-bookmark", tags=["session"])
# async def add_to_bookmark(adv_id: int, request: Request, response: Response):
#     session = BookmarkSession()

#     return session.add_to_bookmark(adv_id, request, response)


# @users_router.get(
#     "/my-list-bookmark",
#     tags=["session"],
#     response_model=list[DefaultAdvertisementScheme],
# )
# async def bookmark_list(request: Request, db: db_depends):
#     session = BookmarkSession()

#     return session.get_bookmark_list(request, db)
