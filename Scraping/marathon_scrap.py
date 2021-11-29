################### MARATHON SCRAP #####################
# @rawmnr v1.1

## IMPORT LIBRARIES

import time
from bs4 import BeautifulSoup
from gazpacho import get, Soup
import pandas as pd
import pickle
from alive_progress import alive_bar
from progress.bar import Bar
import itertools


# class architecture
# Mararthon -> Event -> Athlete

class Marathon:
    def __init__(self, location):
        self.location = location


class Race(Marathon):
    def __init__(self, year, sex, location):
        # Params
        self.year = year
        self.sex = sex
        self.date = ''
        self.yearindex = 0
        # Weather
        self.datetime = ''
        self.tempmax = 0
        self.tempmin = 0
        self.tempmoy = 0
        self.humidity = 0
        self.precip = 0
        self.windspeed = 0
        self.winddir = 0
        self.cloudcover = 0
        self.conditions = ''
        self.description = ''
        # Import Marathon
        Marathon.__init__(self, location)

    def geteventdate(self):
        dates = ['1996-10-20', '1997-10-19', '1998-10-11', '1999-10-24', '2000-10-22', '2001-10-07', '2002-10-13',
                 '2003-10-12',
                 '2004-10-10', '2005-10-09', '2006-10-22', '2007-10-06', '2008-10-12', '2009-10-11', '2010-10-10',
                 '2011-10-09',
                 '2012-10-07', '2013-10-13', '2014-10-12', '2015-10-11', '2016-10-09', '2017-10-08', '2018-10-07',
                 '2019-10-13']
        years = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
                 2013, 2014, 2015, 2016, 2017, 2018, 2019]

        for i in range(len(years)):
            if years[i] == self.year:
                self.date = dates[i]

    def yearindex(self):
        self.yearindex = self.year - 1996
        return self.yearindex

    def getweather(self, location):
        if location == 'Chicago':
            with open('chicagoweather2.pkl', 'rb') as f:
                weatherdata = pickle.load(f)

        index = Race.yearindex(self)

        # day data
        self.datetime = weatherdata[index]['days'][0]['datetime']
        ## temp
        self.tempmax = weatherdata[index]['days'][0]['tempmax']
        self.tempmin = weatherdata[index]['days'][0]['tempmin']
        self.tempmoy = weatherdata[index]['days'][0]['temp']
        ## humidity
        self.humidity = weatherdata[index]['days'][0]['humidity']
        self.precip = weatherdata[index]['days'][0]['precip']
        ## wind
        self.windspeed = weatherdata[index]['days'][0]['windspeed']
        self.winddir = weatherdata[index]['days'][0]['winddir']
        ## cloud
        self.cloudcover = weatherdata[index]['days'][0]['cloudcover']
        self.conditions = weatherdata[index]['days'][0]['conditions']
        self.description = weatherdata[index]['days'][0]['description']


class Scrap(Race):
    def __init__(self, year, sex, location):
        self.url = ''
        self.soup = ''
        self.lines = []
        Race.__init__(self, year, sex, location)

    def chipagegen(self, page, num):
        eventcode = ''

        years = [1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
                 2013, 2014, 2015, 2016, 2017, 2018, 2019]
        eventcodes = ['MAR_9999990E9A9236000000006F',
                      'MAR_9999990E9A9236000000006E',
                      'MAR_9999990E9A9236000000006D',
                      'MAR_9999990E9A9236000000006C',
                      'MAR_9999990E9A9236000000006B',
                      'MAR_9999990E9A9236000000006A',
                      'MAR_9999990E9A92360000000069',
                      'MAR_9999990E9A92360000000068',
                      'MAR_9999990E9A92360000000067',
                      'MAR_9999990E9A92360000000066',
                      'MAR_9999990E9A92360000000065',
                      'MAR_9999990E9A92360000000052',
                      'MAR_9999990E9A92360000000051',
                      'MAR_9999990E9A92360000000002',
                      'MAR_9999990E9A92360000000015',
                      'MAR_9999990E9A92360000000029',
                      'MAR_9999990E9A9236000000003D',
                      'MAR_9999990E9A92360000000079',
                      'MAR_999999107FA3090000000065',
                      'MAR_999999107FA3090000000079',
                      'MAR_999999107FA309000000008D',
                      'MAR_999999107FA30900000000A1',
                      'MAR_999999107FA30900000000B5',
                      'MAR_999999107FA31100000000C9']

        for i in range(len(years)):
            if years[i] == self.year:
                eventcode = eventcodes[i]

        self.url = 'https://chicago-history.r.mikatiming.com/2019/?page=' + str(page) + '&event=' + eventcode \
                   + '&lang=EN_CAP&num_results=' + str(
            num) + '&pid=search&search%5Bage_class%5D=%25&search%5Bsex%5D=' + self.sex + '&search%5Bnation%5D=%25&search_sort=place_nosex'
        return self.url

    def getsoup(self):
        html = get(self.url)
        self.soup = Soup(html)

    def getlines(self):
        self.lines = self.soup.find('li', {'class': 'list-group-item row'}, partial=True)
        return self.lines


