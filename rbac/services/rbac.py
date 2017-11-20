from django.conf import settings


def init_permission(request, user):
    """
    初始化权限信息，并添加到session
    """
    permission_list = user.role.all().values(
        "permission__title",
        "permission__url",
        "permission__code",
        "permission__group_menu_id",
        "permission__group_id",
        "permission__group__title",
        "permission__group__menu_id",
        "permission__group__menu__title",
    ).distinct()

    # 分类处理权限信息
    group_dict = {}
    menu_dict = {}
    for item in permission_list:
        """
权限组字典结构

{
    组ID: {
        "code": ["", "", "", ...]
        "urls": ["url", "url2", "url3", ...]
    }
    ...
}
        """
        group_dict.setdefault(item["permission__group_id"], {}).setdefault("code", []).append(item["permission__code"])
        group_dict.setdefault(item["permission__group_id"], {}).setdefault("urls", []).append(item["permission__url"])

        """
菜单字典结构

{
    组ID: {
        "menu": {"url": 组内菜单url, "menu_title": "所属组名", "menu_title": "所属菜单名", "menu_id": "所属菜单ID"},
        "urls": ["组url", "组url2", "组url3", ...]
    }
    ...
}
        """
        # tpd = menu_dict.setdefault(item["permission__group__menu_id"], {})
        tpd = menu_dict.setdefault(item["permission__group_id"], {})
        tpd.setdefault("urls", []).append(item["permission__url"])
        # 给每个组设置组内菜单
        if not item["permission__group_menu_id"]:
            tpd.setdefault("menu", {"title": item["permission__title"], "url": item["permission__url"],
                                    "group_title": item["permission__group__title"],
                                    "menu_title": item["permission__group__menu__title"],
                                    "menu_id": item["permission__group__menu_id"]})
    request.session[settings.PERMISSION_GROUP] = group_dict
    request.session[settings.PERMISSION_MENU] = menu_dict

