from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

#wev clawer
import selenium.webdriver
from bs4 import BeautifulSoup
import re
import os
import urllib.request
import json
from urllib.parse import quote
import time

import socket
from selenium.webdriver.common.keys import Keys
import threading
#
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
# csrf pass
from django.views.decorators.csrf import csrf_exempt


def index(request):
    global driver
    try:
        if driver :
            handles = driver.window_handles
            while len(handles) > 10:
                driver.switch_to_window(handles[0])
                driver.close()
                driver.switch_to_window(handles[-1])
                handles = driver.window_handles
    except:
        driver = selenium.webdriver.Chrome()
        driver.set_window_position(0,0) #瀏覽器位置
        driver.set_window_size(1280,720) #瀏覽器大小
        driver.get('https://twitter.com/maaya_taso/')
        driver.implicitly_wait(30)
        UserName= ('ncy906302@gmail.com')
        UserPass= ('mkoij2000')
        driver.find_element_by_name('session[username_or_email]').send_keys(UserName)
        driver.find_element_by_name('session[password]').send_keys(UserPass)
        driver.find_element_by_name('session[password]').send_keys(Keys.ENTER)
    return render(request, 'albumApp/index.html')

@csrf_exempt
def upUrl(request):
    try:
        reg = 'https://twitter.com/(.*?)/'
        reg = re.compile(reg)
        url_receive = request.POST['url']+"/"
        _id = re.findall(reg,url_receive)
        url = 'https://twitter.com/' + _id[0] + '/media'
        print(url)
        global driver
        js='window.open("'+ url +'");'
        driver.execute_script(js)
        handle = driver.window_handles[-1]
        driver.switch_to_window(handle)
        title = str(driver.title)
        content = {'handle':handle,'title':title }
        return render(request, 'albumApp/main.html' ,content)
    except:
        return HttpResponse('the twitter url maybe not correct')

@csrf_exempt
def jq(request):
    global driver
    print(request.POST['name'])
    driver.switch_to_window(request.POST['name'])
    soup = BeautifulSoup(driver.page_source,'html.parser')
    img_list=[]
    date_list=[]
    month_list=[]
    tweet=soup.find_all('',{'data-item-type' : 'tweet'})
    for i in range(len(tweet)):
        html =str(tweet[i])

        reg = 'img.*?data-aria-label-part.*?(https.*?)"'
        reg = re.compile(reg)

        date_reg = 'class="tweet-timestamp.*?title="(.*?)"'
        date_reg = re.compile(date_reg)

        month_reg = '- .*?(.*?)月.*?日'
        month_reg = re.compile(month_reg)

        img = re.findall(reg,html)
        date = re.findall(date_reg,html)
        month = re.findall(month_reg,date[0])
        img_list.append(img)
        date_list.append(date)
        month_list.append(month)
    global content
    content = {'img_list':img_list , 'date_list':date_list , 'month_list':month_list }
    idx = len(date_list)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    return HttpResponse(json.dumps(content))


@csrf_exempt
def search(request):
    try:
        global driver
        print(request.POST['key'])
        keyword = request.POST['key']
        key = quote(keyword)
        url = 'https://twitter.com/search?f=images&q='+key
        js='window.open("'+ url +'");'
        driver.execute_script(js)
        time.sleep(1)
        handle = driver.window_handles[-1]
        driver.switch_to_window(handle)
        
        soup = BeautifulSoup(driver.page_source,'html.parser')
        tweet = soup.find_all("span", attrs={"data-component-context": "tweet"})

        img_list = []
        name_list = []
        account_list = []
        for i in tweet:
            html = str(i)
            
            img_reg = r'data-url="(.*?.jpg)"'
            img = re.findall(img_reg,html)
            img_list.append(img)
            
            name_reg = r'data-name="(.*?)"'
            name = re.findall(name_reg,html)
            name_list.append(name)
            
            account_reg = r'data-screen-name="(.*?)"'
            account = re.findall(account_reg,html)
            account_list.append(account)
        global content
        content = {'content':{'img_list':img_list , 'name_list':name_list , 'account_list':account_list}}

        return render(request, 'albumApp/index.html',content)
    except:
        return HttpResponse('error keyword')