class Result(Race):
    def __init__(self, year, sex, location):
        self.GenderRank = 0
        self.NameCountry = ''
        self.link = ''
        self.Div = ''
        self.Time = ''
        self.citystate = ''
        self.placegender = 0
        self.placeAG = 0
        self.placeOverall = 0
        self.year = year
        self.sex = sex
        self.location = location
        self.dict = {}

        Race.__init__(self, year, sex, location)

    def getgenderrank(self, line):
        rank2 = line.find('div', {'class': ' type-place place-primary numeric'}, partial=True)

        if rank2 is not None:
            self.GenderRank = int(rank2.text)
        else:
            self.GenderRank = 'NA'

    def getnamecountry(self, line):
        link = line.find('a')
        self.NameCountry = link.text

    def getlink(self, line):
        self.link = 'https://chicago-history.r.mikatiming.com/2019/' + line.find("a").attrs.get("href")

    def getbib(self, line):
        bibblock = line.find('div', {'class': 'list-field type-field'}, partial=True, mode='first')
        bibparse = BeautifulSoup(str(bibblock), 'html.parser')
        test = bibparse.find('div', class_='visible-xs-block visible-sm-block list-label')
        self.Bib = int(test.next_sibling)

    def getdiv(self, line):
        Divblock = line.find('div', {'class': 'list-field type-age_class'}, partial=True, mode='first')
        Divparse = BeautifulSoup(str(Divblock), 'html.parser')
        test = Divparse.find('div', class_='visible-xs-block visible-sm-block list-label')
        self.Div = str(test.next_sibling).strip()

    def gettime(self, line):
        timeblock = line.find('div', {'class': 'list-field type-time'}, partial=True, mode='first')
        timeparse = BeautifulSoup(str(timeblock), 'html.parser')
        test = timeparse.find('div', class_='visible-xs-block visible-sm-block list-label')
        self.Time = str(test.next_sibling).strip()

    def getdetails(self):
        detailspagehtml = get(self.link)
        soupdetail = Soup(detailspagehtml)
        tablelines = soupdetail.find('tr', {'class': 'f-time_'}, partial=True)
        tablelines = tablelines[1:]
        tablefinish = soupdetail.find('tr', {'class': 'list-highlight f-time_finish_netto highlight'}, partial=True)
        splitmarks = []
        splitlist = []
        splitdiffs = []
        splitpaces = []
        splitspeed = []

        self.citystate = soupdetail.find('td', {'class': "f-__city_state last"}).text
        self.placegender = soupdetail.find('td', {'class': 'f-place_all last'}).text
        self.placeAG = soupdetail.find('td', {'class': 'f-place_age last'}).text
        self.placeOverall = soupdetail.find('td', {'class': 'f-place_nosex last'}).text

        for split in tablelines:
            splitmarks.append(split.find('th', {'class': 'desc'}))
            splitlist.append(split.find('td', {'class': 'time'}, partial=False).text)
            splitdiffs.append(split.find('td', {'class': 'diff'}).text)
            splitpaces.append(
                split.find('td', {'class': 'min_km right opt colgroup-splits colgroup-splits-metric'}).text)
            splitspeed.append(split.find('td', {'class': 'kmh colgroup-splits colgroup-splits-metric'}).text)

        splitmarks.append(tablefinish.find('th', {'class': 'desc'}).text)
        splitlist.append(tablefinish.find('td', {'class': 'time'}, partial=False).text)
        splitdiffs.append(tablefinish.find('td', {'class': 'diff'}).text)
        splitpaces.append(
            tablefinish.find('td', {'class': 'min_km right opt colgroup-splits colgroup-splits-metric'}).text)
        splitspeed.append(tablefinish.find('td', {'class': 'kmh colgroup-splits colgroup-splits-metric'}).text)

        self.ES05K = 'strong' in str(splitmarks[1])
        self.ES10K = 'strong' in str(splitmarks[2])
        self.ES15K = 'strong' in str(splitmarks[3])
        self.ES20K = 'strong' in str(splitmarks[4])
        self.ES21K = 'strong' in str(splitmarks[5])
        self.ES25K = 'strong' in str(splitmarks[6])
        self.ES30K = 'strong' in str(splitmarks[7])
        self.ES35K = 'strong' in str(splitmarks[8])
        self.ES40K = 'strong' in str(splitmarks[9])
        self.ES42K = 'strong' in str(splitmarks[10])

        # print(ES30K)
        self.T05K = splitlist[0]
        self.T10K = splitlist[1]
        self.T15K = splitlist[2]
        self.T20K = splitlist[3]
        self.T21K = splitlist[4]
        self.T25K = splitlist[5]
        self.T30K = splitlist[6]
        self.T35K = splitlist[7]
        self.T40K = splitlist[8]
        self.T42K = splitlist[9]

        self.S05K = splitdiffs[0]
        self.S10K = splitdiffs[1]
        self.S15K = splitdiffs[2]
        self.S20K = splitdiffs[3]
        self.S21K = splitdiffs[4]
        self.S25K = splitdiffs[5]
        self.S30K = splitdiffs[6]
        self.S35K = splitdiffs[7]
        self.S40K = splitdiffs[8]
        self.S42K = splitdiffs[9]

        self.P05K = splitpaces[0]
        self.P10K = splitpaces[1]
        self.P15K = splitpaces[2]
        self.P20K = splitpaces[3]
        self.P21K = splitpaces[4]
        self.P25K = splitpaces[5]
        self.P30K = splitpaces[6]
        self.P35K = splitpaces[7]
        self.P40K = splitpaces[8]
        self.P42K = splitpaces[9]

        self.SP05K = splitspeed[0]
        self.SP10K = splitspeed[1]
        self.SP15K = splitspeed[2]
        self.SP20K = splitspeed[3]
        self.SP21K = splitspeed[4]
        self.SP25K = splitspeed[5]
        self.SP30K = splitspeed[6]
        self.SP35K = splitspeed[7]
        self.SP40K = splitspeed[8]
        self.SP42K = splitspeed[9]

    def getresultpool(self, line, location):
        self.getgenderrank(line)
        self.getnamecountry(line)
        self.getlink(line)
        self.getbib(line)
        self.getdiv(line)
        self.gettime(line)
        self.getdetails()
        self.getweather(location)

    def dictresult(self):
        param = ['year', 'sex', 'sexRank', 'NameCountry', 'link', 'Bib', 'Div',
                 'Time',
                 'T05K', 'T10K', 'T15K', 'T20K', 'T21K', 'T25K', 'T30K', 'T35K', 'T40K', 'T42K',
                 'S05K', 'S10K', 'S15K', 'S20K', 'S21K', 'S25K', 'S30K', 'S35K', 'S40K', 'S42K',
                 'P05K', 'P10K', 'P15K', 'P20K', 'P21K', 'P25K', 'P30K', 'P35K', 'P40K', 'P42K',
                 'SP05K', 'SP10K', 'SP15K', 'SP20K', 'SP21K', 'SP25K', 'SP30K', 'SP35K', 'SP40K', 'SP42K',
                 'CityState', 'RankG', 'RankAG', 'RankOverall',
                 'DateTime', 'TempMax', 'TempMin', 'TempMoy', 'Humidity', 'Precip', 'WindSpeed', 'Winddir',
                 'Cloudcover',
                 'Conditions', 'Desc',
                 'ES05K', 'ES10K', 'ES15K', 'ES20K', 'ES21K', 'ES25K', 'ES30K', 'ES35K', 'ES40K', 'ES42K']

        self.dict = {param[0]: self.year,
                     param[1]: self.sex,
                     param[2]: self.GenderRank,
                     param[3]: self.NameCountry,
                     param[4]: self.link,
                     param[5]: self.Bib,
                     param[6]: self.Div,
                     param[7]: self.Time,
                     param[8]: self.T05K, param[9]: self.T10K, param[10]: self.T15K, param[11]: self.T20K,
                     param[12]: self.T21K,
                     param[13]: self.T25K, param[14]: self.T30K, param[15]: self.T35K, param[16]: self.T40K,
                     param[17]: self.T42K,
                     param[18]: self.S05K, param[19]: self.S10K, param[20]: self.S15K, param[21]: self.S20K,
                     param[22]: self.S21K,
                     param[23]: self.S25K, param[24]: self.S30K, param[25]: self.S35K, param[26]: self.S40K,
                     param[27]: self.S42K,
                     param[28]: self.P05K, param[29]: self.P10K, param[30]: self.P15K, param[31]: self.P20K,
                     param[32]: self.P21K,
                     param[33]: self.P25K, param[34]: self.P30K, param[35]: self.P35K, param[36]: self.P40K,
                     param[37]: self.P42K,
                     param[38]: self.SP05K, param[39]: self.SP10K, param[40]: self.SP15K,
                     param[41]: self.SP20K,
                     param[42]: self.SP21K, param[43]: self.SP25K, param[44]: self.SP30K,
                     param[45]: self.SP35K,
                     param[46]: self.SP40K, param[47]: self.SP42K,
                     param[48]: self.citystate, param[49]: self.placegender, param[50]: self.placeAG,
                     param[51]: self.placeOverall,
                     param[52]: self.datetime, param[53]: self.tempmax, param[54]: self.tempmin,
                     param[55]: self.tempmoy,
                     param[56]: self.humidity, param[57]: self.precip, param[58]: self.windspeed,
                     param[59]: self.winddir,
                     param[60]: self.cloudcover, param[61]: self.conditions, param[62]: self.description,
                     param[63]: self.ES05K, param[64]: self.ES10K, param[65]: self.ES15K,
                     param[66]: self.ES20K,
                     param[67]: self.ES21K,
                     param[68]: self.ES25K, param[69]: self.ES30K, param[70]: self.ES35K,
                     param[71]: self.ES40K,
                     param[72]: self.ES42K}
        return self.dict





def main():
    # PARAMS
    yearlist = [2004]
    sexlist = ['M','W']
    pages = range(1, 4)
    location = 'Chicago'
    samples = 1000

    for year, sex, page in itertools.product(yearlist, sexlist, pages):
        print(location+" Marathon"+" Year = "+str(year)+" Sex = "+sex+" Page n°"+str(page)+"/"+str(len(pages)))
        scraping = Scrap(year, sex, location)
        scraping.chipagegen(page, samples)
        scraping.getsoup()
        lines = scraping.getlines()
        listd = []
        with alive_bar(len(lines), bar = 'filling') as bar:
            for line in lines:
                result = Result(year, sex, location)
                result.getresultpool(line, location)
                d = result.dictresult()
                listd.append(d)
                bar()
            df = pd.DataFrame(listd)
            filename = 'chicago_'+str(year)+"_"+sex+"_"+str(samples)+"_"+str(page)+'.csv'
            df.to_csv(filename, encoding='utf-8', index=False)



if __name__ == "__main__":
    main()
