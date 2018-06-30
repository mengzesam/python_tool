# -*- coding: utf-8 -*-

import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class spider():
    province_codes={'北京':'10003',
    '天津':'10006',
    '河北':'10016',
    '山西':'10010',
    '内蒙古':'10002',
    '辽宁':'10027',
    '吉林':'10004',
    '黑龙江':'10031',
    '上海':'10000',
    '江苏':'10014',
    '浙江':'10018',
    '安徽':'10008',
    '福建':'10024',
    '江西':'10015',
    '山东':'10009',
    '河南':'10017',
    '湖北':'10021',
    '湖南':'10022',
    '广东':'10011',
    '广西':'10012',
    '海南':'10019',
    '重庆':'10028',
    '四川':'10005',
    '贵州':'10026',
    '云南':'10001',
    '西藏':'10025',
    '陕西':'10029',
    '甘肃':'10023',
    '青海':'10030',
    '宁夏':'10007',
    '新疆':'10013',
    '香港':'10020'}
    school_xp = '//div[@class="li-collegeUl"]/p[@class="li-school-label"]/span'
    major_xp = '//table[@class="li-admissionLine"]/tbody/tr'
    url = ''
    html = ''
    school=''
    year=''
    subject=''
    province=''

    def __init__(self,file_name):
        self.file_name='out.csv'
        if file_name!='':
            self.file_name=file_name

    def setMembers(self, school_code, subject, year, pronvice):
        self.school_code=school_code
        self.subject=subject
        self.year=year
        self.province=pronvice
        if subject=='文科':
            subject_code='10034'
        elif subject=='理科':
            subject_code='10035'
        self.url = 'https://gkcx.eol.cn/schoolhtm/specialty/%s/%s/specialtyScoreDetail_%s_%s.htm' % (
        school_code, subject_code, year, self.province_codes[pronvice])

    def openFile(self):
        self.fd=None
        try:
            self.fd = open(self.file_name,'w')
            self.fd.write('学校,考生省份,年份,文理科,专业,最高分,平均分,最低分,批次,网页链接,学校编号\n')
        finally:
            return

    def closeFile(self):
        if self.fd:
            self.fd.close()

    def getHtml(self):
        r = requests.get(self.url)
        r.encoding='utf-8'
        self.html = r.text

    def extraHtml(self):
        print self.url
        selector = etree.HTML(self.html)
        school =selector.xpath(self.school_xp)
        if(len(school)==0):
            return -1
        self.school=school[0].text.strip()
        trs=selector.xpath(self.major_xp)
        ss=u''
        for tr in trs:
            tds=tr.xpath('./td')
            if(len(tds)==6):
                tmp=tds[0].xpath('./p/text()')
                major=''
                if len(tmp)>0:
                    major=tmp[0].strip()
                max_score=tds[2].text.strip()
                average_score=tds[3].text.strip()
                min_score=tds[4].text.strip()
                admission_catalog=tds[5].text.strip()
                ss='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (self.school,self.province,self.year,self.subject,
                                                        major,max_score,average_score,min_score,admission_catalog,
                                                        self.url,self.school_code)
                if self.fd:
                    self.fd.write(ss)


if __name__=='__main__':
    spider=spider('out2.csv')
    spider.openFile()
    school_start=1
    school_end=10001
    #for subject in ['理科','文科']:
    for subject in ['理科']:
        for year in ['2015','2016']:            
            for i in range(school_start,school_end+1,1):
                school_code='%d' % (i)
                print school_code
                #for province in spider.province_codes:
                for province in ['广西']:            
                    spider.setMembers(school_code,subject,year,province)
                    spider.getHtml()
                    spider.extraHtml()
    spider.closeFile()

    
