#!/usr/bin/env python3

import argparse
import smtplib
import textwrap
# import pdb; pdb.set_trace()

from hurry.filesize import size
## from assets import email_message

import xml.etree.ElementTree as etree


# argparse to accept xml document as command line argument
def argument_parser():
    parser = argparse.ArgumentParser(description='Dont fraud, yo')
    parser.add_argument('--xml', dest='xml', help='The xml file')
    args = parser.parse_args()
    return args

def parse_xml(xml_file):
    # grab UUID, will be replaced by internal API request
    uuid = input("Please input UUID: ")
    #Grab hostname, will be replaced by internal API request
    hostname = input("Please input hostname: ")
    data = etree.parse(xml_file)
    root = data.getroot()
    # root[3] = <Element '{http://www.acns.net/ACNS}Source'
    ip_addr = root[3][1].text
    time = root[3][0].text
    port = root[3][2].text
    type = root[3][3].text
    # root[4] = <Element '{http://www.acns.net/ACNS}Content'
    hash = root[4][0][4].text
    title = root[4][0][1].text
    file_name = root[4][0][2].text
    file_size = root[4][0][3].text
    # human readable byte conversion
    hr_size = (size(int(file_size)))

    # I know this is kinda ugly, working on implementing pulling template from separate file
    message = (textwrap.dedent(f'''\
    Subject:Abuse from {ip_addr}\n
    Hello,

    We are contacting you in regards to your server with the IP address {ip_addr}.

    We have received a notice of claimed infringing activity originating from your server
    {ip_addr} / {hostname} / {uuid}. It is possible that your server is
    being used for illegally distributing copyrighted material and therefore we would like you to
    check the integrity of the server.

    If you are able to confirm the claimed infringement, we ask that you take appropriate action
    to stop any illegal sharing of copyrighted material. You will find additional technical details
    regarding the claim below.

    Note that a VPN does not guarantee anonymity and any network traffic on your servers must
    comply with Terms of Service and Acceptable Use Policy.
    https://www.companyname.com/documentation/terms/

    -------------------------INFRINGEMENT DETAILS------------------------------------------------
    Title: {title}
    Timestamp: {time}
    IP Address: {ip_addr}
    Port: {port}
    Type: {type}
    Torrent Hash: {hash}
    Filename: {file_name}
    Filesize: {hr_size}
    ---------------------------------------------------------------------------------------------

    We hope this information will help you in determining the source of the claim and shut it
    down.

    Best Regards,
    Support
    '''))

    return message

def send_tool(message):
    # show message for proofing before sending
    print(message)
    y = input("Does message look correct? y or n: ")
    if y == 'y':
        # grab to email addr; will be automated with internal API tool
        to_list = input("Who should I send this too? ")
        # conect to smtp server and send email then close connection
        smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_obj.starttls()
        smtp_obj.login('support@upcloud.com', 'krezpncvvfirtpiy')
        smtp_obj.sendmail("support@upcloud.com",
                          to_list, message)
        smtp_obj.quit()

def main():
    args = argument_parser()
    # parse_xml(args.xml)
    msg = parse_xml(args.xml)
    send_tool(msg)
    #print(msg)
    #print("complete")


if __name__ == "__main__":
    main()
