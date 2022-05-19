from datetime import datetime
from random import SystemRandom
from string import ascii_letters, digits
from time import time
import urllib.parse
from flask import session

def url_decoder(url: str):
    decode_service = urllib.parse.unquote(url)
    return decode_service

def generate_token(size=6, chars=ascii_letters+digits):
    return ''.join(SystemRandom().choice(chars) for _ in range(size))

def generate_ticket_body(length=29):
    # Default length is 29 to limit string length when
    # concatenated by 'PT-' or 'ST-' by 32 characters,
    # the maximum length a service MUST be able to handle.
    # See more:
    # https://apereo.github.io/cas/5.1.x/protocol/CAS-Protocol-V2-Specification.html#3-cas-entities

    timestamp = str(int(time()))

    return timestamp + generate_token(length-len(timestamp))

def check_token_expired(time: datetime):
    if datetime.now() > time:
        return True
    else: 
        return False
            
    
def xml_return(_id, email, token):
    return f"""
        <cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
            <cas:authenticationSuccess>
                <cas:user>{email}</cas:user>
                <cas:attributes>
                    <cas:user_id>{_id}</cas:user_id>
                    <cas:email>{email}</cas:email>
                    <cas:phone/>
                    <cas:fullname/>
                    <cas:token>{token}</cas:token>
                </cas:attributes>
            </cas:authenticationSuccess>
        </cas:serviceResponse>
    """