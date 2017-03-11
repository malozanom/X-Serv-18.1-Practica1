#!/usr/bin/python3

"""
Miguel Ángel Lozano Montero.
Program implementing a web application that shorten URLs.
"""

import webapp
import urllib.parse
import os.path


class shortenUrls (webapp.webApp):
    """ Web application that shorten URLs.
    Two dictionaries are created: one with long URLs as keys and
    another with the number of short URLs as keys."""

    urlsDict = {}
    numDict = {}

    # Load the CSV file
    exists = os.path.isfile('urls.csv')
    if exists:
        fich = open('urls.csv', 'r')
        for linea in fich.readlines():
            url, shortUrl = linea[:-1].split(',')
            num = shortUrl.split('/')[-1]
            urlsDict[url] = shortUrl
            numDict[int(num)] = url
        fich.close()

    def parse(self, request):
        """Return the method, resource name (without /) and qs (if there is)"""

        method = request.split(' ', 1)[0]
        resourceName = request.split(' ', 2)[1][1:]
        url = request.split('=')[-1]
        urlUnquote = urllib.parse.unquote(url)
        qs = request.split('\r\n\r\n', 2)[-1]

        return (method, resourceName, urlUnquote, qs)

    def process(self, parsed):
        """Process the relevant elements of the request. """

        method, resourceName, url, qs = parsed

        if method == "GET" and resourceName == "":
            httpCode = "200 0K"
            if len(self.urlsDict) > 0:
                lista = self.show()
                htmlBody = "<form method='POST' action=''>" + \
                           "<h1>URL que desea acortar: </h1><br>" + \
                           "<input type='text' name='url' value=''>" + \
                           "<input type='submit' value='Enviar'></form>" + \
                           "<h1><u>Lista de URLs acortadas</u></h1>" + \
                           "<h3>" + lista + "</h3>"

            else:
                htmlBody = "<form method='POST' action=''>" + \
                           "<h1>URL que desea acortar: </h1><br>" + \
                           "<input type='text' name='url' value=''>" + \
                           "<input type='submit' value='Enviar'></form>" + \
                           "<h1><u>Lista de URLs acortadas</u></h1>"

        elif method == "GET" and resourceName.isdigit():
            if int(resourceName) in self.numDict.keys():
                urlRedirect = self.numDict[int(resourceName)]
                httpCode = "301 Moved Permanently"
                if "http" in urlRedirect:
                    htmlBody = "<html><body><h1><meta http-equiv='refresh'" + \
                               "content='0;url=" + urlRedirect + \
                               "'></h1></body></html>"
                else:
                    htmlBody = "<html><body><h1><meta http-equiv='refresh'" + \
                               "content='0;url=http://" + urlRedirect + \
                               "'></h1></body></html>"
            else:
                httpCode = "404 Not Found"
                htmlBody = "<html><body><h1>" + "Recurso no disponible" + \
                           "</h1></body></html>"

        elif method == "POST":
            if len(qs) > 4:     # Due to "url="
                httpCode = "200 0K"
                shortUrl = self.add(url)
                if "http" in url:
                    htmlBody1 = "<html><body><h1><a href=" + url + \
                                 ">URL original<br>"
                else:
                    htmlBody1 = "<html><body><h1><a href=http://" + url + \
                                 ">URL original<br>"
                htmlBody2 = "<a href=" + shortUrl + ">URL acortada" + \
                            "<br></a></h1></body></html>"
                htmlBody = htmlBody1 + htmlBody2
            else:
                httpCode = "404 Not Found"
                htmlBody = "<html><body><h1>" + "No hay query string" + \
                           "</h1></body></html>"

        else:
            httpCode = "404 Not Found"
            htmlBody = "<html><body><h1>" + "No encontrado" + \
                       "</h1></body></html>"
        return (httpCode, htmlBody)

    def add(self, url):
        """Add the URL to a dictionary (if it was not), the number
        to another dictionary, call a method to set this changes in the
        CSV file and finally return the short URL"""

        if "http" not in url:
            url = "http://" + url
        partialUrl = "http://localhost:1234/"
        num = len(self.urlsDict)
        if url not in self.urlsDict.keys():
            shortUrl = partialUrl + str(num)
            self.urlsDict[url] = shortUrl
            self.numDict[num] = url
            self.addFile(url, shortUrl)
        return (self.urlsDict[url])

    def addFile(self, url, shortUrl):
        """Add the new URLs to the CSV file"""

        fich = open('urls.csv', 'a')
        fich.write(url + "," + shortUrl + '\n')
        fich.close()

    def show(self):
        """Show all the URLs stored in the dictionary and their related
        short URL"""

        lista = ''
        for url in self.urlsDict:
            lista = lista + url + " => " + self.urlsDict[url] + '<br>'
        return lista

if __name__ == "__main__":
    testShortenUrls = shortenUrls("localhost", 1234)
