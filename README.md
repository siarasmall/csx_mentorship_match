Last updated: 9/29/24

parse.py
Mentorship match program for Tufts CSX. Parse.py generates the match pairings.

Usage:
'python parse.py [input.csv]'

input.csv has expected format matching Google form.
input.csv expected to be in the same directory or a valid path to the input csv.

Outputs matches to matching.csv.

intros.py
Automates the introduction email process.

Usage:
'python parse.py [input.csv]'
input.csv has expected format matching the matchings csv generated by parse.py

Currently, only Gmail is supported, as Outlook requires Tufts SSO. To generate
an app password for Gmail (required if you use 2FA for Gmail), follow these directions:
https://support.google.com/mail/answer/185833?hl=en . Once you have created the app password, 
use that for the password field below.

Before running, set environment variables in terminal:
export EMAIL_ADDRESS=[YOUR EMAIL ADDRESS]
export EMAIL_PASSWORD=[YOUR EMAIL PASSWORD]
