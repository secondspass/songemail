from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import re


def get_song_path():
    """Because youtube-dl does not replaces the '|' character with the '_'
    character, we need to go directly to the directory and retrieve the
    file name and path from there. This also means we will have to delete the
    file after the file has been sent. That's what delete_song() is for.
    """

    song_name_list = os.listdir('songs')
    song_path = os.path.abspath(os.path.join('songs', song_name_list[0]))
    return song_path


def delete_song(song_path):
    """Deletes the song after it has been sent"""

    os.remove(song_path)


def create_mail(title, to_address):
    send_user = os.environ.get('SEND_USER')
    msg = MIMEMultipart()
    msg['Subject'] = 'songemail sends you: {}'.format(title)
    msg['From'] = send_user
    msg['To'] = to_address
    msg.preamble = 'A song from songemail'

    song_path = get_song_path()

    with open(song_path, 'rb') as fp:
        song = MIMEAudio(fp.read(), 'mp3')
        cleaned_title = " ".join(re.findall('[a-zA-Z0-9]+', title)) + '.mp3'
        song['Content-Disposition'] = 'attachment; filename="{}"'.format(cleaned_title)
        print(song['Content-Disposition'])
        msg.attach(song)

    delete_song(song_path)
    print("song deleted")
    return msg


def send_mail(title, msg, to_address):
    send_user = os.environ.get('SEND_USER')
    send_pwd = os.environ.get('SEND_PWD')

    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    print("Logging in now")
    smtpserver.login(send_user, send_pwd)
    print("logged in to SMTP Server")
    smtpserver.send_message(msg, send_user, to_address)
    print("song sent. Logging out.")
    smtpserver.close()


def email_helper(title, to_address):  # title and to_address is passed from downloadWorker in youdown.py
    msg = create_mail(title, to_address)
    send_mail(title, msg, to_address)
