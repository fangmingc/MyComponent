from re import match

from django.conf import settings
from django.shortcuts import redirect, HttpResponse


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):
    """
    权限管理中间件

    1. url白名单认证
    2. 登录认证
    3. 权限认证、处理权限组
    """

    def process_request(self, request):
        current_url = request.path_info

        # url白名单认证
        for url in settings.VALID_URLS:
            if match("^{0}$".format(url), current_url):
                return None

        # 登录认证
        if not request.session.get(settings.PERMISSION_GROUP):
            return redirect("/login/")

        # 权限认证、处理权限组
        for k, group in request.session.get(settings.PERMISSION_GROUP).items():
            for url in group["urls"]:
                print(url, current_url)
                if match("^{0}$".format(url), current_url):
                    request.code_list = group["code"]
                    return None
        return HttpResponse("无权访问")


