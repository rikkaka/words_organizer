import os
scriptExecutedSignal = True


# 禁用IP代理
os.environ['no_proxy'] = '*' 
if not scriptExecutedSignal:
    print('正在安装依赖包:requests、argparse、bs4、lxml......')
    os.system('sudo apt-get install python3-pip > /dev/null')
    os.system('sudo -H pip3 install requests argparse  bs4 lxml > /dev/null')

import requests
# import argparse
import json
from bs4 import BeautifulSoup




#@@@@@@@@@@@@@@@@@@@@@@@@@@@@ function 目录 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# getUserInput
# openDictFile
# checkLocalWords
# downloadWordTranslation
# printLookupResult
# createBashFile
# createOfflineDict
# changeCurrentFileContent
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# 功能：以参数形式从命令行获取用户要查询的词汇
# 输出：词汇（字符串）
# def getUserInput():
#     # 使用argparse根据获取用户的输入用于创建url link
#     parser = argparse.ArgumentParser(description='Process some strings.')
#     parser.add_argument('strings', metavar='N', type=str, nargs='+',
#                         help='an integer for the accumulator')
#     args = parser.parse_args()
#     userInput = ''
#     for each in args.strings:
#         userInput+= each +' '
#     return userInput.strip()

# 功能：打开本地词库的json文件
# 输入：本地词库路径
# 输出：本地词库（列表）
def openDictFile(localDictPath):
    try:
        with open(localDictPath,'r') as f:
            localDictLib = json.load(f)
    except:
        localDictLib = []
    return localDictLib
# 功能：检查要查询的词语是否包含在本地词库中
# 输入：(本地词库,用户输入） ————>(list,string)
# 返回：该词目本地释义内容（字典） 或者 返回None
def checkLocalWords(localDictLib,userInput):
    #判断用户要查询的词汇是否存在于本地
    for each in localDictLib:
        if each['word']==userInput:
            return each
    return None
    
# 功能：从有道词典的网页上爬取指定词汇的翻译内容
# 输入：词语条目
# 返回：该词语相关的翻译内容（字典）
def downloadWordTranslation(userInput):
    ####################################################
    link = "https://www.youdao.com/w/"+userInput
    response = requests.get(link) #get page data from server, block redirects
    sourceCode = response.content #get string of source code from response
    
    #用beautiful soup中的css选择器方法爬取数据
    soup = BeautifulSoup(sourceCode,'lxml')
    #-以下爬取条目均为标签格式的列表
    wordTranslation = soup.select('#phrsListTab li')
    internetTranslation = soup.select('#tWebTrans .wt-container .title>span')
    possibleWords = soup.select('.typo-rel')
    pronounce = soup.select('.pronounce .phonetic')
    longPhraseTrans = soup.select('#fanyiToggle p:nth-child(2)')
    wordTranslation_ch_to_en = soup.select('#results-contents #phrsListTab .wordGroup')
    internetShortPhrase = soup.select('#webTransToggle .wordGroup')
    #清楚多余空格
    word = {
        'word': userInput.strip(),
        'pronounce':getTextsFromTags(pronounce),
        'wordTranslation':getTextsFromTags(wordTranslation),
        'internetTranslation': getTextsFromTags(internetTranslation),
        'possibleWords': getTextsFromTags(possibleWords),
        'longPhraseTrans':getTextsFromTags(longPhraseTrans),
        'wordTranslation_ch_to_en': getTextsFromTags(wordTranslation_ch_to_en),
        'internetShortPhrase':getTextsFromTags(internetShortPhrase)
    }
    return word
# 功能：将标签类型列表转换成字符串类型列表
# 输入：标签列表
# 输出：字符串列表
def getTextsFromTags(tagObjList):
    textsList = []
    for each in tagObjList:
        text = each.get_text().strip().replace('\n','').replace('   ','')
        textsList.append(text)
    return textsList
    

# 功能：打印出用户查询词汇的相关翻译内容
# 输入：翻译内容（字典）
def printLookupResult(wordDict):
    word = wordDict
    # print(' '*20+'-'*5+' \033[97m'+word['word']+' \033[0m'+'-'*5)
    s = ''
    # if word['pronounce']:
    #     s += ("%s发音:%s" % ('',''))
    #     try:
    #         s+=("英:%s%s%s     美:%s%s%s" % ('',word['pronounce'][0],'','',word['pronounce'][1],''))+'\n'
    #     except:
    #         s+=("英:%s%s%s     美:%s%s%s" % ('',word['pronounce'][0],'','',word['pronounce'][0],''))+'\n'
    if word['wordTranslation']:
        # s+=("%s翻译:%s" % ('',''))
        for each in word['wordTranslation']:
            s+=('%s%s%s' % ('',each,''))+'\n'
    # if word['internetTranslation']:
    #     print("%s网络释义：%s" % ('\033[95m','\033[0m'))
    #     for each in word['internetTranslation']:
    #         print('========= %s%s%s' % ('\033[93m',each,'\033[0m'))
    if word['possibleWords']:
        s+=("%s您要找的是不是:%s" % ('',''))
        for each in word['possibleWords']:
            s+=('%s%s%s' % ('',each,''))+'\n'
    if 'longPhraseTrans' in word:
        if word['longPhraseTrans']:
            s+=("%s长句翻译：%s" % ('',''))
            for each in word['longPhraseTrans']:
                s+=('%s%s%s' % ('',each,''))+'\n'
    if 'wordTranslation_ch_to_en' in word:
        if word['wordTranslation_ch_to_en']:
            s+=("%s翻译(汉译英)：%s" % ('',''))
            for each in word['wordTranslation_ch_to_en']:
                s+=('========= %s%s%s' % ('',each,''))+'\n'
    #以下代码用于显示：【网络短语】 的条目，由于显示内容过多，所以注释掉这一条
    # if 'internetShortPhrase' in word:
    #     if word['internetShortPhrase']:
    #         print("%s网络短语：%s" % ('\033[95m','\033[0m'))
    #         stopPoint = 1
    #         for each in word['internetShortPhrase']:
    #             print('========= %s%s%s' % ('\033[93m',each,'\033[0m'))
    #             stopPoint += 1
    #             if stopPoint>3:
    #                 break

    return s




