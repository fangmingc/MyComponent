from re import match

from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag("menu.html")
def menu_html(request):
    """
    自动生成菜单HTML
    """
    for k, group in request.session.get(settings.PERMISSION_MENU).items():
        for url in group["urls"]:
            if match("^{0}$".format(url), request.path_info):
                group["menu"]["active"] = True
                break
        else:
            continue
        break
    """
    # 抛出异常法
    class TempError(Exception):
        pass
    try:
        for k, group in request.session.get(settings.PERMISSION_MENU).items():
            for url in group["urls"]:
                if match("^{0}$".format(url), request.path_info):
                    group["menu"]["active"] = True
                    raise TempError
    except TempError:
        pass
    # 函数法
    def temp(temp_dict, current_url):
        for k, group in temp_dict:
            for url in group["urls"]:
                if match("^{0}$".format(url), current_url):
                    group["menu"]["active"] = True
                    return
    temp()
    """
    menu_dict = {}
    for k, group in request.session.get(settings.PERMISSION_MENU).items():
        """
菜单字典结构

{
    菜单ID: {
        "title": 菜单名,
        "active": 是否默认展开,
        "children": [
            {"title": 组内菜单名, "url": 组内菜单url, "active": 是否默认选中},
            ...
        ]
    }
    ...
}
        """
        tpd = menu_dict.setdefault(group["menu"]["menu_id"], {})
        tpd.setdefault("title", group["menu"]["menu_title"])
        if group["menu"].get("active"):
            tpd.setdefault("active", True)
        tpd.setdefault("children", []).append({
            "title": group["menu"]["title"], "url": group["menu"]["url"], "active": group["menu"].get("active", False)
        })

    return {"menu_dict": menu_dict}
