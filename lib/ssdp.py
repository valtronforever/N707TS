import socket
try:
    from http.client import HTTPResponse
except ImportError:
    from httplib import HTTPResponse

try:
    from StringIO import StringIO as IOBuff
except ImportError:
    from io import BytesIO as IOBuff

import requests
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from xml.etree import ElementTree


class SSDPResponse(object):
    class _FakeSocket(IOBuff):
        def makefile(self, *args, **kw):
            return self

    def __init__(self, response):
        r = HTTPResponse(self._FakeSocket(response))
        r.begin()
        self.location = r.getheader("location")
        self.usn = r.getheader("usn")
        self.st = r.getheader("st")
        self.cache = r.getheader("cache-control").split("=")[1]

    def __repr__(self):
        return "<SSDPResponse({location}, {st}, {usn})>".format(**self.__dict__)


def discover(service, timeout=2, retries=1, mx=2):
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}',
        'MAN: "ssdp:discover"',
        'ST: {st}', 'MX: {mx}', '', ''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(message.format(*group, st=service, mx=mx).encode('utf-8'), group)
        while True:
            try:
                response = SSDPResponse(sock.recv(1024))
                responses[response.location] = response
            except socket.timeout:
                break
    return list(responses.values())


def get_info_from_xml(url):
    model = None
    serial = None

    ns = '{urn:schemas-upnp-org:device-1-0}'
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)
    for n in root.iter():
        if n.tag == ns + 'modelName':
            model = n.text
        if n.tag == ns + 'serialNumber':
            serial = n.text
    return urlparse(url).netloc, model, serial


def get_available_devices():
    devices = []
    for r in discover("urn:help-micro.kiev.ua:device:webdev:1"):
        devices.append(get_info_from_xml(r.location))
    return devices
