from email.header import Header
from email.mime.text import MIMEText
import json
import mechanicalsoup
import os.path
import smtplib

class Grades:

    def __init__(self):
        self.browser = mechanicalsoup.Browser(soup_config = {'features': 'html.parser'})
        # TUCaN user and password
        user = '#'
        password = '#'
        # @stud.tu-darmstadt.de email address
        email = '#'
        page = self.signin(user, password)
        grades = self.get_grades(page)
        diff = self.get_diff_from_cache(grades)
        if len(diff) > 0:
            self.send_mail(user, password, email, diff)

    def get_page(self, uri):
        page = self.browser.get('https://www.tucan.tu-darmstadt.de' + uri)
        # Check for and follow redirects
        redirect = page.soup.find('meta', attrs={'http-equiv': 'refresh'})
        if redirect is not None:
            page = self.get_page('='.join(redirect['content'].split('=')[1:]))
        return page

    def get_link(self, page, text):
        for link in page.soup.find_all('a'):
            # Get a link by its text attribute
            if link.text == text:
                return link['href']
        raise IndexError

    def signin(self, user, password):
        page = self.get_page('/')
        form = mechanicalsoup.Form(page.soup.select_one('#cn_loginForm'))
        form.input({'usrname': user, 'pass': password})
        response = self.browser.submit(form, page.url)
        return self.get_page('='.join(response.headers['REFRESH'].split('=')[1:]))

    def get_grades(self, page):
        # Go to examinations page
        page = self.get_page(self.get_link(page, 'Prüfungen'))
        # Go to performance record page
        page = self.get_page(self.get_link(page, 'Leistungsspiegel'))
        grades = {}
        for row in page.soup.find_all('tr'):
            cols = row.select('td')
            if len(cols) >= 5 and len(cols[5].text) > 0:
                grades[cols[1].a.text] = cols[5].text
        return grades

    def get_diff_from_cache(self, grades):
        if os.path.isfile('cache.json'):
            f = open('cache.json', 'r')
            cache = json.load(f)
            f.close()
            diff = {course: grade for course, grade in grades.items() if course not in cache or cache[course] != grade}
            # Do not write cache file unless there is a difference
            if len(diff) < 1:
                return diff
        else:
            diff = {}
        f = open('cache.json', 'w')
        json.dump(grades, f)
        f.close()
        return diff

    def send_mail(self, user, password, email, grades):
        text = ''
        for course, grade in grades.items():
            text += '- {}: {}\n'.format(course, grade)
        msg = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
        msg['To'] = email
        msg['From'] = email
        msg['Subject'] = Header('Neue Noten', 'utf-8')
        smtp = smtplib.SMTP_SSL('smtp.tu-darmstadt.de', 465)
        smtp.login(user, password)
        smtp.sendmail(email, email, msg.as_string())
        smtp.quit()

grades = Grades()
