import json
from urllib.parse import urlencode
from django.shortcuts import render
from django.http import HttpResponse
from form_parser import FormParser
import http.cookiejar as cookielib
import urllib.request as urllib2
from urllib.parse import urlparse
from django import forms


class UserForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


def index(request):
    return render(request, 'catalog/list.html')


def auth_user(email, password, app_id, scope, opener):
    response = opener.open(
        "https://oauth.vk.com/oauth/authorize?" + \
        "redirect_uri=https://oauth.vk.com/blank.html&response_type=token&" + \
        "client_id=%s&scope=%s&display=wap" % (app_id, ",".join(scope))
    )
    html = response.read()
    # Find and parse user authorization form
    parser = FormParser()
    parser.feed(str(html))
    parser.close()
    if not parser.form_parsed or parser.url is None:
        raise RuntimeError("Something wrong with a parser. Unable parse VK authorization form.")
    elif "pass" not in parser.params or \
            "email" not in parser.params:
        raise RuntimeError("You already auth.")
    parser.params["email"] = email
    parser.params["pass"] = password
    print('pars url : ',  parser.url)
    if parser.method == "post":
        response = opener.open(parser.url, urlencode(parser.params).encode("utf-8"))  # INPUT
        print('eeeeeboy')
        print(response.geturl())
    else:
        raise NotImplementedError("Method '%s'" % parser.params.method % " for user authorization form \
                    submission is currently not supported. Please implement it if there is a need.")
    return response.read(), response.geturl()


def give_access(html, opener):
    parser = FormParser()
    parser.feed(str(html))
    parser.close()

    if not parser.form_parsed or parser.url is None:
        raise RuntimeError("Something wrong with a parser. Unable parse VK application authorization form.")

    if parser.method == "post":
        response = opener.open(parser.url, urlencode(parser.params).encode("utf-8"))
    else:
        raise NotImplementedError("Form method '%s'" % parser.params.method + "for application authorization \
                form submission is currently not supported. Please implement it if there is a need.")
    return response.geturl()


def get_need_dates(username, password):
    app_id = 7561984
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
        urllib2.HTTPRedirectHandler())
    html, url = auth_user(email=username, password=password, app_id=app_id, scope=['friends', 'account'],
                          opener=opener)
    print(url)
    if urlparse(url).path != "/blank.html":
        url = give_access(html, opener)

    def split_key_value(kv_pair):
        kv = kv_pair.split("=")
        return kv[0], kv[1]
    print('ddssssd^     ', urlparse(url).fragment.split("&"))
    token = urlparse(url).fragment.split("&")[0].split("=")[1]
    id = urlparse(url).fragment.split("&")[2].split("=")[1]
    print(token, id)
    # answer = dict(split_key_value(kv_pair) for kv_pair in urlparse(url).fragment.split("&"))
    return id, token


def call_api(method, params, token):
    if isinstance(params, list):
        params_list = [kv for kv in params]
    elif isinstance(params, dict):
        params_list = params.items()
    else:
        params_list = [params]
    params_list.append(("access_token", token))
    url = "https://api.vk.com/method/%s?%s&v=5.52" % (method, urlencode(params_list))
    return json.loads(urllib2.urlopen(url).read())["response"]


def get_friends(user_id, token):
    return call_api("friends.get", [("uid", user_id), ('fields', ' nickname')], token)


def get_info(user_id, token):
    return call_api("account.getProfileInfo", [("uid", user_id)], token)

def get_pass(request):
    email = '89817882901'
    password = 'RAFAFAfa290911'
    user_id, token = get_need_dates(email, password)
    account_info = 'Имя пользователя:<br />' + get_info(user_id, token)['first_name'] + ' ' + get_info(user_id, token)[
        'last_name'] + '<br />'
    friend_dist = get_friends(user_id, token)
    count = 0
    friends_info = '<br />Список друзей: <br />'
    for field in friend_dist['items']:
        if count == 5:
            break
        friends_info += field['first_name'] + ' ' + field['last_name'] + ' ' + '<br />'
        count += 1
    return HttpResponse(account_info + friends_info)




def submit(request):
    # if request.method == "POST":
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     user_id, token = get_need_dates(email, password)
    #     account_info = 'Имя пользователя:<br />' + get_info(user_id, token)['first_name'] + ' ' + get_info(user_id, token)['last_name'] + '<br />'
    #     friend_dist = get_friends(user_id, token)
    #     count = 0
    #     friends_info = '<br />Список друзей: <br />'
    #     for field in friend_dist['items']:
    #         if count == 5:
    #             break
    #         friends_info += field['first_name'] + ' ' + field['last_name'] + ' ' + '<br />'
    #         count += 1
    #     return HttpResponse(account_info + friends_info)
    # else:
        userform = UserForm()
        return render(request, "catalog/pass_email.html", {"form": userform})
