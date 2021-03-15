import mechanicalsoup
import pandas as pd
import concurrent.futures
df = pd.read_csv('second_half_link.csv')
urls = df.loc[:,'courselink']
urls = urls.dropna()
def login():
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://app.adventus.io/admin/login")
    browser.select_form('form[action="https://app.adventus.io/admin/login"]')
    browser["email"] = "hello@acemyprep.com"
    browser["password"] = "ace_my_prep_2020"
    browser.submit_selected()
    return browser
browser = login()
dic_col = {'course_link':[],
           'course_level': [],
           'Application_Fee' : [],
           'intake': [],
           'url':[]
          }
df = pd.DataFrame(dic_col)
count=0
for url in urls:
    count+=1
    dic={}
    try:
        browser.open(url)
        soup = browser.page
        try:
            dic['url']=url
        except:
            pass
        try:
            dic['course_link'] = soup.find('a', text='Go to course page')['href']
        except:
            pass
        try:
            dic['course_level'] = soup.find('dt', text='Level').findNext('dd').text
        except:
            pass
        try:
            dic['Application_Fee'] = soup.find('dt', text='Application Fee').findNext('dd').text.strip(' ').strip('\n')
        except:
            pass

        try:
            course_date_tab = soup.find('div', id='tab-dates')
            thead = course_date_tab.find('thead')
            th = [i.text for i in thead.find_all('th')]
            startdate_index = th.index('Term Start')
            tbody = course_date_tab.find('tbody')
            tr = tbody.find_all('tr')
            td =[]
            for i in tr:
                try:
                    td.append(i.find_all('td')[startdate_index].text.split('-')[1])
                except:
                    pass
            dic['intake'] = list( dict.fromkeys(td) )
        except:
            pass
        df = df.append(dic, ignore_index = True)
        print(count)
    except:
        continue
df.to_csv("second_half_info.csv")
df.to_excel("second_half_info.xlsx")