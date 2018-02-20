import smtplib
from email.MIMEText import MIMEText
from src.models.user import User


class Emailer(object):

    @staticmethod
    def send_email(author_id, posts, passed_msg):
        user = User.get_by_id(author_id)
        gmail_user = 'kijiji.scraping.app@gmail.com'
        gmail_password = 'kijiji_app'
        fromx = 'kijiji.scraping.app@gmail.com'
        to = user.email

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_password)
        for post in posts:
            title = str(post.title.encode('ascii', errors='ignore'))
            prices0 = str(post.prices[0])
            url = str(post.url)
            print('Emailing regarding this URL: {}, MSG = {}').format(url, passed_msg)
            msg = MIMEText('{} - {} \n{}'.format(title, prices0, url))
            if all([(passed_msg == 'new_post'), (user.new_post_email is True)]):
                msg['Subject'] = 'New post! - {} - {}'.format(title, prices0)
            elif all([(passed_msg == 'price_drop'), (user.price_drop_email is True)]):
                prices1 = str(post.prices[1])
                msg['Subject'] = 'Price drop! - {} - {} <-- {}'.format(title, prices0, prices1)
            msg['From'] = fromx
            msg['To'] = to
            server.sendmail(fromx, to, msg.as_string())
            print('{} email sent!').format(passed_msg)
        server.quit()




