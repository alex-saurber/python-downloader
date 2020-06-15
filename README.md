# python-downloader
testing the ability of python to contact web services, downloading a file, and placing it in a specific directory

The script gdrivedownloader uses Google's Drive API to contact their servers and download a specified file.
You can get the file ID by checking what the unique hash for the file is from looking at the shareable link URL
This code is only useable if you request and authorize your own credentials through the Google API dashboard

This example was to download modified aircraft textures for a simulator.

I attempted to package it with pyinstaller at one point to make it an .EXE I could distibute to friends, but it wasn't worth it.