# 功能：创建bash文件，用于在命令行直接唤出程序
# 输入：(bash文件路径，bash文件内容)
def createBashFile(bashDir,bashContent):
    with open(bashDir,'w') as f:
        f.write(bashContent)
    os.system('chmod +x '+bashDir)

# 功能：创建离线词典库
# 输入：（本地纯英文词汇表，离线词典路径）
def createOfflineDict(pureEngWordsPath,localDictPath):
    localDictLib = []
    localDictLib2 = openDictFile(localDictPath)
    with open(pureEngWordsPath,'r') as f:
        while True:
            data = f.readline()
            data = data.strip()
            localTranslationItem = checkLocalWords(localDictLib2,data)
            if localTranslationItem:
                # printLookupResult(localTranslationItem)
                continue
            else:
                translationItem = downloadWordTranslation(data)
            if translationItem['word'] == '':
                print('网络词典本地化完成！')
                localDictLib.extend(localDictLib2)
                break
            printLookupResult(translationItem)
            localDictLib.append(translationItem)
    with open(localDictPath,'w') as f:
        json.dump(localDictLib,f)
    os.system('chmod 777 '+localDictPath)

# 功能：改变当前脚本文件的执行标记（scriptExecutedSignal）的值，
#       用来区分此脚本是否是第一次执行，
#       第一次执行则会开始下载离线词典库，并创建/usr/bin/bash文件,
#       之后将正常查询词目
# 输入：此脚本文件的路径
def changeCurrentFileContent(curFilePath):
    with open(curFilePath,'r') as f:
        currentFileContent = f.read()
    currentFileContent = currentFileContent.replace('scriptExecutedSignal = True','scriptExecutedSignal = True',2)
    with open(curFilePath,'w') as f:
        f.write(currentFileContent)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 主程序 main @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

cwd = os.getcwd()
dictFileName = 'dict.json'
localDictPath = cwd + '/' + dictFileName
# /usr/bin/bash 路径
bashDir = '/usr/bin/d'
# /usr/bin/bash content
bashContent = 'save_path=$PWD\n'+'cd '+cwd+'\n'+'python3 dict.py $*\n'+'cd $save_path'
curFileName = 'dict.py'
curFilePath = cwd + '/' + curFileName


def translate(word):
    r=''
    if scriptExecutedSignal:
        localDictLib = openDictFile(localDictPath)
        userInput = word
        localTranslationItem = checkLocalWords(localDictLib,userInput)
        if localTranslationItem:
            r=printLookupResult(localTranslationItem)
            # print('\033[90m@本地条目@\033[0m')
        else:
            translationItem = downloadWordTranslation(userInput)
            r=printLookupResult(translationItem)
            #储存查询过的条目到本地json文件
            localDictLib.append(translationItem)
            with open('dict.json','w') as f:
                json.dump(localDictLib,f)

    else:
        userinput = input('请输入需要添加到本地词典的纯英文词汇列表文件名，如不需要请按回车继续：')

        if userinput != '':
            pureEngWordsPath = cwd + '/' + userinput
            createOfflineDict(pureEngWordsPath,localDictPath)
        createBashFile(bashDir,bashContent)
        changeCurrentFileContent(curFilePath)
            
    return r

# print(translate('hazard'))
# #以下代码块可查询当前使用的IP地址
# myIPRequest = requests.get('http://whois.pconline.com.cn/')
# ipPageSourceCode = myIPRequest.content
# myIPHtmlElem = html.document_fromstring(ipPageSourceCode)
# myIP = myIPHtmlElem.xpath("//body/text()[4]")
# print(myIP)

#===================打印字体着色可用列表=============
# Red = '\033[91m'
# Green = '\033[92m'
# Blue = '\033[94m'
# Cyan = '\033[96m'
# White = '\033[97m'
# Yellow = '\033[93m'
# Magenta = '\033[95m'
# Grey = '\033[90m'
# Black = '\033[90m'
# Default = '\033[99m'
# '\033[0m' 结尾用于恢复正常的
