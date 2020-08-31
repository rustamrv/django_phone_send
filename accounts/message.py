import requests
import phone_send.settings as settings

def send_message(to, body):  
    text_xml = xml_gen(to, body)
    headers = {
        'Content-Type': 'application/xml; charset=utf-8',
        'Authorization': 'Bearer ' + getattr(settings, 'SENDSMS_AUTH_TOKEN')
    }
    response = requests.post("https://gate.smsclub.mobi/xml/", headers=headers, data=text_xml) 


def xml_gen(to, body):
    xml = '''<?xml version='1.0' encoding='utf-8'?>
        <request_sendsms>
        <username><![CDATA['''+getattr(settings, 'SENDSMS_FROM_NUMBER')+''']]></username>
        <password><![CDATA['''+getattr(settings, 'SENDSMS_PASSWORD')+''']]></password>
        <from><![CDATA['''+getattr(settings, 'SENDSMS_ALHASMS')+''']]></from>
        <to><![CDATA['''+to+''']]></to>
        <text><![CDATA['''+body+''']]></text>
        </request_sendsms>'''
    # print(xml)
    return xml
