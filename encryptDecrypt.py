"""
Author: Liam Stevens (ICT Analyst, St Joseph's College Gregory Terrace)
Created on: 18/7/2018

Based on a C# example by @ricardorusson and PS example by @sam-fisher:
https://github.com/TheAlphaSchoolSystemPTYLTD/api-introduction/blob/master/encryptDecrypt.cs
https://github.com/TheAlphaSchoolSystemPTYLTD/api-introduction/blob/master/EncryptDecrypt.ps1

An example of encrypting and decrypting your Token and accessing the API using Python; specifically the getStudentsDetails method.

Requires a few packages be installed with pip (or pip3 if you're running multiple versions of python, or have yet to aliase pip for Python3).
Run:
pip install requests
pip install pycrypto
"""
import requests
from Crypto.Cipher import AES
import urllib
import base64

# These variables should be configured as per your own parameters for each application in your API Gateway Maintanence portal.

# Token as generated by API Gateway
tokenKey='x8FWQUedjyiUGlTf5appPQ=='
# Specified upon API setup in TASS API Gateway Maintenance program.
appCode="DEMOAPP"
# TASS company to work with (see top right of TASS.web).
companyCode="10"
# TASS API version.
apiVersion="2"
# TASS API method.
method="getStudentsDetails"
# TASS API endpoint.
endPoint="http://api.tasscloud.com.au/tassweb/api/"
# Parameters for passthrough - varies based on method.
parameters = "{\"currentstatus\":\"current\"}"

def getEncryptedToken(token, params):
    #decode the token from b64 format
    decoded = base64.b64decode(token)
    plaintext = params
    #put ECB padding in place for plaintext
    length = 16 - (len(plaintext) % 16)
    plaintext += chr(length)*length
    rijndael = AES.new(decoded, AES.MODE_ECB)
    #encrypt the plaintext
    ciphertext = rijndael.encrypt(plaintext)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def getDecryptedToken(token, encrypted):
    #decode from b64 for both the token and the encrypted data
    decoded = base64.b64decode(token)
    encoded = base64.b64decode(encrypted)
    decoder = AES.new(decoded, AES.MODE_ECB)
    #decrypt the data
    output = decoder.decrypt(encoded)
    return output

def getURLRequest(endPoint, method, appCode, companyCode, apiVersion, parameters, tokenKey):
    encrypted = getEncryptedToken(tokenKey, parameters)
    requestDict = {"method": method, "appcode": appCode, "company": companyCode, "v": apiVersion, "token": encrypted}
    requestStr = urllib.urlencode(requestDict)
    URLString = endPoint + '?' + requestStr
    print URLString
    return URLString

#When the script is invoked, create a URL based on the variables specified at the head of the file. Output to command line.
if __name__ == "__main__": 
    getURLRequest(endPoint, method, appCode, companyCode, apiVersion, parameters, tokenKey)

