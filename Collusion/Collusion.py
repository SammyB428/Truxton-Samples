import sys
import shutil
import base64
import os

from datetime import datetime
from calendar import timegm
from pathlib import Path
from inspect import currentframe, getframeinfo

sys.path.append('C:/Program Files/Truxton/SDK')
#sys.path.append('C:/Users/Sam/Documents/GitHub/Truxton/Libraries/Python/PyTrux/x64/Debug')
import truxton

# https://www.scribd.com/document/377540616/PS-LP-Text-Messages-Dec-2016-May-2017#from_embed
# https://dailycaller.com/2018/06/12/strzok-texts-highly-questionable/

# Redaction convention.
# Something redacted will have the lable of "--Redacted--"
# Something redacted but a possible reveal included will be "--Redacted/Meaning--"

# Documents to checkout
# https://www.scribd.com/document/456627682/04-15-20-ODNI-Declassified-Footnotes-20-00337-Unclassified
# https://www.scribd.com/document/409058964/KavelecSteeleMemoToFile10-11-16
# https://github.com/codyave/WhiteHat/blob/master/Steele-Kavalec%20notes.txt
# https://www.realclearinvestigations.com/articles/2021/09/23/biden_security_adviser_sullivan_tied_to_16_clinton_plan_to_co-opt_cia_and_fbi_to_tar_trump_795498.html
# https://technofog.substack.com/p/why-is-a-fusion-gps-attorney-risking

# Crossfire's as reported in page 826 of Report_Volume5.pdf
# Crossfire Hurricane - Umbrella Investigation, case number 97F-HQ-2063661
# Crossfire Typhoon - George Papadopoulos, case number 97F-HQ-2067748, Opened 10 Aug 16 2016
# Crossfire Razor - Flynn, case number 97F-NY-2069860, Opened 16 Aug 16 2016
# Crossfire Fury - Paul Manafort, case number 97F-HQ-2067749, Opened 10 Aug 16 2016
# Crossfire Dragon - Carter Page, case number 97F-HQ-2067747, Opened 10 Aug 16 2016
# CROSS WIND - Walid Phares - https://web.archive.org/web/20210215161644/https://www.nytimes.com/2020/05/28/us/politics/mueller-walid-phares.html
# Crossfire Panda - Seth Rich - https://twitter.com/ClimateAudit/status/1614796252255866880?lang=de
# Crossfire Latitude - Flynn and Turkey? - https://twitter.com/nick_weil/status/1248343504880713728
# Midyear Exam - Investigation of Hillary Clinton EMail server with classfied information on it

mccabe_page_associations_were_made = False
strzok_page_associations_were_made = False
Investigation = None
FBI_GROUP = None
CROSSFIRE_HURRICANE_TEAM = None

def main() -> None:

  # print( 'Line ' + str(getframeinfo(currentframe()).lineno) )
  head_and_tail = os.path.split(os.path.realpath(__file__))

  global SUPPORT_DOCUMENTS_FOLDER

  SUPPORT_DOCUMENTS_FOLDER = head_and_tail[0] + os.sep + "Support Docs" + os.sep

  print("Support Documents Folder: " + SUPPORT_DOCUMENTS_FOLDER)

  t = truxton.create()
  print("Truxton Version: " + t.version)
  initialize_types(t)

  # Create the media to load files into
  media = create_media(t)

  # Now create an investigation
  global Investigation
  Investigation = create_investigation(t)
  Investigation.addnote("The redaction convention used here is something that was redacted will be marked --Redacted--, a guess at a redactions meaning will have a question mark --Redacted/Guess-- and an unredaction will be a slash --Redacted/Meaning--")

  # Associate the media with this investigation
  Investigation.addmedia(Crossfire_Typhoon.id)
  Investigation.addmedia(Crossfire_Razor.id)
  Investigation.addmedia(Crossfire_Fury.id)
  Investigation.addmedia(Crossfire_Dragon.id)
  Investigation.addmedia(media.id)

  print("Adding files, events, locations, communications, tags, etc.")

  # Create the top-level file that all other files will have as a parent
  typhoon_root = Crossfire_Typhoon.addroot()
  typhoon_root.save()

  razor_root = Crossfire_Razor.addroot()
  razor_root.save()

  fury_root = Crossfire_Fury.addroot()
  fury_root.save()

  dragon_root = Crossfire_Dragon.addroot()
  dragon_root.save()

  root_file = media.addroot()
  assert isinstance(root_file, truxton.TruxtonChildFileIO)
  root_file.save()

  create_groups(root_file)

  # Now add the things we gathered
  add_crossfire_razor_files(razor_root)
  add_crossfire_typhoon_files(typhoon_root)
  add_crossfire_fury_files(fury_root)
  add_crossfire_dragon_files(dragon_root)
  stephen_laycock(root_file)

  add_campaign_events(root_file)
  add_hillary(root_file)
  add_steele_dossier(root_file)
  add_nytimes_1(root_file)
  add_hrpt(root_file)
  add_election_polling_data(root_file)
  add_12333(root_file)
  add_baltic(root_file)
  add_halifax(root_file)
  add_brennan_in_moscow(root_file)
  add_mike_rogers(root_file)

  add_strzok_page_messages(root_file)
  add_mccabe_page_messages(root_file)
  add_miscellaneous(root_file)
  add_comey_leaks(root_file)
  add_defendant(root_file)
  add_dns(root_file)
  add_fbi_ig_report_fisa(root_file)
  add_clapper_testimony(root_file)
  add_russia_intel(root_file)
  add_brennan(root_file)
  add_fbi_spreadsheet(root_file)
  add_ohr(root_file)
  add_ec(root_file)
  add_danchenko_files(root_file)
  
  ie = Investigation.createevent()
  ie.text = "We have a plan comment"
  ie.when = truxton.parsetime("2016-08-15T12:05:00-05:00")
  ie.save()
  
  ie2 = Investigation.createevent()
  ie2.text = "Something significant was found here..."
  ie2.when = truxton.parsetime("2016-10-09T13:24:27-00:00")
  ie2.save()

  t.reindexmedia(Crossfire_Typhoon.id)
  t.reindexmedia(Crossfire_Razor.id)
  t.reindexmedia(Crossfire_Fury.id)
  t.reindexmedia(Crossfire_Dragon.id)
  t.reindexmedia(media.id)
  
  # Tell the Truxton ETL layer to finish processing the media
  #message = t.newmessage()
  #message.mediaid = Crossfire_Typhoon.id
  #message.send("finished")
  #message.mediaid = Crossfire_Razor.id
  #message.send("finished")
  #message.mediaid = Crossfire_Fury.id
  #message.send("finished")
  #message.mediaid = Crossfire_Dragon.id
  #message.send("finished")
  #message.mediaid = media.id
  #message.send("finished")

  # We are done!
  print("Finished")
  return None

def initialize_types(t):

  # Create the things unique to our investigation
  create_artifact_types(t)
  create_event_types(t)
  create_tags(t)
  create_subjects(t)

  return None

def create_groups(f):

  global FBI_GROUP
  FBI_GROUP = add_group(f, "FBI")

  global CROSSFIRE_HURRICANE_TEAM
  CROSSFIRE_HURRICANE_TEAM = add_group(f, "Crossfire Hurricane")

  return None

def add_person_to_group(p, g):
  return None

def create_investigation(t):
  jurisdiction = t.newjurisdiction()
  jurisdiction.id = 100
  jurisdiction.name = "DOJ-DC"
  jurisdiction.description = "Justice Department DC Headquarters"
  jurisdiction.save()

  investigation = t.newinvestigation()

  investigation.name = "Crossfire Hurricane"
  investigation.description = "Goatus Ropus"
  investigation.case = "97F-HQ-2063661"
  investigation.jurisdiction = jurisdiction.id
  investigation.status = truxton.INVESTIGATION_STATUS_OPEN
  investigation.type = truxton.INVESTIGATION_TYPE_FRAUD

  if investigation.save():
    print("Investigation created")

  return investigation

def add_campaign_events(parent_file: truxton.TruxtonChildFileIO) -> None:
  add_clinton_campaign_events(parent_file)
  add_trump_campaign_events(parent_file)

  return None

def add_clinton_campaign_events(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Campaign.txt")

  add_event( child_file, "2015-04-12T12:00:00-05:00", "2015-04-12T12:00:00-05:00", "Clinton announces candidacy", "Youtube", EVENT_TYPE_HILLARY )
  add_event( child_file, "2016-07-26T20:00:00-05:00", "2016-07-26T20:00:00-05:00", "Clinton becomes Democratic nominee", "Clinton becomes Democratic nominee", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2020-09-30T20:00:00-05:00", "2020-09-30T20:00:00-05:00", "Bruce Ohr Retires", "Retired from DOJ", EVENT_TYPE_DOJ )

  return None

def add_crossfire_typhoon_files(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/120919-examination.pdf")

  url = child_file.newurl()
  url.url = "https://www.justice.gov/storage/120919-examination.pdf"
  url.localfilename = "120919-examination.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-09-01T12:00:00-05:00")
  url.save()

  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:00:00-05:00", "FBI opens Foreign Agents Registration Act (FARA) case on Papadopoulos (Crossfire Typhoon)", "FBI IG Report page 59", EVENT_TYPE_FBI )

  add_papadopoulos(parent_file)
  add_daily_caller_1(parent_file)

  return None

def add_crossfire_fury_files(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/120919-examination.pdf")

  url = child_file.newurl()
  url.url = "https://www.justice.gov/storage/120919-examination.pdf"
  url.localfilename = "120919-examination.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-09-01T12:00:00-05:00")
  url.save()

  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:00:00-05:00", "FBI opens Foreign Agents Registration Act (FARA) case on Paul Manafort (Crossfire Fury)", "FBI IG Report page 59", EVENT_TYPE_FBI )

  return None

def add_sussman_files(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "525726563-Sussmann-Indictment.pdf")
  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/525726563/Sussmann-Indictment"
  url.localfilename = "525726563-Sussmann-Indictment.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2021-09-16T18:06:00-05:00")
  url.save()

  add_event( child_file, "2016-09-19T12:00:00-05:00", "2016-09-19T12:05:00-05:00", "Michael Sussmann meets FBI General Counsel James Baker", "At FBI HQ, three white papers and data files, alleging link between Trump and Alfa Bank", EVENT_TYPE_FBI )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "535125776-Sussmann-Motion.pdf")
  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/535125776/Sussmann-Motion"
  url.localfilename = "535125776-Sussmann-Motion.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2021-10-27T12:17:00-05:00")
  url.save()

  add_event( child_file, "2017-02-09T12:00:00-05:00", "2017-02-09T12:05:00-05:00", "Michael Sussmann meets CIA OGC", "Page 3, alleging link between Trump and Alfa Bank", EVENT_TYPE_CIA )

  return None

def add_exhibit5(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/gov.uscourts.dcd.191592.198.6.pdf")
  url = child_file.newurl()
  url.url = "https://storage.courtlistener.com/recap/gov.uscourts.dcd.191592/gov.uscourts.dcd.191592.198.6.pdf"
  url.localfilename = "gov.uscourts.dcd.191592.198.6.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2021-09-16T18:06:00-05:00")
  url.save()

  add_event(child_file, "2017-01-24T16:00:00-05:00", "2017-01-24T16:00:00-05:00", "Peter Strzok (FBI) and Joe Pientka (FBI) draft 302 about Flynn interview", "Comey testimony to HPSCI on March 2, 2017 page 9-10", EVENT_TYPE_FBI )

  return None

def add_danchenko_files(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "gov.uscourts.vaed.515692.1.0_1.pdf")
  url = child_file.newurl()
  url.url = "https://storage.courtlistener.com/recap/gov.uscourts.vaed.515692/gov.uscourts.vaed.515692.1.0_1.pdf"
  url.localfilename = "gov.uscourts.vaed.515692.1.0_1.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2021-11-04T18:06:00-05:00")
  url.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_HOME
  location.label = "Igor Danchenko - 5837 15th Street North"
  location.latitude = 38.88345350861377
  location.longitude = -77.14053802242607
  location.when = datetime.fromisoformat("2017-04-01T12:00:00-05:00")
  location.save()

  # https://www.washingtonexaminer.com/news/justice/pr-executive-1-identified-as-longtime-clinton-adviser-who-fed-falsehood-to-steele-source

  add_event( child_file, "2016-04-26T12:00:00-05:00", "2016-04-26T12:05:00-05:00", "Danchenko E-Mails Charles Dolan about passing info to Steele", "Page 7, Danchenko passed Dolan's letter to Steele", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-06-10T12:00:00-05:00", "2016-06-10T12:05:00-05:00", "Charles Dolan E-Mails friend about Danchenko", "Page 8, Thinks Danchenko is FSB", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-09-14T12:00:00-05:00", "2016-09-14T12:05:00-05:00", "Charles Dolan Attends Meeting at Russian Embassy", "Page 8, With Organizer-1", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-06-13T12:00:00-05:00", "2016-06-15T12:05:00-05:00", "Charles Dolan Travels to Moscow", "Page 9, Stays at Moscow Ritz-Carlton", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-06-15T12:00:00-05:00", "2016-06-15T12:05:00-05:00", "Charles Dolan Tours Presidential Suite", "Page 9, Was told by hotel staff that Trump stayed there", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-06-17T12:00:00-05:00", "2016-06-17T12:05:00-05:00", "Danchenko Travels from Moscow to London to meet Steele", "Page 9, Supposedly where 'pee' tapes were made", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-06-14T12:00:00-05:00", "2016-06-14T12:05:00-05:00", "Danchenko posts selfie with Charles Dolan Travels", "Page 9, In Red Square", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-10-04T12:00:00-05:00", "2016-10-04T12:05:00-05:00", "Danchenko and Charles Dolan Go To Moscow", "Page 10, For conference attended by Russian Intelligence", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-07-22T12:00:00-05:00", "2016-07-22T12:05:00-05:00", "Charles Dolan EMails Russian Sub-Source 1", "Page 11, Sub Source wanted Hillary's Autograph", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-08-19T12:00:00-05:00", "2016-08-19T12:05:00-05:00", "Danchenko asks Charles Dolan for Info to put into Dossier", "Page 14, to pass to Steele", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-08-20T12:00:00-05:00", "2016-08-20T12:05:00-05:00", "Charles Dolan E-Mails Danchenko about Trump Campaign Manager", "Page 15, the Trump team doesn't like him", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2017-06-15T12:00:00-05:00", "2017-06-15T12:05:00-05:00", "Danchenko Lies to FBI", "Page 17, FBI asks if Charles Dolan told him anything that showed up in Steele Dossier and he said 'no'", EVENT_TYPE_FBI )
  add_event( child_file, "2016-05-31T12:00:00-05:00", "2016-05-31T12:05:00-05:00", "Charles Dolan told by Russian Embassy staff that Russian Diplomat being recalled in September", "Page 22, head of Russian Embassy's Economic Section", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-08-02T12:00:00-05:00", "2016-08-02T12:05:00-05:00", "Charles Dolan meets Russian Diplomat 1", "Page 22, head of Russian Embassy's Economic Section", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-08-19T12:00:00-05:00", "2016-08-19T12:05:00-05:00", "Russian Diplomat 1 EMails Charles Dolan about beig replaced", "Page 22, 'by a talented diplomat and economist with impressive experience in American studies'", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-09-13T12:00:00-05:00", "2016-09-13T12:05:00-05:00", "Russian Diplomat 1 calls Danchenko", "Page 23", EVENT_TYPE_DANCHENKO )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "594155360-78-Gov-Motion-in-Limine-Danchenko-Copy.pdf")
  #child_file.tag("Court Filing", "In Limine")
  
  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/594155360/78-Gov-Motion-in-Limine-Danchenko-Copy"
  url.localfilename = "594155360-78-Gov-Motion-in-Limine-Danchenko-Copy.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2022-09-13T18:06:00-05:00")
  url.save()

  add_event( child_file, "2017-03-01T12:00:00-05:00", "2017-06-15T12:00:00-05:00", "Danchenko becomes paid confidential human source", "Page 3", EVENT_TYPE_FBI )
  add_event( child_file, "2017-06-15T12:00:00-05:00", "2017-06-15T12:00:00-05:00", "Danchenko Lies FBI about Charles Dolan", "Page 3", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-02-24T12:00:00-05:00", "2016-02-24T12:00:00-05:00", "Danchenko emails Cenk Sidar telling him to make up sources", "Page 5", EVENT_TYPE_DANCHENKO )

  url = parent_file.newurl()
  url.url = "https://technofog.substack.com/p/igor-danchenko-trial-revelations"
  url.localfilename = "594155360-78-Gov-Motion-in-Limine-Danchenko-Copy.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2022-10-17T16:25:00-05:00")
  url.save()

  add_event( child_file, "2016-06-16T12:00:00-00:00", "2016-06-16T12:00:00-00:00", "Danchenko is in Moscow meeting with Charles Dolan", "Day 3 of Danchenko trial, FBI Special Agent Kevin Helson testimony", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-06-18T12:00:00-00:00", "2016-06-18T12:00:00-00:00", "Danchenko is in London to give a report to Christopher Steele", "Day 3 of Danchenko trial, FBI Special Agent Kevin Helson testimony", EVENT_TYPE_DANCHENKO )
  add_event( child_file, "2016-10-03T12:00:00-00:00", "2016-10-03T12:00:00-00:00", "Danchenko is in London to give a report to Christopher Steele", "FBI offers $1 million to Christopher Steele for hard evidence backing dossier claims", EVENT_TYPE_FBI )

  return None

def add_crossfire_razor_files(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn Advises Trump.pdf")
  url = child_file.newurl()
  url.url = "https://www.reuters.com/article/us-usa-election-trump-advisor-idUSMTZSAPEC2Q6G3JRH"
  url.localfilename = "Flynn Advises Trump.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2016-02-26T18:06:00-05:00")
  url.save()

  add_event( child_file, "2016-02-26T12:00:00-05:00", "2016-02-26T12:05:00-05:00", "Michael Flynn joins Trump campaign", "https://www.reuters.com/article/us-usa-election-trump-advisor-idUSMTZSAPEC2Q6G3JRH", EVENT_TYPE_CAMPAIGN )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Trump Names Flynn NSA.pdf")

  url = child_file.newurl()
  url.url = "https://www.politico.com/story/2016/11/michael-flynn-national-security-adviser-231591"
  url.localfilename = "Trump Names Flynn NSA.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-11-17T21:40:00-05:00")
  url.save()

  add_event( child_file, "2016-11-17T21:00:00-05:00", "2016-11-17T21:00:00-05:00", "Trump chooses Flynn as National Security Advisor", "https://www.politico.com/story/2016/11/michael-flynn-national-security-adviser-231591", EVENT_TYPE_CAMPAIGN )

  url = child_file.newurl()
  url.url = "https://www.politico.com/story/2016/07/trump-putin-no-relationship-226282"
  url.localfilename = "Trump urges Russia to hack Clinton's email - POLITICO.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2016-07-27T01:59:00-05:00")
  url.save()

  add_event( child_file, "2016-07-27T01:59:00-05:00", "2016-07-27T01:59:00-05:00", "Report: Flynn had dinner in Moscow", "Politico", EVENT_TYPE_FLYNN )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/120919-examination.pdf")

  url = child_file.newurl()
  url.url = "https://www.justice.gov/storage/120919-examination.pdf"
  url.localfilename = "120919-examination.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-09-01T12:00:00-05:00")
  url.save()

  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:00:00-05:00", "FBI opens Crossfire Dragon (Page Investigation)", "FBI IG Report page 59, Foreign Agents Registration Act (FARA) case on Flynn", EVENT_TYPE_FBI )
  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:00:00-05:00", "FBI opens Crossfire Fury (Manafort Investigation)", "FBI IG Report page 59, Foreign Agents Registration Act (FARA) case on Flynn", EVENT_TYPE_FBI )
  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:00:00-05:00", "FBI opens Crossfire Typhoon (Papadopoulos Investigation)", "FBI IG Report page 59, Foreign Agents Registration Act (FARA) case on Flynn", EVENT_TYPE_FBI )
  add_event( child_file, "2016-08-16T12:00:00-05:00", "2016-08-16T12:00:00-05:00", "FBI opens Crossfire Razor (Flynn Investigation)", "FBI IG Report page 59, Foreign Agents Registration Act (FARA) case on Flynn", EVENT_TYPE_FBI )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/From Russia with love why the Kremlin backs Trump Reuters.pdf")
  url = child_file.newurl()
  url.url = "https://www.reuters.com/article/us-usa-election-trump-russia-idUSKCN0WQ1FA"
  url.localfilename = "From Russia with love why the Kremlin backs Trump Reuters.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2016-03-24T09:28:00-00:00")
  url.save()

  add_event( child_file, "2016-03-24T09:28:00-05:00", "2016-03-24T09:28:00-05:00", "Report: Michael Flynn had dinner in Moscow", "Earliest report I could find", EVENT_TYPE_FLYNN )

  add_flynn_unmasking(parent_file)
  add_flynn(parent_file)
  add_pientka_briefing(parent_file)
  add_pientka_testimony(parent_file)
  add_ignatius(parent_file)
  add_schrage(parent_file)
  add_exhibit5(parent_file)

  return None

def add_crossfire_dragon_files(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/120919-examination.pdf")

  url = child_file.newurl()
  url.url = "https://www.justice.gov/storage/120919-examination.pdf"
  url.localfilename = "120919-examination.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-09-01T12:00:00-05:00")
  url.save()

  # 456781456-2018-DOJ-Letter-to-FISC.pdf
  add_event( child_file, "2017-01-12T12:00:00-05:00", "2017-01-12T12:05:00-05:00", "FISA warrant renewed on Carter Page", "Docket 2017-0052 FBI IG Report Executive Summary page VI, Page 209, Signed by Judge Michael W. Mosman", EVENT_TYPE_FISA )
  add_event( child_file, "2017-04-07T12:00:00-05:00", "2017-04-07T12:05:00-05:00", "FISA warrant renewed on Carter Page", "Docket 2017-0375 FBI IG Report Executive Summary page VI", EVENT_TYPE_FISA )
  add_event( child_file, "2017-06-29T12:00:00-05:00", "2017-06-29T12:05:00-05:00", "FISA warrant renewed on Carter Page", "Docket 2017-0679 FBI IG Report Executive Summary page VI", EVENT_TYPE_FISA )
  # add_event( child_file, "2016-10-21T12:00:00-05:00", "2017-09-21T12:00:00-05:00", "Carter Page under FISA surveillance", "FBI IG Report Executive Summary page VI", EVENT_TYPE_FISA )
  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:00:00-05:00", "FBI opens Foreign Agents Registration Act (FARA) case on Carter Page (Crossfire Dragon)", "FBI IG Report page 59", EVENT_TYPE_FBI )
  add_event( child_file, "2016-08-17T12:00:00-05:00", "2016-08-17T12:00:00-05:00", "CIA tells Crossfire Hurricane that Carter Page was an asset for five years", "FBI IG Report page 79, notification known as August 17 Memorandum", EVENT_TYPE_CIA )
  add_event( child_file, "2016-08-20T12:00:00-05:00", "2016-08-20T12:00:00-05:00", "FBI CHS operation 1 - Carter Page", "FBI IG Report page 317", EVENT_TYPE_FBI )
  add_event( child_file, "2016-10-17T12:00:00-05:00", "2016-10-17T12:00:00-05:00", "FBI CHS operation 1 Part 2 - Carter Page", "FBI IG Report page 320", EVENT_TYPE_FBI )
  add_event( child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "FBI CHS operation 1 Part 3 - Carter Page", "FBI IG Report page 323", EVENT_TYPE_FBI )
  add_event( child_file, "2017-01-25T12:00:00-05:00", "2017-01-25T12:00:00-05:00", "FBI CHS operation 1 Part 4 - Carter Page asked if he knew Flynn", "FBI IG Report page 325", EVENT_TYPE_FBI )

  return None

def add_trump_campaign_events(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Campaign.txt")
  add_event( child_file, "2015-06-16T11:00:00-05:00", "2015-06-16T12:00:00-05:00", "Trump announces candidacy", "At Trump Tower on Fifth Avenue", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-07-19T17:55:00-05:00", "2016-07-19T19:11:00-05:00", "Trump becomes Republican nominee", "Trump becomes Republican nominee", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-11-08T23:00:00-05:00", "2016-11-08T23:59:00-05:00", "Trump elected", "Election results are in", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2017-01-20T12:00:00-05:00", "2017-01-20T13:00:00-05:00", "Trump sworn in", "45th President", EVENT_TYPE_CAMPAIGN )

  # Primaries
  add_event( child_file, "2016-02-01T12:00:00-05:00", "2016-02-01T12:05:00-05:00", "Iowa Primary Cruz 8 delegates Trump 7", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN)
  add_event( child_file, "2016-02-09T12:00:00-05:00", "2016-02-09T12:05:00-05:00", "New Hampshire primary Trump 11 delegates (18 total)", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-02-20T12:00:00-05:00", "2016-02-20T12:05:00-05:00", "South Carolina primary Trump 50 delegates (68 total)", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-02-23T12:00:00-05:00", "2016-02-23T12:05:00-05:00", "Nevada primary Trump 14 delegates (82 total)", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-03-01T12:00:00-05:00", "2016-03-01T12:05:00-05:00", "Super Tuesday primary Trump 255 delegates (337 total)", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )

  # Withdrawals
  add_event( child_file, "2016-05-04T12:00:00-05:00", "2016-05-04T12:05:00-05:00", "John Kasich suspends campaign", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-05-03T12:00:00-05:00", "2016-05-03T12:05:00-05:00", "Ted Kruz suspends campaign", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-03-15T12:00:00-05:00", "2016-03-15T12:05:00-05:00", "Marco Rubio suspends campaign", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-03-04T12:00:00-05:00", "2016-03-04T12:05:00-05:00", "Ben Carson suspends campaign", "https://en.wikipedia.org/wiki/Results_of_the_2016_Republican_Party_presidential_primaries", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-03-21T12:00:00-05:00", "2016-03-21T12:05:00-05:00", "Trump names Carter Page and Papadopoulos as Foreign Policy team to Washington Post", "Fred Ryan reporter, Lee Smith page 36", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-03-28T12:00:00-05:00", "2016-03-28T12:05:00-05:00", "Paul Manafort hired by Trump", "https://www.nytimes.com/politics/first-draft/2016/03/28/donald-trump-hires-paul-manafort-to-leaddelegate-effort/", EVENT_TYPE_CAMPAIGN )

  # https://www.theguardian.com/us-news/2016/may/26/donald-trump-delegates-count-republican-nomination-news-campaign-2016
  add_event( child_file, "2016-05-26T12:00:00-05:00", "2016-05-26T12:05:00-05:00", "Trump secures enough delegates to be nominee", "https://www.theguardian.com/us-news/2016/may/26/donald-trump-delegates-count-republican-nomination-news-campaign-2016", EVENT_TYPE_CAMPAIGN )
  return None

def add_steele_dossier(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Images/Christopher Steele.png")
  exif = child_file.newexif()
  exif.latitude = 51.487329
  exif.longitude = -0.124057
  exif.make = "Universal"
  exif.model = "Minute 16"
  exif.devicetime = datetime.fromisoformat("2016-04-01T12:00:00-05:00")
  exif.save()

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Trump-Intelligence-Allegations.pdf")
  #child_file.tag("Steele Report", "Several reports")

  url = child_file.newurl()
  url.url = "https://www.documentcloud.org/documents/3259984-Trump-Intelligence-Allegations.html"
  url.localfilename = "Trump-Intelligence-Allegations.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-01T12:00:00-05:00")
  url.save()

  artifact = child_file.newartifact()
  assert isinstance(artifact, truxton.TruxtonArtifact)
  artifact.type = truxton.ENTITY_TYPE_AUTHOR
  artifact.value = "Christopher Steele"
  artifact.datatype = truxton.DATA_TYPE_ASCII
  artifact.length = 18
  artifact.save()

  add_event( child_file, "2016-06-20T12:00:00-05:00", "2016-06-20T12:05:00-05:00", "Steele report 2016/080 - Russia Cultivating Trump for 5 Years (First report Steele actually authored)", "Page 1 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-06-26T12:00:00-05:00", "2016-06-26T12:05:00-05:00", "Steele report 2016/086 - Russia Cyber Operations Synposis", "Corrected Date, original was 2015-07-26 (Copy Pasta) Page 4 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-07-19T12:00:00-05:00", "2016-07-19T12:05:00-05:00", "Steele report 2016/094 - Secret Carter Page Meeting Report", "Page 9 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-07-20T12:00:00-05:00", "2016-07-20T12:05:00-05:00", "Steele report 2016/095 - Extensive Conspiracy Trump Russia (mentions Manafort and Carter Page)", "Date Approximate. Page 7 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-07-30T12:00:00-05:00", "2016-07-30T12:05:00-05:00", "Steele report 2016/097 - Kremlin Concerned about DNC Hacking", "Page 11 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-08-05T12:00:00-05:00", "2016-08-05T12:05:00-05:00", "Steele report 2016/100 - DNC Hacking Backlash/Trump Withdrawing", "Page 13 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:05:00-05:00", "Steele report 2016/101 - Kremlin Outlines Pro-Trump Efforts (mentions Flynn and Carter Page)", "Page 15 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-08-10T12:00:00-05:00", "2016-08-10T12:05:00-05:00", "Steele report 2016/102 - Trump Camp Reaction to Russian Interference", "Page 17 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-08-22T12:00:00-05:00", "2016-08-22T12:05:00-05:00", "Steele report 2016/105 - Demise of Manafort", "Page 20 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-09-14T12:00:00-05:00", "2016-09-14T12:05:00-05:00", "Steele report 2016/111 - Kremlin Fallout from Media Exposure", "Page 22 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-09-14T12:00:00-05:00", "2016-09-14T12:05:00-05:00", "Steele report 2016/112 - Kremlin Alpha Group Cooperation", "Page 25 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-09-14T12:00:00-05:00", "2016-09-14T12:05:00-05:00", "Steele report 2016/113 - Trump Sex Parties in St. Petersburg", "Page 27 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-10-12T12:00:00-05:00", "2016-10-12T12:05:00-05:00", "Steele report 2016/130 - Kremlin Assessment of Trump", "Page 28 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  # On 2016-10-07, Steele had been told by the FBI of the 4 Crossfire investigations
  add_event( child_file, "2016-10-18T12:00:00-05:00", "2016-10-18T12:05:00-05:00", "Steele report 2016/134 - Further Details of Kremlin Liaison (mentions Carter Page)", "Page 30 - Confirms Sechin-Carter Page meeting. Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-10-19T12:00:00-05:00", "2016-10-19T12:05:00-05:00", "Steele report 2016/135 - Important Role of Cohen (mentions Manafort and Carter Page)", "Page 32 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-10-20T12:00:00-05:00", "2016-10-20T12:05:00-05:00", "Steele report 2016/136 - Cohen Secret Liaison with Kremlin (mentions Manafort and Carter Page)", "Page 18 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)
  add_event( child_file, "2016-12-13T12:00:00-05:00", "2016-12-13T12:05:00-05:00", "Steele report 2016/166 - Further Details Secret Dialog/Hackers in Prague (mentions Manafort and Carter Page)", "Page 34 - Trump-Intelligence-Allegations.pdf", EVENT_TYPE_STEELE)

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "February 9, 2017 Electronic Communication (Danchenko Interview).pdf")
  #child_file.tag("FD-1057", "FBI Electronic Communication", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.judiciary.senate.gov/imo/media/doc/February%209,%202017%20Electronic%20Communication.pdf"
  url.localfilename = "February 9, 2017 Electronic Communication.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-02-09T12:00:00-05:00")
  url.save()

  add_event( child_file, "2017-02-09T12:00:00-05:00", "2017-02-09T12:00:00-05:00", "FBI sends Steele primary subsource (Danchenko) summary", "Page 2 - February 9, 2017 Electronic Communication.pdf", EVENT_TYPE_FBI)
  add_event( child_file, "2017-01-24T13:30:00-05:00", "2017-01-24T17:00:00-05:00", "FBI interviews Steele's primary subsource Igor Danchenko", "Page 5 - February 9, 2017 Electronic Communication.pdf", EVENT_TYPE_FBI)
  add_event( child_file, "2017-01-25T12:00:00-05:00", "2017-01-25T12:00:00-05:00", "FBI interviews Steele's primary subsource Igor Danchenko", "Page 24 - February 9, 2017 Electronic Communication.pdf", EVENT_TYPE_FBI)
  add_event( child_file, "2017-01-26T12:00:00-05:00", "2017-01-26T12:00:00-05:00", "FBI interviews Steele's primary subsource Igor Danchenko", "Page 42 - February 9, 2017 Electronic Communication.pdf", EVENT_TYPE_FBI)
  add_event( child_file, "2016-03-15T12:00:00-05:00", "2016-03-15T12:00:00-05:00", "Steele tasks Danchenko to collect information on Manafort", "Page 13 - Date Approximate.", EVENT_TYPE_STEELE )
  # https://ifoundthepss.blogspot.com/2020/07/unmistakable-proof.html thinks the primary source is
  # Igor Danchenko
  return None
  
def add_mccabe_page_messages(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "McCabe Page Text.pdf")
  child_file.tag("Text Messages", "The main McCabe<->Page Messages", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/402770650/Mccabe-Page-Text"
  url.localfilename = "McCabe Page Text.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-01T12:00:00-05:00")
  url.save()
  
  # These timestamps are BS, they all in in a whole minute
  m = mccabe_to_page(child_file, "2016-10-12T19:11:00-00:00", "OI now has a robust explanation re any possible bias of the chs in the package. Don't know what the holdup is now, other than Stu's continued concerns. Strong operational need to have in place before Monday if at all possible, which means to ct tomorrow. I communicated you and boss's green light to Stu earlier, and just sent an email to Stu asking where things stood. This might take a high-level push. Will keep you posted.")
  m.addnote("OI - Office of Intelligence, chs - Confidential Human Source")
  mccabe_to_page(child_file, "2016-10-12T19:13:00-05:00", "If I have not heard back from Stu in an hour, I will invoke your name to say you want to know where things are, so long as that is okay with you.")
  mccabe_to_page(child_file, "2016-10-12T21:07:00-05:00", "Spoke to Stu. Let's talk in the morning.")
  mccabe_to_page(child_file, "2016-10-12T22:15:00-05:00", "Expect John C. will probably reach out in the morning as well. Just call when you're up. Thx.")
  mccabe_to_page(child_file, "2016-10-13T10:14:00-05:00", "Please. \U0001f60a")
  mccabe_to_page(child_file, "2016-10-13T10:14:01-05:00", "Call my cell when you are free to chat.")
  mccabe_to_page(child_file, "2016-10-13T10:23:00-05:00", "Also, let me know if there is a --Redacted-- that you are related to. I'm guessing not, but just wanted to check.")
  mccabe_to_page(child_file, "2016-10-13T11:00:00-05:00", "Rgr. Thanks.")
  page_to_mccabe(child_file, "2016-10-13T11:00:01-05:00", "Call u after 830")
  page_to_mccabe(child_file, "2016-10-13T11:00:02-05:00", "No Sam I am.")
  page_to_mccabe(child_file, "2016-10-13T11:47:00-05:00", "Ready. Office or cell?")
  mccabe_to_page(child_file, "2016-10-13T11:48:00-05:00", "Cell please")
  mccabe_to_page(child_file, "2016-10-13T20:00:00-05:00", "Correction: CD says letter was def CD-1 fake. NFI from me, but they likely have more.")
  mccabe_to_page(child_file, "2016-10-14T09:54:00-05:00", "You haven't heard from State, correct? We gave them until 10 am eastern to raise their concerns. Our plan is to proceed with the unredacted production to the Hill if we don't hear anything in the next few minutes.")
  page_to_mccabe(child_file, "2016-10-14T10:29:00-05:00", "I have not heard anything from them.")
  mccabe_to_page(child_file, "2016-10-14T10:43:00-05:00", "Can you follow up with Neil again? I spoke to Tash, she also had the same understanding that we cold go alone.\n\nAlso, it would be very very helpful to get DDCIA to clarify that they DO want the content. The DAG continues to use that as an excuse.")
  mccabe_to_page(child_file, "2016-10-14T10:44:00-05:00", "Finally, it looks like BA did not get the call from the senator's ofc, that was inaccurate. BA has it now.")
  page_to_mccabe(child_file, "2016-10-14T10:45:00-05:00", "Ok. Thanks.")
  page_to_mccabe(child_file, "2016-10-14T10:47:00-05:00", "I told Neils office you would be the point person on setting it up for us. Maybe you can call his assistant and ask her if he is ready to schedule. If the answer is no, then tell her I will need to talk to him again.")
  page_to_mccabe(child_file, "2016-10-14T10:48:00-05:00", "She is --Redacted--")
  mccabe_to_page(child_file, "2016-10-14T10:51:00-05:00", "Got it. Will call now.")
  m = mccabe_to_page(child_file, "2016-10-14T10:57:00-05:00", "I also have moffa writing up everything cyd knows about what is on those drives. Will be ready by monday.")
  m.addnote("cyd - FBI Cyber Division")
  mccabe_to_page(child_file, "2016-10-14T10:57:01-05:00", "Just called. Apparently the DAG now wants to be there, and WH wants DOJ to host. So we are setting that up now.\n\nWe will very much need to get Cohen's view before we meet with her. Better, have him weigh in with her before the meeting. We need to speak with one voice, if that is in fact the case.")
  page_to_mccabe(child_file, "2016-10-14T11:27:00-05:00", "Thanks. I will reach out to David.")
  mccabe_to_page(child_file, "2016-10-15T18:48:01-05:00", "Quick press response awaiting your clearance on unclassified email. Could you check it out please?")
  page_to_mccabe(child_file, "2016-10-15T18:52:00-05:00", "Can't take your call as I am in a session. If necessary I can step out. I read the response and it seems fine, with the exception of the use of the term \"billets\". Too military and may not be understood.")
  mccabe_to_page(child_file, "2016-10-15T18:53:01-05:00", "No problem.")
  page_to_mccabe(child_file, "2016-10-15T18:53:01-05:00", "See if you can change it to something like \"space for additional fbi employees assigned abroad\"")
  mccabe_to_page(child_file, "2016-10-15T18:53:03-05:00", "Got it. Just needed clearance on the statement. Will let the team know. Thanks.")
  page_to_mccabe(child_file, "2016-10-15T18:54:00-05:00", "Need me to step out and call?")

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "McCabe Page Text.pdf")
  child_file.tag("Text Messages", "The main McCabe<->Page Messages", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/403323155/McCabe-Page-Meeting-Text"
  url.localfilename = "McCabe Page Text.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-03-27T12:00:00-05:00")
  url.save()  
  
  mccabe_to_page(child_file, "2016-11-15T19:19:00-05:00", "16 packages tomorrow. 4 may come separately because the still need to be signed.")
  m = mccabe_to_page(child_file, "2016-11-16T14:32:00-05:00", "Hey can you call me on your way back. One flag for the sac svtc.")
  m.addnote("svtc - Secure Video Teleconference")
  mccabe_to_page(child_file, "2016-11-16T15:01:00-05:00", "Never mind. Solved.")
  mccabe_to_page(child_file, "2016-11-17T20:28:00-05:00", "An article to share: Trump offers retired Lt. Gen. Michael Flynn the job of national security advisor, a person close to the transition says Trump offers retired Lt. Gen. Michael Flynn the job of national security adviser, a person close to the transition says http://wapo.st/2g186WC")
  mccabe_to_page(child_file, "2016-11-18T05:39:00-05:00", "I tried sending an email to --Redacted-- but it bounced back. Are you still getting the --Redacted-- emails? DAG inquired about our plan re that FISA target if he mobilizes, given the physical access he has. Let me know if you got the email I forwarded from Tash.")
  page_to_mccabe(child_file, "2016-12-12T22:16:01-05:00", "This is the piece that I just --Garbled-- source:\n\n\"U.S. Intelligence officials said the CIA has identified the \"actors\" who took possession of those stolen files and delivered them to WikiLeaks. The individuals are known for their affiliations to Russian intelligence services, but \"one step\" removed from the Russian government.\"\n\nThat is from the Post. Let's confirm tomorrow with CY and CD if they have any idea what this refers to.")
  m = mccabe_to_page(child_file, "2016-12-12T22:33:00-05:00", "Btw, Clapper told Pete that he (Clapper) was meeting with Brennan and Cohen for dinner tonight. Just FYSA")
  m.addnote("FYSA - For Your Situational Awareness")
  page_to_mccabe(child_file, "2016-12-12T22:34:01-05:00", "OK")
  mccabe_to_page(child_file, "2017-01-10T19:05:00-05:00", "Times has it.\n\nNYTimes: Unsubstantiated Report Has Compromising Information on Trump, Intelligence Chiefs Say\nUnsubstantiated Report Has Compromising Information on Trump, Intelligence Chiefs Say http://nyti.ms/2jsp4xR")
  mccabe_to_page(child_file, "2017-01-30T19:06:00-05:00", "There could be 11 packages tomorrow, but I think 8 still need ogc signature. Just fyi.")
  page_to_mccabe(child_file, "2017-01-30T21:25:00-05:00", "I guess those packages won't be going anywhere.")
  mccabe_to_page(child_file, "2017-01-30T21:33:00-05:00", "Ha. I guess not.")
  m = mccabe_to_page(child_file, "2017-02-01T21:44:00-05:00", "You see this?\n\nhttp://wapo.st/2ktHlOX")
  m.addnote("'This was the worst call by far': Trump badgered, bragged and abruptly ended phone call with Australian leader")
  page_to_mccabe(child_file, "2017-02-01T22:20:00-05:00", "Yikes")
  page_to_mccabe(child_file, "2017-02-05T22:20:00-05:00", "Hitting weygandt after")
  # Completed

  return None

def add_strzok_page_messages(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/06.27.18 Interview Of Peter Strzok.pdf")
  #child_file.tag("Testimony", "House Intelligence Committee")

  url = child_file.newurl()
  url.url = "https://dougcollins.house.gov/sites/dougcollins.house.gov/files/06.27.18 Interview Of Peter Strzok.pdf"
  url.localfilename = "06.27.18 Interview Of Peter Strzok.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-01T12:00:00-05:00")
  url.save()

  # Add location for Peter Strzok "3214 Prince William Dr, Fairfax, VA"
  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_HOME
  location.label = "Peter Strzok - 3214 Prince William Drive"
  location.latitude = 38.859329
  location.longitude = -77.268657
  location.when = datetime.fromisoformat("2012-11-26T13:00:00-05:00")
  location.save()

  # Add location for Lisa Page "1229 D Street NE, Washington DC"
  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_HOME
  location.label = "Lisa Page - 1229 D Street NE"
  location.latitude = 38.89466133697017
  location.longitude = -76.98922009969064
  location.when = datetime.fromisoformat("2012-11-26T13:00:00-05:00")
  location.save()

  url = child_file.newurl()
  url.url = "https://dougcollins.house.gov/sites/dougcollins.house.gov/files/06.27.18 Interview Of Peter Strzok.pdf"
  url.localfilename = "06.27.18 Interview Of Peter Strzok.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-01T12:00:00-05:00")
  url.save()

  add_event( child_file, "2017-08-27T12:00:00-05:00", "2017-08-27T13:00:00-05:00", "Strzok Removed From Russia Investigation", "Page 38 - 06.27.18 Interview Of Peter Strzok.pdf", EVENT_TYPE_MUELLER)
  add_event( child_file, "2016-08-06T12:00:00-05:00", "2016-08-06T12:01:00-05:00", "Strzok to Page: F Trump", "Page 41 - 06.27.18 Interview Of Peter Strzok.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  add_event( child_file, "2016-08-06T12:02:00-05:00", "2016-08-06T12:03:00-05:00", "Strzok to Page: I can protect country and many levels", "Page 42 - 06.27.18 Interview Of Peter Strzok.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event( child_file, "2016-08-06T12:04:00-05:00", "2016-08-06T12:05:00-05:00", "Strzok to Page: We'll stop it", "Page 42 - 06.27.18 Interview Of Peter Strzok.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  # Need to check the following three dates
  add_event( child_file, "2016-08-15T12:00:00-05:00", "2016-08-15T12:05:00-05:00", "Strzok to Page: I want to believe the path that you set forth in Andy's office but feel we can't take the risk", "Page 48 - 06.27.18 Interview Of Peter Strzok.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  add_event( child_file, "2017-08-18T12:00:00-05:00", "2016-08-18T12:05:00-05:00", "Strzok to Page: Text message about investigation leading to impeachment", "Page 48 - 06.27.18 Interview Of Peter Strzok.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  add_event( child_file, "2017-08-22T12:00:00-05:00", "2016-08-22T12:05:00-05:00", "Strzok to Page: God, I suddenly want on this. You know why", "Page had sent him a Washington Post article, Page 53 - 06.27.18 Interview Of Peter Strzok.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE)

  add_strzok_page_messages_appendix_c(parent_file)
  add_strzok_page_lync_messages(parent_file)
  return None

  # https://www.foxnews.com/politics/strzok-page-texts-reveal-personal-relationship-between-fbi-official-and-judge-recused-from-flynn-case
  # https://www.grassley.senate.gov/download/lync_text-messages-of-peter-strzok-from-2-13-16-to-12-6-17

def add_ignatius(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/Ignatius.pdf")

  url = child_file.newurl()
  url.url = "https://www.washingtonpost.com/opinions/why-did-obama-dawdle-on-russias-hacking/2017/01/12/75f878a0-d90c-11e6-9a36-1d296534b31e_story.html?itid=lk_inline_manual_28&itid=lk_inline_manual_34"
  url.localfilename = "Ignatius.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-12T12:00:00-05:00")
  url.save()

  artifact = child_file.newartifact()
  artifact.type = truxton.ENTITY_TYPE_AUTHOR
  artifact.value = "David Ignatius"
  artifact.datatype = truxton.DATA_TYPE_ASCII
  artifact.length = 14
  artifact.save()

  e = add_event( child_file, "2017-01-11T12:00:00-05:00", "2017-01-11T12:00:00-05:00", "Flynn Dec 29th phone call leaked to Washington Post", "David Ignatius", EVENT_TYPE_FBI)
  e.tag("Leak", "Source unknown", truxton.TAG_ORIGIN_HUMAN)
  add_event( child_file, "2017-01-12T12:00:00-05:00", "2017-01-12T12:00:00-05:00", "David Ignatius article about Flynn-Kislyac phone call published", "David Ignatius", EVENT_TYPE_FBI)
  return None

def add_papadopoulos(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Papadopoulos/Daily Caller 2018.pdf")
  #child_file.tag("News Article", "Papadopoulos London Meeting", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://dailycaller.com/2018/03/25/george-papadopoulos-london-emails/"
  url.localfilename = "Daily Caller 2018.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2018-03-25T21:47:00-05:00")
  url.save()

  added_event = add_event( child_file, "2016-09-13T12:00:00-05:00", "2016-09-13T12:05:00-05:00", "Stefan Halper (FBI) brings Azra Turk (CIA?) to meet Papadopoulos in London", "At the Connaught Hotel", EVENT_TYPE_FBI )
  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "Connaught Hotel: Stefan Halper (FBI) and Azra Turk (CIA?) meet Papadopoulos"
  location.latitude = 51.51022
  location.longitude = -0.149774
  location.when = datetime.fromisoformat("2018-09-13T12:00:00-05:00")
  location.save()

  relation = child_file.newrelation()
  relation.a = added_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Papadopoulos/Papadopoulos-Statement-Offense.pdf")

  url = child_file.newurl()
  url.url = "https://assets.documentcloud.org/documents/4163402/Papadopoulos-Statement-Offense.pdf"
  url.localfilename = "Papadopoulos-Statement-Offense.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-10-05T12:00:00-05:00")
  url.save()

  add_event( child_file, "2017-02-16T12:00:00-05:00", "2017-02-16T12:05:00-05:00", "Kevin Clinesmith (FBI) interviews Papadopoulos (2nd time)", "Second interview", EVENT_TYPE_FBI)
  arrest_event = add_event( child_file, "2017-07-27T12:00:00-05:00", "2017-07-27T12:05:00-05:00", "Papadopoulos arrested", "Page 13 - At Dulles Airport", EVENT_TYPE_FBI)
  add_event( child_file, "2016-03-06T12:00:00-05:00", "2016-03-06T12:05:00-05:00", "Papadopoulos begins work on campaign", "Starts work", EVENT_TYPE_CAMPAIGN)
  e = add_event( child_file, "2016-03-24T12:00:00-05:00", "2016-03-24T12:05:00-05:00", "Joseph Mifsud (CIA?) brings Female Russian national (Olga Polonskaya/Vinogradova) to meet Papadopoulos", "Meeting in London", EVENT_TYPE_MIFSUD)
  e.tag("CIA", "Mifsud probably on CIA payroll", truxton.TAG_ORIGIN_HUMAN)
  add_event( child_file, "2017-01-27T12:00:00-05:00", "2017-01-27T12:05:00-05:00", "FBI interviews Papadopoulos", "First interview", EVENT_TYPE_FBI )
  email_event = add_event( child_file, "2016-04-26T12:00:00-05:00", "2016-04-26T12:05:00-05:00", "Joseph Mifsud (CIA?) tells Papadopoulos 'the Russians had emails of Clinton'", "Andaz Hotel in London. 'Thousands of emails'", EVENT_TYPE_MIFSUD)
  meeting_event = add_event( child_file, "2016-03-14T12:00:00-05:00", "2016-03-14T12:05:00-05:00", "Joseph Mifsud (CIA?) meets Papadopoulos in Italy", "Meets at Link Campus Italy", EVENT_TYPE_MIFSUD)
  add_event( child_file, "2016-03-31T12:00:00-05:00", "2016-03-31T12:05:00-05:00", "Papadopoulos attends meeting with Trump", "National Security Meeting in DC", EVENT_TYPE_CAMPAIGN)
  add_event( child_file, "2016-04-10T12:00:00-05:00", "2016-04-10T12:05:00-05:00", "Papadopoulos emails female Russian national", "National Security Meeting in DC", EVENT_TYPE_CAMPAIGN)

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_ARREST
  location.label = "FBI Arrests Papadopoulos"
  location.latitude = 38.953576
  location.longitude = -77.446585
  location.when = datetime.fromisoformat("2017-07-27T12:00:00-05:00")
  location.save()

  relation = child_file.newrelation()
  relation.a = arrest_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "Mifsud (CIA?) tells Papadopoulos Russians have Clinton emails at Andaz Hotel"
  location.latitude = 51.51722
  location.longitude = -0.081385
  location.when = datetime.fromisoformat("2016-04-26T12:00:00-05:00")
  location.save()

  relation = child_file.newrelation()
  relation.a = email_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "Mifsud (CIA?) meets Papadopoulos at Link Campus"
  location.latitude = 41.892695
  location.longitude = 12.43284
  location.when = datetime.fromisoformat("2016-03-14T12:00:00-05:00")
  location.save()

  relation = child_file.newrelation()
  relation.a = meeting_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Papadopoulos/Halper Pay Stubs.pdf")
  payment_1 = add_event( child_file, "2016-09-17T12:00:00-05:00", "2016-09-17T12:05:00-05:00", "FBI pays Halper $282,295", "Award ID HQ003416P0148", EVENT_TYPE_FBI)
  payment_2 = add_event( child_file, "2017-07-26T12:00:00-05:00", "2017-07-26T12:05:00-05:00", "FBI pays Halper $129,280", "Award ID HQ003416P0148", EVENT_TYPE_FBI)

  # HQ003415C0100, https://www.usaspending.gov/#/award/CONT_AWD_HQ003415C0100_9700_-NONE-_-NONE-
  add_event( child_file, "2016-09-27T12:00:00-05:00", "2016-09-27T12:05:00-05:00", "DOD pays Halper $244,960", "Award ID HQ003415C0100", EVENT_TYPE_FBI)

  # Add location for Stefan Halper "126 Commonage Dr, Great Falls, VA 22066, USA" as listed in https://govtribe.com/vendors/halper-stefan-6qy62
  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_HOME
  location.label = "Stefan Halper - 126 Commonage Drive"
  location.latitude = 39.038287
  location.longitude = -77.304136
  location.when = datetime.fromisoformat("2017-07-26T12:00:00-05:00")
  location.save()

  relation = child_file.newrelation()
  relation.a = payment_1.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  relation = child_file.newrelation()
  relation.a = payment_2.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  url = child_file.newurl()
  url.url = "https://www.fpds.gov/ezsearch/fpdsportal?q=HALPER%2C+STEFAN+PIID%3A%22HQ003416P0148%22&s=FPDS&templateName=1.4&indexName=awardfull&x=0&y=0"
  url.localfilename = "Halper Pay Stubs.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-07-26T12:00:00-05:00")
  url.save()

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "mifsud 302 page 1.png")

  url = child_file.newurl()
  url.url = "https://twitter.com/Techno_Fog/status/1300998748722601984"
  url.localfilename = "mifsud 302 page 1.png"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-09-01T23:27:00-05:00")
  url.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "FBI interviews Mifsud at Omni Shoreham Hotel, DC"
  location.latitude = 38.92260758111932
  location.longitude = -77.05372325063354
  location.when = datetime.fromisoformat("2017-02-11T12:00:00-05:00")
  location.save()

  interview_event = add_event( child_file, "2017-02-10T08:00:00-05:00", "2017-02-10T08:05:00-05:00", "FBI interviews Mifsud", "First line of 302 says the date is Feb 11th but most other reporting says 10th. Mifsud said he didn't tell Papadopoulos about emails", EVENT_TYPE_FBI)

  relation = child_file.newrelation()
  relation.a = interview_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Eg4jwTHXsAAfQmp.jpg")

  url = child_file.newurl()
  url.url = "https://twitter.com/FOOL_NELSON/status/1301016657045999618/photo/1"
  url.localfilename = "Eg4jwTHXsAAfQmp.jpg"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-09-02T00:38:00-05:00")
  url.save()

  add_event( child_file, "2017-02-11T10:16:00-05:00", "2017-02-11T10:16:00-05:00", "Mifsud emails FBI", "Follow-up to interview", EVENT_TYPE_MIFSUD)

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "455711240-Transcript-of-Papadopoulos-s-Oct-31-2016-conversation-with-FBI-informant.pdf")
  add_event( child_file, "2016-10-31T13:05:00-05:00", "2016-10-31T14:00:00-05:00", "FBI CHS meets Papadopoulos", "CHS: I gotta golden job, man", EVENT_TYPE_FBI)
  
  add_name_and_email( child_file, "Joseph Mifsud", "j.mifsud@stir.ac.uk" )

  return None
  
def add_hrpt(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "HRPT-115-1.pdf")

  url = child_file.newurl()
  url.url = "https://web.archive.org/web/20180502222750/https://docs.house.gov/meetings/IG/IG00/20180322/108023/HRPT-115-1.pdf"
  url.localfilename = "HRPT-115-1.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2018-05-25T00:00:00-05:00")
  url.save()

  add_event( child_file, "2016-11-15T12:00:00-05:00", "2016-11-15T12:05:00-05:00", "CIA/FBI/NSA Fusion Cell shuts down", "HPSCI Report on Russian Active Measures, Chapter 3, report page 38 (PDF page 48)", EVENT_TYPE_CIA )
  return None

def add_12333(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Raw-12333-surveillance-sharing-guidelines.pdf")

  url = child_file.newurl()
  url.url = "https://www.documentcloud.org/documents/3283349-Raw-12333-surveillance-sharing-guidelines.html"
  url.localfilename = "Raw-12333-surveillance-sharing-guidelines.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-03T00:00:00-05:00")
  url.save()

  add_event( child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "James Clapper (DNI) lowers privacy protections on raw SIGINT", "Page 26. This allows US-Persons data to be disseminated more broadly.", EVENT_TYPE_DNI)
  add_event( child_file, "2017-01-03T12:00:00-05:00", "2017-01-03T12:00:00-05:00", "Loretta Lynch (DOJ) approves James Clapper (DNI) loosening restrictions on raw SIGINT", "Page 26. This allows US-Persons data to be disseminated more broadly", EVENT_TYPE_DNI)
  return None

def add_ec(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "JW-v-DOJ-reply-02743.pdf")

  url = child_file.newurl()
  url.url = "https://www.judicialwatch.org/documents/jw-v-doj-reply-02743/"
  url.localfilename = "JW-v-DOJ-reply-02743.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-05-20T00:00:00-05:00")
  url.save()

  add_event( child_file, "2016-07-31T12:00:00-05:00", "2016-07-31T12:00:00-05:00", "Crossfire Hurricane created", "Page 5. At FBI HQ", EVENT_TYPE_FBI )
  add_event( child_file, "2016-07-27T12:00:00-05:00", "2016-07-27T12:00:00-05:00", "Legat called needing to meet US ambassador", "Page 6. In London", EVENT_TYPE_FBI )
  add_event( child_file, "2016-07-29T12:00:00-05:00", "2016-07-29T12:00:00-05:00", "FBI receives Downer info from 'Legat'", "Page 5. Probably legal attache London", EVENT_TYPE_FBI )
  return None

def add_nytimes_1(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Code Name Crossfire Hurricane.pdf")
  #child_file.tag("News Article", "News report", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.nytimes.com/2018/05/16/us/politics/crossfire-hurricane-trump-russia-fbi-mueller-investigation.html"
  url.localfilename = "Code Name Crossfire Hurricane.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-05-16T00:00:00-05:00")
  url.save()

  add_event( child_file, "2016-07-31T12:00:00-05:00", "2016-07-31T13:00:00-05:00", "Crossfire Hurricane created by Edward William (Bill) Priestap", "100 days from election", EVENT_TYPE_FBI )
  add_event( child_file, "2016-08-15T12:00:00-05:00", "2016-08-15T12:05:00-05:00", "CIA Director Brennan shares intelligence with FBI Director Comey", "Russians interfered with election", EVENT_TYPE_CIA )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Annotated New York Times Article.pdf")

  url = child_file.newurl()
  url.url = "https://www.judiciary.senate.gov/imo/media/doc/Annotated%20New%20York%20Times%20Article.pdf"
  url.localfilename = "Annotated New York Times Article.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-02-14T00:00:00-05:00")
  url.save()

  add_event( child_file, "2017-02-14T12:00:00-05:00", "2017-02-14T13:00:00-05:00", "Strzok - 'No contact between any Trump official and Russian Intel'", "Matt Apuzzo - friend of Lisa Page, write this article. Issues lots of NSLs but finds no evidence of anything", EVENT_TYPE_FBI )

  return None

def add_daily_caller_1(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Papadopoulos/FBI Lawyer Who Sent Anti-Trump Resistance Text Message Interviewed George Papadopoulos The Daily Caller.pdf")

  url = child_file.newurl()
  url.url = "https://dailycaller.com/2018/06/25/clinesmith-interviewed-papadopoulos/"
  url.localfilename = "FBI Lawyer Who Sent Anti-Trump Resistance Text Message Interviewed George Papadopoulos The Daily Caller.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-06-25T00:00:00-05:00")
  url.save()

  add_event( child_file, "2016-11-09T12:00:00-05:00", "2016-11-09T12:00:00-05:00", "Kevin Clinesmith (FBI) texts 'I am numb'", "text message", EVENT_TYPE_FBI )
  add_event( child_file, "2017-02-16T12:00:00-05:00", "2017-02-16T12:00:00-05:00", "Kevin Clinesmith (FBI) interviews Papadopoulos", "ff", EVENT_TYPE_FBI )
  return None

def add_election_polling_data(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "RealClearPolitics - 2016 Republican Presidential Nomination.pdf")

  url = child_file.newurl()
  url.url = "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html"
  url.localfilename = "RealClearPolitics - 2016 Republican Presidential Nomination.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-01T00:00:00-05:00")
  url.save()

  add_event( child_file, "2015-07-13T12:00:00-05:00", "2015-07-13T12:00:00-05:00", "Jeb Bush polling at 17.8% Trump 9.3%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2015-08-08T12:00:00-05:00", "2015-08-08T12:00:00-05:00", "Trump polling at 24.3% Jeb Bush 12.5%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2015-09-19T12:00:00-05:00", "2015-09-19T12:00:00-05:00", "Trump polling at 30.5% Ben Carson 20.0% Bush 7.8%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2015-11-05T12:00:00-05:00", "2015-11-05T12:00:00-05:00", "Ben Carson polling at 24.8% Trump 24.6% Bush 5.8%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-01-09T12:00:00-05:00", "2016-01-09T12:00:00-05:00", "Trump polling at 30.4% Ted Cruz 20.7%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-02-20T20:40:00-05:00", "2016-02-20T20:43:00-05:00", "Jeb Bush suspends campaign", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-02-28T12:00:00-05:00", "2016-02-28T12:00:00-05:00", "Trump polling at 32.8% Ted Cruz 20.4%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-03-15T12:00:00-05:00", "2016-03-15T12:00:00-05:00", "Trump polling at 32% Ted Cruz 26%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-03-24T12:00:00-05:00", "2016-03-24T12:00:00-05:00", "Trump polling at 43% Ted Cruz 30.3%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-04-11T12:00:00-05:00", "2016-04-11T12:00:00-05:00", "Trump polling at 39% Ted Cruz 32.3%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-05-04T12:00:00-05:00", "2016-05-04T12:00:00-05:00", "Trump polling at 56.4% Ted Cruz 27%", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  add_event( child_file, "2016-05-04T20:27:00-05:00", "2016-05-04T20:41:00-05:00", "Ted Cruz suspends campaign", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_CAMPAIGN )
  return None

def add_downer_meeting(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "What happened when Trump campaign aide George Papadopoulos sat down with Australian diplomat Alexander Downer.pdf")

  url = child_file.newurl()
  url.url = "https://www.abc.net.au/news/2018-09-22/george-papadopoulos-alexander-downer-meeting-what-happened/10286868"
  url.localfilename = "What happened when Trump campaign aide George Papadopoulos sat down with Australian diplomat Alexander Downer.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2018-09-21T00:03:22-00:00")
  url.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "Papadopoulos meets Alexander Downer at Kensington Wine Rooms"
  location.latitude = 51.507290
  location.longitude = -0.194820
  location.when = datetime.fromisoformat("2016-05-10T18:00:00-00:00")
  location.save()

  add_event(child_file, "2016-05-10T18:00:00-08:00", "2016-05-10T20:00:00-00:00", "Papadopoulos meets Alexander Downer (Australian) in London", "At Kensington Wine Rooms. Papadopoulos repeats Mifsud's 14-day old story of Russians having Clinton emails to Downer", EVENT_TYPE_DOWNER )
  return None

def add_clapper_testimony(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "HPSCI Testimony/James Clapper 20170717.pdf")
  #child_file.tag("Testimony", "Senate Intelligence Committee")

  url = child_file.newurl()
  url.url = "https://intelligence.house.gov/UploadedFiles/JC7.pdf"
  url.localfilename = "James Clapper 20170717.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-07-17T00:03:22-00:00")
  url.save()

  add_event(child_file, "2016-12-13T12:00:00-05:00", "2016-12-13T12:00:00-05:00", "Brennan (CIA) tells Clapper (DNI) about dossier", "Page 30 - Clapper said 'second week of December'", EVENT_TYPE_CIA )
  add_event(child_file, "2017-01-03T12:00:00-05:00", "2017-01-03T12:00:00-05:00", "Robert Litt (DNI-OGC) tells Clapper (DNI) of Flynn-Kislyak call", "Page 35 - from his General Council - Bob Litt", EVENT_TYPE_DNI )
  add_event(child_file, "2017-01-19T18:00:00-05:00", "2017-01-19T18:00:00-05:00", "Clapper (DNI) discusses Flynn-Kislyak call with Comey (FBI) and Brennan (CIA)", "Page 39 - Very alarmed VP Pence defended Flynn on TV. Clapper only had gist of conversation, not transcript", EVENT_TYPE_DNI )
  add_event(child_file, "2017-07-17T09:34:00-05:00", "2017-07-17T09:34:00-05:00", "Clapper (DNI) never saw any evidence of collusion", "Page 26 - 'I never saw any direct empirical evidence that the Trump campaign or someone in it was plotting/conspiring with the Russians to meddle with the election.'", EVENT_TYPE_DNI )
  return None

def add_barnett_302(parent_file: truxton.TruxtonChildFileIO) -> None:

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/477421887-Flynn-filing-9-24-2020.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/477421887/Flynn-filing-9-24-2020"
  url.localfilename = "477421887-Flynn-filing-9-24-2020.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-09-25T00:13:34-05:00")
  url.save()
  
  # Barnett said on page 7 that the investigation had three phases
  # Something was discovered on Jan 4, 2017 that he didn't think was significant
  # Phase 1 - Opening of case until 2017-01-04
  # Phase 2 - 2017-01-04 until 2017-01-24 (Flynn Interview)
  # Phase 3 - 2017-01-24 until present

  # SSA 1 is Pientka? Pientka is SSA in CI briefing
  # SA 1 is Pientka?
  # SCO Atty 1 is most likely Brandon Van Grack (https://www.emptywheel.net/2020/09/25/sidney-powell-accuses-william-barnett-of-outrageous-deliberate-misconduct-and-kenneth-kohl-hides-evidence-that-brandon-van-grack-did-not/)

  e = add_event(child_file, "2016-08-01T12:00:00-05:00", "2016-08-01T12:00:00-05:00", "Date Approximate. William J. Barnett (FBI) Joins Crossfire Razor", "Page 3. Joe Pientka asked him.", EVENT_TYPE_FBI )
  e = add_event(child_file, "2016-09-12T12:00:00-05:00", "2016-09-12T12:00:00-05:00", "Date Approximate. William J. Barnett (FBI) still can't find a reason for Crossfire Razor to exist", "Page 4. After six weeks on the investigation, he is unsure of the basis of the investigation.", EVENT_TYPE_FBI )

  e = add_event(child_file, "2016-11-08T12:00:00-05:00", "2016-11-08T12:00:00-05:00", "William J. Barnett (FBI) request to close Flynn case is denied", "Page 5. Special Agent In Charge of Washington Field Office made the request up the chain but was denied.", EVENT_TYPE_FBI )
  e.tag("Crossfire Razor", "Barnett requests to close case", truxton.TAG_ORIGIN_HUMAN)
  e = add_event(child_file, "2016-12-25T12:00:00-05:00", "2016-12-28T12:00:00-05:00", "Strzok orders Flynn case closed", "Page 6. William J. Barnett (FBI) begins drafting document.", EVENT_TYPE_FBI )
  e.tag("Crossfire Razor", "Strzok orders case closed", truxton.TAG_ORIGIN_HUMAN)
  e = add_event(child_file, "2017-01-04T14:21:00-05:00", "2017-01-04T14:21:00-05:00", "Joe Pientka (FBI) tells William J. Barnett (FBI) to not close Flynn case", "Page 6. Said Peter Strzok (FBI) has information to add to the file.", EVENT_TYPE_FBI )
  e.tag("Crossfire Razor", "Pientka tells Barnett to keep it open", truxton.TAG_ORIGIN_HUMAN)
  add_event(child_file, "2017-01-04T14:21:00-05:00", "2017-01-04T14:21:00-05:00", "William J. Barnett (FBI) told of Logan Act", "Page 7. He was provided the transcript of the Flynn phone call, read it a couple of times and did not see a significant issue. He had never heard of the Logan Act.", EVENT_TYPE_FBI )
  e = add_event(child_file, "2017-01-09T12:00:00-05:00", "2017-01-09T12:00:00-05:00", "Analysts purchase Professional Liability insurance", "Page 7. Intelligence analysts on Flynn case start taking out insurance.", EVENT_TYPE_FBI )
  e.tag("Unhappy", "Afraid they will be prosecuted", truxton.TAG_ORIGIN_HUMAN)
  e = add_event(child_file, "2017-02-06T12:00:00-05:00", "2017-02-06T12:00:00-05:00", "William J. Barnett (FBI) requests removal from Flynn case", "Page 8. Believes an IG investigation of the case will take place", EVENT_TYPE_FBI )
  e.tag("Unhappy", "Barnett asks to be removed from case, felt an IG investigation coming", truxton.TAG_ORIGIN_HUMAN)
  add_event(child_file, "2017-01-04T14:21:00-05:00", "2017-01-25T12:00:00-05:00", "Pientka tells William J. Barnett (FBI) of Flynn Interview", "Page 7. Apologizes Barnett was not consulted or asked to participate.", EVENT_TYPE_FBI )
  return None

def add_russia_intel(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "09-29-20_Letter to Sen. Graham_Declassification of FBI's Crossfire Hurricane Investigations_20-00912_U_SIGNED-FINAL.pdf")

  url = child_file.newurl()
  url.url = "https://www.judiciary.senate.gov/imo/media/doc/09-29-20_Letter%20to%20Sen.%20Graham_Declassification%20of%20FBI's%20Crossfire%20Hurricane%20Investigations_20-00912_U_SIGNED-FINAL.pdf"
  url.localfilename = "09-29-20_Letter to Sen. Graham_Declassification of FBI's Crossfire Hurricane Investigations_20-00912_U_SIGNED-FINAL.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-09-29T00:00:00-05:00")
  url.save()

  add_event(child_file, "2016-07-20T12:00:00-05:00", "2016-07-20T12:00:00-05:00", "US Intelligence learns Russian Intelligence is aware of Hillary approves scandal plans", "Plan was to tie Trump with Putin.", EVENT_TYPE_CIA )
  add_event(child_file, "2016-07-26T12:00:00-05:00", "2016-07-26T12:00:00-05:00", "John Brennan (CIA) briefs Obama on Hillary's plan", "Plan was the idea of one of her foreign policy advisors.", EVENT_TYPE_CIA )
  add_event(child_file, "2016-09-07T12:00:00-05:00", "2016-09-07T12:00:00-05:00", "CIA gave Investigative Referral to Comey (FBI) and Strzok (FBI) about Hillary's Russia plan", "U.S. Presidential candidate Hillary Clinton's approval of a plan concerning U.S. Presidential candidate Donald Trump and Russian hackers hampering U.S. elections as a means of distracting the public from her use of a private mail server.", EVENT_TYPE_CIA )
  return None

def add_brennan(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Opinion _ John Brennan_ Trump will suffocate the intelligence community to get reelected - The Washington Post.pdf")

  url = child_file.newurl()
  url.url = "https://www.washingtonpost.com/opinions/2020/08/31/john-brennan-trump-national-intelligence-congress/"
  url.localfilename = "Opinion _ John Brennan_ Trump will suffocate the intelligence community to get reelected - The Washington Post.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-08-31T19:06:00-05:00")
  url.save()

  add_event(child_file, "2016-07-28T12:00:00-05:00", "2016-07-28T12:00:00-05:00", "Brennan (CIA) briefs Obama that Putin authorized ops against Hillary", "Chief of Staff Denis McDonough also there. 'I informed him in a hurriedly scheduled meeting that Russian President Vladimir Putin had authorized his intelligence services to carry out activities to hurt Democratic candidate Hillary Clinton and boost the election prospects of Donald Trump.'", EVENT_TYPE_CIA )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "ENCLOSURE_1__Brennan_Notes__U.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/478963703/Enclosure-1-Brennan-Notes-u"
  url.localfilename = "ENCLOSURE_1__Brennan_Notes__U.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-10-06T12:00:00-05:00")
  url.save()

  add_event(child_file, "2016-07-26T12:00:00-05:00", "2016-07-26T12:00:00-05:00", "Hillary approves plan to villify Trump", "Or so the Russians think", EVENT_TYPE_HILLARY )
  add_event(child_file, "2016-07-28T12:00:00-05:00", "2016-07-28T12:00:00-05:00", "Brennan (CIA) briefs Obama, Susan Rice, James Comey (FBI) and Denis McDonough that Hillary approved plan to manufacture Trump-Russia scandal", "CITE alleged approved by Hillary Clinton on 26 July of a proposed from one of her foreign policy advisors (Jake Sullivan) to villify Donald Trump by stirring up a scandal claiming interference by The Russian Security Services.", EVENT_TYPE_CIA )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "ENCLOSURE_2__DCIA_Memo_09-07-16__U.pdf")
  #child_file.tag("Memo","CIA to FBI informing them of Hillary's Russian Collusion plan")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/478965057/Enclosure-2-Dcia-Memo-09-07-16-u"
  url.localfilename = "ENCLOSURE_2__DCIA_Memo_09-07-16__U.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-10-06T12:00:00-05:00")
  url.save()

  add_event(child_file, "2016-09-07T12:00:00-05:00", "2016-09-07T12:00:00-05:00", "CIA formally informs Peter Strzok (FBI) and Crossfire Hurricane Fusion Cell of Hillary's plan", "Audio interception discussing Hillary's approval of plan to tie Donald Trump and Russian hackers to distract from her use of a private email server", EVENT_TYPE_CIA )

  return None

def add_ohr(parent_file: truxton.TruxtonChildFileIO) -> None:

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "480057685-2020-10-13-Submission-SJC-SSCI-Part-2-of-2.pdf")
  #child_file.tag("FD-302", "Bruce Ohr 302", truxton.TAG_ORIGIN_HUMAN)
  #child_file.tag("FD-1087", "USB Thumb Drive - Nellie Ohr Research for Fusion GPS", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/480057685/2020-10-13-Submission-SJC-SSCI-Part-2-of-2"
  url.localfilename = "480057685-2020-10-13-Submission-SJC-SSCI-Part-2-of-2.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-10-14T00:03:15-05:00")
  url.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "Bruce Ohr interviewed at FBI Washington Field Office"
  location.latitude = 38.897728
  location.longitude = -77.015607
  location.when = datetime.fromisoformat("2017-05-08T12:00:00-05:00")
  location.save()

  # Now add the SanDisk Cruzer Glide 8GB
  usb = child_file.newusb()
  usb.vendorid = 1921
  usb.productid = 21808
  usb.when = datetime.fromisoformat("2016-12-20T11:00:00-05:00")
  usb.save()

  # Ohr had given FBI another thumbdrive on 12 Dec 2016 with Steele's research
  add_event(child_file, "2016-12-20T11:00:00-05:00", "2016-12-20T11:00:00-05:00", "Bruce Ohr gives Fusion GPS research to FBI", "Nellie Ohr's open source research while employed by Fusion GPS, 8GB SanDisk Cruzer Glide Thumb Drive, page 3", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-20T12:00:00-05:00", "2017-01-20T12:00:00-05:00", "Glenn Simpson (Fusion GPS) contacts Bruce Ohr (DOJ)", "Steele's employees will be named, page 4", EVENT_TYPE_STEELE )
  add_event(child_file, "2017-01-21T12:08:00-05:00", "2017-01-21T08:00:00-05:00", "Steele (Fusion GPS) contacts Bruce Ohr (DOJ)", "Steele's employee will need help quickly, page 5", EVENT_TYPE_STEELE )
  add_event(child_file, "2017-01-23T12:00:00-05:00", "2017-01-23T12:00:00-05:00", "Bruce Ohr interviewed by FBI", " page 4", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-25T12:00:00-05:00", "2017-01-25T12:00:00-05:00", "Bruce Ohr interviewed by FBI", " page 6", EVENT_TYPE_FBI )
  add_event(child_file, "2017-05-03T08:00:00-05:00", "2017-05-03T08:00:00-05:00", "Steele calls Ohr", "Says business is good", EVENT_TYPE_STEELE )

  return None

def add_flynn_kislyak_phone_calls(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/463573448-Flynn-Calls-1.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/463573448/Flynn-Calls-1"
  url.localfilename = "463573448-Flynn-Calls-1.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-09-29T00:03:15-05:00")
  url.save()

  add_event(child_file, "2016-12-23T12:00:00-05:00", "2016-12-23T12:00:00-05:00", "Kislyak calls Flynn", "Page 1. Discuss working together against radical Islamist.", EVENT_TYPE_FLYNN )
  add_event(child_file, "2016-12-29T12:00:00-05:00", "2016-12-29T12:00:00-05:00", "Flynn calls Kislyak", "Page 7. 'Make it reciprocal. Don't make it - don't go any further than you have to. Because I don't want us to get into something that has to escalate, on a, you know, on a tit for tat.'", EVENT_TYPE_FLYNN )
  add_event(child_file, "2016-12-31T12:00:00-05:00", "2016-12-31T12:00:00-05:00", "Kislyak calls Flynn", "Page 11. Kislyak says cooler heads prevailed, discuss meetings in future.", EVENT_TYPE_FLYNN )
  add_event(child_file, "2017-01-12T12:00:00-05:00", "2017-01-12T12:00:00-05:00", "Kislyak calls Flynn", "Page 15. Talk about sending team to Astana.", EVENT_TYPE_FLYNN )
  add_event(child_file, "2017-01-19T12:00:00-05:00", "2017-01-19T12:00:00-05:00", "Kislyak calls Flynn", "Page 19. Kislyak leaves voice mail.", EVENT_TYPE_FLYNN )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/463573453-Flynn-Calls-2.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/463573453/Flynn-Calls-2"
  url.localfilename = "463573453-Flynn-Calls-2.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-09-29T00:03:15-05:00")
  url.save()

  add_event(child_file, "2016-01-05T12:00:00-05:00", "2016-01-05T12:00:00-05:00", "Flynn calls Kislyak", "Page 1. Flynn expresses condolences about death of GRU Director Sergun.", EVENT_TYPE_FLYNN )
  add_event(child_file, "2016-12-22T12:00:00-05:00", "2016-12-22T12:00:00-05:00", "Flynn calls [RADACTED]", "Page 2. Fully redacted.", EVENT_TYPE_FLYNN )
  return None

def add_flynn_NSLs(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/477876530-US-v-Flynn-Flynn-NSL-filing.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/477876530/US-v-Flynn-Flynn-NSL-filing"
  url.localfilename = "477876530-US-v-Flynn-Flynn-NSL-filing.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-09-29T00:03:15-05:00")
  url.save()

  add_event(child_file, "2016-12-23T12:13:40-05:00", "2016-12-23T12:13:40-05:00", "Kevin Clinesmith (FBI) 'No further NSLs are authorized for Razor'", "Page 4. Heavily redacted email.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-02-02T12:00:00-05:00", "2017-02-02T12:00:00-05:00", "Peter Strzok (FBI) authorizes NSL on Flynn phone #1", "Page 6. For the period of July 1 2015 to February 2 2017.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-02-07T12:00:00-05:00", "2017-02-07T12:00:00-05:00", "Peter Strzok (FBI) authorizes NSL on Flynn email #1", "Page 6. For the period of July 15 2015 to February 7 2017.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-02-07T12:00:00-05:00", "2017-02-07T12:00:00-05:00", "Peter Strzok (FBI) authorizes NSL on Flynn phone #2", "Page 6. For the period of August 1 2016 to February 7 2017.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-02-23T12:00:00-05:00", "2017-02-23T12:00:00-05:00", "Peter Strzok (FBI) authorizes NSL on Flynn phone #3", "Page 7. Toll records for the period of January 1 2016 to February 23 2017.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-02-23T12:00:00-05:00", "2017-02-23T12:00:00-05:00", "Peter Strzok (FBI) authorizes NSL on Flynn phone #4 and #5", "Page 7. Toll records for the period of January 1 2016 to February 23 2017.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-02-23T12:00:00-05:00", "2017-02-23T12:00:00-05:00", "Peter Strzok (FBI) authorizes NSL on Flynn email #2", "Page 7. For the period of inception to February 23 2017.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-03-07T12:00:00-05:00", "2017-03-07T12:00:00-05:00", "Peter Strzok (FBI) authorizes NSL on Flynn phone #6", "Page 7. Subscriber and transactional information for the period of December 21 2016 to January 15 2017.", EVENT_TYPE_FBI )
  return None

def add_flynn_filing_10_26(parent_file: truxton.TruxtonChildFileIO) -> None:

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/481804147-DOJ-Flynn-Filing-October-26-2020.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/481804147/DOJ-Flynn-Filing-October-26-2020"
  url.localfilename = "481804147-DOJ-Flynn-Filing-October-26-2020.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-10-26T00:03:15-05:00")
  url.save()

  return None

def add_fbi_spreadsheet(parent_file: truxton.TruxtonChildFileIO) -> None:

  # Bruce Ohr 302's
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "479781400-Steele-Spreadsheet-1.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/479781400/Steele-Spreadsheet-1"
  url.localfilename = "479781400-Steele-Spreadsheet-1.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-10-12T00:03:22-00:00")
  url.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "McCain told of Steele Dossier by Sir Andrew Wood"
  location.latitude = 44.6401547974541
  location.longitude = -63.56827859791606
  location.when = datetime.fromisoformat("2016-11-18T12:00:00-05:00")
  location.save()
  return None
  
def add_mccabe_donations(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Mcaullif Donations to McCabe.pdf")
  
  url = child_file.newurl()
  url.url = "https://www.vpap.org/candidates/257116/donor/248345/?start_year=all&end_year=all&contrib_type=all"
  url.localfilename = "Mcaullif Donations to McCabe.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2022-11-13T00:03:15-05:00")
  url.save()
  
  m = add_event(child_file, "2015-06-09T12:00:00-05:00", "2015-06-09T12:00:00-05:00", "Jill McCabe Receives $7,500 from Terry McAuliffe", "Wife of Andrew McCabe, her first-ever campaign Page 1. She raised $1,668,014, twice the amount of her opponent she lost to.", EVENT_TYPE_FBI )
  m = add_event(child_file, "2015-06-19T12:00:00-05:00", "2015-06-19T12:00:00-05:00", "Jill McCabe Receives $7,500 from Terry McAuliffe ($15,000 total)", "Wife of Andrew McCabe, her first-ever campaign Page 1. She raised $1,668,014, twice the amount of her opponent she lost to.", EVENT_TYPE_FBI )
  m = add_event(child_file, "2015-08-31T12:00:00-05:00", "2015-08-31T12:00:00-05:00", "Jill McCabe Receives $2,500 from Terry McAuliffe ($17,500 total)", "Wife of Andrew McCabe, her first-ever campaign Page 1. She raised $1,668,014, twice the amount of her opponent she lost to.", EVENT_TYPE_FBI )
  m = add_event(child_file, "2015-10-01T12:00:00-05:00", "2015-10-01T12:00:00-05:00", "Jill McCabe Receives $150,000 from Terry McAuliffe ($167,500 total)", "Wife of Andrew McCabe, her first-ever campaign Page 1. She raised $1,668,014, twice the amount of her opponent she lost to.", EVENT_TYPE_FBI )
  m = add_event(child_file, "2015-10-27T12:00:00-05:00", "2015-10-27T12:00:00-05:00", "Jill McCabe Receives $125,000 from Terry McAuliffe ($292,500 total)", "Wife of Andrew McCabe, her first-ever campaign Page 1. She raised $1,668,014, twice the amount of her opponent she lost to.", EVENT_TYPE_FBI )
  m = add_event(child_file, "2015-10-29T12:00:00-05:00", "2015-10-29T12:00:00-05:00", "Jill McCabe Receives $175,000 from Terry McAuliffe ($467,500 total)", "Wife of Andrew McCabe, her first-ever campaign Page 1. She raised $1,668,014, twice the amount of her opponent she lost to.", EVENT_TYPE_FBI )
  # Schaufeld

  return None

def add_flynn_motion_to_dismiss(parent_file: truxton.TruxtonChildFileIO) -> None:

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/460365255-Flynn-motion-to-dismiss.pdf")

  m = add_event(child_file, "2017-01-03T12:00:00-05:00", "2017-01-03T12:00:00-05:00", "Andrew McCabe tells Mary McCord of Flynn investigation and Kislayk phone call.", "Page 32", EVENT_TYPE_FBI )
  m.addnote("Obama administration couldn't figure out why Russians weren't reacting to sanctions. They believed that Flynn (whom they hated) must be the cause.")
  add_event(child_file, "2017-01-13T12:00:00-05:00", "2017-01-13T12:00:00-05:00", "FBI briefs DOJ on background Flynn investigation call. Strzok, Priestap, Sally Moyer", "Page 33", EVENT_TYPE_FBI )
  m = add_event(child_file, "2017-01-15T12:00:00-05:00", "2017-01-15T12:00:00-05:00", "Pence on Face the Nation", "Page 33", EVENT_TYPE_FBI )
  m.addnote("McCord upset that Pence lied. Said Flynn didn't discuss sanctions.")
  add_event(child_file, "2017-01-19T12:00:00-05:00", "2017-01-19T12:00:00-05:00", "Comey visiting ODNI", "Page 35", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-24T12:00:00-05:00", "2017-01-24T12:00:00-05:00", "Yates calls Comey to force him to tell White House of Flynn investigation, Comey tells her he was interviewed that day. Yates dumbfounded.", "Page 35", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:11:00-05:00", "2017-01-04T14:11:00-05:00", "From Strzok: Hey if you havent closed --Redacted-- don't do it yet", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:12:00-05:00", "2017-01-04T14:12:00-05:00", "From Strzok: Sorry, RAZOR", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:14:00-05:00", "2017-01-04T14:14:00-05:00", "From Strzok: Hey if you havent closed RAZOR, don't do so yet", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:15:00-05:00", "2017-01-04T14:15:00-05:00", "To Strzok: Okay", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:15:01-05:00", "2017-01-04T14:15:01-05:00", "From Strzok: Still open right?", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:15:02-05:00", "2017-01-04T14:15:02-05:00", "From Strzok: And youre case agent? Going to send you [RADACTED] for the file", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:15:03-05:00", "2017-01-04T14:15:03-05:00", "To Strzok: I have not closed it, I'll double check to see if --Redacted-- had done it.", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:17:00-05:00", "2017-01-04T14:17:00-05:00", "To Strzok: Still open and I'm still listed as the Case Manager (had to double check)", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:18:00-05:00", "2017-01-04T14:18:00-05:00", "From Strzok: Rgr. I couldn't raise --Redacted-- earlier. Pls keep it open for now", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:18:01-05:00", "2017-01-04T14:18:01-05:00", "To Strzok: Will do", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:19:00-05:00", "2017-01-04T14:19:00-05:00", "Strzok to Page: Razor still open", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:21:00-05:00", "2017-01-04T14:21:00-05:00", "To Strzok: Anything I can help with?", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:22:00-05:00", "2017-01-04T14:22:00-05:00", "From Strzok: Just need to relay to him not to close RAZOR yet. I talked with --Redacted--", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:22:15-05:00", "2017-01-04T14:22:15-05:00", "To Strzok: Oh, OK", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:22:30-05:00", "2017-01-04T14:22:30-05:00", "To Strzok: What's up?", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:22:45-05:00", "2017-01-04T14:22:45-05:00", "From Strzok: Need to decide what to do with him w/r/t the --Redacted--", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:22:50-05:00", "2017-01-04T14:22:50-05:00", "From Strzok: 7th floor involved.", "Page 77", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:23:00-05:00", "2017-01-04T14:23:00-05:00", "To Strzok: I heard that might be the case yesterday. Did DD send that material over?", "Page 77. NOTE: Jan 3 was when Clapper learned of Flynn-Kislyak phone call.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:23:10-05:00", "2017-01-04T14:23:10-05:00", "To Strzok: --Redacted-- has been handling RAZOR's closure -- do you want me to reach out to him?", "Page 77.", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:24:00-05:00", "2017-01-04T14:24:00-05:00", "From Strzok: Yes", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:24:10-05:00", "2017-01-04T14:24:10-05:00", "To Strzok: Will do", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:24:20-05:00", "2017-01-04T14:24:20-05:00", "From Strzok: Hey don't close RAZOR", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:24:30-05:00", "2017-01-04T14:24:30-05:00", "From Strzok: actually, just got him on Lync", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:24:40-05:00", "2017-01-04T14:24:40-05:00", "From Strzok: Has he been doing the bulk of the work on him?>", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:25:00-05:00", "2017-01-04T14:25:00-05:00", "To Strzok: He's been doing the some of the stuff more recently", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:25:10-05:00", "2017-01-04T14:25:10-05:00", "From Strzok: Actually, his green bubble just turned yellow, pls do try and reach him", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T14:25:20-05:00", "2017-01-04T14:25:20-05:00", "To Strzok: Will do", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T15:59:00-05:00", "2017-01-04T15:59:00-05:00", "--Redacted--: have you seen the latest --Redacted--?", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T15:59:05-05:00", "2017-01-04T15:59:05-05:00", "--Redacted--: on the yellow side? yes ... --Redacted--?", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T15:59:10-05:00", "2017-01-04T15:59:10-05:00", "--Redacted--: to give you a thumb nail i heard pete say, 'Andy and Bill will interview...'", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T15:59:20-05:00", "2017-01-04T15:59:20-05:00", "--Redacted--: yep", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T15:59:30-05:00", "2017-01-04T15:59:30-05:00", "--Redacted--: lemme get more clarity before i give you more", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T16:00:00-05:00", "2017-01-04T16:00:00-05:00", "--Redacted--: Bill meaning Preistep, correct?", "Page 78", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-04T16:08:00-05:00", "2017-01-04T16:08:00-05:00", "--Redacted--: nope - barnett", "Page 78", EVENT_TYPE_FBI )

  strzok_to_page(child_file, "2017-01-04T14:19:00-05:00", "Razor still open. :@ but serendipitously good, I guess. You want those chips and oreos ?")
  page_to_strzok(child_file, "2017-01-04T14:19:30-05:00", "phew.")
  page_to_strzok(child_file, "2017-01-04T14:20:00-05:00", "But yeah, that's amazing that he is still open. Good, I guess." )
  strzok_to_page(child_file, "2017-01-04T14:20:30-05:00", "Yeah, our utter incompetence actually helps us. 20% of the time, I'm guessing :)")
  strzok_to_page(child_file, "2017-01-23T06:37:00-05:00", "We'll see, about Bill. He was pretty adamant about what Andy it said with regard to that. And he mentioned on Saturday that he had several conversations.")
  strzok_to_page(child_file, "2017-01-23T06:37:20-05:00", "with Andy. Bill sense with it and he wanted to know why we had to go aggressively doing these things, openly. I worry Bill isn't getting the underlying")
  strzok_to_page(child_file, "2017-01-23T06:37:40-05:00", "distinction that I think is clear. But maybe I'm wrong.")

  # Left off here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  add_event(child_file, "2017-01-24T12:35:00-05:00", "2017-01-24T12:35:00-05:00", "Flynn calls McCabe", "Exhibit 11 Page 94", EVENT_TYPE_FBI )
  return None

def add_obama_flynn_warning(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/obama-flynn-warning.pdf")

  url = child_file.newurl()
  url.url = "https://www.nytimes.com/2017/05/08/us/politics/obama-flynn-trump.html"
  url.localfilename = "obama-flynn-warning.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-07-10T00:03:22-00:00")
  url.save()

  add_event(child_file, "2016-11-10T09:00:00-05:00", "2016-11-10T10:30:00-05:00", "Obama tells Trump of his 'profound concerns' about Flynn", "Told Trump at White House", EVENT_TYPE_OBAMA )
  return None

def add_flynn(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/gov.uscourts.dcd.191592.237.1.pdf")

  url = child_file.newurl()
  url.url = "https://intelligence.house.gov/UploadedFiles/JC7.pdf"
  url.localfilename = "https://www.courtlistener.com/recap/gov.uscourts.dcd.191592/gov.uscourts.dcd.191592.237.1.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-07-10T00:03:22-00:00")
  url.save()

  add_event(child_file, "2017-01-25T12:00:00-05:00", "2017-01-25T12:00:00-05:00", "FBI briefs NSD, ODAG - Determines Flynn not acting as agent of Russia", "Flynn very open and forthcoming, page 10", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-25T11:30:00-05:00", "2017-01-25T11:30:00-05:00", "DOJ - George: No reasonable aros to Logan Act", "Strzok notes page 6", EVENT_TYPE_FBI )
  e = add_event(child_file, "2017-01-10T00:00:00-05:00", "2017-01-10T00:00:00-05:00", "James Clapper (DNI) tells David Ignatius (Washington Post) Flynn story", "Page 22, unconfirmed", EVENT_TYPE_DNI )
  e.tag("Leak", "DNI leaks to Washington Post", truxton.TAG_ORIGIN_HUMAN)

  add_barnett_302(parent_file)
  add_flynn_NSLs(parent_file)
  add_flynn_filing_10_26(parent_file)
  add_flynn_kislyak_phone_calls(parent_file)
  add_flynn_motion_to_dismiss(parent_file)
  add_obama_flynn_warning(parent_file)

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/479125616-Flynn-Fifth-Supplement-in-Support-of-Agreed-Dismissal.pdf")

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/479125616/Flynn-Fifth-Supplement-in-Support-of-Agreed-Dismissal"
  url.localfilename = "479125616-Flynn-Fifth-Supplement-in-Support-of-Agreed-Dismissal.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-10-07T12:00:00-00:00")
  url.save()

  add_event(child_file, "2017-01-25T12:00:00-05:00", "2017-01-25T12:00:00-05:00", "DOJ - Flynn no reasonable prosecutor would pursue Logan Act", "Other transition teams, covert relationship with Russia? No, not based on the facts.", EVENT_TYPE_DOJ )
  return None

def add_hillary(parent_file: truxton.TruxtonChildFileIO) -> None:

  # classified data transmitted from TWO different private systems
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Hillary R. Clinton Part 01 of 05.pdf")
  
  url = child_file.newurl()
  url.url = "https://vault.fbi.gov/hillary-r.-clinton/Hillary%20R.%20Clinton%20Part%2001/at_download/file"
  url.localfilename = "Hillary R. Clinton Part 01 of 05.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-10-07T12:00:00-00:00")
  url.save()

  e = add_event(child_file, "2015-07-10T12:00:00-05:00", "2015-07-10T12:05:00-05:00", "Midyear Exam (Clinton email server) opened", "Found over 2,000 classified emails (Confidential to Top Secret Special Access Program) on two different private servers", EVENT_TYPE_FBI )
  e.tag("Midyear Exam", "Investigation Opened", truxton.TAG_ORIGIN_HUMAN)
  return None
  
def add_miscellaneous(parent_file: truxton.TruxtonChildFileIO) -> None:
  add_downer_meeting(parent_file)

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Catch All.txt")

  add_event(child_file, "2017-05-17T12:00:00-05:00", "2019-04-18T12:00:00-05:00", "Special Counsel Investigation", "https://en.wikipedia.org/wiki/Special_Counsel_investigation_(2017%E2%80%932019)", EVENT_TYPE_MUELLER )
  add_event(child_file, "2016-04-18T12:00:00-05:00", "2016-04-18T12:05:00-05:00", "Professor Joseph Mifsud (CIA?) introduces Papadopoulos to Ivan Timofeev", "https://themarketswork.com/2018/05/10/ties-that-bind-stefan-halper-joseph-mifsud-alexander-downer-papadopoulos/", EVENT_TYPE_MIFSUD )
  add_event(child_file, "2016-09-02T12:00:00-05:00", "2016-09-02T12:05:00-05:00", "Stefan Halper (FBI) offers Papadopoulos $3000", "To write a policy paper https://dailycaller.com/2018/03/25/george-papadopoulos-london-emails/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-09-02T12:00:00-05:00", "2016-09-02T12:05:00-05:00", "Stefan Halper (FBI) meets Carter Page in Cambridge", "Symposium 2016s Race to Change the World http://www.crassh.cam.ac.uk/events/26818", EVENT_TYPE_FBI )
  add_event(child_file, "2016-09-15T12:00:00-05:00", "2016-09-15T12:05:00-05:00", "Stefan Halper (FBI) brings Azra Turk (CIA?) to meet Papadopoulos in London", "Halper bragged about his ties to Russian spies. Met at the Sofitel hotel in London’s West End, https://nypost.com/2019/05/02/fbi-sent-a-blonde-bombshell-to-meet-trump-aide-papadopoulos-report/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-03-16T12:00:00-05:00", "2016-03-16T12:05:00-05:00", "Wikileaks publishes Clinton Private Secretary of State email", "https://wikileaks.org/clinton-emails/", EVENT_TYPE_WIKILEAKS )
  add_event(child_file, "2016-07-22T12:00:00-05:00", "2016-07-22T12:05:00-05:00", "Wikileaks publishes DNC email", "https://en.wikipedia.org/wiki/2016_Democratic_National_Committee_email_leak", EVENT_TYPE_WIKILEAKS )
  add_event(child_file, "2016-07-01T12:00:00-05:00", "2016-07-01T12:05:00-05:00", "Carter Page goes to Moscow", "https://wikileaks.org/clinton-emails/", EVENT_TYPE_CAMPAIGN )
  add_event(child_file, "2016-07-26T12:00:00-05:00", "2016-07-26T12:05:00-05:00", "FBI told of Alexander Downer", "News of DNC Email leak reminds Downer of Papadopoulos meeting https://dailycaller.com/2019/04/19/joseph-mifsud-papadopoulos-mueller/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-09-19T12:00:00-05:00", "2016-09-19T12:05:00-05:00", "FBI receives Steele report", "https://www.nytimes.com/2019/04/19/us/politics/steele-dossier-mueller-report.html", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-10T18:20:00-05:00", "2017-01-10T12:18:20-05:00", "Buzzfeed publishes Steele report", "https://www.buzzfeednews.com/article/kenbensinger/these-reports-allege-trump-has-deep-ties-to-russia", EVENT_TYPE_STEELE )
  add_event(child_file, "2016-09-26T12:00:00-05:00", "2016-09-26T12:05:00-05:00", "Carter Page leaving campaign", "https://sites.google.com/view/politicscentral/crossfire-hurricane/fisa-warrants", EVENT_TYPE_CAMPAIGN )

  # 456781456-2018-DOJ-Letter-to-FISC.pdf
  add_event(child_file, "2016-10-21T12:00:00-05:00", "2016-10-21T12:05:00-05:00", "FISA warrant issued on Carter Page", "Docket 2016-1182 https://sites.google.com/view/politicscentral/crossfire-hurricane/fisa-warrants", EVENT_TYPE_FISA )
# https://themarketswork.com/2018/05/10/ties-that-bind-stefan-halper-joseph-mifsud-alexander-downer-papadopoulos/

  add_event(child_file, "2017-05-09T12:00:00-05:00", "2017-05-09T12:05:00-05:00", "Comey fired", "https://en.wikipedia.org/wiki/Dismissal_of_James_Comey", EVENT_TYPE_FBI )
  add_event(child_file, "2017-02-11T12:00:00-05:00", "2017-02-11T12:05:00-05:00", "FBI interviews Mifsud about Papadopoulos", "https://thehill.com/hilltv/rising/404275-what-professor-really-told-fbi-about-trump-russia-and-papadopoulos", EVENT_TYPE_FBI )
  add_event(child_file, "2016-07-11T12:00:00-05:00", "2016-07-11T12:05:00-05:00", "Stefan Halper (FBI) meets Carter Page", "At University of Cambridge https://dailycaller.com/2019/05/03/azra-turk-cia-fbi-papadopoulos/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-03-14T12:00:00-05:00", "2016-03-14T12:05:00-05:00", "John Brennan (CIA) travels to Moscow", "Meets with Federal Security Service (KGB) https://www.breitbart.com/national-security/2016/03/29/russians-claim-cia-chief-john-brennan-made-secret-trip-to-moscow/", EVENT_TYPE_CIA )
  add_event(child_file, "2017-01-05T13:00:00-05:00", "2017-01-05T14:00:00-05:00", "Comey (FBI) Briefs Obama and Susan Rice (NSC)", "About the status of the Russia investigation. https://www.scribd.com/document/371379264/2018-02-08-CEG-LG-to-Rice-Russia-Investigation-Email#from_embed", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-20T12:15:32-05:00", "2017-01-20T12:15:33-05:00", "Susan Rice (NSC) documents Jan 5 meeting as 'by the book'", "Rice stresses that Obama said 'by the book' but everyone else in the meeting noted it as 'the right people working on this' https://www.scribd.com/document/371379264/2018-02-08-CEG-LG-to-Rice-Russia-Investigation-Email#from_embed", EVENT_TYPE_RICE )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "UAE Crown Prince Sheikh Mohammed bin Zayed al-Nahyan meets Trump Transition Team", "https://www.cnn.com/2017/09/13/politics/susan-rice-house-investigators-unmasked-trump-officials/", EVENT_TYPE_CAMPAIGN )
  add_event(child_file, "2017-03-22T12:00:00-05:00", "2017-03-22T12:00:00-05:00", "Susan Rice lies on PBS Newshour", "Nothing of the sort occurred. I know nothing about (incidental intercept of Trump and associates) https://www.pbs.org/newshour/nation/susan-rice-trumps-wiretapping-claim-nothing-sort-occurred", EVENT_TYPE_RICE )
  add_event(child_file, "2017-04-17T13:08:00-05:00", "2017-04-17T13:08:00-05:00", "Susan Rice admits unmasking", "https://www.nbcnews.com/politics/politics-news/susan-rice-speaks-out-unmasking-accusations-i-leaked-nothing-nobody-n742486", EVENT_TYPE_RICE )
  add_event(child_file, "2016-04-16T12:00:00-05:00", "2016-04-16T12:00:00-05:00", "Fusion GPS hired on behalf of DNC/Clinton campaign", "Marc E. Elias works for Perkins Coie law firm, https://www.vice.com/en_us/article/kzgn3a/clinton-campaign-trump-dossier", EVENT_TYPE_HILLARY )
  add_event(child_file, "2017-01-10T12:00:00-05:00", "2017-01-10T12:00:00-05:00", "CNN reports about Pee Tapes Meeting", "https://www.washingtonexaminer.com/opinion/columnists/new-report-details-comey-plan-to-ambush-trump-with-moscow-sex-allegation", EVENT_TYPE_STEELE )
  add_event(child_file, "2017-01-23T12:00:00-05:00", "2017-01-23T12:00:00-05:00", "Andrew McCabe (FBI) calls Michael Flynn to schedule interview", "https://www.washingtontimes.com/news/2019/oct/25/fbi-ambushed-michael-flynn-then-celebrated/", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-24T14:15:00-05:00", "2017-01-24T15:00:00-05:00", "Peter Strzok (FBI) and Joe Pientka (FBI) interview Michael Flynn", "Determined he was not being defensive. https://themarketswork.com/2018/12/14/new-fbi-302-document-appears-to-reveal-interview-with-agents-not-flynn/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-08-01T12:00:00-05:00", "2016-08-03T12:00:00-05:00", "Peter Strzok (FBI) and Joe Pientka (FBI) interview Alexander Downer (Australian) in London", "https://www.nationalreview.com/2018/05/strzok-page-texts-trump-russia-investigation-origins/", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-23T12:00:00-05:00", "2017-01-23T12:00:00-05:00", "Robert Hannigan (GCHQ) unexpectedly resigns", "Later revealed cause was helping paedophile priest avoid jailtime. https://www.telegraph.co.uk/news/2017/01/23/breaking-gchq-boss-quits-personal-reasons-just-two-years/", EVENT_TYPE_GCHQ )
  add_event(child_file, "2016-09-23T12:00:00-05:00", "2016-09-23T12:05:00-05:00", "Yahoo News publishes Steele leaks", "https://www.realclearpolitics.com/epolls/2016/president/us/2016_republican_presidential_nomination-3823.html", EVENT_TYPE_STEELE )
  add_event(child_file, "2016-07-05T12:00:00-05:00", "2016-07-05T12:05:00-05:00", "Comey won't recommend charges against Clinton", "https://dailycaller.com/2019/10/18/hillary-clinton-violations-state-department-emails/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-03-21T12:00:00-05:00", "2016-03-21T12:05:00-05:00", "Trump 'Time to rethink NATO' on CNN", "This scares Estonia", EVENT_TYPE_CAMPAIGN )
  add_event(child_file, "2016-07-21T12:00:00-05:00", "2016-07-21T12:05:00-05:00", "Estonian President appears to push back on Trump's NATO comments", "Odd", EVENT_TYPE_CAMPAIGN )
  add_event(child_file, "2016-07-02T12:00:00-05:00", "2016-07-02T12:05:00-05:00", "Strzok (FBI) Interviews Clinton", "https://vault.fbi.gov/hillary-r.-clinton/Hillary%20R.%20Clinton%20Part%2002%20of%2043/view", EVENT_TYPE_FBI )
  e = add_event(child_file, "2016-03-02T12:00:00-05:00", "2016-03-02T12:05:00-05:00", "FBI interviews Carter Page", "https://medium.com/@the_war_economy/spygate-part-7-brennans-working-group-e4ab7d8188ac", EVENT_TYPE_FBI )
  e.tag("Crossfire Dragon", "Carter Page was Crossfire Dragon", truxton.TAG_ORIGIN_HUMAN)
  add_event(child_file, "2016-05-02T12:00:00-05:00", "2016-05-02T12:05:00-05:00", "Comey (FBI) drafts Clinton exoneration message", "https://medium.com/@the_war_economy/spygate-part-7-brennans-working-group-e4ab7d8188ac", EVENT_TYPE_FBI )
  add_event(child_file, "2016-05-09T12:00:00-05:00", "2016-05-13T12:05:00-05:00", "Bill Priestap (FBI Counter Intel) travels to London", "Email Midyear Exam May 06, 2016 7:17PM, SMS from Strzok 2016-05-04 21:31:14 Bill gets back from London next week", EVENT_TYPE_FBI )
  add_event(child_file, "2016-10-27T12:00:00-05:00", "2016-10-30T12:05:00-05:00", "Andrew McCabe (FBI) in London", "Multiple sources in Twitter thread https://twitter.com/JohnWHuber/status/999401435078057984", EVENT_TYPE_FBI )
  add_event(child_file, "2016-12-29T12:00:00-05:00", "2016-12-29T12:05:00-05:00", "Intercepted phone call from Flynn to Sergei Kislyak", "https://abcnews.go.com/Politics/russia-probe-timeline-moscow-mueller/story?id=57427441", EVENT_TYPE_FBI )
  add_event(child_file, "2016-06-12T12:00:00-05:00", "2016-06-12T12:05:00-05:00", "Julian Assange says Wikileaks has more Clinton emails", "Page 76 The Plot Against the President", EVENT_TYPE_WIKILEAKS )
  add_event(child_file, "2016-07-05T12:00:00-05:00", "2016-07-05T12:05:00-05:00", "Michael Gaeta (FBI) interviews Steele at Orbis office in London", "Page 79 The Plot Against the President", EVENT_TYPE_FBI )
  add_event(child_file, "2016-09-26T12:00:00-05:00", "2016-09-26T12:05:00-05:00", "NYPD gives 141,000 Clinton emails on Weiner laptop to FBI", "https://www.factcheck.org/2018/08/clintons-emails-weiners-laptop-and-a-falsehood/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-10-28T12:00:00-05:00", "2016-10-28T12:05:00-05:00", "Comey (FBI) tells Congress they will look at 141,000 Clinton emails on Weiner laptop", "https://www.factcheck.org/2018/08/clintons-emails-weiners-laptop-and-a-falsehood/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-10-30T12:00:00-05:00", "2016-10-30T12:05:00-05:00", "FBI gets warrant to look at 141,000 Clinton emails on Weiner laptop", "https://www.factcheck.org/2018/08/clintons-emails-weiners-laptop-and-a-falsehood/", EVENT_TYPE_FBI )
  add_event(child_file, "2016-11-06T12:00:00-05:00", "2016-11-06T12:05:00-05:00", "Comey (FBI) finds nothing new in 141,000 Clinton emails on Weiner laptop", "https://www.factcheck.org/2018/08/clintons-emails-weiners-laptop-and-a-falsehood/", EVENT_TYPE_FBI )
  add_event(child_file, "2015-12-28T19:18:32-05:00", "2015-12-28T19:18:32-05:00", "Page to Strozk - You get all your OCONUS lures approved? ;)", "OIG version", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2015-12-28T19:19:41-05:00", "2015-12-28T19:19:41-05:00", "Strozk to Page - No, it's just implicated a much bigger policy issue I'll explain XXX Might even be able to use it as a pretext for a call... :)", "OIG version", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2016-10-31T13:05:00-05:00", "2016-10-31T17:27:00-05:00", "Jeffery Wiseman (FBI CHS) recorded conversation with Papadopoulos (Crossfire Typhoon)", "transcript reads like they were at a casino, Wiseman identified in https://twitter.com/CasualSemi/status/1248350370985906176", EVENT_TYPE_FBI )
  add_event(child_file, "2016-11-18T09:00:00-05:00", "2016-11-18T09:00:00-05:00", "Steele's Delta File accessed by Crossfire Hurricane Team", "Grassley", EVENT_TYPE_FBI )
  add_event(child_file, "2016-12-06T09:00:00-05:00", "2016-12-06T09:00:00-05:00", "Obama orders Intelligence Community Assessment (ICA) about Russian involvement in election", "Lee Smith, The Plot against the President, page 106", EVENT_TYPE_CIA )
  add_event(child_file, "2016-12-09T09:00:00-05:00", "2016-12-09T09:00:00-05:00", "Washington Post reports ICA leaked Putin-helps-Trump meme", "Lee Smith, The Plot against the President, page 106", EVENT_TYPE_CIA )
  e = add_event(child_file, "2017-01-04T13:49:46-05:00", "2017-01-04T13:49:46-05:00", "FBI closes Crossfire Razor (Flynn) case due to no evidence", "https://thefederalist.com/2020/04/30/breaking-fbi-closed-flynn-case-dubbed-crossfire-razor-in-early-2017-until-strzok-ordered-it-to-stay-open/", EVENT_TYPE_FBI )
  e.tag("Crossfire Razor", "Case dropped, no evidence of any wrong doing", truxton.TAG_ORIGIN_HUMAN)
  add_event(child_file, "2017-01-04T14:11:00-05:00", "2017-01-04T14:14:00-05:00", "Strzok to Crossfire Razor Case Manager: Hay if you havent closed RAZOR, don't do so yet", "https://thefederalist.com/2020/04/30/breaking-fbi-closed-flynn-case-dubbed-crossfire-razor-in-early-2017-until-strzok-ordered-it-to-stay-open/", EVENT_TYPE_FBI )
  e.tag("Crossfire Razor", "Strzok prevents official closing of the case", truxton.TAG_ORIGIN_HUMAN)
  add_event(child_file, "2017-01-04T14:19:01-05:00", "2017-01-04T14:19:01-05:00", "Strzok to Page: Razor still open.", "https://thefederalist.com/2020/04/30/breaking-fbi-closed-flynn-case-dubbed-crossfire-razor-in-early-2017-until-strzok-ordered-it-to-stay-open/", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-01-04T14:19:10-05:00", "2017-01-04T14:19:10-05:00", "Page to Strzok: phew.", "https://thefederalist.com/2020/04/30/breaking-fbi-closed-flynn-case-dubbed-crossfire-razor-in-early-2017-until-strzok-ordered-it-to-stay-open/", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-02-10T17:37:00-05:00", "2017-02-10T17:37:00-05:00", "Page to Strzok: This document pisses me off... This is lazy work on your part.", "The document is probably the Flynn 302. https://thefederalist.com/2020/04/30/breaking-fbi-closed-flynn-case-dubbed-crossfire-razor-in-early-2017-until-strzok-ordered-it-to-stay-open/", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-02-10T22:10:00-05:00", "2017-02-10T22:10:00-05:00", "Strzok to Page: Trying to not completely re-write the thing so as to save Joe's voice... needing it soon...", "https://thefederalist.com/2020/04/30/breaking-fbi-closed-flynn-case-dubbed-crossfire-razor-in-early-2017-until-strzok-ordered-it-to-stay-open/", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-02-15T12:00:00-05:00", "2017-02-15T12:00:00-05:00", "Strzok (FBI) Files 302 on Flynn Interview", "22 days after the interview. https://assets.documentcloud.org/documents/5633260/12-17-18-Redacted-Flynn-Interview-302.pdf", EVENT_TYPE_FBI )
  add_event(child_file, "2017-05-31T12:00:00-05:00", "2017-05-31T12:00:00-05:00", "FBI amends Strzok 302 to remove 'Draft'", "127 days after the interview. https://assets.documentcloud.org/documents/5633260/12-17-18-Redacted-Flynn-Interview-302.pdf", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-23T21:30:41-05:00", "2017-01-23T21:30:41-05:00", "Page to Strzok: USC 1001 Admonition, Of Course You Know Sir Lying...", "459057200-doc-188.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-01-24T06:46:58-05:00", "2017-01-24T06:46:58-05:00", "Strzok to James A Baker (FBI General Counsel): Potential Questions for DD's call to Flynn", "459057200-doc-188.pdf", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-24T06:46:58-05:00", "2017-01-24T06:46:58-05:00", "Priestap's Handwritten Notes: What is our goal? Truth/Admission or get him to lie so we can prosecute.", "459057200-doc-188.pdf", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-24T06:46:00-05:00", "2017-01-24T06:46:00-05:00", "Strzok to Unknown: About to email you questions for Andy in advance of his call to Flynn.", "459199066-us-v-flynn.pdf", EVENT_TYPE_FBI )
  add_event(child_file, "2017-01-24T09:27:00-05:00", "2017-01-24T09:27:00-05:00", "Strzok to Page: Bill just told me that he brought it up again", "459199066-us-v-flynn.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-01-24T09:29:00-05:00", "2017-01-24T09:29:00-05:00", "Page to Strzok: Yeah dd is frustrated. Going into meeting. Don't repeat", "459199066-us-v-flynn.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-01-24T09:30:00-05:00", "2017-01-24T09:30:00-05:00", "Strzok to Page: I won't. Bill said D starting going one way and DD cut him off.", "459199066-us-v-flynn.pdf", EVENT_TYPE_STRZOK_PAGE_MESSAGE )
  add_event(child_file, "2017-01-24T17:00:00-05:00", "2017-01-24T17:30:00-05:00", "Sally Yates (DOJ) briefed on Flynn interview by Tashina Gauhar (DOJ-NSD)", "Tashina Gauhar Calendar https://www.scribd.com/document/455659490/Tashina-Gauhar-Calendars", EVENT_TYPE_DOJ )
  add_event(child_file, "2017-01-25T13:45:00-05:00", "2017-01-25T14:15:00-05:00", "Sally Yates (DOJ) briefed on details Flynn interview by Tashina Gauhar (DOJ-NSD)", "Tashina Gauhar Calendar https://www.scribd.com/document/455659490/Tashina-Gauhar-Calendars", EVENT_TYPE_DOJ )

  # https://www.thegatewaypundit.com/2019/11/new-docs-reveal-peter-strzoks-wife-furious-about-his-cheating-threatened-to-blow-it-all-up-called-lisa-page-to-confront-her-about-the-affair/
  add_event(child_file, "2017-04-04T12:00:00-05:00", "2017-04-04T00:00:00-05:00", "Strzok's wife discovers affair with Lisa Page", "He was using iMessage to conduct FBI business", EVENT_TYPE_FBI )

  # https://s3.documentcloud.org/documents/6244707/8-6-19-Strzok-v-Barr-Complaint.pdf
  add_event(child_file, "2018-08-09T12:00:00-05:00", "2018-08-09T12:00:00-05:00", "Strzok fired from FBI", "One day after signing Last Chance agreement", EVENT_TYPE_FBI )

  # https://media.washtimes.com/media/misc/2019/03/16/BOOK_Kramer_trans..pdf
  add_event(child_file, "2016-11-18T12:00:00-05:00", "2016-11-20T12:00:00-05:00", "David Kramer is told of Steele Dossier by Sir Andrew Wood", "At Halifax International Security Forum, page 22 line 13", EVENT_TYPE_FBI )
  add_mccabe_donations(parent_file)
  return None

def add_flynn_unmasking(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/2020-05-13-ODNI-to-CEG-RHJ-Unmasking.pdf")

  url = child_file.newurl()
  url.url = "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn"
  url.localfilename = "2020-05-13-ODNI-to-CEG-RHJ-Unmasking.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-05-13T00:00:00-05:00")
  url.save()

  add_event(child_file, "2016-11-30T12:00:00-05:00", "2016-11-30T12:00:00-05:00", "Unmask Flynn by Samantha Power", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-02T12:00:00-05:00", "2016-12-02T12:00:00-05:00", "Unmask Flynn by Samantha Power", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-07T12:00:00-05:00", "2016-12-07T12:00:00-05:00", "Unmask Flynn by Samantha Power", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Samantha Power", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T13:00:00-05:00", "2016-12-14T13:00:00-05:00", "Unmask Flynn by Samantha Power", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-23T12:00:00-05:00", "2016-12-23T12:00:00-05:00", "Unmask Flynn by Samantha Power", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2017-01-11T12:00:00-05:00", "2017-01-11T12:00:00-05:00", "Unmask Flynn by Samantha Power", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-02T12:00:00-05:00", "2016-12-02T12:00:00-05:00", "Unmask Flynn by James Clapper", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-28T12:00:00-05:00", "2016-12-28T12:00:00-05:00", "Unmask Flynn by James Clapper", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2017-01-07T12:00:00-05:00", "2017-01-07T12:00:00-05:00", "Unmask Flynn by James Clapper", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-06T12:00:00-05:00", "2016-12-06T12:00:00-05:00", "Unmask Flynn by Kelly Degnan (Italy)", "Kelly Degnan was the Deputy Chief of Mission (DCM) to Ambassador John R. Philips in Italy", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-06T12:00:00-05:00", "2016-12-06T12:00:00-05:00", "Unmask Flynn by John R. Phillips (Ambassador to Italy)", "U.S. Ambassador to Italy", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by John Brennan (CIA)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by John Brennan (CIA)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Patrick Conlon (DOJ Office of International Affairs)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Jacob Lew (Secretary of the Treasury)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Arthur Danny McGlynn (Assistant Secretary of the Treasury)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Mike Neufeld (Deputy Assistant Secretary of the Treasury)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Sarah Raskin (Deputy Secretary of the Treasury)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Nathan Sheets (Under Secretary of the Treasury)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-14T12:00:00-05:00", "2016-12-14T12:00:00-05:00", "Unmask Flynn by Adam Szubin (Acting Under Secretary of the Treasury)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by Robert Bell (USNATO Advisor Defense Advisor)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by VADM John N Christenson (NATO Military Committee)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by James Comey (FBI)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by --Redacted-- PERSON 1 (Chief Syria Group)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by --Redacted-- PERSON 2 (Chief Syria Group)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by --Redacted-- (Deputy Assistant Director NEMC)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by Lt Col Paul Geehreng (USNATO Policy Advisor for Russia)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by --Redacted-- (Policy Advisor to NATO Ambassador Douglas Lute)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by James Hursh (USNATO Deputy Defense Advisor)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by Earle D. Litzenberger (Deputy Chief Mission USNATO)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn" , EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by Ambassador Douglas Lute (PermRep to NATO)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by --Redacted-- PERSON 1 Intelligence Executive Briefer (Department of Energy - IN)", "Office of Intelligence and Counterintelligence https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by --Redacted-- PERSON 2 Intelligence Executive Briefer (Department of Energy - IN)", "Office of Intelligence and Counterintelligence https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by Scott Parrish (USNATO Political Officer)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by Elizabeth Sherwood-Randall (DOE Deputy Secretary of Energy)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-15T12:00:00-05:00", "2016-12-15T12:00:00-05:00", "Unmask Flynn by Tamir Waser (USNATO Political Advisor)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-16T12:00:00-05:00", "2016-12-16T12:00:00-05:00", "Unmask Flynn by --Redacted-- (COS - Chief of Station)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-16T12:00:00-05:00", "2016-12-16T12:00:00-05:00", "Unmask Flynn by --Redacted-- PERSON 1 (CMO - Chief Military/Management Officer)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-16T12:00:00-05:00", "2016-12-16T12:00:00-05:00", "Unmask Flynn by --Redacted-- PERSON 2 (CMO - Chief Military/Management Officer)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-16T12:00:00-05:00", "2016-12-16T12:00:00-05:00", "Unmask Flynn by --Redacted-- (DCOS - Deputy Chief of Station)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-16T12:00:00-05:00", "2016-12-16T12:00:00-05:00", "Unmask Flynn by John Tefft (Ambassador to Russia)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2016-12-28T12:00:00-05:00", "2016-12-28T12:00:00-05:00", "Unmask Flynn by John R. Bass (Ambassador to Turkey)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2017-01-05T12:00:00-05:00", "2017-01-05T12:00:00-05:00", "Unmask Flynn by Denis McDonough (President Obama Chief of Staff)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2017-01-07T12:00:00-05:00", "2017-01-07T12:00:00-05:00", "Unmask Flynn by Michael Dempsey (Deputy DNI for Intelligence Integration)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2017-01-07T12:00:00-05:00", "2017-01-07T12:00:00-05:00", "Unmask Flynn by Stephanie L. O'Sullivan (Principal Deputy DNI for Intelligence Integration)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2017-01-10T12:00:00-05:00", "2017-01-10T12:00:00-05:00", "Unmask Flynn by --Redacted-- (CIA CTMC - Counter Terrorism Mission Center)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  add_event(child_file, "2017-01-12T12:00:00-05:00", "2017-01-12T12:00:00-05:00", "Unmask Flynn by Joseph R. Biden (Vice President)", "https://www.foxnews.com/politics/read-documents-listing-names-of-obama-era-officials-who-sought-to-unmask-michael-flynn", EVENT_TYPE_UNMASK )
  return None

def add_baltic(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "CIA Director Shown Tape of Baltic State Money.pdf")

  url = child_file.newurl()
  url.url = "https://www.bbc.com/news/world-us-canada-38589427"
  url.localfilename = "CIA Director Shown Tape of Baltic State Money.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-01-12T00:00:00-00:00")
  url.save()

  add_event(child_file, "2016-04-01T12:00:00-05:00", "2016-04-01T12:05:00-05:00", "John Brennan (CIA) Kremlin money going into campaign by Baltic state", "Date Approximate. A tape recording of a conversation about money from the Kremlin going into the US presidential campaign given by Baltic state", EVENT_TYPE_CIA )
  add_event(child_file, "2016-04-02T12:00:00-05:00", "2016-04-02T12:05:00-05:00", "John Brennan (CIA) creates CIA/FBI/NSA Fusion Cell", "Date approximate. Six members: CIA, DNI, FBI, NSA, Treasury, Justice", EVENT_TYPE_CIA )
  add_event(child_file, "2016-06-01T12:00:00-05:00", "2016-06-01T12:05:00-05:00", "FISA rejected application 1 (two Russian Banks, Alfa and Silicon Valley)", "FISA court rejects, outright, tapping two Russian banks", EVENT_TYPE_FISA )
  add_event(child_file, "2016-07-01T12:00:00-05:00", "2016-07-01T12:05:00-05:00", "FISA rejected application 2 (two Russian Banks)", "FISA Court rejects more narrowly drawn application tapping two Russian banks", EVENT_TYPE_FISA )
  add_event(child_file, "2016-10-15T12:00:00-05:00", "2016-10-15T12:05:00-05:00", "FISA warrant drawn on Trump server for info on two Russian banks", "New FISA court Judge approves application tapping two Russian banks", EVENT_TYPE_FISA )

  return None

def add_halifax(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "McCain described how he received the Steele dossier on Trump-Russia - Business Insider.pdf")

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "McCain told of Steele Dossier by Sir Andrew Wood"
  location.latitude = 44.6401547974541
  location.longitude = -63.56827859791606
  location.when = datetime.fromisoformat("2016-11-18T12:00:00-05:00")
  location.save()

  url = child_file.newurl()
  url.url = "https://www.businessinsider.com/how-john-mccain-received-steele-dossier-trump-russia-2018-5"
  url.localfilename = "McCain described how he received the Steele dossier on Trump-Russia - Business Insider.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-03-22T13:27:00-05:00")
  url.save()

  # Dates from https://halifaxtheforum.org/forum/2016-halifax-international-security-forum/
  meeting_event = add_event( child_file, "2016-11-18T12:00:00-05:00", "2016-11-18T12:05:00-05:00", "John McCain (R-Senate) meets Sir Andrew Wood (British Ambassador to Russia), told of the Steele dossier", "Wood is former British Ambassador to Russia, Meeting included Chris Brose and David Kramer", EVENT_TYPE_STEELE )

  relation = child_file.newrelation()
  relation.a = meeting_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "McCain Reposponsible for Leaks.pdf")

  url = child_file.newurl()
  url.url = "https://www.zerohedge.com/news/2018-12-19/mccain-responsible-steele-dossier-leak"
  url.localfilename = "McCain Reposponsible for Leaks.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2018-12-19T22:25:00-05:00")
  url.save()

  meeting_event = add_event( child_file, "2016-11-28T12:00:00-05:00", "2016-11-28T12:05:00-05:00", "David Kramer gets copy of Dossier from Steele in Surrey London", "https://www.zerohedge.com/news/2018-12-19/mccain-responsible-steele-dossier-leak", EVENT_TYPE_STEELE )
  add_event( child_file, "2016-11-30T12:00:00-05:00", "2016-11-30T12:05:00-05:00", "David Kramer gives dossier to McCain", "https://www.zerohedge.com/news/2018-12-19/mccain-responsible-steele-dossier-leak", EVENT_TYPE_STEELE )
  e = add_event( child_file, "2016-12-29T12:00:00-05:00", "2016-12-29T12:05:00-05:00", "David Kramer Leaks Dossier to Buzzfeed", "https://www.zerohedge.com/news/2018-12-19/mccain-responsible-steele-dossier-leak", EVENT_TYPE_STEELE )
  e.tag("Leak", "David Kramer Leaks Dossier to Buzzfeed", truxton.TAG_ORIGIN_HUMAN)

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "David Kramer gets Dossier from Steele"
  location.latitude = 51.314841
  location.longitude = -0.55995
  location.when = datetime.fromisoformat("2016-11-28T12:00:00-05:00")
  location.save()

  relation = child_file.newrelation()
  relation.a = meeting_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  return None

def add_brennan_in_moscow(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "John Brennan's Secret Trip to Moscow.pdf")

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "Brennan meets with FSB"
  location.latitude = 55.760833
  location.longitude = 37.628333
  location.when = datetime.fromisoformat("2016-03-14T12:00:00-05:00")
  location.save()

  url = child_file.newurl()
  url.url = "https://www.americanthinker.com/articles/2018/04/john_brennans_secret_trip_to_moscow.html"
  url.localfilename = "John Brennan's Secret Trip to Moscow.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2018-04-28T12:00:00-05:00")
  url.save()

  add_event( child_file, "2016-08-25T12:00:00-05:00", "2016-08-25T12:05:00-05:00", "John Brennan (CIA) briefs Harry Reid (Senate) about Steele Dossier", "After trip to Moscow", EVENT_TYPE_CIA )
  add_event( child_file, "2016-08-27T12:00:00-05:00", "2016-08-27T12:05:00-05:00", "Harry Reid (Senate) presses Comey (FBI) evidence mounts", "evidence of a direct connection between the Russian government and Donald Trump's presidential campaign continues to mount", EVENT_TYPE_FBI )
  add_event( child_file, "2016-04-01T12:00:00-05:00", "2016-04-01T12:05:00-05:00", "John Brennan (CIA) hears Estonian Intelligence recording about Kremlin money going into campaign", "Date Approximate. a tape recording of a conversation about money from the Kremlin going into the US presidential campaign given by Estonian Intelligence", EVENT_TYPE_CIA )

  return None

def add_mike_rogers(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "The Uncovering - Mike Rogers Investigation.pdf")

  url = child_file.newurl()
  url.url = "https://themarketswork.com/2018/04/05/the-uncovering-mike-rogers-investigation-section-702-fisa-abuse-the-fbi/"
  url.localfilename = "The Uncovering - Mike Rogers Investigation.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2018-04-05T12:00:00-05:00")
  url.save()

  e = add_event( child_file, "2016-03-09T12:00:00-05:00", "2016-03-09T12:05:00-05:00", "FBI improperly querying FISA at NSA", "Found in NSA minimization review, 85% of the queries were non-compliant", EVENT_TYPE_FBI )
  e.tag("FISA Abuse", "FBI doing inappropriate queries, lots of them", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-04-18T12:00:00-05:00", "2016-04-18T12:05:00-05:00", "Mike Rogers (NSA) shuts down FBI contractor access to FISA", "This is when FBI and DOJ NSD become aware of a problem", EVENT_TYPE_NSA )
  e.tag("FISA Abuse", "Apparently contractors had access", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-10-20T12:00:00-05:00", "2016-10-20T12:05:00-05:00", "Mike Rogers (NSA) learns of 'About Query' FISA violations", "Briefed by NSA compliance officer", EVENT_TYPE_NSA )
  e.tag("FISA Abuse", "Rogers finds out FBI was getting around the lockout", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-10-21T13:00:00-05:00", "2016-10-21T13:05:00-05:00", "Mike Rogers (NSA) terminates FISA 'About Query' Activity", "Reports violations to DOJ", EVENT_TYPE_NSA )
  e.tag("FISA Abuse", "Rogers terminates FBI access", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-10-24T12:00:00-05:00", "2016-10-24T12:05:00-05:00", "Mike Rogers (NSA) verbally informs FISA court of Significant Non-compliance", "Phone call", EVENT_TYPE_FISA )
  e.tag("FISA Abuse", "Rogers calls the court", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-10-26T12:00:00-05:00", "2016-10-26T12:05:00-05:00", "Mike Rogers (NSA) formally informs FISA court of Significant Non-compliance", "In-person at the FISA court", EVENT_TYPE_FISA )
  e.tag("FISA Abuse", "Rogers appears before the court", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-11-17T12:00:00-05:00", "2016-11-17T12:05:00-05:00", "Mike Rogers (NSA) travels to Trump Tower", "Does not clear it with James Clapper (DNI)", EVENT_TYPE_NSA )
  e.tag("FISA Abuse", "Rogers meets President elect", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-11-17T13:00:00-05:00", "2016-11-17T13:05:00-05:00", "Trump announces move to New Jersey", "Trump National Golf Club in Bedminster, New Jersey", EVENT_TYPE_CAMPAIGN )
  e.tag("FISA Abuse", "Rogers had something interesting to say", truxton.TAG_ORIGIN_HUMAN)

  e = add_event( child_file, "2016-10-28T12:00:00-05:00", "2016-10-28T12:05:00-05:00", "Clapper (DNI) asks Obama to remove Rogers (NSA)", "Date approximate. Comey wanted Rogers fired.", EVENT_TYPE_DNI )
  e.tag("FISA Abuse", "Apparently contractors had access", truxton.TAG_ORIGIN_HUMAN)

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Mike Rogers Unmasking.txt")
  url = child_file.newurl()
  url.url = "https://www.youtube.com/watch?v=lbM1bW7GiuQ"
  url.localfilename = "Mike Rogers Unmasking.txt"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2017-06-07T12:00:00-05:00")
  url.save()

  add_event( child_file, "2017-06-07T12:00:00-05:00", "2017-06-07T12:05:00-05:00", "Mike Rogers (NSA) testifies to Senate Intelligence Committee", "Explains US persons unmasking procedures.", EVENT_TYPE_NSA )
  return None

def add_comey_leaks(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "o1902.pdf")
  #child_file.tag("IG Report", "James Comey's leaks", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://oig.justice.gov/reports/2019/o1902.pdf"
  url.localfilename = "o1902.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-09-01T12:00:00-05:00")
  url.save()

  e = add_event( child_file, "2017-05-16T12:00:00-05:00", "2017-05-16T12:00:00-05:00", "Comey texts photo of memo to Daniel Richman instructing him to leak it to specific NY Times reporter", "Memo 4 'let Flynn go', page 13", EVENT_TYPE_FBI )
  e.tag("Leak", "Comey Leaks to NY Times", truxton.TAG_ORIGIN_HUMAN)
  add_event( child_file, "2017-02-13T12:00:00-05:00", "2017-02-13T12:00:00-05:00", "Flynn resigns", "", EVENT_TYPE_FLYNN )
  add_event( child_file, "2017-02-14T12:00:00-05:00", "2017-02-14T12:00:00-05:00", "Trump hopes Comey can let Flynn go (This is Memo 4)", "Memo 4 - marked Unclassified/FOUO", EVENT_TYPE_FBI )
  add_event( child_file, "2017-01-06T12:00:00-05:00", "2017-01-06T12:00:00-05:00", "On the orders of Clapper (DNI) Comey (FBI) tells Trump of pee tapes", "Page 67 Para 3, also Page 10", EVENT_TYPE_DNI )
  add_event( child_file, "2017-01-27T18:30:00-05:00", "2017-01-27T19:50:00-05:00", "Comey (FBI) tells Trump 'I don't leak' over dinner at Whitehouse", "Page 69 of PDF, Page 67 at bottom of page", EVENT_TYPE_FBI )

  return None

def stephen_laycock(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Stephen Laycock Redacted FINAL.pdf")

  url = child_file.newurl()
  url.url = "https://www.judiciary.senate.gov/imo/media/doc/Stephen%20Laycock%20Redacted%20FINAL.pdf"
  url.localfilename = "Stephen Laycock Redacted FINAL.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2021-10-31T12:08:28-05:00")
  url.save()

  e = add_event( child_file, "2016-10-11T12:00:00-05:00", "2016-10-11T12:00:00-05:00", "Kathleen Kavalec has a meeting with Steele", "Page 24 line 14.", EVENT_TYPE_FBI )

  return None

def add_pientka_testimony(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/Supervisory Special Agent 1 Redacted FINAL.pdf")
  #child_file.tag("Testimony", "Pientka Senate Judiciary Committee")

  url = child_file.newurl()
  url.url = "https://www.judiciary.senate.gov/imo/media/doc/Supervisory%20Special%20Agent%201%20Redacted%20FINAL.pdf"
  url.localfilename = "Supervisory Special Agent 1 Redacted FINAL.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-07-23T12:00:00-05:00")
  url.save()

  add_event( child_file, "2016-11-01T12:00:00-05:00", "2016-11-01T12:00:00-05:00", "Pientka (FBI) Orders Enhanced Validation Review of Steele", "Page 90 line 16, because Steele leaked to Mother Jones.", EVENT_TYPE_FBI )
  add_event( child_file, "2016-11-02T12:00:00-05:00", "2016-11-02T12:00:00-05:00", "Priestap (FBI) Shuts Down Steele Review", "Page 91 line 21, 'concerned about leaks'", EVENT_TYPE_FBI )
  e = add_event( child_file, "2017-01-06T12:00:00-05:00", "2017-01-06T12:00:00-05:00", "Pientka (FBI) Quits Crossfire Hurricane", "Page 100 line 4, asked to return to Washington Field Office (page 102 line 21) because of 'professional disagreement' (page 105, line 17).", EVENT_TYPE_FBI )
  e.tag("Unhappy", "Because Steele would not be validated as a source", truxton.TAG_ORIGIN_HUMAN)

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Politico Sussman Trial.pdf")

  url = child_file.newurl()
  url.url = "https://www.politico.com/news/2022/05/23/fbi-trump-russia-secret-server-claims-00034434"
  url.localfilename = "Politico Sussman Trial.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2022-09-15T12:00:00-05:00")
  url.save()

  add_event( child_file, "2016-09-22T12:00:00-05:00", "2016-09-22T12:00:00-05:00", "Pientka (FBI) Orders Collection of Russian Servers", "To agent Curtis Heide 'People on 7th floor to include Director are fired up about this server. Reachout and put tools on... its not an option - we must do it'", EVENT_TYPE_FBI )

  return None

def add_pientka_briefing(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "470185158-Joseph-Pientka-Briefing-Document.pdf") 
  #child_file.tag("FD-1057", "FBI Electronic Communication", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.scribd.com/document/470185158/Joseph-Pientka-Briefing-Document#from_embed"
  url.localfilename = "470185158-Joseph-Pientka-Briefing-Document.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-07-23T12:00:00-05:00")
  url.save()

  location = child_file.newlocation()
  location.type = truxton.LOCATION_TYPE_MEETING
  location.label = "FBI New York Field Office (NYFO): 25th floor Pientka briefs Trump and Flynn"
  location.latitude = 40.71568778251278
  location.longitude = -74.0041946786598
  location.when = datetime.fromisoformat("2016-08-17T15:55:00-05:00")
  location.save()

  briefing_event = add_event( child_file, "2016-08-17T15:55:00-05:00", "2016-08-17T16:08:00-05:00", "FBI Pientka gives 13 minute Counter Intelligence Overview (defensive) briefing to Trump/Flynn", "Page 2, At New York Field Office. Briefing lasted 13 minutes where Pientka mentioned Russia and carefully noted Flynn's response.", EVENT_TYPE_FBI )

  relation = child_file.newrelation()
  relation.a = briefing_event.id
  relation.atype = truxton.OBJECT_TYPE_EVENT
  relation.b = location.id
  relation.btype = truxton.OBJECT_TYPE_LOCATION
  relation.relation = truxton.RELATION_AT
  relation.save()

  return None

def add_schrage(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Schrage - Spies who hijacked America.pdf")
  #child_file.tag("News Article", "Spies who hijacked America", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://taibbi.substack.com/p/the-spies-who-hijacked-america"
  url.localfilename = "Schrage - Spies who hijacked America.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-08-09T12:00:00-05:00")
  url.save()

  add_event( child_file, "2017-01-10T12:00:00-05:00", "2017-01-10T12:00:00-05:00", "Stefan Halper (FBI) tells Steven Schrage that Flynn won't be around long", "Also says that Flynn is unsuitable for the job.", EVENT_TYPE_FBI )
  return None

def add_defendant(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/DEFENDANT-s-MEMORANDUM.pdf")

  add_event( child_file, "2017-01-24T12:35:00-05:00", "2017-01-24T12:40:00-05:00", "McCabe (FBI) calls Flynn: Send over a couple of agents, no lawyers.", "DEFENDANT-s-MEMORANDUM.pdf", EVENT_TYPE_FBI )
  add_event( child_file, "2017-01-24T14:15:00-05:00", "2017-01-24T15:00:00-05:00", "Strzok (FBI) and Pientka (FBI) interview Flynn. No mention of USC 1001 (lying to investigators)", "DEFENDANT-s-MEMORANDUM.pdf", EVENT_TYPE_FBI )
  return None

def add_dns(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Report_Volume4.pdf")

  url = child_file.newurl()
  url.url = "https://www.intelligence.senate.gov/sites/default/files/documents/Report_Volume4.pdf"
  url.localfilename = "Report_Volume4.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-01-01T00:00:00-05:00")
  url.save()

  add_event( child_file, "2016-10-26T09:00:00-05:00", "2016-10-26T09:00:00-05:00", "FBI given DNS logs from Alfa Bank", "Probably the 2,700 DNS mail1.trump-email.com lookups analyzed by Jean Camp", EVENT_TYPE_FBI )

  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Report_Volume5.pdf")

  url = child_file.newurl()
  url.url = "https://www.intelligence.senate.gov/sites/default/files/documents/Report_Volume5.pdf"
  url.localfilename = "Report_Volume5.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2020-08-18T00:00:00-05:00")
  url.save()

  add_event( child_file, "2017-01-22T12:00:00-05:00", "2017-01-22T12:00:00-05:00", "Flynn sworn in as National Security Advisor", "By Mike Pence, page 787", EVENT_TYPE_FLYNN )
  add_event( child_file, "2016-03-01T08:00:00-05:00", "2016-03-01T08:00:00-05:00", "Glenn Simpson (Fusion GPS) contacts DNC to provide opposition research", "Page 871, footnote 5697", EVENT_TYPE_STEELE )
  return None

def add_fbi_ig_report_fisa(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Flynn/120919-examination.pdf")
  #child_file.tag("IG Report", "Review of Four FISA Applications", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.justice.gov/storage/120919-examination.pdf"
  url.localfilename = "120919-examination.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2019-09-01T12:00:00-05:00")
  url.save()

  add_event( child_file, "2016-07-28T12:00:00-05:00", "2016-07-28T12:00:00-05:00", "FBI is told of Australian conversation with Papadopoulos", "FBI IG Report page 50", EVENT_TYPE_FBI )
  add_event( child_file, "2016-09-04T12:00:00-05:00", "2016-09-04T12:00:00-05:00", "Strzok promoted to Deputy Assistant Director (DAD) CD Operations Branch I", "FBI IG Report page 58", EVENT_TYPE_FBI )
  add_event( child_file, "2016-09-01T12:00:00-05:00", "2016-09-01T12:00:00-05:00", "FBI CHS operation 2 - High-Level Trump Campaign Official", "FBI IG Report page 326", EVENT_TYPE_FBI )
  add_event( child_file, "2016-08-01T12:00:00-05:00", "2016-08-30T12:00:00-05:00", "FBI CHS operation 3 - Papadopoulos at Casino", "FBI IG Report page 80, Transcript available", EVENT_TYPE_FBI )
  add_event( child_file, "2016-07-19T12:00:00-05:00", "2016-07-19T12:00:00-05:00", "Steele emails report 94 to Micheal Gaeta (FBI)", "FBI IG Report page 98, Handling Agent 1 is Michael Gaeta", EVENT_TYPE_STEELE )
  add_event( child_file, "2016-07-28T12:00:00-05:00", "2016-07-28T12:00:00-05:00", "Micheal Gaeta (FBI) emails reports 80 and 94 to ASAC 1 NYFO", "FBI IG Report page 98, Handling Agent 1 is Michael Gaeta", EVENT_TYPE_FBI )
  m = add_event( child_file, "2016-07-13T12:00:00-05:00", "2016-07-13T12:00:00-05:00", "Micheal Gaeta (FBI) tells ASAC 1 NYFO that Fusion GPS is working for Republicans or Hillary", "And that at some point they will use information in Report 80. FBI IG Report page 97, Footnote 223", EVENT_TYPE_FBI )
  m.addnote("At this point (2016-07-13) multiple FBI agents are aware that the Steele reports are of a political nature, Republican or Hillary") # At this point (2016-07-13) multiple FBI agents are aware that the Steele reports are of a political nature, Republican or Hillary
  add_event( child_file, "2016-08-03T12:00:00-05:00", "2016-08-03T12:00:00-05:00", "Meeting about Steele, Simpson and Perkins Coee", "Meeting in NYFO attended by ASAC 1, SAC 1, Chief Division Counsel (CDC), Associate Division Counsel (ADC), and Supervisory Special Agent (SSA). FBI IG Report page 98", EVENT_TYPE_FBI )
  add_event( child_file, "2016-08-02T12:00:00-05:00", "2016-08-02T12:00:00-05:00", "Strzok informed of FBI field agent reported contact by Simpson", "Probably Gaeta, he had been contacted by former CHS that Simpson's firm hired to investigate Trump's long standing relationship with Russia. Crossfire Hurricane team. FBI IG Report page 98, Footnote 223", EVENT_TYPE_FBI )
  add_event( child_file, "2016-10-07T12:00:00-05:00", "2016-10-07T12:00:00-05:00", "Case Agent 2 tells Steele about Papadopoulos, Flynn, Carter Page and Manafort investigations", "In a European city, probably London, Crossfire Hurricane team arrived the morning of this meeting. FBI IG Report page 109, Also SSCI Volume 5 page 911 shows date as single digit we assume 7th because it is a Friday. All Steele reports after this mentions one of these people", EVENT_TYPE_FBI )

  return None

def add_strzok_page_lync_messages(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "lync_text_messages_of_peter_strzok_from_2-13-16_to_12-6-17.pdf")
  child_file.tag("Text Messages", "Lync Messages", truxton.TAG_ORIGIN_HUMAN)

  url = child_file.newurl()
  url.url = "https://www.grassley.senate.gov/download/lync_text-messages-of-peter-strzok-from-2-13-16-to-12-6-17"
  url.localfilename = "lync_text_messages_of_peter_strzok_from_2-13-16_to_12-6-17.pdf"
  url.type = truxton.URL_TYPE_FIREFOX
  url.method = truxton.URL_METHOD_TYPE_CLICKED_ON_A_LINK
  url.format = truxton.URL_FORMAT_ASCII
  url.when = datetime.fromisoformat("2022-09-25T12:00:00-05:00")
  url.save()

  add_name_and_email( child_file, "Brian Auten", "bjauten@ic.fbi.gov" ) # Page 86 of 460365255-Flynn-motion-to-dismiss.pdf
  add_name_and_email( child_file, "James A. Baker", "James.Baker@ic.fbi.gov" )
  add_name_and_email( child_file, "Charles Halliday Dolan, Jr.", "charles.dolan@kglobal.com" )
  add_name_and_email( child_file, "Jonathan Moffa", "Jonathan.Moffa@ic.fbi.gov" )
  add_name_and_email( child_file, "Jonathan Moffa", "jcmoffa@fbi.sgov.gov" )
  add_name_and_email( child_file, "Bruce Ohr", "brohr@jmd.usdoj.gov" )
  add_name_and_email( child_file, "Bruce Ohr", "Bruce.G.Ohr@usdoj.gov" )
  add_name_and_email( child_file, "Lisa C. Page", "Lisa.Page@ic.fbi.gov" ) # Lisa.Page@ic.fbi.gov shown on page 18
  add_name_and_email( child_file, "Lisa C. Page", "lcpage@fbi.sgov.gov" ) # Page 86 of 460365255-Flynn-motion-to-dismiss.pdf
  add_name_and_email( child_file, "Joseph 'Joe' Pientka III", "jpientka@fbi.sgov.gov" ) # SIPR, Page 85 of 460365255-Flynn-motion-to-dismiss.pdf
  add_name_and_email( child_file, "Susan E. Rice", "SRice@nsc.eop.ic.gov" )
  add_name_and_email( child_file, "Curtis R. Ried", "CRied@nsc.eop.ic.gov" )
  add_name_and_email( child_file, "James E. Rybicki", "James.Rybicki@ic.fbi.gov" )
  add_name_and_email( child_file, "Peter P. Strzok II", "peter.strzok@ic.fbi.gov" ) # NIPR, fbi.ic.gov is SCION
  add_name_and_email( child_file, "Peter P. Strzok II", "ppstrzok@fbi.sgov.gov" )
  add_name_and_email( child_file, "Michael Sussman", "MSussmann@perkinscoie.com" )

  # Page 3
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  page_to_strzok(child_file, "2016-02-13T03:27:04-00:00", "I'm no prude, but I'm really appalled by this. So you don't have to go looking (in case you hadn't heard), Trump called him the p-word. The man has no dignity or class. He simply can not be president.\n\nWith a Slur for Ted Cruz, Donald Trump Further Splits Voters http://nyti.ms/1XolCkO")
  #strzok_to_page(child_file, "2016-02-26T11:26:00-00:00", "There won't be. Bill has MYE wrap at 230, just like he did for DD's function. And if like the one for DD, for which I was late, I won't have time. \n\nHopefully I can drive you to --Radacted-- at lunch because I think that may be the only time I can see or talk to you today. \U0001f615")
  m = strzok_to_page(child_file, "2016-02-26T11:26:04-00:00", "There won't be. Bill has MYE wrap at 230, just like he did for DD's function. And if like the one for DD, for which I was late, I won't have time. \n\nHopefully I can drive you to --Radacted-- at lunch because I think that may be the only time I can see or talk to you today. \U0001f615")
  m.addnote("MYE - Midyear Exam")
  m = page_to_strzok(child_file, "2016-03-04T02:10:51-00:00", "God trump is a loathsome human.")
  m.tag("Hatred", "loathsome is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  strzok_to_page(child_file, "2016-03-04T02:12:44-00:00", "Would he be a worse president than cruz?")
  page_to_strzok(child_file, "2016-03-04T02:13:14-00:00", "Trump? Yes, I think so.")

  # Page 4
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  #page_to_strzok(child_file, "2016-03-04T02:34:59-00:00", "Also did you hear him make a comment about the size of his d*ck earlier? This man can not be president.")
  #strzok_to_page(child_file, "2016-03-12T21:05:07-00:00", "That Texas article is depressing as hell. But answers how we could end up with President trump")
  #strzok_to_page(child_file, "2016-03-12T21:05:12-00:00", "That Texas article is depressing as hell. But answers how we could end up with President trump")
  # page_to_strzok(child_file, "2016-03-12T21:07:55-00:00", "Wasn't it? Seriously, how are people so incredibly ignorant?")
  strzok_to_page(child_file, "2016-03-12T21:21:00-00:00", "\U0001f621\nTrump Clarifies, and It\u2019s Worse - NYTimes.com\nhttp://mobile.nytimes.com/2016/03/02/opinion/trump-clarifies-and-its-worse.html?_r=0")
  # strzok_to_page(child_file, "2016-03-12T21:21:04-00:00", "\U0001f621\nTrump Clarifies, and It\u2019s Worse - NYTimes.com\nhttp://mobile.nytimes.com/2016/03/02/opinion/trump-clarifies-and-its-worse.html?_r=0")

  # Page 5
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  # page_to_strzok(child_file, "2016-03-16T04:11:54-00:00", "I can not believe Donald Trump is likely to be an actual, serious candidate for president.")
  strzok_to_page(child_file, "2016-03-29T02:41:15-00:00", "As expected, --Redacted-- couldn't hear Andy or Jim and wasn't clear that we felt we must interview on sort and get on laptops.")
  #strzok_to_page(child_file, "2016-03-29T02:41:36-00:00", "As expected, --Redacted-- couldn't hear Andy or Jim and wasn't clear that we felt we must interview on sort and get on laptops.")
  strzok_to_page(child_file, "2016-03-29T02:44:16-00:00", "Doesn't mean they're not somewhere else, but if true, and done properly, makes this much harder.")
  #strzok_to_page(child_file, "2016-03-29T02:44:21-00:00", "Doesn't mean they're not somewhere else, but if true, and done properly, makes this much harder.")
  m = page_to_strzok(child_file, "2016-04-20T12:53:08-00:00", "Hey check your vm before you talk to your MYE team. Jim spoke to Beth this am, nfi.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")

  # Page 6
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  page_to_strzok(child_file, "2016-04-27T22:55:42-00:00", "He was. Kortan majorly screwed up.")
  m = strzok_to_page(child_file, "2016-04-27T22:56:19-00:00", "Nothing related to us (mye or cd)?")
  m.addnote("MYE - Midyear Exam (Hillary Clinton), CD - Crossfire Dragon (Carter Page)??")
  
  m = strzok_to_page(child_file, "2016-04-29T20:30:36-00:00", "Hey also, mye brief to Bowdich on 5/10. Rainer's on the invite (just the four of us).")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-05-04T00:41:56-00:00", "Now the pressure really starts to finish MYE...")
  # This is strzok to jonathan moffa
  # strzok_to_page(child_file, "2016-05-04T00:42:56-00:00", "Cruz dropped out. Now the pressure to finish MYE really starts.")

  # Page 7
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  m = strzok_to_page(child_file, "2016-05-05T20:27:28-00:00", "Do you have 5 secs for a call on MYE?")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-05-05T20:52:12-00:00", "Ok. Bill now going to wrap at request of --Redacted-- He has the info - CNN breaking fbi has interviewed aides quietly at fbi building, specifically Huma")
  #strzok_to_page(child_file, "2016-05-05T20:52:27-00:00", "Ok. Bill now going to wrap at request of --Redacted-- He has the info - CNN breaking fbi has interviewed aides quietly at fbi building, specifically Huma")
  #strzok_to_page(child_file, "2016-05-06T00:37:48-00:00", "Oh, called --Redacted-- Huma's atty called just afterwards, he's talking to her and calling back.")
  strzok_to_page(child_file, "2016-05-06T00:38:09-00:00", "Oh, called --Redacted-- Huma's atty called just afterwards, he's talking to her and calling back.")

  # Page 8
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  strzok_to_page(child_file, "2016-05-06T00:41:00-00:00", "Yeah. Wonder if they're raising hell about the media stuff. All seemed very pro-Clinton camp")
  #strzok_to_page(child_file, "2016-05-06T00:42:14-00:00", "Yeah. Wonder if they're raising hell about the media stuff. All seemed very pro-Clinton camp")
  page_to_strzok(child_file, "2016-05-06T00:42:36-00:00", "Not gonna be charged isn't anyone at the fbi, that's for sure")

  # Page 9
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  strzok_to_page(child_file, "2016-05-06T01:15:10-00:00", "Sorry, --Redacted-- called right after my last text. Talked to him about our discussion this evening, also threw out the go straight to SW idea. After grumbling, he pulled out the USAM, referenced the non-target atty provisions as essentially use less intrusive means unless concerned about destruction of evidence language.\n\nGoing to go look for your email now")
  strzok_to_page(child_file, "2016-05-06T01:18:29-00:00", "Yep. And --Redacted-- was appalled by thought that we would be showing up in the atty's office with warrant to seize the laptop. I told him he could call her to let her know right before we went in the door.")

  # Page 10
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  strzok_to_page(child_file, "2016-05-06T01:19:32-00:00", "Bottom line I told him there was a very specific and definite sense of urgency, from the DD calling agencies about the class review to not wanting to get engaged in some protracted tit for tat incremental negotiation with Beth")

  # Page 11
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  m = strzok_to_page(child_file, "2016-05-09T10:41:42-00:00", "Hey, work related, with Bill out, does Andy want --Redacted-- bringing MYE daily bullets? Or email from us to you, --Redacted-- I don't see how we don't include him. And I think I def bootleg you in case he Fs it up")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-05-13T10:43:59-00:00", "Talked to --Redacted-- last night, btw. He spoke to Beth. Shockingly, she did not sound surprised about the subpoenas, said she would accept service. \U0001f612")
  strzok_to_page(child_file, "2016-05-15T23:00:35-00:00", "I need some clarifying data - just retention, right? While it might be helpful to put in Petraeus, --Redacted-- that's only to show they are different, ie, involve transmittal to another person. He just wants fact patterns where it was only retention, not disclosure, right? And taking graviman literally, list will not include more serious cases/disclosures which are more than retention.")
  #strzok_to_page(child_file, "2016-05-15T23:40:39-00:00", "I need some clarifying data - just retention, right? While it might be helpful to put in Petraeus, --Redacted-- that's only to show they are different, ie, involve transmittal to another person. He just wants fact patterns where it was only retention, not disclosure, right? And taking graviman literally, list will not include more serious cases/disclosures which are more than retention.")

  # Page 12
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  strzok_to_page(child_file, "2016-05-16T01:06:06-00:00", "Sigh. I know. I wish I could gift you a week somehow. \n\nTalked to Bill for about an hour. He mentioned email, said he would send (though he hasn't yet). He had a slightly different take than I did but we'll get there. His primary concern is asking Doj in such a way that they respond straight to the D (which I can see happening) without us getting a chance to review for accuracy / spin.")
  page_to_strzok(child_file, "2016-05-16T01:11:14-00:00", "If there are so few that someone like --Redacted-- would literally be able to recall them then you have much bigger problems.")
  page_to_strzok(child_file, "2016-05-16T01:11:47-00:00", "We had a list of those cases in which we authorized RICO. I'm not sure why they wouldn't, but if they don't, they're about to.")
  page_to_strzok(child_file, "2016-05-16T01:12:10-00:00", "Description might be hard. But I guess we'll see.")
  strzok_to_page(child_file, "2016-05-16T01:12:48-00:00", "The fbi can come up with a description")

  # Page 13
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  page_to_strzok(child_file, "2016-05-16T01:13:21-00:00", "I'd like to make a suggestion though. I DO NOT think you should ask --Redacted-- I think Bill should ask George --Redacted-- just going to bitch and moan. George sees the d three times a week. He is not going to say no.")
  page_to_strzok(child_file, "2016-05-16T01:16:12-00:00", "Pete. I'm trying to save you some crap from them. Don't get your back up about it. When they ask you, you talk about it. What's the big deal? All they are going to do when you tell them is wait to hear from on high. So all I'm saying is start there.")
  strzok_to_page(child_file, "2016-05-17T00:50:44-00:00", "Nah nah nah can't hear you taking out the trash and the moons up there, hiding behind a soft haze.\n\nLook, I HATE it. I own that.\n\nGotta talk to --Redacted-- shortly. Haven't heard from Mike. Curious to see what Andy and George's convo is about same topic.")
  m = strzok_to_page(child_file, "2016-05-17T01:27:44-00:00", "I'm sorry. Don't read email then. It's --Redacted-- response citing USAM 9-19.220")
  m.addnote("USAM 9-19 - DoJ Justice Manual : Documentary Material Held By Third Parties")
  m.addnote("USAM 9-19.220 - Procedures Where Privileged Materials Sought Are in Possession of a Disinterested Third Party Physician, Lawyer, or Clergyman")
  m = strzok_to_page(child_file, "2016-05-17T10:17:23-00:00", "Sorry. Truly.\n\nI'm trying to figure this out. I know it's not your job - I need Doj and NSLB to get me an answer, because I'm briefing everyone there are different options available. And the 28 CFR guidance seems problematic from a warrant perspective.")
  m.addnote("NSLB - National Security Law Branch at DOJ")
  m.addnote("28 CFR - Title 28 Code of Federal Regulations : Judicial Administration")

  # Page 14
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  strzok_to_page(child_file, "2016-05-17T10:27:20-00:00", "28 CFR is not just policy. But I think there's a path through it as you noted.\n\nSorry about your alarm. I set mine an hour early to draft the comments to --Redacted-- and punched the damn thing seventeen times.\n\nAnd happy anniversary. \U0001f61d")
  page_to_strzok(child_file, "2016-05-17T10:36:07-00:00", "Yes, this is true. But let's be honest, it's not like they've pointed to the cfr as the reason. So let them come up with something.")
  strzok_to_page(child_file, "2016-05-17T10:41:21-00:00", "They haven't pointed to it because they haven't done the research!!! But when they finally do, presumably before a meeting, they will, and we need to have a response lined up.\n\nAnd hi. I hate this case. \U0001f615")

  # Page 15
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  strzok_to_page(child_file, "2016-06-08T11:05:40-00:00", "Did I send you the draft consent letters last night? Thought I did but don't see it in sent folder.\n\nI have NO idea why we let counsel take first crack with pen.")
  page_to_strzok(child_file, "2016-06-08T11:06:39-00:00", "No, you didn't. And I have no idea. Probably bc --Redacted-- aren't real prosecutors.")
  strzok_to_page(child_file, "2016-06-08T12:16:06-00:00", "I'm REALLY angry about the consent letter right now. Much worse than last night.\n\nnit's the little things, like --Redacted-- writing no agents will participate in the otd review. That sense of entitlement about how we staff is the result of Andy not simply saying \"no\" to doj about the obnoxious filter staffing demand")
  strzok_to_page(child_file, "2016-06-08T20:25:55-00:00", "--Redacted-- just called, he's just leaving main justice. They all want to talk to me privately before group call at 4:40.")

  # Page 16
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  strzok_to_page(child_file, "2016-06-10T19:25:21-00:00", "Also, what I discussed with --Redacted-- was don't discuss specific dates, but throw the willingness out there, tell Kendall if we find a lot of material on laptops we might need more time")
  strzok_to_page(child_file, "2016-06-10T19:45:32-00:00", "Funny, I'm sure it's perfectly fine but got that funny feeling telling the DD that the D said something different from him. Andy noted he told Kendall that we wouldn't schedule interview until laptops were reviewed and D didn't have that info, then he said he'd take care of D.\n\nI just don't want him thinking that I felt he needed to explain himself to me.")
  strzok_to_page(child_file, "2016-06-12T01:31:06-00:00", "I'm torn between their achievement and the reality of the limitations it places on others. All of that separate and distinct from the bigoted hatred of half (it seems) of our population.")
  m = strzok_to_page(child_file, "2016-06-13T20:05:29-00:00", "****Also, remind me to tell you to flag for Andy three emails we (actually ICIG) found that have portion marks (C) on a couple of paras. Doj was Very Concerned about this, willing to bet they will tell George")
  m.addnote("(C) - Confidential : Unauthorized is presumed to do damage to national security")
  
  # Page 17
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  page_to_strzok(child_file, "2016-06-13T20:05:33-00:00", "Found on the laptops?")
  strzok_to_page(child_file, "2016-06-13T20:05:48-00:00", "No. Found on the 30k provided to State originally.")
  strzok_to_page(child_file, "2016-06-13T20:06:28-00:00", "No one noticed. And while minor, it cuts against \"I've never send or received anything marked classified\"")
  strzok_to_page(child_file, "2016-06-13T20:08:07-00:00", "Because they're worried, holy cow, if the fbi missed this, what else was missed?")
  strzok_to_page(child_file, "2016-06-13T20:08:39-00:00", "Which I get, because I had the same worry.\n\nAnd they like snitching to George")
  strzok_to_page(child_file, "2016-06-13T20:59:10-00:00", "Get us a clue...")

  # Page 18
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  page_to_strzok(child_file, "2016-06-13T20:59:16-00:00", "July 2")
  m = strzok_to_page(child_file, "2016-06-13T23:35:07-00:00", "Hey do you anticipate mye due-outs tonight? I think I'm going to get out of here.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-06-15T13:29:13-00:00", "Want to ask doj to ask h to come to dc. Do interview at hq. Or nvra.")
  page_to_strzok(child_file, "2016-06-15T13:30:03-00:00", "Sure why not. Is especially important if the goal is to prevent leaks.")
  strzok_to_page(child_file, "2016-06-15T17:18:42-00:00", "Trump's talking about the investigation")
  strzok_to_page(child_file, "2016-06-17T21:56:13-00:00", "Now we're talking about Clinton, and how a lot of people are holding their breath, hoping.")

  # Page 19
  # INBOX is page to Strozk
  # OUTBOX is strozk to page
  page_to_strzok(child_file, "2017-07-14T11:54:03-00:00", "http://www.cnn.com/2017/07/13/politics/peter-strzok-special-counsel-russia-fbi/index.html \n\n\U0001f602")
  page_to_strzok(child_file, "2017-12-05T02:29:49-00:00", "When you talk to --Redacted-- tomorrow, keep in mind he is fiercely loyal to Mueller. One of his concerns was you want to challenge Mueller\u2019s decision to remove you from the investigation. I told him that\u2019ds not the case at all.")
  strzok_to_page(child_file, "2017-12-05T03:06:52-00:00", "Got it, thanks. Mueller and I aree good - no disagreement or anger about decision by either of us, just sadness (all the press speculation otherwise is complete BS - shocker). Pretty sure he would say good things about me if --Redacted-- asked.")
  strzok_to_page(child_file, "2017-12-06T00:17:45-00:00", "You were spot on re Mueller. We're good.")
  page_to_strzok(child_file, "2017-12-06T01:58:28-00:00", "Are you satisfied with the outcome of the conversation?")

  # Page 20
  # 0 - Sent by strzok to page
  # 1 - Sent by page to strzok
  m = strzok_to_page_unix_epoch(child_file, 1466532475828, "Bill went long, --Redacted-- and I have to talk to him about MYE then I'm running...:D")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page_unix_epoch(child_file, 1467386723528, "But AGs talking now. Said she had decided to accept rec prior to meeting with Clinton on Monday")
  strzok_to_page_unix_epoch(child_file, 1467386748058, "Keeps calling it \"investigation of State Department emails.\" Uh, not exactly....")
  m = page_to_strzok_unix_epoch(child_file, 1467395371000, "Bill talked to him about it last night. I talked to andy about it today again. He is going to broach it with DAG extra week, be he wants CD and CyD to have a plan for review.")
  m.addnote("CD - FBI Counterintelligence Division")
  m.addnote("CyD - FBI Cyber Division")
  page_to_strzok_unix_epoch(child_file, 1467504405000, "Because the D says he's not going to say complete, just nearly complete or something like that.")
  strzok_to_page_unix_epoch(child_file, 1467504692983, "Rybicki coming in with D tomorrow...")
  strzok_to_page_unix_epoch(child_file, 1467504786223, "What are they doing? Rehearsing?")
  page_to_strzok_unix_epoch(child_file, 1467504807000, "That's my guess.")
  page_to_strzok_unix_epoch(child_file, 1467935493000, "BBC News: US State Department restarts Hillary Clinton email probe US State Department restarts Hillary Clinton email probe - http://www.bbc.co.uk/news/election-us-2016-36742095")
  strzok_to_page_unix_epoch(child_file, 1468281414631, "Ok. Will grab something and we can share. Just read the Congressional letter to the D. Also CNN poll. Has me stressed out.")
  strzok_to_page_unix_epoch(child_file, 1468494282691, "Poll Finds Emails Weighing on Hillary Clinton, Now Tied With Donald Trump http://nyti.ms/29RV5gf")
  strzok_to_page_unix_epoch(child_file, 1468882441579, "And f*ck the cheating motherf*cking Russians. Bastards. I hate them")
  m = page_to_strzok_unix_epoch(child_file, 1468895008000, "And wow, Donald Trump is an enormous d*uche.")
  m.tag("Hatred", "enormous douche is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  page_to_strzok_unix_epoch(child_file, 1468923509000, "Trump barely spoke, but the first thing out of this mouth was \"we're going to win soooo big.\" The whole thing is like living in a bad dream.")
  strzok_to_page_unix_epoch(child_file, 1468927122271, "Omg. You listening to npr? Apparently Melania's speech had passages lifted from Michele Obama's....unbelievable")
  page_to_strzok_unix_epoch(child_file, 1468927164000, "NO WAY!")
  page_to_strzok_unix_epoch(child_file, 1468927698000, "I saw that one the other day too! On the hill I think!")
  strzok_to_page_unix_epoch(child_file, 1468961119080, "Hey --Redacted-- says Toscas may call Andy about the LHM preamble. \U0001f612")
  strzok_to_page_unix_epoch(child_file, 1468966891081, "Hey do you anticipate Andy will want to meet tomorrow on Congressional response? Various OGCers asking me about deadline...m")
  page_to_strzok_unix_epoch(child_file, 1468966963000, "No. Jim said he needed letter pushed to THursday, andy said that was fine. Not sure about mtg tomorrow.")
  strzok_to_page_unix_epoch(child_file, 1469093999882, "Trump is a disaster. I have no idea how destabilizing his Presidency would be")
  strzok_to_page_unix_epoch(child_file, 1469406698793, "Wildly unrelated, is Brinkema still chief judge of the fisc?")
  page_to_strzok_unix_epoch(child_file, 1469406764000, "Don't think so. Just wiki the Fisc judges. It will tell you.")
  page_to_strzok_unix_epoch(child_file, 1469406809000, "Rosemary Collyer")
  m = page_to_strzok_unix_epoch(child_file, 1469406878000, "Rudy is on the FISC! Did you know that?")
  m.addnote("Rudy - District Judge Rudolph Contreras, judge on the FISC, judge who accepted Michael Flynn's guilty plea")
  page_to_strzok_unix_epoch(child_file, 1469406905000, "Just appointed two months ago!")
  strzok_to_page_unix_epoch(child_file, 1469406930599, "I did. We talked about it before and after. I need to get together with him")
  page_to_strzok_unix_epoch(child_file, 1469406943000, "So get the right folks in then!")
  page_to_strzok_unix_epoch(child_file, 1469407487000, "Go ask her. Thought of it bc you had to Google Fisc judges and saw him there. I'm telling you.")

  # Page 21
  # 0 - Sent by strzok
  # 1 - Sent by page
  page_to_strzok_unix_epoch(child_file, 1469407928000, "I can't imagine either one of you could talk about anything in any detail meaningful enough to warrant recusal.")
  m = strzok_to_page_unix_epoch(child_file, 1469407986489, "Really? Rudy, I'm in charge of espionage for the FBI. Any espionage FISA comes before him, what should he do, given his friend oversees them?")
  m.addnote("Rudy - District Judge Rudolph Contreras, judge on the FISC, judge who accepted Michael Flynn's guilty plea")
  strzok_to_page_unix_epoch(child_file, 1469408033812, "Ok, I believe you that I didn't. Thought I had. Happy to (indeed, wanted to and thought I did) talk about it with you.")
  page_to_strzok_unix_epoch(child_file, 1469408185000, "Standards for recusal are quite high. I just don't think this poses an actual conflict. And doesn't he know what you do?")
  strzok_to_page_unix_epoch(child_file, 1469503848030, "Oh noes. He needs to hear PBS talking about Bernie!")
  strzok_to_page_unix_epoch(child_file, 1469503863562, "They are not, so far, part of the media conspiracy for Clinton.")
  page_to_strzok_unix_epoch(child_file, 1469408185000, "Well that's a relief! :) Just watched your video (think I had seen")
  strzok_to_page_unix_epoch(child_file, 1469579852595, "Did you watch the D's happy birthday fbi message?")
  page_to_strzok_unix_epoch(child_file, 1469580469000, "I didn't yet - I worked my tail off today. I heard he made a Clinton reference though, no?")
  page_to_strzok_unix_epoch(child_file, 1469585517000, "And hey guess what, big surprise. --Redacted-- is a big R Arkansas Clinton-hater.")
  m = page_to_strzok_unix_epoch(child_file, 1469666218000, "Ha. First line made me smile. What does the US Government Know About Russia and the DNC Hack? - Lawfare https://www.lawfareblog.com/what-does-us-government-know-about-russia-and-dnc-hack")
  m.addnote("First line is: Potentially unpleasant news for Jim Comey: We need you to intervene in the 2016 election again.")
  page_to_strzok_unix_epoch(child_file, 1469666256000, "Not from --Redacted-- but yesterday --Redacted-- came by to get the emails and very briefly said Beth yelled at them and accused them of negotiating in bad faith")
  page_to_strzok_unix_epoch(child_file, 1469669924000, "Have we opened on him yet? \U0001f621 Trump & Putin. Yes, It's Really a Thing http://talkingpointsmemo.com/edblog/trump-putin-yes-it-s-really")
  strzok_to_page_unix_epoch(child_file, 1469670664244, "Opened on Trump? If Hillary did, you know 5 field offices would...")
  strzok_to_page_unix_epoch(child_file, 1469748499630, "--Redacted--")
  page_to_strzok_unix_epoch(child_file, 1469748575000, "Yep but people would suspect. --Redacted-- nobody would even think about. --Redacted-- will be noticed")
  page_to_strzok_unix_epoch(child_file, 1469749072000, "Got it. I just think the impact on WFO is much less with --Redacted-- and will be noticed less. Taking out --Redacted-- right now given what he does there would have big impact.")
  strzok_to_page_unix_epoch(child_file, 1469749216592, "How many and where are the current open cases?")
  page_to_strzok_unix_epoch(child_file, 1469749299000, "One. I think Ny?")
  page_to_strzok_unix_epoch(child_file, 1469749353000, "No plan. No strategy. That's all Bill and I have been talking about all week. Clean slate at least...")
  page_to_strzok_unix_epoch(child_file, 1469749455000, "I mean I have a plan for my side but not on ops side.")
  strzok_to_page_unix_epoch(child_file, 1469750161755, "I've got an outline of a plan. Fine, cd tells ny close and consolidate down here. I don't think we can wait 2 weeks for --Redacted--")
  page_to_strzok_unix_epoch(child_file, 1469750393000, "Yep. I will go over my plan when we get together in the morning. I think they will meet in the middle. Agreed we can't wait two weeks. It's all moving too fast.")
  strzok_to_page_unix_epoch(child_file, 1469832334694, "Ooh just saw on CNN first campaign add showing Gowdy and Comey's back and forth with a \"should HRC face criminal charges\" survey via 800 number.")
  page_to_strzok_unix_epoch(child_file, 1469832541000, "Yeah Kortan told us DCCC and Hillary Campaign hacked.")
  m = page_to_strzok_unix_epoch(child_file, 1469882759000, "Totally right there with you. Was thinking before bed last night that it is going to be hard to ramp up for testimony on MYE in the fall bc none of us are going to care at all anymore.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page_unix_epoch(child_file, 1469969571209, "Awesome. Sharing that queen with --Redacted-- is dicey.")

  # Page 22
  # 0 - Sent by strzok
  # 1 - Sent by page
  page_to_strzok_unix_epoch(child_file, 1469970524000, "What happens in --Redacted/London-- stays in --Redacted/London--")
  strzok_to_page_unix_epoch(child_file, 1469975687672, "Not sure if it matters, I'd go with whatever logistically makes sense. Top priority is the --Redacted-- and his people. Not sure if we want to share that with --Redacted--")
  strzok_to_page_unix_epoch(child_file, 1469976183352, "I think we're missing each other. I mean maybe not telling --Redacted-- all the details about the --Redacted-- contact.")
  page_to_strzok_unix_epoch(child_file, 1470015503000, "I mean seriously. What in the hell is this guy talking about? Donald Trump Gives Questionable Explanation of Events in Ukraine http://nyti.ms/2arMCyV")
  m = strzok_to_page_unix_epoch(child_file, 1470083956394, "I may need to have a CH party soon.")
  m.addnote("CH - Crossfire Hurricane")
  page_to_strzok_unix_epoch(child_file, 1470085272000, "Ho boy. Don't tell moffa, but andy is cancelling their brief. And he wants it first.")
  strzok_to_page_unix_epoch(child_file, 1470116147502, "Landed safely. Rainy and 63... hope your stinkies let you sleep well")
  strzok_to_page_unix_epoch(child_file, 1470116181630, "Just landed")
  page_to_strzok_unix_epoch(child_file, 1470103465000, "Ok cool. --Redacted/Heathrow-- Express to --Redacted/Paddington-- Station, taxi stand, to US Emb")
  page_to_strzok_unix_epoch(child_file, 1470103465000, "Ok cool. --Redacted/Heathrow-- Express to --Redacted/Paddington-- Station, taxi stand, to US Emb")
  strzok_to_page_unix_epoch(child_file, 1470139464166, "It's been interesting. ...our request apparently percolated up to their --Redacted/PM-- and they want me and Joe to sign somethig")
  strzok_to_page_unix_epoch(child_file, 1470139478958, "With the --Redacted/Red-- yes, good meeting")
  page_to_strzok_unix_epoch(child_file, 1470125169000, "Make sure you can lawfully protect what you sign. Just thinking about congress, foia, etc.")
  page_to_strzok_unix_epoch(child_file, 1470125225000, "I'm sure it's fine, I just don't know how protection of intel-type stuff works in that context.")
  m = page_to_strzok_unix_epoch(child_file, 1470174199000, "Just you two? Was DCM present for the interview?")
  m.addnote("DCM - Deputy Chief of Mission" )
  strzok_to_page_unix_epoch(child_file, 1470188618891, "No. Two of them, two of us.")
  m = strzok_to_page_unix_epoch(child_file, 1470355172014, "Yep. Trying to be grownup and not ask to come tomorrow based upon mye/--Redacted--/CH overlap. --Redacted-- brief, he's got it. I just love, and am good, at thinking through it.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  m = strzok_to_page_unix_epoch(child_file, 1470406143095, "Have M w f meetings with ch team at 9 like we did with mye. Need to tall to you about Bill")
  m.addnote("ch - Crossfire Hurricane, mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1470406521000, "Coming now")
  page_to_strzok_unix_epoch(child_file, 1470408644000, "--Redacted-- too, right?")
  # Unredaction from https://thehill.com/opinion/campaign/392342-senate-probes-fbis-heavy-handed-use-of-redactions-to-obstruct-congressional/
  strzok_to_page_unix_epoch(child_file, 1470415038866, "And hi. Went well, best we could have expected. Other than L.C's quote \"the White House is running this.\"")
  strzok_to_page_unix_epoch(child_file, 1470415549978, "My answer, \"well, maybe for you they are.\" \U0001f612")
  page_to_strzok_unix_epoch(child_file, 1470416126000, "Yeah, whatever (re the WH comment). We've got emails that say otherwise.")
  m = page_to_strzok_unix_epoch(child_file, 1470494290000, "Jesus. You should read this. And Trump should go f himself. Moment in Convention Glare Shakes Up Khans' American Life http://nyti.ms")
  m.tag("Hatred", "f himself is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  m = page_to_strzok_unix_epoch(child_file, 1470495300000, "And maybe you're meant to stay where you are because you're meant to protect the country from that menace. To that end, read this: Trump's Enablers Will Finally Have to Take a Stand http://nyti.ms/2aFakry")
  m.tag("Hatred", "menace is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  page_to_strzok_unix_epoch(child_file, 1470713184000, "He's not ever going to become president, right? Right?!")
  strzok_to_page_unix_epoch(child_file, 1470714035303, "No. No he's not. We'll stop it.")
  strzok_to_page_unix_epoch(child_file, 1470737324804, "What prompted the Trump.comment last night?")
  strzok_to_page_unix_epoch(child_file, 1470876493707, "So. You come up with a codename? Crossfire --Redacted--.")
  page_to_strzok_unix_epoch(child_file, 1470876686000, "Crossfire Latitude?")
  m = page_to_strzok_unix_epoch(child_file, 1470876864000, "Trying to think of something loosely military, without being obvious.")
  m.addnote("Crossfire Latitude - Probably Michael Flynn")
  
  # Page 23
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1470877015149, "Crossfire YUUUUGE. Though we may save that for the man, if we ever open on him ;)")
  strzok_to_page_unix_epoch(child_file, 1470877046865, "OMG I CANNOT BELIEVE WE ARE SERIOUSLY LOOKING AT THESE ALLEGATIONS AND THE PERVASIVE CONNECTIONS")
  strzok_to_page_unix_epoch(child_file, 1470877059333, "What the hell has happened to our country!?!?!??")
  m = strzok_to_page_unix_epoch(child_file, 1471003489380, "Bill sent an email asking to see me at 9 or 11....have a CH team mtg at 9, so 11 it is")
  m.addnote("CH - Crossfire Hurricane")
  strzok_to_page_unix_epoch(child_file, 1471172513957, "I'm worried about what happens if HRC is elected. And perfect, another excessive heat warning day.")
  strzok_to_page_unix_epoch(child_file, 1471209211713, "Rybicki just emailed me about availability/readiness to do D brief tomorrow at 3:30...I told him we would, same personne lineup from us as with MYE")
  page_to_strzok_unix_epoch(child_file, 1471568009000, "Ukraine Releases More Details on Payments for Trump Aide http://nyti.ms/2breAOV")
  page_to_strzok_unix_epoch(child_file, 1471914236000, "Yeah. Sorry I'm in a bit of a buzz kill place as D is still up and reading the IG report. It's really dry...")
  strzok_to_page_unix_epoch(child_file, 1472229758368, "Just went to a southern Virginia Walmart. I could SMELL the Trump support....")
  m = strzok_to_page_unix_epoch(child_file, 1472394726951, "I AM DONE WITH MYE!!!!\U0001f621\U0001f621")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1472550343000, "D said at am brief thst Reid called him and told him he would be sending a le t ter.")
  strzok_to_page_unix_epoch(child_file, 1472550384349, "Bill didn't mention it \U0001f612")
  strzok_to_page_unix_epoch(child_file, 1472550713599, "And holy cow, let me send you the Reid letter!")
  m = page_to_strzok_unix_epoch(child_file, 1472753269000, "Just got another call from quinn re MYE. Should I direct his call to Steinbach?")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  m = page_to_strzok_unix_epoch(child_file, 1472771810000, "I can't. Now the Midyear production has to happen tomorrow. And you and --Redacted-- and --Redacted-- are all out.")
  m.addnote("Midyear - Midyear Exam (Hillary Clinton)")
  strzok_to_page_unix_epoch(child_file, 1472772176058, "What is production at this point? Certainly, that you can't do from home?")
  page_to_strzok_unix_epoch(child_file, 1472772360000, "Yeah, and get everyone the copies they need, and tell baker and doj and wait for all the hill notifications and tell the agency. I'm not giving State and advance warning. F them.")
  strzok_to_page_unix_epoch(child_file, 1472773899225, "And yes, totally. F state. No heads up")
  m = strzok_to_page_unix_epoch(child_file, 1472780310923, "And I'm not going to stop telling you that's a bad decision, that the bureau - and MYE - will be just fine")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1472824229000, "Yes, bc potus wants to know everything we are doing.")
  strzok_to_page_unix_epoch(child_file, 1473511971706, "Re 302s, didn't search the laptops given to us voluntarily by various attorneys.")
  page_to_strzok_unix_epoch(child_file, 1473512028000, "Why not? Decision that it was unlikely to contain info relevant to our case in like of time constraints?")
  strzok_to_page_unix_epoch(child_file, 1473512154597, "They would not consent and we did not have probable cause to get on them.")
  strzok_to_page_unix_epoch(child_file, 1473512203817, "I will go review the 302s we didn't turn over and send thoughts to everyone except the 0 corridor recipients. You or Trisha or Jason can mention to them.")
  page_to_strzok_unix_epoch(child_file, 1473512220000, "Oh well that's totally defendable. Why did they give them to us? Yeah, but I think that was the context in which it was meant. I.e. like who sucks more")
  page_to_strzok_unix_epoch(child_file, 1473512410000, "Call for one minute? Question about the laptops.")
  page_to_strzok_unix_epoch(child_file, 1473516903000, "IG. I know is just an oversight. Just not great given timing.")
  strzok_to_page_unix_epoch(child_file, 1473516951424, "As long as we get it to them before it comes out in FOIA I think we're ok. I will call him on Mon. Heck, I can leave a vm this weekend.")
  strzok_to_page_unix_epoch(child_file, 1473616365471, "Good idea. Yeah, it's fine. Almost all about production to Congress, punting on everything else.")

  # Page 24
  # 0 - Sent by strzok
  # 1 - Sent by page
  page_to_strzok_unix_epoch(child_file, 1473616568000, "Roger. I'm dreading the week ahead. A lot on the docket. I guess I don't know how to prep for the Director Tuesday either other than to just re-read the LHM and my old notes...")
  strzok_to_page_unix_epoch(child_file, 1473616637298, "That's all I'm doing.")
  strzok_to_page_unix_epoch(child_file, 1473616672095, "We should focus on the criticism from Gowdy and others, you let this guy off, you didn't pursue this, etc.")
  strzok_to_page_unix_epoch(child_file, 1473697628326, "Also going to call --Redacted-- and tell them I want to specifically use him as a source of tasking")
  strzok_to_page_unix_epoch(child_file, 1473714556649, "Chaffetz is horrible....")
  strzok_to_page_unix_epoch(child_file, 1473714568607, "Expected blustering. ...")
  page_to_strzok_unix_epoch(child_file, 1473714833000, "God, glad I'm not watching...")
  strzok_to_page_unix_epoch(child_file, 1473716865662, "Omg Gowdy is being a total dick. All investigative questions. And Jason isn't always sticking to the script on \"I'm not answering that.\"")
  strzok_to_page_unix_epoch(child_file, 1473716869884, "Horrible")
  page_to_strzok_unix_epoch(child_file, 1473717097000, "Oof.")
  strzok_to_page_unix_epoch(child_file, 1473717295055, "This was a mistake")
  page_to_strzok_unix_epoch(child_file, 1473717588000, "Oh no.")
  strzok_to_page_unix_epoch(child_file, 1473717622779, "Lis, it's bad")
  strzok_to_page_unix_epoch(child_file, 1473717669030, "posturing. He haven't done anything wrong. But we look like sh*t")
  m = strzok_to_page_unix_epoch(child_file, 1473979766170, "Fysa, via legat, Ambo Moscow wants to meet D week of Oct 17 to discuss hacking and reciprocity. lod filling out visit request")
  m.addnote("fysa - For Your Situational Awareness")
  page_to_strzok_unix_epoch(child_file, 1474503589000, "Two Ex-Spies and Donald Trump http://nyti.ms/2cYynG6")
  m = page_to_strzok_unix_epoch(child_file, 1474630344000, "She fix the mye one?")
  m.addnote("mye - Midyear Exam (Hillary Clinton)" )
  page_to_strzok_unix_epoch(child_file, 1474936405000, "Did you read this? It's scathing. And I'm scared. Why Donald Trump Should Not Be President http://nyti.ms/2dbQPuR")
  strzok_to_page_unix_epoch(child_file, 1475804855804, "Sigh")
  page_to_strzok_unix_epoch(child_file, 1475834475000, "That sucks.")
  page_to_strzok_unix_epoch(child_file, 1475930133000, "You have a path toward progress?")
  page_to_strzok_unix_epoch(child_file, 1476020165000, "Well Andy AND D are out all week anyway.")
  page_to_strzok_unix_epoch(child_file, 1476020249000, "God, now I want to know what it is.")
  strzok_to_page_unix_epoch(child_file, 1476047032686, "Sigh. And yet, once he gets in there, hopefully just fine.")
  strzok_to_page_unix_epoch(child_file, 1476062593185, "Question about how I'm feeling about our discussion?")
  m = strzok_to_page_unix_epoch(child_file, 1476062632032, "Trump saying agents at FBI are furious at the MYE outcome and he's getting a special prosecutor.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1476241496000, "Hot damn. Big news day. Buffett Calls Trump's Bluff Releases His Tax Data http://nyti.ms/2sSIOM5")
  page_to_strzok_unix_epoch(child_file, 1476925870000, "I'm sending you a neat article on parenting, but just read it later when you're not riled up with the debate.")
  strzok_to_page_unix_epoch(child_file, 1476926108407, "WE WILL GET YOU A STUNNING SUNDAE I cannot believe what I am hearing.")
  m = strzok_to_page_unix_epoch(child_file, 1476926141257, "I am riled up. Trump is a fucking idiot, is unable to provide a coherent answer.")
  m.tag("Hatred", "'fucking idiot' is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  page_to_strzok_unix_epoch(child_file, 1476926200000, "It looks and sounds like a Saturday Night Live skit.")
  page_to_strzok_unix_epoch(child_file, 1476926441000, "--Redacted-- It's not worth your stress either. Come to be")
  strzok_to_page_unix_epoch(child_file, 1476926552475, "I CAN'T PULL AWAY. WHAT THE FUCK HAPPENED TO OUR COUNTRY, LIS?!??!?!")
  strzok_to_page_unix_epoch(child_file, 1476926585395, "And Jesus. --Redacted-- is the ONE thing that could pull me away from this nightmare.")

  # Page 25
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1476926613564, "Bad hombres? That's some jive turkey talk, honkey!")
  page_to_strzok_unix_epoch(child_file, 1476926660000, "I don't know. But we'll get it back. We're America. We rock.")
  strzok_to_page_unix_epoch(child_file, 1476926897393, "Donald just said \"bad hombres\" \U0001f612")
  strzok_to_page_unix_epoch(child_file, 1476926917905, "Chris Wallace is a turd")
  strzok_to_page_unix_epoch(child_file, 1476927015337, "Hillary: Russia and Wikileaks and highest levels of Russian Government and Putin!!! Drink!!!!")
  page_to_strzok_unix_epoch(child_file, 1476927026000, "Do bald eagles cry? The moderator is quoting stolen material from Wikileaks in questions. Trump says \"thank you.\"")
  strzok_to_page_unix_epoch(child_file, 1476927156198, "Oh hot damn. HRC is throwing down saying Trump in bed with russia")
  page_to_strzok_unix_epoch(child_file, 1476928007000, "And yet again it's 10 and I'm not in bed like I wanted to be.")
  page_to_strzok_unix_epoch(child_file, 1476928230000, "Baby, what is watching going to accomplish? Go to bed now, get some rest. You can read about it in the morning. Even watch if you must. Plus you need to get up early to run.")
  strzok_to_page_unix_epoch(child_file, 1476928277038, "I'll run. Will be too angry and need to get it out.")
  page_to_strzok_unix_epoch(child_file, 1476951284000, "Yes, yes I am still up with her. God, I am DONE. \U0001f620\U0001f620\U0001f620")
  strzok_to_page_unix_epoch(child_file, 1477009998440, "When and where? Bastard. Retiree with no responsibility, I bear the weight of the free world on my shoulders.")
  page_to_strzok_unix_epoch(child_file, 1477383433000, "And I'm up. Up up. I should just take a shower and drive in. \U0001f616")
  page_to_strzok_unix_epoch(child_file, 1477384029000, "And read it again and I'm sobbing again. Sigh.")
  page_to_strzok_unix_epoch(child_file, 1477481282000, "Sigh.")
  strzok_to_page_unix_epoch(child_file, 1477481457419, "We'll listen together later. \U0001f642")
  page_to_strzok_unix_epoch(child_file, 1477481463000, "You're silly.")
  strzok_to_page_unix_epoch(child_file, 1477676108326, "K. Door is closed, just walk in.")
  page_to_strzok_unix_epoch(child_file, 1477692140000, "Christ. It's there led on freaking MARKETPLACE.")
  page_to_strzok_unix_epoch(child_file, 1477693473000, "I'm sorry.")
  page_to_strzok_unix_epoch(child_file, 1477841573000, "Almost here. Will try to put the phone away until 1.")
  strzok_to_page_unix_epoch(child_file, 1477856947531, "Oh god babe. I'm sorry Talked to Bill here he's leaning not telling Bill,he was going to call Baker. We need that Kortan info go to weigh in the decision.")
  strzok_to_page_unix_epoch(child_file, 1477862123995, "As long as you'll hire me in 3 years, I'm fine....")
  page_to_strzok_unix_epoch(child_file, 1477959293000, "Great. Can't wait to hear his thoughts.")
  strzok_to_page_unix_epoch(child_file, 1478133346815, "Get one for me and Bill later")
  # Page 431 has unredacted version of this message
  # strzok_to_page_unix_epoch(child_file, 1478133386961, "I'm sure if --Redacted-- sees it the Q will be why not them, too. stupid politics.")
  strzok_to_page_unix_epoch(child_file, 1478133415132, "Or get it for my original plan and do the kiss ass chain of command plan later.")
  page_to_strzok_unix_epoch(child_file, 1478134357000, "Sorry. Rybicki called. Time line article in the post is super specific and not good. Doesn't make sense because I didn't have specific information to give.")
  page_to_strzok_unix_epoch(child_file, 1478135738000, "Okay I can talk again.")
  page_to_strzok_unix_epoch(child_file, 1478141368000, "Ok I should be able to when you are free.")
  page_to_strzok_unix_epoch(child_file, 1478226117000, "So just fly out tomorrow night. You don't need her permission. We might have this stmt out and be substantially done. Leave --Redacted-- with moffa.")
  # Unredacted version on Page 433
  # page_to_strzok_unix_epoch(child_file, 1478226221000, "No Pete. It's your JOB. And plus --Redacted-- actually knows what you're doing this time. And that the American presidential election, and thus, the state of the world, actually hangs in the balance.")
  page_to_strzok_unix_epoch(child_file, 1478226241000, "Do you think --Redacted-- get jealous envious because your job is more important and sexy than --Redacted--")
  page_to_strzok_unix_epoch(child_file, 1478226336000, "You either start with a new blank slate on Nov. 9 or you never make it Pete. You will never live down that unmeasurable subjective debt.")
  page_to_strzok_unix_epoch(child_file, 1478465574000, "I'm on fox. Trump is talking about her.")

  # Page 26
  # 0 - Sent by strzok
  # 1 - Sent by page
  page_to_strzok_unix_epoch(child_file, 1478465621000, "He's talking about cartwright and Petreaeus and how they're not protected. She's protected by a rigged system.")
  page_to_strzok_unix_epoch(child_file, 1478568722000, "Impressive in its accuracy. \U0001f612 How the F.B.I. Reviewed Thousands of Emails in One Week http://nyti.ms/2egA2sg")
  m = strzok_to_page_unix_epoch(child_file, 1478620108312, "Is he going to the Crossfire room, or just sioc?")
  m.addnote( "SIOC is the FBI Strategic Information and Operations Center" )
  # Page 438 has "duhadaway" unredacted
  page_to_strzok_unix_epoch(child_file, 1478620156000, "He will go see the analysts, crossfire room, and sioc. Maybe I'll take him by duhadaway as well.")
  # Page 438 has "Duhadway" unredacted
  strzok_to_page_unix_epoch(child_file, 1478620325985, "Ok, I'm with Crossfire but going to Duhadway at 11 with --Redacted--")
  page_to_strzok_unix_epoch(child_file, 1478921100500, "Yeah, and then the Deputy Director told you to go to --Redacted-- on 24 hours notice.")
  strzok_to_page_unix_epoch(child_file, 1479410538827, "Re your email, --Redacted-- know --Redacted-- briefed Pence, right (just so there are no surprises)?")
  m = page_to_strzok_unix_epoch(child_file, 1479411152000, "Re above re email, it might be more important for Evanina to know that --Redacted-- briefed Pence, no?")
  m.addnote("Evanina is most likely William R. Evanina serving as National Counterintelligence Executive")
  # This area is in page 443 of Appendix C - DOJ-PROD-0000325
  # Strzok and Page talked about infiltrating Pence transition team, quotes from messages are "potential relationships", "the CI guy", "demeanor", "He can assess if thete are any news Qs, or different demeanor. If Katie’s husband is there, he can see if there are people we can develop for potential relationships"
  # https://news.yahoo.com/pence-lashes-strzok-page-talk-181757695.html 
  # Text messages in https://www.scribd.com/document/407635731/Strzok-Page-text-readout
  m = page_to_strzok_unix_epoch(child_file, 1479505710000, "Is Moffa there? I have a MYE q for him.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1479847159000, "Yo. Why are we doing MYE with the D next week?")
  m = strzok_to_page_unix_epoch(child_file, 1479847898258, "Why are we briefing D next week on mye??")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1481418614000, "Great. This sentence aggravated the s out of me. Trump has threatened a lot of people and he's about to be in control of the most pervasive and least accountable surveillance infrastructure in the world.\" Mr. Marlinspike said. \"A lot of people are justifiably concerned about that.\" NYTimes: Worried About the Privacy of Your Messages? Download Signal Worried About the Privacy of Your Messages? Download Signal http://nyti.ms/2hjyVVo")
  strzok_to_page_unix_epoch(child_file, 1481419694608, "Yeah, me too. Don't know who or where to support....")
  strzok_to_page_unix_epoch(child_file, 1481671524119, "Ok, I need to go back in with Bill. Jen and Dina still there. Call me later....particularly interested if D gave a fuller description of his convo with Brennan.")
  page_to_strzok_unix_epoch(child_file, 1481685380000, "NYTimes: Democratic House Candidates Were Also Targets of Russian Hacking Democratic House Candidates Were Also Targets of Russian Hacking http://nyti.ms/2hCOgeY")
  strzok_to_page_unix_epoch(child_file, 1481776347701, "Whatever fine. Let's see where Bill stand. We can move that and Crossfire and whatever. --Redacted--")
  m = page_to_strzok_unix_epoch(child_file, 1481803653000, "Let's talk later, but I'll just say re CH, I didn't realize there was continued rawness there because we were all obviously pissed about it, and expect to convince bill that he's wrong. So I didn't realize there was real rawness there to be sensitive to.")
  m.addnote("CH - Crossfire Hurricane")
  page_to_strzok_unix_epoch(child_file, 1481804425000, "You should tell him that. He is making a mistake, and we all think so. Do you think it makes sense to bring --Redacted-- into the CH convo? You guys do well tag t")
  strzok_to_page_unix_epoch(child_file, 1481943415017, "The re-write headline is still wrong - \" FBI in agreement with CIA that Russia aimed to help Trump win White House\"")
  strzok_to_page_unix_epoch(child_file, 1481979278108, "And OPA wasn't able to get the stupid WP headline changed. \"FBI agrees with CIA that Russia aimed to help Trump win.\"")
  page_to_strzok_unix_epoch(child_file, 1482060648000, "Andy and --Redacted-- are going to --Redacted-- in January. Hasn't told me why or what reason yet, though I sort of asked. Makes me pretty damn resentful.")
  page_to_strzok_unix_epoch(child_file, 1482070198000, "Especially because --Redacted-- has been here for one week, and he's already got a trip planned? AND if it's --Redacted-- it feel like it has to be CH related to some degree, so sure, take --Redacted--")

  # Page 27
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1482070271905, "I can't imagine it's CH and he wouldn't take you.")
  page_to_strzok_unix_epoch(child_file, 1482070305000, "There is no way he goes to --Redacted-- and it doesn't come up.")
  strzok_to_page_unix_epoch(child_file, 1482070357326, "True, I guess. He did ask --Redacted-- if he wanted a copy of the influence paper I brought up Fri nighy5")
  strzok_to_page_unix_epoch(child_file, 1482072196610, "I'm kinda resentful abouot this --Redacted-- Jan trip. Why would he answer --Redacted-- Was he not thinking just trying to be funny?")
  page_to_strzok_unix_epoch(child_file, 1482234791000, "I have no idea what you're talking about. Re hrc?")
  page_to_strzok_unix_epoch(child_file, 1482234885000, "Ogc would usually participate in the osc/other stuff, like answer my question re turning over a full page of notes vs redacted but other than three people, ogc has been recused. Is that what you mean?")
  strzok_to_page_unix_epoch(child_file, 1482234887677, "Yes. And the osc. Don't know if the ig has reached out.")
  strzok_to_page_unix_epoch(child_file, 1482234944361, "Yes. Who hasn't been recused in OGC, ie, who can answer those qiestions? And I'm reacting my notes....")
  page_to_strzok_unix_epoch(child_file, 1482234954000, "Just to Bowdich. \U0001f612")
  strzok_to_page_unix_epoch(child_file, 1482234990003, "Not following re Bowdich?")
  page_to_strzok_unix_epoch(child_file, 1482235012000, "All of ogc has been recused except for the three people who will come interview you.")
  page_to_strzok_unix_epoch(child_file, 1482235028000, "IG has spoken to him. Mostly just updates.")
  strzok_to_page_unix_epoch(child_file, 1482235066668, "Ah. Didn't know they were ogc. And boy, that's suboptimal. Wonder if I will talk to them. You probably")
  page_to_strzok_unix_epoch(child_file, 1482235107000, "You will. Guarantee.")
  strzok_to_page_unix_epoch(child_file, 1482235134482, "You getting outside counsel for it?")
  page_to_strzok_unix_epoch(child_file, 1482235164000, "For osc? No way. Also no for IG. We're not the subject.")
  page_to_strzok_unix_epoch(child_file, 1482496696000, "Brennan on npr talking about reponse to Russia")
  m = strzok_to_page_unix_epoch(child_file, 1483493325885, "Case stuff. Big picture not at ease with outcome of mye, and need for all of us to step back and be strategic in action/engagement")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  m = strzok_to_page_unix_epoch(child_file, 1483493394440, "He, like us, is concerned with over sharing. Doesn't want Clapper giving CR --Redacted/call-- to WH. All political, just shows our hand and potentially makes enemies.")
  m.addnote("CR - Crossfire Razor - Cover term for Flynn investigation")
  page_to_strzok_unix_epoch(child_file, 1483494669000, "Yeah, but keep in mind we were going to put that in the doc on friday, with potentially larger distribution then just the dni.")
  strzok_to_page_unix_epoch(child_file, 1483494824545, "The question is should we, particularly to the entirety of the lame duck usic with partisan axes to grind.")
  strzok_to_page_unix_epoch(child_file, 1483748790657, "Phil Mudd just did a nice job on CNN I'm going to head out - last chance for anything, including a ShakeShack burger....")
  m = page_to_strzok_unix_epoch(child_file, 1484178993000, "Okay. Is it about the CF meeting today?")
  m.addnote("CF - Crossfire Fury - Paul Manafort")
  page_to_strzok_unix_epoch(child_file, 1484269521000, "Did you write up the difference for the D re what you testified to? Might be useful if it comes up before the house tomorrow.")
  m = page_to_strzok_unix_epoch(child_file, 1484785107000, "Haven't thought about it yet. Hey, can you call --Redacted-- re the MYE brown bag? I should have let him know too.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page_unix_epoch(child_file, 1484785139067, "Yes")
  m = strzok_to_page_unix_epoch(child_file, 1484785210241, "Hey, Lisa confirmed a brown bag lunch with Baker on Monday to talk about mye stuff. All the things going on. Don't have a time or location yet")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1484826342000, "Get inspired and depressing reading that article about how Obama approached the mail room. Needless to say, it was very different when I interned there under Clinton.")
  m = page_to_strzok_unix_epoch(child_file, 1484883807000, "Sorry, bickered some, then got over it and watched the second sherlock. I'm really angry about the times article. This just has got to stop.")
  m.addnote("CH - Crossfire Hurricane")

  # Page 28
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1484913859835, "Yeah and it's not evern news! No substance, and largely wrong. The press is going to undermine it's credibility.")
  page_to_strzok_unix_epoch(child_file, 1485094108000, "I think we need to set up a reset meeting re the CH cases for when andy is back. I'm concerned that Bill has such a misunderstanding.")
  page_to_strzok_unix_epoch(child_file, 1485221615000, "See the photo caption NYTimes: Foreign Payments to Trump Firms Violate Constitution, Suit Will Claim Foreign Payments to Trump Firms Violate Constitutio")
  strzok_to_page_unix_epoch(child_file, 1485269191644, "NYTimes: Trump Is Said to Keep James Comey as F.B.I. Director Trump Is Said to Keep James Comey as F.B.I. Director https://nyti.ms/2knrzpO")
  m = strzok_to_page_unix_epoch(child_file, 1485386925242, "Sigh. Assume there's Razor discussion I would like to be a part of. Glad you're there.")
  m.addnote("Razor - Crossfire Razor - Michael Flynn")
  page_to_strzok_unix_epoch(child_file, 1485576792000, "God this is so depressing. NYTimes: Fears That Trump's Visa Ban Betrays Friends and Bolsters Enemies Fears That Trump's Visa Ban Betr")
  page_to_strzok_unix_epoch(child_file, 1485910332000, "Do you see the mockery Trump I'd making of his nominees? The spectacle is appalling.")
  strzok_to_page_unix_epoch(child_file, 1485910448776, "Yeah somebody jokes it was like a college recruit announcing what college he's going to. Remind me --Redacted-- story...")
  page_to_strzok_unix_epoch(child_file, 1486354826000, "Sorry to change the topic but this was really good. NYTimes: Donald Trump's Phony Compassion for Christians Donald Trump's Phony Compassion for Christians https://nyti.ms/2kDcSyE")
  page_to_strzok_unix_epoch(child_file, 1486596187000, "Please let andy know when you know more re flynn")
  strzok_to_page_unix_epoch(child_file, 1486598555352, "Just heard from --Redacted-- he said he went \"up to Flynn's office\" and was unable to get validation of either the brief or the EO.")
  page_to_strzok_unix_epoch(child_file, 1487037670000, "Man, the news is all over the post article.")
  strzok_to_page_unix_epoch(child_file, 1487038458155, "How do you mean?")
  m = strzok_to_page_unix_epoch(child_file, 1487039114913, "Need to imsg pls")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok_unix_epoch(child_file, 1487039204000, "Yes go ahead")
  strzok_to_page_unix_epoch(child_file, 1487068802455, "Hi. Flynn's out")
  page_to_strzok_unix_epoch(child_file, 1487068956000, "Yup, I saw.")
  strzok_to_page_unix_epoch(child_file, 1487210542408, "You read the WP article today? Bad, in an opposite from NYT sense b")
  m = page_to_strzok_unix_epoch(child_file, 1487211490000, "Has typh. 302 been finalized?")
  m.addnote("typh - Crossfire Typhoon - George Papadopoulos")
  strzok_to_page_unix_epoch(child_file, 1487211718744, "And sent, elsewhere")
  page_to_strzok_unix_epoch(child_file, 1487211802000, "Ah. No, meant what I asked.")
  page_to_strzok_unix_epoch(child_file, 1487211885000, "Note the bcc.")
  strzok_to_page_unix_epoch(child_file, 1487211898368, "K")
  page_to_strzok_unix_epoch(child_file, 1487212795000, "Whatever. Whole place is on my nerves. Time to move on I think. Been a tough 2 years. That WaPo article is detailed.")
  strzok_to_page_unix_epoch(child_file, 1487213122038, "I'm really angry with them. They lost huge credibility and f*cked us as well")
  page_to_strzok_unix_epoch(child_file, 1487242552000, "Did you see this? NYTimes: White House Plans to Have Trump Ally Review Intelligence Angencies White Plans to Have Trump Ally Review Intelligence Agencies https://nyti.ms/2kM1Kw7")
  m = strzok_to_page_unix_epoch(child_file, 1487242824533, "Yeah, just read it. Imsg?")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  m = strzok_to_page_unix_epoch(child_file, 1487282253523, "Check WP feed. Article 20 minutes ago that F denied discussing sanctions")
  m.addnote("F - Michael Flynn") 
  strzok_to_page_unix_epoch(child_file, 1487941990845, "CNN running hard about the story. Just had a positive piece about us buttressed by senator/congressman (didn't get his name)")
  page_to_strzok_unix_epoch(child_file, 1488249432000, "Immunity before we've ever spoken. Okey doke.")

  # Page 29
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1488249481053, "BUT WE DON'T GET THE URGENCY, LIS!!!! WE MAY NEVER GET AN OPPORTUNITY LIKE THIS AGAIN!!!!!!!!!!!")
  page_to_strzok_unix_epoch(child_file, 1488249556000, "How far we've gone... NYTimes: Former President George W. Bush Levels Tacit Criticism at Trump Former President George W. Bush Levels Tacit Criticism at Trump https://nyti.ms/2myd4x6")
  page_to_strzok_unix_epoch(child_file, 1488249576000, "Right. \U0001f612")
  strzok_to_page_unix_epoch(child_file, 1488249620699, "Oh, was the thing where he essentially says we need a free press to \"keep guys like me in check\"?")
  page_to_strzok_unix_epoch(child_file, 1488249640000, "Yes")
  strzok_to_page_unix_epoch(child_file, 1488249698732, "Yeah we're pretty much a catastrophuck right now")
  page_to_strzok_unix_epoch(child_file, 1488416463000, "See times story. Should be th eguys correcting their story.")
  strzok_to_page_unix_epoch(child_file, 1488416466601, "Nyt now. Wtf are they doing?!?!")
  page_to_strzok_unix_epoch(child_file, 1488416518000, "Correcting their story, preserving their reput5?")
  page_to_strzok_unix_epoch(child_file, 1488416523000, "Reputation?")
  strzok_to_page_unix_epoch(child_file, 1488416524624, "It's not. In some ways it's doubling down on the inaccuracies. Was the word that they were fixing it?")
  page_to_strzok_unix_epoch(child_file, 1488416556000, "Omg T1!!!!!")
  page_to_strzok_unix_epoch(child_file, 1488416572000, "That's what kortan said.")
  page_to_strzok_unix_epoch(child_file, 1488416577000, "to andy")
  strzok_to_page_unix_epoch(child_file, 1488416676137, "Yep")
  page_to_strzok_unix_epoch(child_file, 1488416700000, "It's long, I can't read it now. Let's discuss later. Seems okay so far.")
  strzok_to_page_unix_epoch(child_file, 1488416747848, "I haven't either. Got to the first and accuracy, got angry, and decided to focus on driving. Sounds like a plan.")
  strzok_to_page_unix_epoch(child_file, 1488416765310, "Inaccuracy")
  strzok_to_page_unix_epoch(child_file, 1488416802875, "T1.....")
  page_to_strzok_unix_epoch(child_file, 1488424157000, "And then this happened... BBC News: Trump Russia: House intelligence committoo agrees inquiry I saw this on the BBC and thought you should see it: Trump Russia: House intelligence committee agrees inquiry - http://www.bbc.co.uk/news/world-us-canada-39136118")
  strzok_to_page_unix_epoch(child_file, 1488424390879, "Oh good")
  page_to_strzok_unix_epoch(child_file, 1488424712000, "Ok. That makes sense.")
  page_to_strzok_unix_epoch(child_file, 1488929760000, "I'm about to explode re --Redacted--. But I'll have to tell you later. I'm furious. \U0001f620\U0001f620\U0001f620\U0001f620\U0001f620\U0001f620")
  strzok_to_page_unix_epoch(child_file, 1488929787423, "Something related to the cases/TPs?")
  page_to_strzok_unix_epoch(child_file, 1488929806000, "Yup. Exceptionally bad judgement.")
  strzok_to_page_unix_epoch(child_file, 1488929895214, "F*ck. Bad? Anything we need to mitigate?")
  page_to_strzok_unix_epoch(child_file, 1489154808000, "Cnn")
  page_to_strzok_unix_epoch(child_file, 1489154828000, "They're still obsessed with the Russian bank stuff.")
  strzok_to_page_unix_epoch(child_file, 1489159242010, "Hey leave early enough for time to tell me what JR said so we can cook up our story. I'm outside of kortans")
  page_to_strzok_unix_epoch(child_file, 1489159287000, "I haven't connected with jr.")
  strzok_to_page_unix_epoch(child_file, 1489159356949, "Ok left a yummy in your office")
  m = page_to_strzok_unix_epoch(child_file, 1489543336000, "And hi. Finally two pages away from finishing atpm. Did you know the president resigns in the end?!")
  m.addnote("atpm - All the President's Men by Bob Woodward and Carl Bernstein")
  page_to_strzok_unix_epoch(child_file, 1489543347000, "\U0001f642")

  # Page 30
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1489543637487, "What?!?! God, that we should be so lucky")
  page_to_strzok_unix_epoch(child_file, 1489543894000, "You can give it to me. No promises that I read it though. All I want for the trip is no expectations.")
  page_to_strzok_unix_epoch(child_file, 1489714460000, "Why no response to my first email?")
  strzok_to_page_unix_epoch(child_file, 1489714634989, "Which one?")
  strzok_to_page_unix_epoch(child_file, 1489714954295, "What has you fired up? Her presumption with --Redacted-- about neing left out? Wasn't --Redacted-- aware anyway? --Redacted-- was out, Trisha had the lead and gave to --Redacted--")
  m = page_to_strzok_unix_epoch(child_file, 1489714975000, "Yes. Totally wait for her comment - It's going to be he's mine, it should have come to me, and then you launch into had zero time, nslb had already done it, they shot it to --Redacted-- who of those available, knew the document best.")
  m.addnote("nslb - National Security Law Branch at DOJ")
  strzok_to_page_unix_epoch(child_file, 1489743880617, "Who had the lead in nslb on this?")
  strzok_to_page_unix_epoch(child_file, 1489743923747, "I know --Redacted-- did the work, but the task go to Baker? Trisha?")
  strzok_to_page_unix_epoch(child_file, 1489794238637, "Hey did I hear that the product we wrote two nights ago was sent to Graham and Whitehouse (or anyone else)?")
  page_to_strzok_unix_epoch(child_file, 1489796174000, "It was not sent. Still working out how to communicate the message to them with doj.")
  page_to_strzok_unix_epoch(child_file, 1489796810000, "Is it not the letter that doj sent up responding to the wiretap question?")
  strzok_to_page_unix_epoch(child_file, 1489796908036, "No. He said it described investigations/techniques. And that she had the one name. None of that would be in the doj letter.")
  page_to_strzok_unix_epoch(child_file, 1489796955000, "Your name isn't in the two or in the 4 Para summary. So must be a leak of docs supporting the report.")
  strzok_to_page_unix_epoch(child_file, 1489797032168, "No, sorry, I wasn't clear. The subject whose name starts with my middle --Redacted--")
  strzok_to_page_unix_epoch(child_file, 1489797034175, "--Redacted--")
  m = strzok_to_page_unix_epoch(child_file, 1489797181557, "And makes sense, she has great sources on hpsci, especially minority side Think about her prior reporting.")
  m.addnote("hpsci - House Permanent Select Committee on Intelligence")
  strzok_to_page_unix_epoch(child_file, 1489799041946, "Do you know what was in the set of documents Doj sent to hpsci?")
  page_to_strzok_unix_epoch(child_file, 1489799112000, "What set of documents? I'm not aware of any other than the two, and possibly the letter answering the question.")
  page_to_strzok_unix_epoch(child_file, 1489799328000, "Don't know. Maybe ask rybicki.")
  strzok_to_page_unix_epoch(child_file, 1489799350698, "Rgr thanks.")
  strzok_to_page_unix_epoch(child_file, 1489801036496, "Jim was only aware of Doj sending the two docs we cleared last night...")
  strzok_to_page_unix_epoch(child_file, 1489848169340, "Hey its Pete. Re email, Manafort")
  page_to_strzok_unix_epoch(child_file, 1489851762000, "Oh, that Paul.")
  m = page_to_strzok_unix_epoch(child_file, 1489856622000, "Will certainly do that. Good luck...hopefully a quiet (er) week despite covering as AD. FYSA, I called Laufman re: setting up a DOJ/WFO/FBI HQ meeting re: Wiki soon.")
  m.addnote("fysa - For Your Situational Awareness")
  strzok_to_page_unix_epoch(child_file, 1489871954802, "What do you think of the addition of assessment about whether crimes were committed? Avoids the \"just an Intel case\" canard?")
  page_to_strzok_unix_epoch(child_file, 1489872088000, "Didn't read it that closely.")
  strzok_to_page_unix_epoch(child_file, 1489872203921, "Not a big change - Added sentence saying CI cases can also include assessment if crimes were committed.")
  strzok_to_page_unix_epoch(child_file, 1490269305096, "CNN said \"officials.\" I assume Dems on gang of 8")
  page_to_strzok_unix_epoch(child_file, 1490269351000, "Oh, I don't think it is us at all.")
  strzok_to_page_unix_epoch(child_file, 1490302302133, "And hey, CNN is playing over and over D's statement about what would trigger an investigation. Do we need to adjust and/or message any adjustments?")

  # Page 31
  # 0 - Sent by strzok
  # 1 - Sent by page
  page_to_strzok_unix_epoch(child_file, 1490313582000, "I guess. It sounded like Lisa gave it up the --Redacted-- chain starting with --Redacted-- but I don't think it made it to you. And by the way, --Redacted-- and --Redacted-- did not even appear to think about the fact your branch needed to see it (which shouldn't be surprising). You definitely need to talk with --Redacted-- about her plan for it")
  page_to_strzok_unix_epoch(child_file, 1490317581000, "Did you read this outrage? NYTimes: Trump Tells G.O.P. to Fall in Line, Demanding House Vote on Health Overhaul Trump Tells G.O.P. to Fall in Line, Demanding House Vote on Health Overhaul https://nyti.ms/2mTCbcC")
  page_to_strzok_unix_epoch(child_file, 1490318463000, "God this is depressing too. NYTimes: Calling On a Few Good Men Calling On a Few Good Men https://nyti.ms/2nAdB55")
  strzok_to_page_unix_epoch(child_file, 1490318487734, "A) no, going to read it now B) no, stopped watching after UM kind of blew it against Oregon")
  strzok_to_page_unix_epoch(child_file, 1490318554926, "I saw the last but didn't read it... Wittes and Hennessey have a column arguing for a select committee")
  strzok_to_page_unix_epoch(child_file, 1490318698424, "Also, --Redacted-- said --Redacted-- called, wanting to talk with Bill with ig (I think) about razor....")
  strzok_to_page_unix_epoch(child_file, 1490318797838, "Will try and attend that if I can.")
  page_to_strzok_unix_epoch(child_file, 1490318822000, "Re the leaks? I'd ask him to hold, it's still very much in Flux I think.")
  strzok_to_page_unix_epoch(child_file, 1490318839305, "Yes re leaks")
  page_to_strzok_unix_epoch(child_file, 1490318987000, "They do.")
  page_to_strzok_unix_epoch(child_file, 1490319001000, "I'd talk to baker first.")
  page_to_strzok_unix_epoch(child_file, 1490319013000, "Where's she getting it from, --Redacted--?")
  strzok_to_page_unix_epoch(child_file, 1490319140419, "No idea")
  strzok_to_page_unix_epoch(child_file, 1490319176619, "You really think IG understands who the likelies are? Their line people don't know a lot about leak work.")
  page_to_strzok_unix_epoch(child_file, 1490319278000, "No, probably not.")
  page_to_strzok_unix_epoch(child_file, 1490614878000, "Whoa, did you see the nyt push?")
  m = page_to_strzok_unix_epoch(child_file, 1490614905000, "I have no idea how ssci does that without compromising sources and methods.")
  m.addnote("ssci - Senate Select Committee on Intelligence")
  strzok_to_page_unix_epoch(child_file, 1490627084857, "Ha. You see CNN reporting Nunes on WH grounds the day before his announcement?")
  page_to_strzok_unix_epoch(child_file, 1490627112000, "Yup. Pulling up miller article now.")
  strzok_to_page_unix_epoch(child_file, 1490627150914, "? Same topic? Also, thanks.for the --Redacted-- invite ;)")
  m = page_to_strzok_unix_epoch(child_file, 1490712351000, "Hey you get a ch brief for doj on today? I got hit up by rybucki")
  m.addnote("ch - Crossfire Hurricane")
  strzok_to_page_unix_epoch(child_file, 1490712359631, "Just coming back from entertaining mtg at doj where --Redacted-- and --Redacted-- got testy at each other.")
  m = page_to_strzok_unix_epoch(child_file, 1490712397000, "Re ch?")
  m.addnote("ch - Crossfire Hurricane")
  page_to_strzok_unix_epoch(child_file, 1490712449000, "The team needs to get with doj today for an update. I think they still have to meet with A/DAG tomorrow.")
  strzok_to_page_unix_epoch(child_file, 1490712467648, "We are")
  strzok_to_page_unix_epoch(child_file, 1490830062314, "Hey heads up JR called, D wants a brief on the WH/NFPO/coverage matter. Likely to be after the unmasking briefing.")
  m = page_to_strzok_unix_epoch(child_file, 1491181282000, "You don't get FT, do you? Looks like a leak out of NY. Maybe the plans re --Redacted-- are real... will explain tomorrow. https://www.ft.com/content/40498d94-155b-11e7-80f4-13e067d5072c")
  m.addnote("Financial Times artle entitled FBI plans to create special unit to co-ordinate Russia probe")
  m = strzok_to_page_unix_epoch(child_file, 1491408022695, "CNN reporting Bannon removed from nsc.")
  m.addnote("nsc - National Security Council")
  page_to_strzok_unix_epoch(child_file, 1491408233000, "Okay. I just told jim trisha --Redacted-- and --Redacted-- about --Redacted-- They all agree.")
  
  # Page 32
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1491861185149, "Per New yorker (you need to subscribe again!) McCauley was in mtg with Flynn, Woolsey, Turkish officials....")
  page_to_strzok_unix_epoch(child_file, 1491953827000, "Baker to call tomorrow about something provocative. Don't mention knowing the call to the d this am please.")
  strzok_to_page_unix_epoch(child_file, 1491953875643, "Ok. Calling me?")
  strzok_to_page_unix_epoch(child_file, 1491954062600, "Can you give me any more detail?")
  page_to_strzok_unix_epoch(child_file, 1491954144000, "Not here. No, he'll ask to meet with you. I asked that he talk to you first, not bill.")
  m = page_to_strzok_unix_epoch(child_file, 1491954177000, "Aggressive effort to break the slog that is and will inevitably be getting to the bottom of CH.")
  m.addnote("CH - Crossfire Hurricane")
  strzok_to_page_unix_epoch(child_file, 1491954286007, "Ok. Thanks  You see the WP article? Gas on the \"cloud\" and leak narrative.")
  strzok_to_page_unix_epoch(child_file, 1491954358369, "An idea of his, or something external threatening us?")
  page_to_strzok_unix_epoch(child_file, 1491954634000, "But that is the narrative you can't know about, other than sitting in on morning meeting or known from Bill.")
  page_to_strzok_unix_epoch(child_file, 1491954642000, "Idea of his.")
  strzok_to_page_unix_epoch(child_file, 1491954715831, "He was there when I sat in with D the first time. Then JB specifically called me into his office to talk about it, remember? I won't mention it today....")
  page_to_strzok_unix_epoch(child_file, 1491954807000, "Yes, and I said both to him. Just can't reference today.")
  strzok_to_page_unix_epoch(child_file, 1492009696711, "Also, two new articles coming, one nyt re your namesake and a guardian one which is worse")
  strzok_to_page_unix_epoch(child_file, 1492009734720, "Hope --Redacted-- did you a solid...")
  page_to_strzok_unix_epoch(child_file, 1492177200000, "Which WP scoop? I'm not following.")
  strzok_to_page_unix_epoch(child_file, 1492177256580, "The fisa one, coupled with the guardian piece from yesterday")
  page_to_strzok_unix_epoch(child_file, 1492872810000, "Article is out!")
  strzok_to_page_unix_epoch(child_file, 1492874770128, "What?!?")
  strzok_to_page_unix_epoch(child_file, 1492874775769, "Got no push!")
  strzok_to_page_unix_epoch(child_file, 1492874813287, "Got no email all damn morning")
  m = strzok_to_page_unix_epoch(child_file, 1492878121113, "--Redacted--, it's Pete. Midyear article is out in NYT online. Thanks for the kind words about investigative team to Goldman and Apuzzo.")
  m.addnote( "Apuzzo - Matt Apuzzo reporter for New York Times" )
  m.addnote( "Goldman - Probably Adam Goldman national security reporter for Washington Post then New York Times" )
  m.addnote("Midyear - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1492913677000, "My smart, informed friend --Redacted-- and I have been texting about the article. It's kind of validating to get his take, because he has so much more context now (though he was never a \"it's all Comey's fault guy\") it's very gratifying to get an outsiders perspective. Remind me to show you.")
  strzok_to_page_unix_epoch(child_file, 1492913724371, "Please")
  strzok_to_page_unix_epoch(child_file, 1492913734659, "I made the mistake of reading the comments on the website")
  strzok_to_page_unix_epoch(child_file, 1492913768976, "There are a lot of vocal Clinton supporters who are never going to feel that it was anything other than our fault")
  m = strzok_to_page_unix_epoch(child_file, 1492913792475, "Did you see Goldman tweet?")
  m.addnote( "Goldman - Probably Adam Goldman national security reporter for Washington Post then New York Times" )
  strzok_to_page_unix_epoch(child_file, 1492913824153, "What did you think of the article, by the way? We didn't get a chance to talk about it.")
  page_to_strzok_unix_epoch(child_file, 1492913896000, "I won't read the comments.")
  strzok_to_page_unix_epoch(child_file, 1492913967863, "Good call")
  page_to_strzok_unix_epoch(child_file, 1492913971000, "Yes, you sent it to me. Kaboom. Though I'm not really sure I understood it. I guess because it's like a bomb going off because the \"liberal\" NYT isn't just shoveling out the Clinton proaganda?")
  page_to_strzok_unix_epoch(child_file, 1492914029000, "I wasn't crazy about the paragraphs before the federal bureau of matters. Felt they were too conclusory, too superficial. But I guess the rest of it was fine.")
  page_to_strzok_unix_epoch(child_file, 1492914080000, "You were mentioned a lot. \U0001f636 Wonder what --Redacted-- is going to say. \U0001f616")

  # Page 33
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1492914099587, "I'm not sure I understand the Tweet either. I think his notion that will cause a stir in the overall liberal New York Times readership.")
  page_to_strzok_unix_epoch(child_file, 1492914112000, "Yup. Same same.")
  strzok_to_page_unix_epoch(child_file, 1492914152167, "And funny, I had exactly the same thought about that part of the article, it seems like somebody had to put that in there. I'm not sure the reason why.")
  page_to_strzok_unix_epoch(child_file, 1492914206000, "Of course you did. \U0001f636")
  strzok_to_page_unix_epoch(child_file, 1493153319806, "Is the source available for recontact?")
  page_to_strzok_unix_epoch(child_file, 1493213557000, "Np. Was just calling to say that we're going to hold on opening that one case for a couple of days while Baker talks to doj. Will explain more later, going to tell --Redacted-- now.")
  page_to_strzok_unix_epoch(child_file, 1493473021000, "That's crazy. Sorry to not respond until now. My phone was all jacked up while over in --Redacted-- Got back --Redacted--")
  strzok_to_page_unix_epoch(child_file, 1493758838493, "Hey turn on CNN re Yates")
  strzok_to_page_unix_epoch(child_file, 1494370184035, "CNN had coverage /advance notice of what they claimed was the Trump security guy dropping off firing letter at fbihq earlier this afternoon.")
  strzok_to_page_unix_epoch(child_file, 1494439199582, "Have to talk to Kortan on motherf*cking Peter  Huckabee said D had \"lost confidence of rank and file of fbi\"")
  m = strzok_to_page_unix_epoch(child_file, 1494521792529, "Hey assume you're getting dump. Meeting with DAG was about coordinating investigation.")
  m.addnote("DAG - Deputy Attorney General")
  strzok_to_page_unix_epoch(child_file, 1494526253660, "WH press conference is interesting. Trump told Lester Holt about dinner, all kinds of Qs about those discussions.")
  page_to_strzok_unix_epoch(child_file, 1494553887000, "NYTimes: Andrew McCabe is Known at F.B.I. for His Precision and Intellect Andrew McCabe is Known at F.B.I. for His Precision and Intellect https://nyti.ms/2q7iuTM")
  page_to_strzok_unix_epoch(child_file, 1494759945000, "I feel that same loss. I want to see what the FBI could become under him! His vision of greatness for our strong but flawed organization. I'm angry. Angry and mourning.")
  strzok_to_page_unix_epoch(child_file, 1494760024603, "Yeah I kept telling myself the organization is much bigger and stronger than any one person, that we'll endure.")
  m = strzok_to_page_unix_epoch(child_file, 1494882826250, "And WP push reporting T disclosed highly classified foreign govt info to Russians last week re CT threat...")
  m.addnote( "CT - Counter Terrorism")
  strzok_to_page_unix_epoch(child_file, 1494967456934, "Call me about --Redacted-- please")
  strzok_to_page_unix_epoch(child_file, 1494970037639, "Nyt push")
  m = page_to_strzok_unix_epoch(child_file, 1494973121000, "OI atty is making some minor changes to package, will have to 7 floor as soon as it gets here, paper copy only. On docket for Monday. All greased and ready once signed.")
  m.addnote("OI - FBI Office of Intelligence")
  strzok_to_page_unix_epoch(child_file, 1494973172272, "Rgr thanks")
  strzok_to_page_unix_epoch(child_file, 1494986499030, "My interview partner. Who I need to tell nothing is set and we're not going first thing. Because --Redacted-- doesn't relay sh*t.")
  page_to_strzok_unix_epoch(child_file, 1494986511000, "Yeah, I get it. And Andy could certainly write it but I took notes.")
  page_to_strzok_unix_epoch(child_file, 1494986536000, "So call --Redacted-- tonight and ask. It didn't come up directly. It was very frenetic.")
  strzok_to_page_unix_epoch(child_file, 1494986544710, "I'd rather you write it  We also need class review. Chaffetz has asked for all writeups")
  strzok_to_page_unix_epoch(child_file, 1494986755730, "Actually you need to write it. Andy's a witness, you're not.")
  strzok_to_page_unix_epoch(child_file, 1494987737927, "He's either a dead man walking and/or a hero. Doing so only helps him, doesn't hurt him.")
  strzok_to_page_unix_epoch(child_file, 1494987807426, "History is watching. He needs to. To redeem his soul, first and foremost.")

  # Page 34
  # 0 - Sent by strzok
  # 1 - Sent by page
  strzok_to_page_unix_epoch(child_file, 1495018869686, "Ooh. Lots on npr")
  page_to_strzok_unix_epoch(child_file, 1495019848000, "I want to go thru some of the arguments on lawfare to chronicle. Will call when I get in the car. About 30.")
  page_to_strzok_unix_epoch(child_file, 1495104765000, "I agree. Can you get them out today? And god, EVERYTHING just got so much better on that case...")
  page_to_strzok_unix_epoch(child_file, 1495106587000, "I get it, but they're not being unreasonable. And yes, we will bring him here. It's easy to monday morning quarterback Pete. You tell me that in the face of two seemingly earnest senators, you'd adamantly hold your absolutely no, no way.")
  strzok_to_page_unix_epoch(child_file, 1495150875122, "Oh god Susan Collins comments on npr....")
  m = strzok_to_page_unix_epoch(child_file, 1495154172161, "For me, and this case, I personally have a sense of unfinished business. I unleashed it with MYE. Now i need to fix it and finish it")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  page_to_strzok_unix_epoch(child_file, 1495154242000, "What does that even mean, scaling up?")
  page_to_strzok_unix_epoch(child_file, 1495154270000, "You shouldn't take this on. I promise you, I would tell you if you should.")
  strzok_to_page_unix_epoch(child_file, 1495154384213, "Why not, re me?")
  strzok_to_page_unix_epoch(child_file, 1495154446794, "Who gives a f*ck, one more AD like Scott or Steve or Carlos or Dave or Tim or whoever. An investigation leading to impeachment?")
  page_to_strzok_unix_epoch(child_file, 1495237300000, "Will explain why later. He thinks this isn't really a CI case, should be approached from a PC perspective.")
  strzok_to_page_unix_epoch(child_file, 1495392318722, "Yep let's see. I can envision the end state following the meeting, but let things run their course. One thing I (we) know is Bill will not buck Carl.")
  page_to_strzok_unix_epoch(child_file, 1495584574000, "They are working very very long hours already. And every weekend. Not --Redacted--, of course, but everyone else.")
  strzok_to_page_unix_epoch(child_file, 1495584639360, "Sigh. That's what I was afraid of. Are you locked in with Baker if something happens to Andy?")
  page_to_strzok_unix_epoch(child_file, 1495585111000, "So long as baker stays, yes.")
  strzok_to_page_unix_epoch(child_file, 1496100022580, "NYTimes: A Constitutional Puzzle: Can the President Be Indicted? A Constitutional Puzzle: Can the President Be Indicted? https://nyti.ms/2scC27a")
  strzok_to_page_unix_epoch(child_file, 1496362301355, "Ha. --Redacted-- just called (but had to answer another call), said he had talked to you on one of the issues...not sure what but will call back.")
  m = page_to_strzok_unix_epoch(child_file, 1496362580000, "Re the mtg tomorrow. Not clear now which subj (which is his Question I am guessing) but either way usao wants to attend which is an issue.")
  m.addnote("usao - United States Attorney's Office")
  m = page_to_strzok_unix_epoch(child_file, 1496362606000, "Ie, --Redacted-- vs. Razor")
  m.addnote("Razor - Crossfire Razor - Micheal Flynn")
  strzok_to_page_unix_epoch(child_file, 1496362655045, "Hmm. I heard --Redacted-- What did you hear?")
  # Page 468 has unredacted version of this message
  #strzok_to_page_unix_epoch(child_file, 1496362669166, "And from who? Mine came from --Redacted--")
  page_to_strzok_unix_epoch(child_file, 1496362692000, "Wait I forget the codename.")
  page_to_strzok_unix_epoch(child_file, 1496362707000, "Oh yes. --Redacted--")
  page_to_strzok_unix_epoch(child_file, 1496362719000, "He thought maybe someone else")
  strzok_to_page_unix_epoch(child_file, 1496362844482, "Who's saying USAO wants to attend?")
  # Page 468 said "Tash" is first redaction
  page_to_strzok_unix_epoch(child_file, 1496362887000, "Tash said --Redacted-- called her said dbi crim invited them.")
  page_to_strzok_unix_epoch(child_file, 1496449424000, "It's just hard to be untethered to the Bureau and Andy right now. It's been bad enough without Comey, just feels like another loss.")
  m = strzok_to_page_unix_epoch(child_file, 1496531222219, "Subj in custody, btw. First ML arrest of the Trump era")
  m.addnote("ML - Major League")
  page_to_strzok_unix_epoch(child_file, 1496539527000, "just based on Mueller's convo with him - he just didn't understand what the problem was. AND I did a lot of work to help them understand that --Redacted-- was al")
  # strzok_to_page_unix_epoch(child_file, 1496540995457, "And sigh. Ok. Don't worry too much about Mueller and --Redacted-- You're going to be ok. :)")

  # Page 35
  # 0 - Sent by strzok
  # 1 - Sent by page
  page_to_strzok_unix_epoch(child_file, 1496689239000, "Let me talk to SC about the memos. I just spoke to Rybicki about them and where things stand.")
  strzok_to_page_unix_epoch(child_file, 1496689297578, "I just talked to Aaron. He said memos are still not decided, in other words, they're not going to block testimony, but the memos are still up in the air")
  strzok_to_page_unix_epoch(child_file, 1496789251090, "I think Papa and --Redacted-- and Stone and Wiki and CI confluence is smack square in your wheelhouse.")
  page_to_strzok_unix_epoch(child_file, 1496832264000, "And jesus, did you see that the networks are carrying Comey's testimony? Interrupting regular tv to broadcast...")
  strzok_to_page_unix_epoch(child_file, 1496832924340, "And I've gotta say I'm a little bummed about Dir C testimony. Is what it is.")
  page_to_strzok_unix_epoch(child_file, 1496832983000, "Yup, it's fine.")
  # Appendix C Page 485 has first redaction as "Aaron"
  strzok_to_page_unix_epoch(child_file, 1496856670939, "Aaron would like you and --Redacted-- to explore supplementing Andy's testimony along the lines we discussed on that one answer")
  page_to_strzok_unix_epoch(child_file, 1496937950000, "Good for Comey.")
  page_to_strzok_unix_epoch(child_file, 1496938906000, "Bad for Loretta Lynch.")
  page_to_strzok_unix_epoch(child_file, 1496938914000, "Bad for Sessions.")
  page_to_strzok_unix_epoch(child_file, 1496938955000, "Mixed for Trump.")
  page_to_strzok_unix_epoch(child_file, 1496973411000, "Great. --Redacted-- just called me to say that Rachel Maddow just listed by name each of the people the Director listed as having discussed the matter with, but she that I was the only one identified yet but that they were working on it. \U0001f612")
  strzok_to_page_unix_epoch(child_file, 1496973731850, "And we do need to discuss your role in obstruction aspect in light of being a witness. Not sure if I'm overthinking that.")
  page_to_strzok_unix_epoch(child_file, 1496973887000, "I don't think I know a lot of enemies/crazies. Well, there is one.")
  #page_to_strzok_unix_epoch(child_file, 1497109998000, "Finally, I don't like not including that one person. He is NOT recused, Bill should not be making that call for him. He can make that decision himself. --Redacted--")
  #page_to_strzok_unix_epoch(child_file, 1497109999000, "--Redacted-- always takes a conservative approach and can be trusted to do the right thing.")
  strzok_to_page_unix_epoch(child_file, 1497353038055, "Damn. --Redacted-- had a funny relationship with me. There's a big CNN graphic on the SC teams political donations...")
  page_to_strzok_unix_epoch(child_file, 1497487439000, "Thanks. Saw your politico article too. God help me I don't think I can take much more of this.")
  page_to_strzok_unix_epoch(child_file, 1497526529000, "Or because of the nyt story saying that SC seems to be pursuing potus in light of these interviews.")
  strzok_to_page_unix_epoch(child_file, 1497556004836, "WP picked your name up in an online blog, citing Wired. \"Right Turn,\" 9:15 today")
  strzok_to_page_unix_epoch(child_file, 1497556092815, "And you're on Wiki https://en.m.wikipedia.org/wiki/2017_Special_Counsel_for_the_United_States_Department_of_Justice_team")
  strzok_to_page_unix_epoch(child_file, 1497610054354, "I don't know how you correct it - realistically you probably dont. And it would probably be a good thing to get some long time Russian OC folks on board.")
  strzok_to_page_unix_epoch(child_file, 1497610143816, "You saw you're in the print nyt, right?")
  strzok_to_page_unix_epoch(child_file, 1497610168004, "I was talking prosecutors, but maybe. He's ny. Can he be trusted?")
  page_to_strzok_unix_epoch(child_file, 1497805918000, "I must have really freaked him out on Friday when I told him I wanted to join the Russian influence team.")
  strzok_to_page_unix_epoch(child_file, 1497807377691, "Wonder what changed. I worry it's the FOIA yuck, with a realization there will be a hundred things like that he doesn't want.")
  page_to_strzok_unix_epoch(child_file, 1497927847000, "Make sure you don't tell her anything about whether the press accounts are accurate. Nothing. Just say you don't know what I did at doj.")

  # Page 36
  # 0 - Sent by strzok
  # 1 - Sent by page
  page_to_strzok_unix_epoch(child_file, 1497970125000, "If I am going to call, I think it makes sense to do while you are still there. Thoughts? Also, I will do it on a SC phone, just so no number comes up. --Redacted--")
  strzok_to_page_unix_epoch(child_file, 1497983692441, "That, Lisa, is entirely 100% your business. You don't need me to tell you that - I'm saying that so you know I understand.")
  strzok_to_page_unix_epoch(child_file, 1497987778456, "Shockingly, --Redacted-- is pushing me to go to OSC. How do you feel about that? How would --Redacted--")
  page_to_strzok_unix_epoch(child_file, 1497987985000, "I don't prefer that, but I really really just want this all to be over so I don't care.")
  page_to_strzok_unix_epoch(child_file, 1497988012000, "I'm sure --Redacted-- wouldn't be thrilled, but I presume we'll manage.")
  page_to_strzok_unix_epoch(child_file, 1498005328000, "Just say, I'm not really needed on SC, I am needed at HQ.")
  page_to_strzok_unix_epoch(child_file, 1498135693000, "I'm thinking I might leave SC. Maybe hold to say something.")
  # Completed
  return None

def add_strzok_page_messages_appendix_c(parent_file: truxton.TruxtonChildFileIO) -> None:
  child_file = add_file(parent_file, SUPPORT_DOCUMENTS_FOLDER + "Appendix C - Documents.pdf")
  child_file.tag("Text Messages", "The main Strzok<->Page Messages", truxton.TAG_ORIGIN_HUMAN)

  # Page 29
  page_to_strzok(child_file, "2015-08-16T20:52:54-00:00", "Love this line in the article: 'the fbi and dhs are in charge of tracking the activities of foreign govt agents inside the US...' Uh, in what universe is that dhs's job?")
  page_to_strzok(child_file, "2015-08-16T20:53:26-00:00", "You are wildly wrong.")
  strzok_to_page(child_file, "2015-08-16T20:54:36-00:00", "Well I'm sure Jeh Johnson said it is...gotta assume it's some wildly liberal interpretation of immigration responsibilities.")
  page_to_strzok(child_file, "2015-08-16T21:31:37-00:00", "Finally, and related to nothing, but I just saw my first Bernie Sanders bumper sticker. Made me want to key the car.")
  strzok_to_page(child_file, "2015-08-16T21:37:53-00:00", "He's an idiot like Trump. Figure they cancel each other out.")
  page_to_strzok(child_file, "2015-08-30T18:18:49-00:00", "Not related, but this is also outrageous. I mean, come on. The woman needed all this outside employment? An article to share: How Huma Abedin operated at the center of the Clinton universe")
  strzok_to_page(child_file, "2015-10-14T01:11:52-00:00", "And Martin OMalley's a douche.")
  page_to_strzok(child_file, "2015-10-14T01:14:29-00:00", "I'm not watching. I can't tell you how little I care right now.")
  strzok_to_page(child_file, "2015-10-14T01:17:12-00:00", "Kind of a foregone conclusion but so much more substabtive than the Rep debates.")
  strzok_to_page(child_file, "2015-10-14T02:22:05-00:00", "Ooh hillary Bernie throw down on 215.")
  page_to_strzok(child_file, "2015-11-01T23:19:31-00:00", "Hey, I assume going forward that it's okay to send entirely innocuous news articles, right?")

  # Page 30
  page_to_strzok(child_file, "2015-11-01T23:21:36-00:00", "Anyway, I sent one. And I hope Paul Ryan fails and crashes in a blaze of glory.")
  strzok_to_page(child_file, "2015-11-01T23:23:04-00:00", "Yes. And, me too. At some point the Rep party needs to pull their head out of their *ss. Shows no sign of occurring any time soon.")
  page_to_strzok(child_file, "2015-12-13T01:36:54-00:00", "And funny re --Redacted-- husband, bc Kasich has long been suspected of being gay. Lived with his campaign manager for a looooong time, until maybe 10+ years ago when he married a supermodel wife and immediately popped out kids, twins even, I think.")
  page_to_strzok(child_file, "2015-12-21T01:19:26-00:00", "What an utter idiot. An article to share: Donald Trump on Putin 'Nobody has proven that he's killed anyone'")
  strzok_to_page(child_file, "2015-12-21T01:47:08-00:00", "No doubt. \U0001f612 Ok to gmail some pics?")
  page_to_strzok(child_file, "2015-12-28T18:26:22-00:00", "It's sick, but I really like policy issues. And having tight deadlines. Sigh...")

  # Page 31
  strzok_to_page(child_file, "2015-12-28T19:18:11-00:00", "Is that what doj wanted?")
  strzok_to_page(child_file, "2015-12-28T19:18:32-00:00", "You get all your oconus lures approved?")
  page_to_strzok(child_file, "2015-12-28T19:19:41-00:00", "No, it's just implicated a much bigger policy issue. I'll explain later. Might even be able to use it as a pretext to call... :)")
  strzok_to_page(child_file, "2016-01-18T03:13:35-00:00", "Martin O'Malley's a freakshow")
  page_to_strzok(child_file, "2016-01-18T03:14:59-00:00", "Yikes baby! Yeah, that's what everyone says. Okay, really going to bed now --Redacted--")

  # Page 32
  page_to_strzok(child_file, "2016-01-22T17:50:34-00:00", "Yeah, some extremely offensive video screens set up in front of dist ct. Thank goodness D can't read and wasn't paying attention. Blood and guts and gore. I truly hate these people. No support for the woman who actually has to spend the rest fo her life rearing this child, but we care about 'life.' Assholes.")
  strzok_to_page(child_file, "2016-01-26T00:16:54-00:00", "And J*sus Martin O'Malley, just pack it in and go home!")
  strzok_to_page(child_file, "2016-02-19T02:17:26-00:00", "NOW HOW THE F CAN HE BE A REPUBLICAN? !?!?")
  page_to_strzok(child_file, "2016-01-22T17:50:34-00:00", "I have absolutely no idea. Still, he is so very interesting.")

  # Page 33
  strzok_to_page(child_file, "2016-02-19T02:17:26-00:00", "Gotta get that promotion party so you can meet him.")
  strzok_to_page(child_file, "2016-02-19T02:20:55-00:00", "And find the right moment to introduce you to N about the Apple pclob Lisa buckets stuff...")
  strzok_to_page(child_file, "2016-03-02T01:19:48-00:00", "He IS proud. And therefore me, too. \U0001f636\U0001f636\U0001f636\U0001f636\U0001f636\U0001f636\nVoted for Bernie, of course. As young idealistic kids should.")
  strzok_to_page(child_file, "2016-03-02T01:20:01-00:00", "He asked me who I'd vote for, guessed Kasich")

  # Page 34
  page_to_strzok(child_file, "2016-03-02T01:20:11-00:00", "Yes, they should.")
  page_to_strzok(child_file, "2016-03-02T01:20:29-00:00", "Seriously?! Would you not D?")
  strzok_to_page(child_file, "2016-03-02T01:20:39-00:00", "I don't know. I suppose Hillary.")
  strzok_to_page(child_file, "2016-03-02T01:20:46-00:00", "I would D")

  # Page 35
  page_to_strzok(child_file, "2016-03-02T01:21:00-00:00", "He doesn't think you're an R, does he?")
  strzok_to_page(child_file, "2016-03-02T01:21:04-00:00", "VA's going to go her way anyway.")
  strzok_to_page(child_file, "2016-03-02T01:21:17-00:00", "He thinks I wouldn't vote for her right now.")
  strzok_to_page(child_file, "2016-03-02T01:21:34-00:00", "He knows I'm a conservative Dem.")

  # Page 36
  strzok_to_page(child_file, "2016-03-02T01:21:37-00:00", "But now I wonder.")
  page_to_strzok(child_file, "2016-03-02T01:21:45-00:00", "Got it.")
  #page_to_strzok(child_file, "2016-03-04T02:10:50-00:00", "God trump is a loathsome human.")
  strzok_to_page(child_file, "2016-03-04T02:11:26-00:00", "Yet he may win.")

  # Page 37
  strzok_to_page(child_file, "2016-03-04T02:11:35-00:00", "Good for Hillary.")
  page_to_strzok(child_file, "2016-03-04T02:11:51-00:00", "It is.")
  # Following are repeated in Lync-messages
  # strzok_to_page(child_file, "2016-03-04T02:12:44-00:00", "Would he be a worse president than cruz?")
  # page_to_strzok(child_file, "2016-03-04T02:13:14-00:00", "Trump? Yes, I think so.")

  # Page 38
  strzok_to_page(child_file, "2016-03-04T02:13:37-00:00", "I'm not sure.")
  strzok_to_page(child_file, "2016-03-04T02:20:34-00:00", "Omg he's an idiot.")
  page_to_strzok(child_file, "2016-03-04T02:20:33-00:00", "He's awful.")
  strzok_to_page(child_file, "2016-03-04T02:21:02-00:00", "America will get what the voting public deserves")

  # Page 39
  page_to_strzok(child_file, "2016-03-04T02:21:36-00:00", "That's what I'm afraid of.")
  strzok_to_page(child_file, "2016-03-04T02:22:11-00:00", "Department of Environmental Protection? !?!")
  page_to_strzok(child_file, "2016-03-04T02:22:33-00:00", "Yup.")
  strzok_to_page(child_file, "2016-03-04T02:24:25-00:00", "God Hillary should win 100,000,000 - 0.")

  # Page 40
  page_to_strzok(child_file, "2016-03-04T02:25:16-00:00", "I know.")
  m = page_to_strzok(child_file, "2016-03-04T02:34:56-00:00", "Also did you hear him make a comment about the size of his d*ck earlier? This man can not be president.")
  m.tag("Hatred", "cannot be president is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  strzok_to_page(child_file, "2016-03-04T02:37:06-00:00", "Yes I did. In relation to the size of his hands. And all the 'Little Mario' blah blag blah")
  strzok_to_page(child_file, "2016-03-04T02:38:08-00:00", "And God, Detroit used to be SO beautiful and shining and elegant. \U0001f61e Sigh.")

  # Page 41
  page_to_strzok(child_file, "2016-03-04T02:38:35-00:00", "I know. Detroit is really a beautiful city. Camden was too.")
  strzok_to_page(child_file, "2016-03-04T02:56:09-00:00", "Ok I may vote for Trump ;)")
  strzok_to_page(child_file, "2016-03-04T02:57:00-00:00", "'And look, I'M OLD'")
  page_to_strzok(child_file, "2016-03-04T02:58:39-00:00", "What?! Poor Kasich. He's the only sensible man up there.")

  # Page 42
  strzok_to_page(child_file, "2016-03-04T02:59:53-00:00", "He was pretty much calling for death for Snowden. I'm a single issue voter. ;) Espionage Machine Party")
  strzok_to_page(child_file, "2016-03-04T03:00:23-00:00", "Exactly re Kasich. And he has ZERO appeal")
  page_to_strzok(child_file, "2016-03-12T20:58:35-00:00", "What the f is wrong with people? A Texas Candidate Pushes the Boundary of the Far Right http://nyti.ms/1QTgBgj")
  strzok_to_page(child_file, "2016-03-12T21:05:11-00:00", "That Texas article is depressing as hell. But answers how we could end up with President Trump")

  # Page 43
  page_to_strzok(child_file, "2016-03-12T21:07:50-00:00", "Wasnt't it? Seriously, how are people so incredibly ignorant?")
  strzok_to_page(child_file, "2016-03-12T21:12:46-00:00", "I have no idea, but it depresses me. Same people who drive more when they get extra daylight from daylight savings, I'm guessing.")
  #strzok_to_page(child_file, "2016-03-12T21:21:03-00:00", "\U0001f621\nTrump Clarifies, and it's Worse - NYTimes.com http://mobile.nytimes.com/2016/03/12/opinion/trump-clarifies-and-its-worse.html?_r=0")
  page_to_strzok(child_file, "2016-03-14T11:53:08-00:00", "Don't listen to npr this morning - Richard Clarke is an uninformed douche. \U0001f621\U0001f621\U0001f621")

  # Page 44
  strzok_to_page(child_file, "2016-03-14T11:53:43-00:00", "Yeah, I really don't like him. What did he say?")
  page_to_strzok(child_file, "2016-03-14T11:54:39-00:00", "Totally unnecessary. He's aweful.")
  strzok_to_page(child_file, "2016-03-14T11:58:38-00:00", "You can tell me about --Redacted-- and we can get indignant together.")
  page_to_strzok(child_file, "2016-03-14T12:11:09-00:00", "It is not boring or weak. It is life, and I am happy to help. He is a blowhard who doesn't know what he is talking about anymore, if he ever did. I will when I can. Not sure what his schedule is like this am.")

  # Page 45
  page_to_strzok(child_file, "2016-03-16T04:11:51-00:00", "I can not believe Donald Trump is likely to be an actual, serious candidate for president.")
  page_to_strzok(child_file, "2016-04-02T01:19:29-00:00", "So look, you say we text on that phone when we talk about hillary because it can't be traced, you were just venting bc you feel bad that you're gone so much but it can't be helped right now.")
  strzok_to_page(child_file, "2016-04-02T01:20:30-00:00", "Right. But did you say anything other than work? I did, but may have only gotten smiles or blushes back.")
  strzok_to_page(child_file, "2016-04-09T01:18:28-00:00", "All this from N:\www.greenpeace.org/usa/campaign-updates/hillary-clintons-connections-oil-gas-industry Everything sanders said about Clinton is true. If you ready through their fact check they don't state a single thing of his is 'false', however they argue that it is completely false because 1.4 million from fossil fuel lobbyists and 3.3 million directly from large donors connected to the fossil fuel industry, a total of 4.5 million alone in 2016 as 'not much' compared to her total raising a")

  # Page 46
  strzok_to_page(child_file, "2016-04-09T01:18:35-00:00", "This is clear and utter bias by the media specifically the NYTIMES, WAPO, and CNN who if you look at all of them have large donors for Clinton")
  strzok_to_page(child_file, "2016-04-09T01:18:45-00:00", "The fact citing source they used is owned by a newspaper which publicly endorsed Clinton")
  page_to_strzok(child_file, "2016-05-04T00:40:51-00:00", "And holy shit Cruz just dropped out of the race. It's going to be a Clinton Trump race. Unbelievable.")
  strzok_to_page(child_file, "2016-05-04T00:41:24-00:00", "What?!?!??")

  # Page 47
  #page_to_strzok(child_file, "2016-05-04T00:41:37-00:00", "You heard that right my friend.")
  strzok_to_page(child_file, "2016-05-04T00:41:37-00:00", "I saw trump won, figured it would be a bit")
  strzok_to_page(child_file, "2016-06-12T01:49:47-00:00", "They fully deserve to go, and demonstrate the absolute bigoted nonsense of Trump")
  strzok_to_page(child_file, "2016-06-12T01:49:47-00:00", "Truly")

  # Page 48
  #strzok_to_page(child_file, "2016-06-17T21:56:15-00:00", "Now we're talking about Clinton, and how a lot of people are holding their breath, hoping.")
  page_to_strzok(child_file, "2016-06-22T16:39:25-00:00", "Hi. Just leaving my meeting now. How we make law in this country is offensive and irresponsible. \U0001f621")
  strzok_to_page(child_file, "2016-06-22T16:41:56-00:00", "I know it is. Its whey I LOATHE congress. Can't wait to hear the story.")
  page_to_strzok(child_file, "2016-07-07T10:36:34-00:00", "Thought this was spot on. Hillary Clinton: Ma'am Survivor http:://nyti.ms/29zO0ku")

  # Page 49
  strzok_to_page(child_file, "2016-07-08T22:45:38-00:00", "And meanwhile, we have Black Lives Matter protesters, right now, chanting 'no justice no peace' around DOJ and the White House...")
  page_to_strzok(child_file, "2016-07-08T23:15:13-00:00", "That's awful")
  strzok_to_page(child_file, "2016-07-10T01:22:24-00:00", "I didn't get the chance to ask about the 88s. But I did sit and stare at the portrait of Elliot Richardson staring at me.")
  strzok_to_page(child_file, "2016-07-10T01:22:44-00:00", "It's next to the portrait of Eric Holder, which is wildly offensive.")

  # Page 50
  page_to_strzok(child_file, "2016-07-14T01:33:53-00:00", "Have you read this? It's really frightening. For Whites Sensing Decline, Donald Trump Unleashes Words of Resistance http://nyti.ms/29WCu51")
  strzok_to_page(child_file, "2016-07-14T01:35:35-00:00", "I have not. But I think it's clear he's capturing all the white, poor voters who the mainstream Republicans abandoned in all but name in the quest for the almighty $$$$")
  page_to_strzok(child_file, "2016-07-14T01:36:32-00:00", "Yeah, it's not good. Anyway, --Redacted--")
  #strzok_to_page(child_file, "2016-07-14T11:04:45-00:00", "Poll Finds Emails Weighing on Hillary Clinton, Now Tied With Donald Trump http://nyti.ms/29RVSgf")

  # Page 51
  page_to_strzok(child_file, "2016-07-14T11:05:15-00:00", "it is.")
  strzok_to_page(child_file, "2016-07-19T00:12:19-00:00", "And are you kidding me? Duck Dynasty now Scott Baio? Ridiculous.")
  page_to_strzok(child_file, "2016-07-19T00:27:05-00:00", "Wait, is that who is speaking at the convention?")
  strzok_to_page(child_file, "2016-07-19T00:27:24-00:00", "Yes!!!!!!")

  # Page 52
  page_to_strzok(child_file, "2016-07-19T00:27:27-00:00", "Charles in Charge?! That's the best they can do?! Lmfao")
  strzok_to_page(child_file, "2016-07-19T00:27:37-00:00", "It's PATHETIC!")
  page_to_strzok(child_file, "2016-07-19T00:27:59-00:00", "That unbelievable. My god. Thank god it's not on.")
  strzok_to_page(child_file, "2016-07-19T00:28:44-00:00", "It's on! PBS!")

  # Page 53, INBOX is Strozk->Page
  strzok_to_page(child_file, "2016-07-19T00:29:56-00:00", "What did you do? Republican snark, \U0001f636")
  strzok_to_page(child_file, "2016-07-19T00:36:18-00:00", "AND COME ON!!!! TURN ON THE CONVENTION!!!!")
  page_to_strzok(child_file, "2016-07-19T00:37:52-00:00", "NO!! I WILL NOT BE SUCKED IN!")
  strzok_to_page(child_file, "2016-07-19T00:43:55-00:00", "TURN IT ON. PBS. --Redacted--")

  # Page 54, INBOX is Strozk->Page
  page_to_strzok(child_file, "2016-07-19T00:44:39-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-19T00:45:03-00:00", "Well Christ. YOU got me there. :D")
  page_to_strzok(child_file, "2016-07-19T00:45:25-00:00", "--Redacted-- likely to come down soon shortly so we can bust through more of this sh*t. Just fyi.") # Probably first letter of husband's name
  strzok_to_page(child_file, "2016-07-19T00:57:55-00:00", "Oooh, TURN IT ON, TURN IT ON!!! THE DOUCHEBAGS ARE ABOUT TO COME OUT.\n\nYou can tell by the excitable clapping.")

  # Page 55, INBOX is Strozk->Page
  page_to_strzok(child_file, "2016-07-19T01:04:46-00:00", "My god, I'm so embarrassed for them. These are like second-run stars. Nothing the B-list to relate to the kids these days...")
  #page_to_strzok(child_file, "2016-07-19T02:23:29-00:00", "And wow, Donald Trump is an enormous d*uche.")
  strzok_to_page(child_file, "2016-07-19T10:16:23-00:00", "Hi. How was Trump, other than a douche? Melania? And any luck with home purchases?\n\nI have --Redacted-- this morning. \U0001f61d")
  #page_to_strzok(child_file, "2016-07-19T10:18:31-00:00", "Trump barely spoke, but the first thing out of his mouth was \"we're going to win soooo big.\" The whole thing is like living in a bad dream.")

  # Page 56, INBOX is Strozk->Page
  strzok_to_page(child_file, "2016-07-19T10:19:41-00:00", "Jesus")
  page_to_strzok(child_file, "2016-07-19T10:20:06-00:00", "Melania was perfectly fine, except the whole point of the spouse talking is to reveal those personal stories, what a kind human the candidate is. There was none of that.")
  strzok_to_page(child_file, "2016-07-19T10:21:20-00:00", "That was her job! What the hell did she talk about? Winning yuuuge?")
  page_to_strzok(child_file, "2016-07-19T10:22:12-00:00", "I don't know. Lots of my husband is great, but no description to back it up.")

  # Page 57, INBOX is Strozk->Page
  #strzok_to_page(child_file, "2016-07-19T11:18:46-00:00", "Omg. You listening to npr? Apparently Melania's speech had passages lifted from Michele Obama's....unbelievable")
  #page_to_strzok(child_file, "2016-07-19T11:19:25-00:00", "NO WAY!")
  page_to_strzok(child_file, "2016-07-19T11:20:06-00:00", "God, it's just a two-bit organization. I do so hope his disorganization comes to bite him hard in November.")
  strzok_to_page(child_file, "2016-07-19T11:21:13-00:00", "It HAS to, right? Panicked \U0001f628")

  # Page 58, INBOX is Strozk->Page
  strzok_to_page(child_file, "2016-07-20T00:14:02-00:00", "Hopefully you get home in time for crazy - ass grain storage pyramid Ben Carson tonight.")
  strzok_to_page(child_file, "2016-07-20T00:14:10-00:00", "Pence being introduced")
  page_to_strzok(child_file, "2016-07-20T01:12:03-00:00", "Mitch McConnell always reminds me of a turtle.")
  page_to_strzok(child_file, "2016-07-20T01:14:54-00:00", "My god, the crowd looks soooooooo bored.")

  # Page 59, INBOX is Strozk->Page
  strzok_to_page(child_file, "2016-07-20T01:15:04-00:00", "Droopy dog")
  strzok_to_page(child_file, "2016-07-20T01:22:23-00:00", "Amd Paul Ryan's a jerky")
  page_to_strzok(child_file, "2016-07-21T08:52:19-00:00", "This is really shocking.\n\nDonald Trump Sets Conditions for Defending NATO Allies Against Attack http://nyti.ms/2ai4u3g")
  page_to_strzok(child_file, "2016-07-21T09:09:58-00:00", "This campaign is like watching a train wreck happen over and over again.\n\nHow Donald Trump Picked His Running Mate http://nyti.ms/2a8aCJ9")

  # BIG GAP
  # Page 60, INBOX is Strozk->Page
  #strzok_to_page(child_file, "2016-07-26T23:54:42-00:00", "And hey. Congrats on a woman nominated for President in a major party\n\nAbout damn time! Many many more returns of the day! \U0001f60a")
  #page_to_strzok(child_file, "2016-07-26T23:55:57-00:00", "\U0001f60a That's cute. Thanks \U0001f636")
  #page_to_strzok(child_file, "2016-07-26T23:57:51-00:00", "\U0001f60a That's cute. Thanks \U0001f636")
  strzok_to_page(child_file, "2016-07-26T23:58:20-00:00", "I had to hold --Redacted-- hand when Bernie just now moved for her nomination.\U0001f636\U0001f636\U0001f636")

  # Page 61, INBOX is Strozk->Page
  page_to_strzok(child_file, "2016-07-26T23:58:48-00:00", "I'm not watching. What happened?")
  strzok_to_page(child_file, "2016-07-27T00:02:08-00:00", "They went thru roll call, she got enough votes about an hour ago. Vermont went last, they cast their votes. Then introduced Bernie, who called for some procedural things then moved for HRC to become the Democratic Nominee.")
  strzok_to_page(child_file, "2016-07-27T00:02:41-00:00", "Chills, just because I'm a homer for American democracy that way. \U0001f636\U0001f636\U0001f636\U0001f636")
  #strzok_to_page(child_file, "2016-07-27T00:03:06-00:00", "If they played patriotic music or did something with the flag and an honor guard, I probably would have teared up.....")

  # Page 62, INBOX is Strozk->Page
  strzok_to_page(child_file, "2016-07-27T00:05:18-00:00", "Turn on pbs!")
  strzok_to_page(child_file, "2016-07-27T00:07:14-00:00", "Oh God, Holder! Turn it off turn it off turn it off!!!!")
  #page_to_strzok(child_file, "2016-07-27T00:11:47-00:00", "Yeah, I saw him yesterday and booed at the tv. \U0001f60a")
  page_to_strzok(child_file, "2016-07-27T00:11:56-00:00", "Sigh. Thank you. \U0001f636")

  # Page 63, INBOX is Strozk->Page
  page_to_strzok(child_file, "2016-07-27T00:21:39-00:00", "Yeah, it is pretty cool. She just has to win now. I'm not going to lie, I got a flash of nervousness yesterday about trump. The sandernistas have the potential to make a very big mistake here...")
  #strzok_to_page(child_file, "2016-07-27T00:32:09-00:00", "I'm not worried about them. I'm worried about the anarchist Assanges who will take fed information and disclose it to disrupt. --Redacted--")
  #strzok_to_page(child_file, "2016-07-27T02:54:17-00:00", "So sad, the comment about more yesterdays than tomorrows. \U0001f622\n\nAnd I don't like Chelsea! Her husband even less...\U0001f612 ")
  page_to_strzok(child_file, "2016-07-27T02:57:07-00:00", "I like Chelsea fine. Why not?")

  # Page 64, INBOX is Strozk->Page
  #strzok_to_page(child_file, "2016-07-27T03:00:18-00:00", "Self entitled. Deels she deserves something she hasn't earned")
  #page_to_strzok(child_file, "2016-07-28T00:59:03-00:00", "Stupid *ss Bernie supporters shouting no more war so that he couldn't be heard hardly at all. I'm sorry, they're idiots.")
  strzok_to_page(child_file, "2016-07-28T01:01:27-00:00", "They really are.")
  page_to_strzok(child_file, "2016-07-28T01:18:01-00:00", "I really really like Joe Biden.")

  # Page 65, INBOX is Strozk->Page
  strzok_to_page(child_file, "2016-07-28T01:24:09-00:00", "Was literally grabbing phone to say Joe's doing great!")
  page_to_strzok(child_file, "2016-07-28T01:26:14-00:00", "He's just a really sincere guy.")
  #strzok_to_page(child_file, "2016-07-28T01:29:15-00:00", "--Redacted-- said he was absolutely beloved by Deleware State Police. And funny story about him and gtwn basketball team in China a few years ago. Too long for here.")
  #strzok_to_page(child_file, "2016-07-28T01:51:10-00:00", "Opened on Trump? If Hillary did, you know 5 field offices would...")

  # Page 66, INBOX is Strozk->Page
  #strzok_to_page(child_file, "2016-07-28T01:54:20-00:00", "This article highlights the thing I mentioned to you earlier, asking if Bill had noted it to 7th floor. I'm going to send it to him")
  #page_to_strzok(child_file, "2016-08-01T01:38:23-00:00", "I mean seriously, What in the hell is this guy talking about?\n\nDonald Trump Gives Questionable Explanation of Events in Ukraine http://nyti.ms/2arMCyV")
  #page_to_strzok(child_file, "2016-08-06T14:38:09-00:00", "Jesus. You should read this. And Trump should go f himself.\n\nMoment in Convention Glare Shakes Up Khans\u2019American Life http://nyti.ms/2aHuLE0")
  m = strzok_to_page(child_file, "2016-08-06T14:53:36-00:00", "God that's a great article.\U0001f621\U0001f61e\U0001f61e\u2764\n\nThanks for sharing.\n\nAnd F Trump.")
  m.tag("Hatred", "f Trump is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)

  # Page 67, INBOX is Strozk->Page
  #page_to_strzok(child_file, "2016-08-06T14:55:00-00:00", "And maybe you're meant to stay where you are because you're meant to protect the country from that menace. To that end read this:")
  page_to_strzok(child_file, "2016-08-06T14:55:19-00:00", "Trump\u2019s Enablers Will Finally Have to Take a Stand http://nyti.ms/2aFakry")
  strzok_to_page(child_file, "2016-08-06T15:04:43-00:00", "Thanks. It's absolutely true that we're both very fortunate.\n\nAnd of course I'll try and approach it that way. I just know it will be tough at times.\n\nI can protect our country at many levels, not sure if that helps...")
  page_to_strzok(child_file, "2016-08-06T15:05:51-00:00", "I know it will too. But it's just a job. It's not a reflection of your worth or quality or smarts.")

  # Page 68, INBOX is Strozk->Page
  strzok_to_page(child_file, "2016-08-06T15:28:50-00:00", "I really like this:\nHe appears to have no ability to experience reverence, which is the foundation for any capacity to admire or serve anything bigger than self, to want to learn about anything beyond self, to want to know and deeply honor the people around you.")
  #page_to_strzok(child_file, "2016-08-06T15:30:59-00:00", "Sigh. That's the paragraph, upon reading, that caused me to want to send it to you. \U0001f636")
  #page_to_strzok(child_file, "2016-08-09T03:26:25-00:00", "He's not ever going to be president, right? Right?!")
  strzok_to_page(child_file, "2016-08-09T21:56:09-00:00", "OMG did you hear what Trump just said?")
  
  # Page 69, INBOX is Strozk->Page
  m = strzok_to_page(child_file, "2016-08-11T00:53:46-00:00", "Why Latitude? (other than it sounds badass, and you came up with it \U0001f636)")
  m.addnote("I think this is the first reference to creating Crossfire Latitude which became Crossfire Hurricane")
  #page_to_strzok(child_file, "2016-08-11T00:54:24-00:00", "Trying to think of something loosely military, without being obvious.")
  #strzok_to_page(child_file, "2016-08-11T00:56:56-00:00", "--Redacted-- YUUUUGE.\n\nThough we may save that for the man, if we ever open on him ;)")
  #strzok_to_page(child_file, "2016-08-11T00:57:27-00:00", "OMG I CANNOT BELIEVE WE ARE SERIOUSLY LOOKING AT THESE ALLEGATIONS AND THE PERVASIVE CONNECTIONS")

  # Page 70
  #strzok_to_page(child_file, "2016-08-11T00:57:41-00:00", "What the hell has happened to our country!?!?!??")
  #page_to_strzok(child_file, "2016-08-14T10:55:22-00:00", "God this makes me so angry. Donald Trump Is Making America Meaner http://nyti.ms/2b6gG38")
  strzok_to_page(child_file, "2016-08-14T11:00:46-00:00", "And I am worried about what Trump is encouraging in our behavior. The things that made me proud about our tolerance for dissent - what makes us different from Sunnis and Shias losing each other up - is disappearing.")
  #strzok_to_page(child_file, "2016-08-14T11:01:54-00:00", "I'm worried about what happens if HRC is elected. And perfect, another excessive heat day.")

  # Page 71
  # OUTBOX == Page
  # INBOX == Strzok
  #strzok_to_page(child_file, "2016-08-15T10:29:55-00:00", "I want to believe the path you threw out for consideration in Andy's office - that there's no way he gets elected - but I'm afrais we can't take that risk. It's like an insurance policy in the unlikely event you die before you're 40...")
  #page_to_strzok(child_file, "2016-08-17T10:28:37-00:00", "An article to share: Trump shakes up campaign, demotes top adviser Trump shakes up campaign, demotes top adviser http://wapo.st/2bzAUGD")
  #strzok_to_page(child_file, "2016-08-17T10:29:25-00:00", "Just reading it")

  # Page 72
  #strzok_to_page(child_file, "2016-08-17T11:02:31-00:00", "--Redacted--")
  #strzok_to_page(child_file, "2016-08-26T16:42:40-00:00", "Just went to a southern Virginia Walmart. I could SMELL the Trump support...")
  page_to_strzok(child_file, "2016-08-26T16:54:18-00:00", "Yup. Out to lunch with --Redacted-- We both hate everyone and everything.")
  #strzok_to_page(child_file, "2016-08-26T17:02:52-00:00", "I want to be there and hate with you, or charm you back to happy. Looked for the two trump yard signs I saw on the way out to take a picture, but couldn't find them")

  # Page 73
  page_to_strzok(child_file, "2016-08-26T20:51:12-00:00", "Just riffing on the hot mess that is our country.")
  strzok_to_page(child_file, "2016-08-26T20:52:28-00:00", "Yeah....it's scary real down here")
  #strzok_to_page(child_file, "2016-08-30T09:44:50-00:00", "Here we go: Harry Reid Cites Evidence of Russian Tampering in U.S. Vote and Seeks F.B.I. Inquiry http://mobile.nytimes.com/2016/08/30/us/politics/harry-reid-russia-tampering-election-fbi.html")
  #strzok_to_page(child_file, "2016-08-30T09:45:20-00:00", "But Mr. Reid argued that the connections between some of Donald J. Trump's former and current advisers and the Russian leadership should, by itself, prompt an investigation. He referred indirectly in his letter to a speech given in Russia by one Trump adviser, Carter Page, a consultant and investor in the energy giant Gazprom, who criticized American sanctions policy toward Russia. 'Trump and his people keep saying the election is rigged,' Mr. Reid said. 'Why is he saying that? Because people are telling him the election can be messed with.' Mr. Trump's advisers say they are concerned that unnamed elites could rig the election for his opponent, Hillary Clinton.")

  # Page 74
  page_to_strzok(child_file, "2016-08-30T09:45:44-00:00", "--Redacted-- called him and told him he would be sending a letter.")
  strzok_to_page(child_file, "2016-08-30T09:46:15-00:00", "Trying isn't enough! Or rather, it may be, but I'm not content with trying. Seriously. I'm walking over and paying for it today. You need to tell me a time.")
  #strzok_to_page(child_file, "2016-08-30T09:46:29-00:00", "Bill didn't mention it \U0001f612")
  #strzok_to_page(child_file, "2016-08-30T09:51:55-00:00", "And holy cow, let me send you the Reid letter!")

  # Page 75
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  #page_to_strzok(child_file, "2016-08-31T03:27:14-00:00", "Did you ever look at this? It's incredibly powerful.And really, really depressing.\n\nAt least 110 Republican Leaders Won\u2019t Vote for Donald Trump. Here\u2019s When They Reached Their Breaking Point. http://nyti.ms/2bTNAbb")
  page_to_strzok(child_file, "2016-08-31T11:37:05-00:00", "Re the case, Jim Baker honks you should have it. But I'm sure andy would defer to bill. I won't mention.")
  strzok_to_page(child_file, "2016-08-31T11:39:54-00:00", "--Redacted--")
  m = strzok_to_page(child_file, "2016-09-03T14:28:55-00:00", "I've been busy distracting myself, waiting on N to get up, not wanting to spin, reading the Federalist Papers looking for a great foreign influence quote. Yeah, I'm a nerd.")
  m.addnote("N could be a garble for M - Melissa, his wife")
  strzok_to_page(child_file, "2016-09-12T11:25:13-00:00", "Npr says Trump hotel opens today. It doesn't look ready...")

  # Page 76
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-09-12T11:26:16-00:00", "That's one place I hope I never stay in.")
  strzok_to_page(child_file, "2016-09-12T11:29:23-00:00", "Agreed. Hope it fails horribly. It wont, but still.")
  #page_to_strzok(child_file, "2016-09-27T00:40:23-00:00", "Did you read this? It's scathing. And I'm scared.\n\nWhy Donald Trump Should Not Be President http://nyti.ms/2dbQPuR")
  page_to_strzok(child_file, "2016-09-27T00:40:43-00:00", "Man, I should have started drinking earlier. I'm genuinely stressed about the debate.")

  # Page 77
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-09-27T10:37:52-00:00", "Can I ask you a question about yesterday's discussion? Why rule out a job at Doj or ODAG?")
  strzok_to_page(child_file, "2016-09-27T10:38:13-00:00", "Too political?")
  page_to_strzok(child_file, "2016-09-27T10:39:43-00:00", "No way. I don't see what I get out of that, and I'd have to deal with all the political BS.")
  strzok_to_page(child_file, "2016-09-27T10:40:32-00:00", "Political connections. Better entree into other jobs? Maybe not the latter.")

  # Page 78
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-09-29T01:10:28-00:00", "And suddenly I'm realizing, they're like Trump demographic people, just democrats. \U0001f612")
  strzok_to_page(child_file, "2016-09-29T01:10:29-00:00", "Like --Redacted--!!!!!!!!!\n\nOh sweet jes*s I need to send you what --Redacted-- has been sending. The liberal media is all in the tank for Hillary. Because, you know, Trump isn't batsh*t crazy for our country...")
  page_to_strzok(child_file, "2016-09-29T01:11:38-00:00", "Please don't. I really don't want to know what is out there.")
  strzok_to_page(child_file, "2016-09-29T01:13:46-00:00", "--Redacted-- is crazy, btw")

  # Page 79
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-09-29T01:14:28-00:00", "EVERYTHING about him is a dem. Except maybe string national defense (except Hillary is that but she can't be, because, you know, CLINTON!).")
  page_to_strzok(child_file, "2016-09-29T01:17:46-00:00", "I know. His political affiliation is truly baffling. He's a HUGE D.")
  strzok_to_page(child_file, "2016-09-29T01:18:16-00:00", "I know!")
  strzok_to_page(child_file, "2016-09-29T01:18:29-00:00", "I WANT YOU TO MEET HIM AND CONVINCE HIM!")

  # Page 80
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-09-29T01:19:06-00:00", "You're very persuasive. \n\nWe'll have to stay here as my iPhone is apparently syncing and downloading for the rest of the night\U0001f612")
  #strzok_to_page(child_file, "2016-09-29T01:53:27-00:00", "\"Found it hard to focus\"?\n\n\"Found it hard to focus\"?!?!??!\n\nAre you f*cking kidding me?!??!!\n\nDonald Trump got too much debate advice, so he took none of it.\nhttp://www.slate.com/blogs/the_slatest/2016/09/28/donald_trump_got_too_much_debate_advice_so_he_took_none_of_it.html")
  page_to_strzok(child_file, "2016-10-06T23:11:14-00:00", "So, I think --Redacted-- \U0001f628")
  strzok_to_page(child_file, "2016-10-06T23:18:44-00:00", "What?!?! Why?\n\nInvite --Redacted-- and Giacalone to your housewarming! That'll be fun!")

  # Page 81
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  m = page_to_strzok(child_file, "2016-10-06T23:20:17-00:00", "We got a list of kids with their parents' names. How many Matt Apuzzo's could there be in DC? Showed J a picture, he said he thinks he has seen a guy who kinda looks like that, but always really schlubby. I said that sounds like every reporter I have ever seen.")
  m.addnote("J - probably Joseph Burrow her husband")
  page_to_strzok(child_file, "2016-10-06T23:21:08-00:00", "Found what I think might be their address too.")
  strzok_to_page(child_file, "2016-10-06T23:21:37-00:00", "He's TOTALLY schlubby! Dont you remember?")
  m = page_to_strzok(child_file, "2016-10-06T23:22:31-00:00", "Wife is Becky Found address looking for her. Lawyer.")
  m.addnote("Unredacted with simple Google search")
  
  # Page 82
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-06T23:24:01-00:00", "Address?")
  m = page_to_strzok(child_file, "2016-10-06T23:24:34-00:00", "They met at Colby College Good on him, he started writing at the school paper.")
  m.addnote("Unredacted with simple Google search")

  page_to_strzok(child_file, "2016-10-06T23:24:58-00:00", "--Redacted-- I think.")
  page_to_strzok(child_file, "2016-10-06T23:26:39-00:00", "Just have to look up if it is inbounds for --Redacted-- ")

  # Page 83
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-06T23:26:41-00:00", "I wouldn't search on your work phone....no idea what that might trigger in --Redacted-- shop.... ;]")
  page_to_strzok(child_file, "2016-10-06T23:27:31-00:00", "Oops. Too late.")
  m = strzok_to_page(child_file, "2016-10-07T10:02:33-00:00", "Yeah and I made the mistake of reading some stupid NY Post article about how agents are ready to revolt against D because of MY...now I'm really angry....")
  m.addnote("MY - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-10-07T10:03:33-00:00", "There are a bunch of really ignorant people out there blinded by their politics.")

  # Page 84
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-10-07T10:03:56-00:00", "You can't read that sh*t. And honestly, let them. The bu would be better off without them.")
  page_to_strzok(child_file, "2016-10-07T10:04:02-00:00", "There are.")
  strzok_to_page(child_file, "2016-10-07T10:04:37-00:00", "Sadly reminds me how deeply politics, like religion, can sometimes blind objectivity.")
  strzok_to_page(child_file, "2016-10-07T10:04:38-00:00", "I can't help it. It's click bait. I emailed it to you.")

  # Page 85
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-08T12:35:47-00:00", "Currently reading about Trump. Wondering if he stepped down if Pence could actually get elected.")
  page_to_strzok(child_file, "2016-10-08T12:36:20-00:00", "That's probably more likely than Trump getting elected.")
  strzok_to_page(child_file, "2016-10-08T12:37:10-00:00", "I agree. I think it would actually energize the Republican vote.\n\nAnd no, not really re path forward.")
  strzok_to_page(child_file, "2016-10-09T21:07:51-00:00", "And funny quote from my cousin-in-law: \"No way Trump will drop out. Hey Republicans: how does it feel to carry something to term?\"")

  # Page 86
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  #strzok_to_page(child_file, "2016-10-10T01:23:55-00:00", "Trump saying agents at FBI are furious at the MYE outcome and he's getting a special prosecutor.")
  #page_to_strzok(child_file, "2016-10-12T03:04:57-00:00", "Hot damn. Big news day.\n\nBuffett Calls Trump\u2019s Bluff and Releases His Tax Data http://nyti.ms/2dSIOMS")
  page_to_strzok(child_file, "2016-10-12T03:16:35-00:00", "Wow, more forceful than I have seen him. Wonder what --Redacted-- would say about it.\n\nDonald Trump\u2019s Sad, Lonely Life http://nyti.ms/2dTCZxP")
  page_to_strzok(child_file, "2016-10-14T00:40:26-00:00", "Not sure why I thought this was so neat. Suppose it's just the law nerd in me.\n\nThe Times\u2019s Lawyer Responds to Donald Trump http://nyti.ms/2eOWNza")

  # Page 87
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-10-14T00:40:28-00:00", "God, she's an incredibly impressive woman. The Obamas in general, really. While he has certainly made mistakes, I'm proud to have him as my president. \n\nVoice Shaking, Michelle Obama Calls Trump Comments on Women\u2018Intolerable\u2019 http://nyti.ms/2eOMtoY")
  # Following two messages were also sent to Jon Moffa
  page_to_strzok(child_file, "2016-10-14T00:48:08-00:00", "Ugh. More of the same.\n\nDonald Trump, Slipping in Polls, Warns of \u2018Stolen Election\u2019 http://nyti.ms/2eO7imx")
  #m = page_to_strzok(child_file, "2016-10-14T00:51:26-00:00", "Nope. Full of dog whistles too: \"We do not want election stolen from us. Everybody knows what I'm talking about.\" The racism is barely even veiled anymore.")
  #m.addnote("Lisa Page thinks Trump is a racist")

  # Page 88
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  # Following two messages were also sent to Jon Moffa
  page_to_strzok(child_file, "2016-10-14T00:53:52-00:00", "The Roger Stone comments are scary as sh*t.")
  strzok_to_page(child_file, "2016-10-14T01:00:59-00:00", "Roger Stone is horrible.")
  strzok_to_page(child_file, "2016-10-15T01:26:22-00:00", "Stone \u2018happy to cooperate\u2019 with FBI on WikiLeaks, Russian hacking probes - POLITICO\nhttp://www.politico.com/story/2016/10/roger-stone-fbi-wikileaks-russia-229821")

  # Page 89
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-15T21:25:48-00:00", "That didn't take long \U0001f621")
  page_to_strzok(child_file, "2016-10-15T21:28:10-00:00", "At least we made the f-ers work on the weekend...")
  strzok_to_page(child_file, "2016-10-15T21:30:09-00:00", "Uh, and, yeah - like they're doing to us.\n\nI HATE this case.\n\nAnd a LOT to tell you about my convo with JG...")
  page_to_strzok(child_file, "2016-10-15T22:04:26-00:00", "Very nice work on that initial statement. Maybe we can talk tomorrow re JG..")

  # Page 90
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-17T23:58:22-00:00", "I'm seriously thinking one of us needs to host election night party.")
  page_to_strzok(child_file, "2016-10-18T00:00:22-00:00", "I nominate --Redacted--")

  # Page 91
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  m = strzok_to_page(child_file, "2016-10-18T00:00:35-00:00", "I'll probably have to write talking points (likely for CyD) so I won't be able to make it.")
  m.addnote("CyD - FBI Cyber Division")
  page_to_strzok(child_file, "2016-10-18T00:05:39-00:00", "You don't have to write talking points for Cyber if they don't tell you about the tasking!")

  # Page 92
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  m = strzok_to_page(child_file, "2016-10-18T00:28:47-00:00", "CyD prepping for election day on November 35th....")
  m.addnote("CyD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-10-19T09:55:26-00:00", "You see Tim Cook made the list of potential HRC running mates?")
  strzok_to_page(child_file, "2016-10-19T09:57:48-00:00", "It was a big list, but still, he was on there. From Podesta email.")
  strzok_to_page(child_file, "2016-10-19T13:04:19-00:00", "Came up with election night plan - we should all hit HH somewhere. Figure this damn thing better be called early. \U0001f612\n\nYou watching the debate tonight?")

  # Page 93
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  #strzok_to_page(child_file, "2016-10-20T01:15:44-00:00", "I am riled up. Trump is a fucking Idiot, is unable to provide a coherent answer.")
  #strzok_to_page(child_file, "2016-10-20T01:22:36-00:00", "I CAN'T PULL AWAY. WHAT THE FUCK HAPPENED TO OUR COUNTRY --Redacted/LIS--??!?!")
  #page_to_strzok(child_file, "2016-10-20T01:24:19-00:00", "I don't know. But we'll get it back. We're America. We rock.")
  #strzok_to_page(child_file, "2016-10-20T01:28:22-00:00", "Donald just said \"bad hombres\"\n\n\U0001f612")

  # Page 94
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  #strzok_to_page(child_file, "2016-10-20T01:30:00-00:00", "Chris Wallace is a turd")
  #strzok_to_page(child_file, "2016-10-20T01:30:02-00:00", "Hillary: Russia and WikiLeaks and highest levels of Russian Government and Putin!!!\n\nDrink!!!!")
  #strzok_to_page(child_file, "2016-10-20T01:32:40-00:00", "Oh hot damn, HRC is throwing down saying Trump in bed with russia")
  strzok_to_page(child_file, "2016-10-20T01:50:50-00:00", "She could do SO MUCH BETTER\n\nBut she's just not getting traction.\n\nJesus.\U0001f621\U0001f621\U0001f621\U0001f621")

  # Page 95
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  # Page 411 has the unredacted version of this message
  # strzok_to_page(child_file, "2016-10-20T02:02:43-00:00", "Maybe. I have to watch this.\n\nAnd I'm so damn mad --Redacted--\n\nAnd disgusted. And disappointed.")
  strzok_to_page(child_file, "2016-10-20T02:12:37-00:00", "Trump just said what the fbi did is disgraceful")
  strzok_to_page(child_file, "2016-10-20T09:55:27-00:00", "Hi. Watching the post-debate commentary. Vaguely satisfying to see Megyn Kelley (who had botox and looks HORRIBLE) utterly going after Trump.")
  page_to_strzok(child_file, "2016-10-24T00:00:15-00:00", "Article is out, but hidden behind paywall so can't read it.")

  # Page 96
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  # Page 413 has the unredacted version of this message
  # strzok_to_page(child_file, "2016-10-24T00:02:22-00:00", "Wsj? Boy, that was fast.\n\nNo word from --Redacted-- Should I \"find\" it and tell the team?")
  # Page 413 has the unredacted version of this message
  # page_to_strzok(child_file, "2016-10-24T00:03:38-00:00", "No, I think not. Maybe he didn't get a chance, or --Redacted-- decided not to say anything until tomorrow.")
  strzok_to_page(child_file, "2016-10-24T00:04:04-00:00", "Not behind a pay wall. I need to send")
  page_to_strzok(child_file, "2016-10-24T00:04:32-00:00", "Huh?")

  # Page 97
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-24T00:04:59-00:00", "The article is not behind a paywall\n\nWe get several hours of warning about every other email, but not this, arguably more important than most...")
  # Page 414 has the unredacted version of this message
  # page_to_strzok(child_file, "2016-10-24T00:05:30-00:00", "Jesus --Redacted-- Then fine. Send it to everyone you know. Or I can not tell you about it at all and you can just come across it given all the time you spend reading the Journal. \U0001f621")
  # page_to_strzok(child_file, "2016-10-24T00:05:50-00:00", "What difference does it make to send it to the team Sunday night vs monday morning?")
  page_to_strzok(child_file, "2016-10-24T00:07:37-00:00", "Thanks dude. Appreciate it. \U0001f621")
  
  # Page 98
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-24T00:08:15-00:00", "Or I can get it like I do every other article that hits my Google news alert. Seriously.")
  page_to_strzok(child_file, "2016-10-24T00:09:00-00:00", "Send me the Google alert.")
  strzok_to_page(child_file, "2016-10-24T00:10:31-00:00", "Give me a break. Go look at EVERY article I've sent the team.\n\nCount them.\n\nThen count every Godd*mn heads up I get from --Redacted-- but NOT this one.\n\nThen tell me i should sit on THIS one and let them hear from someone else. You're not being fair about this.")
  strzok_to_page(child_file, "2016-10-24T00:12:17-00:00", "I really cannot believe you're taking this position and it angers me. I'm going to hope your anger about --Redacted-- getting dragged into this is clouding things.")
  
  # Page 99
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  # Better unredacted version elsewhere
  #page_to_strzok(child_file, "2016-10-24T00:12:28-00:00", "I AM being fair about this. I asked you not to. I don't care that --Redacted-- sucks. 1) This is about trust, and 2) WHAT THE F DIFFERENCE DOES IT MAKE TO ANYONE ON THE TEAM? Is there some investigative step to take? Some mitigation measure?")
  # A whole bunch of messages are missing here
  page_to_strzok(child_file, "2016-10-25T00:46:57-00:00", "I hate this case. \U0001f621")
  strzok_to_page(child_file, "2016-10-25T00:52:31-00:00", "Why? What happened?")
  page_to_strzok(child_file, "2016-10-25T00:54:08-00:00", "Nothing more. Just all of it.")

  # Page 100
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  # Page 417 has unredacted version of this message
  # page_to_strzok(child_file, "2016-10-25T00:55:02-00:00", "I asked --Redacted-- and --Redacted-- to meet tomorrow morning. Please let me just meet with them alone. Please.")
  strzok_to_page(child_file, "2016-10-25T00:59:55-00:00", "Sure")
  page_to_strzok(child_file, "2016-10-25T10:11:45-00:00", "Christ. Make sure you scroll down and read that guy's comment about the polls.\n\nDonald Trump Dismisses Latest Accuser:\u2018Oh, I\u2019m Sure She\u2019s Never Been Grabbed Before\u2019 http://nyti.ms/2eyZhVL")
  page_to_strzok(child_file, "2016-10-26T11:39:00-00:00", "Let's talk about this later.\n\n\u2018We Need to Clean This Up\u2019: Clinton Aide\u2019s Newly Public Email Shows Concern http://nyti.ms/2dG6zaI")

  # Page 101
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-10-26T12:58:14-00:00", "And yup, me and --Redacted/Apuzzo-- at drop-off today...")
  strzok_to_page(child_file, "2016-10-26T13:06:37-00:00", "Nice!!!")
  strzok_to_page(child_file, "2016-10-26T13:06:46-00:00", "Hit piece on Andy from VA GOP in Hampton newspaper")
  page_to_strzok(child_file, "2016-10-26T13:13:47-00:00", "That sucks. I can talk btw.")

  # Page 102
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-27T00:06:05-00:00", "Interesting - one of the Podesta emails talks about him hosting Peter Kadzik at his house for dinner in Oct 2015. And in May, 2015, Kadaik's sone asked for a job on the campaign")
  # Page 421 has unredacted version of this message
  # strzok_to_page(child_file, "2016-10-27T00:29:59-00:00", "Not announced, but they all know. Calls actually happened yesterday.\n\nAnd I feel (hopefully don't look as old) like Keith Richards. --Redacted-- joining via call? There's nothing classified....")
  page_to_strzok(child_file, "2016-10-27T21:08:58-00:00", "On with --Redacted-- still.")
  strzok_to_page(child_file, "2016-10-27T21:09:48-00:00", "Hope it's going well...")

  # Page 103
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-10-27T21:21:08-00:00", "I'm done.")
  # Page 423 has unredacted version of this message
  # page_to_strzok(child_file, "2016-10-28T17:19:06-00:00", "Still on with --Redacted-- phone is ON FIRE.")
  strzok_to_page(child_file, "2016-10-28T17:19:38-00:00", "It's on news")
  # Page 423 has unredacted version of this message
  # strzok_to_page(child_file, "2016-10-28T17:29:58-00:00", "You may wanna tell --Redacted-- he should turn on CNN , there's news going on ;(")

  # Page 104
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-10-28T17:30:17-00:00", "He knows. He just got handed a note.")
  strzok_to_page(child_file, "2016-10-28T17:33:54-00:00", "Ha. He asking about it now?")
  m = strzok_to_page(child_file, "2016-10-30T13:50:53-00:00", "This is all Matt\n\n Justice officials warned FBI that Comey\u2019s decision to update Congress was not consistent with department policy - The Washington Post\nhttps://www.washingtonpost.com/world/national-security/justice-officials-warned-fbi-that-comeys-decision-to-update-congress-was-not-consistent-with-department-policy/2016/10/29/cb179254-9de7-11e6-b3c9-f662adaa0048_story.html?hpid=hp_hp-top-table-main_campaignprint-810pm%3Ahomepage%2Fstory")
  m.addnote("Matt - probably Matt Apuzzo, national security reporter a the Washington Post")
  m = page_to_strzok(child_file, "2016-10-30T13:56:06-00:00", "Yeah, I saw it. Makes me feel WAY less bad about throwing him under the bus in the forthcoming CF article.")
  m.addnote("CF - Possibly Crossfire Fury - Paul Manafort")

  # Page 105
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-10-30T13:57:24-00:00", "Yep the whole tone is anti Bu. Just a tiny bit from us. And serves him right. He's gonna be pissed....")
  page_to_strzok(child_file, "2016-10-30T17:27:31-00:00", "An article to share: FBI agents knew of Clinton-related emails weeks before director was briefed\nFBI agents knew of Clinton-related emails weeks before director was briefed\nhttp://wapo.st/2f2EhEO")
  page_to_strzok(child_file, "2016-10-30T18:32:07-00:00", "Okay now I'm getting angry.")
  # There's a better unredacted version
  # strzok_to_page(child_file, "2016-10-30T19:06:48-00:00", "What - --Redacted-- opening comments?")

  # Page 106
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  #page_to_strzok(child_file, "2016-10-30T19:30:47-00:00", "Sorry, utterly terrible day. I'm not sure I can identify one single redeeming thing about it.")
  #page_to_strzok(child_file, "2016-11-03T00:50:57-00:00", "Sorry. Rybicki called. Time line article in the post is super specific and not good. Doesn't make sense because I didn't have specific information to give.")
  strzok_to_page(child_file, "2016-11-03T00:55:50-00:00", "What post article?!?")
  page_to_strzok(child_file, "2016-11-03T00:56:28-00:00", "Just went up. WaPo.")

  # Page 107
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  #strzok_to_page(child_file, "2016-11-03T00:57:08-00:00", "Goddamn bills opaque comments.....")
  strzok_to_page(child_file, "2016-11-03T00:57:45-00:00", "Can I send to team?")
  page_to_strzok(child_file, "2016-11-03T00:57:54-00:00", "Yes")
  page_to_strzok(child_file, "2016-11-03T11:29:46-00:00", "The nyt probability numbers are dropping every day. I'm scared for our organization.")

  # Page 108
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-11-04T03:19:04-00:00", "Dude. On Inauguration Day, in addition to our kegger we should also have a screening of the Weiner documentary! \U0001f60a")
  strzok_to_page(child_file, "2016-11-06T20:33:54-00:00", "Trump about to get off his plane")
  page_to_strzok(child_file, "2016-11-06T20:52:54-00:00", "I'm on fox. Trump is talking about her.")
  #page_to_strzok(child_file, "2016-11-06T20:53:42-00:00", "He's talking about cartwright and Petraeus and how they're not protected. She's protected by a rigged system.")

  # Page 109
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-11-07T01:43:03-00:00", "Good lord...\n\nInside Donald Trump\u2019s Last Stand: An Anxious Nominee Seeks Assurance http://nyti.ms/2esuTs3")
  # strzok_to_page(child_file, "2016-11-08T01:56:33-00:00", "OMG THIS IS F*CKING TERRIFYING:\nA victory by Mr. Trump remains possible: Mrs. Clinton\u2019s chance of losing is about the same as the probability that an N.F.L. kicker misses a 38-yard field goal.")
  # page_to_strzok(child_file, "2016-11-08T02:05:51-00:00", "Yeah, that's not good.")
  m = page_to_strzok(child_file, "2016-11-08T02:42:33-00:00", "Oh god --Redacted/babe--.")
  m.addnote("Possibly 'babe' because Strzok has called Page that before")
  

  # Page 110
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-11-08T02:42:40-00:00", "What is she saying?")
  page_to_strzok(child_file, "2016-11-08T02:43:40-00:00", "She does realize you've been in EVERY conversation that has been had about this case, right?")
  m = strzok_to_page(child_file, "2016-11-08T02:44:54-00:00", "That we should have gone on the record saying Kallstrom and others are not credible (which may be valid), but then saying we could pull his tolls if we wanted to. Because she knows all about our policy regarding investigations of members of the media. \U0001f621")
  m.addnote("Kallstrom - Possibly Former FBI Assistant Director James Kallstrom ")
  strzok_to_page(child_file, "2016-11-08T02:45:31-00:00", "Yes. But she's an expert who knows everything. \n\nI'm telling you, it's wildly infuriating. She has good points buy then assumes wildly impossible understanding of things to make groundless assertions.")
  
  # Page 111
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-11-08T02:45:59-00:00", "Told her twice she was either calling me stupid or a liar. \U0001f621\U0001f621\U0001f621\U0001f621")
  page_to_strzok(child_file, "2016-11-08T02:46:06-00:00", "Uh, what crime are we investigating?\n\nAnd I'm sorry, that's a terrible idea. Go to war with the formers?")
  page_to_strzok(child_file, "2016-11-08T02:47:14-00:00", "Jesus, --Redacted--. I'm sorry. That would make me blind with rage.")
  #strzok_to_page(child_file, "2016-11-08T02:47:53-00:00", "Leaking information about ongoing investigations. Which is incorrect information. By agents who don't know about things talking to him. \n\nSee? That's the thing. Her initial point, that we should have gone after the agents talking harder and sooner, is not unreasonable. But the subsequent discussion falls into uninformed assertions.")

  # Page 112
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-11-09T01:06:45-00:00", "\U0001f60a\n\nHsppy Election geekdom here.")
  page_to_strzok(child_file, "2016-11-09T04:06:58-00:00", "Trump won NC")
  page_to_strzok(child_file, "2016-11-09T04:20:14-00:00", "PBS is projecting Florida as well.")
  page_to_strzok(child_file, "2016-11-09T09:34:14-00:00", "And there it is.")

  # Page 113
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-11-09T09:58:18-00:00", "Analogous to the public editor article Bill handed out.\n\nNews Media Yet Again Misreads America\u2019s Complex Pulse http://2eCqXVM")
  strzok_to_page(child_file, "2016-11-09T12:11:02-00:00", "Just woke up. We fought on and off all night.")
  #strzok_to_page(child_file, "2016-11-09T12:13:37-00:00", "Too hard to explain here. Election related. Which is also godawful bad. \n\nSure")
  page_to_strzok(child_file, "2016-11-09T12:43:13-00:00", "Are you even going to give out your calendars? Seems kind of depressing. Maybe it should just be the first meeting of the secret society.")
  
  # Page 114
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-11-13T19:11:15-00:00", "I bought all the president's men. Figure I needed to brush up on watergate. \U0001f615")
  page_to_strzok(child_file, "2016-11-14T13:51:27-00:00", "God, being here makes me angry. Lots of high fallutin' national security talk. Meanwhile, we have OUR task ahead of us...")
  page_to_strzok(child_file, "2016-11-14T20:08:18-00:00", "It's making me very angry.")
  page_to_strzok(child_file, "2016-11-14T20:08:40-00:00", "BBC News: Trump and Putin hold telephone talks\nTrump and Putin hold telephone talks - http://www.bbc.co.uk/news/world-us-canada-37981770")
  
  # Page 115
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  strzok_to_page(child_file, "2016-11-15T01:43:02-00:00", "\"CNN: Source says naming a Trump national security team a 'knife fight'\"")
  page_to_strzok(child_file, "2016-11-15T01:43:43-00:00", "Christ. What does that mean?!")
  strzok_to_page(child_file, "2016-11-15T01:46:21-00:00", "I can only guess difference of opinion between Trump and Republican establishment?")
  page_to_strzok(child_file, "2016-11-15T01:47:05-00:00", "I get it. I'm just exclaiming how f-ed it all is.")
  
  # Page 116
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-11-15T01:50:30-00:00", "My god, Sessions for DoD or AG.")
  strzok_to_page(child_file, "2016-11-15T01:51:43-00:00", "Which is the f-ed uppedness of it")
  strzok_to_page(child_file, "2016-11-18T12:40:45-00:00", "Sessions for AG")
  page_to_strzok(child_file, "2016-11-18T12:49:19-00:00", "Good god.")
  
  # Page 117
  # OUTBOX == Page to Strzok
  # INBOX == Strzok to Page
  page_to_strzok(child_file, "2016-11-21T01:14:10-00:00", "This is really disgusting. \n\nNYTimes: White Nationalists Celebrate \u2018an Awakening\u2019 After Donald Trump\u2019s Victory\nWhite Nationalists Celebrate \u2018an Awakening\u2019 After Donald Trump\u2019s Victory http://nyti.ms/2fc6vve")
  strzok_to_page(child_file, "2016-11-21T01:19:38-00:00", "Im worried racial tension is going to get really bad...")
  strzok_to_page(child_file, "2016-11-26T12:45:01-00:00", "You see Trump chose a Fox News analyst as his Dep Ntnl Security advisor?")
  strzok_to_page(child_file, "2016-12-01T01:52:01-00:00", "And I keep thinking about what the D said, what was it, sick to one's stomach? Want to talk with you about it more. And in would like to talk to Jim and Andy too. Jim may be too much a true believer though.")

  # Page 118
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-12-01T01:52:23-00:00", "Mildly nauseous, he said.")
  page_to_strzok(child_file, "2016-12-01T01:52:48-00:00", "Technically not sure you can talk to andy about it.\U0001f621")

  # Page 119 - This begins a section that looks to come from a different source.
  # Labelled DOJ-PROD-0000001
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2015-08-21T17:30:50-00:00", "Hi. Just got done with meeting now to working lunch. Starting working out of hq on Mon. Not kidding. Much more later of course")
  
  
  # SKIP AHEAD


  # Page 232
  page_to_strzok(child_file, "2016-05-04T00:40:51-00:00", "And holy shit Cruz just dropped out of the race. It's going to be a Clinton Trump race. Unbelievable.")
  strzok_to_page(child_file, "2016-05-04T00:41:24-00:00", "What?!?!??")
  page_to_strzok(child_file, "2016-05-04T00:41:37-00:00", "You heard that right my friend.")
  strzok_to_page(child_file, "2016-05-04T00:41:37-00:00", "I saw trump won, figured it would be a bit")
  #strzok_to_page(child_file, "2016-05-04T00:41:57-00:00", "Now the pressure really starts to finish MYE...")
  page_to_strzok(child_file, "2016-05-04T00:42:32-00:00", "It sure does. We need to talk about follow up call tomorrow. We still never have.")

  # Page 308
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-07-22T10:58:38-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-22T12:03:05-00:00", "I'm sending --Redacted-- to my 830...\U0001f612")
  page_to_strzok(child_file, "2016-07-22T12:54:01-00:00", "I'm talking to --Redacted-- about American exceptionalism right now.")
  page_to_strzok(child_file, "2016-07-22T13:01:04-00:00", "Pretty strongly in favor. As I said to --Redacted-- doesn't mean we're perfect or do everything right, but as a system of government, country of laws, I think we're pretty damn great.")
  strzok_to_page(child_file, "2016-07-22T13:03:44-00:00", "But there's a difference between that and exceptionalism. Just look at the word. It implies not only that we're great, but that you suck. And that we are better and you should change to be like us. It goes hand in hand with American arrogancism")
  page_to_strzok(child_file, "2016-07-22T13:05:27-00:00", "I know. I get that. I'm using the term loosely, not in the political philosophy way.")
  page_to_strzok(child_file, "2016-07-22T13:05:49-00:00", "And plus, I'm explaining why America is great --Redacted--")
  strzok_to_page(child_file, "2016-07-22T13:10:47-00:00", "\U0001f60a\n\nGoing to have to bail on my offer of ride, just got called to Bills")
  strzok_to_page(child_file, "2016-07-22T13:19:43-00:00", "And waiting outside his office...\U0001f612")
  m = page_to_strzok(child_file, "2016-07-22T17:49:06-00:00", "On my way. Have mye Qs.")
  m.addnote("mye - Midyear Exam - Hillary Clinton Classified Emails")
  strzok_to_page(child_file, "2016-07-22T17:49:28-00:00", "K --Redacted-- here")
  page_to_strzok(child_file, "2016-07-22T19:29:14-00:00", "Mtg just moved to 3:45 --Redacted--")
  strzok_to_page(child_file, "2016-07-22T19:30:08-00:00", "K. Maybe after.....hour mtg?")
  strzok_to_page(child_file, "2016-07-22T19:34:28-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-22T19:43:34-00:00", "Great, sounds fun.")
  strzok_to_page(child_file, "2016-07-22T21:50:17-00:00", "Just yelled at --Redacted-- for 15 minutes if you want to hear about it. ..")
  strzok_to_page(child_file, "2016-07-22T22:30:16-00:00", "Programs wonj't tell him anything. ..")
  page_to_strzok(child_file, "2016-07-22T22:33:12-00:00", "K. Will mention if Jim calls. \n\nWhat time so they get home?")
  page_to_strzok(child_file, "2016-07-22T23:51:15-00:00", "One sec. --Redacted-- and Jim Baker called.")
  page_to_strzok(child_file, "2016-07-22T23:58:47-00:00", "Also, Jim Baker said he understood and would think about it.")
  strzok_to_page(child_file, "2016-07-22T23:59:06-00:00", "Oh good. Thank you.")
  strzok_to_page(child_file, "2016-07-23T00:05:58-00:00", "Did you tell Jim that --Redacted-- wildly betrayed his confidence and --Redacted-- needs to pay a price for that?") 

  # Page 309
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-07-23T00:07:30-00:00", "B) Truly, it's like parenting a child (how he should think about --Redacted-- punishing/not rewarding bad behavior). They're just bullies and we need to f*cking grow a pair.") 
  page_to_strzok(child_file, "2016-07-24T21:14:27-00:00", "--Redacted-- And I still need to read Moffa's thing. --Redacted--")
  strzok_to_page(child_file, "2016-07-24T21:15:02-00:00", "You can read Moffa's thing tomorrow...won't take long.") 
  strzok_to_page(child_file, "2016-07-24T21:16:47-00:00", "Did you bring it home?") 
  strzok_to_page(child_file, "2016-07-24T21:17:04-00:00", "Moffa's thing") 
  page_to_strzok(child_file, "2016-07-24T21:17:05-00:00", "Oh the document? Yes.")
  m = strzok_to_page(child_file, "2016-07-24T21:17:15-00:00", "Or via eras?") 
  m.addnote("eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2016-07-24T23:26:28-00:00", "--Redacted-- then read Moffa's thing, --Redacted--")
  m = strzok_to_page(child_file, "2016-07-24T23:37:51-00:00", "Boo. Though I've got to read it too. Going the eras route...") 
  m.addnote("eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2016-07-24T23:47:30-00:00", "Though I will say it's a little bit of a challenge to read since I don't know her 302, and there's no commentary about why a particular passage was chosen.")
  strzok_to_page(child_file, "2016-07-24T23:51:00-00:00", "--Redacted--") 
  page_to_strzok(child_file, "2016-07-24T23:51:38-00:00", "Ah. So there's not necessarily an inconsistency hidden in there. Got it. Thanks, that helps.")
  strzok_to_page(child_file, "2016-07-24T23:51:49-00:00", "And yeah, without the 302 I'm not sure how much you can really do other than familiarize yourself. --Redacted--")
  strzok_to_page(child_file, "2016-07-24T23:52:17-00:00", "No. Many - most - are fully consistent. Maybe even all.")
  page_to_strzok(child_file, "2016-07-24T23:53:28-00:00", "Got into a disagreement with my two State friends. Nothing major, just making excuses for how they do business.")
  page_to_strzok(child_file, "2016-07-24T23:53:40-00:00", "Remind me tomorrow.")
  strzok_to_page(child_file, "2016-07-24T23:54:02-00:00", "Well they have a decades long pattern of it.") 
  page_to_strzok(child_file, "2016-07-25T00:09:56-00:00", "Jesus, did you read this?\n\nDonand Trump a racist? http://nyti.ms/2aiqD08")
  # better messages in lync_text_messages_of_peter_strzok_from_2-13-16_to_12-6-17.pdf
  #strzok_to_page(child_file, "2016-07-25T00:31:40-00:00", "Wildly unrelated, is --Redacted-- still chief judge of the fisc?")
  #page_to_strzok(child_file, "2016-07-25T00:32:45-00:00", "Don't think so. Just wiki the Fisc judges. It will tell you.")
  #page_to_strzok(child_file, "2016-07-25T00:33:29-00:00", "--Redacted--")

  # Page 310
  # OUTBOX == Page
  # INBOX == Strzok
  #page_to_strzok(child_file, "2016-07-25T00:34:40-00:00", "--Redacted--")
  #page_to_strzok(child_file, "2016-07-25T00:35:07-00:00", "--Redacted--")
  m = strzok_to_page(child_file, "2016-07-25T00:35:20-00:00", "--Redacted/Mitch-- has lined up a CI threat briefing for --Redacted/Brinkman-- in advance of her travel to --Redacted/the PRC--. I want to get ci training lined up for the whole federal judiciary. I'm worried we're sending the wrong folks to do the briefing.")
  m.addnote("Unredaction by Fox News https://web.archive.org/web/20181225103513/https://www.foxnews.com/politics/strzok-page-texts-reveal-personal-relationship-between-fbi-official-and-judge-recused-from-flynn-case")
  # better messages in lync_text_messages_of_peter_strzok_from_2-13-16_to_12-6-17.pdf
  #strzok_to_page(child_file, "2016-07-25T00:35:33-00:00", "I did. We talked about it before and after. I need to get together with him")
  page_to_strzok(child_file, "2016-07-25T00:35:43-00:00", "So get the right folks in then!")
  page_to_strzok(child_file, "2016-07-25T00:36:02-00:00", "You didn't tell me. \U0001f615")
  m = strzok_to_page(child_file, "2016-07-25T00:36:19-00:00", "I just emailed him and --Redacted/Sally-- that he --Redacted/(Mitch)-- and I should do it.")
  m.addnote("Unredaction by Fox News https://web.archive.org/web/20181225103513/https://www.foxnews.com/politics/strzok-page-texts-reveal-personal-relationship-between-fbi-official-and-judge-recused-from-flynn-case")
  strzok_to_page(child_file, "2016-07-25T00:36:24-00:00", "I did!")
  page_to_strzok(child_file, "2016-07-25T00:37:18-00:00", "No, you definitely didn't.")
  strzok_to_page(child_file, "2016-07-25T00:38:21-00:00", "I am almost certain I did. It may have been in passing in another discussion, but I have a memory of it.")
  page_to_strzok(child_file, "2016-07-25T00:38:32-00:00", "I think that makes sense. Remind me to tell you frustrating --Redacted-- convo I had with --Redacted--")
  strzok_to_page(child_file, "2016-07-25T00:39:00-00:00", "Ok. He won't let some things go....")
  page_to_strzok(child_file, "2016-07-25T00:39:13-00:00", "I honestly truly don't think you did. I'm serious. I would have remembered that. It's too central in my life. --Redacted--")
  strzok_to_page(child_file, "2016-07-25T00:40:11-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-25T00:41:16-00:00", "Well I have zero recollection of it. Recent, old, on phone, in person, text, nothing.")
  strzok_to_page(child_file, "2016-07-25T00:41:44-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-25T00:41:54-00:00", "In person.")
  strzok_to_page(child_file, "2016-07-25T00:42:30-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-25T00:42:50-00:00", "Was Moffa's thing low side or high side? Can't find it.")
  strzok_to_page(child_file, "2016-07-25T00:43:09-00:00", "Oops, just found it")
  page_to_strzok(child_file, "2016-07-25T00:43:10-00:00", "High.")

  # Page 311
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-07-25T00:44:07-00:00", "Peter. It wasn't me. No memory of minority mention or any of it. I'm sorry.")
  # Unredacted version above (Page 20 of lync messages...)
  # page_to_strzok(child_file, "2016-07-25T00:44:47-00:00", "--Redacted/Go ask her. Thought of it bc you had to Google Fisc judges and saw him there. I'm telling you--")
  m = strzok_to_page(child_file, "2016-07-25T00:50:43-00:00", "--Redacted/I just did. She confirmed I hadn't.-- So either in told you or wanted to tell you and hadn't. --Redacted/She brought up a good point about being circumspect in talking to him in terms of notplacing him into a situation where he'd have to recuse himself.--")
  m.addnote("Unredaction by Fox News https://web.archive.org/web/20181225103513/https://www.foxnews.com/politics/strzok-page-texts-reveal-personal-relationship-between-fbi-official-and-judge-recused-from-flynn-case")

  # unredacted version Page 21 of lync messages.pdf
  # page_to_strzok(child_file, "2016-07-25T00:52:07-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-25T00:52:23-00:00", "Anyway, maybe you meant to, but you didn't.")
  #strzok_to_page(child_file, "2016-07-25T00:53:08-00:00", "--Redacted--/Really? Rudy, I'm in charge of espionage for the FBI. Any espionage FISA comes before him, what should he do? Given his friend oversees them?--")

  # better messages in lync_text_messages_of_peter_strzok_from_2-13-16_to_12-6-17.pdf
  #strzok_to_page(child_file, "2016-07-25T00:53:55-00:00", "Ok, I believe you that I didn't. Thought I had. Happy to (indeed, wanted to and thought I did) talk about it with you.")
  #page_to_strzok(child_file, "2016-07-25T00:56:24-00:00", "--Redacted/standards for recusal are quite high. I just don't think this poses an actual conflict. And he doesn't know what you do?--")
  m = strzok_to_page(child_file, "2016-07-25T01:00:00-00:00", "Generally he does know what I do. Not the level or scope or area. Be he's super thoughtful and rigorous about ethics and conflicts. M suggested a social setting with others would probably be better than a one on one meeting. I'm sorry, I'm just going to have to invite you to that cocktail party.")
  m.addnote("M - probably his wife Melissa Hodgman")
  m.addnote("Unredaction by Fox News https://web.archive.org/web/20181225103513/https://www.foxnews.com/politics/strzok-page-texts-reveal-personal-relationship-between-fbi-official-and-judge-recused-from-flynn-case")

  strzok_to_page(child_file, "2016-07-25T01:08:13-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-25T01:08:23-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-25T01:08:35-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-25T10:29:56-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-25T10:31:41-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-25T10:32:37-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-25T10:35:59-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-25T10:36:55-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-25T10:43:24-00:00", "--Redacted--")
  # https://www.foxnews.com/politics/strzok-page-texts-reveal-personal-relationship-between-fbi-official-and-judge-recused-from-flynn-case

  # Page 312
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-07-25T10:44:59-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-25T11:57:34-00:00", "Have to brief this guy from hpsci at 2")
  page_to_strzok(child_file, "2016-07-25T13:10:20-00:00", "Was talking to andy, then rybicki, then new counsel guy.")
  strzok_to_page(child_file, "2016-07-25T14:25:10-00:00", "Did Baker decide whether he's participating in --Redacted-- call?")
  page_to_strzok(child_file, "2016-07-25T15:27:46-00:00", "Have not had a chance to ask, but I did check his calendar for today and tomorrow and didn't see it.")
  strzok_to_page(child_file, "2016-07-25T17:01:16-00:00", "Hey having a quick meeting with Bill --Redacted--")
  strzok_to_page(child_file, "2016-07-25T22:49:39-00:00", "Talking to Bill, want to catch up with you later. \U0001f615")
  strzok_to_page(child_file, "2016-07-25T23:44:38-00:00", "Leave = jeh, not Andy's office, right?")
  m = page_to_strzok(child_file, "2016-07-26T01:50:00-00:00", "--Redacted-- now about to read mye letter while I listen to Corey booker. He's doing very well.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok(child_file, "2016-07-26T01:52:02-00:00", "Hey, in case you haven't already, can you answer Jim's question re --Redacted--")
  strzok_to_page(child_file, "2016-07-26T01:52:21-00:00", "--Redacted-- letter? I thought Bakers comments were ok\n\nIt's amazing to me how much better this convention is. --Redacted--")
  strzok_to_page(child_file, "2016-07-26T01:52:30-00:00", "Which one --Redacted--")
  strzok_to_page(child_file, "2016-07-26T01:55:25-00:00", "Btw, any more discussion about JB not joining the call with --Redacted-- tomorrow?")
  page_to_strzok(child_file, "2016-07-26T02:03:00-00:00", "It's SO much more positive.")
  page_to_strzok(child_file, "2016-07-26T02:03:15-00:00", "I haven't heard anything more from Jim.")
  strzok_to_page(child_file, "2016-07-26T02:03:38-00:00", "Sigh. --Redacted-- was really upset.")
  strzok_to_page(child_file, "2016-07-26T02:05:46-00:00", "And so so so much better organized and coordinated than the rnc...")
  page_to_strzok(child_file, "2016-07-26T02:06:02-00:00", "Really upset that he would join the call? I get it. :(")
  strzok_to_page(child_file, "2016-07-26T02:07:02-00:00", "Yes. And even more at --Redacted-- and what she thought was utterly unprofessional behavior on his part. Which I also get.")
  strzok_to_page(child_file, "2016-07-26T02:08:11-00:00", "I just hope if JB participates, that somebody preps him. Because I'm not sure he knows the points to make on the call.\n\nMe too. \U0001f636")

  # Page 313
  # OUTBOX == Page
  # INBOX == Strzok
  # Unredacted from https://dailycaller.com/2018/06/12/strzok-texts-highly-questionable/
  strzok_to_page(child_file, "2016-07-26T02:30:57-00:00", "Here's what I'm about to send everyone in answer to JBs question Clinton, Mills, and Abedin all said they felt the server was permitted and did not receive information that it was not. To the extent there was objection down the line in IRM, we did not pursue that as State OIG did, because it was not a key question behind our investigation. There are going to be many avenues we might have pursued if we had unlimited time and resources, but this is one of those categories of wouldn't have changed our fundamental understanding of the gravamen of the case.")
  page_to_strzok(child_file, "2016-07-26T02:34:22-00:00", "Hmm. Should we send that? Maybe just find a quick moment to discuss it with him tomorrow?")
  strzok_to_page(child_file, "2016-07-26T02:35:29-00:00", "Either way. I want him to have the answer. We also have a-c privilege and deliberative process slapped all over it, but I take your point.")
  page_to_strzok(child_file, "2016-07-26T02:36:23-00:00", "Let's try to slip in and see him in the morning.")
  strzok_to_page(child_file, "2016-07-26T02:36:27-00:00", "Bottom line: it wasn't key to what we were looking at and it certainly was waaaay below the cut line of getting this done with the timeliness the D wanted.")
  strzok_to_page(child_file, "2016-07-26T02:36:39-00:00", "I have --Redacted-- early.\U0001f612")
  page_to_strzok(child_file, "2016-07-26T02:37:10-00:00", "Well I won't be there before --Redacted-- anyway.")
  page_to_strzok(child_file, "2016-07-26T02:46:45-00:00", "Your boy Bernie better not f this up. ;)")
  strzok_to_page(child_file, "2016-07-26T02:56:05-00:00", "Just sent you background on --Redacted--")
  strzok_to_page(child_file, "2016-07-26T03:23:02-00:00", "Jesus Christ how can he talk that long?!?!??!")
  page_to_strzok(child_file, "2016-07-26T03:26:36-00:00", "Okay, I stopped watching him like 20 minutes ago. I just don't care.\n\nThis however, was terribly charming. I \u2764 her.\n\nFirst Lady Michelle Obama Carpool Karaoke - Youtube\nhttps://m.youtube.com/watch?v=ln3wAdRAim4")
  page_to_strzok(child_file, "2016-07-26T03:54:19-00:00", "Well that's a relief! :)\n\nJust watched your video (think I had seen it) and a couple others. --Redacted--")
  strzok_to_page(child_file, "2016-07-26T11:48:26-00:00", "Just was talking with him...want to talk with you about strategies of what Bill wants to do with Brief.")
  strzok_to_page(child_file, "2016-07-26T15:31:31-00:00", "Hey so you want --Redacted-- on low side or high side? And how do you want ot tell Baker the answer to his --Redacted-- question?")

  # Page 314
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-07-26T15:33:39-00:00", "Oh yeah, forgot we wanted to do that.")
  page_to_strzok(child_file, "2016-07-26T15:57:47-00:00", "Still in here")
  page_to_strzok(child_file, "2016-07-26T16:06:40-00:00", "Headed to my ofc now")
  page_to_strzok(child_file, "2016-07-26T16:09:27-00:00", "Bring your wallet. Jim wants to meet at 430 instead.")
  page_to_strzok(child_file, "2016-07-26T18:08:34-00:00", "Stay there. Only have 20 minutes before I need to see andy again")
  strzok_to_page(child_file, "2016-07-26T18:11:39-00:00", "Mainly trying to one Starbucks run...want something later post-Andy mtg and pre-4:30 with Baker?")
  page_to_strzok(child_file, "2016-07-26T18:23:03-00:00", "We can try. I need to finish this letter today though. And I need to get out right after wrap.")
  strzok_to_page(child_file, "2016-07-26T23:54:42-00:00", "And hey. Congrats on a woman nominated for President in a major party!\n\nAbout damn time! Many many more returns of the day! \U0001f60a")
  page_to_strzok(child_file, "2016-07-26T23:56:57-00:00", "\U0001f60a That's cute. Thanks. \U0001f636")
  #strzok_to_page(child_file, "2016-07-26T23:58:20-00:00", "I had to --Redacted-- when Bernie just now moved for her nomination. \U0001f636\U0001f636\U0001f636")
  page_to_strzok(child_file, "2016-07-26T23:58:48-00:00", "I'm not watching. What happened?")
  strzok_to_page(child_file, "2016-07-27T00:02:08-00:00", "They went thru roll call, she got enough votes about an hour ago. Vermont went last, they cast their votes. Then introduced Bernie, who called for some procedural things then moved for HRC to become the Democratic Nominee.")
  strzok_to_page(child_file, "2016-07-27T00:02:41-00:00", "Chills, just because I'm a homer for American democracy that way. \U0001f636\U0001f636\U0001f636\U0001f636")
  strzok_to_page(child_file, "2016-07-27T00:03:06-00:00", "If they played patriotic music or did something with the flag and an honor guard, I probably would have teared up.....")
  strzok_to_page(child_file, "2016-07-27T00:05:18-00:00", "Turn on pbs!")
  strzok_to_page(child_file, "2016-07-27T00:07:14-00:00", "Oh God, Holder! Turn it off turn it off turn it off!!!!")
  page_to_strzok(child_file, "2016-07-27T00:11:56-00:00", "Sigh. Thank you. \U0001f636")
  page_to_strzok(child_file, "2016-07-27T00:11:47-00:00", "Yeah, I saw him yesterday and booed at the tv. \U0001f60a")
  strzok_to_page(child_file, "2016-07-27T00:15:56-00:00", "And --Redacted-- asked, since she's married to a man, there's no First Lady. What is there?")
  strzok_to_page(child_file, "2016-07-27T00:16:57-00:00", "(who's gonna be an utter charismatic hound dog, btw...)")
  page_to_strzok(child_file, "2016-07-27T00:21:39-00:00", "Yeah, it is pretty cool. She just has to win now. I'm not going to lie, I got a flash of nervousness yesterday about trump. The sandernistas have the potential to make a very big mistake here...")

  # Page 315
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-07-27T00:32:09-00:00", "I'm not worried about them. I'm worried about the anarchist Assanges who will take fed information and disclose it to disrupt.\n\n--Redacted--")
  #strzok_to_page(child_file, "2016-07-27T00:37:35-00:00", "Did you watch the D's happy birthday fbi message?")
  #page_to_strzok(child_file, "2016-07-27T00:47:48-00:00", "I didn't yet - I worked my tail off today. I heard he made a Clinton reference though, no?")
  strzok_to_page(child_file, "2016-07-27T00:50:29-00:00", "He did. Any referenced - again - that it wasn't just his decision, that it was the teams'")
  strzok_to_page(child_file, "2016-07-27T00:52:32-00:00", "More than a reference. Two points: terrorism Miami St Bernadino everywhere we're vigilant; second, HRC. Right decision. You may disagree but don't you dare think or say it was biased.")
  strzok_to_page(child_file, "2016-07-27T00:53:11-00:00", "Thinking of having lunch with Randy and seeking his support at the board. What do you think?")
  strzok_to_page(child_file, "2016-07-27T00:55:12-00:00", "If he's calling on MY credibility, my character, my career, my integrity, to defend his decision, that's gotta be worth something, right?")
  page_to_strzok(child_file, "2016-07-27T00:58:50-00:00", "I think it can't hurt. He's been reaching out, right?")
  page_to_strzok(child_file, "2016-07-27T00:59:31-00:00", "I would probably just wait to see if he asks what your next steps are. I wouldn't bring it up if he doesn't")
  strzok_to_page(child_file, "2016-07-27T01:16:08-00:00", "Just saw nyt feed. Jon said D's first Q at brief was about the case/two emails?")
  page_to_strzok(child_file, "2016-07-27T01:44:45-00:00", "Maybe not the first ut it came up very soon thereafter.")
  page_to_strzok(child_file, "2016-07-27T01:45:08-00:00", "Yeah, I saw it too. --Redacted-- so it wasn't us.")
  strzok_to_page(child_file, "2016-07-27T01:51:37-00:00", "I want to hear about it. --Redacted-- funny, he doesn't always share about stuff like that (and didn't much in this case).\n\nGuess I could ask him.")
  page_to_strzok(child_file, "2016-07-27T02:10:19-00:00", "Dammit, I just turned on the convention. I'm tired! But Bill is going to suck me in!")
  strzok_to_page(child_file, "2016-07-27T02:10:52-00:00", "Of course he is.\n--Redacted--")
  strzok_to_page(child_file, "2016-07-27T02:11:55-00:00", "Oh God, he's OLD \U0001f62f\U0001f622")
  # page_to_strzok(child_file, "2016-07-27T02:11:58-00:00", "And hey guess what, big surprise. --Redacted-- is a big R Arkansas Clinton-hater.")
  page_to_strzok(child_file, "2016-07-27T02:12:28-00:00", "And so skinny!")
  strzok_to_page(child_file, "2016-07-27T02:13:22-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-27T02:13:23-00:00", "Yeah. Really old. And missing words. But still charming.")
  page_to_strzok(child_file, "2016-07-27T02:14:28-00:00", "He's not using a teleprompter. He should")
  
  # Page 316
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-07-27T02:14:58-00:00", "You sure?")
  strzok_to_page(child_file, "2016-07-27T02:15:21-00:00", "Oh gosh his fingers Re trembling")
  page_to_strzok(child_file, "2016-07-27T02:16:56-00:00", "I know. I saw that too.")
  page_to_strzok(child_file, "2016-07-27T02:17:58-00:00", "Yeah, maybe he is using one")
  strzok_to_page(child_file, "2016-07-27T02:18:10-00:00", "He's def using teleprompter")
  strzok_to_page(child_file, "2016-07-27T02:20:40-00:00", "Will he get all 50 states before his speech is thru?")
  page_to_strzok(child_file, "2016-07-27T02:50:07-00:00", "It's fine, but not like Michelle.")
  strzok_to_page(child_file, "2016-07-27T02:50:55-00:00", "He's doing better now. He gets energy from the crowd.")
  page_to_strzok(child_file, "2016-07-27T02:53:03-00:00", "Yup, he does.")
  strzok_to_page(child_file, "2016-07-27T02:54:17-00:00", "So sad, the comment about more yesterdays than tomorrows. \U0001f622\n\nAnd i don't like Chelsea! Her husband even less...\U0001f612")
  page_to_strzok(child_file, "2016-07-27T02:57:07-00:00", "I like Chelsea fine. Why not?")
  strzok_to_page(child_file, "2016-07-27T03:00:18-00:00", "Self entitled. Feels she deserves something she hasn't earned")
  page_to_strzok(child_file, "2016-07-27T03:02:01-00:00", "Why do you think that?")
  page_to_strzok(child_file, "2016-07-27T03:02:17-00:00", "And crap! It's late again!")
  strzok_to_page(child_file, "2016-07-27T09:46:32-00:00", "God I'm tired. No cenvention tonight for me...")
  page_to_strzok(child_file, "2016-07-27T09:51:49-00:00", "Though Tim Kaine will likely speak.")
  strzok_to_page(child_file, "2016-07-27T23:58:38-00:00", "Arghh. Talked to --Redacted-- SO frustrating. --Redacted--\n\nAlso VERY different recounting from JB of call had with --Redacted--.")
  page_to_strzok(child_file, "2016-07-28T00:12:25-00:00", "No --Redacted-- it's not. STFU.")
  page_to_strzok(child_file, "2016-07-28T00:12:58-00:00", "Oh god. How different? Trisha and --Redacted-- were on the call - can't we get confirmation from them?")
  strzok_to_page(child_file, "2016-07-28T00:16:21-00:00", "Primary thing was no mention of perhaps doj over promised. I'll ask --Redacted-- tomorrow. Trisha won't tell (at least me) because it's secretsecretsecret. Sort of like this goddamn --Redacted-- Jon and I can't see...yet...\U0001f612")
  page_to_strzok(child_file, "2016-07-28T00:18:53-00:00", "He didn't say he said that. That was just offline to us.")

  # Page 317
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-07-28T00:21:17-00:00", "I understand that. --Redacted-- description of their behavior was based on a different interpretation --Redacted-- must have really over promised her clients, \"\"glad they got to see first hand how unreasonable she is, witness is yellig, etc etc\"")
  page_to_strzok(child_file, "2016-07-28T00:22:07-00:00", "Oh. Yeah, I didn't credit that at all.")
  #m = page_to_strzok(child_file, "2016-07-28T00:36:58-00:00", "Ha. First line made me smile.\n\nWhat Does the US Government Know Abour Russia and the DNC Hack? - Lawfare\nhttps://www.lawfareblog.com/what-does-us-government-know-about-russia-and-dnc-hack")
  #m.addnote("first line is Potentially unpleasant news for Jim Comey: We need you to intervene in the 2016 election again.")
  strzok_to_page(child_file, "2016-07-28T00:42:34-00:00", "Interesting. Good comments about Comey, too\n\nTrump and the Powers of the American Presidency, Part III - Lawfare\nhttps://www.lawfareblog.com/trump-and-powers-american-presidency-part-iii")
  page_to_strzok(child_file, "2016-07-28T00:55:29-00:00", "Damn. Didn't realize Panetta was on already.")
  page_to_strzok(child_file, "2016-07-28T00:59:03-00:00", "Stupid *ss Bernie supporters shouting no more war so that he couldn't be heard hardly at all. I'm sorry, they're idiots.")
  strzok_to_page(child_file, "2016-07-28T01:01:27-00:00", "They really are.")
  strzok_to_page(child_file, "2016-07-28T01:02:21-00:00", "And he was a really important speaker for them.\U0001f621")
  page_to_strzok(child_file, "2016-07-28T01:04:06-00:00", "I know. I'm really angry.")
  page_to_strzok(child_file, "2016-07-28T01:18:01-00:00", "I really really like Joe Biden.")
  strzok_to_page(child_file, "2016-07-28T01:24:09-00:00", "Was literally grabbing phone to say Joe's doing great!")
  page_to_strzok(child_file, "2016-07-28T01:26:14-00:00", "He's just a really sincere guy.")
  strzok_to_page(child_file, "2016-07-28T01:29:15-00:00", "Bob said he was absolutely beloved by Delaware State Police. And funny story about him and gtwn basketball team in China a few years ago. Too long for here.")
  #page_to_strzok(child_file, "2016-07-28T01:38:44-00:00", "--Redacted-- \U0001f621\n\nTrump & Putin. Yes, It's Really a Thing\nhttp://talkingpointsmemo.com/edblog/trump-putin-yes-it-s-really-a-thing")
  #strzok_to_page(child_file, "2016-07-28T01:51:10-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T01:54:20-00:00", "This article highlights the thing I mentioned to you earlier, asking if Bill had noted it to 7th floor. I'm going to send it to him")
  strzok_to_page(child_file, "2016-07-28T02:01:15-00:00", "I'm not going to be able to hold out until Obama...")
  strzok_to_page(child_file, "2016-07-28T10:04:56-00:00", "Hi. I'll be glad when the convention is over...I'm exhausted. Tom Kaine's a little weird.\n\nAnd it's a gorgeous sunrise...")
  page_to_strzok(child_file, "2016-07-28T10:34:30-00:00", "I also need this convention to be over. I'm extremely tired.")
  
  # Page 318
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-07-28T11:01:14-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T11:05:13-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-28T11:07:00-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-28T11:07:18-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T11:08:35-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T11:08:55-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-28T11:08:56-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-28T11:09:34-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T11:10:22-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-28T11:11:21-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-07-28T11:11:58-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T11:49:46-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T11:52:08-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-28T14:05:01-00:00", "Ok, now I'm angry...George called Bill --Redacted-- \U0001f621")
  page_to_strzok(child_file, "2016-07-28T14:05:43-00:00", "Yeah, that's irritating. Let them overrule us, then.")
  strzok_to_page(child_file, "2016-07-28T15:34:25-00:00", "Who is that --Redacted-- woman?")
  page_to_strzok(child_file, "2016-07-28T15:36:35-00:00", "--Redacted-- Head of the --Redacted-- unit.")
  page_to_strzok(child_file, "2016-07-28T15:40:34-00:00", "--Redacted-- out to lunch with --Redacted-- \U0001f612")
  strzok_to_page(child_file, "2016-07-28T15:59:45-00:00", "Oh boy. Working the board...")

  # Page 319
  # OUTBOX == Page
  # INBOX == Strzok
  # Page 319
  strzok_to_page(child_file, "2016-07-28T16:00:24-00:00", "I have better connections;)")
  strzok_to_page(child_file, "2016-07-28T16:00:49-00:00", "Wonder how he knows him")
  page_to_strzok(child_file, "2016-07-28T16:00:57-00:00", "Yeah, no clue.")
  strzok_to_page(child_file, "2016-07-28T16:03:57-00:00", "Gotta make sure I time Randy right")
  strzok_to_page(child_file, "2016-07-28T16:10:21-00:00", "And this is one of those instances where I'm proud of the people I know and don't know....")
  page_to_strzok(child_file, "2016-07-28T16:10:54-00:00", "You should be.")
  page_to_strzok(child_file, "2016-07-28T18:28:00-00:00", "Just finished meeting with --Redacted-- Don't care for him.\U0001f612")
  page_to_strzok(child_file, "2016-07-28T18:28:35-00:00", "No. Need to go see andy")
  strzok_to_page(child_file, "2016-07-28T18:30:05-00:00", "And I'm not surprised. All indications are he's a d*ck. Want to hear about it, of course.")
  page_to_strzok(child_file, "2016-07-28T18:36:58-00:00", "Of course. Ttyl.")
  strzok_to_page(child_file, "2016-07-28T22:27:39-00:00", "Just done with Bill you in office")
  page_to_strzok(child_file, "2016-07-28T22:28:09-00:00", "I'm going to bills right now. Figured you were there. :(")
  strzok_to_page(child_file, "2016-07-28T22:28:28-00:00", "He left.")
  strzok_to_page(child_file, "2016-07-28T22:28:33-00:00", "I'll come up")
  page_to_strzok(child_file, "2016-07-28T22:28:44-00:00", "For sure he's gone?")
  strzok_to_page(child_file, "2016-07-29T10:48:22-00:00", "Watched hillary is all")
  strzok_to_page(child_file, "2016-07-29T10:49:24-00:00", "She was ok. B+\n\nChelsea was awful. Tried to do Bills up close sharing. Didn't come across as genuine. Plus, she has a HORRIBLE billy goat speech tic")
  page_to_strzok(child_file, "2016-07-29T16:31:08-00:00", "Yeah, I didn't go. Too busy. Lunching with DD. Locking this up now")
  m = strzok_to_page(child_file, "2016-07-29T17:16:48-00:00", "Hey if you discussed new case with Andy would appreciate any input/guidance before we talk to Bill at 3. Let me know I'm happy to come up if that's easier.")
  m.addnote("new case - Probably Crossfire Hurricane")
  page_to_strzok(child_file, "2016-07-29T21:20:25-00:00", "Hey, can you ask jon to stick around?")
  m = page_to_strzok(child_file, "2016-07-29T21:20:46-00:00", "Going to try to finalize the lhm tonight")
  m.addnote("lhm - letterhead memorandum")
  m = strzok_to_page(child_file, "2016-07-29T22:17:01-00:00", "Oh - and Trisha mentioned to --Redacted-- to put --Redacted-- on this new case for seniority until she comes back from al....")
  m.addnote("al - Alabama?")

  # Page 320
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-07-29T22:40:47-00:00", "Oh. News breaking Russians hacked Clinton email.\n\nAlso, you talk to Eric?\n\nAnd yeah, re --Redacted-- \U0001f612 I told --Redacted-- to tell Trisha not to bother, that --Redacted-- can cover a week.")
  #strzok_to_page(child_file, "2016-07-29T22:45:40-00:00", "Ooh just saw on CNN first campaign add showing Gowdy and Comey's back and forth with a \"should HRC face criminal charges\" survey via 800 number.")
  page_to_strzok(child_file, "2016-07-29T22:48:34-00:00", "I agree re --Redacted--")
  #page_to_strzok(child_file, "2016-07-29T22:49:02-00:00", "Yeah Kortan told us DCCC and Hillary Campaign hacked.")
  page_to_strzok(child_file, "2016-07-29T22:50:32-00:00", "Spoke to eric. No real information, but she clearly wants to come back in a year. Over my dead body. Need to talk to rybibki. Spent a lot of talking with her.")
  m = strzok_to_page(child_file, "2016-07-29T22:51:58-00:00", "WTF!!!! The new guy, then her, again?!?\n\nShe can be a special assistant to the head of the TSC... \U0001f612\U0001f612\U0001f612")
  m.addnote("TSC - Terrorist Screening Center?")
  strzok_to_page(child_file, "2016-07-29T22:55:55-00:00", "Hey also note in the email you forwarded from --Redacted--")
  page_to_strzok(child_file, "2016-07-29T23:14:09-00:00", "Thanks. I didn't read it closely. Do you want t me to reach out to --Redacted--")
  strzok_to_page(child_file, "2016-07-29T23:16:43-00:00", "I don't know. What's the ask --Redacted--")
  page_to_strzok(child_file, "2016-07-29T23:17:11-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-30T00:26:38-00:00", "It will be great. Lots of light, it will be just fine.\n\nUnrelated, I cannot BELIEVE --Redacted-- thinks she can get back in. Talk about cognitive dissonance.")
  strzok_to_page(child_file, "2016-07-30T00:26:46-00:00", "And what it Rybicki thinking?!??!")
  page_to_strzok(child_file, "2016-07-30T00:27:28-00:00", "I know. Where? What on earth would she do?")
  page_to_strzok(child_file, "2016-07-30T00:27:46-00:00", "I don't think he's entertaining anything.")
  strzok_to_page(child_file, "2016-07-30T00:29:36-00:00", "Oh there's always room somewhere, just look at --Redacted-- and --Redacted-- and and and. Could replace --Redacted-- \n\nOh I thought he was the one who she had pitched. At length.")
  strzok_to_page(child_file, "2016-07-30T00:30:00-00:00", "I GUARANTEE Randy would take her, though he'll be gone")
  page_to_strzok(child_file, "2016-07-30T00:30:52-00:00", "I do think she was talking to him about it. But really, he would never. If he did, he'd be an utter lying hypocrite.")
  page_to_strzok(child_file, "2016-07-30T00:31:34-00:00", "I do think it's funny that she's not trying to get back to doj. Or maybe she is. Who knows.")
  strzok_to_page(child_file, "2016-07-30T00:32:11-00:00", "Probably both. But doj's too smart to rehire")

  # Page 321
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-07-30T00:32:33-00:00", "Yes. That's my guess too.")
  page_to_strzok(child_file, "2016-07-30T11:46:12-00:00", "Hey, do you want me to respond to --Redacted--")
  page_to_strzok(child_file, "2016-07-30T11:47:19-00:00", "He emailed.")
  strzok_to_page(child_file, "2016-07-30T11:47:45-00:00", "I didn't get a email notification. Let me go check")
  strzok_to_page(child_file, "2016-07-30T11:48:40-00:00", "Stupid phones.")
  strzok_to_page(child_file, "2016-07-30T11:49:41-00:00", "I'll respond. Answer is we're telling verbally via OGC channels of our intent to do so and following with written notice along with list of what we're providing?")
  page_to_strzok(child_file, "2016-07-30T11:51:08-00:00", "Yes, but we're not doing either until we meet with DOJ again and have come to final agreement about what we're turning over.")
  strzok_to_page(child_file, "2016-07-30T11:51:26-00:00", "Right")
  m = strzok_to_page(child_file, "2016-07-30T12:35:37-00:00", "Just got this from Jon. Couldn't agree more:\nI've mentally moved on to the next big thing. All this back and forth w/ DOJ on docs seems needlessly petty and irrelevant at this point. Not to them I guess...")
  m.addnote("next big thing - Crossfire Hurricane?")
  m = page_to_strzok(child_file, "2016-07-30T12:45:59-00:00", "Totally right there with you. Was thinking before bed last night that it is going to be hard to ramp up for testimony on MYE in the fall bc none of us are going to care at all anymore.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-07-30T12:50:52-00:00", "Do you know if Andy got concurrence back from George about the preamble? No need to ask Andy right now, I think we can in very good faith date the LHM July, 2016")
  page_to_strzok(child_file, "2016-07-30T13:07:00-00:00", "No, I haven't heard back.")
  strzok_to_page(child_file, "2016-07-30T13:08:45-00:00", "Np problem, it can absolutely wait. It's funny, I didn't see how last night's made any real difference, but of it makes Doj happier, great.")
  strzok_to_page(child_file, "2016-07-30T13:25:01-00:00", "Note addition of Jon and --Redacted-- to last email")
  page_to_strzok(child_file, "2016-07-30T13:30:50-00:00", "You saw this, right? It was incredibly moving.\n\nIn Tribute to Son, Khizr Khan Offered Citizenship Lesson at Convention http://nyti.ms/2azktsN")
  page_to_strzok(child_file, "2016-07-30T13:32:53-00:00", "Oh, you should go watch it. It was quite powerful. Read the article too.")
  strzok_to_page(child_file, "2016-07-30T15:32:20-00:00", "Hi. --Redacted-- I'm partial to any woman sending articles about how nasty the Russians are. --Redacted--")

  # Page 322
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-07-30T15:35:52-00:00", "--Redacted-- hate them. I think they're probably the worst. Very little I find redeeming about this. Even in history. Couple of good writers and artists I guess. --Redacted--")
  strzok_to_page(child_file, "2016-07-30T15:41:26-00:00", "--Redacted-- \nB)f*cking conniving cheating savages. At statecraft, athletics, you name it. I'm glad I'm on Team USA. --Redacted-- ...\nD) talking with --Redacted--, who's been great. Going back through acting DCM. All good, and asked him to keep quiet, bu+H3382t I think it's likely he will inform main State and they may call over to see what's going on. Will forward you the update I'm about to send Bill")
  strzok_to_page(child_file, "2016-07-30T18:24:56-00:00", "And unrelated, re work, of course I thought about you going. No chance Andy would want someone there for visibility?")
  page_to_strzok(child_file, "2016-07-30T18:25:27-00:00", "One sec, --Redacted--")
  page_to_strzok(child_file, "2016-07-30T18:25:44-00:00", "No chance of me going. He trusts you guys.")
  strzok_to_page(child_file, "2016-07-30T18:26:39-00:00", "--Redacted-- And poop. I'm glad he does, but just saying. Poop.")
  page_to_strzok(child_file, "2016-07-30T20:35:35-00:00", "The Real Plot Against America http://nyti.ms/2amhEYR")
  page_to_strzok(child_file, "2016-07-30T21:56:01-00:00", "\u2018I\u2019m Resigned to Having a Terrible President\u2019 http://nyti.ms/2aoV6GV")
  strzok_to_page(child_file, "2016-07-31T16:36:02-00:00", "--Redacted-- doing a million administrative things, dealing with personnel tweaks.")
  strzok_to_page(child_file, "2016-07-31T23:10:23-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-07-31T23:11:35-00:00", "And damn this feels momentous. Because this matters. The other one did, too, but that was to ensure we didn't F something up. This matters because this MATTERS. So super glad to be on this voyage with you.")
  strzok_to_page(child_file, "2016-07-31T23:12:06-00:00", "Roger thanks")
  strzok_to_page(child_file, "2016-07-31T23:13:52-00:00", "Thanks for doing that...")
  m = strzok_to_page(child_file, "2016-07-31T23:14:59-00:00", "Well wait a minute. Sentinel now shows --Redacted-- Go with this one.")
  m.addnote("Sentinel is the FBI's case management system")
  strzok_to_page(child_file, "2016-07-31T23:15:58-00:00", "10 4")
  page_to_strzok(child_file, "2016-07-31T23:20:46-00:00", "So on the other text, is Moffa --Redacted-- and --Redacted--")
  strzok_to_page(child_file, "2016-07-31T23:27:00-00:00", "Yes, but not sure which is which")

  # Page 323
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-07-31T23:28:52-00:00", "Don't you have their numbers in your phone?")
  strzok_to_page(child_file, "2016-07-31T23:30:01-00:00", "Sigh. Yes. But I need to go check...")
  strzok_to_page(child_file, "2016-07-31T23:30:32-00:00", "Plus I don't want the DD's office texting my people direct. I'm a control freak. :D")
  strzok_to_page(child_file, "2016-07-31T23:31:03-00:00", "Other way around. --Redacted--")
  page_to_strzok(child_file, "2016-07-31T23:31:11-00:00", "Oh please. I will find that out right quick. This is all about whether you want to make it easy on yourself.")
  page_to_strzok(child_file, "2016-07-31T23:31:17-00:00", "Ha. Thanks.")
  page_to_strzok(child_file, "2016-07-31T23:39:02-00:00", "--Redacted-- This makes me very angry.\n\nDonald Trump\u2019s Confrontation With Muslim Soldier\u2019s Parents Emerges as Unexpected Flash Point http://nyti.ms/2aEwvgz")
  strzok_to_page(child_file, "2016-07-31T23:41:10-00:00", "Yeah I'm furious about it. Interwebs are on fire. --Redacted--")
  #page_to_strzok(child_file, "2016-08-01T01:38:23-00:00", "I mean seriously. What in the hell is this guy talking about?\n\nDonald Trump Gives Questionable Explanation of Events in Ukraine http://nyti.ms/2arMCyV")
  page_to_strzok(child_file, "2016-08-01T01:58:10-00:00", "How Paul Manafort Wielded Power in Ukraine Before Advising Donald Trump http://nyti.ms/2aFy026")
  page_to_strzok(child_file, "2016-08-01T16:11:37-00:00", "I am just waiting for my calendar to open so I can check Andy's schedule and then I can go.")
  strzok_to_page(child_file, "2016-08-01T20:07:55-00:00", "Did Andy mention if he talked to --Redacted/Jeremy-- Don't ask if he didn't, just curious.")
  page_to_strzok(child_file, "2016-08-01T20:11:03-00:00", "He didn't reach him. He said he would try again.")
  page_to_strzok(child_file, "2016-08-01T20:38:03-00:00", "Ha. That's fine. I'm walking down to andy now.")
  #page_to_strzok(child_file, "2016-08-01T21:01:13-00:00", "Ho boy. Don't tell moffa, but andy is cancelling their brief. And he wants it first.")
  strzok_to_page(child_file, "2016-08-01T21:06:27-00:00", "Worried about it?")
  strzok_to_page(child_file, "2016-08-01T21:06:44-00:00", "I think that's smart. Bill may need a little saving from himself....")
  page_to_strzok(child_file, "2016-08-01T21:56:10-00:00", "Also, Andy spoke to --Redacted-- was out, he has a POC for you over there when you need it.")
  page_to_strzok(child_file, "2016-08-01T22:07:25-00:00", "Brief for tomorrow is just for DD now. It's better that way, I think.")
  page_to_strzok(child_file, "2016-08-02T12:04:11-00:00", "Hi! Good meeting? :)")

  # Page 324
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-02T12:04:29-00:00", "--Redacted--")
  #strzok_to_page(child_file, "2016-08-02T12:04:43-00:00", "With the --Redacted--, yes, good meeting")
  page_to_strzok(child_file, "2016-08-02T12:05:22-00:00", "--Redacted-- Whoa.")
  page_to_strzok(child_file, "2016-08-02T12:06:10-00:00", "Make sure you can lawfully protect what you sign. Just thinking about congress, foia, etc.")
  page_to_strzok(child_file, "2016-08-02T12:07:06-00:00", "I'm sure it's fine, I just don't know how protection of intel-type stuff works in that context.")
  page_to_strzok(child_file, "2016-08-02T12:07:21-00:00", "You probably know better than me.")
  strzok_to_page(child_file, "2016-08-02T12:07:43-00:00", "Oh. You're Gering this to review. I TOLD you that you should have come. ;)")
  strzok_to_page(child_file, "2016-08-02T12:19:34-00:00", "Getting, not Gering. Just sent to your fbinet email.\n\nAnd hi.\U0001f636\U0001f636\U0001f636")
  page_to_strzok(child_file, "2016-08-02T12:20:22-00:00", "K. I probably won't be in until about 9. Could you send to --Redacted-- and trisha too?")
  strzok_to_page(child_file, "2016-08-02T12:41:51-00:00", "\u0500\u03b3\u0201I did.\n\nBut if you were here, you could be reading it now as we wa")
  page_to_strzok(child_file, "2016-08-02T12:42:47-00:00", "I know.:(\n\nI just called trisha to make sure she looks at it soon. She is acting Jim so probably still in morning meetings.")
  strzok_to_page(child_file, "2016-08-02T12:45:39-00:00", "oh ooh ooh. --Redacted-- also told --Redacted-- at their mentoring session, \"one day I can see you on my staff.\"\n\nAnd \"ive cracked the code. Come to me and I'll tell y")
  strzok_to_page(child_file, "2016-08-02T12:48:06-00:00", "ou how to get where you want to go.\"\n\nWhat an ASTOUNDING douche")
  strzok_to_page(child_file, "2016-08-02T13:36:19-00:00", "Dude hurry up and get in. I worry ogc is making happy to glad changes which are nice to have but not legally necessary and which will derail this thing.")
  page_to_strzok(child_file, "2016-08-02T13:37:09-00:00", "I'm here. Reading it now")
  strzok_to_page(child_file, "2016-08-02T14:37:30-00:00", "Interesting fact. Guy we're about to interview was --Redacted--")
  page_to_strzok(child_file, "2016-08-02T16:56:19-00:00", "Yeah, that's helpful --Redacted/Ben-- is calling you a bunch of d*cks right now.")
  strzok_to_page(child_file, "2016-08-02T17:00:39-00:00", "Tell him to suck it! Enjoy your presentation about background investigations!")
  page_to_strzok(child_file, "2016-08-02T17:01:09-00:00", "We're all in the same place then. Ttyl.")
  page_to_strzok(child_file, "2016-08-02T17:50:13-00:00", "Have moffa and --Redacted-- here. Stand by.")
  strzok_to_page(child_file, "2016-08-02T17:56:53-00:00", "You knew THIS was inevitable...")
  strzok_to_page(child_file, "2016-08-02T18:17:32-00:00", "Oh good lord. Did you see Laufman's email?")

  # Page 325
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-02T18:36:59-00:00", "I did have to field an awkward \"so who are you? And what are you doing on this case\" kind of question from --Redacted/Ben-- Jon did me a solid and answered for me. :)")
  page_to_strzok(child_file, "2016-08-02T19:27:22-00:00", "--Redacted-- holier- --Redacted--")
  strzok_to_page(child_file, "2016-08-02T19:55:44-00:00", "And you HAVE had to deal with --Redacted/Richard-- and --Redacted/David-- I thought --Redacted-- was out all week")
  strzok_to_page(child_file, "2016-08-02T21:53:59-00:00", "Hi. --Redacted-- emailed me, so im hoping that might mean you're done...\U0001f636")
  strzok_to_page(child_file, "2016-08-02T22:44:57-00:00", "And hey. I just had an extraordinary flash of anger that our long-stated desire to Doj to get us comments by Thursday in order to have a meeting on Friday was trumped by --Redacted-- and --Redacted-- being absent. You know what? I'm absent now. I'll be back on Wed. So, Doj, stick to the original time frame we've had so Pete can be present. I guess --Redacted/Richard-- and --Redacted/David-- being there is SO much more important. Crank crank crank.\n\nAre we still having a meeting on Fri?")
  strzok_to_page(child_file, "2016-08-02T23:03:21-00:00", "And just heard from Jon. Thanks so much for having the discipline to wait another 24 hours to have the first meeting about the case with Doj. I really appreciate it.")
  page_to_strzok(child_file, "2016-08-02T23:30:47-00:00", "Jesus. There's a lot to read here. Let me call --Redacted/Joe-- check in with andy, and I will call you.")
  strzok_to_page(child_file, "2016-08-03T00:57:16-00:00", "Yeah well I'm going to go write some recollections from the interviews this afternoon. The fact that I'm thinking of things that I just mentioned right now that I didn't immediately remember makes me think I need to get them jotted down.")
  strzok_to_page(child_file, "2016-08-03T00:57:50-00:00", "Ooh. Remind me about the scif and the embassy history.")
  strzok_to_page(child_file, "2016-08-03T00:58:10-00:00", "And I want to tell you now. \U0001f636")
  strzok_to_page(child_file, "2016-08-03T00:58:33-00:00", "The first part needs to be on another system, though. Or in person.")
  strzok_to_page(child_file, "2016-08-03T01:07:28-00:00", "Oooh. And remind me --Redacted-- \U0001f628")
  page_to_strzok(child_file, "2016-08-03T01:08:44-00:00", "Think so. Not sure. For sure his RNC experience is going to be a zero, don't know enough to tell more.")
  strzok_to_page(child_file, "2016-08-03T01:09:26-00:00", "A zero in terms of not the same characters?")
  m = strzok_to_page(child_file, "2016-08-03T01:10:12-00:00", "Also, lhm preamble is fine. I cannot believe how long it took \U0001f612")
  m.addnote("lhm - Letterhead Memorandum")
  page_to_strzok(child_file, "2016-08-03T01:10:25-00:00", "Just don't think it's going to be useful. Think interactions are going to be more with his security folks. (Bc he has private, ex-Bu ones in addition to the Service).")

  # Page 326
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-03T01:11:02-00:00", "Yeah, George finally got it when I explained why Andy was concerned and first asked for it. That helped, I think.")
  strzok_to_page(child_file, "2016-08-03T01:17:00-00:00", "So looking at this form, I think we need to consider the lines of what we disclose to Doj. For example, the last stipulation notes we will not disclose the identities outside the FBI. I think we and they could live with that.\n\nAnd frankly, I think you might argue the unauthorized disclosure might reasonably be expected to cause exceptionally grave damage to US national security...")
  strzok_to_page(child_file, "2016-08-03T01:40:24-00:00", "--Redacted-- talked about the Embassy. It's the longest continuously staffed establishment in London (he noted the Audtrian was the oldest but they were thrown out during the War (s))")
  page_to_strzok(child_file, "2016-08-03T01:43:20-00:00", "--Redacted/Just you two? Was DCM present for the interview?--")
  strzok_to_page(child_file, "2016-08-03T01:43:42-00:00", "--Redacted/No, two of them, two of us--")
  strzok_to_page(child_file, "2016-08-03T01:47:56-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-08-03T01:47:57-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-08-03T01:50:26-00:00", "--Redacted--")
  m = strzok_to_page(child_file, "2016-08-03T01:50:27-00:00", "Random fact? (I'm looking at the dip list to get a name) Armenian Ambassador to London? Armen Sarkissian. Wife Nouneh.")
  m.addnote( "dip - diplomat. He is in the A's so probably looking up Australian diplomat")
  page_to_strzok(child_file, "2016-08-03T02:14:50-00:00", "FYI, just checked yellow, and there are POCs for you from both OGAs waiting there for you. Both may have already reached out. Safe travels home.")

  ie = Investigation.createevent()
  ie.text = "Strzok in London"
  ie.when = truxton.parsetime("2016-08-03T02:14:50-00:00")
  ie.save()

  page_to_strzok(child_file, "2016-08-03T07:33:34-00:00", "New case. Information flow. Control.")
  page_to_strzok(child_file, "2016-08-03T07:34:14-00:00", "Andy. The dynamic.\n\nAnd yeah, but it's not mine to worry about.")
  # This URL contains hand written unredactions
  # https://www.scribd.com/document/415514300/Strzok-Page-text-messages
  strzok_to_page(child_file, "2016-08-03T07:35:59-00:00", "Right there with you. Already told --Redacted/Joe we're writing it up.--\n\nI plan on telling Bill I'm obviously going to tell him anything he wants to know, but recommended we not tell him or higher specific data so that he and higher can tell DOJ, even we don't know the admin details.")
  strzok_to_page(child_file, "2016-08-03T07:36:23-00:00", "You're Andy's counsel. By definition it's yours to worry about.")

  # Page 327
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-03T07:37:02-00:00", "No it's not. Not like this. He's clearly not.")
  strzok_to_page(child_file, "2016-08-03T07:38:31-00:00", "this is MUCH more tasty for one of those --Redacted-- aholes to leak. For the first time in a while I'm not worried about our side. \U0001f612")
  strzok_to_page(child_file, "2016-08-03T07:39:29-00:00", "He's clearly not what? Worrying about --Redacted--")
  page_to_strzok(child_file, "2016-08-03T07:39:52-00:00", "Information flow and control.")
  strzok_to_page(child_file, "2016-08-03T07:40:58-00:00", "He should be. I can reinforce that when I brief you/Bill, and Andy, if I talk to him about it.")
  m = page_to_strzok(child_file, "2016-08-03T17:51:41-00:00", "Sheesh, I'm glad you're back. I'm really busy. I'm about to send an email. We NEED to focus on getting mye out the door, and quickly. We're not going to be able to withstand the pressure soon.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-08-03T17:54:00-00:00", "Yep we do, and I haven't experienced the last two days on it. I'll call (you know there's no way I could wait, though --Redacted-- will be in the cab), let me know what I need to push.\n\nAnd hi \U0001f60a")
  strzok_to_page(child_file, "2016-08-03T18:54:45-00:00", "I like you dealing with Laufman.\u263a\n\nAnd we may beat 410. Rahmatullan Rahimi drives like the wind in hi Prius...")
  page_to_strzok(child_file, "2016-08-03T19:08:48-00:00", "What's the plan for briefing Bill? Have you reached out to him?")
  strzok_to_page(child_file, "2016-08-03T19:09:15-00:00", "Not yet \U0001f636")
  page_to_strzok(child_file, "2016-08-03T19:09:49-00:00", "Oh, bc that's on purpose?")
  strzok_to_page(child_file, "2016-08-03T19:10:07-00:00", "Wanted to get in first. Ideally want to do when you and Moffa are around. Should I send an email to the three of you re availability")
  page_to_strzok(child_file, "2016-08-03T19:10:28-00:00", "Have you called George? I'm telling you, you should do that before you get in here.")
  strzok_to_page(child_file, "2016-08-03T19:10:32-00:00", "No. Just hadn't thought it through yet. Will send an email. At 14th and Penn.")
  page_to_strzok(child_file, "2016-08-03T19:10:41-00:00", "Oh! \U0001f636")
  strzok_to_page(child_file, "2016-08-03T19:11:07-00:00", "I havent, but I don't want to talk in front of our cab driver. I'll call him from cell from my office.")
  page_to_strzok(child_file, "2016-08-03T19:15:18-00:00", "Or mine. \U0001f636")
  strzok_to_page(child_file, "2016-08-03T21:38:55-00:00", "Hi. Our 4:00 meeting was Not Helpful. \U0001f60a\U0001f636")
  page_to_strzok(child_file, "2016-08-03T22:10:20-00:00", "--Redacted-- in my ofc. Will let you know when he is gone.")
  strzok_to_page(child_file, "2016-08-04T12:37:43-00:00", "I did ok briefing Bill yesterday. .. :D")

  # Page 328
  # OUTBOX == Page
  # INBOX == Strzok
  #strzok_to_page(child_file, "2016-08-04T23:59:34-00:00", "Yep.\n\nTrying to be grownup and not ask to come tomorrow based on mye, --Redacted-- overlap. Jon's brief, he's got it. I just love, and am good, at thinking thru it.")
  m = strzok_to_page(child_file, "2016-08-05T00:01:38-00:00", "Yep but willing to bet all those things will come up. Along with ci briefs to candidates.")
  m.addnote("ci - Counterintelligence")
  strzok_to_page(child_file, "2016-08-05T00:01:50-00:00", "We need to figure out what's going on with that")
  page_to_strzok(child_file, "2016-08-05T00:02:14-00:00", "We need jon to enter in his guys to the system.")
  page_to_strzok(child_file, "2016-08-05T00:02:27-00:00", "Oh, we haven't talked about that solution yet, have we?")
  page_to_strzok(child_file, "2016-08-05T00:02:39-00:00", "It's pretty elegant.")
  page_to_strzok(child_file, "2016-08-05T00:03:00-00:00", "Don't really want to tell you here. Will tell you tomorrow.")
  strzok_to_page(child_file, "2016-08-05T00:03:51-00:00", "Oh, they brought it up - to check when it gets entered")
  strzok_to_page(child_file, "2016-08-05T00:04:09-00:00", "Without having g to ask/rely on others")
  strzok_to_page(child_file, "2016-08-05T00:04:20-00:00", "--Redacted-- mentioned it")
  strzok_to_page(child_file, "2016-08-05T00:10:42-00:00", "Seriously, you don't think I should try and go to the AM meeting? How does it not involve extensive discussions about the --Redacted--")
  page_to_strzok(child_file, "2016-08-05T00:11:11-00:00", "Pete. It's not a meeting. It's pulling up jon for 5 minutes to discuss lanes in the road.")
  strzok_to_page(child_file, "2016-08-05T00:11:35-00:00", "Think of the threshold you use when deciding whether you go to a meeting...\n\nOk\U0001f636")
  strzok_to_page(child_file, "2016-08-05T00:12:06-00:00", "Gonna take more than 5 minutes. Or, give Andy the questions/issues for an answer later.")
  page_to_strzok(child_file, "2016-08-05T00:12:57-00:00", "It's quick and informal. And this is not going to be the last opportunity to talk about this. Especially if --Redacted-- there will be lots of time to discuss.")
  strzok_to_page(child_file, "2016-08-05T00:16:24-00:00", "I get it. I'm not talking about options so much as the difficult questions are ones that I'm directly involved with.\n\nBut OK. I will. If you were in my spot, wouldn't you want to go? For examole, I have no desire to be at the joint run through with Cyber.")
  page_to_strzok(child_file, "2016-08-05T00:17:35-00:00", "And --Redacted-- how many meeting are you at that Jon has an equal right and contribution to make that he is not at?")
  strzok_to_page(child_file, "2016-08-05T00:18:27-00:00", "Those times I can invite him, I do.")
  strzok_to_page(child_file, "2016-08-05T00:18:57-00:00", "And I, for example, the agency said today their group is too big to comet to us. So we either go to them, and jon is out, or reschedule till next week. What should I do?")
  strzok_to_page(child_file, "2016-08-05T00:19:33-00:00", "Re your question, I can think of two with Andy.")

  # Page 329
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-05T00:20:00-00:00", "Reschedule.")
  page_to_strzok(child_file, "2016-08-05T00:20:33-00:00", "Pete, I'm not going to fight with you about this. You asked for my opinion, I gave it to you.")
  strzok_to_page(child_file, "2016-08-05T00:21:59-00:00", "And push till next week? We willing to bear the \"FBI is delaying\" line?")
  page_to_strzok(child_file, "2016-08-05T00:22:57-00:00", "The work right now is all analytical. Does Monday make a difference? Will other analysts go?")
  strzok_to_page(child_file, "2016-08-05T00:27:23-00:00", "My concern is the perceived delay of not going it this week. A day clearly doesn't matter, though we pushed till the end of this week at my request due to not being available at the beginning of the week.")
  strzok_to_page(child_file, "2016-08-05T00:27:50-00:00", "And it's not just analysis. And, shockingly, agents are also capable of analysis as well...")
  page_to_strzok(child_file, "2016-08-05T00:29:18-00:00", "Okay, I'm done having this conversation with you.")
  page_to_strzok(child_file, "2016-08-05T00:29:32-00:00", "I asked if the other analysts would be going.")
  strzok_to_page(child_file, "2016-08-05T00:32:40-00:00", "That's up to Jon. I just told him I was calling --Redacted-- and telling her he needs to be there and to reschedule to Monday unless he doesn't want to do that.")
  page_to_strzok(child_file, "2016-08-05T00:33:00-00:00", "Are you going by yourself or planning to take others?")
  strzok_to_page(child_file, "2016-08-05T00:33:43-00:00", "No, I told --Redacted-- him, me, --Redacted-- just our leadership. Her group is apparently too big to fit into a car.\U0001f612")
  strzok_to_page(child_file, "2016-08-05T00:34:24-00:00", "If Jon says keep it, I will take --Redacted-- and defer to Jon if he wants me to take one of his guys.\n\nBut when we spoke earlier, he wanted me to postpone it.")
  page_to_strzok(child_file, "2016-08-05T00:34:30-00:00", "Yes Peter. That is my point. She has a whole team, all you need is yourself.")
  strzok_to_page(child_file, "2016-08-05T00:37:31-00:00", "No, damnit, that's not it. I don't want to wait longer.")
  strzok_to_page(child_file, "2016-08-05T00:38:19-00:00", "What I don't like about their behavior is knowing we were only bringing leadership, they can't bring three to us?")
  strzok_to_page(child_file, "2016-08-05T00:38:59-00:00", "But instead they'll fill the room to take notes on everything we say and also ensure that no one on their side says anything sensitivr")
  strzok_to_page(child_file, "2016-08-05T00:39:04-00:00", "Sensitive.")
  strzok_to_page(child_file, "2016-08-05T00:39:28-00:00", "And why I told Jon I was going to push the meetig")
  strzok_to_page(child_file, "2016-08-05T00:39:35-00:00", "Meeting")
  page_to_strzok(child_file, "2016-08-05T00:40:12-00:00", "So ask them to skinny down and come to you. It's your meeting, and we're leading this effort.")
  strzok_to_page(child_file, "2016-08-05T00:45:18-00:00", "Yep, that's what I plan to do. And if the can't, we'll reschedule.")

  # Page 330
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-05T00:53:29-00:00", "And so you know, I value your advice. Letting the meeting tomorrow go, and rescheduling the one tomorrow so Jon can be there, and also not play into agency's bs game")
  m = page_to_strzok(child_file, "2016-08-05T11:28:23-00:00", "--Redacted-- You can. If you need a day, take a day. I can pickup the mye stuff, nothing else is that pressing.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  m = strzok_to_page(child_file, "2016-08-05T11:29:44-00:00", "That's not true. There's the meeting with my team, the meeting at the agency (looks like Jon can go, not sure where the notion of a schedule conflict came from), mye, everything else in my Section, acting DAD.\n\n--Redacted--")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  #strzok_to_page(child_file, "2016-08-05T14:09:05-00:00", "Have M w f meetings with --Redacted-- at 9 like we did with mye.\n\nNeed to tall to you about Bill")
  page_to_strzok(child_file, "2016-08-05T14:50:44-00:00", "--Redacted-- too, right?")
  strzok_to_page(child_file, "2016-08-05T14:52:47-00:00", "Not sure. Probably, right? Defer to --Redacted--")
  page_to_strzok(child_file, "2016-08-05T14:53:45-00:00", "I'm just going to invite him. Though it's a big group now (10). Added baker.")
  strzok_to_page(child_file, "2016-08-05T14:59:40-00:00", "4 ogc attorneys...")
  strzok_to_page(child_file, "2016-08-05T14:59:40-00:00", "Whatever. It's fine. --Redacted-- deserves to be there")
  page_to_strzok(child_file, "2016-08-05T15:00:09-00:00", "Yup. Who do I exclude?")
  page_to_strzok(child_file, "2016-08-05T15:00:18-00:00", "Agreed. Okay, whatever.")
  #strzok_to_page(child_file, "2016-08-05T16:37:25-00:00", "And hi. Went well, best we could have expected. Other than L.C's quote, \"the White House is running this.\"")
  #strzok_to_page(child_file, "2016-08-05T16:37:46-00:00", "My answer, \"well, maybe for you they are.\" \U0001f612")
  strzok_to_page(child_file, "2016-08-05T16:44:35-00:00", "And of course, I was planning on telling this guy, thanks for coming, we've got an hour, but with Bill there, I've got no control.\n\nWhat time do you need to leave?")
  page_to_strzok(child_file, "2016-08-05T16:54:55-00:00", "Don't you have work to do?")
  page_to_strzok(child_file, "2016-08-05T16:55:26-00:00", "Yeah, whatever (re the WH comment). We've got emails that say otherwise.")
  strzok_to_page(child_file, "2016-08-05T20:45:10-00:00", "Gotta see Bill. Ttyl.")
  page_to_strzok(child_file, "2016-08-05T22:05:41-00:00", "Jesus, are you STILL talking to Bill?\U0001f612")
  strzok_to_page(child_file, "2016-08-05T22:10:10-00:00", "He is FREAKING out")
  page_to_strzok(child_file, "2016-08-05T22:34:13-00:00", "Think I'm going in on Sunday. 2-3 hours. I just NEED to read that LHM or I'm not going to be able to.")
  strzok_to_page(child_file, "2016-08-05T22:41:05-00:00", "Of course if you do, I'll try, too\U0001f636")

  # Page 331
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-05T22:41:36-00:00", "I can also email it to you if you want me to encouraging ERASing...")
  strzok_to_page(child_file, "2016-08-05T22:41:49-00:00", "Encourage")
  m = page_to_strzok(child_file, "2016-08-05T22:49:18-00:00", "No, I have it on eras. I can't read critically that way.")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-08-06T10:40:39-00:00", "I'm not sure. I had a lot of late back and forth with --Redacted-- on the --Redacted-- Told her --Redacted-- had done them but it was last night. Think it's that but I'm not certain. I'll ask him.")
  strzok_to_page(child_file, "2016-08-06T10:40:46-00:00", "Just emailed him and Jon")
  strzok_to_page(child_file, "2016-08-06T11:28:43-00:00", "And Jon and I are about to go ballistic, between --Redacted-- email (if you're frustrated at 12:09 and you haven't tried to call me at some point before then, part of this is on you) AND THE ABSOLUTE INABILITY GO SEND ANY EMAIL.\U0001f621")
  page_to_strzok(child_file, "2016-08-05T11:35:06-00:00", "Yeah, the email seemed a little unnecessarily harsh. I mean, it's not like we all haven't been working on it all damn day.")
  strzok_to_page(child_file, "2016-08-06T11:44:39-00:00", "And I can't send a f*cking email in response. ...")
  m = strzok_to_page(child_file, "2016-08-06T11:45:17-00:00", "Just pulled out eras, talking to 1500...")
  m.addnote("eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2016-08-06T11:46:19-00:00", "Hmm. I'm going to send you a low side email, see if it's just you.")
  strzok_to_page(child_file, "2016-08-06T11:46:53-00:00", "Thanks. Jon can't either. I can receive just fine")
  page_to_strzok(child_file, "2016-08-06T11:47:08-00:00", "Sending failed.")
  page_to_strzok(child_file, "2016-08-06T11:47:47-00:00", "I do wonder if it was a quasi-drunk email...")
  strzok_to_page(child_file, "2016-08-06T11:47:57-00:00", "Yup. Think it's a system - wide thing. Call 1500 and make them put in a ticket. Could we suck more?")
  strzok_to_page(child_file, "2016-08-06T11:49:28-00:00", "Might have been. And we're fine. Still")
  strzok_to_page(child_file, "2016-08-06T13:52:00-00:00", "Did you read the one pager --Redacted-- send to Andy, the --Redacted-- What on earth?\U00016f15")
  page_to_strzok(child_file, "2016-08-06T13:56:03-00:00", "Yes. Incomprehensible. I was utterly shocked that he is as impressed by him as he is.")
  page_to_strzok(child_file, "2016-08-06T13:56:40-00:00", "I had no idea what those lists are supposed to mean. No wonder Andy didn't remember reading it.\U0001f612")
  strzok_to_page(child_file, "2016-08-06T13:56:50-00:00", "I'm speechless. Did Andy say anything? I mean, it's bad. It's going to hurt --Redacted-- reputation.")
  page_to_strzok(child_file, "2016-08-06T13:57:08-00:00", "No, I haven't talked to him about it yet.")
  strzok_to_page(child_file, "2016-08-06T13:57:24-00:00", "God just avoid it and hope it goes away.")
  page_to_strzok(child_file, "2016-08-06T13:57:34-00:00", "But you'll recall, --Redacted-- said he gave it to Andy before. Andy probably glanced at it and threw it out.")

  # Page 332
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-06T13:57:45-00:00", "I've got to figure out a way to broach with --Redacted--.")
  strzok_to_page(child_file, "2016-08-06T13:58:29-00:00", "Oh. I thought this was the first time. This is what Eric wrote? It didn't say that in the email.")
  strzok_to_page(child_file, "2016-08-06T13:59:56-00:00", "And I don't know if I can mention to --Redacted-- I... --Redacted-- look, as a friend, I'd be cautious about what you send to the DD...he's got limited bandwidth and I'd be really selective?\n\n\nI mean, I don't know...it's really bad. I had to force myself to read all of it carefully.")
  strzok_to_page(child_file, "2016-08-06T14:15:12-00:00", "I wasn't there when --Redacted-- I said he had given it to Andy before")
  page_to_strzok(child_file, "2016-08-06T14:24:55-00:00", "No, on this, you can't say anything. Moffa and I were discussing. The most you can say is \"I'm not sure I found that as compelling as you did\" or something to that effect.")
  page_to_strzok(child_file, "2016-08-06T14:27:02-00:00", "Emails appear to be going through now.")
  strzok_to_page(child_file, "2016-08-06T14:30:45-00:00", "Yeah I don't know. I've got a different relationship with him than Jon does but I don't know if I can do much on this.")
  page_to_strzok(child_file, "2016-08-06T14:31:43-00:00", "I just don't think this one is the right one to bring up with him.")
  strzok_to_page(child_file, "2016-08-06T14:33:29-00:00", "That's fair. I just hate not mentioning it because it plays to/highlights some of --Redacted-- weaknesses (some true, some perceived). And it's absolutely the wrong time to bring it up.")
  page_to_strzok(child_file, "2016-08-06T14:34:27-00:00", "We've all talked to him a lot about it. He's now got to figure it out for himself.")
  strzok_to_page(child_file, "2016-08-06T14:36:39-00:00", "Yeah but wotking for him that calculation is different. And certainly much more so in the event I get the DAD job.")
  page_to_strzok(child_file, "2016-08-06T14:37:01-00:00", "Yeah, maybe.")
  strzok_to_page(child_file, "2016-08-06T14:37:08-00:00", "And that's weighing on me much more than I want to admit to you (or probably myself).")
  strzok_to_page(child_file, "2016-08-06T14:37:33-00:00", "Getting/not getting the job, not advising Bill")
  #page_to_strzok(child_file, "2016-08-06T14:38:09-00:00", "Jesus. You should read this. And Trump should go f himself.\n\nMoment in Convention Glare Shakes Up Khans\u1029 American Life http://nyti.ms/2aHuLE0")
  strzok_to_page(child_file, "2016-08-06T14:41:33-00:00", "I know. And as it stands, I'm going to have (and already do) a pretty tough time wiht it.\n\n5 months, Lisa. Out of 19 years. 5 months, because Giacalone was too busy interviewing to be there to SES board it earlier. There was literally NO difference in what I was doing day to day.")
  page_to_strzok(child_file, "2016-08-06T14:42:34-00:00", "I know, --Redacted-- I know. It's senseless and not fair, but you can't control it.")
  m = strzok_to_page(child_file, "2016-08-06T14:53:36-00:00", "God that's a great article.\U0001f621\U0001f61e\U0001f61e\u2764\n\nThanks for sharing.\n\nAnd F Trump.")
  m.tag("Hatred", "F Trump is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  
  # Page 333
  # OUTBOX == Page
  # INBOX == Strzok
  #page_to_strzok(child_file, "2016-08-06T14:55:00-00:00", "And maybe you're meant to stay where you are because you're meant to protect the country from that menace. To that end, read this:")
  page_to_strzok(child_file, "2016-08-06T14:55:19-00:00", "Trump\u2019s Enablers Will Finally Have to Take a Stand http://nyti.ms/2aFakry")
  strzok_to_page(child_file, "2016-08-06T15:04:43-00:00", "Thanks. It's absolutely true that we're both very fortunate.\n\nAnd of course I'll try and approach it that way. I just know it will be tough at times.\n\nI can protect our country at many levels, not sure if that helps...")
  page_to_strzok(child_file, "2016-08-06T15:05:51-00:00", "I know it will too. But it's just a job. It's not a reflection of your worth or quality or smarts.")
  strzok_to_page(child_file, "2016-08-06T15:28:50-00:00", "I really like this:\nHe appears to have no ability to experience reverence, which is the foundation for any capacity to admire or serve anything bigger than self, to want to learn about anything beyond self, to want to know and deeply honor the people around you.")
  page_to_strzok(child_file, "2016-08-06T15:30:59-00:00", "Sigh. That's the paragraph, upon reading, that caused me to want to send it to you.\U0001f636")
  page_to_strzok(child_file, "2016-08-06T17:24:11-00:00", "Okay, so maybe not the best national security president, but a genuinely good and decent human being.\n\nPresident Barack Obama on Feminism, Michelle, and His Daughters|Glamour http://www.glamour.com/story/glamour-exclusive-president-barack-obama-says-this-is-what-a-feminst-looks-like")
  strzok_to_page(child_file, "2016-08-06T17:34:25-00:00", "Yeah, I like him. Just not a fan of the weakness globally. Was thinking about what the administration will be willing to do re Russia. As I tried to focus Bill.")
  page_to_strzok(child_file, "2016-08-07T12:58:44-00:00", "Carl. Jon Moffa. --Redacted--")
  page_to_strzok(child_file, "2016-08-07T12:59:16-00:00", "You trust these people. You've just never tried to trust them with anything other than work.")
  strzok_to_page(child_file, "2016-08-08T00:10:09-00:00", "Well, I'll be here if you want to bounce questions tonight, and will be in early tomorrow...either way...")
  strzok_to_page(child_file, "2016-08-08T00:13:02-00:00", "Truly, will make you this offer - will input your changes as you finish reading what you haven't done yet. Plus, it's all the cyber stuff...your eyes will glaze over.")
  strzok_to_page(child_file, "2016-08-08T00:15:30-00:00", "But if you want me to kick you in the butt to motivate you to go in, let me know. You can be done with it by 9:30 or so...leave it and I can start inputting changes when I get in tomorrow morning.")
  strzok_to_page(child_file, "2016-08-08T12:31:32-00:00", "Hey head Andy called Jason")
  page_to_strzok(child_file, "2016-08-08T12:34:36-00:00", "Oh he did? So does he start today?")
  strzok_to_page(child_file, "2016-08-08T13:05:09-00:00", "Sounds like it - Jason was looking for me...talk to you in 30 or so")
  page_to_strzok(child_file, "2016-08-08T13:10:47-00:00", "K. Spoke to --Redacted-- about LHM FOIA timing. Remind me.")
  
  # Page 334
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-08T13:47:03-00:00", "K. Done. Stop by in a few?")
  strzok_to_page(child_file, "2016-08-08T14:18:12-00:00", "K heading up")
  strzok_to_page(child_file, "2016-08-08T15:14:52-00:00", "Hey no update yet, waiting on Moffa, he's in with Dina at mtg scheduled to end at 11...\U0001f612")
  strzok_to_page(child_file, "2016-08-08T15:28:43-00:00", "Hey talked to him, will let him fill you in. Internal joint cyber cd Intel piece for D, scenesetter for --Redacted-- brief, --Redacted-- directed all the cyber info be pulled. Doesn't make sense, at all. I'd think let Bill and Jim hammer out first, though it would be best for D to have it before the Wed WH session.")
  strzok_to_page(child_file, "2016-08-08T15:28:50-00:00", "But doesn't need you to step out")
  page_to_strzok(child_file, "2016-08-08T15:51:33-00:00", "Hey I didn't understand the above. I just tried your desk and cell.")
  strzok_to_page(child_file, "2016-08-08T15:53:52-00:00", "Sorry missed the first ring. Eating with Jason.")
  strzok_to_page(child_file, "2016-08-08T17:13:07-00:00", "Heading up")
  page_to_strzok(child_file, "2016-08-08T17:14:00-00:00", "Okay, but I need to talk to --Redacted-- in a little bit. Strategizing about you, actually.")
  #page_to_strzok(child_file, "2016-08-09T03:26:25-00:00", "He's not ever going to become president, right? Right?!")
  #strzok_to_page(child_file, "2016-08-09T10:08:45-00:00", "What prompted the Trump.comment last night?")
  page_to_strzok(child_file, "2016-08-09T10:09:28-00:00", "Just reading the times.")
  strzok_to_page(child_file, "2016-08-09T14:31:04-00:00", "Funny. --Redacted-- is here. Has a 1030 with Steinbach.\U0001f612")
  strzok_to_page(child_file, "2016-08-09T14:31:15-00:00", "Both of them are still in meetings.")
  page_to_strzok(child_file, "2016-08-09T15:54:35-00:00", "Ho boy.")
  strzok_to_page(child_file, "2016-08-09T16:20:31-00:00", "Just finished Bill wants another 5")
  page_to_strzok(child_file, "2016-08-09T16:21:50-00:00", "Im.coming down to talk to Bill.")
  page_to_strzok(child_file, "2016-08-09T17:00:17-00:00", "He said he spoke to mike, and that Mike said he supports you, so maybe you don't need to say anything. Just email randy.")
  page_to_strzok(child_file, "2016-08-09T17:01:22-00:00", "Yeah, yeah. Add it to the list. ;)")

  # Page 335
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-09T20:42:46-00:00", "Hey I ran into Bill, he wants to keep the brief smaller. His point (which I hadn't thought of) is Andy is more likely to share his internal thinking in front of a smaller group of people he knows rather than a larger group. Plus, fysa/atmospherics, Bull noted \"it's just so hard to get time with him.\" Whether true or not that's Bills perception. Thought you'd want to know")
  strzok_to_page(child_file, "2016-08-09T21:56:09-00:00", "OMG did you hear what Trump just said?")
  strzok_to_page(child_file, "2016-08-10T00:08:38-00:00", "Just sent you report with changes accepted")
  strzok_to_page(child_file, "2016-08-10T00:53:14-00:00", "And hey, do i need to tell Randy the board is Thurs?")
  page_to_strzok(child_file, "2016-08-10T00:57:58-00:00", "I'd shoot him an email.")
  page_to_strzok(child_file, "2016-08-10T10:10:52-00:00", "What Intelligence Briefings Can Tell Us About Candidates http://nyti.ms/2aUCaQB")
  strzok_to_page(child_file, "2016-08-10T10:36:38-00:00", "Hey I did not mention to Jon Andy's preference for more detail. Would you send an email to him, Bill and I saying same, e.g., don't care who, but need to be able to deep dive?\n\nThen Jon and I can meet with Bill and decide.\n\nUnless you want to handle differently.")
  page_to_strzok(child_file, "2016-08-10T10:45:38-00:00", "That's fine.")
  m = page_to_strzok(child_file, "2016-08-10T10:49:21-00:00", "You can imsg again if you had more to say.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2016-08-10T11:35:59-00:00", "About to drive. Talk in a sec - work?")
  page_to_strzok(child_file, "2016-08-10T11:53:51-00:00", "Going to go sit in on the morning brief. Carl said it's s good one and I shouldn't miss it. Ttyl.")
  page_to_strzok(child_file, "2016-08-10T15:34:14-00:00", "Been talking to --Redacted-- for like an hour. Was a really good talk.")
  strzok_to_page(child_file, "2016-08-10T15:37:23-00:00", "Can I stop by? TON to tell you")
  m = strzok_to_page(child_file, "2016-08-10T19:46:32-00:00", "I remember what it was. Toscas already told Stu Evans everything. --Redacted-- called to set up a meeting, he already knew --Redacted--\n\nThanks nsd...")
  m.addnote("nsd - FBI National Security Division")
  strzok_to_page(child_file, "2016-08-10T21:39:42-00:00", "Hey call me re D brief. Moffa and I had the immediate same reaction")
  strzok_to_page(child_file, "2016-08-10T23:52:58-00:00", "In fairness, from the email i's not clear what wf is proposing to do")
  strzok_to_page(child_file, "2016-08-11T00:13:09-00:00", "And hey, I read that wfo email again and it's just a press inquiry and confusion/suggestion --Redacted-- might be linked to it...not consideration of opening a case.")
  page_to_strzok(child_file, "2016-08-11T00:33:54-00:00", "Got it. Yeah, the press inquiry was brief at wrap. Didn't mention to ddm")
  page_to_strzok(child_file, "2016-08-11T00:33:58-00:00", "Dd.")

  # Page 336
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-11T00:34:30-00:00", "Oh, and funny. Ran into --Redacted-- AGAIN this afternoon going to the briefing. He peeled off to Mikes. Not sure if he had to reschedule from yesterday.")
  strzok_to_page(child_file, "2016-08-11T00:34:39-00:00", "He looked sheepish....")
  page_to_strzok(child_file, "2016-08-11T00:35:19-00:00", "Well, he can't rely on quality...")
  strzok_to_page(child_file, "2016-08-11T00:46:22-00:00", "--Redacted-- went crazy stalky on me to figure out if there was anything to the inquiry. She IS persistent.")
  #strzok_to_page(child_file, "2016-08-11T00:48:15-00:00", "So. You come up with a codename? --Redacted--")
  page_to_strzok(child_file, "2016-08-11T00:51:26-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-08-11T00:53:00-00:00", "Ooh. I like it \n\nWant me to send to --Redacted--")
  page_to_strzok(child_file, "2016-08-11T00:53:39-00:00", "If you want.")
  #strzok_to_page(child_file, "2016-08-11T00:53:46-00:00", "Why --Redacted-- (other than it sounds badass, and you came up with it\U0001f636)")
  #page_to_strzok(child_file, "2016-08-11T00:54:24-00:00", "Trying to think of something --Redacted-- without being obvious.")
  #strzok_to_page(child_file, "2016-08-11T00:56:56-00:00", "--Redacted--")
  #strzok_to_page(child_file, "2016-08-11T00:57:27-00:00", "OMG I CANNOT BELIEVE WE ARE SERIOUSLY LOOKING AT THESE ALLEGATIONS AND THE PERVASIVE CONNECTIONS")
  #strzok_to_page(child_file, "2016-08-11T00:57:41-00:00", "What the hell has happened to our country!?!?!??")
  strzok_to_page(child_file, "2016-08-11T11:13:28-00:00", "Is Baker around today? I need 5 minutes with him. You can cone ifnyou want. I want to talk to him about the CI brief, specifically the --Redacted--")
  strzok_to_page(child_file, "2016-08-11T11:14:30-00:00", "That might also be something appropriate to ask NSD. Thoughts?")
  page_to_strzok(child_file, "2016-08-11T11:16:21-00:00", "I'll think about it. I bet baker can handle.")
  strzok_to_page(child_file, "2016-08-11T11:18:15-00:00", "Thanks.\n\nWill read shortly, hustling to get out the door. --Redacted--")
  page_to_strzok(child_file, "2016-08-11T16:06:05-00:00", "Andy had a wry smile when I saw me waiting for him. Of course I have no idea what that means.")
  strzok_to_page(child_file, "2016-08-11T16:18:22-00:00", "We decided to take --Redacted-- to lunch instead.\U0001f61c")
  strzok_to_page(child_file, "2016-08-11T16:18:42-00:00", "Still have room for you. ...")
  page_to_strzok(child_file, "2016-08-11T16:18:47-00:00", "Jerkies.")
  page_to_strzok(child_file, "2016-08-11T16:19:10-00:00", "I'm still waiting for Andy to come out of his meeting so I can get the news!")
  page_to_strzok(child_file, "2016-08-11T16:19:27-00:00", "Can I call Jon to buy you a drink if I get it?\U0001f60a")

  # Page 337
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-11T16:20:08-00:00", "Ha. Yes.")
  strzok_to_page(child_file, "2016-08-11T16:21:44-00:00", "Lost Moffa somewhere. Added --Redacted--")
  page_to_strzok(child_file, "2016-08-11T16:22:16-00:00", "How could you lose Moffa? He's like 6 feet tall?")
  strzok_to_page(child_file, "2016-08-11T16:23:23-00:00", "He disappeared")
  page_to_strzok(child_file, "2016-08-11T16:56:50-00:00", "Congratulations, --Redacted-- You're the new DAD of the Counterintelligence Division. --Redacted--")
  page_to_strzok(child_file, "2016-08-11T16:56:56-00:00", "Don't tell...")
  strzok_to_page(child_file, "2016-08-11T16:58:36-00:00", "--Redacted-- 1pm then follow on with Bill. Doj at 4 then Baker 430.")
  page_to_strzok(child_file, "2016-08-11T16:59:14-00:00", "Obviously, don't tell Bill. I'll call you when I'm back.")
  page_to_strzok(child_file, "2016-08-11T20:30:43-00:00", "Can you and --Redacted-- come up and see me when you are done?")
  page_to_strzok(child_file, "2016-08-11T20:31:06-00:00", "Is --Redacted-- with you? Can you please come up here?")
  strzok_to_page(child_file, "2016-08-11T20:31:49-00:00", "A) whew. I did\U0001f636\nB) walking to see JB. She is still in 4017")
  strzok_to_page(child_file, "2016-08-11T20:36:48-00:00", "We're in Jims SCIF")
  page_to_strzok(child_file, "2016-08-11T22:58:37-00:00", "On with rybicki.")
  strzok_to_page(child_file, "2016-08-11T23:20:02-00:00", "Hey just swung by your office on the way out...you close by? Otherwise will head out")
  page_to_strzok(child_file, "2016-08-11T23:20:14-00:00", "I'm in kortan")
  page_to_strzok(child_file, "2016-08-11T23:21:07-00:00", "Coming with herring, you need to leave.")
  strzok_to_page(child_file, "2016-08-11T23:21:36-00:00", "Going towards --Redacted-- office")
  m = strzok_to_page(child_file, "2016-08-11T23:21:47-00:00", "Sorry, to nslb")
  m.addnote("nslb - National Security Law Branch at DOJ")
  strzok_to_page(child_file, "2016-08-11T23:21:55-00:00", "I hear you")
  page_to_strzok(child_file, "2016-08-12T11:46:09-00:00", "Do you get a car as DAD? What time will you have to be there?")
  strzok_to_page(child_file, "2016-08-12T12:00:49-00:00", "I do get a car. I don't know if I'm authorized to take it home. Obviously will check on that. 745 first meeting, so 730...")
  strzok_to_page(child_file, "2016-08-12T12:01:39-00:00", "Hey Jon and I talked around and round on these briefs, whether to leave him and me or give to --Redacted-- Do you think Andy would have a preference? Do you?")

  # Page 338
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-12T12:01:50-00:00", "I think give to --Redacted--")
  strzok_to_page(child_file, "2016-08-12T12:01:58-00:00", "Need to get a final answer to --Redacted-- this morning.")
  page_to_strzok(child_file, "2016-08-12T12:02:05-00:00", "I think it protects you guys better.")
  strzok_to_page(child_file, "2016-08-12T12:02:11-00:00", "Would Andy object?")
  page_to_strzok(child_file, "2016-08-12T12:04:08-00:00", "To --Redacted-- No, I can't imagine he would.")
  #strzok_to_page(child_file, "2016-08-12T12:04:51-00:00", "Bill sent an email asking to see me at 9 or 11... have a --Redacted-- mtg at 9, so 11 it is")
  strzok_to_page(child_file, "2016-08-12T13:09:38-00:00", "Hi. Bill pulled me aside to say he was told the board went the way he wanted, but still needs the D's blessing")
  page_to_strzok(child_file, "2016-08-12T13:10:03-00:00", "Yay.\U0001f60a")
  strzok_to_page(child_file, "2016-08-12T14:57:58-00:00", "And that's SUPER aggravating about --Redacted-- flipping\U0001f621")
  page_to_strzok(child_file, "2016-08-12T15:00:24-00:00", "Yeah whatever.")
  page_to_strzok(child_file, "2016-08-12T15:01:05-00:00", "Hey you NEED to pull that 302 before you leave for the day.")
  strzok_to_page(child_file, "2016-08-12T15:31:22-00:00", "Come down. To my office for lunch and I'll pull it now")
  strzok_to_page(child_file, "2016-08-12T15:31:39-00:00", "And I'm going to blow your mind")
  strzok_to_page(child_file, "2016-08-12T15:57:39-00:00", "Let me know when you're done, we can eat")
  strzok_to_page(child_file, "2016-08-12T15:58:03-00:00", "And/or discuss 302s, as needed")
  strzok_to_page(child_file, "2016-08-12T16:40:29-00:00", "Hey I have a 130 with Bill and would like to eay before then. Should I wait for you? Maybe go at 1 if I haven't heard from you?")
  page_to_strzok(child_file, "2016-08-12T16:47:12-00:00", "I don't have to grab anything bc now I need to write up an email to the d explaining all of this.")
  strzok_to_page(child_file, "2016-08-12T19:29:01-00:00", "You around? I NEED to talk to you before I go")
  strzok_to_page(child_file, "2016-08-13T00:38:33-00:00", "Just talked to --Redacted--. Indications Guccifer 2.0 claiming massive hack of Congress, or at least Dems. All on line now.\n\nSigh. Well he's going to feel super defensive, because as you pointed out, he was there all week. You going to stew until you talk? If so, might as well get it out...")
  strzok_to_page(child_file, "2016-08-13T00:52:43-00:00", "Cells and private emails for House Dems")
  page_to_strzok(child_file, "2016-08-13T01:03:03-00:00", "God, did you read some of the comments on that article?!")
  strzok_to_page(child_file, "2016-08-13T01:32:54-00:00", "And the comments in the Smoking Gun article? Can't get them to load....")

  # Page 339
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-13T11:04:47-00:00", "Im going to have --Redacted-- do his CI brief presentation for me and Jon and --Redacted-- on Mon afternoon. I want to do another one Tues Am for at least Bill. You think add you, Jim Baker? I want both rank and thoughtfulness for feedback. Plus repetitions for him.")
  page_to_strzok(child_file, "2016-08-13T11:21:21-00:00", "Yes. I'll be there.")
  strzok_to_page(child_file, "2016-08-13T13:02:03-00:00", "Hey read the email I just sent. I did not include OPA or oca on the distro")
  page_to_strzok(child_file, "2016-08-13T13:11:55-00:00", "There's no debate. I'm going to forward to kortan. God, makes me want to tell state to go f it.")
  strzok_to_page(child_file, "2016-08-13T13:14:29-00:00", "Yep! You think we should have commented, if only to rebut States \"expectation of interagency coordination\" crap?")
  strzok_to_page(child_file, "2016-08-13T13:22:29-00:00", "--Redacted-- And yeah, States BS just makes me want to include those additional 302s. But that's just vindictiveness talking.")
  page_to_strzok(child_file, "2016-08-14T01:13:27-00:00", "But see, this article so rings true that then I think the --Redacted-- Inside the Failing Mission to Save Donald Trump From Himself http://nyti.ms/2b5WSNA")
  page_to_strzok(child_file, "2016-08-14T10:35:59-00:00", "This was very interesting.\n\nThe Decline of Unions and the Rise of Trump http://nyti.ms/2bc7a1U")
  page_to_strzok(child_file, "2016-08-14T10:41:11-00:00", "God this makes me so angry.\n\nDonald Trump Is Making America Meaner http://nyti.ms/2b6gG38")
  strzok_to_page(child_file, "2016-08-14T10:57:57-00:00", "I'm not!\U0001f636\n\nIsaw but didn't read the first article.")
  page_to_strzok(child_file, "2016-08-14T10:58:46-00:00", "Just about their force in moderating the political debate. It was interesting.")
  strzok_to_page(child_file, "2016-08-14T11:00:46-00:00", "And I am worried about what Trump is encouraging in our behavior. The things that made me proud about our tolerance for dissent - what makes us different from Sunnis and Shias losing each other up - is disappearing.")
  page_to_strzok(child_file, "2016-08-14T11:01:23-00:00", "That's what that last article is all about.")
  #strzok_to_page(child_file, "2016-08-14T11:01:54-00:00", "I'm worried about what happens if HRC is elected.\n\nAnd perfect, another excessive heat warning day.")
  page_to_strzok(child_file, "2016-08-14T20:06:22-00:00", "Just spoke to --Redacted-- She and --Redacted-- and Jim in some mandatory leadership training tomorrow --Redacted--")
  strzok_to_page(child_file, "2016-08-14T20:07:55-00:00", "Np. We'll get done whatever needs doing. Primarily QC, no? --Redacted--")
  page_to_strzok(child_file, "2016-08-14T20:17:55-00:00", "No, all the work of pulling out --Redacted-- first.")
  strzok_to_page(child_file, "2016-08-14T20:18:56-00:00", "Well, Jon and I can do that.\n\nI didn't see the --Redacted--")
  strzok_to_page(child_file, "2016-08-14T20:24:10-00:00", "Anything other than scrub 302s for agency equities?")
  page_to_strzok(child_file, "2016-08-14T20:25:53-00:00", "I don't think scrub. Just remove the ones that are their employees.")

  # Page 340
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-14T20:27:02-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-08-14T20:36:27-00:00", "In 302s, you mean? I just think no. But we can discuss. --Redacted--")
  m = strzok_to_page(child_file, "2016-08-14T21:20:01-00:00", "Hey. So Rybicki just emailed me about briefing D on --Redacted-- tomorrow at 330. If not then, Wed. I said we could do either. Dont know Andy's availability / desire to svtc in. Assume you can, right?")
  m.addnote("svtc - Secure VIdeo Teleconference")
  page_to_strzok(child_file, "2016-08-14T21:23:09-00:00", "Andy not going to. Either is fine for me.")
  strzok_to_page(child_file, "2016-08-14T21:25:25-00:00", "Jim proposing D dd add ead GC Trisha --Redacted-- you him bill me jon")
  page_to_strzok(child_file, "2016-08-14T21:27:55-00:00", "Fine, I suppose. Don't love add obviously, but so be it.")
  strzok_to_page(child_file, "2016-08-14T22:56:30-00:00", "And uh, yeah, I then forgot to actually ADD him to the distro.\n\nSo I just forwarded to him. Good work, Pete.\U0001f612")
  strzok_to_page(child_file, "2016-08-14T23:34:36-00:00", "So it's a little weird to me that Jason, a subordinate a week ago, will be the one discussing with Toscas amd OLA as well as with Steinbach and everyone else at the 8... fine, I guess, but weird...")
  strzok_to_page(child_file, "2016-08-15T10:29:55-00:00", "I want to believe the path you threw out for consideration in Andy's office - that there's no way he gets elected - but I'm afraid we can't take that risk. It's like an insurance policy in the unlikely event you die before you're 40...")
  page_to_strzok(child_file, "2016-08-15T10:41:11-00:00", "I really should take off the whole damn day.\U0001f621")
  strzok_to_page(child_file, "2016-08-15T10:48:42-00:00", "So go ahead! We'll get the production done.\n\nI'd obviously love to have you at the D brief, but if not, I'll stop by and give you an in-person debrief. --Redacted--")
  page_to_strzok(child_file, "2016-08-15T10:51:45-00:00", "Oh, crap, has that been scheduled?")
  strzok_to_page(child_file, "2016-08-15T11:15:01-00:00", "Not that I've seen. JR said he'd get with --Redacted-- this morning")
  page_to_strzok(child_file, "2016-08-15T11:17:03-00:00", "Are you still acting DAD?")
  strzok_to_page(child_file, "2016-08-15T11:17:28-00:00", "No. Why?")
  strzok_to_page(child_file, "2016-08-15T11:18:05-00:00", "I ask because that will change whenever board is official")
  strzok_to_page(child_file, "2016-08-15T12:59:00-00:00", "OMG this production alone is going to kill my inbox....")
  strzok_to_page(child_file, "2016-08-15T21:16:52-00:00", "Going to talk to --Redacted-- Call me here when you're done...\U0001f60a")
  page_to_strzok(child_file, "2016-08-15T21:48:55-00:00", "Herring here.")

  # Page 341
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-15T21:51:03-00:00", "K. Want me to hold off?")
  page_to_strzok(child_file, "2016-08-15T21:54:47-00:00", "You can come, just have something you are here to talk about.")
  strzok_to_page(child_file, "2016-08-15T22:01:27-00:00", "Hey I want to talk about feedback from brief and other stuff. --Redacted--")
  strzok_to_page(child_file, "2016-08-15T22:05:22-00:00", "Or, I can walk up and find you left.\U0001f612\n\nGive me a shout when you get back.")
  page_to_strzok(child_file, "2016-08-16T00:43:35-00:00", "Changing topics a little, but I'm really excited about all the \"whoa that was quick\" congratulatory emails...")
  strzok_to_page(child_file, "2016-08-16T00:45:07-00:00", "Sigh. Yeah, I know. I need to hit the right tone. Probably just, thanks very much, tremendous opportunity, I'm looking forward to it.")
  strzok_to_page(child_file, "2016-08-16T10:05:29-00:00", "Nice email from Bowdich last night \U0001f60a")
  strzok_to_page(child_file, "2016-08-16T11:21:20-00:00", "When's your WH thing on Thurs? You going to be too busy with prep?")
  page_to_strzok(child_file, "2016-08-16T11:21:58-00:00", "No. No prep really.")
  strzok_to_page(child_file, "2016-08-16T11:21:20-00:00", "Ooh. Ok, so I think any work. Probably Wed so I don't have to worry about the 1:00 cd mtg")
  page_to_strzok(child_file, "2016-08-16T11:33:06-00:00", "So your first meeting is at 745 with whom, Bill?")
  strzok_to_page(child_file, "2016-08-16T11:35:06-00:00", "730 with my Special Assistant. Who im.not convinced I need")
  strzok_to_page(child_file, "2016-08-16T11:35:45-00:00", "And based on my Boston contacts, I rold --Redacted-- not to select.\U0001f612")
  page_to_strzok(child_file, "2016-08-16T11:36:01-00:00", "I also don't think you need one, but give it a month before you decide.")
  strzok_to_page(child_file, "2016-08-16T22:40:19-00:00", "I'm strongly opposed to making any more copies for Congress. We limited on purpose, After careful consideration. If they let any particular committee get the copy, tough. Let them sort it out.")
  strzok_to_page(child_file, "2016-08-16T23:08:20-00:00", "Can you talk briefly?\n\nWhat time do these need to be done? How many copies? Stop worrying / making calls about who should do it. I will have 4-5 of my people come in early. Is complete by 10 OK?")
  page_to_strzok(child_file, "2016-08-16T13:14:17-00:00", "--Redacted-- is doing it now, --Redacted-- is headed back in. I'm going to join shortly.")
  strzok_to_page(child_file, "2016-08-17T03:01:26-00:00", "Hey was --Redacted-- or Trisha on --Redacted-- update from Jim? Don't want Bill blindsided in the morning")
  page_to_strzok(child_file, "2016-08-17T03:06:37-00:00", "Trisha and --Redacted--")
  strzok_to_page(child_file, "2016-08-17T03:07:23-00:00", "I'll ask --Redacted--")

  # Page 342
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-17T10:28:37-00:00", "An article to share: Trump shakes up campaign, demotes top adviser\nTrump shares up campaign, demotes top adviser\nhttp://wapo.st/2bzAUGD")
  strzok_to_page(child_file, "2016-08-17T10:29:25-00:00", "Just reading it")
  strzok_to_page(child_file, "2016-08-17T10:33:38-00:00", "Re last email and text last night, I'm going to stop asking. I want to be in the loop, also want Bill in the loop, but that's not my job.\nA) makes me feel like a whiny b*tch\nB) --Redacted--\nC) need to talk to --Redacted-- about making sure her clients are in the loop. Thats part of her job, not yours")
  page_to_strzok(child_file, "2016-08-17T10:35:51-00:00", "Sigh.\n\nThe story behind the \u2018American Dream\u2019 photo at West Point that went viral - The Washington Post\nhttps://www.washingtonpost.com/news/checkpoint/wp/2016/05/25/the-story-behind-the-american-dream-photo-at-west-point-what-went-viral/?tid=hybrid_experimentrandomcheckpoint_2_na")
  page_to_strzok(child_file, "2016-08-17T10:38:29-00:00", "--Redacted-- You can ask, that doesn't bother me.")
  strzok_to_page(child_file, "2016-08-17T10:47:25-00:00", "Thats fair.\n\nI think sometimes it's not directed (or not meant to be directed) at you, it's expressing frustration. I want to vent and you're the only place (because of both friendship and shared knowledge of the email) that I can.\n\nI'm aware you probably hear me in even those times and either don't need me to tell you what I'm telling you what I'm telling you, feel like I'm asking you do do something about it, or both.\n\nAnd sometimes, I'm just looking for a little validation. Yes, the Andy - George dynamic did cause some problems. Yes, Jim in particular isn't always goot at email distro. Thats all.\n\nAnyway, all of this probably better talked about it person, or not at all.\n\nI'm tired of it, and I hate myself during it (and I then remember you saying, well, at least you're seeing it in yourself. So change)")
  strzok_to_page(child_file, "2016-08-17T10:51:14-00:00", "Thank you for the article \U0001f636")
  page_to_strzok(child_file, "2016-08-17T10:51:33-00:00", "Pete.")
  strzok_to_page(child_file, "2016-08-17T10:51:39-00:00", "Yeah I may be overthinking")
  page_to_strzok(child_file, "2016-08-17T10:53:52-00:00", "I hear you above, but I think I know the difference between when you are just \"venting\" or wanting to be validated, and when you're just being unreasonable and taking your sh*t out on me.")
  
  # Page 343
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-17T10:56:57-00:00", "I agree. Yesterday --Redacted-- was the latter, asking for the email last night was the former. And as you noted, probably ordinarily ok to gripe about it, but not last night. --Redacted--")
  strzok_to_page(child_file, "2016-08-17T10:57:50-00:00", "And I don't mean to cut you off if you have more to say on the topic.")
  m = strzok_to_page(child_file, "2016-08-17T11:02:31-00:00", "Re the email, resisted the urge to tell him, well, Randys briefing it may be an insider threat, he's getting that from somewhere. Will sort it out today. Thanks for the heads up.\n\nAlso got --Redacted-- I think to get Moffa an invite for all the IPC stuff going on with election threat. Talked with Moffa at length about it beforehand. Right now fbi being represented entirely by Cyber. --Redacted-- asked CD1, and they punted to C3S. I'm certain --Redacted-- didn't realize th broader implications.")
  m.addnote("C3S - Cyber Counterintelligence Coordination")
  strzok_to_page(child_file, "2016-08-17T11:03:13-00:00", "The sigh to you getting it, not some stupid IPC process.")
  page_to_strzok(child_file, "2016-08-17T11:10:37-00:00", "Totally. Moffa the right guy. Let me know if you need help. Easy fix by --Redacted-- and I.")
  strzok_to_page(child_file, "2016-08-17T11:03:13-00:00", "No, I think it's fixed. As normal, we're our own worst enemy")
  m = strzok_to_page(child_file, "2016-08-17T13:46:19-00:00", "Just met with oca team. All set. (No jinxes)")
  m.addnote("oca - Office of Congressional Affairs ??")
  page_to_strzok(child_file, "2016-08-17T20:46:41-00:00", "Hey, headed down to B2 now")
  strzok_to_page(child_file, "2016-08-17T20:47:27-00:00", "K see you there")
  page_to_strzok(child_file, "2016-08-17T20:47:28-00:00", "No, I'm not. Kortan just stopped me in the hall")
  page_to_strzok(child_file, "2016-08-17T20:49:27-00:00", "OK leaving now")
  strzok_to_page(child_file, "2016-08-18T10:46:05-00:00", "--Redacted-- I have svtc with Brits at 9, 302 party at 10, you have lunch with either your friend or me and --Redacted-- at 1130, I have my 1 cd exec mtg, you have WH....suppose we could go at the end of the day, I can take --Redacted--")
  m = strzok_to_page(child_file, "2016-08-18T19:45:21-00:00", "What time is deadline for state TPs to Jim?")
  m.addnote("TPs - Talking Points")
  m = strzok_to_page(child_file, "2016-08-18T23:46:10-00:00", "Can you eras? Just clear email. That will be enough")
  m.addnote("eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2016-08-18T23:49:36-00:00", "I do wonder if they are waiting to get briefs for the email handling classified information mess to die down before they get the briefings.")
  strzok_to_page(child_file, "2016-08-18T23:52:05-00:00", "I can't see that. They're either worried about --Redacted-- or don't really need them.")
  #page_to_strzok(child_file, "2016-08-19T00:53:28-00:00", "Ukraine Releases More Details on Payments for Trump Aide http://nyti.ms/2breAOV")

  # Page 344
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-19T10:26:19-00:00", "Just sent you i think a good way for --Redacted-- to proceed. --Redacted--")
  page_to_strzok(child_file, "2016-08-19T10:54:02-00:00", "Should I forward leak article to baker and rybicki? The Powell stuff was in her 302 and lhm, right? Did we turn over his 302?")
  strzok_to_page(child_file, "2016-08-19T11:04:50-00:00", "Sure, but note that odd sourcing. It was in her 302; I'd want to double check if we turned over his 302, though I'm almost certain we did.\n\nAnd I'd bet the unnamed source is almost certainly Powell.")
  page_to_strzok(child_file, "2016-08-19T11:06:23-00:00", "I'm just going to forward your email, so the sourcing ref is in there.")
  strzok_to_page(child_file, "2016-08-19T17:59:16-00:00", "Sorry I have 20 minutes to get my shit together for dni")
  strzok_to_page(child_file, "2016-08-19T18:00:09-00:00", "Shouldn't take that log. Let me pull data, should take 10 minutes")
  strzok_to_page(child_file, "2016-08-19T18:08:38-00:00", "Good side effect of briefing this a million times.")
  add_event( child_file, "2016-08-19T19:30:00-00:00", "2016-08-19T20:30:00-00:00", "Strzok meets with DNI Clapper", "Times approximate, mentioned in text messages, page 344", EVENT_TYPE_DNI)
  page_to_strzok(child_file, "2016-08-19T20:50:08-00:00", "Might skip prep, we'll see. How'd it go?")
  strzok_to_page(child_file, "2016-08-19T20:53:05-00:00", "Ooh god I love that answer :)\n\nReally well. He's calling D, I left message for Rybicki. Will call you when I get back...")
  strzok_to_page(child_file, "2016-08-19T20:58:52-00:00", "Ok, I REALLY love that answer \U0001f636")
  page_to_strzok(child_file, "2016-08-19T20:59:39-00:00", "Why calling D? To say you guys are awesome? Get your thoughts?")
  strzok_to_page(child_file, "2016-08-19T21:22:36-00:00", "Just got to hq")
  page_to_strzok(child_file, "2016-08-19T21:22:45-00:00", "Sheesh.")
  strzok_to_page(child_file, "2016-08-19T22:54:33-00:00", "Where's this coming from?\n\nFirst on CNN: Feds investigate Manafort firm as part of Ukraine probe - CNNPolitics.com\nhttp://www.cnn.com/2016/08/09/paul-manafort-donald-trump-ukraine/index.html")
  page_to_strzok(child_file, "2016-08-19T23:12:31-00:00", "Yeah, don't know. Heard or saw something about it yesterday too. At wrap Tues or Wed I think.")
  strzok_to_page(child_file, "2016-08-19T23:14:28-00:00", "Oh well. --Redacted--")
  strzok_to_page(child_file, "2016-08-20T01:13:46-00:00", "And thanks for forwarding the other email. I'm disappointed that --Redacted-- Jon and I don't have the opportunity to input, where --Redacted-- and --Redacted-- and Jason do, but I'm letting go and not worrying about it or letting it bother me. Bill has not forwarded, but I think he may assume that since 80 people are on the distro, we got it.\n\nI'm angriest for --Redacted-- because of what --Redacted-- and --Redacted-- did w/r/t her and going direct with Jim.")

  # Page 345
  # OUTBOX == Page
  # INBOX == Strzok
  m = strzok_to_page(child_file, "2016-08-20T11:20:05-00:00", "And a favor, please - to the extent there are follow on relevant Kendall/MYE emails (and there may not be), please forward if appropriate. Bill has told Jon and me that he isn't typically reading them, and is relying on us to flag any issue he needs to weigh in on. Given the large distro of Jim's emails, I'm willing to bet he doesn't notice we're not on there. I will discuss with him next week as well. Thanks")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-08-20T11:47:50-00:00", "--Redacted-- Jon and Bill and I had a group rant about these. --Redacted--")
  page_to_strzok(child_file, "2016-08-21T20:38:37-00:00", "Dude, I bcc'ed. But on well.")
  strzok_to_page(child_file, "2016-08-21T20:39:10-00:00", "That's why I went to you and --Redacted--....")
  page_to_strzok(child_file, "2016-08-22T16:57:10-00:00", "Meeting is at 1:15 now.")
  page_to_strzok(child_file, "2016-08-22T17:04:49-00:00", "Going to talk to --Redacted-- now.")
  page_to_strzok(child_file, "2016-08-22T17:04:56-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-08-22T18:04:36-00:00", "I prefer --Redacted--)")
  page_to_strzok(child_file, "2016-08-23T01:03:57-00:00", "Yeah.\n\nSorry, I'm --Redacted-- reading the IG report. It's really dry...")
  strzok_to_page(child_file, "2016-08-23T01:04:53-00:00", "Eep. Yeah, that's pretty terrible. Put that trash down. ;)")
  page_to_strzok(child_file, "2016-08-23T01:06:13-00:00", "I can't. This week is going to be terrible. I need to get crap done where I can...")
  strzok_to_page(child_file, "2016-08-23T23:37:59-00:00", "Hey I'm not going to that training tomorrow, I will hit a later session. --Redacted--")
  page_to_strzok(child_file, "2016-08-24T21:54:32-00:00", "Good thing you skipped the implicit bias training, it was apparently AWFUL. So bad, folks are likely to go back to the DAG to object to it.")
  strzok_to_page(child_file, "2016-08-24T22:28:45-00:00", "Hi. Still going with Bill. Stepped out to tell you....\U0001f636")
  page_to_strzok(child_file, "2016-08-24T22:29:31-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-08-24T23:36:46-00:00", "--Redacted-- Are we in thunderdome tomorrow? Have audio/video for briefing. Can --Redacted-- get there 15 min early with AV guy? Coordinate thru --Redacted--")
  page_to_strzok(child_file, "2016-08-24T23:37:38-00:00", "Ooh. A/V time.")

  # Page 346
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-24T23:38:56-00:00", "We can be wherever you want. Thunder dome is fine. Early is fine. He should be able to log on to his fbi net terminal and do whatever he needs. I'll send an email to --Redacted-- now letting her know we will need a/V.")
  strzok_to_page(child_file, "2016-08-24T23:38:57-00:00", "No. Not worth it.\n\nYep! Everyone loves a video, even if the subj is wildly uncooperative. Great tech work, shows competence and urgency. Plus --Redacted-- is kind of a douche.")
  strzok_to_page(child_file, "2016-08-24T23:39:37-00:00", "Thank you\n\nWe can do video in his office but figure that would be weird/awkward....")
  strzok_to_page(child_file, "2016-08-24T23:40:09-00:00", "Am I still buying you and --Redacted-- lunch tomorrow?\U0001f60a\U0001f60a\U0001f60a")
  page_to_strzok(child_file, "2016-08-24T23:40:34-00:00", "Will probably depend on his schedule. It's his only day in the office.")
  page_to_strzok(child_file, "2016-08-25T14:08:20-00:00", "I'm here. Also, let's meet at my ofc at 1130 for lunch. --Redacted-- is still good.")
  strzok_to_page(child_file, "2016-08-25T14:39:47-00:00", "No to --Redacted--, have been talking to Legat Canberra")
  strzok_to_page(child_file, "2016-08-25T19:30:56-00:00", "What do you have after --Redacted-- brief? --Redacted-- \U0001f636")
  page_to_strzok(child_file, "2016-08-25T19:33:14-00:00", "Oh crap. I'm sorry. Been in back to back mtgs. Have a mtg with kerry sleeper now.")
  strzok_to_page(child_file, "2016-08-26T02:13:49-00:00", "It's ok. It's nothing compared to your night.\n\nAnd Gowdy is really starting to p*ss me off. I'm going to need to stop the news.")
  page_to_strzok(child_file, "2016-08-26T15:29:45-00:00", "302 and lhm going to be further delayed. I love my job.")
  strzok_to_page(child_file, "2016-08-26T15:34:48-00:00", "Sweet Jesus. OGA?")
  m = page_to_strzok(child_file, "2016-08-26T16:25:27-00:00", "And just had an hour long conversation with --Redacted-- re nsls. It's really never going to end...")
  m.addnote("nsls - National Security Letters?")
  strzok_to_page(child_file, "2016-08-26T16:41:51-00:00", "What? Trnasparency crap?")
  strzok_to_page(child_file, "2016-08-26T16:42:07-00:00", "Good lord. Talk about an unexpected and unpleasant blast from the past....")
  #strzok_to_page(child_file, "2016-08-26T16:42:40-00:00", "Just went to a southern Virginia Walmart. I could SMELL the Trump support....")
  page_to_strzok(child_file, "2016-08-26T16:54:18-00:00", "Yup. Out to lunch with --Redacted-- We both hate everyone and everything.")
  strzok_to_page(child_file, "2016-08-26T17:02:52-00:00", "I want to be there and hate with you, or charm you back to happy\n\nLooked for the two trump yard signs I saw on the way out to take a picture, but couldn't see them")
  page_to_strzok(child_file, "2016-08-26T18:43:35-00:00", "Going to another meeting. Glad you're having a good time.")
  page_to_strzok(child_file, "2016-08-26T20:49:14-00:00", "Actually, Jon Moffa just made me chuckle. First time all day. I like that kid.")
  strzok_to_page(child_file, "2016-08-26T20:50:09-00:00", "What'd he say?")

  # Page 347
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-26T20:51:12-00:00", "Just riffing on the hot mess that is our country.")
  strzok_to_page(child_file, "2016-08-26T20:52:28-00:00", "Yeah....it's scary real down here")
  page_to_strzok(child_file, "2016-08-27T20:07:01-00:00", "Have to go into work tomorrow afternoon. Have a --Redacted-- which has changed in scope that I need to write prep for.\U0001f612")
  strzok_to_page(child_file, "2016-08-27T20:18:46-00:00", "God that sucks. Are you --Redacted-- only backup?")
  strzok_to_page(child_file, "2016-08-27T20:19:39-00:00", "I know we've discussed before, but he's got to start developing subordinates.\U0001f61e")
  page_to_strzok(child_file, "2016-08-27T20:20:50-00:00", "--Redacted-- would normally be his true backup, but she's out until Tuesday or Wednesday.")
  strzok_to_page(child_file, "2016-08-27T20:36:07-00:00", "Well that stinks. You've been working plenty hard...\U0001f615")
  page_to_strzok(child_file, "2016-08-27T21:27:42-00:00", "Yeah well.")
  strzok_to_page(child_file, "2016-08-27T21:34:54-00:00", "How much different is it (the scope)?")
  strzok_to_page(child_file, "2016-08-27T21:35:37-00:00", "--Redacted--")
  m = strzok_to_page(child_file, "2016-08-28T00:07:09-00:00", "And \U0001f621 --Redacted-- not so good at updating. Sent something I already did, just much later. CYD clearly leading this (which is fine), but don't send half the info - an hour late - the AD already has from CYD.")
  m.addnote("CYD - FBI Cyber Division")
  page_to_strzok(child_file, "2016-08-28T13:23:37-00:00", "I'll send separately to Andy, though I'm sure Bill will brief it at a morning meeting.\U0001f612\n\nA Powerful Russian Weapon: The Spread of False Stories http://nyti.ms/2bR9n3c")
  page_to_strzok(child_file, "2016-08-28T13:35:33-00:00", "It was just an nyt article to you and jon about Russia.")
  strzok_to_page(child_file, "2016-08-28T13:38:33-00:00", "Thanks a lot. This will definitely come up tomorrow morning too...")
  strzok_to_page(child_file, "2016-08-28T13:39:49-00:00", "Thanks. Hopefully without printed handouts. ;) There was another one about the --Redacted--")
  #strzok_to_page(child_file, "2016-08-28T14:32:10-00:00", "I AM DONE WITH MYE!!!!\U0001f621\U0001f621")
  page_to_strzok(child_file, "2016-08-28T14:43:16-00:00", "Yup. And you're only getting about 70% of it compared to the rest of us.")
  page_to_strzok(child_file, "2016-08-29T11:15:55-00:00", "Np. --Redacted-- s in (not sure why I'm doing this then, but whatever). Just let me know when you are coming back up.")
  strzok_to_page(child_file, "2016-08-29T11:19:12-00:00", "\U0001f621 re --Redacted-- being in...your weekend and morning could have been nicer...almost to Peets")
  page_to_strzok(child_file, "2016-08-29T11:20:17-00:00", "Yeah, but she offered to put the binder together so I'll take that.")
  strzok_to_page(child_file, "2016-08-29T11:23:18-00:00", "\u263a good. I like her, I think. Is she still officially Steinbach's staff, or ONP, or DO generally?")
  page_to_strzok(child_file, "2016-08-29T11:24:00-00:00", "Steinbach's staff. And yes, she's excellent.")

  # Page 348
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-29T11:27:02-00:00", "Entering turnstiles now. Your office?")
  page_to_strzok(child_file, "2016-08-29T22:28:55-00:00", "Dude you there?")
  strzok_to_page(child_file, "2016-08-29T22:46:56-00:00", "In answer to your question, was in wrap. --Redacted--")
  strzok_to_page(child_file, "2016-08-29T22:47:12-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-08-29T22:27:41-00:00", "Fun!")
  page_to_strzok(child_file, "2016-08-29T22:56:06-00:00", "I need to call Jason first")
  strzok_to_page(child_file, "2016-08-30T08:25:31-00:00", "Struggling with he role of the new job. I get what you were saying about \"don't be --Redacted--\" where everything has to go through me, but I don't know if that's entirely right. I better know what's going on in my branch. I better know more about what's going on under me than my AD, and surely more than the EAD or you or Andy or the D.\n\nI get find people who can do a good job and let them do it. Completely agree. It's figuring out the right amount to be involved to track and guide, provide input.")
  page_to_strzok(child_file, "2016-08-30T08:55:17-00:00", "--Redacted--\n\nAnd let's talk about the DAD thing later. All I'm saying is worry be present for the things that matter, not the things that don't.")
  page_to_strzok(child_file, "2016-08-30T08:59:57-00:00", "My point is, that brief went super well. So even if you would have phrased a fee things differently, and even of you would have liked to have known every fact before hand, it was superbly. And you not knowing was very much a function of your not being here on Friday. So all I'm saying is focus on the things that matter.")
  strzok_to_page(child_file, "2016-08-30T09:02:32-00:00", "I guess. Still not entirely comfortable with it. Will figure that out, there's an element of Jon in there that I also need to clarify what I'm feeling, what's reasonable, what's not.\n\nThanks for being there to hear all my doubt and concern --Redacted--")
  page_to_strzok(child_file, "2016-08-30T09:03:18-00:00", "Last thing: I get knowing more than the guy above you, but Mike knew far far less than even Andy and I knew about it. Hell, he didn't even know we were having the brief. And I completely under how frustrated that must have made him, but ultimately, the brief was no worse off. Again, it's the focus on the things that matter.")
  strzok_to_page(child_file, "2016-08-30T09:03:19-00:00", "Let me ask you this. How many times had you heard that brief, between prep for that and --Redacted-- and otherwise?")
  page_to_strzok(child_file, "2016-08-30T09:03:39-00:00", "--Redacted-- and then on Friday.")
  page_to_strzok(child_file, "2016-08-30T09:04:18-00:00", "--Redacted--")

  # Page 349
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-08-30T09:05:07-00:00", "No, you heard the prebrief for --Redacted-- to Andy, then the one to the D. Then you heard the prebrief on Fri to Andy, then this one. You've heard it at least FOUR times.")
  strzok_to_page(child_file, "2016-08-30T09:06:23-00:00", "--Redacted--")
  m = strzok_to_page(child_file, "2016-08-30T09:10:05-00:00", "Yeah but that's generally not Ok (re Mike). He came in late to MYE and has been in and out of --Redacted-- And he HAD the TPs for this, he just chose not to read them. Because Jon made sure to send me them to Dina and Bill and Mike, but still hasn't sent them to me.\n\nThats what I'm saying - there's some stuff that's reasonable for me to ask and not reasonable for Jon not to do - hey dude, email me, just cc:, the TPs please - and stuff that isn't.\n\nAnd this is only a tiny bit of ALL the stuff going on. Had a truly horrible proposal for an op come out of WFO in CD2.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  page_to_strzok(child_file, "2016-08-30T09:16:07-00:00", "Agree re the Ps. --Redacted--")
  strzok_to_page(child_file, "2016-08-30T09:20:30-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-08-30T09:44:50-00:00", "Here we go:\nHarry Reid Cites Evidence of Russian Tampering in U.S. Vote, and Seeks F.B.I. Inquiry\n\nhttp://mobile.nytimes.com/2016/08/30/us/politics/harry-reid-russia-tampering-election-fbi.html")
  strzok_to_page(child_file, "2016-08-30T09:45:20-00:00", "But Mr. Reid argued that the connections between some of Donald J. Trump\u2019s former and current advisers and the Russian leadership should, by itself, prompt an investigation. He referred indirectly in his letter to a speech given in Russia by one Trump adviser, Carter Page, a consultant and investor in the energy giant Gazprom, who criticized American sanctions policy toward Russia.\n\n\u201cTrump and his people keep saying the election is rigged,\u201d Mr. Reid said.\u201cWhy is he saying that? Because people are telling him the election can be messed with.\u201d Mr. Trump\u2019s advisers say they are concerned that unnamed elites could rig the election for his opponent, Hillary Clinton.")
  page_to_strzok(child_file, "2016-08-30T09:45:44-00:00", "D said at am brief thst Reid called him and told him he would be sending a le t ter.")
  #strzok_to_page(child_file, "2016-08-30T09:46:29-00:00", "Bill didn't mention it\U0001f612")
  #strzok_to_page(child_file, "2016-08-30T09:51:55-00:00", "And holy cow, let me send you the Reid letter!")
  page_to_strzok(child_file, "2016-08-30T11:10:10-00:00", "Have a meeting with turgal about getting iPhone in a day or so")
  strzok_to_page(child_file, "2016-08-30T11:13:56-00:00", "Oh hot damn. I'm happy to pilot that. ...\n\nWe get around our security / monitoring issues?")

  # Page 350
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-08-30T11:28:50-00:00", "No, he's proposing that we just stop following them. Apparently the requirement to capture texts came from omb, but we're the only org (I'm told) who is following that rule. His point is, if no one else is doing it why should we.")
  page_to_strzok(child_file, "2016-08-30T11:29:25-00:00", "Helps that Dd had a terrible time with his phone --Redacted-- which made him concerned for our folks all over the place.")
  page_to_strzok(child_file, "2016-08-30T11:29:54-00:00", "These phones suck as much as they do because of the program we use to capture texts, full stop.")
  strzok_to_page(child_file, "2016-08-30T11:34:03-00:00", "No doubt.")
  strzok_to_page(child_file, "2016-08-30T11:34:34-00:00", "I'm not convinced, short of OPR, that text capture capability really deters anything.")
  strzok_to_page(child_file, "2016-08-30T11:34:58-00:00", "If I want to copy/take classified, I'm sure as hell not going to do it on this phone.")
  page_to_strzok(child_file, "2016-08-30T11:36:40-00:00", "I thought it was more from a discovery perspective.")
  strzok_to_page(child_file, "2016-08-30T11:39:49-00:00", "Probably. So just make a rule no texts of a discoverable nature.\n\nLike you said, what are CBP, DEA, others doing?")
  page_to_strzok(child_file, "2016-08-30T11:57:27-00:00", "I'm told - though I have seen - that there is an IG report that says everyone is failing. But no one has changed anything, so why not just join in the failure.")
  strzok_to_page(child_file, "2016-08-30T11:58:42-00:00", "Well, if our mission is degraded, that's the reason to do it. Plus, these phones suck")
  page_to_strzok(child_file, "2016-08-30T12:55:38-00:00", "Call my please?")
  page_to_strzok(child_file, "2016-08-30T16:17:38-00:00", "Call desk?")
  strzok_to_page(child_file, "2016-08-30T16:29:43-00:00", "You got the --Redacted-- card?")
  page_to_strzok(child_file, "2016-08-30T16:30:03-00:00", "Yes. In the binder already.")
  strzok_to_page(child_file, "2016-08-30T16:30:53-00:00", "Wow. You're good. :)")
  page_to_strzok(child_file, "2016-08-31T00:33:49-00:00", "VOM-IT. VOMIT. Vomit vomit vomit.\n\nEdward Snowden\u2019sLong, Strange Journey to Hollywood http://nyti.ms2c4Kz50")
  strzok_to_page(child_file, "2016-08-31T00:34:55-00:00", "I told him I thought it might be harder for me than for him, but that that was ok.\U0001f636\n\nI will not read about Snowden tonight.")
  page_to_strzok(child_file, "2016-08-31T01:03:16-00:00", "And seriously, don't read the article, but jesus, V-O-M-I-T.")
  m = strzok_to_page(child_file, "2016-08-31T01:06:15-00:00", "Believe me, I'm not touching that article. Maybe CYD can take that case, too...")
  m.addnote("CYD - FBI Cyber Division")
  page_to_strzok(child_file, "2016-08-31T02:37:11-00:00", "Did you ever look at this? It's incredibly powerful. And really, really depressing.\n\nAt least 110 Republican Leaders Won\u2019t Vote for Donald Trump. Here\u2019s When They Reached Their Breaking Point. http://nyti.ms/2bTNAbb")

  # Page 351
  # OUTBOX == Page
  # INBOX == Strzok  
  page_to_strzok(child_file, "2016-08-31T11:37:05-00:00", "Re the case, Jim Baker honks you should have it. But I'm sure andy would defer to bill. I won't mention.")
  strzok_to_page(child_file, "2016-08-31T11:39:54-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-01T01:19:30-00:00", "And yeah, that article is pretty much guaranteed to get a response out of me in my current state...\U0001f636")
  strzok_to_page(child_file, "2016-09-01T01:19:54-00:00", "How Russia Often Benefits When Julian Assange Reveals the West\u2019s Secrets http://myti.ms/2c1qTIf")
  strzok_to_page(child_file, "2016-09-01T01:24:07-00:00", "Had a long talk with Bill. Can we work talk tomorrow morning re same?")
  strzok_to_page(child_file, "2016-09-01T01:27:45-00:00", "Bottom line Mike read Bill the riot act, said Andy yelled at him and DJ that \"the teams aren't sharing info\" and told them to fix it. Sounds like Mike and Randy want to get everyone together and tell at us, daily updates, and other silliness.\n\nI will relay much more detail when we talk.")
  page_to_strzok(child_file, "2016-09-01T01:40:45-00:00", "Ho boy. Andy said nothing to me except it went well. Makes me nervous that people think I was involved or at the meeting.")
  strzok_to_page(child_file, "2016-09-01T01:43:27-00:00", "Bill wanted to know what generated it. Did he (Andy) get spun up with you?")
  strzok_to_page(child_file, "2016-09-01T01:44:04-00:00", "Let's def talk tomorrow AM. Bill will likely seek you out to talk.")
  m = strzok_to_page(child_file, "2016-09-01T01:44:41-00:00", "I'll give you more detail hete, or better on imsg, but far easier to relay with conversation.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2016-09-01T01:44:56-00:00", "Here. Not hete. Hete sounds like gibberish.")
  page_to_strzok(child_file, "2016-09-01T01:47:50-00:00", "Let's talk tomorrow.")
  strzok_to_page(child_file, "2016-09-01T01:53:31-00:00", "K. --Redacted--")
  page_to_strzok(child_file, "2016-09-01T09:36:11-00:00", "Going to ask Eric who he told about my mtg with Andy. If not him, then it is --Redacted-- running her mouth again.")
  strzok_to_page(child_file, "2016-09-01T11:41:10-00:00", "Tried reaching out to Bill but didn't comnect")
  page_to_strzok(child_file, "2016-09-01T11:42:11-00:00", "I sent an email to he and Randy asking to talk after morning meeting. No answer, but presumably will see them in a couple.")
  strzok_to_page(child_file, "2016-09-01T12:02:45-00:00", "Good luck. Id just tell them what you told me. You're doing a good job, Lisa.\n\nI had more to say about what I think drives the perception. Mainly people want to identify eternal causes of problems rather than face that it might be them.")
  
  # Page 352
  # OUTBOX == Page
  # INBOX == Strzok  
  strzok_to_page(child_file, "2016-09-01T12:07:39-00:00", "That means a lot of times it isn't YOU, it's the position. I heard grumbling about such things as soon as i was in a professional position to hear it, about --Redacted-- and --Redacted-- and --Redacted-- and everyone in between.\n\nThis is no doubt a sh*tty drawback of your job.")
  page_to_strzok(child_file, "2016-09-01T13:15:33-00:00", "Just did it. Mike S. didn't and hasn't said a word to me. Bill defended me, DJ said he understood Andy's frustration, Randy said nothing.")
  strzok_to_page(child_file, "2016-09-01T13:17:32-00:00", "Good. Proud of Bill.")
  strzok_to_page(child_file, "2016-09-01T13:17:53-00:00", "How are you feeling about it?")
  page_to_strzok(child_file, "2016-09-01T13:18:14-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-01T13:18:34-00:00", "I sent an email to Bill saying we had talked and you were going to call him.")
  page_to_strzok(child_file, "2016-09-01T13:19:44-00:00", "I just pulled them all together after the morning meeting. Steinbach obviously didn't have any interest in hearing what I had to say, but I figured I would just be further criticized if I excluded him.")
  page_to_strzok(child_file, "2016-09-01T13:20:37-00:00", "I'm going to try to call Eric now, because of course he's not here because Andy's not here. Then I get to tell Andy and tell him what I just said.")
  strzok_to_page(child_file, "2016-09-01T13:39:45-00:00", "Hope it goes well. What are you going to say? Just what you told all of them?")
  page_to_strzok(child_file, "2016-09-01T13:41:22-00:00", "Yes. Doing it now.")
  strzok_to_page(child_file, "2016-09-01T14:07:14-00:00", "Yes. For a call?")
  page_to_strzok(child_file, "2016-09-01T14:07:28-00:00", "If you can. Nothing major")
  strzok_to_page(child_file, "2016-09-01T16:12:48-00:00", "Hi, How you dping?")
  page_to_strzok(child_file, "2016-09-01T16:27:47-00:00", "Fine. Spoke to Eric. Went okay. Something relevant to you, but can tell you later.")
  strzok_to_page(child_file, "2016-09-01T16:29:30-00:00", "He have any insight?\n\nGood? Bad? Neither?")
  page_to_strzok(child_file, "2016-09-01T16:34:53-00:00", "Potentially bad.")
  page_to_strzok(child_file, "2016-09-01T16:36:04-00:00", "No, he took what Steinbach said as truth, said it made sense once we spoke. Same old sh*t.")
  strzok_to_page(child_file, "2016-09-01T16:37:23-00:00", "What did Steinbach say? That Andy yelled at him? Or something else?")
  strzok_to_page(child_file, "2016-09-01T16:37:31-00:00", "I can call later, too")
  page_to_strzok(child_file, "2016-09-01T16:38:12-00:00", "Let's just talk later. It's not clear what he said, just some things that Eric implied.")

  # Page 353
  # OUTBOX == Page
  # INBOX == Strzok  
  strzok_to_page(child_file, "2016-09-01T16:53:36-00:00", "Talk now?")
  page_to_strzok(child_file, "2016-09-01T17:09:29-00:00", "Sorry, was in with Baker. I can talk in 2.")
  strzok_to_page(child_file, "2016-09-01T17:10:05-00:00", "Sorry, can't now, 15 min?")
  page_to_strzok(child_file, "2016-09-01T17:11:14-00:00", "Baker ran into Steinbach, who complained about me. Steinbach and Coleman want to talk to Andy.")
  strzok_to_page(child_file, "2016-09-01T17:22:13-00:00", "F them.\U0001f621\U0001f621\U0001f621\U0001f621\n\nCall you in 3 minutes")
  strzok_to_page(child_file, "2016-09-01T17:59:15-00:00", "Man I'm angry")
  strzok_to_page(child_file, "2016-09-01T17:59:29-00:00", "For you")
  page_to_strzok(child_file, "2016-09-01T18:01:53-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-01T18:03:00-00:00", "Believe me, no way I try and do that any time soon.\U0001f61e")
  strzok_to_page(child_file, "2016-09-01T18:03:18-00:00", "You DO good work. --Redacted--")
  strzok_to_page(child_file, "2016-09-01T18:04:19-00:00", "What did Jim recommend? Anything?")
  page_to_strzok(child_file, "2016-09-01T18:07:23-00:00", "He doesn't know what to do. He honestly said he didn't know what to recommend.")
  #page_to_strzok(child_file, "2016-09-01T18:07:48-00:00", "Just got another call from quinn re MYE. Should I direct his call to Steinbach?")
  strzok_to_page(child_file, "2016-09-01T18:08:03-00:00", "Hah. No.")
  strzok_to_page(child_file, "2016-09-01T18:09:05-00:00", "--Redacted-- Thats who Bill told me to coordinate the --Redacted-- thing with. Mike can take over \"messaging\" from here....")
  strzok_to_page(child_file, "2016-09-01T18:19:21-00:00", "Speaking of media, did you see the Wash Times quotes the OPA person shared with --Redacted-- (And why --Redacted-- Would have throught one of us, us including Jon and Bill)")
  strzok_to_page(child_file, "2016-09-01T18:19:29-00:00", "They worry me a bit")
  m = page_to_strzok(child_file, "2016-09-01T18:19:33-00:00", "I have mye questions. No one is around.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-09-01T18:19:50-00:00", "Ask away")
  page_to_strzok(child_file, "2016-09-01T18:20:30-00:00", "I'm not typing it all out. Forget it.")

  # Page 354
  # OUTBOX == Page
  # INBOX == Strzok  
  m = strzok_to_page(child_file, "2016-09-01T18:20:42-00:00", "Seriously, I can hop on eras and answer if I don't have them off the top of my head. Or are they legal?")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-09-01T18:20:59-00:00", "Can you talk to me and ask?")
  page_to_strzok(child_file, "2016-09-01T18:21:03-00:00", "No. Factual. Three more comments from the wash times.")
  page_to_strzok(child_file, "2016-09-01T18:21:09-00:00", "Yes, if you can talk.")
  strzok_to_page(child_file, "2016-09-01T18:38:33-00:00", "Def get with --Redacted-- for legal analysis. FRA contains language about each agency establishing record keeping procedures, and I vaguely recall it's not clear that she was not in compliance with State's program at the time.")
  strzok_to_page(child_file, "2016-09-01T19:26:41-00:00", "Obviously if Andy is good with the statement, I'm not adding \"me too\"!")
  page_to_strzok(child_file, "2016-09-01T20:57:38-00:00", "Need to go to wrap. Because I'm so stupid and loyal I stayed here the same day so Andy doesn't miss anything.")
  #page_to_strzok(child_file, "2016-09-01T23:16:49-00:00", "I can't. Now the Midyear production has to happen tomorrow. And you and --Redacted-- and --Redacted-- are all out.")
  strzok_to_page(child_file, "2016-09-01T13:22:58-00:00", "What is production at this point? Certainly, that you can't do from home?")
  #page_to_strzok(child_file, "2016-09-01T23:26:00-00:00", "Yeah, and get everyone the copies they need, and tell baker and doj an wait for all the hill notifications and tell the agency. I'm not giving State an advance warning. F them.")
  strzok_to_page(child_file, "2016-09-01T23:42:11-00:00", "Email. They all have secretaries who can print for them. Jason handles the hill. It will ALL work out without you there")
  #strzok_to_page(child_file, "2016-09-01T23:51:41-00:00", "And yes, totally. F State. No heads up")
  page_to_strzok(child_file, "2016-09-02T01:00:54-00:00", "Yeah, well you can add that to the list of things that is never going to happen, like me gaining the respect of superiors simply because I work hard and do a good job.")
  page_to_strzok(child_file, "2016-09-02T01:02:15-00:00", "I'm also incredibly disappointed in Bill. I would have hoped for some follow-up from him. Even just feedback or thanks or disagreement or something. But instead he just fell off the map.")
  strzok_to_page(child_file, "2016-09-02T01:05:08-00:00", "--Redacted--\n\nI think Bill is busy and worried about H7462where he stands with his boss, and based on what Mike told him, with Andy. I'm not there to bounce things off of, so it makes it worse. That will be ok. From what you said, he was the only stand up guy at your meeting.")
  strzok_to_page(child_file, "2016-09-02T01:26:56-00:00", "You should take tomorrow off.")
  strzok_to_page(child_file, "2016-09-02T01:27:30-00:00", "The Bu will continue as it has for decades.")
  page_to_strzok(child_file, "2016-09-02T01:37:20-00:00", "You know I'm not going to stay home. You can stop insisting.")
  #strzok_to_page(child_file, "2016-09-02T01:38:32-00:00", "And I'm not going to stop telling you that's a bad decision, that the bureau - and MYE - will be just fine.")

  # Page 355
  # OUTBOX == Page
  # INBOX == Strzok  
  strzok_to_page(child_file, "2016-09-02T01:40:53-00:00", "I promise you...tell me, what needs to be done that can't be done by you via phone or email OR by someone else?\n\nTake the day, --Redacted--")
  page_to_strzok(child_file, "2016-09-02T01:41:23-00:00", "Note the bcc. Because, I've already spoken to --Redacted-- about this today once already. In addition to the tri-weekly email I get from Laufman.")
  page_to_strzok(child_file, "2016-09-02T01:41:59-00:00", "Yup, I'll just do it from home.")
  page_to_strzok(child_file, "2016-09-02T01:42:23-00:00", "WHO IS THE SOMEONE ELSE?!")
  strzok_to_page(child_file, "2016-09-02T01:46:35-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-02T01:46:43-00:00", "Jason")
  strzok_to_page(child_file, "2016-09-02T01:46:45-00:00", "OCA")
  strzok_to_page(child_file, "2016-09-02T01:46:52-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-02T01:46:54-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-02T01:47:00-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-02T01:47:01-00:00", "Moffa")
  page_to_strzok(child_file, "2016-09-02T01:47:08-00:00", "Stop. Now you're just insulting me.")
  strzok_to_page(child_file, "2016-09-02T01:47:14-00:00", "YOU CAN STAY HOME")
  strzok_to_page(child_file, "2016-09-02T01:49:22-00:00", "Make the calls from home")
  strzok_to_page(child_file, "2016-09-02T01:49:51-00:00", "Tell everyone \"call so-and-so and email me when you're done\"")
  strzok_to_page(child_file, "2016-09-02T01:49:55-00:00", "Then call OPA and tell them to release")
  strzok_to_page(child_file, "2016-09-02T01:50:12-00:00", "And DOJ is a wild pain in the ass")
  strzok_to_page(child_file, "2016-09-02T01:50:25-00:00", "Not as bad as State, but still")
  page_to_strzok(child_file, "2016-09-02T01:50:41-00:00", "Yes, George. I know we have to call counsel.")
  strzok_to_page(child_file, "2016-09-02T01:51:11-00:00", "Lisa, I don't think that's the right decision, and i dont agree. But having said that, and meaning it, I'll leave it alone.")
  page_to_strzok(child_file, "2016-09-02T01:51:23-00:00", "And what's the other agency reference? Is that State?")
  strzok_to_page(child_file, "2016-09-02T01:52:44-00:00", "I don't know. I assumed it was WH")
  strzok_to_page(child_file, "2016-09-02T01:53:02-00:00", "DoJ has NO obligation as far as I'm aware of.")

  # Page 356
  # OUTBOX == Page
  # INBOX == Strzok  
  page_to_strzok(child_file, "2016-09-02T01:55:38-00:00", "Forgot to show you this text from Eric, who is essentially blaming me for Andy's late hours:\n\nGood deal. I also want to stay a little tighter in the future so we can ensure Unity of effort for both Andy and the whole floor. This will also help in streamlining any after wrap discussions with Andy as I want to try to get him out the door at a more reasonable hour then what he has been doing. And that goes for you too! --Redacted--")
  strzok_to_page(child_file, "2016-09-02T01:58:21-00:00", "Andy's the DD. He's going to be late. You've got nothing to do with it.\U0001f612")
  page_to_strzok(child_file, "2016-09-02T01:59:49-00:00", "What I wanted to respond is how is staying tighter going to allow Andy to get out earlier? Is Eric going to cover my questions?")
  strzok_to_page(child_file, "2016-09-02T01:59:56-00:00", "Streamlining after wrap discussions? How about Andy decides whether he wants that?")
  strzok_to_page(child_file, "2016-09-02T02:00:21-00:00", "Exactly. No. Maybe it will allow him to understand the depth of what you're doing.")
  page_to_strzok(child_file, "2016-09-02T02:01:09-00:00", "Which I'm fine with. So just sit down with us after wrap. But don't make more goddamn work for me.")
  strzok_to_page(child_file, "2016-09-02T02:07:01-00:00", "Yeah I'm not sure what he thinks he's accomplishing other than understanding what you're doing. At which point he'll say (if he's smart), oh, wow, that's a lot, and then let you go. After wasting your time. --Redacted--")
  strzok_to_page(child_file, "2016-09-02T13:41:30-00:00", "Checkout my 9:30 mtg on the 7th")
  page_to_strzok(child_file, "2016-09-02T13:42:40-00:00", "I can tell you why you're having that meeting.")
  page_to_strzok(child_file, "2016-09-02T13:42:46-00:00", "It's not what you think.")
  strzok_to_page(child_file, "2016-09-02T13:49:39-00:00", "TPs for D?")
  m = page_to_strzok(child_file, "2016-09-02T13:50:29-00:00", "Yes, bc potus wants to know everything we are doing.")
  m.addnote("potus - President of the United States")
  strzok_to_page(child_file, "2016-09-02T13:55:21-00:00", "I'm sure an honest answer will come out of that meeting....\U0001f612")
  page_to_strzok(child_file, "2016-09-02T15:38:05-00:00", "--Redacted-- never knocks on the door. It's kind of weird.\n\nWhat are you doing? Why are you gone so much? God!\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d")
  strzok_to_page(child_file, "2016-09-02T16:04:46-00:00", "Thoughts on --Redacted-- email? Maybe just send her a copy of FOIA?")
  page_to_strzok(child_file, "2016-09-02T16:05:34-00:00", "There's more to discuss. Don't feel like typing.")
  strzok_to_page(child_file, "2016-09-02T16:07:35-00:00", "Work call after lunch? I also have 5 now before food arrives")
  strzok_to_page(child_file, "2016-09-02T16:09:10-00:00", "Just tried calling...will hit you after lunch")

  # Page 357
  # OUTBOX == Page
  # INBOX == Strzok  
  strzok_to_page(child_file, "2016-09-02T17:26:11-00:00", "NYTimes.com breaking")
  strzok_to_page(child_file, "2016-09-02T17:26:49-00:00", "You saw the byline, right?")
  page_to_strzok(child_file, "2016-09-02T18:07:01-00:00", "It helps that the Director and Deputy really hate these phones too. And really love their personal iphones.")
  strzok_to_page(child_file, "2016-09-02T18:09:05-00:00", "Now if Tim Cook would only fall off the face of the earth")
  strzok_to_page(child_file, "2016-09-02T20:57:43-00:00", "Def still up for coming in Sun to work magic.\n\nAnd I mean that work-wise, I'm really excited about writing it into his language.\n\n\U0001f60b\U0001f636")
  strzok_to_page(child_file, "2016-09-02T22:08:19-00:00", "I love our Director")
  page_to_strzok(child_file, "2016-09-02T22:08:40-00:00", "I know. I do too")
  page_to_strzok(child_file, "2016-09-02T22:10:00-00:00", "You obviously did not get a hold of Bill.")
  strzok_to_page(child_file, "2016-09-02T22:10:42-00:00", "What? More? He didn't send whatever it was to me. Please forward?")
  strzok_to_page(child_file, "2016-09-02T22:10:58-00:00", "And no, I didn't. No office answer, no cell.")
  page_to_strzok(child_file, "2016-09-02T22:11:15-00:00", "What were you talking about then?")
  page_to_strzok(child_file, "2016-09-02T22:11:52-00:00", "The Grassley email you meant, right? I did too.")
  m = page_to_strzok(child_file, "2016-09-02T22:12:35-00:00", "If he doesn't call tonight I would freaking call SIOC and them connect you to his home.")
  m.addnote("SIOC - Strategic Information and Operations Center")
  page_to_strzok(child_file, "2016-09-02T22:39:45-00:00", "Please tell me this absence means you're talking to Bill...")
  strzok_to_page(child_file, "2016-09-02T22:40:26-00:00", "Yes. Just got done talking with him. Talk? --Redacted-- is here so will be work")
  page_to_strzok(child_file, "2016-09-02T22:42:21-00:00", "No. --Redacted-- Please tell me he has relaxed")
  strzok_to_page(child_file, "2016-09-02T22:45:04-00:00", "Yes. Call for data came at wrap (jr and bowdich) for desire for D to have data to chew on.\n\nHe also talked about your meeting with everyone to try and clear air. Remond me, though nothing really there to report.")
  page_to_strzok(child_file, "2016-09-02T22:48:53-00:00", "Got it. But we are still writing the op ed, yes?")
  strzok_to_page(child_file, "2016-09-02T22:51:05-00:00", "Yes, -ish. He said too much data, would be good to identify the key pieces of data and frame it in an argument, but not to spend \"too much time on the opening or closing.\" I told him we were too much of perfectionists to not do all of it.")
  page_to_strzok(child_file, "2016-09-03T00:28:51-00:00", "Gotta say, most of the coverage has been quite favorable.\n\nF.B.I. Papers Offer Closer Look at Hillary Clinton Email Inquiry http://nyti.ms/2cfM00m")
  page_to_strzok(child_file, "2016-09-03T00:29:15-00:00", "And crap, we should have told the agents/analysts that the docs were coming out today.\U0001f615")

  # Page 358
  # OUTBOX == Page
  # INBOX == Strzok  
  strzok_to_page(child_file, "2016-09-03T00:51:32-00:00", "I did tell them")
  strzok_to_page(child_file, "2016-09-03T01:28:30-00:00", "That nyt article was pretty good")
  strzok_to_page(child_file, "2016-09-03T01:30:05-00:00", "This was also good. Probably what in would have noted, too:\nhttp://mobile.nytimes.com/2016/09/03/us/politics/6-things-we-learned-in-the-fbi-clinton-email-investigation.html")
  m = strzok_to_page(child_file, "2016-09-04T15:36:28-00:00", "Just told Jon I was on eras thinking of coming in. Figured give us 10 minutes to talk before getting together if he wants to stick around for all of us to work")
  m.addnote("eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2016-09-04T15:52:45-00:00", "So I don't understand, you are going to tell jon you're here? You aren't?")
  strzok_to_page(child_file, "2016-09-04T15:53:13-00:00", "I told him I may drive in")
  page_to_strzok(child_file, "2016-09-05T10:50:01-00:00", "An article to share: Intelligence community investigating covert Russian influence operations in the United States\n\nIntelligence community investigating covert Russian influence operations in the United States\nhttp://wapo.st/2c0UA2H")
  strzok_to_page(child_file, "2016-09-05T10:51:51-00:00", "This is the one --Redacted-- was taking about I think")
  page_to_strzok(child_file, "2016-09-05T10:52:37-00:00", "Yup. It is very well sourced. 100% authorized.")
  strzok_to_page(child_file, "2016-09-05T10:54:03-00:00", "Doesn't really look like it")
  page_to_strzok(child_file, "2016-09-05T10:54:26-00:00", "Not really. --Redacted--")
  strzok_to_page(child_file, "2016-09-05T11:02:09-00:00", "Just read the article. We say a lot of the same things. I guess that's ok.")
  page_to_strzok(child_file, "2016-09-05T11:02:42-00:00", "Yeah, but that's why ours is going to need to be more folksy. So it's not like a news article.")
  strzok_to_page(child_file, "2016-09-05T11:02:48-00:00", "I really have no faith the administration will deal with it effectively")
  page_to_strzok(child_file, "2016-09-05T11:02:56-00:00", "Nope. You shouldn't.")
  strzok_to_page(child_file, "2016-09-05T11:19:54-00:00", "I am losing my mind because I can't get my stupid laptop to connect to FBINET. I got up early to see the draft you giys worked on but no dice. Want to spike it in the street.")
  strzok_to_page(child_file, "2016-09-05T11:50:03-00:00", "Sorry. I'm going to try in a bit. Came up with a lot of little edits")
  strzok_to_page(child_file, "2016-09-05T11:55:42-00:00", "I can't go in today so if I can't connect in the next hour or so I'll just have to see it tomorrow. Obviously fire it off to the AD though. I'm sure it's great. Won't take my password for some reason...")
  m = strzok_to_page(child_file, "2016-09-05T14:08:22-00:00", "--Redacted-- After inputting edits in eras.\n\nLet me know when you leave")
  m.addnote("eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2016-09-05T14:11:20-00:00", "Left")

  # Page 359
  # OUTBOX == Page
  # INBOX == Strzok  
  strzok_to_page(child_file, "2016-09-05T15:10:03-00:00", "Just sent op-ed to Bill, cc:ed both of you.")
  strzok_to_page(child_file, "2016-09-05T22:50:03-00:00", "And ooh, you're at ODNI on Wed. LX? H8013Me too! From 11:30 till 2:00. I'll give you a ride!")
  page_to_strzok(child_file, "2016-09-05T22:58:10-00:00", "No, only if trisha wants me to, and I'm sure she won't.")
  strzok_to_page(child_file, "2016-09-05T23:08:07-00:00", "Can you just go? Or go to my thing then go to the other one since you're there?")
  m = page_to_strzok(child_file, "2016-09-05T23:19:47-00:00", "I'm sure that would cause some turmoil (why is Lisa there and not nslb...)")
  m.addnote("nslb - National Security Law Branch at DOJ")
  strzok_to_page(child_file, "2016-09-05T23:21:37-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-05T22:27:36-00:00", "Yes! About what?")
  m = strzok_to_page(child_file, "2016-09-05T23:39:35-00:00", "Gotta figure that out tomorrow. Insider threat perhaps. Maybe Electoral shenanigans. I'm between Clapper and Evanina and another person or two.")
  m.addnote("Evanina - William Evanina, Director National Counterintelligence and Security Center")
  page_to_strzok(child_file, "2016-09-06T11:39:31-00:00", "Stupid ass --Redacted-- and --Redacted-- and I don't think she was successful.\U0001f621")
  page_to_strzok(child_file, "2016-09-06T11:40:41-00:00", "At clearing the air.\U0001f621\U0001f621\U0001f621\U0001f621\U0001f621")
  strzok_to_page(child_file, "2016-09-06T11:43:02-00:00", "Got it. You going to talk to him? You said at the time he backed you up.")
  strzok_to_page(child_file, "2016-09-06T11:43:37-00:00", "But might be better to let it go for now?")
  page_to_strzok(child_file, "2016-09-06T11:44:00-00:00", "He just didn't leave me out the hanging, but he didn't say, thanks for explaining or anything like that.")
  strzok_to_page(child_file, "2016-09-06T11:44:05-00:00", "And I know \U0001f614")
  strzok_to_page(child_file, "2016-09-06T11:46:02-00:00", "How about go to him, say, you know how you said you appreciated it when I gave you honest feedback, that that's rare? I'd appreciate the same from you. What do you think about how last week unfolded?")
  strzok_to_page(child_file, "2016-09-06T11:46:19-00:00", "But you CANNOT burn me as a source...")
  page_to_strzok(child_file, "2016-09-06T11:47:19-00:00", "And I'm far more pissed that after doing it, he didn't come to me separately and say thanks or I'm not sure you made any progress but thanks anyway or ANYTHING.")
  page_to_strzok(child_file, "2016-09-06T11:47:49-00:00", "Nope. F it. He wants to lose an ally, so be it.")
  strzok_to_page(child_file, "2016-09-06T11:59:41-00:00", "I think he was feeling the results of Mike talking to him. Put yourself in his shoes, with his personality. Not saying he's right, but I'm saying he's thoughtful and different from Mike and Randy.\n\nWhile I'd be angry, too, I wouldn't throw out an ally/work friendship over it.")
  strzok_to_page(child_file, "2016-09-06T12:00:11-00:00", "He didn't sell you out. Just understand his personality and you relationship and consider that.")

  # Page 360
  # OUTBOX == Page
  # INBOX == Strzok  
  page_to_strzok(child_file, "2016-09-06T12:20:47-00:00", "Maybe not. But if that's just \"his personality\" I'm sure not going to stick my neck out for him again. HE doesn't want the headache? Yeah, well I don't either.")
  strzok_to_page(child_file, "2016-09-06T12:28:42-00:00", "Look, I get it. I'm as frustrated as you are. I can understand not sticking you neck out, too.")
  strzok_to_page(child_file, "2016-09-06T12:29:05-00:00", "A different frustration - I didn't get burned like you did")
  page_to_strzok(child_file, "2016-09-06T13:19:37-00:00", "And good, --Redacted-- is still not back from --Redacted--")
  strzok_to_page(child_file, "2016-09-06T13:51:23-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-06T13:51:36-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-06T21:01:58-00:00", "Hi. Funny (not haha) convo with Mike. Call me when you're done. And I have no expectation my wrap will be done before 6, so if you can get the hell out of here before then, go.")
  strzok_to_page(child_file, "2016-09-06T22:19:40-00:00", "And gosh that was a fast wrap....")
  strzok_to_page(child_file, "2016-09-06T22:47:47-00:00", "And your silly TWO HOUR OVER LUNCH brief on Friday is Hull prep, guessing for Jason. You him Baker --Redacted-- is out. Let me know if I can'should join. --Redacted--")
  strzok_to_page(child_file, "2016-09-06T23:10:34-00:00", "Were your ears burning? Just talked about you for 30 minutes with Bill.\n\nIn part about what he's going to say to Andy.\n\nWho he's trying to call right now.")
  page_to_strzok(child_file, "2016-09-06T23:12:27-00:00", "Sigh. Thank you. Can you give me a quick recap?")
  strzok_to_page(child_file, "2016-09-06T23:26:05-00:00", "On a call?")
  page_to_strzok(child_file, "2016-09-06T23:26:30-00:00", "No. --Redacted-- Meeting Andy at 0700 to talk about operational stuff. Will Bill tell you of he connected with andy? Also, did he provide further info re how you came up?")
  strzok_to_page(child_file, "2016-09-06T23:26:38-00:00", "Meaning, I'm driving, and it's hard for me to text that. I would be happy to tell you on the phone.")
  page_to_strzok(child_file, "2016-09-06T23:27:00-00:00", "Got it, sorry, I can't for about 30.")
  strzok_to_page(child_file, "2016-09-06T23:27:10-00:00", "I don't think he will tonight.")
  strzok_to_page(child_file, "2016-09-06T23:27:27-00:00", "He didn't (re me)")
  page_to_strzok(child_file, "2016-09-06T23:28:02-00:00", "I will probably email bill and ask him if he'd be willing to tell me if they talk, just so I know what I am walking into.")
  strzok_to_page(child_file, "2016-09-06T23:28:11-00:00", "Brought the topic up, but didn't specifically ask. A lot to talk about. Nothing earthshaking. Just a lot of detail.")
  strzok_to_page(child_file, "2016-09-06T23:29:09-00:00", "I think you'd be fine with that. Obviously don't reference our talking about it.")
  strzok_to_page(child_file, "2016-09-06T23:29:12-00:00", "He'd not you'd")

  # Page 361
  # OUTBOX == Page
  # INBOX == Strzok  
  page_to_strzok(child_file, "2016-09-06T23:29:49-00:00", "Of course. I presume a call later not worth it the trouble for you?")
  strzok_to_page(child_file, "2016-09-06T23:30:08-00:00", "And I'm now more worried about me. Think Jon is fine")
  strzok_to_page(child_file, "2016-09-06T23:31:01-00:00", "Depends, --Redacted--")
  page_to_strzok(child_file, "2016-09-06T23:31:13-00:00", "You have nothing to worry about. They'll both be gone before your next job. AND they both like you. It's ME they don't like.")
  page_to_strzok(child_file, "2016-09-06T23:31:47-00:00", "Is it detail i need to know before tomorrow?")
  strzok_to_page(child_file, "2016-09-06T23:33:39-00:00", "A) then why you and Bill both getting my name mentions of me\nB)no. Only the fresher it is, the more detail.")
  strzok_to_page(child_file, "2016-09-06T23:34:05-00:00", "I'm old and forgetful. ;)")
  page_to_strzok(child_file, "2016-09-06T23:55:58-00:00", "A) Pete, it's going to be fine. Don't make this something else to unnecessarily worry about. Your reputation precedes you, and the D and DD think you're great. Worry about those things that matter.")
  strzok_to_page(child_file, "2016-09-06T23:58:08-00:00", "Sigh. I want to believe that but for my boss mentioning it to me. Just ignore that?")
  page_to_strzok(child_file, "2016-09-06T23:58:53-00:00", "It's a mention about perception. Be aware of perception. I wouldn't worry further than that.")
  page_to_strzok(child_file, "2016-09-06T23:59:51-00:00", "And uh yeah, your advice for me, even when you know I am in the line of fire, is always, f them. So...")
  strzok_to_page(child_file, "2016-09-07T00:01:02-00:00", "You're leaving in 18 months. And you work directly for the DD.")
  page_to_strzok(child_file, "2016-09-07T00:01:34-00:00", "I don't have another job, and when he leaves I have no job.")
  page_to_strzok(child_file, "2016-09-07T00:01:53-00:00", "I'm just saying if the advice is good enough for me...")
  strzok_to_page(child_file, "2016-09-07T00:01:54-00:00", "I also sometimes advise you to keep your head down ;)")
  strzok_to_page(child_file, "2016-09-07T00:04:22-00:00", "I appreciate what you're telling me. I'm saying advice for you and me may be slightly different. I am part of that white male agent hierarchy. Well below the DD.\n\nAnd I fully appreciate your advice to be aware of the perception and otherwise F them, keep working hard.")
  page_to_strzok(child_file, "2016-09-07T00:05:32-00:00", "That white male hierarchy that NEVER eats its own. That pushes even idiots forward for promotion. I think you're going to be okay.")
  strzok_to_page(child_file, "2016-09-07T00:06:40-00:00", "Sigh. Agreed.\n--Redacted--")
  page_to_strzok(child_file, "2016-09-07T00:09:17-00:00", "I don't know. I think I was feeling momentarily resentful at you worry. Yours is speculative and distant, mine is front and center and the in fact named problem.")
  page_to_strzok(child_file, "2016-09-07T00:09:30-00:00", "Probably not bring fair to you, I realize.")

  # Page 362
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-07T00:13:21-00:00", "Lisa, It's not. I was feeling the same resentment. My boss told me specifically I was mentioned, including in the context of Pete going around the chain of command to get Lisa to feed something to Andy. I did not make that up. I am not exaggerating that. Thus isn't ALL you, nor is it a zero sum game, not is it a comparison or competition. But simply waving my concerns aside, saying \"it's all me.\" isn't accurate.")
  strzok_to_page(child_file, "2016-09-07T01:18:30-00:00", "Oh. And prepping Bill tonight to call Andy. Tack that somewhere in the second sentence above.")
  page_to_strzok(child_file, "2016-09-07T01:44:43-00:00", "And don't conflate my email to Bill with my gratitude for you. That's totally unfair.")
  page_to_strzok(child_file, "2016-09-07T01:55:45-00:00", "--Redacted-- I'm meeting andy at 0700.")
  strzok_to_page(child_file, "2016-09-07T02:44:54-00:00", "Btw, realistically you think you'll have time to talk or coffee tomorrow am? Guessing you'll go straight from 7:00 into morning Intel brief, right?")
  strzok_to_page(child_file, "2016-09-07T11:37:22-00:00", "Need to talk to you on work issue")
  strzok_to_page(child_file, "2016-09-07T11:37:30-00:00", "We've got time")
  strzok_to_page(child_file, "2016-09-07T11:37:46-00:00", "I can talk work on the way there and back")
  page_to_strzok(child_file, "2016-09-07T01:37:47-00:00", "K. One sec. Will call from ofc phone.")
  page_to_strzok(child_file, "2016-09-07T01:37:56-00:00", "K. Let's go.")
  page_to_strzok(child_file, "2016-09-07T01:38:06-00:00", "Meet you in ctyard")
  page_to_strzok(child_file, "2016-09-07T01:38:48-00:00", "Let's just do Starbucks. There's not time.")
  strzok_to_page(child_file, "2016-09-07T12:45:33-00:00", "Hey just stopped by your office. --Redacted-- \U0001f60a")
  page_to_strzok(child_file, "2016-09-07T12:50:40-00:00", "Sorry, went to see --Redacted--")
  page_to_strzok(child_file, "2016-09-07T12:50:47-00:00", "Headed back now")
  strzok_to_page(child_file, "2016-09-07T12:57:11-00:00", "K will swing by now on way to Jason's")
  strzok_to_page(child_file, "2016-09-07T13:00:00-00:00", "At Jason's")
  page_to_strzok(child_file, "2016-09-07T13:00:11-00:00", "Okay, be right there.")
  strzok_to_page(child_file, "2016-09-07T14:24:10-00:00", "Hoooo boy. Call me")
  strzok_to_page(child_file, "2016-09-07T15:21:42-00:00", "Finishing SC mtg, 5 min")
  strzok_to_page(child_file, "2016-09-07T19:49:00-00:00", "Just got done with Castor.")

  # Page 363
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-07T22:15:34-00:00", "Andy not going to reply all. I am furious. Don't call back.")
  page_to_strzok(child_file, "2016-09-07T22:23:26-00:00", "So, do I call him and explain why not responding by email entirely undermines me?")
  strzok_to_page(child_file, "2016-09-07T23:11:54-00:00", "Def don't email. Talk to him. NOT tonight")
  page_to_strzok(child_file, "2016-09-07T23:12:26-00:00", "I'm not unless he calls. I'm actually not going by his ofc unless he calls.")
  page_to_strzok(child_file, "2016-09-07T23:16:20-00:00", "But I am absolutely enraged. He is purposefully choosing to save Mike and Dave's face at my expense.")
  strzok_to_page(child_file, "2016-09-07T23:39:22-00:00", "Lis. You must talk to him. But don't do it tonight.")
  strzok_to_page(child_file, "2016-09-07T23:39:26-00:00", "I'm sorry. You must be livid")
  page_to_strzok(child_file, "2016-09-07T23:40:10-00:00", "I am. I texted him this:\n\nI would like to speak to you before you talk to Steinbach and Bowdich about their email.")
  page_to_strzok(child_file, "2016-09-07T23:40:47-00:00", "So it doesn't have to be tonight; we'll see what he says.")
  strzok_to_page(child_file, "2016-09-08T00:19:34-00:00", "Of course let me know how it goes with JB. And if he's not there, call me \U0001f614\u2764")
  m = strzok_to_page(child_file, "2016-09-08T00:31:52-00:00", "Great. Now i have daily meetings, twice a day either CyD. An hour long each. 930-1030 and 4-5.")
  m.addnote("CyD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-09-08T00:32:35-00:00", "Because their division is incapable of pulling its head out of its ass. I don't have two hours a day to give to this b*******.")
  strzok_to_page(child_file, "2016-09-08T00:44:47-00:00", "Now I'm livid....I do not have two hours a day to throw at this.")
  page_to_strzok(child_file, "2016-09-07T23:45:08-00:00", "You should be. That's an utter waste.")
  page_to_strzok(child_file, "2016-09-07T23:45:33-00:00", "Twice a day. That is so outrageous.")
  strzok_to_page(child_file, "2016-09-08T00:46:31-00:00", "And inexplicably, no one, not even after the director's comments today, is willing to say: cyber is f***** up. Cyber needs to fix itself. Cybers way of doing business is unacceptable.")
  page_to_strzok(child_file, "2016-09-08T00:47:00-00:00", "Well that's the profile in courage of you EAD.")
  strzok_to_page(child_file, "2016-09-08T00:47:05-00:00", "Instead, everybody has to be a little wrong, everybody has to be a little right. Randy and Mike bear nothing. They grind their divisions under them to a halt.")
  strzok_to_page(child_file, "2016-09-08T00:48:38-00:00", "So instead, other stuff will drop. I hope Andy in the director are happy. I hope the opportunity cost to the FBI is worth it.")
  page_to_strzok(child_file, "2016-09-08T01:18:21-00:00", "Sorry for the delay, was just on with --Redacted--. God, I see right through her...")
  strzok_to_page(child_file, "2016-09-08T01:19:07-00:00", "What did she want \U0001f612")

  # Page 364
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-08T01:20:32-00:00", "Oh, just make sure I understood where things were on the --Redacted-- paper, trying to talk Axelrod because he's \"so angry\" with how this came over to them. I told her not to put herself out too much, if Matt wants to call and yell at Andy it's fine.")
  page_to_strzok(child_file, "2016-09-08T01:20:47-00:00", "It's all perception management.")
  strzok_to_page(child_file, "2016-09-08T01:21:05-00:00", "And funny quote of the evening. \"upon my arrival, I made the mistake of believing Americans understood irony.\"")
  strzok_to_page(child_file, "2016-09-08T01:21:16-00:00", "I really do love the British.")
  page_to_strzok(child_file, "2016-09-08T01:21:30-00:00", "Was it a nice night?")
  strzok_to_page(child_file, "2016-09-08T01:22:17-00:00", "Meh. Would have been far better with you there. I got to speak on behalf of Counter Intelligence Division, so it's good I was there.")
  page_to_strzok(child_file, "2016-09-08T01:22:54-00:00", "That is good.")
  strzok_to_page(child_file, "2016-09-08T01:25:03-00:00", "Did you get ahold of Baker?")
  page_to_strzok(child_file, "2016-09-08T01:27:48-00:00", "I did. Good conversation, he gets it, offered to say something but I said no. Said there was no question that it was a request from the DD.")
  strzok_to_page(child_file, "2016-09-08T01:28:46-00:00", "He have any ideas how you should approach Andy?")
  page_to_strzok(child_file, "2016-09-08T01:28:52-00:00", "Says I need to keep trying to cultivate a relationship with Steinbach, ask him to coffee or lunch or a drink. I'm not sure I will try that.")
  page_to_strzok(child_file, "2016-09-08T01:29:26-00:00", "I'm just going to explain to andy why it is important to me that he respond via email.")
  strzok_to_page(child_file, "2016-09-08T01:30:23-00:00", "--Redacted-- out of here, right?")
  strzok_to_page(child_file, "2016-09-08T01:30:51-00:00", "And while you may not be cultivating him, it's not like you're a jerk to him.")
  page_to_strzok(child_file, "2016-09-08T01:31:29-00:00", "I told him I was thinking of stepping down if he does not.")
  page_to_strzok(child_file, "2016-09-08T01:31:38-00:00", "He is, once he finds a job.")
  strzok_to_page(child_file, "2016-09-08T01:32:20-00:00", "What did he say to that?")
  page_to_strzok(child_file, "2016-09-08T01:32:24-00:00", "Baker doesn't think I should. I told him if he said no re the email, that I would come talk to him first.")
  page_to_strzok(child_file, "2016-09-08T01:32:58-00:00", "But when I say that it means Andy doesn't really have my back, he understands why I would. And while I feel that way.")
  page_to_strzok(child_file, "2016-09-08T01:34:05-00:00", "I'm very disappointed that Andy didn't reach out tonight.")
  page_to_strzok(child_file, "2016-09-08T01:51:11-00:00", "Boy, this guy is a big R like you.\n\nFortress of Tedium: What I Learned as a Substitute Teacher. http://nyti.ms/2crUNfV")

  # Page 365
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-08T01:52:52-00:00", "Andy just replied, said \" Already spoke to S before I went to WH. Let's talk in the morning.\"\n\nI said okay.")
  strzok_to_page(child_file, "2016-09-08T01:56:31-00:00", "--Redacted-- was there tonight but I didn't get a chance to talk with him. Probably figured I'd be furious with him about the --Redacted--")
  strzok_to_page(child_file, "2016-09-08T01:56:41-00:00", "He'd be right")
  strzok_to_page(child_file, "2016-09-08T01:56:42-00:00", "Talked to John G")
  page_to_strzok(child_file, "2016-09-08T01:57:23-00:00", "How's he doing? He's a decent human being. And not an egomaniac.")
  m = strzok_to_page(child_file, "2016-09-08T01:57:24-00:00", "Mye notwithstanding, I really like him. Huge heart")
  m.addnote("Mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-09-08T01:58:24-00:00", "And god, now I want to know what Andy said. Like Right Now.")
  strzok_to_page(child_file, "2016-09-08T01:58:30-00:00", "He's good. --Redacted--")
  strzok_to_page(child_file, "2016-09-08T01:58:31-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-08T01:58:56-00:00", "He is a very decent human being. Told him we should get lunch.")
  m = page_to_strzok(child_file, "2016-09-08T01:59:04-00:00", "He does. Bad judgement re mye, but genuinely good person.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-09-08T01:59:33-00:00", "Yep. Completely agree. And that makes him good in my book.")
  strzok_to_page(child_file, "2016-09-08T02:00:53-00:00", "Good response from Andy, I think. Right??")
  strzok_to_page(child_file, "2016-09-08T02:00:54-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-08T02:01:16-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-08T02:01:18-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-08T02:08:38-00:00", "I think it's better than thay")
  page_to_strzok(child_file, "2016-09-08T02:10:08-00:00", "I don't. He still did it to protect Steinbach.")
  strzok_to_page(child_file, "2016-09-08T02:11:51-00:00", "Not emailing, you mean?")
  strzok_to_page(child_file, "2016-09-08T02:12:49-00:00", "Wait and decide what you think after you talk.")
  strzok_to_page(child_file, "2016-09-08T02:13:09-00:00", "Same as waiting until after Bill finally talked to you")
  strzok_to_page(child_file, "2016-09-08T02:13:31-00:00", "I think (god I pray) it will be better after you talk to Andy")
  page_to_strzok(child_file, "2016-09-08T02:16:57-00:00", "Well if it's not I'll leave. Make the same amount of money, be more bored, but have a better life.")
  
  # Page 366
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-08T02:18:04-00:00", "I think it will be a good convo with Andy.")
  strzok_to_page(child_file, "2016-09-08T02:18:21-00:00", "Still want to know what --Redacted-- feedback was")
  page_to_strzok(child_file, "2016-09-08T02:23:21-00:00", "We can talk tomorrow. --Redacted--")
  strzok_to_page(child_file, "2016-09-08T09:21:24-00:00", "--Redacted-- And yeah, you're going to be angry until you clear the air with Andy.")
  page_to_strzok(child_file, "2016-09-08T10:40:09-00:00", "I know. It's complete bs. Hopefully it has the effect of snapping cyber into place so that these stupid meeting won't be necessary.")
  m = strzok_to_page(child_file, "2016-09-08T22:06:15-00:00", "And OMG CyD just gets worse. Have a story for you, --Redacted--")
  m.addnote("CyD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-09-08T22:12:39-00:00", "And yay your conversation with Andy.\U0001f60a\U0001f60a")
  strzok_to_page(child_file, "2016-09-08T22:14:56-00:00", "Is --Redacted-- there?")
  page_to_strzok(child_file, "2016-09-08T22:15:16-00:00", "--Redacted-- so around generally.")
  strzok_to_page(child_file, "2016-09-08T22:54:10-00:00", "God I want to drive by with this report...")
  page_to_strzok(child_file, "2016-09-08T23:22:44-00:00", "It went extremely well. I am grateful for his call.")
  strzok_to_page(child_file, "2016-09-08T23:24:02-00:00", "He do it on his own or at Andy/JB's urging?")
  strzok_to_page(child_file, "2016-09-08T23:24:10-00:00", "How long?")
  page_to_strzok(child_file, "2016-09-08T23:24:40-00:00", "I don't know. Am emailing/thanking/informing andy and Jb now.")
  strzok_to_page(child_file, "2016-09-08T23:33:26-00:00", "Well gosh now I want to hear about it more than you want to see the report!")
  strzok_to_page(child_file, "2016-09-08T23:38:01-00:00", "Ack!!!!! Details! Synopsis!")
  page_to_strzok(child_file, "2016-09-08T23:38:31-00:00", "It was honestly very helpful. Not that he told me anything I didn't know (7th floor is political, perception matters, etc.), but just him simply acknowledging the issues, the balancing that needs to happen, how you still won't please everyone gives me the room to include him more in the failings I report to Andy, etc.")
  page_to_strzok(child_file, "2016-09-08T23:39:31-00:00", "--Redacted-- reached out to him. I love that kid.\U0001f636")
  page_to_strzok(child_file, "2016-09-08T23:42:35-00:00", "I am lucky. Thank you too, for your friendship. I couldn't survive any of this without you.")
  strzok_to_page(child_file, "2016-09-08T23:45:29-00:00", "Not following entirely:\ngives me the room to include him more in the failings I report to Andy\n\nDoes that mean you trust him more to tell him problems?")

  # Page 367
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-08T23:51:15-00:00", "Yes, potentially. It may never happen, but at least now he has opened the door to the possibility of that happening. I'll have to explain more tomorrow, unless you can talk quickly now.")
  page_to_strzok(child_file, "2016-09-09T00:30:12-00:00", "Thank you. \U0001f636 Jon sent a text checking in, made me realize he and Bill should know.")
  strzok_to_page(child_file, "2016-09-09T00:43:06-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-09T00:58:17-00:00", "Aaron wants to get coffee at 0730 this weekend. \U0001f61d\U0001f61d\U0001f61d")
  strzok_to_page(child_file, "2016-09-09T01:02:27-00:00", "I'd like to see Aaron with you \U0001f636")
  strzok_to_page(child_file, "2016-09-09T01:55:27-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-09T01:56:04-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-09T01:56:47-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-09T01:56:59-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-09T01:57:45-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-09T01:57:46-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-09T01:57:50-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-09T02:19:02-00:00", "Matt Laurer's an idiot\nhttp://mobile.nytimes.com/2016/09/09/opinion/a-debate-disaster-waiting-to-happen.html")
  strzok_to_page(child_file, "2016-09-09T02:39:00-00:00", "--Redacted-- Glad things worked out for you, Andy and Mike \u263a")
  m = page_to_strzok(child_file, "2016-09-09T11:52:19-00:00", "It was. I'm glad mye didn't start up until the end of summer.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok(child_file, "2016-09-09T17:23:08-00:00", "--Redacted-- You need to show me that report that --Redacted-- told you about yesterday!")
  strzok_to_page(child_file, "2016-09-09T17:34:32-00:00", "Ah yes. Standby let me get it")
  page_to_strzok(child_file, "2016-09-09T17:34:58-00:00", "Sweet. --Redacted-- might be in here when you come. Just knock.")
  strzok_to_page(child_file, "2016-09-09T18:31:04-00:00", "I need my crimes report. I'll stop by on the. Way to OPA at 315")
  page_to_strzok(child_file, "2016-09-09T20:26:29-00:00", "I want to hear about --Redacted-- too!")
  strzok_to_page(child_file, "2016-09-09T20:27:13-00:00", "I don't tell Bill what Castor said, right?")
  page_to_strzok(child_file, "2016-09-09T20:27:35-00:00", "Let me.")
  page_to_strzok(child_file, "2016-09-09T20:27:49-00:00", "Not today.")

  # Page 368
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-10T00:25:43-00:00", "No prob. Just calling to say I called jason, told him everything, including having a call without him. He totally agreed. Told him I would draft TPs this weekend too, he's grateful for it.")
  strzok_to_page(child_file, "2016-09-10T00:27:32-00:00", "\u263a thanks. I'd like to help, obviously")
  m = page_to_strzok(child_file, "2016-09-10T00:28:24-00:00", "I'd appreciate it, obviously. Going to send an email to mye core team to tell them I'll draft TPs this weekend, but will likely need a look Sunday night.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-09-10T00:30:29-00:00", "\u263aStill thinking to draft on Sunday?")
  page_to_strzok(child_file, "2016-09-10T00:36:47-00:00", "Yeah, think so. Maybe Saturday night. We'll see.")
  page_to_strzok(child_file, "2016-09-10T00:51:21-00:00", "If --Redacted-- sets up the call the real test will be whether he sends me the call in info. I am angry, Pete. \U0001f621")
  strzok_to_page(child_file, "2016-09-10T00:56:08-00:00", "Just ask Andy, no? The problem is no one on that call has knowledge of the case anywhere near you. Face it, --Redacted-- was utterly absent for it. Not saying he shouldn't be there, but include Bill. And, obviously, you.")
  page_to_strzok(child_file, "2016-09-10T01:01:49-00:00", "Oh, I'll get the info. I just have a feeling I'm going to be left off \"accidentally.\"")
  page_to_strzok(child_file, "2016-09-10T01:04:58-00:00", "God, I'm really in a bad mood now.")
  page_to_strzok(child_file, "2016-09-10T01:05:07-00:00", "I hope I'm wrong.")
  strzok_to_page(child_file, "2016-09-10T01:06:19-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-10T11:50:25-00:00", "Re call, Bowdich won't set it up, --Redacted-- or whoever will. And you want to bet if he calls in?")
  page_to_strzok(child_file, "2016-09-10T11:56:35-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-10T11:58:56-00:00", "Re --Redacted-- I'm not sure he has the intellectual curiosity to call in. How's that for an insult?")
  strzok_to_page(child_file, "2016-09-10T12:16:16-00:00", "And re my last, I'd add that at this point the questions at this point are organizational risk best answered by people with throughtful smarts. And I'm not sure about the group on there, either.")
  strzok_to_page(child_file, "2016-09-10T12:37:16-00:00", "B) thing is, there are VERY inflammatory things in the 302s we didn't turn over to Congress (because they weren't relevant to understanding the focus of the investigation) that are going to come out in FOIA and absolutely inflame Congress. I'm sure Jim and Trisha and Dave and Mike are all considering how things like that play out as they talk amongst themselves.")
  strzok_to_page(child_file, "2016-09-10T12:37:38-00:00", "You never told me what she said; when I asked you pushed back a little.")
  strzok_to_page(child_file, "2016-09-10T12:37:47-00:00", "So I didn't press you on it.")

  # Page 369
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-10T12:39:01-00:00", "I'll tell you. Just didn't feel like talking about it that time you brought it up. --Redacted--")
  strzok_to_page(child_file, "2016-09-10T12:40:05-00:00", "B) and as they prep Jason. Who is going to be the first person they call. That settles it - I'm calling him, or at least giving you material so he's aware of it (which I GUARANTEE didn't come up yesterday).")
  m = strzok_to_page(child_file, "2016-09-10T12:40:30-00:00", "Want to imsg it to me, or want to do it in person?")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-09-10T12:41:05-00:00", "It's not that sensitive.")
  m = strzok_to_page(child_file, "2016-09-10T12:41:50-00:00", "Ok. You can imsg just for convenience of typing, too, if you want.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-09-10T12:44:22-00:00", "I know the material. The --Redacted-- stuff, right? I know it.")
  page_to_strzok(child_file, "2016-09-10T12:45:16-00:00", "And the state shenanigans stuff. Anything else?")
  strzok_to_page(child_file, "2016-09-10T12:48:26-00:00", "Certainly those. Probably others. All the laptops and media voluntarily turned over to us by the attorneys (\"why didnt you ever serach this\"? \"Why isnt this relevant to our oversight responsibilities\"?) I want to go read through the ones we didn't produce. The point is Reps will try and spin and attack whatever is in the ones not initially turned over to them.")
  strzok_to_page(child_file, "2016-09-10T12:53:04-00:00", "Re 302s, didn't search the laptops given to us voluntarily by various attorneys.")
  page_to_strzok(child_file, "2016-09-10T12:53:49-00:00", "Why not? Decision that it was unlikely to contain info relevant to our case in like of time constraints?")
  strzok_to_page(child_file, "2016-09-10T12:55:59-00:00", "They would not consent and we did not have probable cause to get on them.")
  # strzok_to_page(child_file, "2016-09-10T12:56:47-00:00", "I will go review the 302s we didn't turn over and send thoughts to everyone except the 0 corridor recipients. You or Trisha or Jason can mention to them.")
  # page_to_strzok(child_file, "2016-09-10T12:57:00-00:00", "Oh well that's totally defendable. Why did they give them to us?\n\nYeah, but I think that was the context in which it was meant. I.e., like who sucks more, me or her?")
  page_to_strzok(child_file, "2016-09-10T12:57:21-00:00", "--Redacted-- it's not worth your time. I've got it. Truly.")
  page_to_strzok(child_file, "2016-09-10T12:57:48-00:00", "I'll put a placeholder in - there may be more unsavory facts, these are the ones I'm aware of.")
  strzok_to_page(child_file, "2016-09-10T12:58:32-00:00", "Because they had classified on them. Classified we already had in our possession.\n\nLisa, it's a mistake not to have someone from the investigative team not quietly back banching on these conversations. I know you may not disagree. I will prep you as best I can.")
  page_to_strzok(child_file, "2016-09-10T12:59:27-00:00", "I know that! What am I supposed to do about it?!")
  page_to_strzok(child_file, "2016-09-10T13:00:10-00:00", "Call for one minute? Question about the laptops.")

  # Page 370
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-10T13:49:56-00:00", "Did you ever call the State IG re the --Redacted-- allegations?")
  page_to_strzok(child_file, "2016-09-10T13:56:46-00:00", "Can you be on the call at noon? I asked Andy, he said it was a good idea.")
  strzok_to_page(child_file, "2016-09-10T14:14:24-00:00", "Crap about ID or --Redacted-- Frankly, both. Both my fault. \U0001f621")
  page_to_strzok(child_file, "2016-09-10T14:14:35-00:00", "Okay, thanks. Sent you call in info already.")
  # page_to_strzok(child_file, "2016-09-10T14:15:05-00:00", "IG. I know is just an oversight. Just not great given timing.")
  # strzok_to_page(child_file, "2016-09-10T14:16:02-00:00", "As long as we get it to them before it comes out in FOIA I think we're ok. I will call him on Mon. Heck, I can leave a vm this weekend.")
  page_to_strzok(child_file, "2016-09-10T14:16:26-00:00", "No, Monday is fine.")
  page_to_strzok(child_file, "2016-09-10T14:16:35-00:00", "I'll try to set a reminder for us.")
  page_to_strzok(child_file, "2016-09-10T14:24:23-00:00", "Maybe it's for Bowdich. Regardless.")
  strzok_to_page(child_file, "2016-09-10T14:45:06-00:00", "Re Bowdich, I'd just let it go. Andy's going to be out for a bit so it'll get worse before it ets better. As I think about it, I don't know that I'd talk to him.")
  strzok_to_page(child_file, "2016-09-10T15:33:13-00:00", "What?!?!?!?\n\"So I'm going to ask Bill to fill in for me\"")
  page_to_strzok(child_file, "2016-09-10T15:35:54-00:00", "Yup. It's a small wonder that I don't rely on the EADs...")
  page_to_strzok(child_file, "2016-09-10T17:19:25-00:00", "I am going to go tomorrow morning after Aaron. Probably 9 am or so. Going to cancel with --Redacted-- Would be great if you can be there, but no worries if not.")
  strzok_to_page(child_file, "2016-09-10T19:32:11-00:00", "You want to answer Jason?")
  strzok_to_page(child_file, "2016-09-10T19:36:59-00:00", "Hmm. Ok.\n\nWas thinking of telling Jason his points were raised and happy to discuss. Don't want to get into a long written description of thought process on email and particularly on Samsungs...")
  page_to_strzok(child_file, "2016-09-10T19:38:04-00:00", "But I don't think we're an absolute no on this one. Just we're not going to get to subpoena (ie not going to tell the committe f no), but we're not conceding yet I don't thinkm")
  m = strzok_to_page(child_file, "2016-09-10T19:39:48-00:00", "Oh. I got the impression we were going to offer come to HQ for no PII redactions as our opening offer...")
  m.addnote("PII - Personally Identifial Information")
  page_to_strzok(child_file, "2016-09-10T19:40:03-00:00", "I can clarify.")
  strzok_to_page(child_file, "2016-09-10T19:41:55-00:00", "That was my takeaway from Andy's 2:14 email.")

  # Page 371
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-11T17:39:37-00:00", "Ok, this is *slightly* over the top. --Redacted--\n\nFBI agent climbed the ranks but chose to end his career back in a field office - The Washington Post\nhttps://www.washingtonpost.com/world/national-security/fbi-agent-climbed-the-ranks-but-chose-to-end-his-career-back-in-a-field-office/2016/09/10/7f2caa32-7605-11e6-be4f-3f42f2e5a49e_story.html")
  strzok_to_page(child_file, "2016-09-11T21:23:44-00:00", "Are you F*CKING KIDDING ME. A) That's pretty much the OPPOSITE of what was said yesterday. Kind of radically changes some of our thinking. B) Isn't it OCA's job to talk to OLA?")
  strzok_to_page(child_file, "2016-09-11T21:35:17-00:00", "Hey, let me know once you're read --Redacted-- email. How substantively does it change what we want to do? Maybe not, if we want to avoid a fight on this.")
  page_to_strzok(child_file, "2016-09-11T22:10:49-00:00", "--Redacted-- Trisha is going to be SO mad. Not only did Andy ask HER to reach out, but she even told Jason in an email to us that she had already reached out, but hadn't heard back yet.")
  page_to_strzok(child_file, "2016-09-11T22:12:08-00:00", "But no, I don't think it changes anything.")
  strzok_to_page(child_file, "2016-09-11T22:12:14-00:00", "--Redacted-- he might work himself out of contention. I'm glad that my 6th sense of dude, I don't know that you know what you're talking about/are wrong was working...")
  page_to_strzok(child_file, "2016-09-11T22:12:41-00:00", "Always with that guy. He just desperately wants to be in charge, in the know...")
  strzok_to_page(child_file, "2016-09-11T23:41:27-00:00", "Talked with Bill")
  strzok_to_page(child_file, "2016-09-12T00:20:30-00:00", "Everything. He sounded like he thought I had called him, though he dialed me. Perhaps he butt dialed.")
  strzok_to_page(child_file, "2016-09-12T00:21:35-00:00", "In any case, the week ahead. --Redacted-- He said Bowdich and Mike S aren't happy with it. Prep for Jason. His concern that we're throwing him up there, and the absence of an alternative.")
  strzok_to_page(child_file, "2016-09-12T00:21:41-00:00", "Prep for the D tomorrow.")
  m = page_to_strzok(child_file, "2016-09-12T00:33:47-00:00", "Have you been on eras to know whether anyone else edited Jason's TPs?")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-09-12T00:40:05-00:00", "Stupid WH session")
  strzok_to_page(child_file, "2016-09-12T01:10:28-00:00", "Give me a sec.\n\nAnd yeah... but --Redacted-- DID talk to Doj\U0001f612")
  page_to_strzok(child_file, "2016-09-12T10:35:45-00:00", "What time is your meeting?")
  strzok_to_page(child_file, "2016-09-12T10:36:25-00:00", "1030-1200")

  # Page 372
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-12T11:11:08-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-12T11:25:13-00:00", "Npr says Trump hotel opens today. It doesn't look ready...")
  page_to_strzok(child_file, "2016-09-12T11:26:16-00:00", "That's one place I hope I never stay in.")
  strzok_to_page(child_file, "2016-09-12T11:29:23-00:00", "Agreed. Hope it fails horribly. It wont, but still.")
  strzok_to_page(child_file, "2016-09-12T13:40:07-00:00", "Cyber blah blah blah. --Redacted-- got comments back, so I think Jason should be set")
  page_to_strzok(child_file, "2016-09-12T13:40:42-00:00", "That's great.")
  strzok_to_page(child_file, "2016-09-12T13:53:33-00:00", "Heard from SESU, pay raise waiver is at ODAG. I need to call Iris anyway, do you have her #?")
  page_to_strzok(child_file, "2016-09-12T13:54:48-00:00", "Iris is --Redacted--")
  page_to_strzok(child_file, "2016-09-12T14:30:08-00:00", "Hey btw, make sure when dale/castor lose their minds bc you were asked to go, you identify jm as the person who tapped you, not me.")
  strzok_to_page(child_file, "2016-09-12T16:05:28-00:00", "Yep, I will")
  strzok_to_page(child_file, "2016-09-12T17:47:20-00:00", "Hmm. It's paper only, that might work. Need to find Carl")
  page_to_strzok(child_file, "2016-09-12T18:08:56-00:00", "JM is going to meet with him now I think, I'd walk down to him.")
  strzok_to_page(child_file, "2016-09-12T18:15:09-00:00", "Good idea. Will try and drop in. In which case I'll be free at 4/4:30 \U0001f60a")
  strzok_to_page(child_file, "2016-09-12T18:22:37-00:00", "Carl isn't there :(\n\nMtg upstairs till 3...")
  strzok_to_page(child_file, "2016-09-12T21:09:53-00:00", "Chaffetz is horrible....")
  strzok_to_page(child_file, "2016-09-12T21:13:37-00:00", "Expected blustering. ...")
  page_to_strzok(child_file, "2016-09-12T21:13:53-00:00", "God, glad I'm not watching...")
  strzok_to_page(child_file, "2016-09-12T21:47:49-00:00", "Omg Gowdy is being a total dick. All investigative questions. And Jason isn't always sticking to the script on \"I'm not answering that.\"")
  strzok_to_page(child_file, "2016-09-12T21:47:53-00:00", "Horrible")
  strzok_to_page(child_file, "2016-09-12T21:54:47-00:00", "This was a mistake")
  # page_to_strzok(child_file, "2016-09-12T21:59:48-00:00", "Oh no")
  strzok_to_page(child_file, "2016-09-12T22:00:28-00:00", "Lis, it's bad.")

  # Page 373
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-12T22:01:12-00:00", "They aren't asking Qs on the topic. And based on the Qs, he can't defer. It's ALL posturing. He haven't done anything wrong. But we look like sh*t")
  strzok_to_page(child_file, "2016-09-12T22:17:11-00:00", "--Redacted-- in here he's leaving in a sec")
  strzok_to_page(child_file, "2016-09-12T22:33:17-00:00", "Hey. Who decided Jason would go up there?")
  page_to_strzok(child_file, "2016-09-12T22:33:42-00:00", "D. Rybicki.")
  page_to_strzok(child_file, "2016-09-12T22:33:47-00:00", "I think.")
  strzok_to_page(child_file, "2016-09-12T22:40:56-00:00", "Recessed for a vote. Back to more OPEN session at 730, followed by closed session after that.")
  strzok_to_page(child_file, "2016-09-12T22:41:07-00:00", "Call if you want to discuss")
  strzok_to_page(child_file, "2016-09-12T22:41:36-00:00", "Is Rybicki in?")
  page_to_strzok(child_file, "2016-09-12T22:43:11-00:00", "I assume so. --Redacted--")
  page_to_strzok(child_file, "2016-09-12T23:01:32-00:00", "Should have mentioned that rybicki screens. Next time leave a msg.")
  strzok_to_page(child_file, "2016-09-12T23:04:12-00:00", "Yeah well I'm not calling back.")
  strzok_to_page(child_file, "2016-09-12T23:04:56-00:00", "They can drive mitigating this...")
  strzok_to_page(child_file, "2016-09-12T23:09:06-00:00", "IMing with --Redacted-- From him. \"I can't remember a worse open hearing.\"")
  page_to_strzok(child_file, "2016-09-12T23:09:34-00:00", "Moffa?")
  strzok_to_page(child_file, "2016-09-12T23:09:48-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-12T23:10:05-00:00", "That is bad.")
  strzok_to_page(child_file, "2016-09-12T23:10:16-00:00", "Yes, that bad. I told him I was sorry he confirmed it, I thought I might not to be objective due to how close I am")
  page_to_strzok(child_file, "2016-09-12T23:10:17-00:00", "He needs to mention to andy.")
  strzok_to_page(child_file, "2016-09-12T23:11:19-00:00", "Talk, briefly? Just want to read dialogue to you")
  strzok_to_page(child_file, "2016-09-12T23:21:20-00:00", "\"It was horrendous. It was so bad, I actually plan to go back and watch the whole thing to be aware of it all.\"")
  page_to_strzok(child_file, "2016-09-12T23:23:35-00:00", "--Redacted-- said that?")
  strzok_to_page(child_file, "2016-09-12T23:24:56-00:00", "Yes. Along with one other thing I'm not writing here")
  m = page_to_strzok(child_file, "2016-09-12T23:30:57-00:00", "Oof. Imsg it?")
  m.addnote("Imsg - Strzok/Page had private iPhones to communicate without leaving evidence")

  # Page 374
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-12T23:45:18-00:00", "Man, that is not good.")
  strzok_to_page(child_file, "2016-09-12T23:45:44-00:00", "God I'm getting angry")
  page_to_strzok(child_file, "2016-09-12T23:46:07-00:00", "You should stop watching. You can't do anything about it.")
  page_to_strzok(child_file, "2016-09-12T23:46:32-00:00", "I'm frankly glad I'm not. I'm sick to my stomach and I haven't even seen a minute of it.")
  strzok_to_page(child_file, "2016-09-12T23:47:05-00:00", "I have to! We have to mitigate it!")
  page_to_strzok(child_file, "2016-09-13T01:19:23-00:00", "--Redacted-- should be here in about 15 minutes or so. Just fyi.")
  strzok_to_page(child_file, "2016-09-13T01:32:37-00:00", "And I'm trying to get lunch with --Redacted-- tomorrow, to talk about his future.")
  strzok_to_page(child_file, "2016-09-13T01:35:14-00:00", "Here you gk5\n\nFederal Officials Testify FBI's Investigation | Video | C-SPAN.org\nhttps://www.c-span.org/video/?415070-1/federal-officials-testify-fbis-investigation-hillary-clinton")
  strzok_to_page(child_file, "2016-09-13T11:52:32-00:00", "I have Many Papers and Binders. Jesus too much to do. \U0001f614")
  strzok_to_page(child_file, "2016-09-13T13:02:06-00:00", "You in yet? Waiting to talk to Andy, you should meander down if it get in in the next 15 or so.")
  strzok_to_page(child_file, "2016-09-13T13:02:16-00:00", "I'll of course fill you in later if you're not")
  page_to_strzok(child_file, "2016-09-13T13:02:59-00:00", "I'm coming down to see andy now.")
  page_to_strzok(child_file, "2016-09-13T14:53:06-00:00", "--Redacted-- Is a b*tch.")
  strzok_to_page(child_file, "2016-09-13T17:15:24-00:00", "--Redacted-- and I both noticed (i didn't mention to you earlier) we both want happy Friday Lisa back \U0001f614")
  strzok_to_page(child_file, "2016-09-13T17:44:02-00:00", "--Redacted-- and I got a TOTAL brush back from --Redacted-- and lunch. Passed without recognition, I even offered a \"Hi --Redacted--\"")
  strzok_to_page(child_file, "2016-09-13T17:44:07-00:00", "And ok, I really want to hang out. You can come watch shoot. I'm next to Carl g")
  strzok_to_page(child_file, "2016-09-13T22:31:54-00:00", "Need to talk to you about --Redacted-- mtg and email I'm sending")
  page_to_strzok(child_file, "2016-09-13T22:32:38-00:00", "Can call you from the car")
  strzok_to_page(child_file, "2016-09-13T22:38:19-00:00", "Call when you're out I'll give you an update on --Redacted-- call and --Redacted-- calls.\n\nIf you want.\n\nWill both totally wait until tomorrow")
  strzok_to_page(child_file, "2016-09-13T23:47:56-00:00", "Forgot to mention Andy this morning asked ogc to own subpoena response, JB gave it to Browder")
  page_to_strzok(child_file, "2016-09-13T23:54:35-00:00", "Copy.")
  m = strzok_to_page(child_file, "2016-09-14T09:10:57-00:00", "I cancelled my trip to mission ridge today. If you have time to talk about the --Redacted-- to D this afternoon I would appreciate it")
  m.addnote("mission ridge - Could be the Mission Ridge buildings in Chantilly, VA home of FBI Cyber Division National Cyber Investigative Joint Task Force (NCIJTF)")

  # Page 375
  # OUTBOX == Page
  # INBOX == Strzok
  m = strzok_to_page(child_file, "2016-09-14T12:23:28-00:00", "Btw, talked with Bill at length about --Redacted-- (in the context of going through what's going on). In a way that didn't burn any source, he said he hasn't had any coordination on this, that he never discussed (or wants) giving anything up, and that if anything, ITC efforts should be located within one Branch with CD and CYD and SecD. Said Steinbach also thought the same. Though of course he's out this week, all week.")
  m.addnote("CD - FBI Counterintelligence Division")
  m.addnote("CyD - FBI Cyber Division")
  m.addnote("SecD - Security Division")
  m = strzok_to_page(child_file, "2016-09-14T14:10:16-00:00", "I have the two pdbs that ran today if you want them.")
  m.addnote("pdbs - Presidential Daily Briefs?")
  strzok_to_page(child_file, "2016-09-14T14:10:42-00:00", "I do. Can I stop by?")
  strzok_to_page(child_file, "2016-09-14T17:57:23-00:00", "Crap I just stepped out of really good nsa brief on --Redacted--")
  page_to_strzok(child_file, "2016-09-14T17:57:43-00:00", "So go back in")
  strzok_to_page(child_file, "2016-09-14T18:00:59-00:00", "No, not to just leave again early.\n\nAnd \"maybe\" above? Throw me a bone.....;)")
  page_to_strzok(child_file, "2016-09-14T18:01:36-00:00", "In Andy's ofc.")
  page_to_strzok(child_file, "2016-09-14T18:01:53-00:00", "Why don't you come in and talk intc?")
  strzok_to_page(child_file, "2016-09-14T18:02:08-00:00", "Invite me...")
  strzok_to_page(child_file, "2016-09-14T18:02:54-00:00", "Outside with Castor")
  page_to_strzok(child_file, "2016-09-14T18:03:13-00:00", "He is talking to --Redacted-- right now.")
  strzok_to_page(child_file, "2016-09-14T18:08:33-00:00", "Boo. Still standing ;)")
  m = strzok_to_page(child_file, "2016-09-14T22:29:25-00:00", "Hi. You still here (hope not)? Supposed to meet Parmaan in 2...")
  m.addnote("Parmaan - C. Bryan Paarmann")
  page_to_strzok(child_file, "2016-09-14T22:35:23-00:00", "No. Why mtg with paarman?")
  strzok_to_page(child_file, "2016-09-14T23:02:53-00:00", "With a Legat over an issue. I'll tell you tomorrow. May eventually hit Andy. I'm sure you've heard of it.\n\nRemembered vaguely more detail from mtg. Andy mentioned he was still hearing (\"3 or 4 instances\") recently that info was not flowing quickly enough and more re Mike and Randy and his previous convo with them.\n\nHappy to discuss now or tomorrow. I just had 10-11 open up...")
  strzok_to_page(child_file, "2016-09-14T23:28:34-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-14T23:30:53-00:00", "So have bill call and tell him to knock it off.")

  # Page 376
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-14T23:34:06-00:00", "I already told him, then yelled at him about numbers in general, then yelled about Snowden. Not yell, but professional angry. It was very cathartic. I will invite you next time to sit at the chef's table and watch ;)\n--Redacted-- Claims edva is (/was) the delay.")
  strzok_to_page(child_file, "2016-09-15T00:47:41-00:00", "And I have no good, awful, sh*tty terrible (work) news. I can't say it here, and you can't share with Andy (yet). I'm upset.")
  m = page_to_strzok(child_file, "2016-09-15T01:10:06-00:00", "Can you share it on imsg?")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2016-09-15T01:14:55-00:00", "Yes just sent")
  strzok_to_page(child_file, "2016-09-15T16:14:49-00:00", "GREAT convo with JR, let me know when you're back....")
  page_to_strzok(child_file, "2016-09-15T16:15:18-00:00", "Sincerely good?")
  strzok_to_page(child_file, "2016-09-15T16:16:28-00:00", "But want to get your thoughts on how he might play it/spin....")
  strzok_to_page(child_file, "2016-09-15T16:28:03-00:00", "Have a 1230 with Bill to prep him for Andy, then 1 staff meeting.")
  strzok_to_page(child_file, "2016-09-15T22:49:28-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-15T23:11:21-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-15T23:11:56-00:00", "Also, Bill did not tell Andy about the loss. Background reasons why, which make sense. I can fill you in on imessage later if you want.")
  page_to_strzok(child_file, "2016-09-16T00:39:25-00:00", "Yeah really. No photos in fbi space.")
  strzok_to_page(child_file, "2016-09-16T02:59:17-00:00", "Does Andy know he hurt Jim the other day with the \"I don't have time for this\"?\n\nI think that was the purpose of his look down the table. \"See? You're right.\"")
  page_to_strzok(child_file, "2016-09-16T03:00:03-00:00", "I don't know. I plan to tell him, just haven't had the opportunity.")
  strzok_to_page(child_file, "2016-09-16T03:03:28-00:00", "Re --Redacted-- he knows he was a dick. Don't know if Jim picked up on his acknowledgement of it.")
  page_to_strzok(child_file, "2016-09-16T18:15:13-00:00", "In --Redacted-- ofc.")
  m = strzok_to_page(child_file, "2016-09-18T13:17:32-00:00", "Thanks for adding Jon and me into that email chain. I think I added you on some of that correspondence on Friday, right (re Datto)?")
  m.addnote("Datto is a managed service provider that was providing Hillary Clinton email support")
  page_to_strzok(child_file, "2016-09-18T14:53:01-00:00", "BBC is saying that bombs in NY were CT. Sucks.")
  strzok_to_page(child_file, "2016-09-18T14:55:32-00:00", "--Redacted--")

  # Page 377
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-18T14:55:52-00:00", "If it's a different thing, they're busy right now.")
  strzok_to_page(child_file, "2016-09-19T10:35:02-00:00", "Hi. Not sure I'm up for this job. Up past midnight worrying about the thing I told you about on Saturday morning. There's always going to be something to worry about. And I'm not able to turn it off right now.")
  page_to_strzok(child_file, "2016-09-19T10:51:58-00:00", "Hi. I'm sorry. We can control that part, I would try not to worry about it.")
  strzok_to_page(child_file, "2016-09-19T11:08:09-00:00", "Sorry got up super late and scrambling. I hope so, re work thing. It really bothers me. My general upset has settled into disappointment at putting Bill in a bad spot and anger at the others for having tried to do the right thing for the right reasons.")
  page_to_strzok(child_file, "2016-09-19T11:09:46-00:00", "You didn't put Bill in a bad spot. You've done exactly what he's wanted you to do.")
  strzok_to_page(child_file, "2016-09-19T12:03:13-00:00", "See, this is the crap that aggravates me: I specifically DIDN'T tell Bill about the new Intel we got on Fri on --Redacted-- so that --Redacted-- could present it. Then --Redacted-- runs in this morning and does it without me. Whatever....")
  page_to_strzok(child_file, "2016-09-19T12:25:19-00:00", "I know. But you have a LOT more access to bill than he does. It's not that important. He's feeling insecure. Let it go...")
  strzok_to_page(child_file, "2016-09-19T12:26:57-00:00", "Hmmm. Sure, but. We've got a good working relationship because stuff like this doesn't happen. I'll say something, nicely.")
  page_to_strzok(child_file, "2016-09-19T12:31:32-00:00", "Okay. And yes, Thursday works. I told Jim that --Redacted-- and I are going to have a talk with Andy, asked if I could talk to him about it first.")
  page_to_strzok(child_file, "2016-09-19T12:37:42-00:00", "And re --Redacted--, I still think I disagree. It would be one thing if he told Bill first. But why do you actually NEED to be there? --Redacted--")
  strzok_to_page(child_file, "2016-09-19T12:59:27-00:00", "B) inasmuch as --Redacted-- walked out of a meeting him and said to me, hey you need to talk to Bill about operational next steps on the guy, yes. Look, it's really not a big deal. For all i know Bill called him down. And there's a ton going on. A) good idea. I'm still thinking in should talk to JB about the issues (both our organizational one as well as the dynamic Andy may be creating without realizing it). --Redacted-- \U0001f636")
  strzok_to_page(child_file, "2016-09-19T13:02:37-00:00", "A) and then part of me thinks, this is the point. DADs should not be having lunch with the GC. Let the process work and keep my head down.")
  page_to_strzok(child_file, "2016-09-19T13:28:06-00:00", "Is there something going on around hq? Traffic is at a stand still.")
  page_to_strzok(child_file, "2016-09-19T13:33:17-00:00", "Something going on on down 9th. No cars, no pedestrians, even with badge.")
  page_to_strzok(child_file, "2016-09-19T13:36:15-00:00", "Suspicious package, my fbi ofcr just told me.")

  # Page 378
  # OUTBOX == Page
  # INBOX == Strzok
  m = page_to_strzok(child_file, "2016-09-19T13:58:24-00:00", "SSCI member brief tomorrow by cyd. You aware?")
  m.addnote("cyd - FBI Cyber Division")
  strzok_to_page(child_file, "2016-09-19T14:02:54-00:00", "I think so...members, though?\n\nAlso, walking up")
  m = page_to_strzok(child_file, "2016-09-20T00:02:26-00:00", "Forgot to mention that DD asked about what --Redacted-- was calling about. We should discuss tomorrow")
  strzok_to_page(child_file, "2016-09-20T00:07:42-00:00", "Wasn't out stuff. I have details. Shockingly not a flaming turd bag. More precisely, not one of the flaming turd bags of interest to us now.\n\nJust leaving, Bill wanted to talk. ...\n\nTtyl")
  strzok_to_page(child_file, "2016-09-20T10:15:04-00:00", "--Redacted--\n\nWork Q: were you there for discussion of SSCI appearance today? --Redacted-- did prep and is scheduled to go with Eric. Bill wants me to go - I'm not sure if it's necessary, particularly given what session was supposed to focus on. Think it would be better for him to go and defer answering stuff not on point of the briefing. Bill said Andy said no --Redacted-- but that was it.")
  strzok_to_page(child_file, "2016-09-20T10:15:39-00:00", "Did Jason say anything about the expected topics?\n\nAnd why are we doing this the DAY before the D goes up?")
  page_to_strzok(child_file, "2016-09-20T10:26:04-00:00", "--Redacted--\n\nYes, I was. We're doing it bc it was already on the calendar. Multiagency. Nothing about expected topics, just the overall topic.")
  page_to_strzok(child_file, "2016-09-20T10:27:22-00:00", "You going not a bad idea, though the goal is to try to defer a lot of it to the D tomorrow.")
  strzok_to_page(child_file, "2016-09-20T10:38:56-00:00", "Right. And --Redacted-- already prepped for the other stuff, him not knowing other stuff may help. We are already taking two, out of a three agency panel. I would need to bump him to go. I'll talk to Bill - think it might be smarter to brief him up on what not to say/red lines rather than me learn --Redacted-- stuff...")
  strzok_to_page(child_file, "2016-09-20T10:40:53-00:00", "Plus I'm supposed to talk to Glenn Fine at 145 with Baker...")
  strzok_to_page(child_file, "2016-09-20T11:11:19-00:00", "Ha. I just pulled into work. Talk to Bill quickly, send an email to 4 to remind them about TPs on --Redacted-- then off to --Redacted--")
  page_to_strzok(child_file, "2016-09-20T11:19:10-00:00", "Did you tell Bill why?")
  page_to_strzok(child_file, "2016-09-20T11:19:52-00:00", "What ever came of keeping --Redacted-- on?")
  strzok_to_page(child_file, "2016-09-20T11:40:35-00:00", "A) nope!\U0001f60a\nB) I have no idea. I made the request to --Redacted-- and Trisha. Not sure where it went, I'll ask. Neither were opposed in principle.")
  strzok_to_page(child_file, "2016-09-20T11:42:04-00:00", "--Redacted-- And while I hate it, i kinda want to walk over to the old post office and see what they've done with it. Want to go with me?")
  strzok_to_page(child_file, "2016-09-20T11:42:33-00:00", "--Redacted--")
  
  # Page 379
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-20T11:42:35-00:00", "The new Trump hotel? No.")
  page_to_strzok(child_file, "2016-09-20T11:42:49-00:00", "You've looked?")
  strzok_to_page(child_file, "2016-09-20T11:44:00-00:00", "No, only some review online.")
  strzok_to_page(child_file, "2016-09-20T11:44:55-00:00", "A) i didn't say anything. We don't have a scheduling conflict - he's upstairs...")
  strzok_to_page(child_file, "2016-09-20T11:49:20-00:00", "I'll just move my 830 with SCs every Tuesday.")
  m = strzok_to_page(child_file, "2016-09-20T16:41:43-00:00", "Omg omg omg you would not believe what CYD just proposed to put in our update for you......\n\nHope lunch is going well. Kinda really can't wait to hear.\U0001f60a")
  m.addnote("CYD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-09-20T16:45:50-00:00", "And may I please preposition a notebook in your office (and drop stuff after firearms)? Need to go straight to a mtg with Baker")
  strzok_to_page(child_file, "2016-09-20T16:55:47-00:00", "Disregard dropoff, I have all my stuff here. I would like use your office to drop stuff on the way to JB's, if I may. :)")
  strzok_to_page(child_file, "2016-09-20T19:34:41-00:00", "You with Jason? Just saw mtg invite for 3-330. I'm going to stop by now")
  strzok_to_page(child_file, "2016-09-20T20:18:36-00:00", "You rock \u263a")
  strzok_to_page(child_file, "2016-09-20T21:17:55-00:00", "Because you send quick tips like Andy wanting a brief tomorrow morning.\n\n--Redacted--")
  strzok_to_page(child_file, "2016-09-20T21:17:56-00:00", "Doj gave the letter back to you and Trisha for Jim/Andy's approval, right?")
  strzok_to_page(child_file, "2016-09-20T21:24:16-00:00", "And if I get done in time need to tell you about convo with JR on prep tomorrow as well as feedback from today")
  page_to_strzok(child_file, "2016-09-20T21:30:42-00:00", "Not Andy, the D. But thanks.")
  strzok_to_page(child_file, "2016-09-20T22:28:11-00:00", "Thanks. Still salty from even Bills reaction subsequent to talking to you. Will explain.\n\nBut thank you. Deeply.")
  strzok_to_page(child_file, "2016-09-20T23:46:07-00:00", "Good talk with Bill")
  strzok_to_page(child_file, "2016-09-20T23:46:49-00:00", "Got much more info, which I'll share. One will irritate you (not about you, about Andy)")
  strzok_to_page(child_file, "2016-09-21T00:21:15-00:00", "Well.he made the right damn decision.\U0001f636\n\nAnd I'm sorry, just reading emails. --Redacted--...")
  strzok_to_page(child_file, "2016-09-21T00:23:39-00:00", "Sorry. \"As quickly as possible.\"")
  page_to_strzok(child_file, "2016-09-21T00:27:06-00:00", "I know. I loved --Redacted-- response, will print for signature.\U0001f612")
  strzok_to_page(child_file, "2016-09-21T00:28:33-00:00", "I didn't take that as a joke or a comeback. Did you?")

  # Page 380
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-21T00:28:50-00:00", "No, just true.")
  page_to_strzok(child_file, "2016-09-21T00:31:27-00:00", "And god, that makes me angry, what you told me. I think it would make the D ripsh*t. That's exactly the opposite of what he is saying to foster.")
  strzok_to_page(child_file, "2016-09-21T00:32:22-00:00", "It's deeply angering")
  page_to_strzok(child_file, "2016-09-21T00:32:32-00:00", "I hope we have the last laugh...")
  strzok_to_page(child_file, "2016-09-21T00:33:06-00:00", "Let me stifle alternative, competent opinion by threatening future retaliation")
  page_to_strzok(child_file, "2016-09-21T00:33:12-00:00", "Andy knows the --Redacted-- There is no one more perceptive that the D, he surley does as well.")
  strzok_to_page(child_file, "2016-09-21T00:33:56-00:00", "Maybe this is all something I should talk to Baker. But that would really be breaking the code with both of the two who said it. And would be unforgivable to them")
  page_to_strzok(child_file, "2016-09-21T00:34:07-00:00", "Exactly. That is why bill needs to go get a cup of coffee or a drink with Andy, frame it in terms of protection of Andy, he needs to know what is being said behind his back.")
  page_to_strzok(child_file, "2016-09-21T00:34:40-00:00", "I think telling baker is quite wise. He already knows what I think of --Redacted-- He agrees.")
  strzok_to_page(child_file, "2016-09-21T00:34:46-00:00", "The other thing that Bill said that I thought was interesting was considered what these people will say not only in the bureau, but they might also say in the post Bureau Business world")
  strzok_to_page(child_file, "2016-09-21T00:35:08-00:00", "I'd have to wait to tell Jim. It's too close on the heels of you talking to him")
  page_to_strzok(child_file, "2016-09-21T00:35:33-00:00", "Worse case scenario, you just have to be prepared for this to be your last job in the bu. Though I do think that is unlikely.")
  page_to_strzok(child_file, "2016-09-21T00:35:55-00:00", "Just wait a couple of days. Ask to meet soon.")
  strzok_to_page(child_file, "2016-09-21T00:36:47-00:00", "Okama I definitely definitely need to get out as sac before Andy goes")
  strzok_to_page(child_file, "2016-09-21T00:36:51-00:00", "I'd work for you")
  page_to_strzok(child_file, "2016-09-21T00:38:09-00:00", "So we've got 18 months to make that happen.")
  strzok_to_page(child_file, "2016-09-21T15:58:48-00:00", "Hi. Bill and Jon re-did essentially what you and I did earlier for Mike.\U0001f612 At least we gave the same answer\n\nI find I'm really miserable. Not asking you to do anything. Kind of moping. Thanks for your patience.")
  page_to_strzok(child_file, "2016-09-21T16:01:36-00:00", "Re-did what?")
  m = strzok_to_page(child_file, "2016-09-21T16:06:09-00:00", "Go through D and DD's insa comments and said, here are the limits of what's been said (which is essentially nothing)\n\nI'm positive neww, NSC called out FBI positively in the SVTC. Yay us.")
  m.addnote("SVTC - Secure Videl Teleconference")

  # Page 381
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-21T22:31:26-00:00", "You still here? Got background on the --Redacted--....but have to go back into wrap. These are going to KILL me.")
  page_to_strzok(child_file, "2016-09-21T22:41:44-00:00", "We can talk about it tomorrow. It is not urgent. Also, --Redacted-- will need the info too.")
  strzok_to_page(child_file, "2016-09-21T23:23:59-00:00", "Great. Just had to tell a very angry --Redacted-- that Bill was posting 3 (which means --Redacted-- won't be returning there - he's currently --Redacted-- I don't enjoy this part of the job. \U0001f615")
  strzok_to_page(child_file, "2016-09-21T23:29:06-00:00", "Not going well tonight? I get the sadness and frustration, and the feeling of not doing what you'd want, but I honestly think you're too hard on yourself. I'm sorry\n\nYeah it really sucked. At least Bill did me a solid of not asking me, just called me and Dina in and said, I've told them to post 3...essentially telling a SC the Div does not have confidence in him to run the --Redacted-- program.")
  strzok_to_page(child_file, "2016-09-21T23:38:40-00:00", "--Redacted--\n\nUnrelated, your thing tomorrow afternoon is Hill, not WH, right? If so, and open (I think you or --Redacted-- said it was), you should tell your Mom and Dad to watch CSpan....")
  page_to_strzok(child_file, "2016-09-21T23:46:25-00:00", "Not open, closed, member only.")
  strzok_to_page(child_file, "2016-09-21T23:47:31-00:00", "Oh. WAH wah")
  page_to_strzok(child_file, "2016-09-21T23:49:42-00:00", "Yeah, it's really fine.")
  strzok_to_page(child_file, "2016-09-21T23:51:18-00:00", "Ha. I'm sure it is.\n\nSpeaking of, forgot to follow up on whatever sumo silliness --Redacted-- relayed...confo for lunch tomorrow")
  page_to_strzok(child_file, "2016-09-22T00:14:59-00:00", "Not really important. Just didn't want to make an inquiry of me about whether i attended some standing mtg, specifically told --Redacted-- he wanted to go through me.")
  strzok_to_page(child_file, "2016-09-22T00:17:12-00:00", "No - it was something about taping (himself?) --Redacted--")
  page_to_strzok(child_file, "2016-09-22T00:19:49-00:00", "Two Ex-Spies and Donald Trump http://nyti.ms/2cYynG6")
  strzok_to_page(child_file, "2016-09-22T11:49:59-00:00", "Having second thoughts about --Redacted-- Not sure what the other options are, though.\n\nAnyway, would like to bounce around with you")
  page_to_strzok(child_file, "2016-09-22T11:51:06-00:00", "More than --Redacted-- A spy around every corner? I'm not sure about that, but yes, we can chat.")
  strzok_to_page(child_file, "2016-09-22T11:52:17-00:00", "But much better asc and UCs in --Redacted-- ..Def let's chat")

  # Page 382
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-22T11:53:24-00:00", "Different topic, you don't think I should talk to Castor first, or both of them, or schedule a mtg rather than drop in?")
  page_to_strzok(child_file, "2016-09-22T11:55:56-00:00", "No, I wouldn't worry about castor. Schedule, maybe. Let's think about that.")
  strzok_to_page(child_file, "2016-09-22T11:59:25-00:00", "Clear through Bill then a short email, sir, do you have 15 minutes?")
  strzok_to_page(child_file, "2016-09-22T12:01:47-00:00", "The \"drop in\" seems to contrived and too great a chance that some random person would be in there....")
  strzok_to_page(child_file, "2016-09-22T12:03:26-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-22T12:15:28-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-22T15:55:32-00:00", "I'm thinking about saying something to Eric first, what do you think?")
  page_to_strzok(child_file, "2016-09-22T15:56:35-00:00", "Do it in the context of, look, this puss andy off, but I don't need a secretary second guessing something I say, and certainly, not second guessing me in front of the division. If she is that concerned, let her ask andy.")
  page_to_strzok(child_file, "2016-09-22T15:57:06-00:00", "*this will piss andy off.")
  strzok_to_page(child_file, "2016-09-22T16:45:14-00:00", "I think that's smart. How do explain that you know that she did it?")
  strzok_to_page(child_file, "2016-09-22T16:46:13-00:00", "Any thought going direct with --Redacted-- I don't think that's a good idea.")
  strzok_to_page(child_file, "2016-09-22T16:54:33-00:00", "And God, I haven't stopped, with no end in sight. I know you're the same.\n--Redacted--")
  page_to_strzok(child_file, "2016-09-22T17:33:09-00:00", "I'm just going to make reference to her going to a division to question my judgement. If he asks I'll say CD, but there are plenty of people I could have heard it from, I'm friends with lots of people on that division.")
  strzok_to_page(child_file, "2016-09-22T18:48:38-00:00", "3-4, right? I know you're excited.\U0001f60a\n\nBtw, afternoon D session invites didn't go. What time, so Jon and I can block?")
  page_to_strzok(child_file, "2016-09-22T18:49:08-00:00", "No clue. --Redacted-- hasn't sent it yet. God I hate her.")
  page_to_strzok(child_file, "2016-09-22T18:50:23-00:00", "Email says 3:30-4:30, but those times can be a little flex.")
  strzok_to_page(child_file, "2016-09-22T18:50:32-00:00", "Hey, also note that when --Redacted-- responded to her, he also cc:ed me and Jon, then --Redacted-- responded \"thanks\" to all of us.")
  page_to_strzok(child_file, "2016-09-22T18:51:03-00:00", "Yup, I know. That's my point, it could be you, jon, --Redacted-- bill")

  # Page 383
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-22T18:52:47-00:00", "Got it, thanks\n\nI'm all good for you to use me as source of email, just gotta have a logical answer. \"Pete sent the email asking me what the D expected/wanted\" I think would make sense. If it even comes p")
  strzok_to_page(child_file, "2016-09-22T18:54:21-00:00", "While I hate Congress, there's something about all of it together at once.\n\nCurious how many actually show....\n\nCivics nerds, we are")
  strzok_to_page(child_file, "2016-09-22T20:40:47-00:00", "I'm covering wrap with EAD for Bill....")
  page_to_strzok(child_file, "2016-09-22T20:47:11-00:00", "We are just leaving the Hill now. I expect it will be a late night.")
  strzok_to_page(child_file, "2016-09-22T22:10:30-00:00", "(asking because talking to Bill, I can easily break away, though)")
  page_to_strzok(child_file, "2016-09-22T22:16:58-00:00", "I am. Might try to sit on a 6:30 call with andy though.")
  m = strzok_to_page(child_file, "2016-09-22T22:18:47-00:00", "Talking with Sporre now about your call....")
  m.addnote("Sporre - Eric W. Sporre, deputy assistant directory of Cyber Operations Branch in Cyber Division at FBI headquarters")
  page_to_strzok(child_file, "2016-09-22T22:19:16-00:00", "My call? I met with him.")
  strzok_to_page(child_file, "2016-09-22T22:42:47-00:00", "No. You're upcoming call with --Redacted--")
  page_to_strzok(child_file, "2016-09-23T11:30:17-00:00", "You are not going to leave your all hands early. You are a DAD.")
  strzok_to_page(child_file, "2016-09-23T11:30:29-00:00", "And --Redacted-- just sent the cyber/cd D invite...")
  page_to_strzok(child_file, "2016-09-23T11:30:30-00:00", "Probably 45 or so. We'll see.")
  page_to_strzok(child_file, "2016-09-23T11:31:02-00:00", "Not to me yet. Am I on there?")
  strzok_to_page(child_file, "2016-09-23T11:31:08-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-23T11:31:37-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-23T11:31:42-00:00", "No....\n\nAnd head explodes in 3...2...1")
  page_to_strzok(child_file, "2016-09-23T11:31:59-00:00", "Jesus.\U0001f621")
  page_to_strzok(child_file, "2016-09-23T11:32:17-00:00", "I am simply going to send another f-ing email, cc Eric. AGAIN.")
  m = page_to_strzok(child_file, "2016-09-23T11:32:24-00:00", "She fix the mye one?")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-09-23T11:32:39-00:00", "Want me to forward to you? \U0001f61c")
  page_to_strzok(child_file, "2016-09-23T11:33:05-00:00", "No, she can see that.")
  m = page_to_strzok(child_file, "2016-09-23T11:37:07-00:00", "So I'm going to forward the original email, and write, \"Hi --Redacted-- Thanks for updating the CD/CyD meeting. Could you please add me as well?\" Nothing wrong with that, right?")
  m.addnote("CD - FBI Counterintelligence Division")
  m.addnote("CYD - FBI Cyber Division")

  # Page 384
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-23T12:14:44-00:00", "Hey the picked 2 SACs for NY yesterday. Let me know if you hear --Redacted-- name...Mike said something that made me hopeful")
  page_to_strzok(child_file, "2016-09-23T13:14:57-00:00", "I'm almost there.")
  page_to_strzok(child_file, "2016-09-23T13:15:08-00:00", "Though I forgot the paper. \U0001f612")
  strzok_to_page(child_file, "2016-09-23T14:33:43-00:00", "Hey let's find 30 min to tweak editorial and add voter stuff. You ok if I hit Rybicki for latest version?")
  page_to_strzok(child_file, "2016-09-23T15:49:40-00:00", "I did not go. Let go. I'm furious at --Redacted-- again.")
  page_to_strzok(child_file, "2016-09-23T15:55:23-00:00", "I'm waiting for Jim B. I'll be done noon.")
  strzok_to_page(child_file, "2016-09-23T15:56:03-00:00", "What'd she do? Other than be crappy?")
  strzok_to_page(child_file, "2016-09-23T16:00:32-00:00", "Hey heads up im in your office")
  strzok_to_page(child_file, "2016-09-23T16:47:02-00:00", "Ridiculous, right? I'm waiting to see if --Redacted-- called to ask him, cam you just send Pete?")
  page_to_strzok(child_file, "2016-09-23T16:57:44-00:00", "Yes, please find out.")
  strzok_to_page(child_file, "2016-09-23T21:02:41-00:00", "You still around? Would like to talk to you before leaving.")
  page_to_strzok(child_file, "2016-09-23T21:06:26-00:00", "Yuo")
  page_to_strzok(child_file, "2016-09-23T21:14:02-00:00", "Headed to my scif. Just knock there")
  strzok_to_page(child_file, "2016-09-24T00:47:18-00:00", "Don't feel like crying. He was a dick. And if he's an SES, and about to be an SAC, he needs more maturity and consideration")
  page_to_strzok(child_file, "2016-09-24T00:49:42-00:00", "I do. Fighting tears at the table.")
  page_to_strzok(child_file, "2016-09-24T00:49:49-00:00", "I'm not happy.")
  strzok_to_page(child_file, "2016-09-24T00:50:34-00:00", "I know. I want to go confront him. That would not end well for any of us (him, me, you) on a number of levels.")
  strzok_to_page(child_file, "2016-09-24T00:51:33-00:00", "Best I can tell you us try and see his offering an insight into his admission of his own weakness and insecurity and try and take that in the best possible light.")
  m = strzok_to_page(child_file, "2016-09-24T18:06:40-00:00", "Hey. Work Q. CyD is doing some big thing for the D still. Do you think we'd be ok giving separate products to him? Ours is (good and concise and) done, I want to avoid our guys having to come in tomorrow to fight through editing a joint product.")
  m.addnote("CyD - FBI Cyber Division")
  m.addnote("D - Director FBI")
  strzok_to_page(child_file, "2016-09-24T18:07:45-00:00", "Disregard. We're going to send them what we've got and let them incorporate it into theirs.")
  page_to_strzok(child_file, "2016-09-24T19:21:55-00:00", "D's PC is from 11:30-1, so yeah, it's going to have to be right first thing Monday.")
  
  # Page 385
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-24T19:24:35-00:00", "Work talk quickly?")
  strzok_to_page(child_file, "2016-09-24T20:05:25-00:00", "--Redacted-- What did he think? Have you come to any ideas about how you'd like to address some of the work stuff?")
  page_to_strzok(child_file, "2016-09-24T20:03:37-00:00", "No. Just that I need to find my --Redacted-- The conversation was mostly he and I, work and --Redacted-- But at least he knows how I feel about a whole mix of things now.")
  m = strzok_to_page(child_file, "2016-09-24T20:50:27-00:00", "And \U0001f621\U0001f621\U0001f621\U0001f621\U0001f621\U0001f621 eras just disconnected and I lost the mye prep email I was writing.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-09-24T20:58:08-00:00", "Whew. Was able to recover it, and just sent")
  strzok_to_page(child_file, "2016-09-24T22:21:21-00:00", "The Mystery of Trump\u2019s Man in Moscow - POLITICO Magazine\nhttp://www.politico.com/magazine/story/2016/09/the-mystery-of-trumps-man-in-moscow-214283")
  m = strzok_to_page(child_file, "2016-09-25T20:49:05-00:00", "Walking to the office, see what CYD put together...not holding my breath")
  m.addnote("CYD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-09-25T20:58:54-00:00", "--Redacted--\n\nOf course, cyber sent everyone home without sending the doc to review. AFTER specifically asking us to come in today to chop....\n\nI AM SO MAD")
  page_to_strzok(child_file, "2016-09-25T21:02:56-00:00", "You should call spore right f-ing now.")
  strzok_to_page(child_file, "2016-09-25T21:04:46-00:00", "Talking to him now. They're on the S side, with less detail.")
  strzok_to_page(child_file, "2016-09-25T21:22:22-00:00", "Well, it's not bad. THey feel compelled to add/adjust things in our section, which is irritating (much more so to Jon than me). \U0001f612 But we should have something tonight.\n\nFinally, it's A PAGE AND A HALF. Jon and I were laughing the two of us could probably do that in 40 minutes...")
  page_to_strzok(child_file, "2016-09-26T00:21:27-00:00", "Note the BCC. I'm inclined to say no.")
  m = strzok_to_page(child_file, "2016-09-26T00:36:38-00:00", "And def i would not send our (CD) stuff. I got the impression from Andy there was some question if the D would want to use the --Redacted-- info into the PC.\n\nI need to make sure CYD knows not to send it far and wide. I can see them messing that up.\n\nAnd if the background - that the community is saying it's all our fault and waiting for us, I wouldn't want to play into that in unexpected ways.")
  m.addnote("CD - FBI Counterintelligence Division")
  m.addnote("CYD - FBI Cyber Division")
  m.addnote("D - Director FBI")

  page_to_strzok(child_file, "2016-09-26T00:45:59-00:00", "I would email sporre tonight so that he knows to limit distribution.")

  # Page 386
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-26T00:48:25-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-26T00:48:52-00:00", "Re Sporre, I did.")
  page_to_strzok(child_file, "2016-09-26T00:49:12-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-26T00:50:16-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-26T00:50:40-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-26T12:44:13-00:00", "I know I need to watch it, but I'm not sure I have the stomach for the debate tonight.")
  page_to_strzok(child_file, "2016-09-26T12:50:44-00:00", "Turns out I don't want to go to work. Apparently it's the biggest source of my issues.")
  strzok_to_page(child_file, "2016-09-26T12:52:43-00:00", "--Redacted-- I don't want to watch the debate either, but I will")
  strzok_to_page(child_file, "2016-09-26T12:53:41-00:00", "And re work issues, did you decide what, if anything, you want to do with --Redacted-- and Eric?")
  strzok_to_page(child_file, "2016-09-26T12:54:01-00:00", "Eric getting a job will help...but who knows how long that will be")
  strzok_to_page(child_file, "2016-09-26T12:55:25-00:00", "I'm busy responding to work emails from the week of Aug 15th that got stuck unread. Yep, it's pretty pathetic to say thanks for the job congratulations a MONTH after the fact")
  strzok_to_page(child_file, "2016-09-26T12:56:11-00:00", "I agree with you, but not following \"no one is going to do it for me\" you mean make you prioritize them?")
  m = page_to_strzok(child_file, "2016-09-26T19:20:02-00:00", "Could you bring up that CD/CyD doc?")
  m.addnote("CD - FBI Counterintelligence Division")
  m.addnote("CYD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-09-26T23:44:26-00:00", "Just rode the elevator down with Andy, had a nice convo. He went thru some of the stuff you shared earlier. \U0001f60a")
  page_to_strzok(child_file, "2016-09-26T23:46:24-00:00", "Work stuff?")
  page_to_strzok(child_file, "2016-09-27T00:33:25-00:00", "Did you read this? It's scathing. And I'm scared.\n\nWhy Donald Trump Should Not Be President http://nyti.ms/2dbQPuR")
  page_to_strzok(child_file, "2016-09-27T00:40:43-00:00", "Man, I should have started drinking earlier. I'm genuinely stressed about the debate.")
  page_to_strzok(child_file, "2016-09-27T01:06:47-00:00", "Oh god, she's already boring.")
  strzok_to_page(child_file, "2016-09-27T01:08:20-00:00", "I know. 100% produced. And I REALLY don't think she's that bad. She just can't escape the formula....")
  m = page_to_strzok(child_file, "2016-09-27T01:10:33-00:00", "She can't. Can you imsg instead?")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-09-27T01:11:09-00:00", "Btw, is he a gtown grad? No way...")

  # Page 387
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-27T01:12:40-00:00", "--Redacted-- B) masters degree. He told me after some briefing where D and Jon made of their Gtwn - William and Mary riffs....")
  page_to_strzok(child_file, "2016-09-27T01:13:49-00:00", "Wow, really? Masters in what?")
  strzok_to_page(child_file, "2016-09-27T09:50:46-00:00", "Hi. I don't know. --Redacted--")
  strzok_to_page(child_file, "2016-09-27T10:37:52-00:00", "Can I ask you a question about yesterday's discussion? Why rule out a job ad Doj. Not NSD or ODAG?")
  strzok_to_page(child_file, "2016-09-27T10:38:13-00:00", "Too political?")
  page_to_strzok(child_file, "2016-09-27T10:39:43-00:00", "No way. I don't see what I get out of that, and I'd have to deal with all the political BS.")
  strzok_to_page(child_file, "2016-09-27T10:40:32-00:00", "Political connections. Better entree into other jobs? Maybe not the latter.")
  strzok_to_page(child_file, "2016-09-27T11:44:15-00:00", "Npr just mentioned jeh appearing before Congress today. No mention of the FBI.")
  page_to_strzok(child_file, "2016-09-27T11:48:48-00:00", "Jeh? Hoover risen from the dead?")
  page_to_strzok(child_file, "2016-09-27T11:49:01-00:00", "Oh. Jeh Johnson. Right.")
  page_to_strzok(child_file, "2016-09-27T11:49:27-00:00", "Honestly, that's good. The less people ask of us the better. I need a tv in my office. \U0001f621")
  strzok_to_page(child_file, "2016-09-27T13:26:49-00:00", "Just seeing if I could reach you. Bill having Thoughts about the PC yesterday\n\nAlso per agency they may have them every Mon.")
  strzok_to_page(child_file, "2016-09-27T13:29:08-00:00", "K.\n\nGet the intel report!:)\n\nAbout to talk with Scott. But that should be s shirt meeting")
  strzok_to_page(child_file, "2016-09-27T13:29:09-00:00", "Short meeting. Not shirt meeting. We both have shirts.")
  page_to_strzok(child_file, "2016-09-27T13:36:32-00:00", "Going to go see moffa now. With report.;)")
  strzok_to_page(child_file, "2016-09-27T13:37:10-00:00", "Irritatingly, I am waiting on Scott for an SSA who went in at 955 for \"a quick 5 minutes\" \U0001f612")
  page_to_strzok(child_file, "2016-09-27T14:52:35-00:00", "I'm watching the D. He is so impressive.")
  strzok_to_page(child_file, "2016-09-27T17:35:02-00:00", "You nearby? In your office")
  page_to_strzok(child_file, "2016-09-27T17:37:36-00:00", "No. Down with andy. May not be back")
  strzok_to_page(child_file, "2016-09-27T19:50:27-00:00", "Hi! I'm jealous about your Hill trip (again) --Redacted--")
  page_to_strzok(child_file, "2016-09-27T20:43:45-00:00", "Today's was more contentious, but more cool, because I recognize most of them.")
  strzok_to_page(child_file, "2016-09-27T20:59:27-00:00", "Doing Judiciary prep with Rybicki think I'll be done before you")

  # Page 388
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-27T21:25:02-00:00", "Hi. And the prep was with Rybicki AND the D. I like my job sometimes.")
  strzok_to_page(child_file, "2016-09-27T21:25:29-00:00", "Call my desk when you're done, I may need an assist shooing someone off")
  strzok_to_page(child_file, "2016-09-27T21:34:50-00:00", "Never mind, he left. Just hit me here when you're done. You can tell me Senate stories \U0001f60a")
  strzok_to_page(child_file, "2016-09-27T22:06:11-00:00", "Hey you done? Bill's been back, trying to avoid getting pulled into a convo...I may go hide somewhere \U0001f636")
  page_to_strzok(child_file, "2016-09-27T22:12:21-00:00", "Done now")
  strzok_to_page(child_file, "2016-09-27T23:52:02-00:00", "Sheesh. Just leaving. Talked to --Redacted-- you can't tell him yet you know that), you lawyers sure can talk ;)")
  page_to_strzok(child_file, "2016-09-27T23:59:53-00:00", "NO ONE talks more than --Redacted-- He talk to you about --Redacted--?")
  strzok_to_page(child_file, "2016-09-28T00:02:23-00:00", "No this is about thing Baker got a call on. What's --Redacted--")
  strzok_to_page(child_file, "2016-09-28T00:06:20-00:00", "Ah. No. I didn't mention. And I've got to follow up with Bill on that following our conversation.")
  strzok_to_page(child_file, "2016-09-28T00:08:27-00:00", "Anyway, have a 10 o'clock link call with him and --Redacted-- You should get the deputy to assign you so you can come play with us.;)\n\nHonestly, it doesn't need the deputies office involved, but I know we're all cool, and you like the cool kids \U0001f60a")
  page_to_strzok(child_file, "2016-09-28T00:12:50-00:00", "I DO want to be part of that call!\U0001f60a")
  strzok_to_page(child_file, "2016-09-28T10:45:25-00:00", "I know! That's why I'm admonishing you.\n\nOh - remind me to tell you what Bill said about Eric last night. You haven't talked to him about him, have you?")
  page_to_strzok(child_file, "2016-09-28T11:09:45-00:00", "I haven't talked to whom? Bill? Eric? Answer is no to both.")
  strzok_to_page(child_file, "2016-09-28T11:16:02-00:00", "Ha. Ok. You won't be surprised. \U0001f612 Not about you.")
  m = page_to_strzok(child_file, "2016-09-28T13:13:08-00:00", "Goodlatte opened with the mye stuff")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  m.addnote("Goodlatte - House Judiciary Committee Chairman Bob Goodlatte ")
  strzok_to_page(child_file, "2016-09-28T13:14:36-00:00", "Today? Is it on now?")
  page_to_strzok(child_file, "2016-09-28T13:14:52-00:00", "Yes. Started at 9.")
  page_to_strzok(child_file, "2016-09-28T13:15:09-00:00", "I'm in the D's conference roo. Watching with rybicki et al")
  strzok_to_page(child_file, "2016-09-28T13:16:48-00:00", "Oh. Boo. I was going to stop by...\n\nHow's he doing?")
  strzok_to_page(child_file, "2016-09-28T13:17:36-00:00", "Who was the npr interview?")
  page_to_strzok(child_file, "2016-09-28T13:17:45-00:00", "Just remember opening remarks")
  page_to_strzok(child_file, "2016-09-28T13:17:59-00:00", "I'm not sure I am going to be able to stomach all of this.")

  # Page 389
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-28T13:18:18-00:00", "I'm not telling re npr! I want to listen together.\U0001f636")
  page_to_strzok(child_file, "2016-09-28T13:18:52-00:00", "We're watching online.")
  strzok_to_page(child_file, "2016-09-28T13:19:01-00:00", "I don't have it on CSpan 1 2 or 3")
  strzok_to_page(child_file, "2016-09-28T13:19:07-00:00", "CSpan?")
  page_to_strzok(child_file, "2016-09-28T13:19:21-00:00", "I'm sure, yes. Are you fee? Come up?")
  strzok_to_page(child_file, "2016-09-28T13:19:45-00:00", "Ok with everyone there?")
  strzok_to_page(child_file, "2016-09-28T13:19:58-00:00", "Until 10...")
  strzok_to_page(child_file, "2016-09-28T13:20:39-00:00", "Oh re npr \U0001f636 --Redacted--")
  strzok_to_page(child_file, "2016-09-28T13:41:53-00:00", "--Redacted-- And I'm so f*cking proud that we nailed all these Qs in advance of the prep \u263a")
  strzok_to_page(child_file, "2016-09-28T14:57:21-00:00", "--Redacted-- I can miss my 130 no problem (frankly, a SC - level meeting, but need to be here by 2")
  strzok_to_page(child_file, "2016-09-28T14:58:45-00:00", "Np. Iris and --Redacted--")
  page_to_strzok(child_file, "2016-09-28T15:13:33-00:00", "Trisha needs to talk at 1. What time is you 2:00 meeting over?")
  strzok_to_page(child_file, "2016-09-28T15:18:20-00:00", "B\xf6\xf4\xf5\n\n230. Gotta be back at 345.\n\nWhat are you doing for lunch.")
  m = strzok_to_page(child_file, "2016-09-28T15:21:19-00:00", "Still talking midyear?")
  m.addnote("midyear - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-09-28T15:21:32-00:00", "I worry the appearance to JR and --Redacted--")
  strzok_to_page(child_file, "2016-09-28T15:21:40-00:00", "You think OK?")
  page_to_strzok(child_file, "2016-09-28T15:21:41-00:00", "Yup. Gowdy now.")
  page_to_strzok(child_file, "2016-09-28T15:21:56-00:00", "Yup. Why not. Kortan here too.")
  page_to_strzok(child_file, "2016-09-28T16:06:16-00:00", "I know. Me too. I have to meet with Trisha at 1. Maybe eat after that?")
  strzok_to_page(child_file, "2016-09-28T16:07:18-00:00", "Sure if there's time before my 2. Trisha meeting brief?")
  strzok_to_page(child_file, "2016-09-28T16:13:03-00:00", "--Redacted-- sending me emails about the number of people in the room. \U0001f612 Yes, I was there.\n\nHas D said anything about #s of people in the interview?")
  strzok_to_page(child_file, "2016-09-28T16:15:20-00:00", "You need help? I can step out in a few...")

  # Page 390
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-28T16:17:54-00:00", "Your sacs badge is in here..")
  strzok_to_page(child_file, "2016-09-28T19:07:56-00:00", "Cyber fucked everything up wiht Iris and --Redacted-- I have calls in to both")
  page_to_strzok(child_file, "2016-09-28T19:10:07-00:00", "You are kidding me. \U0001f621 How so?")
  page_to_strzok(child_file, "2016-09-28T19:28:47-00:00", "Hey, just called you back.")
  strzok_to_page(child_file, "2016-09-28T19:31:36-00:00", "Sorry talking to Iris, --Redacted-- calling 3:30. Which I guess was 2 minutes ago.")
  strzok_to_page(child_file, "2016-09-28T21:28:23-00:00", "Sorry. A lot of poeple want a lot of time. Not all of them need it. Didn't gatekeep for Andy as EAD, or was it better at that level? Can't imagine it would be")
  page_to_strzok(child_file, "2016-09-28T21:28:54-00:00", "No, he had --Redacted-- to do that for him.")
  strzok_to_page(child_file, "2016-09-28T21:28:56-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-28T21:29:12-00:00", "--Redacted--")
  m = strzok_to_page(child_file, "2016-09-28T23:25:31-00:00", "Got called up to Andy's earlier...hundreds of thousands of emails turned over by Weiner's atty to sdny, includes a ton of material from spouse.\U0001f628\n\nSending team up tomorrow to review...this will never end....")
  m.addnote("This is one month before Comey notified Congress of the 141,000 emails")
  page_to_strzok(child_file, "2016-09-28T23:27:03-00:00", "Turned over to them why?")
  strzok_to_page(child_file, "2016-09-28T23:28:24-00:00", "Apparently one of his recent texting partners may not have been 18...don't have the details yet")
  page_to_strzok(child_file, "2016-09-28T23:29:00-00:00", "Yes, reported 15 in the news.")
  strzok_to_page(child_file, "2016-09-28T23:31:15-00:00", "And funny. Bill and I were waiting outside his door. He was down with the director. --Redacted-- saw us from the inner hallway, made a point of coming over to see what it was that we were talking about. We didn't know. I think --Redacted-- is a little bit of a busybody.")
  page_to_strzok(child_file, "2016-09-28T23:32:17-00:00", "He us a busy body. Not to be trusted.")
  strzok_to_page(child_file, "2016-09-28T23:34:14-00:00", "Tell me.....")
  strzok_to_page(child_file, "2016-09-28T23:51:57-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-29T01:08:50-00:00", "And suddenly I'm realizing, they're like Trump demographic people, just democrats.\U0001f612")
  m = strzok_to_page(child_file, "2016-09-29T01:10:29-00:00", "--Redacted-- I need to send you what my --Redacted-- has been sending. The liberal media is all in the tank for Hillary. Because, you know, Trump isn't batsh*t crazy for our country...")
  m.tag("Hatred", "batshit crazy is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)

  # Page 391
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-09-29T01:11:38-00:00", "Please don't. I really don't want to know what is out there.")
  strzok_to_page(child_file, "2016-09-29T01:14:28-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-09-29T01:15:53-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-29T01:18:16-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-29T01:18:29-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-29T01:19:06-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-09-29T01:50:27-00:00", "Republicans Just Cannot Let The Clinton Emails Go | Huffington Post\nhttp://m.huffpost.com/us/entry/us_57ec1965e4b082aad9b8c728")
  strzok_to_page(child_file, "2016-09-29T01:53:27-00:00", "\"Found it hard to focus\"?\n\n\"Found it hard to focus\"?!?!??!\n\nAre you f*cking kidding me?!??!!\n\nDonald Trump got too much debate advice, so he took none of it.\nhttp://www.slate.com/blogs/the_slatest/2016/09/28/donald_trump_got_too_much_debate_advice_do_he_took_none_of_it.html")
  strzok_to_page(child_file, "2016-09-29T14:08:10-00:00", "Ran into Bill, he was trying to get a hold of Jim, who was in with his Deputies. Secretary offered to grab him but Bill said no")
  strzok_to_page(child_file, "2016-09-29T14:08:29-00:00", "He's calendared to go to the session board. Does he normally do that?")
  strzok_to_page(child_file, "2016-09-29T21:17:11-00:00", "Hey are you able to step out to grab the product we discussed with andy? They want it cleared tonight")
  strzok_to_page(child_file, "2016-09-29T23:46:34-00:00", "Hey I honestly did not know the specific reason for the concern, other than what I told you. Thats why I was answering as I did, to see if he'd provide more detail.")
  strzok_to_page(child_file, "2016-09-29T23:46:58-00:00", "It was a convo between him, Jim and Kortan....")
  strzok_to_page(child_file, "2016-09-29T23:49:58-00:00", "You also left your --Redacted-- update. Let me know when, I'll bring it up before you go. \U0001f636")
  strzok_to_page(child_file, "2016-09-30T01:42:15-00:00", "Hey I'm almost home, sorry. Remind me tomorrow what --Redacted-- said.")
  strzok_to_page(child_file, "2016-09-30T11:16:33-00:00", "And do you still have that O'Reilly article about the D? I can't find it")
  page_to_strzok(child_file, "2016-09-30T11:31:00-00:00", "--Redacted-- Wasn't an article, was Jason telling me that O'Reilly was critical.")
  
  # Page 392
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-09-30T11:45:34-00:00", "--Redacted-- Yeah I could only find some a-hole blogger who was going on his show.\n\nI am really tired of these people who are so blind with extreme belief and hatred of the Clintons that ANYTHING that does not fit their world view must be corrupt or incompetent.")
  strzok_to_page(child_file, "2016-09-30T12:19:07-00:00", "Omg I need to talk to you \U0001f621\n\nIt obviously can wait, but I just had a flash of two more years of cyber dysfunction")
  strzok_to_page(child_file, "2016-09-30T23:05:07-00:00", "Yeah, --Redacted-- is awesome! She coordinated that response apparently with absolutely no one in CD. Because, you know, she was doing it.")
  strzok_to_page(child_file, "2016-09-30T23:05:23-00:00", "Even though she's had a sum total of 0 interaction on the topic before this afternoon.")
  page_to_strzok(child_file, "2016-09-30T23:08:05-00:00", "Yeah, that's incredibly aggravating. You call her, figure out where it went?")
  strzok_to_page(child_file, "2016-09-30T23:36:01-00:00", "Check email")
  page_to_strzok(child_file, "2016-10-01T00:37:48-00:00", "Worse than anticipated, no?")
  strzok_to_page(child_file, "2016-10-01T00:44:00-00:00", "The article? Not sure")
  page_to_strzok(child_file, "2016-10-01T00:45:45-00:00", "Yeah, I couldn't tell either.")
  strzok_to_page(child_file, "2016-10-01T00:50:38-00:00", "The same reporter wrote an article about --Redacted-- that was completely wrong...")
  page_to_strzok(child_file, "2016-10-01T01:01:35-00:00", "Well that's good at least.")
  strzok_to_page(child_file, "2016-10-01T01:11:10-00:00", "I think so. Don't think this will be too bad. I hope.\n\nAnd hi")
  strzok_to_page(child_file, "2016-10-01T12:23:06-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-01T13:56:16-00:00", "--Redacted-- And finished that Politico article. Pretty good and accuarte, all in all")
  strzok_to_page(child_file, "2016-10-02T01:14:31-00:00", "Holy sh*t. You see the NYT feed? No taxes for 20 years...")
  strzok_to_page(child_file, "2016-10-02T12:16:35-00:00", "--Redacted-- And you should YouTube the opening SNL skit. It was really funny.")
  strzok_to_page(child_file, "2016-10-02T13:20:54-00:00", "Ooh. Yay. I'll check it out. Did you watch the SNL opener?")

  # Page 393
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-02T13:22:20-00:00", "No, not yet. But --Redacted-- texted me too and told me we had to watch it.")
  m = strzok_to_page(child_file, "2016-10-02T13:26:59-00:00", "--Redacted-- Working on ERAS. Just emailed Sporre to essentially say are you SURE you have absolutely no update for the D from last week? (Because I know you do) \U0001f612")
  m.addnote("ERAS - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-10-02T13:27:01-00:00", "I'm also going to email Bill and ask him to say we need a 5 minute carve out at the beginning or end to --Redacted-- and sensitive agency stuff. We can't do that with 20 people there.")
  strzok_to_page(child_file, "2016-10-02T13:37:48-00:00", "Oh. And watch snl campaign family feud. Putin is on Trumps team. Hilarious.")
  page_to_strzok(child_file, "2016-10-02T14:07:58-00:00", "I would just email Bill and rybicki at the same time.")
  strzok_to_page(child_file, "2016-10-02T16:06:19-00:00", "Sigh. I'm sitting here working. --Redacted--")
  page_to_strzok(child_file, "2016-10-03T12:12:47-00:00", "Damn. Might have made it for the D brief, except that there are a billion people in line trying to get in. \U0001f612")
  strzok_to_page(child_file, "2016-10-03T19:36:29-00:00", "Hi. Getting coffee with Jon and --Redacted--")
  strzok_to_page(child_file, "2016-10-03T20:35:24-00:00", "Ooh, and I have personnel gossips")
  strzok_to_page(child_file, "2016-10-03T21:01:44-00:00", "And just got back at --Redacted-- for his DAD demotion comment. \u263a")
  strzok_to_page(child_file, "2016-10-03T21:02:30-00:00", "Going to sign my PAR")
  m = strzok_to_page(child_file, "2016-10-04T17:43:39-00:00", "Cartwright took the plea! --Redacted--")
  m.addnote("Cartwright - General James E. Cartwright - Lying to investigators about classified leak")
  strzok_to_page(child_file, "2016-10-05T01:00:23-00:00", "TPs sent. Wasn't able to link up with --Redacted--")
  strzok_to_page(child_file, "2016-10-05T01:06:42-00:00", "Tried calling, luncing, and emailing")
  page_to_strzok(child_file, "2016-10-05T01:11:02-00:00", "He texted me at 836 to ask if I could talk, i said yes at 9, but no reponse yet.")
  strzok_to_page(child_file, "2016-10-05T01:15:33-00:00", "Ok,: that's a little aggravating. Maybe he was out and just had his phone. Please let me know if there's anything relevant so I can answer if somebody asks me a question. Thanks.")
  page_to_strzok(child_file, "2016-10-05T01:19:01-00:00", "He probably had just left already.")
  page_to_strzok(child_file, "2016-10-05T01:27:34-00:00", "He just wrote me back\n\nah never mind. We just talked to --Redacted-- Will fill every body tomorrow.")
  strzok_to_page(child_file, "2016-10-05T01:30:42-00:00", "Thanks\n\nThen I'm going to let Bill run up the chain tomorrow morning what's in his inbox now, you can adjust Andy later as needed.")

  # Page 394
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-05T01:39:36-00:00", "--Redacted-- just called me. Can you talk?")
  strzok_to_page(child_file, "2016-10-05T01:55:21-00:00", "Sh*tty days that I want over as soon as possible.\n\nThe whole --Redacted-- thing was a nice little kick in the nuts way to end the day.\n\nAnyway.")
  strzok_to_page(child_file, "2016-10-05T12:01:25-00:00", "WH sent language, let me know if you can talk.")
  page_to_strzok(child_file, "2016-10-05T13:22:04-00:00", "Toscas called Bill on same. Said DIRNSA was --Redacted--")
  page_to_strzok(child_file, "2016-10-05T13:38:24-00:00", "Kortan with me now, don't think they have the name. Just asked Andy if thst changes their calculus.")
  strzok_to_page(child_file, "2016-10-05T13:55:29-00:00", "Steinbach said same thing. You around?")
  page_to_strzok(child_file, "2016-10-05T13:56:03-00:00", "Have his last name only. Now looking for everyone in Maryland with that last name. Ha.")
  page_to_strzok(child_file, "2016-10-05T13:56:28-00:00", "I need to talk to Jim re intc, then will be.")
  page_to_strzok(child_file, "2016-10-05T16:34:24-00:00", "Hey --Redacted-- just called.")
  strzok_to_page(child_file, "2016-10-05T22:22:24-00:00", "Going in to see Bill. Will try not to smile too big")
  m = strzok_to_page(child_file, "2016-10-05T22:48:10-00:00", "OH SWEET JESUS\n\nTHERE ARE 128 EMAILS ON SCION SINCE LAST NIGHT")
  m.addnote("SCION - Sensitive Compartmented Information Operational Network")
  page_to_strzok(child_file, "2016-10-05T22:48:56-00:00", "I know! That's what I was telling you!")
  strzok_to_page(child_file, "2016-10-05T22:52:16-00:00", "And a bunch of crapola about European data privacy officials expressing grave concern about this, Commerce getting calls from the European Commission and OH MY GOD I HATE F*CKING INTERNATIONAL ORGANIZATIONS ONLY MARGINALLY MORE EFFECTIVE THAN FIFA!")
  strzok_to_page(child_file, "2016-10-05T22:52:53-00:00", "I hate them\n\nI have no idea why I studied them so with my undergraduate and graduate formal education\n\nThey are abhorrent.")
  strzok_to_page(child_file, "2016-10-05T22:55:08-00:00", "And oh my God the Privacy Shield may fall apart, leading to civil disorder and and (breathless) and")
  page_to_strzok(child_file, "2016-10-05T23:03:22-00:00", "Yup, I hate them too. --Redacted--")
  m = strzok_to_page(child_file, "2016-10-05T23:21:52-00:00", "Sigh. I'm sorry. I'm clearing sentinel. --Redacted--")
  m.addnote("sentinel - Case management system")
  strzok_to_page(child_file, "2016-10-05T23:38:30-00:00", "Just saw Eric going into HQ, talking with our favorite officer...had a post-HH look")
  page_to_strzok(child_file, "2016-10-05T23:45:16-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-05T23:47:05-00:00", "All good...yeah, that's me just finally leaving work. I see you...")

  # Page 395
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-05T23:50:20-00:00", "You see me? What are you talking about?")
  strzok_to_page(child_file, "2016-10-05T23:51:27-00:00", "My look to him")
  page_to_strzok(child_file, "2016-10-05T23:54:36-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-05T23:58:13-00:00", "Sorry you're there so late.")
  strzok_to_page(child_file, "2016-10-05T23:59:49-00:00", "Did he travel with him?!?!\n\nYeah all good, had to solve the world's ECJ problems. --Redacted--")
  page_to_strzok(child_file, "2016-10-06T00:01:47-00:00", "And yes, he did. He always does.")
  strzok_to_page(child_file, "2016-10-06T00:02:57-00:00", "I didn't know that. Thats irritating")
  page_to_strzok(child_file, "2016-10-06T01:58:51-00:00", "Kinda crazy about the Atlantic and USA Today.\n\nThe Editorialists Have Spoken; Will Voters Listen? http://nyti.ms/2dFmvcm")
  strzok_to_page(child_file, "2016-10-06T02:05:09-00:00", "No they won't listen, because they're f*cking stupid")
  strzok_to_page(child_file, "2016-10-06T02:05:17-00:00", "And I'm moving to NZ")
  page_to_strzok(child_file, "2016-10-06T14:04:27-00:00", "In with andy. One sec")
  strzok_to_page(child_file, "2016-10-06T14:04:37-00:00", "Sorry been in meetings with Bill since 9, another one with him starting now. Just left you VM. Done around 1040.")
  strzok_to_page(child_file, "2016-10-06T14:43:41-00:00", "Boo.;)\n\nWhen do you open up? And did you get what you needed that you wanted me to call about?")
  page_to_strzok(child_file, "2016-10-06T14:57:19-00:00", "Yes, call i sobe. Should be free at 11:15.")
  page_to_strzok(child_file, "2016-10-06T22:43:51-00:00", "Might just be like what DD asked ours today. What's the plan to figure out what else is out there.")
  page_to_strzok(child_file, "2016-10-06T23:11:14-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-06T23:18:44-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-06T23:20:17-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-06T23:21:08-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-06T23:21:37-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-06T23:21:48-00:00", "--Redacted--")

  # Page 396
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-06T23:22:04-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-06T23:22:31-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-06T23:24:01-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-06T23:24:34-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-06T23:24:58-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-06T23:25:08-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-06T23:26:41-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-06T23:27:31-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-07T09:53:05-00:00", "Jesus. More --Redacted-- leaks in the NYT")
  # strzok_to_page(child_file, "2016-10-07T10:02:33-00:00", "Yeah and I made the mistake of reading some stupid NY Post article about how agents are ready to revolt against D because of MY...now I'm really angry...")
  # strzok_to_page(child_file, "2016-10-07T10:03:33-00:00", "There are a bunch of really ignorant people out there blinded by their politics")
  # page_to_strzok(child_file, "2016-10-07T10:03:56-00:00", "You can't read that sh*t. And honestly, let them. The bu would be better off without them.")
  # page_to_strzok(child_file, "2016-10-07T10:04:02-00:00", "There are.")
  # strzok_to_page(child_file, "2016-10-07T10:04:37-00:00", "Sadly reminds me how deeply politics, like religion, can sometimes blind objectivity.")
  # strzok_to_page(child_file, "2016-10-07T10:04:38-00:00", "I can't help it. It's click bait. I emailed it to you.")
  page_to_strzok(child_file, "2016-10-07T10:05:04-00:00", "I don't want it!")
  strzok_to_page(child_file, "2016-10-07T10:05:41-00:00", "Too late. Just ignore it. Also sent a really thoughtful David Brooks column. I really like him. \U0001f60a")
  strzok_to_page(child_file, "2016-10-07T10:26:15-00:00", "Poor --Redacted-- gotta be up, too...")
  page_to_strzok(child_file, "2016-10-07T10:28:17-00:00", "You meeting at hq? You should have just offered to get her at home, avoid the metro ride?")
  strzok_to_page(child_file, "2016-10-07T10:28:54-00:00", "True. Suppose I could still do that")
  strzok_to_page(child_file, "2016-10-07T10:34:04-00:00", "Just shot her an email")
  page_to_strzok(child_file, "2016-10-07T10:42:50-00:00", "Referenced in Brooks' article. I was one of his blog devotees for YEARS.\n\nAndrew Sullivan: My Distraction Sickness \u2014 and Yours\nhttp://nymag.com/selectall/2016/09/andrew-sullican-technology-almost-killed-me.html")

  # Page 397
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-07T10:44:17-00:00", "Haven't read him...")
  page_to_strzok(child_file, "2016-10-07T10:45:49-00:00", "One of the finest thinkers of our day. An HIV+gay conservative, but thoughtful and open to change. A lot like David Brooks.")
  strzok_to_page(child_file, "2016-10-07T10:59:54-00:00", "What time is prep - 1130?")
  strzok_to_page(child_file, "2016-10-07T11:12:18-00:00", "God npr is depressing right noe")
  page_to_strzok(child_file, "2016-10-07T11:17:34-00:00", "Yes.\n\nWhy?")
  strzok_to_page(child_file, "2016-10-07T11:21:31-00:00", "No invite, trying to make sure my calendar is right")
  page_to_strzok(child_file, "2016-10-07T11:23:49-00:00", "Sorry, looks like she screwed it up.")
  strzok_to_page(child_file, "2016-10-07T11:26:24-00:00", "Np. Not casting aspersions, just getting mine right. Did she send it out to others at least (so they know)?")
  page_to_strzok(child_file, "2016-10-07T11:26:52-00:00", "Yes. Appears to be correct otherwise.")
  strzok_to_page(child_file, "2016-10-07T11:32:07-00:00", "K. DD's Conf room?")
  strzok_to_page(child_file, "2016-10-07T12:17:35-00:00", "Yeah thanks. Got background ok doj's concerns about this. P*ssies...\U0001f621\U0001f621\U0001f621")
  page_to_strzok(child_file, "2016-10-07T15:09:30-00:00", "I want to set up a mtg with you and Bill re intc.")
  strzok_to_page(child_file, "2016-10-07T15:10:09-00:00", "Ok. He's back Thurs afternoon")
  m = strzok_to_page(child_file, "2016-10-07T15:10:50-00:00", "What's up with intc?")
  m.addnote( "intc - Insider Threat Center?")
  page_to_strzok(child_file, "2016-10-07T15:11:51-00:00", "Had mtg with Bowdich et al this am")
  m = strzok_to_page(child_file, "2016-10-07T21:45:45-00:00", "Rethought my response to the CYD advisory. Think it's probably good for morale.")
  m.addnote("CYD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-10-08T12:35:47-00:00", "Currently reading about Trump. Wondering if he stepped down if Pence could actually get elected.")
  page_to_strzok(child_file, "2016-10-08T12:36:20-00:00", "That's probably more likely than Trump getting elected.")
  # Page 85 of this document has the unredacted version of this message
  # strzok_to_page(child_file, "2016-10-08T12:37:10-00:00", "I agree. I think it would actually energize the Republican vote. --Redacted--")
  strzok_to_page(child_file, "2016-10-08T12:39:06-00:00", "You watching the debate on Sunday?")
  page_to_strzok(child_file, "2016-10-08T12:39:47-00:00", "We'll see how things are going.")
  strzok_to_page(child_file, "2016-10-09T01:15:18-00:00", "Plus, sent you some emails with articles. Watching the Republicans melt down")

  # Page 398
  # OUTBOX == Page
  # INBOX == Strzok
  m = strzok_to_page(child_file, "2016-10-09T13:24:27-00:00", "And I'm HUGE pissed because we found info (via searching Sentinel on an account that came out) that is wildly, hugely relevant to what we're doing. Just sitting there in a field office CYD file. Nobody caring, not interested. \U0001f620\U0001f620\U0001f620\U0001f620\n\nThey're BROKEN, Lisa! Is it going to take some f*cking 9/11 - type event for everybody to stop saying, just coordinate better, have lots of meetings, figure it out?\n\nThe Bu will still recruit people if we can offer them work againse cyber criminals, or state actors, or terrorists.")
  m.addnote("CYD - FBI Cyber Division")
  m = strzok_to_page(child_file, "2016-10-09T13:29:37-00:00", "And dammit, our guys shared it with the TF on Fri (the right thing to do). Challenge is I bet both agency and Fort share it with their seniors Tues AM, if not before.")
  m.addnote("TF - probably Task Force")
  # page_to_strzok(child_file, "2016-10-09T13:36:06-00:00", "Well Andy AND D are out all week anyway.")
  # page_to_strzok(child_file, "2016-10-09T13:37:30-00:00", "God, now I want to know what it is.")
  m = strzok_to_page(child_file, "2016-10-09T13:38:11-00:00", "I'll send it on eras. I'm just worried dcia gets it and goes direct with D and/or WH.")
  m.addnote("eras - Enterprise Remote Access System")
  m = page_to_strzok(child_file, "2016-10-09T13:39:59-00:00", "Wow. Yeah but there's no way I'm getting the time to get on eras today.")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-10-09T13:40:47-00:00", "Ok. I'll call you later and we can talk around it")
  m = page_to_strzok(child_file, "2016-10-09T13:41:13-00:00", "Do you want to send to DD and I can let him know to check eras?")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-10-09T13:41:57-00:00", "Not before I talk with Bill and/or Mike.")
  page_to_strzok(child_file, "2016-10-09T13:42:22-00:00", "Although he's in Hawaii with the DNI so I'm not sure he has it.")
  strzok_to_page(child_file, "2016-10-09T13:45:24-00:00", "Jackson Hole (or wherever) then Hawaii. Tough life if you're the dni....")
  page_to_strzok(child_file, "2016-10-09T13:48:32-00:00", "Yeah but this is actually a follow on to a trip to Germany and is an utter waste of time. Dd absolutely doesn't want to be there.")
  strzok_to_page(child_file, "2016-10-09T13:49:56-00:00", "I can imagine. It's a long way to go to then have to come back to SD. Is Eric with him?")
  page_to_strzok(child_file, "2016-10-09T13:56:20-00:00", "Don't think so, but don't know.")
  page_to_strzok(child_file, "2016-10-09T19:57:12-00:00", "Hey, andy just texted the following:\n\nThere is a HO agent --Redacted-- who is coming to the airport to show us something else. You might be able to have him bring it. But we are about to leave SF and will be in HO in 5.5 hours.")
  m = page_to_strzok(child_file, "2016-10-09T19:58:33-00:00", "His email is completely failing right now, so he didn't get you email. If you want to email it to the above agent when you get home, there should be plenty of time.\n\nOr you can check erase --Redacted--")
  m.addnote("eras - Enterprise Remote Access System")

  # Page 399
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-09T20:19:05-00:00", "--Redacted--")
  #strzok_to_page(child_file, "2016-10-09T21:07:51-00:00", "And funny quote from --Redacted-- \"No way Trump will drop put. Hey Republicans: how does it feel to carry something to term?\"")
  page_to_strzok(child_file, "2016-10-10T00:12:38-00:00", "--Redacted-- I'm not sure I have it in me to watch the debate. --Redacted--")
  m = page_to_strzok(child_file, "2016-10-10T00:31:07-00:00", "Did you get my text re sending an eras to that dude?")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2016-10-10T00:33:34-00:00", "I did, but wasn't clear if --Redacted-- would get it. Do you think it's worth sending? Bill did say he talked to Steinback and talked around the subject with him.")
  page_to_strzok(child_file, "2016-10-10T00:34:46-00:00", "I told Andy you would. Up to you. Don't really know what it says so it's hard for me to evaluate.")
  strzok_to_page(child_file, "2016-10-10T00:35:11-00:00", "Then ok, I will.")
  page_to_strzok(child_file, "2016-10-10T00:35:44-00:00", "Make sure you email him on the low side too. Is there still time?")
  strzok_to_page(child_file, "2016-10-10T00:37:19-00:00", "I just did to ask.")
  page_to_strzok(child_file, "2016-10-10T00:38:05-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-10T00:46:09-00:00", "Decide if you're watching the debate?")
  page_to_strzok(child_file, "2016-10-10T00:47:49-00:00", "I think no. --Redacted-- will let you know")
  strzok_to_page(child_file, "2016-10-10T01:22:32-00:00", "--Redacted-- Debate is nasty....\n\nAlso, heard from --Redacted-- he's already at airport. He's willing to make a second trip but I'm not sure if it's worth if right now, especially if Bill got gist to Mike.")
  m = strzok_to_page(child_file, "2016-10-10T01:23:55-00:00", "Trump saying agents at FBI are furious at the MYE outcome and he's getting a special prosecutor.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  page_to_strzok(child_file, "2016-10-10T01:24:06-00:00", "I'm not watching.")
  strzok_to_page(child_file, "2016-10-10T01:27:32-00:00", "I am. Just getting aggravated. --Redacted--")
  strzok_to_page(child_file, "2016-10-11T02:01:21-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-11T02:01:27-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-11T02:02:03-00:00", "I'll ask Dina if she can go...")
  page_to_strzok(child_file, "2016-10-11T02:02:21-00:00", "It doesn't even count. It's just --Redacted-- Email him now and let him know something came up at home and tell him you can back brief.")
  page_to_strzok(child_file, "2016-10-11T02:02:25-00:00", "Good, yes.")

  # Page 400
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-11T02:05:45-00:00", "And look at how much you have to talk to --Redacted-- about!\U0001f61a")
  strzok_to_page(child_file, "2016-10-11T10:00:11-00:00", "Sigh\U0001f636\n\nI went to sleep imagining it.\n\nRe your timing this morning, it'll be late, but I can swing by after --Redacted--")
  page_to_strzok(child_file, "2016-10-11T10:24:43-00:00", "Give a call post- --Redacted--")
  strzok_to_page(child_file, "2016-10-11T10:24:58-00:00", "--Redacted-- then hustling out to --Redacted--")
  strzok_to_page(child_file, "2016-10-11T10:25:39-00:00", "I will. Of course, I want to stop by, regardless. \U0001f636")
  page_to_strzok(child_file, "2016-10-11T10:26:12-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-11T21:54:43-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-11T21:55:45-00:00", "Uh yeah, that's not going to happen.")
  strzok_to_page(child_file, "2016-10-11T21:56:08-00:00", "Uh, it just did")
  page_to_strzok(child_file, "2016-10-11T21:59:43-00:00", "But yeah, I can totally see that.")
  page_to_strzok(child_file, "2016-10-11T21:59:59-00:00", "I get that, but it's going to unhappen, and right quick.")
  strzok_to_page(child_file, "2016-10-11T22:04:19-00:00", "Yeah, checking Sentinel now. Looks like cd7A now has access...not sure if that was a recent add. Jon and I can no longer see it, though it's more relevant for the IAs to be able to. Of course, Jon and I are still here, and none of them are.\n\nStill, irritating....we'll get it fixed")
  strzok_to_page(child_file, "2016-10-11T22:21:22-00:00", "Currently fighting with --Redacted--")
  strzok_to_page(child_file, "2016-10-11T22:38:19-00:00", "Can I call you when we're done?")
  page_to_strzok(child_file, "2016-10-11T22:48:26-00:00", "Yes, though will be hard.")
  m = strzok_to_page(child_file, "2016-10-12T00:05:06-00:00", "And yes, please bring it in. Just leaving now. Had to double back to talk to Toscas. Have his nsts line now, at least.")
  m.addnote("nsts - NSA/CSS Secure Telephone System")
  page_to_strzok(child_file, "2016-10-12T00:08:37-00:00", "That's good, because that's literally all he uses.")
  page_to_strzok(child_file, "2016-10-12T02:54:03-00:00", "Ho-ly sh*t. Did you read this?\n\nFor Many Women, Trump\u2019s \u2018Locker Room Talk\u2019 Brings Memories of Abuse http://nyti.ms/2dSWWF6")
  strzok_to_page(child_file, "2016-10-12T02:54:22-00:00", "Sigh. Stupid dnd, I didn't see these.")
  # page_to_strzok(child_file, "2016-10-12T03:04:57-00:00", "Hot damn. Big news day.\n\nBuffett Calls Trump\u2019s Bluff and Releases His Tax Data http://nyti.ms/2dSIOM5")

  # Page 401
  # OUTBOX == Page
  # INBOX == Strzok
  #page_to_strzok(child_file, "2016-10-12T03:16:30-00:00", "Wow, more forceful than I have seen him. --Redacted--\n\nDonald Trump\u2019s Sad, Lonely Life http://nyti.ms/2dTCZxP")
  strzok_to_page(child_file, "2016-10-12T09:59:46-00:00", "Ok, the locker room talk twitter campaign was amazing and sad. And I do like David Brooks. --Redacted-- Reading Warren buffet now")
  page_to_strzok(child_file, "2016-10-12T10:00:06-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-12T10:01:08-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-12T10:08:33-00:00", "And \U0001f621\nhttp://mobile.nytimes.com/2016/10/12/us/politics/donald-trump-voters.html")
  strzok_to_page(child_file, "2016-10-12T14:47:50-00:00", "--Redacted-- Hi. Done. You at your desk?")
  strzok_to_page(child_file, "2016-10-12T21:37:22-00:00", "Nice. Talked to Laycock and Josh still in wrap....")
  strzok_to_page(child_file, "2016-10-13T02:49:40-00:00", "To check email. We got the reporting on Sept 19. Looks like --Redacted-- got it early August.\n\nLooking at --Redacted-- lync replies to me it's not clear if he knows if/when he told them. But --Redacted-- and --Redacted-- talked with --Redacted-- they're both good and will remember.\n\nIt's not about rubbing their nose in it. I don't care if they don't know. I just want to know who's playing games/scared covering.\n\nI totally get it will never be provable.")
  strzok_to_page(child_file, "2016-10-13T02:54:25-00:00", "Aaaaand I left my badge in the card reader. Can't get back in, so get in extra early for temp badge tomorrow \U0001f621")
  strzok_to_page(child_file, "2016-10-13T15:44:08-00:00", "30 sec\n\nRan into --Redacted--")
  page_to_strzok(child_file, "2016-10-13T23:18:41-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-13T23:20:00-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-13T23:45:35-00:00", "Sorry, was on with andy. Told him about senator and BA. Did ask about Monday, so I'll bring them in.")
  strzok_to_page(child_file, "2016-10-13T23:47:09-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-13T23:47:30-00:00", "Asked him to tell them what I do. \U0001f612")
  strzok_to_page(child_file, "2016-10-13T23:47:35-00:00", "Had Rybicki mentioned? Was sent about an hour ago")
  page_to_strzok(child_file, "2016-10-13T23:48:27-00:00", "Mentioned what? About --Redacted-- No. Andy hadn't heard.")
  strzok_to_page(child_file, "2016-10-13T23:48:38-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-13T23:48:51-00:00", "--Redacted--")

  # Page 402
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-13T23:50:20-00:00", "What did you take care of? --Redacted-- Do we know it's a forgery? Could just be the guy feeling sheepish that he got caught sharing stuff he couldn't, right?")
  strzok_to_page(child_file, "2016-10-13T23:51:16-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-13T23:52:12-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-13T23:52:32-00:00", "? Not following you last. Def a --Redacted--")
  strzok_to_page(child_file, "2016-10-13T23:53:39-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-13T23:54:09-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-13T23:59:52-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T00:00:36-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T00:05:32-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T00:08:37-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T00:10:26-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T00:12:58-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T00:13:28-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T00:13:41-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T00:37:47-00:00", "Not sure why I thought this was so neat. Suppose it's just the law nerd in me.\n\nThe Times\u2019s Lawyer Responds to Donald Trump http://nyti.ms/2e0WNza")
  # page_to_strzok(child_file, "2016-10-14T00:40:28-00:00", "God, she's an incredibly impressive woman. The Obamas in general, really. While he has certainly made mistakes, I'm proud to have had him as my president.\n\nVoice Shaking, Michelle Obama Calls Trump Comments on Women \u2018Intolerable\u2019 http://nyti.ms/2e0MtgY")
  strzok_to_page(child_file, "2016-10-14T00:42:48-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T00:43:24-00:00", "--Redacted--")
  # page_to_strzok(child_file, "2016-10-14T00:48:08-00:00", "Ugh. More of the same.\n\nDonald Trump, Slipping in Polls, Warns of \u2018Stolen Election\u2019 http://nyti.ms/2e07imx")

  # Page 403
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-14T00:49:51-00:00", "That's not very helpful.")
  strzok_to_page(child_file, "2016-10-14T00:50:39-00:00", "He's not going to do much to tamp down the conspiracy theories...")
  m = page_to_strzok(child_file, "2016-10-14T00:51:26-00:00", "Nope. Full of dog whistles too: \"We do not want this election stolen from us. Everybody knows what I'm talking about.\" The racism is barely even veiled anymore.")
  m.tag("Hatred", "racism is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  m.addnote("Lisa Page thinks Trump is a racist")
  strzok_to_page(child_file, "2016-10-14T00:52:36-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T00:52:43-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T00:53:52-00:00", "The Roger Stone comments are scary as sh*t.")
  strzok_to_page(child_file, "2016-10-14T01:00:20-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T01:00:59-00:00", "Roger Stone is horrible.")
  strzok_to_page(child_file, "2016-10-14T01:36:28-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T01:37:21-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T01:38:58-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T01:45:11-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T01:45:57-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T01:49:35-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T01:50:48-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T01:51:01-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-14T12:04:49-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T12:06:00-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T12:06:56-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-14T12:15:49-00:00", "Reading the most depressing lead story about Trump in the NYT. And couldn't be prouder, or sadder, of first lady's comments.")
  strzok_to_page(child_file, "2016-10-14T14:25:25-00:00", "You in your ofc?")
  strzok_to_page(child_file, "2016-10-14T14:26:41-00:00", "\U0001f636 K. I'll bring PAR motivation...")

  # Page 404
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-15T00:54:42-00:00", "Hi. Talked with JG for a while. A lot to tell you. --Redacted--")
  strzok_to_page(child_file, "2016-10-15T01:26:22-00:00", "Stone \u2018happy to cooperate\u2019 with FBI on WikiLeaks, Russian hacking probes - POLITICO\nhttp://www.politico.com/story/2016/10/roger-stone-fbi-wikileaks-russia-229821")
  strzok_to_page(child_file, "2016-10-15T11:18:48-00:00", "Sorry, was emailing Jon and Bill and Jason about the PC prep. --Redacted-- came back and asked if WF should reach out to Carper's DC staff.\n\nIn the interest of time, I think Jason and I should just conference call his staff director this weekend, and wf can follow up as needed. At least that way we have initial info and the D can say we've made contact.")
  page_to_strzok(child_file, "2016-10-15T11:19:49-00:00", "Makes sense to me.")
  strzok_to_page(child_file, "2016-10-15T11:55:13-00:00", "Sorry was just talking to Jason.\n\nNo plans other than this Congress call and writing the stupid prep stuff")
  m = strzok_to_page(child_file, "2016-10-15T12:19:58-00:00", "This is appalling\nhttp://m.huffpost.com/us/entry/us_580120b7e4b0e8c198a7f139")
  m.addnote("Armed Trump Supporters Protest In Front Of Democrat's Campaign Office")
  m = strzok_to_page(child_file, "2016-10-15T12:19:58-00:00", "http://m.huffpost.com/us/entry/us_5800381fe4b0e8c198a74744")
  m.addnote("Frenzied Donald Trump Supporters Are Turning On The Media -- And It's Getting Scary")
  m = strzok_to_page(child_file, "2016-10-15T13:45:20-00:00", "--Redacted--\n\nSpeaking with Carper's COS shortly....")
  m.addnote("Sen. Tom Carper's Chief of Staff")
  strzok_to_page(child_file, "2016-10-15T14:14:44-00:00", "Call went well. She confirmed Sen spoke with Monaco on Thurs night. They're issuing a press release about it on Mon.")
  page_to_strzok(child_file, "2016-10-15T14:45:11-00:00", "That's going to get political in a hurry.")
  strzok_to_page(child_file, "2016-10-15T14:48:25-00:00", "And I was careful about my statements to her but nontheless will document them in an email on the Secret side....")
  page_to_strzok(child_file, "2016-10-15T14:51:22-00:00", "That's smart.")
  page_to_strzok(child_file, "2016-10-15T14:51:31-00:00", "No, re Andy and lunch.")
  strzok_to_page(child_file, "2016-10-15T15:15:06-00:00", "Lunch get political? Not following.")
  strzok_to_page(child_file, "2016-10-15T15:15:13-00:00", "Even if just the four of you go?")
  page_to_strzok(child_file, "2016-10-15T15:15:59-00:00", "No, carpers statement.")
  page_to_strzok(child_file, "2016-10-15T15:16:57-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-15T15:18:53-00:00", "--Redacted--")

  # Page 405
  # OUTBOX == Page
  # INBOX == Strzok
  # strzok_to_page(child_file, "2016-10-15T21:25:48-00:00", "That didn't take long\U0001f621")
  # page_to_strzok(child_file, "2016-10-15T21:28:10-00:00", "At least we made the f-ers work on the weekend...")
  # strzok_to_page(child_file, "2016-10-15T21:30:09-00:00", "Uh, and, yeah - like they're doing to us.\n\nI HATE this case.\n\nAnd a LOT to tell you about my convo with JG...")
  # page_to_strzok(child_file, "2016-10-15T22:04:26-00:00", "Very nice work on that initial statement. Maybe we can talk tomorrow re JG..")
  m = strzok_to_page(child_file, "2016-10-16T00:13:34-00:00", "Do we prevent Hardy from being subpoenaed?")
  m.addnote("Hardy - Possibly David Hardy, head of FOIA at FBI")
  page_to_strzok(child_file, "2016-10-16T00:14:56-00:00", "I don't know. But he'll be okay...")
  strzok_to_page(child_file, "2016-10-16T14:56:11-00:00", "Maybe. --Redacted--")
  page_to_strzok(child_file, "2016-10-16T14:45:25-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T14:56:43-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T16:23:37-00:00", "Hey just thinking - do you have a current official passport?")
  page_to_strzok(child_file, "2016-10-16T17:45:54-00:00", "I do. Need to find it, but I think it is still good. Remind me Monday.")
  page_to_strzok(child_file, "2016-10-16T18:23:30-00:00", "And if we do go to london, I'm going to have to call --Redacted--")
  strzok_to_page(child_file, "2016-10-16T18:24:20-00:00", "--Redacted-- And Rybicki just called - need to call him back.")
  page_to_strzok(child_file, "2016-10-16T18:25:35-00:00", "K. Let me know what he's talking about. ..")
  strzok_to_page(child_file, "2016-10-16T18:33:49-00:00", "Hi. Done. Talk?")
  page_to_strzok(child_file, "2016-10-16T18:55:03-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T18:55:28-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T18:56:39-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T18:57:12-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T19:09:15-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T19:10:22-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T20:58:00-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T20:58:24-00:00", "--Redacted--")

  # Page 406
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-16T20:59:35-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T21:01:57-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T21:09:31-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:09:21-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:09:55-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T22:14:09-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:20:38-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:28:34-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:29:27-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T22:43:38-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:44:33-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:44:57-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T22:45:09-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:45:28-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T22:45:51-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:47:21-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T22:50:15-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-16T22:51:59-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-16T23:25:28-00:00", "Nostalgia for the Grace of George H.W. Bush http://nyti.ms/2e6GssP")
  strzok_to_page(child_file, "2016-10-17T13:03:32-00:00", "Thbtbtbtbt. Really?\U0001f618\n\nBill just filled 10:00 AM fire drill time with DAD interviews.\U0001f612\n\n--Redacted--")
  page_to_strzok(child_file, "2016-10-17T14:11:52-00:00", "--Redacted--")

  # Page 407
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-17T14:27:08-00:00", "Rgr. Doing interviews thru the alarms. ..")
  page_to_strzok(child_file, "2016-10-17T14:27:32-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-17T15:01:01-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-17T15:02:06-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-17T15:03:08-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-17T20:43:23-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-17T20:44:44-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-17T23:07:45-00:00", "I worry they're written for non-lawuers by lawyers, and reviewed by lawyers.\n\nDon't forget how dumb we are.")
  strzok_to_page(child_file, "2016-10-17T23:07:59-00:00", "There's some exclamation points there!\n\nHaving some concerns about these TPs, especially if they're leaked....")
  strzok_to_page(child_file, "2016-10-17T23:08:31-00:00", "Sorry, order of last two texts filpped")
  page_to_strzok(child_file, "2016-10-17T23:09:23-00:00", "Well they are for public disem, so we will have to read them in that light.\n\nI'm certainly worried about your dumb brethren not understanding the nuance, but what's the leak worry?")
  page_to_strzok(child_file, "2016-10-17T23:09:55-00:00", "You know who would be good to review and put them in dumb speak? Stephen Kelly. Lots of years dealing with dummies.")
  strzok_to_page(child_file, "2016-10-17T23:12:10-00:00", "I think we need to expand the other sections. In some cases, they don't adequately convey our reasoning behind decisions.")
  page_to_strzok(child_file, "2016-10-17T23:12:29-00:00", "Then let's do it.")
  strzok_to_page(child_file, "2016-10-17T23:13:57-00:00", "Let's. Need to get home and will take a crack at it.")
  page_to_strzok(child_file, "2016-10-17T23:14:11-00:00", "I need to print this tomorrow! Important.")
  strzok_to_page(child_file, "2016-10-17T23:35:16-00:00", "It's ok, you've got that bg bonus coming....oh, wait, no. Thats for the people there for more than a year. Like --Redacted-- and --Redacted--...")
  strzok_to_page(child_file, "2016-10-17T23:36:24-00:00", "They drink in London.")
  page_to_strzok(child_file, "2016-10-17T23:37:06-00:00", "I especially like drinking in London. I will be the official food and beverage tour guide.")
  strzok_to_page(child_file, "2016-10-17T23:41:54-00:00", "Can blue collar Budweiser guys like me and Jon afford your taste?")
  page_to_strzok(child_file, "2016-10-17T23:45:11-00:00", "On per diem you can! ;)")

  # Page 408
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-17T23:47:23-00:00", "Ha. I have made poor career decisions for sure. Can i go to London and not talk about any of this stuff that I'm incredibly sick of thinking and talking about? Maybe do a dramatic poetry reading or something instead?")
  strzok_to_page(child_file, "2016-10-17T23:49:56-00:00", "...or better yet...maybe I can just carry the bags for a DAD and wait outside?")
  strzok_to_page(child_file, "2016-10-17T23:52:52-00:00", "No. You will be --Redacted-- the Mysterious Mute Election Analyst. Just grunt and shake your head up and down or left and right.\n\nGet that carnie vibe going")
  page_to_strzok(child_file, "2016-10-17T23:53:13-00:00", "I thought I was the official bag carrier!")
  strzok_to_page(child_file, "2016-10-17T23:55:22-00:00", "I'll take one handle of the bag and you take the other.")
  strzok_to_page(child_file, "2016-10-17T23:58:22-00:00", "I'm seriously thinking one of us needs to host election night party.")
  page_to_strzok(child_file, "2016-10-18T00:00:22-00:00", "I nominate --Redacted--")
  #m = strzok_to_page(child_file, "2016-10-18T00:02:35-00:00", "I'll probably have to write talking points (likely for CyD) so I won't be able to make it.")
  #m.addnote("CyD - FBI Cyber Division")
  page_to_strzok(child_file, "2016-10-18T00:05:39-00:00", "You don't have to write talking points for Cyber if they don't tell you about the tasking!")
  strzok_to_page(child_file, "2016-10-18T00:09:59-00:00", "Word.")
  m = strzok_to_page(child_file, "2016-10-18T00:28:47-00:00", "CyD prepping for election day on November 35th....")
  m.addnote("CyD - FBI Cyber Division")
  strzok_to_page(child_file, "2016-10-18T00:30:40-00:00", "Fine, fine, was an SNL joke.\n\nhttp://youtu.be/qVMW_1aZXRk")
  strzok_to_page(child_file, "2016-10-18T00:50:24-00:00", "Hi. This is literally slowing to a crawl since I have a months long thread. I should delete it but I don't wanna....")
  m = strzok_to_page(child_file, "2016-10-18T00:50:51-00:00", "Plus it'll take 5 minutes to delete. Suppose I could imsg. \U0001f60a")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-10-18T00:51:03-00:00", "I honestly don't think the size is what slows it. These phones just suck.")
  strzok_to_page(child_file, "2016-10-18T00:52:22-00:00", "To be fair, the thread goes back to Aug 23 \U0001f636\U0001f636\U0001f636\U0001f636")
  page_to_strzok(child_file, "2016-10-18T00:53:43-00:00", "I think mine might be April. I just don't want to make the effort to find out.")
  strzok_to_page(child_file, "2016-10-18T09:54:35-00:00", "Sigh. I've got to get going and get stuff to Bill before --Redacted-- \U0001f612")
  strzok_to_page(child_file, "2016-10-18T09:55:00-00:00", "You ever hear back from Jim or Trisha on TPs?")
  page_to_strzok(child_file, "2016-10-18T10:00:24-00:00", "Yes. --Redacted-- said they would read it and provide comments this am.")
  page_to_strzok(child_file, "2016-10-18T10:12:13-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-18T11:39:38-00:00", "--Redacted--")

  # Page 409
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-18T11:40:19-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-18T13:10:47-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-18T13:36:36-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-18T13:38:03-00:00", "Np. Need 10 min...")
  strzok_to_page(child_file, "2016-10-18T16:29:13-00:00", "Hey I've gotta go now because I have no break after 1. I'm bringing back, let me know if you want me to get you something")
  page_to_strzok(child_file, "2016-10-18T21:08:26-00:00", "Need to call --Redacted-- first.")
  strzok_to_page(child_file, "2016-10-18T22:32:59-00:00", "Me too. Walked into office, Jon and Bill were there....really want to talk to you now...\U0001f636")
  page_to_strzok(child_file, "2016-10-18T22:44:33-00:00", "And I found my official passport...")
  strzok_to_page(child_file, "2016-10-18T22:46:23-00:00", "Yay! Still valid?")
  page_to_strzok(child_file, "2016-10-18T22:46:50-00:00", "Yup! Exactly a year to go...")
  page_to_strzok(child_file, "2016-10-18T23:29:36-00:00", "How late you think you are going to be there? --Redacted--")
  strzok_to_page(child_file, "2016-10-18T23:30:25-00:00", "Just left")
  m = page_to_strzok(child_file, "2016-10-18T23:37:25-00:00", "No, not necessarily. Just thoughtby your mye description that you might be there a while.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-10-18T23:39:26-00:00", "No I gave up, will re engage tomorrow. Brought home TPs to review. --Redacted--")
  page_to_strzok(child_file, "2016-10-19T00:29:20-00:00", "A little heavy-handed, but still, kind of incredible.\n\nHow do we respond to threats after our endorsement?\nhttp://www.azcentral.com/story/opinion/2016/10/16/publisher-response-to-threats-after-republic-endorsement-clinton-trump/92058964/")
  strzok_to_page(child_file, "2016-10-19T00:45:08-00:00", "Can you talk? We absolutely must expedite. It was submitted as an expedite. I had to email as much. What the fuck is going on?")
  strzok_to_page(child_file, "2016-10-19T01:22:17-00:00", "--Redacted--\n\nThe only thing I objected to was the he said - she said comment. There is no ambiguity about who's right on this current point, and I furious at doj for suggesting otherwise 0 and we need to call them on it")
  strzok_to_page(child_file, "2016-10-19T09:55:26-00:00", "You see Tim Cook made the list of potential HRC running mates?")
  page_to_strzok(child_file, "2016-10-19T09:56:05-00:00", "Gross, no.")
  strzok_to_page(child_file, "2016-10-19T09:57:48-00:00", "It was a big list, but still, he was on there. From Podesta email.")

  # Page 410
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-19T10:04:26-00:00", "\u201cI\u2019 look for ... well, it\u2019s called racial profiling. Mexicans. Syrians. People who can\u2019t speak American,\u201d he said. \u201cI\u2019m going to go right up behind them. I\u2019ll do everything legally. I want to see if they are accountable. I\u2019m not going to do anything illegal. I\u2019m going to make them a little bit nervous.\u201d\n\nTrump\u2019s supporters talk rebellion, assassination at this rallies - The Boston Globe\nhttp://bostonglobe.com/news/politics/2016/10/15/donald-trump-warnings-conspiracy-rig-election-are-stoking-anger-among-his-followers/LcCT6e0QOcfH8VdeK9UdsM/story.html?p1=Article_Trending_Most_Viewed")
  strzok_to_page(child_file, "2016-10-19T11:54:12-00:00", "It's --Redacted-- Briefed up Bill with that and dates. He will provide to Andy.")
  # strzok_to_page(child_file, "2016-10-19T13:04:19-00:00", "Came up with election night plan - we should all hit HH somewhere. Figure this damn thing better be called early. \U0001f612\n\nYou watching the debate tonight? --Redacted--")
  page_to_strzok(child_file, "2016-10-19T13:04:50-00:00", "That's a good plan.")
  page_to_strzok(child_file, "2016-10-19T13:04:59-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-19T20:18:08-00:00", "DAG approved. I told --Redacted-- already to stand by for one edit. Am going to go tell andy now.")
  page_to_strzok(child_file, "2016-10-19T20:23:06-00:00", "Might be a minute past 4:30 because I am waiting for Andy to leave d office to tell him.")
  page_to_strzok(child_file, "2016-10-19T20:31:29-00:00", "Yeah. But still waiting for Andy.")
  m = strzok_to_page(child_file, "2016-10-20T00:34:16-00:00", "--Redacted-- You got a bonus from MYE.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-10-20T00:37:04-00:00", "Just write, look, I'm supposed to get some small amount, --Redacted-- or something I, for MYE. Plus some time off. Then do 4-5 days.\n\nPlease. I insist. I'll make up the $ in per diem in London...")
  strzok_to_page(child_file, "2016-10-20T00:54:15-00:00", "You gotta watch the debates....")
  page_to_strzok(child_file, "2016-10-20T00:57:07-00:00", "I'm not watching. I honestly don't want to. It is not worth the stress to me.")
  strzok_to_page(child_file, "2016-10-20T01:15:12-00:00", "--Redacted-- I cannot believe what I am hearing.")
  #m = strzok_to_page(child_file, "2016-10-20T01:15:44-00:00", "I am riled up. Trump is a fucking idiot, is unable to provide a coherent answer.")
  #m.tag("Hatred", "fucking idiot is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  page_to_strzok(child_file, "2016-10-20T01:16:28-00:00", "Please. I honestly don't want to know.")
  #page_to_strzok(child_file, "2016-10-20T01:20:41-00:00", "--Redacted-- It's not worth your stress either. --Redacted--")

  # Page 411
  # OUTBOX == Page
  # INBOX == Strzok
  #strzok_to_page(child_file, "2016-10-20T01:22:36-00:00", "I CAN'T PULL AWAY. WHAT THE FUCK HAPPENED TO OUR COUNTRY, LIS?!??!?!")
  strzok_to_page(child_file, "2016-10-20T01:23:08-00:00", "--Redacted--")
  #page_to_strzok(child_file, "2016-10-20T01:24:19-00:00", "I don't know. But we'll get it back. We're America. We rock.")
  #strzok_to_page(child_file, "2016-10-20T01:28:22-00:00", "Donald just said \"bad hombres\"\n\n\U0001f612")
  #strzok_to_page(child_file, "2016-10-20T01:30:00-00:00", "Chris Wallace is a turd")
  #strzok_to_page(child_file, "2016-10-20T01:30:02-00:00", "Hillary: Russia and WikiLeaks and highest levels of Russian Government and Putin!!\n\nDrink!!!!")
  page_to_strzok(child_file, "2016-10-20T01:31:15-00:00", "--Redacted-- No.")
  #strzok_to_page(child_file, "2016-10-20T01:32:40-00:00", "Oh hot damn. HRC is throwing down saying Trump in bed with russia")
  strzok_to_page(child_file, "2016-10-20T01:49:01-00:00", "Sigh. I'm sorry. Just don't turn on this goddamn debate.")
  page_to_strzok(child_file, "2016-10-20T01:49:29-00:00", "There's no chance.")
  page_to_strzok(child_file, "2016-10-20T01:50:30-00:00", "--Redacted-- what is watching going to accomplish? --Redacted-- You can read about it in the morning. Even watch clips if you must. --Redacted--")
  # Page 94 has the unredacted version
  #strzok_to_page(child_file, "2016-10-20T01:50:50-00:00", "She could do SO MUCH BETTER\n\nBut she's just not getting traction. --Redacted-- \U0001f621\U0001f621\U0001f621\U0001f621")
  strzok_to_page(child_file, "2016-10-20T01:51:20-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-20T01:52:13-00:00", "--Redacted-- You DO have control over this anger and frustration.")
  strzok_to_page(child_file, "2016-10-20T02:02:43-00:00", "Maybe. I have to watch this.\n\nAnd I'm so damn mad, Lisa.\n\nAnd disgusted. And disappointed.")
  strzok_to_page(child_file, "2016-10-20T02:12:37-00:00", "Trump just said what the fbi did is disgraceful")
  #strzok_to_page(child_file, "2016-10-20T09:56:27-00:00", "Hi. Watching the post-debate commentary. Vaguely satisfying to see Megyn Kelley (who had botox and looks HORRIBLE) utterly going after Trump.")
  page_to_strzok(child_file, "2016-10-20T10:57:57-00:00", "--Redacted-- Our prep for Andy is at 9. --Redacted--")
  page_to_strzok(child_file, "2016-10-20T15:19:55-00:00", "Have to go down and talk to andy probably around 12:30. Probably only have time for lunch around here. Maybe tomorrow...")
  strzok_to_page(child_file, "2016-10-20T17:00:41-00:00", "Noon tomorrow for call with seniors. Mikes office")

  # Page 412
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-20T20:42:35-00:00", "And hey can we talk on the 302 stuff? Bill has me doing a bunch of stuff that may be duplicative of what you may have asked --Redacted-- And /or I can get him to provide the data to Bill. Thanks")
  strzok_to_page(child_file, "2016-10-20T22:34:52-00:00", "--Redacted-- Reading the 302 attachment I mentioned earlier. Yeah its a bit nflammatory, but nothing more than what's already apparent. And drags in Rybicki, Biuliano and Giacalone (none in a bad way)")
  strzok_to_page(child_file, "2016-10-20T22:48:11-00:00", "Also makes me certain that we need to go through the whole damn file. I'm happy to help.")
  page_to_strzok(child_file, "2016-10-20T22:59:33-00:00", "Please have someone make one big binder of all the material. We'll split it up.")
  strzok_to_page(child_file, "2016-10-20T23:07:29-00:00", "Will do. Whole case, starting with 302s? --Redacted--")
  strzok_to_page(child_file, "2016-10-21T00:02:32-00:00", "Maybe.\n\nI mentioned to Bill, he wants to sit in, mentioned he wouldn't say anything....")
  page_to_strzok(child_file, "2016-10-21T00:03:17-00:00", "I'll talk to andy/kortan tomorrow.")
  strzok_to_page(child_file, "2016-10-21T00:11:07-00:00", "A) ok. Don't really want Bill there but I get it. --Redacted--")
  strzok_to_page(child_file, "2016-10-21T11:35:25-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-21T16:01:26-00:00", "Yay. \u263a Talking wiht Mike. May be hard to check this with --Redacted-- and --Redacted-- in here....")
  page_to_strzok(child_file, "2016-10-21T16:18:40-00:00", "You sound a little defensive. Bring your voice down a notch.")
  page_to_strzok(child_file, "2016-10-21T16:22:15-00:00", "But correct Mike, we didn't make the decision re prosecution.")
  strzok_to_page(child_file, "2016-10-21T16:22:43-00:00", ";) done")
  page_to_strzok(child_file, "2016-10-21T16:29:35-00:00", "We don't know but that's is not our job.")
  page_to_strzok(child_file, "2016-10-21T16:29:48-00:00", "That is not a crime that we can prosecute.")
  page_to_strzok(child_file, "2016-10-21T16:44:39-00:00", "Don't answer that. You can't defend the d")
  strzok_to_page(child_file, "2016-10-21T16:45:05-00:00", "I've got it")
  page_to_strzok(child_file, "2016-10-21T16:54:20-00:00", "Yeah but the d has done that. Chaffetz texts him directly.")
  strzok_to_page(child_file, "2016-10-21T16:57:44-00:00", ";) passed that for ya")

  # Page 413
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-21T17:03:35-00:00", "Be careful...")
  strzok_to_page(child_file, "2016-10-21T20:34:54-00:00", "Yep. I'm out, dropping stuff at ofc")
  page_to_strzok(child_file, "2016-10-21T20:37:10-00:00", "Mine? I need to unlock then.")
  strzok_to_page(child_file, "2016-10-21T20:42:07-00:00", "My office. Headed to elevator now")
  page_to_strzok(child_file, "2016-10-21T22:38:27-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-21T22:46:17-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-21T22:49:05-00:00", "Also, work-wise, --Redacted-- called b/c Toscas now aware NY has hrc-huma emails via weiner invest. Told him we knew. Wanted to know our thoughts on getting it.\n\nGeorge wanted to ensure info got to Andy. I told Bill.")
  strzok_to_page(child_file, "2016-10-21T22:49:51-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-21T22:54:57-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-21T22:55:10-00:00", "I'm sure Andy is aware, but whatever.")
  page_to_strzok(child_file, "2016-10-23T18:49:08-00:00", "One sec, andy calling.")
  page_to_strzok(child_file, "2016-10-23T18:55:00-00:00", "Christ.")
  page_to_strzok(child_file, "2016-10-23T18:55:06-00:00", "He just called.")
  m = page_to_strzok(child_file, "2016-10-23T18:55:24-00:00", "Let me know when you can imsg. Not for here.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2016-10-23T20:54:08-00:00", "Dd 100% supportive re your idea re --Redacted-- Was grateful for the suggestion. I'm sorry I couldn't give you credit.")
  page_to_strzok(child_file, "2016-10-23T20:54:55-00:00", "He's also going to tell the Eads in the am, and call bill tonight, who is supposed to call you, so you can call --Redacted-- given the PC crap from back when.")
  page_to_strzok(child_file, "2016-10-23T20:55:09-00:00", "I know, but I meant with him. It was a very smart idea.")
  page_to_strzok(child_file, "2016-10-24T00:00:15-00:00", "Article is out, but hidden behind paywall so can't read it.")
  page_to_strzok(child_file, "2016-10-24T00:04:32-00:00", "Huh?")
  strzok_to_page(child_file, "2016-10-24T00:02:22-00:00", "Wsj? Boy, that was fast.\n\nNo word from Bill. Should I \"find\" it and tell the team?")
  page_to_strzok(child_file, "2016-10-24T00:03:38-00:00", "No, I think not. Maybe he didn't get a chance, or bill decided not to say anything until tomorrow.")

  # Page 414
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-24T00:04:04-00:00", "Not behind a pay wall. I need to send")
  strzok_to_page(child_file, "2016-10-24T00:04:59-00:00", "The article is not behind a paywall\n\nWe get several hours of warning about every other email, but not this, arguably more important than most...")
  page_to_strzok(child_file, "2016-10-24T00:06:30-00:00", "Jesus Pete. Then fine. Send it to everyone you know. Or I can not tell you about it at all and you can just come across it given all the time you spend reading the Journal. \U0001f621")
  page_to_strzok(child_file, "2016-10-24T00:06:50-00:00", "What difference does it make to send it to the team Sunday noght vs monday morning?")
  #page_to_strzok(child_file, "2016-10-24T00:07:37-00:00", "Thanks dude. Appreciate it. \U0001f621")
  #strzok_to_page(child_file, "2016-10-24T00:08:15-00:00", "Or I can get it like I do every other article that hits my Google news alert. Seriously.")
  #page_to_strzok(child_file, "2016-10-24T00:09:00-00:00", "Send me the Google alert.")
  #strzok_to_page(child_file, "2016-10-24T00:10:31-00:00", "Give me a break. Go look at EVERY article I've sent the team.\n\nCount them.\n\nThen count every Godd*mn heads up I get from Kortan and --Redacted-- but NOT this one.\n\nThen tell me i should sit on THIS one and let them hear from someone else. You're not being fair about this.")
  #strzok_to_page(child_file, "2016-10-24T00:12:17-00:00", "I really cannot believe you're taking this position and it angers me. I'm going to hope your anger about Andy and --Redacted-- getting dragged into this is clouding things.")
  page_to_strzok(child_file, "2016-10-24T00:12:48-00:00", "I AM being fair about this. I asked you not to. I don't care that OPA sucks. 1) This is about trust, and 2) WHAT THE F DIFFERENCE DOES IT MAKE TO ANYONE ON THE TEAM? Is there some investigative step to take? Some mitigation measure?")
  strzok_to_page(child_file, "2016-10-24T00:13:02-00:00", "IT'S ON THE INTERNET!!!!!!")
  page_to_strzok(child_file, "2016-10-24T00:13:26-00:00", "WHICH YOU ONLY KNOW ABOUT BECAUSE I TOLD YOU IT THERE.")
  page_to_strzok(child_file, "2016-10-24T00:14:12-00:00", "Good, then we can both be angry.")
  strzok_to_page(child_file, "2016-10-24T00:14:24-00:00", "I want people who worked this reading it online before people read it first and ask them about it. I want them forewarned.\n\nFind so I see it in an hour? When I open the paper WSJ tomorrow?\n\nThat's somehoe different and OK?")
  page_to_strzok(child_file, "2016-10-24T00:15:27-00:00", "Yes. Opening the paper tomorrow is not the same as 30 seconds after if fucking posted.")
  m = strzok_to_page(child_file, "2016-10-24T00:16:05-00:00", "You told me it was there 30 minutes after it went up.\n\nWhy are you angry? Because it's critical of Andy? That's even MORE reason to get the word out.\n\nAnd how dare you accuse me of violating trust!?!? I give you candid advice for which I will tell no one and get no credit because I care about him and the FBI. How dare you!")
  m.addnote("Man complaining to his mistress (not wife) that she questions his trustworthiness.")

  # Page 415
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-10-24T00:17:24-00:00", "Forewarned to do what? Because moffa or bill or --Redacted-- are going to spread it around town? So what, you sending TPs to fucking --Redacted-- so that he is forewarned and knows that the truth is? Because without that your claim is just bullshit.")
  page_to_strzok(child_file, "2016-10-24T00:19:13-00:00", "This has nothing to do with Andy. I asked you to wait until it came to you. You would have had no idea any of this was out there but for me. And I already thanked you for your excellent advice. Just a tip, it's not the way to engender good will by doing a good deed then rubbing a fucking nose in it.")
  strzok_to_page(child_file, "2016-10-24T00:20:29-00:00", "Why do I send noteworthy articles at all, Lisa? Should I wait on all of those? Should I treat ones accusing the FBI of stuff specially? Hold these?\n\nYou never have had a SINGLE issue with my promptness before. Typically, you appreciate it. This is in no way points to you.\n\nI'm so angry you'd accuse me ov violating trust! God! That hurts and I try exceedingly hard to honor that in every aspect of my life and I certainly did here.")
  strzok_to_page(child_file, "2016-10-24T00:21:05-00:00", "Lisa I'm not rubbing your nose in it! I'm telling you your betrayal of trust line is wrong and out of bounds.")
  strzok_to_page(child_file, "2016-10-24T00:21:47-00:00", "I will ALWAYS give you my honest good advice and opinion without any regard to what credit I get. I KNOW you go out of your way to credit me whenever you can.")
  strzok_to_page(child_file, "2016-10-24T00:22:17-00:00", "Again, why are you so damn angry? It was posted at 740!")
  page_to_strzok(child_file, "2016-10-24T00:22:22-00:00", "Show me your Google alert.")
  page_to_strzok(child_file, "2016-10-24T00:22:39-00:00", "You don't know to go look for this one but for me.")
  strzok_to_page(child_file, "2016-10-24T00:26:14-00:00", "It hasn't hit Google yet! I'll send it when it happens. Maybe 5 min, maybe 2 hours.\n\nBut the article was up a good 30 minutes before you told me.\n\nAre you upset because you thinks this points to you? Because if I waited (20 minutes 2 hours whatever) time it would be OK?\n\nWhatis it that's making you so angry? Because I simply don't get it.")
  page_to_strzok(child_file, "2016-10-24T00:27:59-00:00", "Yeah, and I told you a grand total of 2 minutes after I learned it was up from andy. And you sent it 5 minutes after that. And if you actually read your texts instead of desperately trying to be first, you'll see that us said no, I don't think you should send it.")
  page_to_strzok(child_file, "2016-10-24T00:29:24-00:00", "I shouldn't have to explain all of this. You knew it was there NOT because of your Google alert, which is totally fair game, but because of ME. I don't know why any of this is so hard to understand.")
  strzok_to_page(child_file, "2016-10-24T00:29:29-00:00", "And god, I'm not trying to engender goodwill by doing a good job. I didn't rub your nose in it.")

  # Page 416
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-24T00:31:47-00:00", "I know that, and haven't said otherwise.\n\nNone of this is hard to understrand, which is why I'm asking you why you're so damn angry at this. LITTERALLY EVERY OTHER SIGNIFICANT ARTICLE we've treated this way. And the article was out for half an hour. My sending it in no way points to you.\n\nThe fact that everyone is treating this so hush hush differently is part of the problem.")
  m = strzok_to_page(child_file, "2016-10-24T00:33:27-00:00", "And I can only take your lack of response to my fury at being accused of betraying your trust as either equal fury on your part or an acknowledgement that you were wrong about that.\n\nI don't treat your trust lightly or carelessly, Lisa. Don't so lightly accuse me of doing so.")
  m.addnote("Man furious at his mistress (not wife) for her accusing him of betraying her trust")
  page_to_strzok(child_file, "2016-10-24T00:34:09-00:00", "I'm done talking about this. No one is treating it all hush hush. Could you stop already? This has nothing to do with the case or the investigative team, and is all about trying to smear a public servant. So how about you withhold judgement about what is actually going on.")
  page_to_strzok(child_file, "2016-10-24T00:34:59-00:00", "I believe you betrayed my trust. If I thought I was wrong or had made a mistake, I would just say so, thanks.")
  strzok_to_page(child_file, "2016-10-24T09:58:44-00:00", "Sent you two good articles I doubt our press roundup will pick up. --Redacted--")
  strzok_to_page(child_file, "2016-10-24T10:01:30-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-24T10:05:50-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-24T10:09:15-00:00", "--Redacted-- Was that on a bu website, or did you hear about it word of mouth?\n\n(and yes I'm truly interested in all this stuff at the same time I'm trying to find footing)")
  page_to_strzok(child_file, "2016-10-24T10:19:21-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-24T10:23:40-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-24T10:40:40-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-24T10:41:35-00:00", "And it's above the fold. Jerks.")
  strzok_to_page(child_file, "2016-10-24T10:41:55-00:00", "I wonder how Devin got a hold of the story. I have theories.")
  strzok_to_page(child_file, "2016-10-24T10:42:42-00:00", "And I don't want to waste time today on the stupid argument last night. --Redacted--")
  strzok_to_page(child_file, "2016-10-24T10:46:23-00:00", "And Devlin is saying, not implying there's a connection here, but look at the timing - service, then meeting, then case, then funding. The point we need to highlight isn't the March date of discovery of the server - because to us, who cares? - it's the date anyone realized there was classified on there.")
  
  # Page 417
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-24T11:13:01-00:00", "A) He did. And he's right.\n\nB) I agree we can't just drop it where it is - I just hate that this case is so all-consuming and I'm so tired of it and --Redacted-- C) yeah me too. Just got out. --Redacted--\n\nAny word as to timing of election brief to D?")
  page_to_strzok(child_file, "2016-10-24T11:17:26-00:00", "No, shitty ass --Redacted-- still hasn't sent the invite out. I hate her.")
  strzok_to_page(child_file, "2016-10-24T11:53:27-00:00", "And talking to Moffa now, need to talk to you before you talk to him")
  page_to_strzok(child_file, "2016-10-24T12:01:15-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-24T12:03:27-00:00", "Yes of course. Just don't talk to Moffa before")
  strzok_to_page(child_file, "2016-10-24T18:23:19-00:00", "Sorry Bill is hell on keeping on schedule")
  strzok_to_page(child_file, "2016-10-24T18:23:45-00:00", "And then Scott ambushes me \U0001f612\U0001f612\U0001f612\U0001f612")
  page_to_strzok(child_file, "2016-10-24T18:35:49-00:00", "Going to go talk to --Redacted-- Hit me here.")
  strzok_to_page(child_file, "2016-10-24T18:36:52-00:00", "Rgr. On the IA? --Redacted--? I have info on the first.")
  page_to_strzok(child_file, "2016-10-24T18:47:14-00:00", "The second. Have more Qs for you too.")
  strzok_to_page(child_file, "2016-10-24T19:16:04-00:00", "Need to talk to you alone before 345")
  page_to_strzok(child_file, "2016-10-25T00:46:57-00:00", "I hate this case. \U0001f621")
  page_to_strzok(child_file, "2016-10-25T00:54:08-00:00", "Nothing more. Just all of it.")
  page_to_strzok(child_file, "2016-10-25T00:55:02-00:00", "I asked Jim and Trisha to meet tomorrow morning. Please let me just meet with them alone. Please.")
  #strzok_to_page(child_file, "2016-10-25T00:59:55-00:00", "Sure")
  strzok_to_page(child_file, "2016-10-25T01:00:51-00:00", "I'm still angry at them over this stupid --Redacted--")
  page_to_strzok(child_file, "2016-10-25T01:01:23-00:00", "But I thought our ogc had you back?")
  strzok_to_page(child_file, "2016-10-25T01:03:09-00:00", "Whatever. Did get a warm fuzy from Trisha. A little too reticent to say DOD was WAY out of line")
  strzok_to_page(child_file, "2016-10-25T01:04:34-00:00", "Too much to explain here.\n\nJim and Trisha talking about shielding the one / any 302s?")
  page_to_strzok(child_file, "2016-10-25T01:05:38-00:00", "I haven't talked to them about it at all. Didn't want to get into it here.")
  m = page_to_strzok(child_file, "2016-10-25T01:15:30-00:00", "Hey George T called me tonight about the mye letter they are getting ready to send out. Remind me I need to ask you something. Tomorrow is fine.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  
  # Page 418
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-25T01:15:49-00:00", "Np. Just cranky at them for bad choices about --Redacted--")
  m = strzok_to_page(child_file, "2016-10-25T01:16:09-00:00", "Letter to who? And sure. You can also imsg me")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-10-25T01:17:02-00:00", "Congress. Too hard to write.")
  strzok_to_page(child_file, "2016-10-25T01:18:34-00:00", "Got it. F them.")
  page_to_strzok(child_file, "2016-10-25T01:20:09-00:00", "Got the email. That's great. Let me get as much as I can to tell dd tomorrow, at least give him some good news.")
  strzok_to_page(child_file, "2016-10-25T01:21:50-00:00", "Ok, though we have prebrief (maybe) at 10?")
  page_to_strzok(child_file, "2016-10-25T01:22:15-00:00", "Whenever works.")
  page_to_strzok(child_file, "2016-10-25T01:22:27-00:00", "And not critical. Just something to distract.")
  page_to_strzok(child_file, "2016-10-25T01:47:05-00:00", "Thanks for the note to Andy. \u2764")
  strzok_to_page(child_file, "2016-10-25T01:56:23-00:00", "Ok, no?")
  page_to_strzok(child_file, "2016-10-25T08:32:12-00:00", "Christ. Make sure you scroll down and read that guy's comment about the polls.\n\nDonald Trump Dismisses Latest Accuser: \u2018Oh, I\u2019m Sure She\u2019s Never Been Grabbed Before\u2019 http://nyti.ms/2eyZhVL")
  strzok_to_page(child_file, "2016-10-25T11:34:46-00:00", "Oh, I'm calling High Confidence.\n\nI am soooo late. Just sent Bob en email that I'd be late. \U0001f612")
  page_to_strzok(child_file, "2016-10-25T11:36:12-00:00", "Why so late?")
  strzok_to_page(child_file, "2016-10-25T11:55:09-00:00", "So Andy didn't respond...I'm sure busy/full mailbox/maybe not wanting email trail...still, have a tiny concern he took it poorly. Please let me know if you hear anything along those lines.")
  page_to_strzok(child_file, "2016-10-25T11:56:11-00:00", "Of course I will. I'm sure he did not.")
  strzok_to_page(child_file, "2016-10-25T12:57:56-00:00", "Remind me to tell you my slightly cranky at Trisha yesterday story")
  page_to_strzok(child_file, "2016-10-25T16:11:39-00:00", "--Redacted-- stood me.up!")
  page_to_strzok(child_file, "2016-10-25T18:10:58-00:00", "And I officially just asked my boss about London. He's good. \U0001f60a")
  strzok_to_page(child_file, "2016-10-25T18:11:25-00:00", "Were you with him when he called Bill? I was here....")
  page_to_strzok(child_file, "2016-10-25T21:37:53-00:00", "Hey, you should not wait. I caught randy, he 100% wants --Redacted-- and cd there. Now waiting for andy.")
  page_to_strzok(child_file, "2016-10-25T21:55:53-00:00", "I'm with andy and kortan.")
  strzok_to_page(child_file, "2016-10-25T23:29:33-00:00", "Was talking to Bill, rehashed rehashed the the whole cyber ddpi talk. Looked at their (horrible ) slides")

  # Page 419
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-25T23:29:51-00:00", "\U0001f636 well, yay!")
  strzok_to_page(child_file, "2016-10-25T23:30:39-00:00", "He didn't mention the --Redacted-- brief tomorrow - did he tell you who of us he wanted to go?")
  page_to_strzok(child_file, "2016-10-25T23:31:00-00:00", "You jon --Redacted--")
  strzok_to_page(child_file, "2016-10-25T23:32:30-00:00", "Cool.\n\nAnd I just blocked out London on my calendar.\U0001f60a\U0001f60a\U0001f60a\U0001f60a")
  page_to_strzok(child_file, "2016-10-25T23:33:03-00:00", "So should I officially have --Redacted-- move my trip?")
  strzok_to_page(child_file, "2016-10-25T23:33:47-00:00", "I need to tell Bill")
  strzok_to_page(child_file, "2016-10-25T23:34:18-00:00", "But yes, let me get confirmation from legat Brits can do it, and if so, then I would")
  strzok_to_page(child_file, "2016-10-26T11:24:10-00:00", "And you, egging Jon on...you knew I had those dates! ;)")
  page_to_strzok(child_file, "2016-10-26T11:25:34-00:00", "Wasn't thinking about it when I emailed, still had a foggy brain.")
  page_to_strzok(child_file, "2016-10-26T11:29:47-00:00", "What Drives Donald Trump? Fear of Losing Status, Tapes Show http://nyti.ms/2eHQZJs")
  page_to_strzok(child_file, "2016-10-26T11:30:03-00:00", "I see. I only caught the last 30 seconds or so.")
  page_to_strzok(child_file, "2016-10-26T11:39:00-00:00", "Let's talk about this later.\n\n\u2018We Need to Clean This Up\u2019: Clinton Aide\u2019s Newly Public Email Shows Concern http://nyti.ms/2dG6zaI")
  strzok_to_page(child_file, "2016-10-26T11:55:50-00:00", "It's true! Plus, you were playing all too col for school. \U0001f60a\n\nYeah, I saw that...happy to discuss.")
  m = strzok_to_page(child_file, "2016-10-26T11:56:34-00:00", "Stupid CIRG amateur hour")
  m.addnote("CIRG - Critical Incident Response Group")
  strzok_to_page(child_file, "2016-10-26T13:06:46-00:00", "Hit piece on Andy from VA GOP in Hampton newspaper")
  page_to_strzok(child_file, "2016-10-26T13:13:47-00:00", "That sucks. I can talk btw.")
  page_to_strzok(child_file, "2016-10-26T14:37:04-00:00", "I'm here. Talking to --Redacted--")
  strzok_to_page(child_file, "2016-10-26T14:37:29-00:00", "Your office?")
  strzok_to_page(child_file, "2016-10-26T14:37:42-00:00", "Can/should I stop by?")
  page_to_strzok(child_file, "2016-10-26T15:37:00-00:00", "Walking back now.")
  page_to_strzok(child_file, "2016-10-26T19:21:46-00:00", "Hey sorry. Was in with andy, now talking WITH --Redacted-- I missed the call, right?")
  strzok_to_page(child_file, "2016-10-26T20:31:29-00:00", "Got it. Bill moved wrap to 430 but he's late")
  
  # Page 420
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-26T20:40:10-00:00", "--Redacted--")
  m = page_to_strzok(child_file, "2016-10-26T20:50:15-00:00", "Gotta go check scion")
  m.addnote("SCION - Sensitive Compartmented Information Operational Network")
  page_to_strzok(child_file, "2016-10-26T22:03:00-00:00", "Okay, I'm going to leave now. Call you from the car to talk about Chaffetz and current issue.")
  strzok_to_page(child_file, "2016-10-26T22:37:45-00:00", "Don't forget we have --Redacted-- chat with Bill tomorrow at 10 (same time Jason proposed)")
  m = strzok_to_page(child_file, "2016-10-26T23:37:56-00:00", "Sigh\n\nLike --Redacted-- going tdy to head up --Redacted--")
  m.addnote("tdy - Temporary Duty Yonder, a business trip")
  page_to_strzok(child_file, "2016-10-26T23:38:56-00:00", "Wow, really? That's news to me.")
  m = page_to_strzok(child_file, "2016-10-26T23:43:55-00:00", "It's not that exactly. Long story, but we're in a real bind re the --Redacted-- And plus, if it's just tdy...")
  m.addnote("tdy - Temporary Duty Yonder, a business trip")
  strzok_to_page(child_file, "2016-10-26T23:45:17-00:00", "Bill went through the open to the community bit. But not --Redacted--?")
  strzok_to_page(child_file, "2016-10-26T23:46:15-00:00", "I shouldn't complain, I guess, if it ultimately open --Redacted--")
  page_to_strzok(child_file, "2016-10-26T23:46:20-00:00", "Beats me. But why are you complaining? --Redacted-- Plus just tdy, right?")
  m = page_to_strzok(child_file, "2016-10-26T23:46:37-00:00", "It's not good for you to have wfo open now.")
  m.addnote("wfc - Washington Field Office")
  strzok_to_page(child_file, "2016-10-26T23:49:06-00:00", "Just grumbling. Because --Redacted-- should be tdying in hrd or training or something.")
  strzok_to_page(child_file, "2016-10-26T23:50:43-00:00", "So. What made you cranky? Was it not seeing Andy/Eric/--Redacted-- stuff? Something at wrap?\n\nOr just because, no reason needed?")
  page_to_strzok(child_file, "2016-10-26T23:53:05-00:00", "First your overshare re Andy with George, then coming home and --Redacted--, yeah, just everything.")
  strzok_to_page(child_file, "2016-10-27T00:00:00-00:00", "And i hooe you really dont see that as an overshare. Intention was to say we're moving it quickly. Truly it's minor - don't think it's somethig George wouldn't find out, and don't think it slow rolls them. I'll keep up the pressure.\n\nThe others stink, no question about it. I'm sorry")
  # Page 102 has unredacted version of this message
  #strzok_to_page(child_file, "2016-10-27T00:06:05-00:00", "Interesting - one of the Podesta emails talks about him hosting Peter Kadzik at his house for dinner Oct, 2015. And in May, 2015, --Redacted-- asked Podesta for a job on the campaign")
  page_to_strzok(child_file, "2016-10-27T00:16:55-00:00", "Sorry, was on with andy, now have to deal with --Redacted-- Brb.")
  m = page_to_strzok(child_file, "2016-10-27T00:18:58-00:00", "Hey, guess what. We're going to have a mye exam meeting tomorrow. Like old times...")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-10-27T00:25:57-00:00", "Holy moly. Who?")

  # Page 421
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-27T00:26:40-00:00", "Was talking with Jen. Picking our SCs. I'm glad she got the job.")
  page_to_strzok(child_file, "2016-10-27T00:26:54-00:00", "Announced today?")
  page_to_strzok(child_file, "2016-10-27T00:27:22-00:00", "The whole band! We're back on tour!")
  strzok_to_page(child_file, "2016-10-27T00:29:59-00:00", "Not announced, but they all know. Calls actually happened yesterday.\n\nAnd I feel (hopefully don't look as old) like Keith Richards. Andy joining via call? There's nothing classified....")
  page_to_strzok(child_file, "2016-10-27T00:30:48-00:00", "Yes, he is.")
  page_to_strzok(child_file, "2016-10-27T00:31:03-00:00", "Good. I saw her today, but didn't say anything.")
  strzok_to_page(child_file, "2016-10-27T00:33:52-00:00", "Woohoo! It's a Banner Day. What special occasion outfit should I wear? ;)")
  page_to_strzok(child_file, "2016-10-27T00:35:15-00:00", "No idea. But I did just realize that we all should have dressed up as classified emails for halloween.")
  m = strzok_to_page(child_file, "2016-10-27T00:46:03-00:00", "Or blackberries. Or B1 redactions. Or sketchy big brown shaddy shit")
  m.addnote("B1 radactions - Maybe 3.3 (b) (1) Reveal the identity of a confidential human source, a human intelligence source, a relationship with an intelligence or security service of a foreign government or international organization, or a nonhuman intelligence source; or impair the effectiveness of an intelligence method currently in use, available for use, or under development")
  page_to_strzok(child_file, "2016-10-27T00:51:22-00:00", "That would be one needy halloween party.")
  page_to_strzok(child_file, "2016-10-27T00:51:30-00:00", "Nerdy, not needy.")
  page_to_strzok(child_file, "2016-10-27T09:33:52-00:00", "Buckle in...\n\nDonations to Foundation Vexed Hillary Clinton\u2019s Aides, Emails Show http://myti.ms/2dK7eYx")
  strzok_to_page(child_file, "2016-10-27T10:06:39-00:00", "--Redacted-- Reading the article you sent")
  strzok_to_page(child_file, "2016-10-27T10:45:07-00:00", "But, meetings!\n\nYou locked in for lunches today and tomorrow? --Redacted-- wants to meet, can either do a 30 minute coffee or lunch.")
  page_to_strzok(child_file, "2016-10-27T10:45:56-00:00", "Today is --Redacted--, tomorrow is trisha, so yes, I think so.")
  strzok_to_page(child_file, "2016-10-27T10:47:21-00:00", "Sigh. Hopefully Trisha has something come up ..tomorrow would be an EXCELLECT day to get out")
  page_to_strzok(child_file, "2016-10-27T14:26:02-00:00", "I obviously don't have to tell you how completely INFURIATED I am with Jim right now.")
  page_to_strzok(child_file, "2016-10-27T14:42:59-00:00", "Did --Redacted-- come up in any substantive way?")
  strzok_to_page(child_file, "2016-10-27T15:12:47-00:00", "No. Will stop by with --Redacted--")
  page_to_strzok(child_file, "2016-10-27T15:13:01-00:00", "Shocking.")
  strzok_to_page(child_file, "2016-10-27T15:59:34-00:00", "--Redacted-- Need to make a call to Toscas at 1:05.")
  page_to_strzok(child_file, "2016-10-27T16:21:41-00:00", "In with Kortan now.")

  # Page 422
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-27T16:25:15-00:00", "Just spoke with JB...he relayed your convo...")
  strzok_to_page(child_file, "2016-10-27T16:33:42-00:00", "D is going to call Andy, we should talk before then. Have you talked with Andy, particularly w/r/t what JB subsequently told me?")
  page_to_strzok(child_file, "2016-10-27T16:36:11-00:00", "He already did.")
  strzok_to_page(child_file, "2016-10-27T16:38:06-00:00", "JB told me there was no requirement to recuse you, that is was optics,we went round and round playing that out.")
  m = page_to_strzok(child_file, "2016-10-27T18:03:22-00:00", "Please, let's figure out what it is we HAVE first. What if we can't make out PC? Then we have no further investigative step.")
  m.addnote("PC - Personal Conflict")
  strzok_to_page(child_file, "2016-10-27T18:05:29-00:00", "Agreed")
  page_to_strzok(child_file, "2016-10-27T18:25:56-00:00", "Going to the scif, brb, in case you come by.")
  strzok_to_page(child_file, "2016-10-27T19:01:23-00:00", "I've got a 345 with Bill...")
  strzok_to_page(child_file, "2016-10-27T20:38:14-00:00", "K. There's stuff from discussion today we haven't covered but you have the big stuff. Will think and write down anything else")
  strzok_to_page(child_file, "2016-10-27T21:08:18-00:00", "God I am aggravated. Call me...now have a 530 re-group.")
  page_to_strzok(child_file, "2016-10-27T21:08:58-00:00", "On with Devlin still.")
  strzok_to_page(child_file, "2016-10-27T21:09:48-00:00", "Hope it's going well...")
  page_to_strzok(child_file, "2016-10-27T21:21:08-00:00", "I'm done.")
  strzok_to_page(child_file, "2016-10-27T21:30:44-00:00", "I'm 20 feet from you and this feels unnatural. ....")
  page_to_strzok(child_file, "2016-10-27T21:31:09-00:00", "I just walked in on Jim to force the issue. Me> \"I'm not recused, but I'm not sitting in on this meeting.\"")
  page_to_strzok(child_file, "2016-10-27T21:31:19-00:00", "He told me to just go chill out for a while, so that's what I'm doing.")
  strzok_to_page(child_file, "2016-10-27T21:33:01-00:00", "That's good advice. --Redacted--")
  page_to_strzok(child_file, "2016-10-27T22:33:39-00:00", "You should not come by. We should talk by phone.")
  strzok_to_page(child_file, "2016-10-28T00:18:45-00:00", "Do you have George's cell?")
  strzok_to_page(child_file, "2016-10-28T02:09:04-00:00", "I do now kinda love George")
  page_to_strzok(child_file, "2016-10-27T02:10:06-00:00", "Glad to hear it. We should talk before your 7:30. Also sent a couple of things on gtown.")

  # Page 423
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-28T02:46:34-00:00", "Of course. Let me know when. I'll be driving in by 7.\n\nStill conference calling, 1:15 in...")
  page_to_strzok(child_file, "2016-10-28T03:11:49-00:00", "Conference call with whom? This late?")
  strzok_to_page(child_file, "2016-10-28T03:13:23-00:00", "George David --Redacted-- Jon --Redacted--\n\nYes.\n\nMany feelings. \U0001f612")
  page_to_strzok(child_file, "2016-10-28T07:50:42-00:00", "Any plan to tell the case agents? You know, since so much of this has hinged on the credibility of \"the team.\"\U0001f621")
  strzok_to_page(child_file, "2016-10-28T14:11:26-00:00", "Never mind Conf call now")
  page_to_strzok(child_file, "2016-10-28T14:31:36-00:00", "Frankly didn't want to. I don't need to be privy when I had no role in the decision.")
  page_to_strzok(child_file, "2016-10-28T14:47:09-00:00", "I cancelled lunch with Trisha. I'm in no mood.")
  page_to_strzok(child_file, "2016-10-28T17:19:06-00:00", "Still on with devlin. Mike's phone is ON FIRE.")
  strzok_to_page(child_file, "2016-10-28T17:19:38-00:00", "It's on news")
  strzok_to_page(child_file, "2016-10-28T17:29:58-00:00", "You may wanna tell Devlin he should turn on CNN, there's news going on ;(")
  strzok_to_page(child_file, "2016-10-28T17:30:13-00:00", "Sorry ;)")
  page_to_strzok(child_file, "2016-10-28T17:30:17-00:00", "He knows. He just got handed a note.")
  strzok_to_page(child_file, "2016-10-28T17:33:54-00:00", "Ha. He asking about it now?")
  page_to_strzok(child_file, "2016-10-28T17:34:44-00:00", "Yeah. It was pretty funny. Coming now.")
  strzok_to_page(child_file, "2016-10-28T19:24:48-00:00", "News picked up Weiner source")
  #page_to_strzok(child_file, "2016-10-28T22:02:21-00:00", "Christ. It's there led on freaking MARKETPLACE.")
  m = page_to_strzok(child_file, "2016-10-28T22:27:32-00:00", "Rybicki just called to check in. He very clearly 100% believes that Andy should be recused because of the \"perception.\"")
  m.addnote("perception - Probably because of the million+ in campaign donations to his wife")
  strzok_to_page(child_file, "2016-10-28T22:30:57-00:00", "God. \U0001f621")
  page_to_strzok(child_file, "2016-10-28T22:34:58-00:00", "Our statement affected the stock market. \U0001f621")
  page_to_strzok(child_file, "2016-10-29T00:52:04-00:00", "Don't understand your email, if it's a matter similar to those we've been talking about lately, why no recusal before? Something different?")
  strzok_to_page(child_file, "2016-10-29T01:21:48-00:00", "I assume McAuliffe picked up. But that doesn't make sense.\n\nHe said he was interviewing, maybe he's headed into private sector?")
  strzok_to_page(child_file, "2016-10-29T02:05:35-00:00", "Talking to --Redacted--")
  strzok_to_page(child_file, "2016-10-29T02:06:47-00:00", "Can talk if you want. Not that that would make any sense.")

  # Page 424
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-10-29T12:31:53-00:00", "About to hop on phone with --Redacted-- and Jon")
  strzok_to_page(child_file, "2016-10-29T15:33:41-00:00", "Thbtbtbtbt. Can you work talk?")
  page_to_strzok(child_file, "2016-10-29T15:41:31-00:00", "No. Going to brunch with --Redacted--. I might miss the 1.")
  m = strzok_to_page(child_file, "2016-10-29T15:44:11-00:00", "Oof. Hope you dont...actually, check that. I.hooe you have a nice time/break. I will fill you in if you miss it. Remind me later then about my convo with NYO")
  m.addnote("NYO - New York Field Office")
  page_to_strzok(child_file, "2016-10-29T18:32:46-00:00", "Hey is there a way to find out from soic which numbers called in to the call? I'm concerned about all the beeps. I'm sure between the two of us, we could figure out what number folks were using.")
  strzok_to_page(child_file, "2016-10-29T18:41:22-00:00", "Good thought. I'll ask.")
  strzok_to_page(child_file, "2016-10-29T19:04:34-00:00", "Set up tomorrow for 12 people. Please check my math on that....")
  strzok_to_page(child_file, "2016-10-29T19:11:40-00:00", "And they cannot see the number for who dialed in")
  strzok_to_page(child_file, "2016-10-30T00:00:26-00:00", "K. About to eat, so good timing. I will set away to review affidavit afterwards.")
  page_to_strzok(child_file, "2016-10-30T00:00:44-00:00", "Have you sent it around yet?")
  strzok_to_page(child_file, "2016-10-30T00:29:27-00:00", "I did! You got it from me, right?")
  strzok_to_page(child_file, "2016-10-30T00:57:39-00:00", "Hi. Excused myself from the table to read it. Have you looked at it?")
  page_to_strzok(child_file, "2016-10-30T00:58:57-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-30T01:31:39-00:00", "In a basement study by myself working. \U0001f612\n\nSee, e.g., the email in just sent JB.")
  strzok_to_page(child_file, "2016-10-30T04:03:27-00:00", "Going back up now to join the group...--Redacted--")
  page_to_strzok(child_file, "2016-10-30T04:04:23-00:00", "I'm sorry. There's no way you could have planned any of this...")
  strzok_to_page(child_file, "2016-10-30T04:05:45-00:00", "What are you doing up? I'm red lining. Want me to.forward to you? It's sure to.put you back to sleep")
  page_to_strzok(child_file, "2016-10-30T04:14:25-00:00", "And god, poor --Redacted-- Seems like she's been working the entire day.")
  # strzok_to_page(child_file, "2016-10-30T13:50:53-00:00", "This is all Matt\n\nJustice officials warned FBI that Comey\u2019s decision to update Congress was not consistent with department policy - The Washington Post\nhttps://www.washingtonpost.com/world/national-security/justice-officials-warned-fbi-that-comeys-decision-to-update-congress-was-not-consistent-with-department-policy/2016/10/29/cb179254-9de7-11e6-b3c9-f662adaa0048_story.html?hpid=hp_hp-top-table-main_campaignprint-810nm%3AAhomepage%2Estory")

  # Page 425
  # OUTBOX == Page
  # INBOX == Strzok
  # page_to_strzok(child_file, "2016-10-30T13:56:06-00:00", "Yeah, I saw it. Makes me feel WAY less bad about throwing him under the bus in the forthcoming --Redacted-- article.")
  strzok_to_page(child_file, "2016-10-30T13:57:24-00:00", "Yep the whole tone is anti Bu. Just a tiny bit from us. And serves him right. He's gonna be pissed....")
  m = strzok_to_page(child_file, "2016-10-30T15:10:36-00:00", "--Redacted-- I'm heading in to JEH now")
  m.addnote("JEH - J Edgar Hoover building?")
  page_to_strzok(child_file, "2016-10-30T15:11:41-00:00", "You going to ny?")
  strzok_to_page(child_file, "2016-10-30T15:17:55-00:00", "No. Can review here. From my office, even. --Redacted--")
  page_to_strzok(child_file, "2016-10-30T17:27:31-00:00", "An article to share: FBI agents knew of Clinton-related emails weeks before director was briefed\nFBI agents knew of Clinton-related emails weeks before director was briefed\nhttp://wapo.st/2f2EhEO")
  page_to_strzok(child_file, "2016-10-30T18:32:07-00:00", "Okay now I'm getting angry.")
  strzok_to_page(child_file, "2016-10-30T19:06:48-00:00", "What - Dave's opening comments?")
  page_to_strzok(child_file, "2016-10-30T19:30:47-00:00", "Sorry, utterly terrible day. I'm not sure I can identify one single redeeming thing about it.") 
  # strzok_to_page(child_file, "2016-10-30T19:49:27-00:00", "Oh god --Redacted-- I'm sorry\n\nTalked to Bill he's leaning not telling Bill,he was going to call Baker. We need that Kortan info go to weigh in the decision.")
  strzok_to_page(child_file, "2016-10-30T20:39:03-00:00", "Oh God. I'm sorry. Stupid f*cking election.")
  strzok_to_page(child_file, "2016-10-30T21:13:57-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-30T21:14:45-00:00", "The bureau honestly doesn't deserve us.")

  # Page 426
  # OUTBOX == Page
  # INBOX == Strzok
  # strzok_to_page_unix_epoch(child_file, 1477862123995, "As long as you'll hire me in 3 years, I'm fine....")
  page_to_strzok(child_file, "2016-10-30T21:18:17-00:00", "--Redacted-- I'm concerned that there will surely be a holdover after the 9, if that's the case, I want to be there.")
  page_to_strzok(child_file, "2016-10-30T21:18:31-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-10-30T21:19:37-00:00", "God, I'm so incredibly furious. I would just walk out and if I had anywhere to go. Let him deal with everything.")
  strzok_to_page(child_file, "2016-10-30T21:26:07-00:00", "Yeah I think it would be helpful to have you here. --Redacted-- will be, too (I think).")
  page_to_strzok(child_file, "2016-10-30T21:26:28-00:00", "For morning meeting?")
  m = strzok_to_page(child_file, "2016-10-30T21:26:59-00:00", "You want to talk about it? I can imsg...")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2016-10-30T21:27:26-00:00", "No, standing by after that's done in case they want to talk about it then")
  strzok_to_page(child_file, "2016-10-30T21:30:33-00:00", "You can come hang out in 4012 with me --Redacted-- and --Redacted--...\n\nI have remnants of Qdoba chips and salsa....")
  strzok_to_page(child_file, "2016-10-30T22:11:22-00:00", "--Redacted-- tolds doj we have at least one classified. I left a vague vm for --Redacted--")
  strzok_to_page(child_file, "2016-10-30T22:38:59-00:00", "Connected w/ George")
  strzok_to_page(child_file, "2016-10-30T23:06:03-00:00", "Great f*cking nyt...")
  strzok_to_page(child_file, "2016-10-30T23:09:31-00:00", "You saw the authors. ...what that even means anymore, I don't know")
  page_to_strzok(child_file, "2016-10-31T00:38:32-00:00", "Oh, but DB wants to be able to show he's Doing Something. \U0001f621")
  strzok_to_page(child_file, "2016-10-31T00:53:02-00:00", "Yeah, I thought so.\n\nOk. I need to call Bryan at WFO (was talking with --Redacted-- and when he called earlier). Let me knock that out and will text here after that")
  strzok_to_page(child_file, "2016-10-31T15:04:05-00:00", "Heading into 11....Bill stressed")
  page_to_strzok(child_file, "2016-10-31T16:05:28-00:00", "Can't WITH j--Redacted--.")
  strzok_to_page(child_file, "2016-10-31T16:05:28-00:00", "Any idea how it went? Not sure source of his info, but bill thought Andy adamant he wouldn't.")
  m = strzok_to_page(child_file, "2016-10-31T16:54:13-00:00", "K. Bill said Andy mentioned pushing mye until tomorrow.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok(child_file, "2016-10-31T17:17:11-00:00", "That's the tentative plan.")
  page_to_strzok(child_file, "2016-10-31T18:33:34-00:00", "Hey there. Want to meet with bill now to 4 better? Will need to leave right after if we keep it at 4 --Redacted--")
  strzok_to_page(child_file, "2016-10-31T22:07:15-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-10-31T23:43:55-00:00", "Hoo boy. Just talked to Lou. Remind me....")

  # Page 427
  # OUTBOX == Page
  # INBOX == Strzok
  # page_to_strzok(child_file, "2016-11-01T00:14:54-00:00", "Great. Can't wait to hear this thoughts.")
  strzok_to_page(child_file, "2016-11-01T00:16:25-00:00", "Oh, it wasn't his thoughts (though he supports Andy, btw) - its who and what people said/asked him. --Redacted--")
  strzok_to_page(child_file, "2016-11-01T00:16:49-00:00", "And remind me Bills comments about Mike vs Randy response this morning. ...")
  page_to_strzok(child_file, "2016-11-01T00:17:02-00:00", "I want to know now. This is kind of sh*tty of you to hand out there.")
  page_to_strzok(child_file, "2016-11-01T00:17:42-00:00", "Did you see the times this evening? Another Apuzzo/Schmidt special, all about the damn review process.")
  strzok_to_page(child_file, "2016-11-01T00:18:50-00:00", "Sorry.\n\nAnd no...\U0001f621")
  page_to_strzok(child_file, "2016-11-01T00:19:28-00:00", "You seriously can't tell me now? \U0001f612")
  m = page_to_strzok(child_file, "2016-11-01T00:19:56-00:00", "Not on this. Imsg in a bit?")
  m.addnote("Imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-11-01T00:20:16-00:00", "You can't just talk?")
  strzok_to_page(child_file, "2016-11-01T00:20:47-00:00", "What's the article? I'm not in the cool kids club who gets a notification")
  strzok_to_page(child_file, "2016-11-01T00:49:18-00:00", "Did you read the MJ article?!?!?!?")
  strzok_to_page(child_file, "2016-11-01T00:58:17-00:00", "I'm sorry.\U0001f614\n\nThe articls isn't nearly as important, obviously, but it's depression....")
  strzok_to_page(child_file, "2016-11-01T13:06:23-00:00", "Hey have to go to meeting with Jon --Redacted-- right now")
  page_to_strzok(child_file, "2016-11-01T13:09:07-00:00", "I'm on with --Redacted-- Sorry.")
  strzok_to_page(child_file, "2016-11-01T13:21:02-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-01T16:57:29-00:00", "Just leaving his ofc now. He's going down to talk to the boss. It's not looking good.")
  strzok_to_page(child_file, "2016-11-01T18:11:09-00:00", "Hey done. You around? Bill shared Andy's email")
  page_to_strzok(child_file, "2016-11-01T18:11:39-00:00", "I'm waiting outside his ofc.")
  strzok_to_page(child_file, "2016-11-01T18:29:15-00:00", "K. Let me know when you're free")
  strzok_to_page(child_file, "2016-11-01T21:50:57-00:00", "Hey Bill want to talk so I'm going to be out. He said it wouldn't take long but Dina and Jen will join so I truly have no idea.\n\nFor sure will be here until a little after 6. Call my desk if you want after that, I'll use it as an excuse to get up")
  page_to_strzok(child_file, "2016-11-01T22:02:58-00:00", "I'm sorry just got out. Lots to share.")

  # Page 428
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-01T23:05:28-00:00", "Figured out why they legally can't do what you just said. We are comparing against material (to determine what is new) that we obtained during the investigation that we cannot share with them.")
  m = strzok_to_page(child_file, "2016-11-01T23:05:31-00:00", "Oh hey! Did you realize we affirmatively tweeted abou tthe release of the wjc foundation? Yup! Let's take out the highlighter....")
  m.addnote("wfc - William Jefferson Clinton")
  page_to_strzok(child_file, "2016-11-01T23:25:15-00:00", "Yes! I heard about it at wrap. Utter complete disaster.")
  strzok_to_page(child_file, "2016-11-01T23:27:04-00:00", "I mean, wtf?!?!?\n\nWe're getting crucified in the news. We should have waited. Did JR or anyone weigh in?")
  page_to_strzok(child_file, "2016-11-01T23:27:59-00:00", "It was automatic. They got it back up and running two days ago. \U0001f612")
  page_to_strzok(child_file, "2016-11-01T23:28:55-00:00", "I'll explain when we talk.")
  page_to_strzok(child_file, "2016-11-01T23:29:10-00:00", "Oh and ruemmler called Jim b...")
  strzok_to_page(child_file, "2016-11-02T00:29:32-00:00", "See email I just sent. Recommend you let the request (whatever for it ended up taking) trickle down, then --Redacted-- and i will address")
  strzok_to_page(child_file, "2016-11-02T00:31:35-00:00", "You CANNOT source me")
  page_to_strzok(child_file, "2016-11-02T00:35:30-00:00", "I will. This makes me VERY angry.")
  strzok_to_page(child_file, "2016-11-02T00:35:54-00:00", "Well, Jon and I agree")
  page_to_strzok(child_file, "2016-11-02T00:36:23-00:00", "Yeah, wtf is Bill and Randy's plan?")
  strzok_to_page(child_file, "2016-11-02T00:37:09-00:00", "Like I said, see Jon and ny convo. ...")
  m = strzok_to_page(child_file, "2016-11-02T00:38:02-00:00", "And honestly, the other thing I'm thinking about? \"The cat's away....\"")
  m.addnote("Cat's away - Could be a reference to Andy McCabe being in London")
  strzok_to_page(child_file, "2016-11-02T00:45:44-00:00", "This response, from Jon:\n...and considering we haven't shared any facts, those certainly aren't factoring into decisionmaking. We should essentially have no reason for contact with NYO going forward in this.")
  page_to_strzok(child_file, "2016-11-02T00:46:17-00:00", "I know. Which is what I tried to impose.")
  page_to_strzok(child_file, "2016-11-02T00:47:03-00:00", "God, this makes me very very angry. I honestly think I should bow out rather than find out things, be unable to tell Andy, and powerless to stop them.")
  strzok_to_page(child_file, "2016-11-02T00:48:24-00:00", "No. Need you on the inside now more than ever. Truly. And no bs, your country needs you now.\n\nWe are going to have to be very wise about all of this.")
  strzok_to_page(child_file, "2016-11-02T00:49:01-00:00", "The only thing wrong in your statement is your powerlessness")
  page_to_strzok(child_file, "2016-11-02T00:49:09-00:00", "I am going to have to use Jim Baker a lot to get to the D. But I don't trust that he can convey details accurately!")

  # Page 429
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-11-02T00:49:27-00:00", "I'm not sure I agree with you there.")
  strzok_to_page(child_file, "2016-11-02T00:50:14-00:00", "Not just JB. And this is a finite thing. I want to be done before the inauguration.")
  strzok_to_page(child_file, "2016-11-02T00:50:45-00:00", "You're wrong. Not the type of power you (or i) would prefer, but not powerless")
  page_to_strzok(child_file, "2016-11-02T00:50:47-00:00", "Who else can I use?")
  page_to_strzok(child_file, "2016-11-02T00:51:02-00:00", "JR? Do't think so.")
  m = strzok_to_page(child_file, "2016-11-02T00:53:41-00:00", "I don't know. Trisha (to Mike) --Redacted--\n\nAnd not just you. Me, Jon, --Redacted--\n\nMe? Randy. My QT roommate.")
  m.addnote("QT - Quantico")
  strzok_to_page(child_file, "2016-11-02T00:56:32-00:00", "We're going to make sure the right thing is done.\n\nYou underestimate my - our - enthusiasm and competence and motivation.\n\nYou can be worried. Take strength from me. Then add Jon and --Redacted-- and Bill and Jim onto that. It's gonna be ok")
  page_to_strzok(child_file, "2016-11-02T00:57:54-00:00", "I know you guys are. I have complete confidence in the team. You know that.")
  strzok_to_page(child_file, "2016-11-02T01:02:14-00:00", "Our team.\n\nI do. I'm telling you to take comfort in that.")
  page_to_strzok(child_file, "2016-11-02T01:06:21-00:00", "I just don't know.")
  page_to_strzok(child_file, "2016-11-02T01:07:00-00:00", "And god, I just had a horrible realization: what if I can't talk to Andy about my back and forth about what to do?!")
  strzok_to_page(child_file, "2016-11-02T01:07:33-00:00", "? What do you mean?")
  page_to_strzok(child_file, "2016-11-02T01:08:52-00:00", "Baker said to me tonight that if Bowdich or Steinbach come to him about the leadership decision that he shouldn't discuss it with them because once he is out he shouldn't have discussions about any of it, even personnel.")
  page_to_strzok(child_file, "2016-11-02T01:09:24-00:00", "Pete, I really think this isn't a good idea for me.")
  strzok_to_page(child_file, "2016-11-02T01:13:31-00:00", "Lisa. The more I think about it, the more certain I am that it is.")
  strzok_to_page(child_file, "2016-11-02T01:14:16-00:00", "Your conversations with Andy would be covered under atty privilege, no?")
  page_to_strzok(child_file, "2016-11-02T01:14:53-00:00", "As I said to you the other day, and I meant, my country just might have to do without me this time. I mean it.")
  page_to_strzok(child_file, "2016-11-02T01:15:09-00:00", "I'm not sure I'm following your second.")
  strzok_to_page(child_file, "2016-11-02T01:15:49-00:00", "Stop it\n\nYes, but give me 5")
  page_to_strzok(child_file, "2016-11-02T01:16:29-00:00", "Jesus. Another article pushed by nyt on this.")
  m = page_to_strzok(child_file, "2016-11-02T01:19:03-00:00", "Richman is a friend of Comey and baker. \U0001f612")
  m.addnote("Richman - Possibly Dan Richman the man Comey leaked to")

  # Page 430
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-02T13:50:03-00:00", "Bill told Randy no.")
  strzok_to_page(child_file, "2016-11-02T13:50:13-00:00", ":) yay Bill")
  page_to_strzok(child_file, "2016-11-02T14:40:33-00:00", "No. Herring here. Stand by.")
  strzok_to_page(child_file, "2016-11-02T21:04:40-00:00", "Hey big dummy you were supposed to stop by and unlock you computer so I could finish self assessment. ...\U0001f60a")
  page_to_strzok(child_file, "2016-11-02T21:24:41-00:00", "I went back to back with mtg with andy to wrap.")
  strzok_to_page(child_file, "2016-11-02T21:27:11-00:00", "Btw it took me staring at Kortan to out the info abou the nyt\n\nAlso remind me re --Redacted--")
  strzok_to_page(child_file, "2016-11-02T21:27:17-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-02T21:27:44-00:00", "Huh? Not following your kortan comment. Talk to you later about it.")
  page_to_strzok(child_file, "2016-11-02T21:28:34-00:00", "Gotta go back to kortan.")
  page_to_strzok(child_file, "2016-11-02T21:30:33-00:00", "Do you know how to get a cached copy of the version of the article the times pushed out last night re Manafort and foundation?")
  strzok_to_page(child_file, "2016-11-02T21:31:45-00:00", "How do you mean? An old version, or without showing current interest in nyt")
  page_to_strzok(child_file, "2016-11-02T21:32:20-00:00", "Yes. They changed the article dramatically after kortan called, we want to see the old version.")
  strzok_to_page(child_file, "2016-11-02T21:38:52-00:00", "Who's the byline? Let me do some looking")
  page_to_strzok(child_file, "2016-11-02T21:45:47-00:00", "Coming back now. Apuzzo plus his buds.")
  strzok_to_page(child_file, "2016-11-02T23:48:41-00:00", "Getting Mangialardos for next Tues' meeting...and cancelling --Redacted-- I think.")
  strzok_to_page(child_file, "2016-11-02T23:49:23-00:00", "--Redacted-- called, left a msg...")
  page_to_strzok(child_file, "2016-11-03T00:02:10-00:00", "Yeah, bill and to scare talked about getting subs.")
  page_to_strzok(child_file, "2016-11-03T00:03:08-00:00", "I suppose I'm okay with cancelling bob. Just this once.")
  strzok_to_page(child_file, "2016-11-03T00:08:03-00:00", "Bill just called to say George called Bill for an update. Bill tap danced without saying anything. George proposed I update --Redacted-- twice a day. \U0001f612\n\nI told Bill to mention at the meeting tomorrow and come up with an answer.")
  page_to_strzok(child_file, "2016-11-03T00:15:15-00:00", "Also a dad is not updating --Redacted-- twice a day. Thanks, but no.")
  page_to_strzok(child_file, "2016-11-03T00:24:53-00:00", "Also, we are going to have to share with DOJ. There's already not a lot of trust here, and let's face it, --Redacted-- and George are not the problems.")

  # Page 431
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-03T00:26:08-00:00", "--Redacted-- And no, it's not. I'm not sure anyone should be\n\nI agree with you. When we do it matters, though, and in what detail.")
  page_to_strzok(child_file, "2016-11-03T00:26:54-00:00", "I agree. But how much we've gone through and what we've found seems reasonable.")
  strzok_to_page(child_file, "2016-11-03T00:31:32-00:00", "I may have to short someone so as to give Andy and the Director one.")
  strzok_to_page(child_file, "2016-11-03T00:36:29-00:00", "I'm sure if Dave (or Mike) sees it in the Q will by why not them, too. stupid politics")
  #strzok_to_page(child_file, "2016-11-03T00:36:58-00:00", "Or get it for my original plan and do the kiss ass chain of command plan later.")
  #page_to_strzok(child_file, "2016-11-03T00:50:57-00:00", "Sorry. Rybicki called. Time line article in the post is super specific and not good. Doesn't make sense because I didn't have specific information to give.")
  strzok_to_page(child_file, "2016-11-03T00:55:50-00:00", "What post article?!?")
  page_to_strzok(child_file, "2016-11-03T00:56:28-00:00", "Just went up. WaPo.")
  strzok_to_page(child_file, "2016-11-03T00:57:08-00:00", "Goddamn bills opaque comments......")
  page_to_strzok(child_file, "2016-11-03T00:57:36-00:00", "Call you?")
  #strzok_to_page(child_file, "2016-11-03T00:57:45-00:00", "Can I send to team?")
  page_to_strzok(child_file, "2016-11-03T00:57:54-00:00", "Yes")
  page_to_strzok(child_file, "2016-11-03T01:15:38-00:00", "Okay I can talk again.")
  strzok_to_page(child_file, "2016-11-03T01:34:00-00:00", "Need to talk to you when you're done")
  page_to_strzok(child_file, "2016-11-03T01:34:27-00:00", "I'm done. But rybicki may call back. But I can talk now.")
  page_to_strzok(child_file, "2016-11-03T01:59:36-00:00", "I hate this case.")
  page_to_strzok(child_file, "2016-11-03T02:26:42-00:00", "Sorry, on with rybicki again. Email incoming from him.")
  strzok_to_page(child_file, "2016-11-03T02:39:40-00:00", "To me? Didn't get it.")
  page_to_strzok(child_file, "2016-11-03T02:40:01-00:00", "You should. Maybe he will in the am.")
  m = page_to_strzok(child_file, "2016-11-03T02:40:57-00:00", "Also you can imsg but I might not be able to respond.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  m = strzok_to_page(child_file, "2016-11-03T02:42:27-00:00", "I didn't. Whatever is fine. I'll imsg in a sec, need to work out timing.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-11-03T02:43:12-00:00", "It is coming.")
  page_to_strzok(child_file, "2016-11-03T02:49:28-00:00", "Ok I should be able to when you are free.")

  # Page 432
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-03T02:55:34-00:00", "Ok so obviously I want the background on the email.")
  strzok_to_page(child_file, "2016-11-03T03:18:53-00:00", "And dammit I specifically ASKED for guidance about what and to WHOM we tell DoJ")
  strzok_to_page(child_file, "2016-11-03T03:47:54-00:00", "--Redacted-- Bill talked to George well before Jim's email. DoJ hs hyperventilating --Redacted-- I want to talk!!!!")
  page_to_strzok(child_file, "2016-11-03T10:00:48-00:00", "You guys didn't do anything wrong. Just say the D wanted to think about it. --Redacted--")
  strzok_to_page(child_file, "2016-11-03T10:15:36-00:00", "Well, it's a little more than that. Bill did talk to George. I guess he didn't tell him much, but still. Anyway. --Redacted--")
  page_to_strzok(child_file, "2016-11-03T10:28:29-00:00", "I know it's a little more than that. I'm just saying now that we are going to do regular updates just say that.")
  strzok_to_page(child_file, "2016-11-03T10:36:52-00:00", "What did Rybicki have to say?")
  page_to_strzok(child_file, "2016-11-03T10:37:14-00:00", "Will tell you later.")
  strzok_to_page(child_file, "2016-11-03T10:37:41-00:00", "K. Stuff to tell you later, too")
  #page_to_strzok(child_file, "2016-11-03T11:29:41-00:00", "The nyt probability numbers are dropping every day. I'm scared for our organization.")
  strzok_to_page(child_file, "2016-11-03T11:30:50-00:00", "Was just talking to Bill then Andy called him and he had to get off")
  strzok_to_page(child_file, "2016-11-03T11:32:36-00:00", "Stein and moron --Redacted-- are F'ing everything up, too")
  page_to_strzok(child_file, "2016-11-03T11:40:09-00:00", "Stein?")
  page_to_strzok(child_file, "2016-11-03T11:40:19-00:00", "Oh right.")
  strzok_to_page(child_file, "2016-11-03T11:40:39-00:00", "Green")
  strzok_to_page(child_file, "2016-11-03T11:45:11-00:00", "Oh :(\n\nBill wants me to call --Redacted-- before 10, which means now. \U0001f612 Told.him I would bow hut that Jon and I are too busy to be producing regular, let alone twice daily updates to a gs15. He was fine with that.\n\nFor background, he gave a general update to George at 615 last night. I am certain that's probably not what was communicated to Rybicki. Bill is feeling defensive abou the email. I told him we had done nothing wrong.")
  strzok_to_page(child_file, "2016-11-03T17:05:17-00:00", "Shhh don't tell anyone, mtg invite is thank you good job calendar hand out..... \U0001f60a\n\nYou back?")
  strzok_to_page(child_file, "2016-11-03T17:24:15-00:00", "Sigh. Have a 130 with Bill, prob nor enough to stop by.\n\nWe're doing par after D brief")
  strzok_to_page(child_file, "2016-11-03T23:04:29-00:00", "Bill said be forwarded, hopefully you were on it; I was not. If there is substabtive response /conversation, would appreciate the feedback.")

  # Page 433
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-11-03T23:05:21-00:00", "Nope. Didn't get anything. That's irritating. Green side?")
  strzok_to_page(child_file, "2016-11-03T23:13:47-00:00", "Yes. If he forwards anything back, I'll add you.")
  strzok_to_page(child_file, "2016-11-03T23:15:44-00:00", "Not much to say about it, though.")
  strzok_to_page(child_file, "2016-11-04T01:27:32-00:00", "--Redacted-- worry we'll be drafting this damn statement all day.")
  m = strzok_to_page(child_file, "2016-11-04T02:02:39-00:00", "And no I don't want to talk anymore. --Redacted-- said --Redacted-- had called him, also apparently talked to Jim earlier this week, was going to call him again tonight. I sent an email to Jim to call me for details about what ces did and didn't tell her. I don't really care at this point.")
  m.addnote("ces - ?? Stein?")
  page_to_strzok(child_file, "2016-11-04T02:21:57-00:00", "--Redacted-- We might have this stmt out and be substantially done. --Redacted--")
  page_to_strzok(child_file, "2016-11-04T02:23:21-00:00", "No Pete. It's your JOB. And plus she actually knows what you're doing this time. And that the American presidential election, and thus, the state of the world, actually hands in the balance.")
  #page_to_strzok(child_file, "2016-11-04T03:19:04-00:00", "Dude. On Inauguration Day, in addition to our kegger we should also have a screening of the Weiner documnetary! \U0001f60a")
  page_to_strzok(child_file, "2016-11-04T14:03:23-00:00", "I'm sending the dogs, --Redacted-- down to the review room in about 10. --Redacted-- Randy's guy, will be with. \U0001f612 Tried to stop that, so maybe just a heads up to --Redacted-- but let the rest of the team be surprised.")
  strzok_to_page(child_file, "2016-11-05T17:22:42-00:00", "I hate this case")
  strzok_to_page(child_file, "2016-11-05T20:24:17-00:00", "Ok. \U0001f615\n\nArriving work around 5 or so")
  page_to_strzok(child_file, "2016-11-05T22:00:48-00:00", "He had heard. Guy is in custody. Thanks.")
  strzok_to_page(child_file, "2016-11-05T22:20:35-00:00", "Yeah apparently it's been there since 11")
  strzok_to_page(child_file, "2016-11-05T22:21:11-00:00", "Guess we're not so good at the paint scrubbing thing. Or, maybe, you know, tape some trash bags over it or something")
  m = strzok_to_page(child_file, "2016-11-05T22:40:45-00:00", "Jon and I forming the new facilities maintenance branch of the mye team. Cause we're doing it ALL...")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok(child_file, "2016-11-05T23:52:38-00:00", "I don't want to make a statement anymore.")
  strzok_to_page(child_file, "2016-11-05T23:58:39-00:00", "Oh yeah still here. Here until we're done, review the potential unique cat 1s whenever we're done and report up.\n\nYeah I don't either. We're kind of out of the news cycle, let's leave it that way")
  strzok_to_page(child_file, "2016-11-06T00:39:34-00:00", "Going though status now. We may be complete reviewing in an hour.")

  # Page 434
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-06T00:39:59-00:00", "--Redacted-- Jon and I going to look at potentially cat 1s")
  page_to_strzok(child_file, "2016-11-06T00:49:05-00:00", "Sorry, I don't think I am calling at 10.")
  page_to_strzok(child_file, "2016-11-06T01:10:19-00:00", "Why didn't you tell me all of you would be in this afternoon? \U0001f612")
  strzok_to_page(child_file, "2016-11-06T01:13:18-00:00", "A) im really sorry\n\nB) i didn't know we would be. Jon --Redacted-- and I didn't get in until 5")
  strzok_to_page(child_file, "2016-11-06T02:42:03-00:00", "Hi. Missed you. No real update. The three of us are going through the 3l (1000 each) to narrow down so the team can come back tomorrow early and de-dupe")
  strzok_to_page(child_file, "2016-11-06T06:09:20-00:00", "Finishing up")
  strzok_to_page(child_file, "2016-11-06T06:34:09-00:00", "Leaving finally now. Turns our no new classified")
  page_to_strzok(child_file, "2016-11-06T09:23:53-00:00", "It was okay.\n\nWhy didn't you tell me that you all were getting together? Did someone not want me there?")
  strzok_to_page(child_file, "2016-11-06T11:42:25-00:00", "I thought I did mention. Jon and I were there to get an update and buy dinner and monitor progress, which evolved as you saw into very quick progress. --Redacted-- arrived at some point in the process. Certainly no intent to exclude you.")
  strzok_to_page(child_file, "2016-11-06T11:44:07-00:00", "I didn't know --Redacted-- was coming until she was there - --Redacted--")
  page_to_strzok(child_file, "2016-11-06T12:11:03-00:00", "I still don't know that we should make this statement.")
  m = strzok_to_page(child_file, "2016-11-06T12:11:41-00:00", "I don't either. Imsg?")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2016-11-06T14:09:05-00:00", "Hey do you want to send that email out suggesting a conference call? I can if you want but defer to you.\n\n--Redacted--")
  page_to_strzok(child_file, "2016-11-06T14:15:11-00:00", "I did at 8:56. Did you not get it?")
  strzok_to_page(child_file, "2016-11-06T14:28:46-00:00", "I did. But my phone has stupid 20 minute gaps when it decodes it needs a break to rest or something")
  strzok_to_page(child_file, "2016-11-06T14:29:21-00:00", "Add Conf room might be smart if we want to edit whilst we talk")
  page_to_strzok(child_file, "2016-11-06T14:30:55-00:00", "I'm having a hard time deciding what is appropriate for a Weekend With the Director. Have on grey jeans, navy v-neck, tan cardi. Brown loafers? Brown boots?")
  strzok_to_page(child_file, "2016-11-06T14:36:09-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-06T14:37:36-00:00", "Sorry I'm very close to being late")

  # Page 435
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-06T14:38:23-00:00", "Hey, just trying to pass along the substance of a call I just had with Jim.")
  page_to_strzok(child_file, "2016-11-06T14:38:45-00:00", "Will call from car")
  strzok_to_page(child_file, "2016-11-06T14:38:54-00:00", "And yeah me too. On bridge")
  strzok_to_page(child_file, "2016-11-06T14:42:35-00:00", "Great ANOTHER fucking road race")
  page_to_strzok(child_file, "2016-11-06T14:54:44-00:00", "Might be about 2 minutes late.")
  strzok_to_page(child_file, "2016-11-06T14:55:47-00:00", "Rgr. In add Conf room")
  page_to_strzok(child_file, "2016-11-06T18:14:05-00:00", "We're still in the D's conf room.")
  strzok_to_page(child_file, "2016-11-06T18:15:06-00:00", "Nice! D still there? :)")
  strzok_to_page(child_file, "2016-11-06T18:15:52-00:00", "Would you pls ask Jon to check his email? Q for him.\n\nThanks")
  page_to_strzok(child_file, "2016-11-06T18:16:26-00:00", "He doesn't have your phone. Are you done?")
  page_to_strzok(child_file, "2016-11-06T18:16:49-00:00", "Can you come back in here? Are you still on the call?")
  strzok_to_page(child_file, "2016-11-06T18:17:01-00:00", "No still on call")
  strzok_to_page(child_file, "2016-11-06T18:17:24-00:00", "Disregard, --Redacted-- got answer")
  page_to_strzok(child_file, "2016-11-06T18:26:48-00:00", "We're watching football in the directors office now. It's kind of surreal.")
  strzok_to_page(child_file, "2016-11-06T19:56:58-00:00", "It's funny I see Jim and Jim on the email and feel painfully left out. There's a Bridgewater flaw I need to work on. \U0001f615")
  page_to_strzok(child_file, "2016-11-06T19:58:34-00:00", "That's probably because they both know that part of his life. Don't feel excluded --Redacted-- It's not personal in the least.")
  strzok_to_page(child_file, "2016-11-06T20:03:36-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-06T20:04:34-00:00", "I know. But you know it's there, which is the first step to not letting it conquer you.")
  strzok_to_page(child_file, "2016-11-06T20:30:52-00:00", "Out on CNN now")
  strzok_to_page(child_file, "2016-11-06T20:31:00-00:00", "And fox")
  strzok_to_page(child_file, "2016-11-06T20:31:58-00:00", "I WANT TO WATCH THIS WITH YOU!")
  strzok_to_page(child_file, "2016-11-06T20:33:54-00:00", "Trump about to get off his plane")
  strzok_to_page(child_file, "2016-11-06T20:34:43-00:00", "Going to pour myself a glass of wine...")

  # Page 436
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-11-06T20:52:54-00:00", "I'm on fox. Trump is talking about her.")
  #page_to_strzok(child_file, "2016-11-06T20:53:42-00:00", "He's talking about cartwright and Patraeus and how they're not protected. She's protected by a rigged system.")
  page_to_strzok(child_file, "2016-11-07T01:43:03-00:00", "Good lord...\n\nInside Donald Trump\u2019s Last Stand: An Anxious Nominee Seeks Assurance http://nyti.ms/2esuTs3")
  page_to_strzok(child_file, "2016-11-07T09:31:20-00:00", "This was good. --Redacted-- --Redacted--\n\nIs there Life After Trump? http://nyti.ms/2eppNN6")
  strzok_to_page(child_file, "2016-11-07T12:05:34-00:00", "Was just clearing 8 emails that somehow appeared overnight. Concerningly, there were several from earlier (ie, 5-ish) that didn't appear until after I last check this around 8")
  strzok_to_page(child_file, "2016-11-07T12:11:13-00:00", "Ok. I have a 930 with the team and a 10 with --Redacted-- and --Redacted-- (I can do the 10 on the phone)")
  strzok_to_page(child_file, "2016-11-07T12:14:49-00:00", "Ok. I'm going to rush now. Will see if DOJ can call earlier. --Redacted--")
  strzok_to_page(child_file, "2016-11-07T13:25:48-00:00", "Once conference call done")
  page_to_strzok(child_file, "2016-11-07T16:01:13-00:00", "Andy asked to meet with me right after my 11; will hit you up afterwards.")
  page_to_strzok(child_file, "2016-11-07T17:16:26-00:00", "I'm done now too. Need to talk to you about a couple of work things.")
  strzok_to_page(child_file, "2016-11-07T17:18:12-00:00", "K. In with Bill. He hoped I went to --Redacted-- mtg, told him I didn't know about it but would catch up with you")
  page_to_strzok(child_file, "2016-11-07T17:20:03-00:00", "It's essentially a pissing match btwn ny and Sf. Nothing for cd at this time. But yes, I can describe.")
  page_to_strzok(child_file, "2016-11-07T20:08:32-00:00", "Waiting to meet with DD at 3:30 now. I should have gone at lunch. \U0001f612")
  strzok_to_page(child_file, "2016-11-07T20:11:34-00:00", "Apparently no...just came up...\n\nTalked to Bill about our convo, are you Ok for me to reach out to JB to ask to speak about what you discussed earlier? His thoughts will impact what we do and we need to move one way or the other")
  strzok_to_page(child_file, "2016-11-07T20:28:34-00:00", "How long is your 330? Want to try afterwards at 430?")
  page_to_strzok(child_file, "2016-11-07T20:29:16-00:00", "I have to go sooner than that. I probably have to go right after I am done with Andy.")
  strzok_to_page(child_file, "2016-11-07T22:17:14-00:00", "--Redacted-- Jason wanted to talk idea of providing briefings to the Hill, menioned you two working on how to approach drafting them tomorrow")
  strzok_to_page(child_file, "2016-11-07T23:06:28-00:00", "Can you talk work? \U0001f621")
  page_to_strzok(child_file, "2016-11-07T23:09:44-00:00", "No I really can't.")
  strzok_to_page(child_file, "2016-11-07T23:12:20-00:00", "Np. Just JB frustration. It can wait. --Redacted--")

  # Page 437
  # OUTBOX == Page
  # INBOX == Strzok
  #page_to_strzok(child_file, "2016-11-08T01:32:02-00:00", "Impressive in its accuracy. \U0001f612\n\nHow the F.B.I. Reviewed Thousands of Emails in One Week http://nyti.ns/2egA2sg")
  m = strzok_to_page(child_file, "2016-11-08T01:56:33-00:00", "OMG THIS IS F*CKING TERRIFYING:\nA vistory by Mr. Trump remains possible: Mrs. Clinton\u2019s chance of losing is about the same as the probability than an N.F.L. kicker misses a 38-yard field goal.")
  m.tag("Hatred", "TERRIFYING is not a term of endearment", truxton.TAG_ORIGIN_HUMAN)
  page_to_strzok(child_file, "2016-11-08T02:05:51-00:00", "Yeah, that's not good")
  strzok_to_page(child_file, "2016-11-08T02:42:03-00:00", "I'm sorry. Managed to get into a huge fight here about the Bu and Clinton. Because --Redacted-- just can't stop at fair observations. She has to assert mastery of things about which she has NO knowledge.")
  page_to_strzok(child_file, "2016-11-08T02:43:40-00:00", "She does realize you've been in EVERY conversation that has been had about this case, right?")
  strzok_to_page(child_file, "2016-11-08T02:44:54-00:00", "That we should have gone on the record saying Kallstrom and others are not credible (which may be valid), but then saying we could pull his tolls if we wanted to. Because she knows all about our policy regarding investigations of members of the media. \U0001f621")
  strzok_to_page(child_file, "2016-11-08T02:45:31-00:00", "Yes. But she's an expert who knows everything.\n\nI'm telling you, it's wildly infuriating. She has good points but then assumes wildly impossible understanding of things to make groundless assertions.")
  page_to_strzok(child_file, "2016-11-08T02:46:06-00:00", "Uh, what crime are we investigating?\n\nAnd I'm sorry, that's a terrible idea. Go to war with the formers?")
  strzok_to_page(child_file, "2016-11-08T02:47:53-00:00", "Leaking information about ongoing investigations. Which is incorrect information. By agents who don't know about things talking to him.\n\nSee? That's the thing. Her initial point, that we should have gone after the agents talking harder and sooner, is not unreasonable. But the subsequent discussion falls into uninformed assertions.")
  page_to_strzok(child_file, "2016-11-08T02:49:08-00:00", "If it's not classified, what's the crime though?")
  strzok_to_page(child_file, "2016-11-08T02:49:26-00:00", "Maybe we should go to war with them, if they're spouting bile like Kallstrom. He's really out of bounds. THat is a valid debate. Talking - telling - me how we should have done it is what's infuriating.")
  strzok_to_page(child_file, "2016-11-08T02:50:35-00:00", "There's not a crime. So you publicly shame or disavow him. And you find out who's talking to him and go after them with opr. It's a legitimate criticism that we might have looked sooner at all these people running their mouths to the press.")
  page_to_strzok(child_file, "2016-11-08T02:50:52-00:00", "I get it. I'm not trying to fight with you too. I'm sorry.")

  # Page 438
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-08T02:53:39-00:00", "I mean how in the HELL do you assume you know something outside of your field? How can you not, as an accomplished lawyer, understand how far and wide the field of law is? You or --Redacted-- or whoever would ever assume knowledge of things outside of criminal law. It boggles my mind.")
  strzok_to_page(child_file, "2016-11-08T15:44:13-00:00", "I don't think it's bad. I think there are agents doing as much who will not get a visit from the DD because Jon does a good job of advertising his people")
  strzok_to_page(child_file, "2016-11-08T15:47:25-00:00", "They are Jens people not mine.\n\nAlthough it looks like Jon said --Redacted--")
  # Page 26 has unredacted version of this message
  # m = strzok_to_page(child_file, "2016-11-08T15:48:31-00:00", "Is he going to the --Redacted-- room, or just sioc?")
  # Page 26 has unredacted version of this message
  # page_to_strzok(child_file, "2016-11-08T15:49:16-00:00", "He will go see the analysts, --Redacted-- room, and sioc. Maybe I'll take him by duhadaway as well.")
  # strzok_to_page(child_file, "2016-11-08T15:52:09-00:00", "Ok I'm with --Redacted-- but going to Duhadway at 11 with --Redacted--")
  strzok_to_page(child_file, "2016-11-08T16:03:27-00:00", "I guess I'm also cranky that --Redacted-- has a prominent role at the 11 mtg that he should be at ON ELECTION DAY.")
  strzok_to_page(child_file, "2016-11-09T01:06:45-00:00", "\U0001f60a\n\nHsppy Election geekdom here.")
  page_to_strzok(child_file, "2016-11-09T04:06:58-00:00", "Trump won NC")
  page_to_strzok(child_file, "2016-11-09T04:20:14-00:00", "PBS is projecting Florida as well.")
  page_to_strzok(child_file, "2016-11-09T04:35:02-00:00", "CNN is projecting FL for Trump.")
  strzok_to_page(child_file, "2016-11-09T05:49:11-00:00", "Damn")
  page_to_strzok(child_file, "2016-11-09T09:34:14-00:00", "And there it is.")
  #page_to_strzok(child_file, "2016-11-09T09:58:18-00:00", "Analogous to the public editor article Bill handed out.\n\nNews Media Yet Again Misreads America\u2019s Complex Pulse http://nyti.ms/2eCqXVM")
  strzok_to_page(child_file, "2016-11-09T12:13:37-00:00", "Too hard to explain here. Election related. Which is godawful bad.\n\nSure")
  page_to_strzok(child_file, "2016-11-09T09:58:18-00:00", "Are you even going to give out your calendars? Seems kind of depressing. Maybe it should just be the first meeting of the secret society.")
  page_to_strzok(child_file, "2016-11-09T12:44:06-00:00", "And Christ, we should just hit those thumb drives now. Their opinion is totally irrelevant.")
  strzok_to_page(child_file, "2016-11-09T12:50:49-00:00", "No. And yes")
  page_to_strzok(child_file, "2016-11-09T12:51:16-00:00", "I'll mention to Andy.")
  strzok_to_page(child_file, "2016-11-09T16:35:28-00:00", "Omg I am so depressed")
  page_to_strzok(child_file, "2016-11-09T17:03:50-00:00", "Yes, maybe. I need to see what --Redacted-- wants to do first.")

  # Page 439
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-11-09T18:01:21-00:00", "And honestly, I don't know if I can eat. I am very nauseous.")
  strzok_to_page(child_file, "2016-11-09T23:41:50-00:00", "Nice. Flash mob in front of old post office. Great for the commute.")
  page_to_strzok(child_file, "2016-11-10T09:32:53-00:00", "Hey without thinking I replied to the email you sent me on Gmail. But it went to your verizon. So please clear. Let me know if you want me to send it again somewhere else.")
  page_to_strzok(child_file, "2016-11-10T11:11:57-00:00", "you clear verizon?")
  page_to_strzok(child_file, "2016-11-10T11:15:42-00:00", "Okay, I've gotta go. Read that lawfare article. It's really sobering.")
  strzok_to_page(child_file, "2016-11-10T11:16:34-00:00", "I'm reading it now. Resent you (and --Redacted--) his much earlier post about whether to stay in government")
  strzok_to_page(child_file, "2016-11-10T13:11:21-00:00", "Bill just sent a two hour invite to talk strategy from 1-3. Im in no mood to do so.")
  strzok_to_page(child_file, "2016-11-10T17:50:43-00:00", "Drafting TPs for andy, can I send to you and further refine so he can hopefully call tomorrow.\n\nWe're now thinking Bill and I go, will explain. Maybe even fly Sun night, met Mon, fly back Mon night, only out of the office one work day. Or fly Thurs after work, meet and fly back Fri.")
  page_to_strzok(child_file, "2016-11-11T01:11:17-00:00", "--Redacted-- went to Bob today. He got me two names as referals. \U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d\U0001f61d")
  strzok_to_page(child_file, "2016-11-11T01:12:51-00:00", "YES!!!!! We'll talk about it tomorrow. Send me the names so you dont forget and I can research. --Redacted--")
  strzok_to_page(child_file, "2016-11-11T12:33:32-00:00", "K. I'm sitting here kind of depressed about the reality of the TPs we wrote yesterday...")
  page_to_strzok(child_file, "2016-11-11T12:36:09-00:00", "I'm extremely depressed. Though today it's mostly not about work. Ttyl.")
  page_to_strzok(child_file, "2016-11-11T19:57:20-00:00", "God, I'm really f-ing depressed. --Redacted--")
  strzok_to_page(child_file, "2016-11-11T20:09:17-00:00", "--Redacted--\nBill just called to talk about the sentiment of everyone he was talking to....")
  page_to_strzok(child_file, "2016-11-11T20:27:58-00:00", "Just everything.\n\nSentiment about what?")

  # Page 440
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-11T20:38:49-00:00", "I'm sorry. --Redacted--\n\nEveryone thinks we had something to do with the outcome.\n")
  strzok_to_page(child_file, "2016-11-12T00:24:32-00:00", "I like.our new case name")
  page_to_strzok(child_file, "2016-11-12T00:56:45-00:00", "We'll see what others think. Alright, well sorry for interrupting. Talk to you later.")
  strzok_to_page(child_file, "2016-11-12T15:16:06-00:00", "Except recently it's been checking gtwn every 5\n\nHaving a really tough time with election this morning")
  page_to_strzok(child_file, "2016-11-12T18:20:00-00:00", "--Redacted-- changed to Trump weekend, but it was more expensive. He said I can save $500 if I go dec 20-23.")
  page_to_strzok(child_file, "2016-11-13T12:14:18-00:00", "NYTimes: Facebook, in Cross Hairs After Election, Is Said to Question Its Influence\nFacebook, in Cross Hairs After Election, Is Said to Question Its Influence http://nyti.ms/2erVrPd")
  strzok_to_page(child_file, "2016-11-13T12:34:03-00:00", "How Teens In The Balkans Are Duping Trump Supporters With Fake News\nhttps://www.buzzfeed.com/craigsilverman/how-macedonia-became-a-global-hub-for-pro-trump-misinfo?utm_term=.fwg4a1k1b2#.ws7vnxJxN6")
  page_to_strzok(child_file, "2016-11-13T12:56:56-00:00", "--Redacted-- you don't think there is any risk of that interfering with london? I don't want to change it again.")
  page_to_strzok(child_file, "2016-11-13T19:11:15-00:00", "I bought all the president's men. Figure I needed to brush up on watergate. \U0001f615")
  page_to_strzok(child_file, "2016-11-14T13:05:23-00:00", "Ran into --Redacted-- in the elevator. Told him I was sad about the prospect that he might not be staying on. He said he'd see what you want to do... so maybe there's hope...")
  #page_to_strzok(child_file, "2016-11-14T13:51:27-00:00", "God, being here makes me angry. Lots of high fallutin national security talk. Meanwhile, we have OUR task ahead of us...")
  strzok_to_page(child_file, "2016-11-14T14:06:53-00:00", "Yeah, I can only imagine. --Redacted-- So no update here. \U0001f621")
  page_to_strzok(child_file, "2016-11-14T14:10:15-00:00", "Okay, I'll follow up.")
  page_to_strzok(child_file, "2016-11-14T14:15:58-00:00", "Did I tell you that Charlie Savage is on a panel tomorrow? \U0001f621")
  page_to_strzok(child_file, "2016-11-14T14:40:34-00:00", "I really need to be here for the EAD/AD mtg because it will be all about transition.")
  strzok_to_page(child_file, "2016-11-14T14:41:10-00:00", "A) ha. You going to introduce yourself? I wouldn't, nothing good will come of it.\nB) open. Something worth listening to?")
  strzok_to_page(child_file, "2016-11-14T14:41:18-00:00", "Talking planning with --Redacted-- right now")
  page_to_strzok(child_file, "2016-11-14T14:42:37-00:00", "B) dd plan to lay out the lanes in the road. Just need to be there I think. Would love a ride back to hq. Will just miss a session here.")

  # Page 441
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-11-14T14:47:14-00:00", "Don't think so. Just Eads and ads. Dd doesn't intend to have anyone lower than an AD talk to transition folks. Frankly, I'd prefer he do all the engagement, but that's not feasible.")
  strzok_to_page(child_file, "2016-11-14T14:48:13-00:00", "Oh. Thought you meant this case.")
  strzok_to_page(child_file, "2016-11-14T14:48:15-00:00", "You have names?")
  page_to_strzok(child_file, "2016-11-14T14:48:51-00:00", "Not yet. --Redacted-- knows to email me here.")
  page_to_strzok(child_file, "2016-11-14T14:49:27-00:00", "Oh, sorry. No, I meant transition writ large. Sorry for the confusion.")
  strzok_to_page(child_file, "2016-11-14T15:01:51-00:00", "Still talking with --Radacted-- Many transition issues to talk with you about")
  strzok_to_page(child_file, "2016-11-14T15:15:56-00:00", "We'll get there ;)\n\nYou willing to set up lunch for me and --Redacted-- and you to introduce us to --Redacted-- to talk about C?")
  page_to_strzok(child_file, "2016-11-14T15:24:43-00:00", "Call you in a minute?")
  strzok_to_page(child_file, "2016-11-14T16:07:08-00:00", "Bill stuck his head in, said travel as early as tomorrow. Didn't get detail as I was in a mtg and he went upstairs to --Redacted--.")
  page_to_strzok(child_file, "2016-11-14T20:06:56-00:00", "God, I hate academics. Lots on the big bad fbi litigation with apple.")
  page_to_strzok(child_file, "2016-11-14T20:08:18-00:00", "It's making me very angry.")
  page_to_strzok(child_file, "2016-11-14T20:08:40-00:00", "BBC News: Trump and Putin hold telephone talks\nTrump and Putin hold telephone talks - http://www.bbc.co.uk/news/world-us-canada-37981770")
  strzok_to_page(child_file, "2016-11-14T22:57:39-00:00", "CNN news crawl says source reports Trump wants Top Secret clearance for his children")
  strzok_to_page(child_file, "2016-11-14T23:13:24-00:00", "Bill out of the office tonight, btw. So if you need him, call cell, or call me.")
  #strzok_to_page(child_file, "2016-11-15T01:43:02-00:00", "CNN: Source says naming Trump national security team a 'knife fight'")
  page_to_strzok(child_file, "2016-11-15T01:43:43-00:00", "Christ. What does that mean?!")
  strzok_to_page(child_file, "2016-11-15T01:46:21-00:00", "I can only guess difference of opinion between Trump and Republican establishment?")
  page_to_strzok(child_file, "2016-11-15T01:47:05-00:00", "I get it. I'm just exclaiming how f-ed it all is.")
  strzok_to_page(child_file, "2016-11-15T01:48:52-00:00", "Problem is, I don't know if that's it. I just have no idea...")
  page_to_strzok(child_file, "2016-11-15T01:50:30-00:00", "My god, Sessions for DoD or AG.")
  strzok_to_page(child_file, "2016-11-15T01:51:43-00:00", "Which is the f-ed uppedness of it")
  strzok_to_page(child_file, "2016-11-15T01:51:50-00:00", "Who said that?")

  # Page 442
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-15T01:52:20-00:00", "And if goes AG, then bolsters the Giuliani State idea")
  page_to_strzok(child_file, "2016-11-15T01:52:29-00:00", "The same article you referenced.")
  page_to_strzok(child_file, "2016-11-15T01:52:40-00:00", "It also says either Bolton or Giuliani for state.")
  strzok_to_page(child_file, "2016-11-15T01:56:53-00:00", "Ha. States going to EXPLODE")
  strzok_to_page(child_file, "2016-11-15T02:05:06-00:00", "What page you on?")
  page_to_strzok(child_file, "2016-11-15T02:06:37-00:00", "15. You distracted me with the news.")
  page_to_strzok(child_file, "2016-11-15T11:56:44-00:00", "Yeah, and then the Deputy Director told you to go to London on 24 hours notice.")
  page_to_strzok(child_file, "2016-11-16T08:25:18-00:00", "An article to share: How Bannon flattered and coaxed Trump on policies key to the alt-right\nHow Bannon flattered and coaxed Trump on policies key to the alt-right\nhttp://wapo.st/2fDJCSV")
  page_to_strzok(child_file, "2016-11-16T19:29:36-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-16T19:34:08-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-16T19:34:13-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-16T19:37:08-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-16T19:38:00-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-16T19:58:15-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-16T21:27:29-00:00", "You, your age, plans after Andy goes, how to keep talent in the Bu.")
  page_to_strzok(child_file, "2016-11-17T09:27:46-00:00", "God, this is scary. He apparently has not reached out to state at all for briefing materials. \U0001f612\n\nNYTimes: How Shinzo Abe Will Try to Size Up Donald Trump\nHow Shinzo Abe Will Try to Size Up Donald Trump http://nyti.ms/2elhGjP")
  strzok_to_page(child_file, "2016-11-17T09:33:36-00:00", "@ H/ @Yep. And the reason he wanted clearances for the kids is so Jared Kushner could receive the PDB with him. Legally, I think he can pretty much designate w")
  strzok_to_page(child_file, "2016-11-17T09:33:39-00:00", "@ H/ @hoever he wants to receive it without clearance..")
  page_to_strzok(child_file, "2016-11-17T09:34:27-00:00", "Article today is saying none of that is going to happen.")
  strzok_to_page(child_file, "2016-11-17T09:35:46-00:00", "@ P/ @I know he backed off of clearances, but there was another legal piece looking at his authority to just grant access, and it's pretty broad.\n\nAnd, I don't")
  page_to_strzok(child_file, "2016-11-17T09:35:52-00:00", "It's is broad. He doesn't. And yes.")

  # Page 443
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-17T09:35:52-00:00", "@ P/ @ think he has any idea what he's doing from one day to the next.")
  #strzok_to_page(child_file, "2016-11-17T19:22:30-00:00", "Re your email, --Redacted-- know --Redacted-- briefed Pence, right (just so there are no surprises)?")
  page_to_strzok(child_file, "2016-11-17T19:23:24-00:00", "I don't know if they would recall who did, but they know we sent someone. I spoke to --Redacted-- about it. We both think there's no action for us to take.")
  # Page 26 has unredacted version of this message
  # page_to_strzok(child_file, "2016-11-17T19:32:32-00:00", "Re above re email, it might be more important for --Redacted-- to know that --Redacted-- briefed Pence, no?")
  strzok_to_page(child_file, "2016-11-17T19:33:48-00:00", "I think that's a good idea. I'll talk with --Redacted-- so they build messaging/don't overlap")
  strzok_to_page(child_file, "2016-11-17T19:46:00-00:00", "Harumph. I want to see you. Is Andy on/regular length wrap?")
  page_to_strzok(child_file, "2016-11-17T19:46:19-00:00", "Yes, so far as I know.")
  strzok_to_page(child_file, "2016-11-17T19:47:10-00:00", "Talking with Bill. Do we want --Redacted-- to go with --Redacted-- instead of --Redacted-- for a variety of reasoms?")
  page_to_strzok(child_file, "2016-11-17T19:47:52-00:00", "Hmm. Not sure. Would it be unusual to have him show up again? Maybe another agent from the team?")
  strzok_to_page(child_file, "2016-11-17T19:49:43-00:00", "Or, he's 'the CI guy.' Same.might make sense. He can assess if thete are any news Qs, or different demeanor. If --Redacted-- husband is there, he can see if there are people we can develop for potential relationships")
  page_to_strzok(child_file, "2016-11-17T19:50:33-00:00", "Should I as Andy about it? Or Bill to reach out for andy?")
  strzok_to_page(child_file, "2016-11-17T19:52:09-00:00", "I told him I'm sure we could ask you to make the swap if we thought it was smart. It's not until Mon so Bill can always discuss with him tomorrow.")
  page_to_strzok(child_file, "2016-11-17T19:53:02-00:00", "It's the regular mtg with Jim and Andy.")
  strzok_to_page(child_file, "2016-11-17T19:54:54-00:00", "Oh. No you cant. WAH-wah.")
  page_to_strzok(child_file, "2016-11-18T01:12:18-00:00", "Ha. This gave me a chuckle.\n\nNYTimes: A Trumpian Silver Lining\n\nA Trumpian Silver Lining http://nyti.ms/2f37625")
  strzok_to_page(child_file, "2016-11-18T01:47:35-00:00", "Nope. Fixed it. Fly Tues, arr Wed. Meet Thurs and Fri. Fly back Sat. All that assuming the other side can do those dates.")
  strzok_to_page(child_file, "2016-11-18T11:18:07-00:00", "--Redacted-- Was just reading NYT. Apparently Mike Rogers has been to NY to visit Trump")
  strzok_to_page(child_file, "2016-11-18T12:40:45-00:00", "Sessions for AG")
  page_to_strzok(child_file, "2016-11-18T12:49:19-00:00", "Good god.")
  strzok_to_page(child_file, "2016-11-18T21:22:11-00:00", "Disagree with Bill on last topic")
  page_to_strzok(child_file, "2016-11-18T21:45:39-00:00", "Just hit you in lync but need to go see andy")
  strzok_to_page(child_file, "2016-11-18T21:48:17-00:00", "Ok guess I missed you. Talking with --Redacted-- and --Redacted--")

  # Page 444
  # OUTBOX == Page
  # INBOX == Strzok
  m = page_to_strzok(child_file, "2016-11-18T21:48:30-00:00", "Is Moffa there? I have a MYE q for him.")
  m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-11-18T21:49:23-00:00", "No. Don't know where he is what's the Q?")
  strzok_to_page(child_file, "2016-11-18T22:15:46-00:00", "Also, pls ask Andy for the name of the 6 woman, I didn't write it down. Thank you")
  page_to_strzok(child_file, "2016-11-18T22:43:26-00:00", "--Redacted--?")
  page_to_strzok(child_file, "2016-11-18T22:43:44-00:00", "He said just use --Redacted--")
  strzok_to_page(child_file, "2016-11-19T00:37:40-00:00", "And hey just talked to Boone have clarity on the Errant email I sent you, what --Redacted-- said to Andy, questions Andy asked Boone about it, and answers.")
  m = strzok_to_page(child_file, "2016-11-19T00:41:10-00:00", "Finally, let me know if I can imsg you a question")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2016-11-21T01:14:10-00:00", "This is really disgusting.\n\nNYTimes: White Nationalists Celebrate \u2018an Awakening\u2019s Victory\nWhite Nationalists Celebrate \u2018an Awakening\u2019 Adter Donald Trump\u2019s Victory http://nyti.ms/2fc6vve")
  strzok_to_page(child_file, "2016-11-21T01:19:38-00:00", "I'm worried racial tension is going to get really bad...")
  strzok_to_page(child_file, "2016-11-21T01:19:45-00:00", "And god that was a depressing article")
  strzok_to_page(child_file, "2016-11-21T17:24:07-00:00", "Trump spokesman declines to back FBI Director James Comey - The Washington Post\nhttps://www.washingtonpost.com/politics/trump-spokesman-declines-to-back-fbi-directory-james-comey/2016/11/21/e9cde350-afe5-11e6-8616-52b15787add0_story.html?hpid=hp_hp-cards_mhp-card-politics%3Ahomepage%2Fcard")
  strzok_to_page(child_file, "2016-11-21T23:00:25-00:00", "You gong past you old office after talking to Andy?")
  strzok_to_page(child_file, "2016-11-22T10:55:20-00:00", "I have to study up for the briefing this afternoon")
  page_to_strzok(child_file, "2016-11-22T10:56:35-00:00", "I didn't realize you guys weren't ready to give it. You should have said something.")
  strzok_to_page(child_file, "2016-11-22T10:57:47-00:00", "It's really overdue. And if Mike is briefing it, wrong, and if DI is trying to charge out and do dumb things, we need to do it.")
  page_to_strzok(child_file, "2016-11-22T10:58:26-00:00", "True.")
  page_to_strzok(child_file, "2016-11-22T11:10:42-00:00", "God, there's just so much to be wary of.\n\nNYTimes: Build He Won\u2019t\nBuild He Won\u2019t http://nyti.ms/2eWb0Pu")
  m = strzok_to_page(child_file, "2016-11-22T11:19:15-00:00", "Do you have a SATO travel account?")
  m.addnote("SATO - Scheduled Airline Ticket Office")
  page_to_strzok(child_file, "2016-11-22T11:20:10-00:00", "I need DD ofc to pay, right? That's annoying. Don't need --Redacted-- and Eric all up in my business. \U0001f612")

  # Page 445
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-22T11:21:42-00:00", "No, use CD codes. Who's your on paper supervisor?")
  page_to_strzok(child_file, "2016-11-22T11:22:13-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-22T11:22:41-00:00", "May come out of ogc, I don't know. Worse case, if it does, put down her or Baker")
  strzok_to_page(child_file, "2016-11-22T11:25:35-00:00", "Need to get you a Sato account ASAP. You can do on the phone but there's an extra block to check about why you didn't online")
  page_to_strzok(child_file, "2016-11-22T11:36:02-00:00", "It's not fair for it to come out of ogc. I guess I want dd ofc to pay. It's only fair.")
  page_to_strzok(child_file, "2016-11-22T11:36:28-00:00", "Maybe I have one. You'll have to help me figure out when I get in")
  strzok_to_page(child_file, "2016-11-22T11:38:20-00:00", "CD is the right place. It's our business and we have a comparatively big budget. I will check today.")
  page_to_strzok(child_file, "2016-11-22T12:31:33-00:00", "--Redacted-- Thats one thing THAT Is Goind To Suck ABOUT MY New office, EVERY ONE WiLL KNOW HOW Late I Get in. I stay late, so it shouldn't matter but still.")
  strzok_to_page(child_file, "2016-11-22T15:42:19-00:00", "You in yet? Want to talk briefing structure as I am befuddled.")
  page_to_strzok(child_file, "2016-11-22T15:49:10-00:00", "No. On way now.")
  m = strzok_to_page(child_file, "2016-11-22T15:51:33-00:00", "Ok. Bill is aggravating me about the D brief tomorrow. He wants me to handle the CHS and he'll do all the cases. \U0001f612")
  m.addnote("CHS - Confidential Human Source")
  page_to_strzok(child_file, "2016-11-22T15:52:43-00:00", "Well that's his perogative I guess. It represents a strange change. Has he said why?")
  m = strzok_to_page(child_file, "2016-11-22T15:55:06-00:00", "No. I assume it's to take work off my plate. He said, since Jon's not in, I'll do it. But I had been doing all of the CH when Jon was focusing on the broader election stuff. I need to talk to him.")
  m.addnote("CH - Crossfire Hurricane?")
  strzok_to_page(child_file, "2016-11-22T15:56:30-00:00", "And I gave the D a summary of all of it last week with Andy just before travel. Whatever, I'm not that worried, just think Bill is over thinking this, especially the guy who's been named")
  page_to_strzok(child_file, "2016-11-22T18:24:40-00:00", "In with andy")
  strzok_to_page(child_file, "2016-11-22T18:25:36-00:00", "Oh. You going to be out before the 2? I'm SUPER curious about JR'S 5% worry - didn't hear what he said and didn't feel it was appropriate to scream, like an old deaf man, WHAT?")
  strzok_to_page(child_file, "2016-11-23T00:35:31-00:00", "Aggravated talking with Bill about the brief tomorrow morning but that will be fine. Baker going to be there?")
  page_to_strzok(child_file, "2016-11-23T16:58:02-00:00", "Sheesh. Bill get in touch with andy?")
  strzok_to_page(child_file, "2016-11-23T16:59:08-00:00", "No, he left him a message")
  strzok_to_page(child_file, "2016-11-23T17:01:55-00:00", "Tell you what, this is going to be an interesting meeting with them in a couple of weeks")

  # Page 446
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-11-23T22:09:17-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-23T22:20:04-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-24T02:08:54-00:00", "I am reading. Started All the President's Men.")
  page_to_strzok(child_file, "2016-11-24T02:12:50-00:00", "--Redacted-- Pretty good so far. Just started, so only a few pages in. The press focus is going to be annoying, especially knowing how obnoxious and self-righteous they both turned out to be.")
  page_to_strzok(child_file, "2016-11-24T20:11:46-00:00", "Just sent you Andy's response. It makes me happy.")
  strzok_to_page(child_file, "2016-11-24T20:28:35-00:00", "That was a very nice response from Andy")
  page_to_strzok(child_file, "2016-11-24T20:32:30-00:00", "Yeah. It made me happy.")
  strzok_to_page(child_file, "2016-11-26T12:45:01-00:00", "You see Trump chose a Fox News analyst as his Dep Ntnl Security advisor?")
  page_to_strzok(child_file, "2016-11-27T19:57:13-00:00", "Maybe take an informal poll of folks tomorrow re flights/hotels.")
  strzok_to_page(child_file, "2016-11-27T19:57:57-00:00", "Yep. Meeting with Jon and --Redacted-- and --Redacted-- tomorrow to decide what to talk about, get all the paperwork going.")
  strzok_to_page(child_file, "2016-11-27T19:59:31-00:00", "At which point I'll direct everyone to take the Tuesday daytime flight :D")
  page_to_strzok(child_file, "2016-11-28T13:01:13-00:00", "--Redacted-- asked me about flight info etc., so at a minimum I expect she'll be flying with us.")
  strzok_to_page(child_file, "2016-11-28T13:06:08-00:00", "And boo. That sucks. SHould I move my seat so she can grab the one next to yours?")
  strzok_to_page(child_file, "2016-11-28T13:07:35-00:00", "And anticipate that means she will hang on Tues...all expected, I guess, was just hoping for different.\n\nJust got into work, have my standing 830")
  page_to_strzok(child_file, "2016-11-28T13:15:35-00:00", "Maybe re Tuesday. She might do touristy things though, since it's been two decades since she was there.")
  page_to_strzok(child_file, "2016-11-28T13:24:48-00:00", "--Redacted-- and jon and the rest of them should be encouraged to take another flight though.")
  strzok_to_page(child_file, "2016-11-29T01:45:21-00:00", "Hey do you know why Bill was talking to Jim?")
  strzok_to_page(child_file, "2016-11-29T01:46:45-00:00", "I'll try and find out, re Bill. A bit concerning.")
  page_to_strzok(child_file, "2016-11-29T01:48:38-00:00", "Also, jason herring spoke to me tonight about needing to get the andy letters out to congress. I need to prioritize those ASAP. Like have to be done and finalized before I can leave. \U0001f612")
  strzok_to_page(child_file, "2016-11-29T01:50:24-00:00", "Ok, well, that's motivation. I'll help, obviously")
  strzok_to_page(child_file, "2016-11-29T02:34:43-00:00", "--Redacted--")

  # Page 447
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-29T02:37:26-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-29T02:38:34-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-29T02:38:37-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-29T02:38:43-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-29T02:38:59-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-29T02:39:19-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-29T02:39:24-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-29T02:39:40-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-29T02:43:06-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-11-29T02:48:03-00:00", "--Redacted--")
  m = page_to_strzok(child_file, "2016-11-29T14:27:33-00:00", "God, the mye letters re Andy ask for SOOOOOO much information. \U0001f621\U0001f621\U0001f621")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-11-29T14:30:01-00:00", "Can we taylor what we sent, ie, give them some subset of what they're asking for?")
  page_to_strzok(child_file, "2016-11-29T14:31:03-00:00", "We're going to have to.")
  strzok_to_page(child_file, "2016-11-29T14:36:00-00:00", "Oof. Which letter(s), (or tabs in the binder)?")
  page_to_strzok(child_file, "2016-11-29T14:36:40-00:00", "14 and 15.")
  page_to_strzok(child_file, "2016-11-29T14:37:00-00:00", "I'm going to meet with Andy at 5:30 about it.")
  strzok_to_page(child_file, "2016-11-29T21:11:27-00:00", "And all good on both prep sessions tomorrow :)")
  page_to_strzok(child_file, "2016-11-29T22:51:28-00:00", "Haven't met with andy yet. He is still in with the director.")
  strzok_to_page(child_file, "2016-11-29T23:13:39-00:00", "How long you think you'll be with him? (Rough guess - 30 min? Hour and a half?)")
  page_to_strzok(child_file, "2016-11-29T23:13:58-00:00", "Probably 45 minutes at least.")
  page_to_strzok(child_file, "2016-11-30T21:59:52-00:00", "Sorry. Was in with andy.")
  strzok_to_page(child_file, "2016-12-01T01:52:01-00:00", "And I keep thinking about what the D said, what was it, sick to one's stomach? Want to talk with you about it more. And in would like to talk to Jim and Andy too. Jim may be too much a true believer though.")
  page_to_strzok(child_file, "2016-12-01T01:52:23-00:00", "Mildly nauseous, he said.")

  # Page 448
  # OUTBOX == Page
  # INBOX == Strzok
  #page_to_strzok(child_file, "2016-12-01T01:52:48-00:00", "Technically not sure you can talk to andy about it. \U0001f621")
  strzok_to_page(child_file, "2016-12-01T02:05:14-00:00", "Yeah well Jims too blindly boyscoutish and others not thoughtful so I can talk to him about his experience pre recusal. I'm not asking for decisions. I'm asking how to think about it.")
  # End of messages on this page

  # Page 449
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-11-30T12:35:55-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-11-30T12:37:43-00:00", "\U0001f636 Thanks.")
  strzok_to_page(child_file, "2016-11-30T21:25:20-00:00", "Boo. Stopped by your office before ead wrap and no Lisa... :(")
  strzok_to_page(child_file, "2016-11-30T21:25:51-00:00", "Btw, your office location sucks \U0001f615")
  page_to_strzok(child_file, "2016-11-30T21:59:52-00:00", "Sorry. Was in with andy.")
  page_to_strzok(child_file, "2016-11-30T22:00:01-00:00", "Wrap nlw.")
  # Skipped some repeats of aboce
  strzok_to_page(child_file, "2016-12-01T01:53:19-00:00", "F that I cant")
  page_to_strzok(child_file, "2016-12-01T01:53:43-00:00", "I'm just saying...")
  # A redacted version of 2016-12-01T02:05:14-00:00
  strzok_to_page(child_file, "2016-12-01T02:29:57-00:00", "Ok, vomit")
  page_to_strzok(child_file, "2016-12-01T02:30:19-00:00", "--Redacted-- Relax.")
  strzok_to_page(child_file, "2016-12-01T02:33:56-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-12-01T02:36:09-00:00", "--Redacted--")
  strzok_to_page(child_file, "2016-12-01T02:36:31-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-12-01T21:03:05-00:00", "Sorry to miss you. Had an excellent conversation with --Redacted-- though.")
  m = strzok_to_page(child_file, "2016-12-02T00:47:12-00:00", "Hi. Just leaving. Infuriating story from Bill, can tell you tomorrow or on imsg")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  m = page_to_strzok(child_file, "2016-12-02T00:48:26-00:00", "Feel free to imsg.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2016-12-02T01:06:40-00:00", "Sent there")
  strzok_to_page(child_file, "2016-12-02T10:52:14-00:00", "Weird about the clock. Thats interesting. Tells me how.much of this is messed up in your head stuff.\n\nRemind me the first 15 minutes of talking to Bill last night. Full page with list of things about head guy.")

  # Page 450
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-12-02T10:53:33-00:00", "I don't understand the second half of your text at all.")
  strzok_to_page(child_file, "2016-12-02T10:54:19-00:00", "--Redacted--")
  page_to_strzok(child_file, "2016-12-02T10:55:33-00:00", "Awesome.")
  strzok_to_page(child_file, "2016-12-02T10:55:36-00:00", "Last night, I talked with Bill before leaving. Very first thing he did was show me a page of notes, bullets, he had written about --Redacted--")
  page_to_strzok(child_file, "2016-12-02T10:58:00-00:00", "Oh jeez.")
  page_to_strzok(child_file, "2016-12-02T10:58:15-00:00", "Bill is just not getting it. \U0001f612")
  strzok_to_page(child_file, "2016-12-02T10:55:36-00:00", "I think it's he can't get over his outrage at how bad it it. I said, Bill, we're not going to get anywhere trying to prove those things. --Redacted--")
  page_to_strzok(child_file, "2016-12-02T11:03:27-00:00", "Exactly. It IS awful. But it's not something we can do something about without grave risk. Andy and I talked about this piece of it too the other day. He'll discuss today I expect.")
  strzok_to_page(child_file, "2016-12-02T19:59:43-00:00", "Bill moved wrap up to 3. Will hit you when done.")
  page_to_strzok(child_file, "2016-12-02T21:12:08-00:00", "Okay, coming back.")
  strzok_to_page(child_file, "2016-12-02T21:12:42-00:00", "Oh. Thought I was supposed to leave.")
  strzok_to_page(child_file, "2016-12-02T21:12:50-00:00", "Want me to come back?")
  strzok_to_page(child_file, "2016-12-02T21:12:50-00:00", "\U0001f60a")
  page_to_strzok(child_file, "2016-12-02T21:13:39-00:00", "Oh. Yes, that's right. I probably wasn't listening. :D")
  strzok_to_page(child_file, "2016-12-02T21:13:59-00:00", "EXACTLY")
  strzok_to_page(child_file, "2016-12-02T21:14:14-00:00", "Be right there :D")
  strzok_to_page(child_file, "2016-12-02T21:50:26-00:00", "Ok that didn't take long, I'm bored let me know when I can come up")
  page_to_strzok(child_file, "2016-12-02T21:52:34-00:00", "Ha.")
  strzok_to_page(child_file, "2016-12-02T21:55:20-00:00", "So that's a \"now\"? :D")
  page_to_strzok(child_file, "2016-12-02T21:55:37-00:00", "No.")
  strzok_to_page(child_file, "2016-12-02T22:10:09-00:00", "--Redacted-- Whatcha doing?")
  page_to_strzok(child_file, "2016-12-02T22:10:41-00:00", "Waiting for --Redacted-- to call back.")

  # Page 451
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-12-02T23:38:23-00:00", "Ho boy. This is going to stir up some sh*t\n\nNYTimes: Trump Speaks With Taiwan\u2019s Leader, a Likely Affront to China\nTrump Speaks With Taiwan\u2019s Leader, a Likely Affront to China http://nyti.ms/2gwshOM")
  page_to_strzok(child_file, "2016-12-02T23:45:14-00:00", "I know. I saw. Idiots...")
  strzok_to_page(child_file, "2016-12-10T04:19:41-00:00", "We need to talk about this in the context of the testimony last Friday. And I need to ask Jason to get a transcript if he can.\n\nNYTimes: Russia Hacked Republican Committee, U.S. Concludes\nRussia Hacked Republican Committee, U.S. Concludes http:://nyti.ms/2h5Xpoi")
  strzok_to_page(child_file, "2016-12-10T17:42:20-00:00", "Had an hour long convo with Bill. Talked about the meeting (they had it at DoJ, Bill, Jim and Jon), expressed our frustration, Bill responded.\n\nTalked about --Redacted-- and WFO SAC job, what I expected, --Redacted-- and --Redacted-- saying --Redacted-- which is fine, you know the conflicted way I feel about that but it is what it is. Mike said something super irritating to Bill, essentially, Pete briefs well but he needs more time to demonstrate his ability to manage. Bill said he thought that was just a fig leaf for saying --Redactedd-- about it aggravates me. I'm sorry, I'm not briefing what someone tells me, I'm briefing what I'm doing. And I'm managing (for the case) a ton of people in various divisions and multiple agencies and foreign governments. Not to mention the issues I've briefed you on and am managing for cd3, etc.\n\nI do think it's a fig leaf, but have the balls to say, Pete, you're doing a great job. Keep it up. Youve just gotten promoted, twice, and we need you as DAD where you can do good: embrace that role. DON'T tell me, you brief well but you need to show me some more management skill. F you. I manage my ass off every goddamn day in thie sh*tshorm, and keep the branch running to boot." )
  strzok_to_page(child_file, "2016-12-10T17:42:27-00:00", "Lots more to discuss.")
  page_to_strzok(child_file, "2016-12-10T17:46:16-00:00", "That is 100% a fig leaf. And more than a fig leaf, it's a reflection of --Redacted-- insecurity and arrogant overconfidence. Don't give it a second more thought. I mean it.")
  page_to_strzok(child_file, "2016-12-10T17:47:06-00:00", "Was Bill's reponse re meeting adequate?")
  strzok_to_page(child_file, "2016-12-10T17:50:00-00:00", "But how much does his saying that translate to the other EADs? --Redacted-- out the door, as is --Redacted-- but I don't want --Redacted-- poisoned by it. Think I'm good with --Redacted-- and --Redacted-- just with more time.")
  strzok_to_page(child_file, "2016-12-10T17:51:48-00:00", "It was OK. I told him we heard via --Redacted--/--Redacted-- and that we were all disappointed. he said he understood, but he was able to talk that way broadly without giving any specifics, so he thinks it helped rather than hurt. Said we hadn't closed anything, and generally talked about our path forward. Said they didn't ask for an update when we got back, and that he thought we were in a good place.")

  # Page 452
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-12-10T17:51:55-00:00", "It won't. Andy's views on the matter will carry a lot more weight than Mike saying something on his way out the door.")
  strzok_to_page(child_file, "2016-12-10T17:53:46-00:00", "And I appreciate you saying don't give it a second thought, but it burns me. Bill did say my reputation with the D and DD is solid, which is fine. But the fact of the matter is the D doesn't sit on the board, and Andy is much happier going with the boards recommendation. So I need to not let this view become the common wisdom/stock answer on the zero corridor.")
  page_to_strzok(child_file, "2016-12-10T17:54:33-00:00", "The D reviews every one of the decisions of the Board. And if he disagrees, pushes back.")
  strzok_to_page(child_file, "2016-12-10T17:56:18-00:00", "I know, but I told Bill really needed him to determine whether or not I should even put in, and the message it sends either way. He said he would talk to Andy this week.")
  page_to_strzok(child_file, "2016-12-10T17:56:40-00:00", "It won't. Stop worrying. Trust me.\n\nIf you had more time as DAD under your belt, do you actually think --Redacted-- would even stand a chance because of some bs claim that you need more proven leadership? Because that happened when you both were up for DAD? Come on. It's face-saving for --Redacted-- pure and simple.")
  page_to_strzok(child_file, "2016-12-10T17:57:16-00:00", "The answer is no, Pete. 100% no. Andy will say the same.")
  strzok_to_page(child_file, "2016-12-10T17:58:14-00:00", "In other news, he said OCA is posted and Andy looking to take care of --Redacted-- Thus came up in the context of bill asking about a term for --Redacted-- who deserves it, and Bill was told no. I assume that would be a different answer for --Redacted-- So I need to talk to --Redacted-- to see if he'd be interested in an SC job in CD, because he'd be better than 95% of the candidates we have putting in. Even though we can't get a term for --Redacted-- All this irks me. Let's just be open and honest. \U0001f612")
  page_to_strzok(child_file, "2016-12-10T17:58:54-00:00", "It's not good for you or Bill to have to ask Andy this. Please. Just go to Bill and tel him no. You need to trust me on this.")
  page_to_strzok(child_file, "2016-12-10T17:59:17-00:00", "I believe --Redacted-- is interested.")
  m = strzok_to_page(child_file, "2016-12-10T17:59:44-00:00", "Good, but then let Andy clearly tell Bill that and it will be fine. I'll work hard, and in 12 months when I've been DAD enough time and there's nothing at WFO, we'll figure out what to do.")
  m.addnote("WFO - Washington Field Office")
  page_to_strzok(child_file, "2016-12-10T18:00:41-00:00", "Why do you need to make andy tell Bill? I'm telling you, it's to neither of your advantage to ask him. Bill should be able to figure this out on his own.")
  m = strzok_to_page(child_file, "2016-12-10T18:01:10-00:00", "Ok fine I will (re telling Bill). I can suggest he not tell Andy, but I kind of WOULD like him to ask, OK, Pete wants to stay and work hard as DAD, what do you see him doing August when he's now been a CD SESer for a year and a half?")
  m.addnote("SES - Senior Executive Service")
  page_to_strzok(child_file, "2016-12-10T18:01:52-00:00", "And it won't be a term for --Redacted-- It will be a permanent SC, I suspect, but he will just have to sign a promise to not try to go be as sac. So be smart about where you place him, because he'll probably stay there the rest of his career.")

  # Page 453
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-12-10T18:02:51-00:00", "I think --Redacted--'s interested, too, based on convos we've had. I don't know whether to put him in 4 or 2. Don't think he has the CI background for 3.")
  strzok_to_page(child_file, "2016-12-10T18:03:13-00:00", "--Redacted-- problem is he's never even been an SSA.")
  m = strzok_to_page(child_file, "2016-12-10T18:03:39-00:00", "People obviously understand he's now been both dgc and ad of oca, but stuff like that matters.")
  m.addnote( "OCA - Office of Congressional Affairs")
  page_to_strzok(child_file, "2016-12-10T18:03:59-00:00", "That's a different conversation, and one he can have not in this context. Or even better, one YOU should have with Andy. It would be more meaningful that way anyway. \"Andy, I'm not putting in for sac, but where do you see me... Especially since I heard criticism of me from Mike which I didn't think was fair, wanted to make sure you didn't think that was widely thought...\"\n\n2.")
  strzok_to_page(child_file, "2016-12-10T18:04:07-00:00", "Most importantly, as far as I'm concerned, he's a good guy and I would trust him as a SC.")
  page_to_strzok(child_file, "2016-12-10T18:04:16-00:00", "It does. That's why he won't be allowed to advance.")
  strzok_to_page(child_file, "2016-12-10T18:05:54-00:00", "I didn't tell you the grown up convo I had to have with --Redacted-- in London, when he asked and got angry at why I was likely not to be the next SAC, and had to be the calm measured professional explaining all the reasons why not.")
  page_to_strzok(child_file, "2016-12-10T18:07:14-00:00", "--Redacted-- got angry? Understandable, but I'm proud of you for explaining it. I hope you truly believe it as well.")
  strzok_to_page(child_file, "2016-12-10T18:08:53-00:00", "Yes he did. You know how I fell. I believe it, just as I believe had I not applied for or applied for and not gotten the DAD job, that I would have a great shot at it. And that I believe I'm the best person for both jobs, and ultimately, the best to be Bill's successor in CD.")
  page_to_strzok(child_file, "2016-12-10T18:10:19-00:00", "All of that is correct. You just can't move having been DAD for three months. If you had stayed SC, you would be SAC. And you will be AD too.")
  strzok_to_page(child_file, "2016-12-10T18:11:52-00:00", "If I stay long enough or am willing to move, for sure. But neither of those are necessarily true. But nothing I can do but work hard and answer whatever decision is in front of me.")
  page_to_strzok(child_file, "2016-12-10T18:14:42-00:00", "That's the right attitude. I just hope you believe it in your heart of hearts.")
  strzok_to_page(child_file, "2016-12-10T18:16:40-00:00", "You know im conflicted! To show my muddle, think of it this alternative way: I've now been back at HQ for 16 months. Had John G not been gone all the time and the board gone earlier, I would have been an SESer for over a year now. Woulda coulda shoulda, I know.\n\nHow long was Jason acting?")
  page_to_strzok(child_file, "2016-12-10T18:18:04-00:00", "Acting AD? Since August, I think.")
  page_to_strzok(child_file, "2016-12-10T18:18:45-00:00", "Back at HQ doesn't count. You were still an asac, on detail.")

  # Page 454
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-12-10T18:20:03-00:00", "Even an SESer over a year doesn't change three month as DAD. It's not long enough in your current role. And christ, you're NEED in this role. Way more than you'd need to be as SAC. Just relax, --Redacted-- It will come. I promise you.")
  strzok_to_page(child_file, "2016-12-10T18:20:54-00:00", "I'm not needed. I need to show I can effectively manage. \U0001f612")
  strzok_to_page(child_file, "2016-12-10T18:21:11-00:00", "Wish --Redacted-- wouldn't have said anything about that, or called --Redacted-- BS")
  strzok_to_page(child_file, "2016-12-10T18:21:37-00:00", "Cause this is going to sit in the back of my head like a festering pile of crap.")
  page_to_strzok(child_file, "2016-12-10T18:22:12-00:00", "Peter. In the immortal words of Jim Baker/Taylor Swift: Haters gonna hate...shake it off, shake it off. \U0001f60a")
  page_to_strzok(child_file, "2016-12-10T18:22:25-00:00", "Don't let it. Do you respect --Redacted--")
  strzok_to_page(child_file, "2016-12-10T18:24:31-00:00", "And how did that guidance work for you?\n\nEnough. I thought at least we had a decent relationship he would say that sort of BS. I get his faults, but still. Just say the truth.")
  page_to_strzok(child_file, "2016-12-10T18:27:32-00:00", "He's too arrogant. He can't see the truth.")
  strzok_to_page(child_file, "2016-12-10T18:29:45-00:00", "I haven't worked closely with him enough to see that")
  strzok_to_page(child_file, "2016-12-10T18:30:10-00:00", "And maybe vaguely related, man I'm angry the way --Redacted-- worked out. That article is horrible.")
  page_to_strzok(child_file, "2016-12-10T18:47:30-00:00", "Oh please. I'm calling BS on you respect him. I don't. What non-critical thing have you ever had to say about him?\n\nAnd yes, probably related. \U0001f612")
  strzok_to_page(child_file, "2016-12-10T19:15:56-00:00", "A) I think he does a decent job advocating for CD in front of audiences like the SAC conference.")
  page_to_strzok(child_file, "2016-12-10T19:16:26-00:00", "Okay, great. Mad props to him then. \U0001f612")
  strzok_to_page(child_file, "2016-12-10T19:17:45-00:00", "A) fine. Look, I'm obviously cranky/stung/demotivated by it.")
  strzok_to_page(child_file, "2016-12-10T22:04:18-00:00", "Just talked with Jon for an hour.")
  strzok_to_page(child_file, "2016-12-10T22:06:03-00:00", "Back to being a little cranky with Bill about the meeting. Jon asked Bill on Thurs if it was still on. Bill told him to talk to him Fri AM. Jon said JB was really good at the mtg, kept saying, we don't know or we're not going to discuss that. He's obviously as worried as he was.")
  strzok_to_page(child_file, "2016-12-10T22:06:28-00:00", "Plus remind me stories of iod f'ing up visit with Andy and --Redacted--")
  page_to_strzok(child_file, "2016-12-10T22:17:34-00:00", "I can talk if you want. Have 10 minutes or so.")
  strzok_to_page(child_file, "2016-12-10T22:23:14-00:00", "I can't. Check email.")
  strzok_to_page(child_file, "2016-12-10T22:23:27-00:00", "Though I desperately want to \U0001f636")
  page_to_strzok(child_file, "2016-12-10T22:25:46-00:00", "Yeah, I saw.")
  strzok_to_page(child_file, "2016-12-10T22:29:17-00:00", "Bill told Mike...")

  # Page 455
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2016-12-10T22:29:51-00:00", "Npr just reported that that ExxonMobil guy possibly nominated for state has close ties to putin.")
  strzok_to_page(child_file, "2016-12-10T22:37:12-00:00", "Oh yeah! He got an Award of Friendship directly from Putin!")
  page_to_strzok(child_file, "2016-12-10T22:38:17-00:00", "Interesting choice for Sec State then.")
  strzok_to_page(child_file, "2016-12-10T22:39:47-00:00", "Yep! He's 64, and has spent 41 of them at Exxon. Started as a production engineer, and rose to do oil and gas deals around the world. Statecraft.")
  #page_to_strzok(child_file, "2016-12-11T01:10:13-00:00", "Great. This sentence aggravated the s out of me.\nTrump has threatened a lot of people and he\u1029s about to be in control of the most pervasive and least accountable surveillance infrastructure in the world,\u201d Mr. Marlinspike said.\u201cA lot of people are justifiably concerned about that.\u201d\n\nNYTimes: Worried About the Privacy of Your Messages? Download Signal\nWorried About the Privacy of Your Messages? Download Signal http:://nyti.ms/2hjyVVo")
  #strzok_to_page(child_file, "2016-12-11T01:28:18-00:00", "Yeah, me too. Don't know who or where to support....")
  strzok_to_page(child_file, "2016-12-12T11:36:37-00:00", "God.\n\nIn separately irritating news,JB apparently offered to meet with David Kendall and his secretary set it up. None of us, including --Redacted-- heard anything about it until --Redacted-- mentioned it to us.")
  strzok_to_page(child_file, "2016-12-12T11:37:18-00:00", "Possibly today. Possibly about return of evidence. Possibly he'll take --Redacted-- along. Possibly he'll want to do some prep. None of us really know. \U0001f612")
  strzok_to_page(child_file, "2016-12-12T11:37:35-00:00", "Maybe it came up at the Fri meeting none of us attended.")
  page_to_strzok(child_file, "2016-12-12T11:41:37-00:00", "Then somebody whose name is not Lisa Page needs to tell him that it is insulting to have to learn about important meetings from DOJ.")
  strzok_to_page(child_file, "2016-12-12T11:43:14-00:00", "I will. I don't think --Redacted-- can in the same way.")
  strzok_to_page(child_file, "2016-12-12T11:43:41-00:00", "After I find out if Bill and/or Jon knew")
  strzok_to_page(child_file, "2016-12-12T11:44:00-00:00", "Though neither mentioned.")
  strzok_to_page(child_file, "2016-12-12T20:32:25-00:00", "I talked to Bill about the CyD matter we discussed, he said Andy is aware.\n\nThank you for stepping out to grab the lifesavers.")
  strzok_to_page(child_file, "2016-12-13T19:57:40-00:00", "What floor is jcc?")
  page_to_strzok(child_file, "2016-12-13T19:58:44-00:00", "6 or 7. On the 9th Street side.")
  strzok_to_page(child_file, "2016-12-13T19:59:15-00:00", "Oh. Thought it was 10th...you sure?")
  page_to_strzok(child_file, "2016-12-13T20:30:29-00:00", "Sorry. Was on with the intercept. Yeah, Mike just mentioned. Something sanctioned, obviously. God, I hate the intercept.")

  # Page 456
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-12-13T20:57:46-00:00", "Coffee/tea?\n\nStories for you.....")
  strzok_to_page(child_file, "2016-12-13T21:03:21-00:00", "Let me know when you're done, want to hear about it, obviously")
  strzok_to_page(child_file, "2016-12-13T21:36:50-00:00", "Need to talk to you before wrap")
  strzok_to_page(child_file, "2016-12-13T22:31:53-00:00", "Who is --Redacted--?")
  page_to_strzok(child_file, "2016-12-13T22:34:06-00:00", "No idea.")
  strzok_to_page(child_file, "2016-12-13T22:34:33-00:00", "These texts are quite the.....")
  page_to_strzok(child_file, "2016-12-13T22:35:24-00:00", "You're killing me.")
  strzok_to_page(child_file, "2016-12-13T22:36:01-00:00", "Text from reporter: retrieving my password for skype. I forgot it.\n\nText from reporter and hour and 31 minutes later: thanks man. Awesome as usual")
  page_to_strzok(child_file, "2016-12-13T22:36:26-00:00", "Jesus.")
  strzok_to_page(child_file, "2016-12-13T22:37:23-00:00", "And Oh. I'm literally on the 5th line of a 2417 line spreadsheet.")
  page_to_strzok(child_file, "2016-12-13T22:42:07-00:00", "I'm calling now.")
  page_to_strzok(child_file, "2016-12-13T22:43:28-00:00", "Wtf, where'd you go?")
  strzok_to_page(child_file, "2016-12-13T22:44:38-00:00", "In with Bill and dads")
  page_to_strzok(child_file, "2016-12-13T22:45:00-00:00", "Aaarggh.")
  page_to_strzok(child_file, "2016-12-13T22:54:05-00:00", "I'm going to try to leave as soon as I get 5 minutes with andy. The d had wrap.")
  page_to_strzok(child_file, "2016-12-13T22:55:03-00:00", "Jm said that the D asked Dd about the phone records pull today. So I am going to mention it, but no details.")
  strzok_to_page(child_file, "2016-12-13T22:55:12-00:00", "K. Bill is rambling. I'll let you know when done")
  strzok_to_page(child_file, "2016-12-13T23:17:22-00:00", "Hi. You in with him?")
  page_to_strzok(child_file, "2016-12-13T23:18:17-00:00", "Still waiting for him to get out. \U0001f621")
  m = strzok_to_page(child_file, "2016-12-13T23:21:14-00:00", "Talked with Doj about HA interview. Told them we had to interview, no immunity. They said they thought that would get counsel to the point of saying she's either taking the 5th in the Gj or you need to give her immunity. I said that's fine, please have discussions to get the decision to that point and I would run up the chain.")
  m.addnote("HA - Huma Abedin, Gj - Grand Jury")
  page_to_strzok(child_file, "2016-12-13T23:21:50-00:00", "Do I need to bring up to andy at some point?")
  strzok_to_page(child_file, "2016-12-13T23:22:03-00:00", "I said Bill would be better, but that I needed to run past Bill to see what he says")

  # Page 457
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2016-12-13T23:22:15-00:00", "Is he recused? (\U0001f621\U0001f621)")
  page_to_strzok(child_file, "2016-12-13T23:22:18-00:00", "Oh yeah. I forgot. \U0001f621\U0001f612")
  m = page_to_strzok(child_file, "2016-12-13T23:22:39-00:00", "Yes! All mye matters.")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  strzok_to_page(child_file, "2016-12-13T23:22:47-00:00", "Double \U0001f621\U0001f612\U0001f621\U0001f612")
  strzok_to_page(child_file, "2016-12-13T23:22:50-00:00", "I know.")
  strzok_to_page(child_file, "2016-12-13T23:23:11-00:00", "I'm just angry about it.")
  page_to_strzok(child_file, "2016-12-13T23:23:17-00:00", "Me too.")
  strzok_to_page(child_file, "2016-12-13T23:23:27-00:00", "I fell into the same, what in the hell are you talking about Mike as POC mental trap \U0001f621")
  strzok_to_page(child_file, "2016-12-13T23:24:22-00:00", "Literally wondered if Andy had finally decided to delegate down management of George")
  strzok_to_page(child_file, "2016-12-13T23:24:25-00:00", "I kinda want to print these logs out and take them home :D")
  page_to_strzok(child_file, "2016-12-13T23:24:58-00:00", "No kidding. Will figure out a day to work late.")
  #m = strzok_to_page(child_file, "2016-12-13T23:25:31-00:00", "Ok, I need to go back in with Bill. Jen and Dina still there. Call me later....particularly interested if D gave a fuller description of his convo with Brennan")
  #m.addnote("Brennan probably told Director Comey about Steele dossier, this was about when Brennan told DNI Clapper")
  strzok_to_page(child_file, "2016-12-14T00:01:58-00:00", "Shocker, problems in ny. --Redacted--")
  # HUGE GAP IN MESSAGES! They skip aheas to May 18th! That's 155 days (5 months, 4 days)
  strzok_to_page(child_file, "2017-05-18T18:58:07-00:00", "If you get done and have Bill and Jon for a dump about last eve, please cal me....")
  page_to_strzok(child_file, "2017-05-18T22:56:59-00:00", "Sorry one sec.")
  strzok_to_page(child_file, "2017-05-18T23:08:21-00:00", "K. Talking with Bill about you, actually")
  page_to_strzok(child_file, "2017-05-18T23:08:39-00:00", "Hmmm.")
  strzok_to_page(child_file, "2017-05-18T23:09:59-00:00", "Just called your desk")
  page_to_strzok(child_file, "2017-05-18T23:13:06-00:00", "Was talking to bill. He is calling me back when he is done with you.")
  strzok_to_page(child_file, "2017-05-18T23:29:13-00:00", "Let me know what he says. I was surprised how hard he pushed me to think about it. The strength of my reaction to that is kinda confirming to me I don't want to.")
  # strzok_to_page(child_file, "2017-05-18T23:41:18-00:00", "Oh god Susan Collis comments on npr....")
  page_to_strzok(child_file, "2017-05-19T00:08:40-00:00", "--Redacted-- said absolutely no question I have to be on the team. I'm so confused right now...")
  strzok_to_page(child_file, "2017-05-19T00:11:23-00:00", "Really?!?!")
  strzok_to_page(child_file, "2017-05-19T00:11:29-00:00", "As in, with her?")

  # Page 458
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-05-19T00:11:58-00:00", "And that's what I wanted to talk about!!!!\n\nMy answer is no way, sac then AD and lead the Division")
  strzok_to_page(child_file, "2017-05-19T00:12:09-00:00", "And then I think..")
  strzok_to_page(child_file, "2017-05-19T00:13:43-00:00", "A case which will be in the history books. A chapter - much like you tell me about my extra time in the field and all the cases (\"would you trade it\"?).\n\nA million people sit in AD and staff jobs. This is a chance to DO. In maybe the most important case of our lives.")
  strzok_to_page(child_file, "2017-05-19T00:13:54-00:00", "What did Andy say about --Redacted-- going?")
  page_to_strzok(child_file, "2017-05-19T00:19:05-00:00", "No way dude. I really don't think you should do it..")
  strzok_to_page(child_file, "2017-05-19T00:19:17-00:00", "You would obviously excel on the team.\n\nIn a thousand ways they need someone EXACTLY like you")
  page_to_strzok(child_file, "2017-05-19T00:19:43-00:00", "I don't really know what she meant when she said on the team. Full time, part time, I got home so our convo was cut short.")
  page_to_strzok(child_file, "2017-05-19T00:22:03-00:00", "Why? I don't understand what they need me for! Not when they have someone like Aaron. Or --Redacted-- or --Redacted--")
  page_to_strzok(child_file, "2017-05-19T00:22:49-00:00", "And --Redacted-- paid some really outrageous complements to me. I just don't get what she even means.")
  strzok_to_page(child_file, "2017-05-19T00:14:26-00:00", "Ok I obviously want to hear what --Redacted-- said")
  page_to_strzok(child_file, "2017-05-19T00:25:28-00:00", "I won't be able to repeat. Something about being the second smartest lawyer she has ever worked with besides comey. It can't be true.")
  page_to_strzok(child_file, "2017-05-19T00:26:41-00:00", "And how I lean in and have a stronger work ethic than anyone she knows. And more but I don't remember.")
  strzok_to_page(child_file, "2017-05-19T00:29:27-00:00", "You're in an entirely different class than --Redacted-- or --Redacted--")
  strzok_to_page(child_file, "2017-05-19T00:30:08-00:00", "You see the future. You assimilate and combine things in am uncanny way.")
  strzok_to_page(child_file, "2017-05-19T00:32:35-00:00", "And re your attorney image of yourself, that's because you equate brilliant lawyer with --Redacted-- or Trisha sitting in a room writing something as a clerk.\n\nREAL law is the application in a complex, dynamic environment. And you're astoundingly good at that")
  strzok_to_page(child_file, "2017-05-19T00:32:54-00:00", "Plus you have passion and curiosity, which is more than half of the battle anyway")
  page_to_strzok(child_file, "2017-05-19T00:33:34-00:00", "I am so not in a different class from --Redacted-- and --Redacted-- That is crazy.")
  strzok_to_page(child_file, "2017-05-19T00:35:40-00:00", "They don't get the big picture like you do --Redacted-- is operationally amazing. But scaling law up rapidly and with agility is something that makes you special. THAT'S the mark of a brilliant mind.")
  #m = strzok_to_page(child_file, "2017-05-19T00:36:15-00:00", "For me, and this case, I personally have a sense of unfinished business.\n\nI unleashed it with MYE. Now i need to fix it and finish it")
  #m.addnote("MYE - Midyear Exam (Hillary Clinton)")
  #page_to_strzok(child_file, "2017-05-19T00:37:23-00:00", "What does that even mean, scaling up?")

  # Page 459
  # OUTBOX == Page
  # INBOX == Strzok
  #page_to_strzok(child_file, "2017-05-19T00:37:51-00:00", "You shouldn't take this on. I promise you, I would tell you if you should.")
  strzok_to_page(child_file, "2017-05-19T00:39:44-00:00", "It means you can see a small point of law and know it, rapidly understand the strategic importance of it not just on that issue but intuitively get the value or role of it in a much broader context.\n\nYou're not constrained to an issue. Your mind rapidly makes valid and important connections and associations in a way most people don't. Can't.")
  #strzok_to_page(child_file, "2017-05-19T00:39:47-00:00", "Why not, re me?")
  # Page 34 has unredacted version of this message
  #strzok_to_page(child_file, "2017-05-19T00:40:50-00:00", "Who gives a f*ck, one more AD like --Redacted-- or whoever.\n\nAn investigation leading to impeachment?")
  strzok_to_page(child_file, "2017-05-19T00:41:45-00:00", "And with D gone, and Andy leaving, all these --Redacted--\n\nWho says I get another promotion from DAD?!?")
  page_to_strzok(child_file, "2017-05-19T00:45:57-00:00", "We should stop having this conversation here. Just tell bill you need another day and we can discuss tomorrow.")
  page_to_strzok(child_file, "2017-05-19T00:47:33-00:00", "And certainly, that would certainly impact my thinking too. We can't work closely on another case again, though obviously, I want you to do what is right for you.")
  strzok_to_page(child_file, "2017-05-19T00:54:23-00:00", "A) ok. Though now I'm curious.\n\nB) sigh. Yeah I suppose that's right. But god we're a good team. \U0001f636\U0001f614 Is that playing into yur decision/your advice to me?")
  strzok_to_page(child_file, "2017-05-19T00:54:34-00:00", "Chaffetz stepping down June 30....")
  page_to_strzok(child_file, "2017-05-19T00:55:13-00:00", "No. Not at all. I just think we are both ready for a change. Truly.")
  page_to_strzok(child_file, "2017-05-19T00:55:59-00:00", "A) is just about the different realistic outcomes of this case.")
  strzok_to_page(child_file, "2017-05-19T00:56:37-00:00", "B) that's definitely true. I want/need you to give me your old resume.\n\nC) I think I'll wait and see what happens with sac wfo. I'm not expecting to get it, I just want to see what I feel like after the decision.")
  strzok_to_page(child_file, "2017-05-19T00:57:39-00:00", "A) you and I both know the odds are nothing. If I thought it was likely, I'd be there no question. I hesitate in part because of my gut sense and concern there's no big there there.")
  page_to_strzok(child_file, "2017-05-19T00:58:32-00:00", "A) Pete. Let's talk about this tomorrow. \U0001f621")
  strzok_to_page(child_file, "2017-05-19T00:58:59-00:00", "Regardless of the outcome, I think there's a certain savvy business decision for you to do it \n\n600k/year + doing white hat corporate investigations isn't a bad exit strategy.")
  page_to_strzok(child_file, "2017-05-19T00:59:12-00:00", "C) Is that going tomorrow?")
  strzok_to_page(child_file, "2017-05-19T00:59:52-00:00", "A) fine! Didn't think I said anything wrong. But fine.\nC) yep. Is Andy going to the board?")
  strzok_to_page(child_file, "2017-05-19T01:00:40-00:00", "C) I suppose he can't. He has to sign as D so I don't know if that means he can't chair the board.")

  # Page 460
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-05-19T01:00:46-00:00", "Don't know.")
  page_to_strzok(child_file, "2017-05-19T01:01:06-00:00", "Have to go eat. Talk to you tomorrow.")
  strzok_to_page(child_file, "2017-05-19T01:01:30-00:00", "K. Bye, Lisa. Hope some sleep brings clarity.")
  strzok_to_page(child_file, "2017-05-19T02:15:28-00:00", "If I don't go, does that make your decision easier?")
  page_to_strzok(child_file, "2017-05-19T02:17:18-00:00", "Nope.")
  strzok_to_page(child_file, "2017-05-19T02:20:20-00:00", "I'm struggling")
  page_to_strzok(child_file, "2017-05-19T02:23:22-00:00", "I honestly think the break will be rejuvenating.")
  page_to_strzok(child_file, "2017-05-19T02:24:46-00:00", "Want to talk to Andy? Be honest that you're worried about your future with D and him gone? Be honest that if you don't get AD, you'd rather just finish out your career doing work you love?")
  strzok_to_page(child_file, "2017-05-19T02:33:23-00:00", "Maybe. But I don't want to before the board.\n\nI just want to make a difference. To have counted for something, to be in the game, down by one.\n\nWhy such a desire to prove myself?")
  strzok_to_page(child_file, "2017-05-19T03:16:04-00:00", "And I know you deal with it with me all the time, so you're inured, in a different spot...but it was wrong, injust, even - for me to not be there today.\n\nYou may not get it.\n\nJon does.\n\nWhat was --Redacted-- thinking? WHere was that in talking to his boss?\n\nDid you care once you got an invite? (be brutally honest no you didn't)\n\nAnd that may make my decision.")
  strzok_to_page(child_file, "2017-05-19T03:28:55-00:00", "I deserved a chance to see these people, to see if I wanted to go with them")
  strzok_to_page(child_file, "2017-05-19T09:42:32-00:00", "4:45 and still no better answer. Just trying to get the angry/cranky/whiny out of my thinking. I need to objectively see the issue and set it, sterile, on a shelf. Sorry about my second to last text last night.")
  page_to_strzok(child_file, "2017-05-19T10:07:08-00:00", "I get that you should have been there! Geez Pete.")
  strzok_to_page(child_file, "2017-05-19T10:18:02-00:00", "I know! I was grumpiness.\n\nAnd I figured out what's behind that (which we said yesterday), but been thinking in terms of how that impacts my decision. Not for here, though.\n\nYou seel at all?")
  strzok_to_page(child_file, "2017-05-19T10:26:58-00:00", "You wake up with a better sense of what you want to do?")
  page_to_strzok(child_file, "2017-05-19T10:41:08-00:00", "No. I'm just going to have to feel it out. Probably talk to --Redacted-- more.")
  page_to_strzok(child_file, "2017-05-19T10:41:30-00:00", "I'll be in the car at 710 bc I have to meet --Redacted-- if you want to talk.")
  strzok_to_page(child_file, "2017-05-19T10:43:28-00:00", "I do. Ok let me hustle.")
  strzok_to_page(child_file, "2017-05-19T17:31:37-00:00", "So did --Redacted-- convince you? ;)")

  # Page 461
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-05-19T17:40:13-00:00", "Remind me --Redacted--")
  strzok_to_page(child_file, "2017-05-19T23:39:47-00:00", "What about --Redacted-- for the project?")
  page_to_strzok(child_file, "2017-05-19T23:42:10-00:00", "Will explain why later. He thinks --Redacted--")
  strzok_to_page(child_file, "2017-05-19T23:42:10-00:00", "Bill threw out --Redacted-- I was real excited.")
  page_to_strzok(child_file, "2017-05-19T23:44:16-00:00", "Nope. Me neither. No strategic thinking.")
  strzok_to_page(child_file, "2017-05-19T23:44:18-00:00", "Well that's just dumb. He heard Director Comey's statement about what we're trying to achieve, right?\n\nAnyway. Try to not swell on all this.\n\nGetting stuff ready to go out the door...\n\n--Redacted-- \U0001f60a")
  page_to_strzok(child_file, "2017-05-19T23:47:39-00:00", "--Redacted-- said, immediately, that sounds like an offer you must accept. He wants me to.")
  strzok_to_page(child_file, "2017-05-19T23:48:29-00:00", "That's really good! Im glad. That from him must be a relief for you, right?")
  strzok_to_page(child_file, "2017-05-19T23:48:45-00:00", "I REALLY like your 30 day idea.")
  page_to_strzok(child_file, "2017-05-19T23:49:08-00:00", "I guess. --Redacted--")
  strzok_to_page(child_file, "2017-05-19T23:49:13-00:00", "America needs you, Lis. \U0001f60a")
  strzok_to_page(child_file, "2017-05-20T01:46:15-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-05-20T10:04:37-00:00", "Hi. How are you feeling about things?\n\n--Redacted-- \U0001f612")
  strzok_to_page(child_file, "2017-05-21T13:16:13-00:00", "You don't have to move your office (I mean, obviously you'll be working out of the SC space) do you? At least you can put that decision off for a while?\n\nYou feeling any different about it this morning?")
  page_to_strzok(child_file, "2017-05-21T13:26:13-00:00", "No, I just need to figure out what I need to hand off, clean up a little.")
  page_to_strzok(child_file, "2017-05-21T13:27:36-00:00", "No, I'm still really stressed out. I feel like an imposter. There's no way I can live up to their expectations.")
  strzok_to_page(child_file, "2017-05-21T13:49:30-00:00", "Lis. You're gonna be great. Of all the things to worry about, your competence isn't one of then. Promise.")
  page_to_strzok(child_file, "2017-05-21T13:52:05-00:00", "But I'm not a real lawyer anymore! They have no idea. \U0001f615")
  strzok_to_page(child_file, "2017-05-21T13:58:08-00:00", "You have government savvy. And know the Bu. And IC. You're going to be great. \U0001f60a")
  strzok_to_page(child_file, "2017-05-21T14:09:52-00:00", "Did Aaron say they want you primarily for criminal prosecutor stuff, or is that you worrying?")
  page_to_strzok(child_file, "2017-05-21T14:10:41-00:00", "Me worrying. But I have the same job that they do so I mean I feel like it is founded.")
  page_to_strzok(child_file, "2017-05-21T14:17:33-00:00", "Driving to work. In business wear. Because Mueller. \U0001f610")
  strzok_to_page(child_file, "2017-05-21T14:38:08-00:00", "Oh lord. You meeting them?")

  # Page 462
  # OUTBOX == Page
  # INBOX == Strzok
  m = strzok_to_page(child_file, "2017-05-21T15:22:30-00:00", "And Lisa. Aaron's time as an AUSA was about equivalent to your OCRS time.\n\nYou bring law and knowledge they can hope to get. It will be fine. I promise. You'll be am integral part of the team before the end of the month. Promise promise promise. You're a rock star. \U0001f60a")
  m.addnote("AUSA - Assistant US Attorney, OCRS - Department of Justice Organized Crime and Racketeering Section")
  page_to_strzok(child_file, "2017-05-21T15:47:56-00:00", "Man, I'm frustrated re Andy and Carl. That may be the hardest thing moving forward. Will be at the ofc for hours if you free up to chat.")
  page_to_strzok(child_file, "2017-05-21T15:48:21-00:00", "Aaron did a LOT more in that time than I did.")
  strzok_to_page(child_file, "2017-05-21T15:50:38-00:00", "I would be too. You shul talk with Andy about it, even of its some time from now. But part of me really thinks should should before --Redacted--\n\nOk --Redacted-- I'll try and leave a little early, maybe 1220 or so.\n\nAaron did different. You're going to be solid. I'm telling you, Lisa. It's normal and appropriate to feel not on par (I'd worry if you didn't), but you're going to be spectacular.")
  strzok_to_page(child_file, "2017-05-21T15:53:12-00:00", "Actually I may be able to call in a couple, standby")
  strzok_to_page(child_file, "2017-05-21T16:36:38-00:00", "Hey parking --Redacted-- should be free after 130-140 or so, I'll call then if you can talk.")
  page_to_strzok(child_file, "2017-05-21T17:10:26-00:00", "Had excellent convo with Andy. Let me know when you are done.")
  strzok_to_page(child_file, "2017-05-21T17:31:31-00:00", "Done. Just tried calling your desk.")
  page_to_strzok(child_file, "2017-05-21T17:37:36-00:00", "Grabbing food. One sec.")
  strzok_to_page(child_file, "2017-05-21T17:39:25-00:00", "K. Heading home (10 out), though I can plan a work call later on. --Redacted--")
  page_to_strzok(child_file, "2017-05-21T18:15:56-00:00", "I told Aaron let's see how this might goes, then decide whether it makes sense for Bob to talk to andy.")
  strzok_to_page(child_file, "2017-05-21T18:16:32-00:00", "Might = week?")
  strzok_to_page(child_file, "2017-05-21T18:17:04-00:00", "I think that's smart.")
  page_to_strzok(child_file, "2017-05-21T18:18:28-00:00", "Sorry mtg. Was an autocoreect.")
  page_to_strzok(child_file, "2017-05-21T18:18:47-00:00", "Except even the new phone can't correct autocorrect.")
  strzok_to_page(child_file, "2017-05-21T18:20:46-00:00", "Mtg is one you're having tomorrow? Regardless, yes, meet with the team and get a sense if you all feel comfortable if you're on the right path.\n\nYeah these suck *ss. Of course it's the entire brand. --Redacted-- died as well.")
  page_to_strzok(child_file, "2017-05-21T18:26:50-00:00", "I'm not in it, but a mtg with Carl and zebley and I think Bill.")
  strzok_to_page(child_file, "2017-05-21T18:42:18-00:00", "Tomorrow?")
  # Page 34 has the unredacted version of this message
  # strzok_to_page(child_file, "2017-05-21T18:45:21-00:00", "Yep let's see. I can envision the end state following the meeting, but let things run their course. One thing I (we) know is --Redacted-- will not buck --Redacted--")

  # Page 463
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-05-21T19:02:22-00:00", "You still at wotk? Just left you a vm.")
  page_to_strzok(child_file, "2017-05-21T19:08:22-00:00", "Got your vm. I'm at my desk.")
  strzok_to_page(child_file, "2017-05-21T19:14:45-00:00", "Just tried")
  strzok_to_page(child_file, "2017-05-21T19:27:01-00:00", "Hey called again --Redacted-- sorry I missed you.")
  page_to_strzok(child_file, "2017-05-21T19:33:28-00:00", "Sorry. Went in with Andy again.")
  strzok_to_page(child_file, "2017-05-21T19:36:56-00:00", "Np. Just staffing thoughts. I think Carl and Bill are too far removed from working at that level to know.\n\nOne of the advantages I have from a big a glorified case agent. \U0001f612")
  strzok_to_page(child_file, "2017-05-21T20:03:42-00:00", "And hey, fwiw, the announcement of wf sac (and assuming I don't get it), I still think I want to talk to Andy, if only to discuss what you and I talked about. My worry is he's so damn busy right now I don't want to impose on his time. But I AM worried what the future holds with the dynamics changing....")
  page_to_strzok(child_file, "2017-05-23T18:28:58-00:00", "And I'm not sitting in on this meeting now. \U0001f612 Honestly, I'm really not sure I want this. Am waiting for our team to arrive, then I'm going to walk back and I'll call...")
  strzok_to_page(child_file, "2017-05-23T19:07:26-00:00", "Hey just missed you")
  strzok_to_page(child_file, "2017-05-23T19:07:42-00:00", "Stopped by your office, too")
  page_to_strzok(child_file, "2017-05-23T19:08:31-00:00", "Stay there, I'm coming up. I was on 4.")
  strzok_to_page(child_file, "2017-05-23T20:50:53-00:00", "Can you talk? Jon needs to cancel hpsci tomorrow so we can meet with Bob. He's going to talk to Beth to do so.")
  strzok_to_page(child_file, "2017-05-23T21:25:44-00:00", "So this drives me nuts - just had the most collegial convo with Carl (since I left your office) weird")
  page_to_strzok(child_file, "2017-05-24T00:00:00-00:00", "--Redacted-- Yes, it's an honor to be asked, but so what. I don't want to live constantly straddling two worlds.")
  strzok_to_page(child_file, "2017-05-24T00:02:12-00:00", "That's a very valid concern. You truly will never get this time back, ever.\n\nAnd I have no way to predict what the schedule will look like. The only thing I can tell you is the best predictor is there past, and both Bob and Aaron are tremendous Workaholics. Both demanding.")
  strzok_to_page(child_file, "2017-05-24T00:02:49-00:00", "Have you had a conversation wiht Aaron about what his hours have been like this past week? If he's working until 9 or 10, that says something. If they're all leaving at 6, that says another.")
  strzok_to_page(child_file, "2017-05-24T00:03:51-00:00", "My worry is that all these attorneys that they're bringing from the private sector will be used to long hours, because they're used to law firm salaries. They won't mind missing the money, but will bring that same expection of long long hours.")

  # Page 464
  # OUTBOX == Page
  # INBOX == Strzok
  # Page 34 has unredacted version of this message
  # page_to_strzok(child_file, "2017-05-24T00:09:35-00:00", "They are working very very long hours already. And every weekend. --Redacted--")
  # strzok_to_page(child_file, "2017-05-24T00:10:41-00:00", "Sigh. That's what I was afraid of. Are you locked in with Baker if something happens to Andy?")
  # page_to_strzok(child_file, "2017-05-24T00:18:32-00:00", "So long as baker stays, yes.")
  page_to_strzok(child_file, "2017-05-24T00:37:01-00:00", "I really don't want to do this, I see myself growing more resolute about that with this time away.")
  strzok_to_page(child_file, "2017-05-24T00:38:15-00:00", "I'm proud of you.\n\nIn a million ways, I'm proud of you, and admire you.\n\nAnd please take that in the context of me having that pride without any obligation from you, any expectation of needing to live up to it, anything else. Just :)")
  strzok_to_page(child_file, "2017-05-24T00:38:34-00:00", "Then all the more reason to have that time.")
  page_to_strzok(child_file, "2017-05-24T00:40:18-00:00", "So if you really do want to join the team, don't let my participation stop you. Truly.")
  strzok_to_page(child_file, "2017-05-24T00:40:49-00:00", "Make sure you're weighting all your considerations honestly and appropriately. You said tonight you want to stay and protect the FBI. Is that true, or is it really stay and protect Andy? What if it's Director Townsend? Staying for Andy is perfectly fine. Just be brutally honest with yourself.")
  strzok_to_page(child_file, "2017-05-24T00:42:23-00:00", "I don't know what I want, Lisa. I don't want to be anything but the lead agent. And I think that is going to be a far cry from the inner sanctum of what Bob decides. I don't think agents will play a significant role. I (or whoever) might work into that circle of trust, but he's not going to view the lead agent the same as aaron")
  page_to_strzok(child_file, "2017-05-24T00:43:26-00:00", "No, but Aaron might, which would be as good as Bob doing it.")
  strzok_to_page(child_file, "2017-05-24T00:52:12-00:00", "I guess. Still. I would likely retire out of that job. No way its done in --Redacted--")
  page_to_strzok(child_file, "2017-05-24T01:03:01-00:00", "Could I have oca get Brennan's testimony and send it to you? Then you provide to SC?")
  strzok_to_page(child_file, "2017-05-24T01:05:38-00:00", "Just talked to Andy. I have to go in now and meet the AG with him and Bill.")
  page_to_strzok(child_file, "2017-05-24T01:08:41-00:00", "Now? Like, tonight?")
  strzok_to_page(child_file, "2017-05-24T01:09:43-00:00", "Yes. Talk?")
  strzok_to_page(child_file, "2017-05-24T02:55:06-00:00", "Well that was fun. AG had --Redacted-- leave \"because he wasn't on the list.\" \U0001f62e That'll help my relationship with him...")
  strzok_to_page(child_file, "2017-05-24T02:55:25-00:00", "It's what we speculated")
  page_to_strzok(child_file, "2017-05-24T03:09:32-00:00", "Hell, that's not your fault. I'm headed to bed. Good luck with everything tomorrow.")
  strzok_to_page(child_file, "2017-05-24T03:10:59-00:00", "True, it's not. Surreal, chapter #832.\n\nSleep well, Lisa. :)")
  strzok_to_page(child_file, "2017-05-24T09:30:56-00:00", "Hi there.\n\nOne more observation from last night - --Redacted-- a snake.")

  # Page 465
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-05-24T09:50:24-00:00", "Absolutely, yes. I'm curious to know why you say that. I'm at the airport. Lines are unlike any I've ever seen. Not sure why.")
  strzok_to_page(child_file, "2017-05-24T16:27:37-00:00", "Hi\n\nHad a somewhat detailed convo about structure with Bob and aaron and --Redacted-- (who is --Redacted-- on steroids). They're envisioning --Redacted-- You are above that handling all leg affairs, assume reporting direct into Bob and leadership.")
  page_to_strzok(child_file, "2017-05-24T16:29:05-00:00", "Hmm.")
  page_to_strzok(child_file, "2017-05-24T16:29:23-00:00", "Will call you once I am at the gate.")
  page_to_strzok(child_file, "2017-05-24T17:07:17-00:00", "Hey did you get the Brennan transcript to Aaron?")
  page_to_strzok(child_file, "2017-05-24T17:09:05-00:00", "Never mind, I just sent it to him.")
  strzok_to_page(child_file, "2017-05-24T18:06:16-00:00", "No I hadn't. Thanks.")
  strzok_to_page(child_file, "2017-05-29T23:20:26-00:00", "NYTimes: A Constitutional Puzzle: Can the President Be Indicted?\nA Constitutional Puzzle: Can the President Be Indicted? https://nyti.ms/2scC27a")
  page_to_strzok(child_file, "2017-05-31T00:38:22-00:00", "You going to give az a heads up tonight?")
  m = strzok_to_page(child_file, "2017-05-31T00:43:50-00:00", "Oh, he was there. Standby on imsg")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2017-05-31T03:10:00-00:00", "Asked me at the end whether I would be willing to serve in a similar role as I have for Andy. It frankly makes more sense than conf. affairs. Let's talk through. Also, please clear.")
  page_to_strzok(child_file, "2017-06-01T00:53:04-00:00", "Btw andy called me earlier but I was at --Redacted-- and couldn't talk. Our plan is to talk tomorrow. Good sign that he is reaching out I think.")
  strzok_to_page(child_file, "2017-06-01T01:06:05-00:00", "Gosh I hope so. I was having some regret that I didn't tell him what I was currently thinking")
  page_to_strzok(child_file, "2017-06-01T01:09:41-00:00", "I'm sure he's calling to follow up from my text yesterday in light of Bob's call today.\n\nTo be clear, if he asks about you I'm going to say you're always a benefit to the team, but that the team will be okay without you.")
  strzok_to_page(child_file, "2017-06-01T01:15:14-00:00", "Is that the right answer re me? It may be true, but I'm reassessing what the hell I want right now. I don't have a great feeling about the big bureau right now and my role (and others perception of that) in it, and the SC seems like a tangible, worthwhile effort to do before I retire.")
  strzok_to_page(child_file, "2017-06-01T01:16:50-00:00", "What do you think I should do?")
  page_to_strzok(child_file, "2017-06-01T01:19:30-00:00", "I think you should stay the course. But I will talk to Andy honestly about --Redacted-- and future and all that.")

  # Page 466
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-01T01:23:35-00:00", "Is Andy truly accepting of the fact of the potential limitations that he may not be DD as long as he thought, and regardless, that we'll have a new D, as all this unfolds?\n\nBtw, Bill said he heard some guy in INSD was ranked #2 for the job. Someone we interviewed of a SC job in CD and turned down. Truly I don't know wtf is going on. Do I have cognitive dissonance?")
  strzok_to_page(child_file, "2017-06-01T01:44:36-00:00", "Look, here's the bottom line as best as I can sum up (and I hope you already know all this)\n\n- I don't think Andy's acting in bad faith. I do think what he hypothetically proposes isn't something in his thought process or skillset or his available time and ability. In other words, when JG or Randy or even Bob said they had a plan, they had a PLAN. I don't think Andy does. And as A/D that's something too small for him to worry about. To put a fine point on in --Redacted-- Wtf. Such a pin to the balloon of faith and confidence in the system.\n\n- I knew my standing with Comey and Andy. One is gone, the other uncertain at best.\n\n- I don't trust/believe in my standing with Dave and Carl and the rest of the EADs.\n\n- the SC is straightforward and rewarding, meaningful, honorable and a known quantity. It would cement my image as the \"special project guy\" or \"glorified case agent\" (nevermind they'll never see --Redated-- that way for doing the same job less well). I guess I'm feeling like I don't care about that right now. But it's not like i have a long time left.")
  page_to_strzok(child_file, "2017-06-01T02:05:56-00:00", "I understand all this. So what do you want me to say to him? Can I lay out this thinking, attributes to me?")
  strzok_to_page(child_file, "2017-06-01T02:20:26-00:00", "I don't know.\n\nMaybe i should sleep on it.\n\nMaybe, Pete's uncertain, between Comey the --Redacted-- he's reassessing if he should just go?\n\nI don't know, Lis.")
  page_to_strzok(child_file, "2017-06-01T02:25:27-00:00", "We can talk in the morning.")
  page_to_strzok(child_file, "2017-06-01T02:25:56-00:00", "But I think that's a perfectly reasonable way to approach it.")
  strzok_to_page(child_file, "2017-06-01T02:34:23-00:00", "Thank you \U0001f636")
  strzok_to_page(child_file, "2017-06-01T02:36:40-00:00", "Sorry I don't have a ready answer here. I feel strongly - if ambiguously - at the same time I want to represent myself at the same time I don't want to be \"that guy\"\n\nNone of us are owed anything. Except when I think of the last 18 months.\n\nAnd then I think several of us ARE owed something. --Redacted--")
  strzok_to_page(child_file, "2017-06-01T10:09:59-00:00", "Hi.\n\nThe only additional thought I had is it's not tenable to have both me and --Redacted--chere. If he's in charge and I'm around, it undermines him (because Mueller and Aaron will be looking to me), it puts me in a horrible position, and it's a waste of Bureau resources. I told Bill that, but in don't know that will get up from him thru Carl to Andy.")

  # Page 467
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-01T10:14:34-00:00", "Yeah, I definitely plan to do that.")
  page_to_strzok(child_file, "2017-06-01T10:16:51-00:00", "I'm growing more doubtful about my role staying on. For the same reason you're not absolutely essential once 30 or 45 days is up, I'm not absolutely essential. You don't need someone to see around corners and check for pitfalls when you have the most all-star of all-star teams. I mean sure, might catch a ball or two? Maybe. But not like the value I add at HQ when it's mostly not all-stars.")
  strzok_to_page(child_file, "2017-06-01T10:16:59-00:00", "Thanks. Really curious to hear what he's thinking.")
  strzok_to_page(child_file, "2017-06-01T10:21:01-00:00", "I hear you. But a couple of things. First, I really truly believe you're not giving yourself enough credit for how good you are. Depends on what you want. At the Bu, you'll be a superstar amongst mostly not all-stars. There, you're a superstar amongst superstars.\n\nSecond, be really honest, what is your future at the Bureau? As long as Andy is A/D, you're in a weird place with JR and --Redacted-- I don't know what his future is when a D is confirmed. Nor do I know Bakers future. --Redacted-- And in terms of launching into the private sector, it's FAR more valuable.")
  strzok_to_page(child_file, "2017-06-01T10:22:01-00:00", "On the flip side, I probably wouldn't want to be --Redacted-- not with --Redacted--")
  page_to_strzok(child_file, "2017-06-01T10:22:03-00:00", "This is all true. But do I want this enough if my job is --Redacted--")
  strzok_to_page(child_file, "2017-06-01T10:22:21-00:00", "Jesus")
  page_to_strzok(child_file, "2017-06-01T10:23:20-00:00", "I honestly just don't see much of a role working for Bob/Aaron. They don't really need me. I'm happy to shag issues, but I don't really see that happening. Aaron doesn't give up much.")
  strzok_to_page(child_file, "2017-06-01T10:25:12-00:00", "That's definitely true re Aaron. I don't know if you'll be part of the true inner core, especially when they're fully staffed. Nor whoever the lead fbi person is.")
  page_to_strzok(child_file, "2017-06-01T10:25:50-00:00", "So then what am I doing there? Just padding my resume?")
  strzok_to_page(child_file, "2017-06-01T10:30:40-00:00", "Doing something meaningful, historic")
  strzok_to_page(child_file, "2017-06-01T10:31:15-00:00", "And yes, making contacts and superbly positioning yourself for whatever comes next")
  page_to_strzok(child_file, "2017-06-01T10:32:00-00:00", "Meh. Not if I'm the least impressive among the most impressive brains in America.")
  strzok_to_page(child_file, "2017-06-01T10:32:06-00:00", "Sorry was reading Carrie Johnson tweet and thread about Andrew being added to the team")
  page_to_strzok(child_file, "2017-06-01T10:32:44-00:00", "Send it please? He must have told her - they're close")
  strzok_to_page(child_file, "2017-06-01T10:33:55-00:00", "Lisa. I don't think that's true. You won't be least impressive. You (and/or i, if I go) will solidly hold our own. Thats more than enough for you when it's all done. And that group will forever take take of itself. Look at the Enron crew.")
  
  # Page 468
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-01T10:34:28-00:00", "Yeah, maybe.")
  strzok_to_page(child_file, "2017-06-01T22:48:19-00:00", "--Redacted-- and I thought Jim (maybe you too but i couldn't read that) was cranky. Was that from your convo before?")
  strzok_to_page(child_file, "2017-06-01T22:50:55-00:00", "Argued with him along the lines of what I assume you did. I get his unanticipated consequences arguments, but I think it strains logic.\n\nAnyway. Sorry that review made you late. --Redacted--")
  page_to_strzok(child_file, "2017-06-01T22:51:54-00:00", "I didn't think Jim was cranky. Probably just tired because he was just on an hours long panel on 702. I thought YOU were cranky.")
  strzok_to_page(child_file, "2017-06-01T22:53:31-00:00", "Oh.\n\nAmd really?Im sorry. Just felt really strongly on that one early point. Was I a jerk? If so, I apologize. :(")
  page_to_strzok(child_file, "2017-06-01T22:54:44-00:00", "No, you just get that weird defensive way that isn't really appropriate for a colleague but whatever.")
  strzok_to_page(child_file, "2017-06-01T23:11:24-00:00", "Sorry, I didn't notice. Was just working up about it. I did note your \"can I finish\" which I now assume might have been driven by that perception. Anway, sorry. I'll watch out for it.\n\n--Redacted--")
  strzok_to_page(child_file, "2017-06-01T23:49:32-00:00", "--Redacted-- delayed reaction to --Redacted-- made me laugh.\n\nFwiw, I got no further on the structure argument than I think you did. Even made the shifting organizational risk argument.")
  strzok_to_page(child_file, "2017-06-02T00:11:44-00:00", "Ha. Aaron just called (but had to answer another call), said he had talked to you on one of the issues...not sure what but will call back.")
  # Page 34 has unredacted version of this message
  # page_to_strzok(child_file, "2017-06-02T00:16:22-00:00", "Re the mtg tomorrow. Not clear now which subj (which is his Question I am guessing) but either way --Redacted-- wants to attend which is an issue.")
  # Page 34 has unredacted version of this message
  # page_to_strzok(child_file, "2017-06-02T00:16:47-00:00", "Ie, --Redacted--")
  #strzok_to_page(child_file, "2017-06-02T00:17:40-00:00", "Hmm. I heard --Redacted-- What did you hear?")
  strzok_to_page(child_file, "2017-06-02T00:17:51-00:00", "And from who? Mine came from Paul")
  #page_to_strzok(child_file, "2017-06-02T00:18:13-00:00", "Wait I forget the codename.")
  #page_to_strzok(child_file, "2017-06-02T00:18:28-00:00", "Oh yes. --Redacted--")
  #page_to_strzok(child_file, "2017-06-02T00:18:40-00:00", "He thought maybe someone else")
  # Page 34 has unredacted version of this message 
  # strzok_to_page(child_file, "2017-06-02T00:20:46-00:00", "Who's saying --Redacted-- wants to attend?")
  # page_to_strzok(child_file, "2017-06-02T00:21:28-00:00", "Tash said --Redacted-- called her said --Redacted-- invited them.")

  # Page 469
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-02T00:41:10-00:00", "Yeah just talked to aaron, he relayed same. --Redacted-- is f*cking this ALL up. I think Paul A gets it and Andy's intent (or at least made statements to Carl about it in front of me), but word most certainly is not getting down the chain.\n\nYou've now GOTTA come to this sh*t show of a brief tomorrow.")
  strzok_to_page(child_file, "2017-06-02T00:41:32-00:00", "That is not, however, the topic insane your praises about. \U0001f60a")
  page_to_strzok(child_file, "2017-06-02T00:43:47-00:00", "So what'd you say? I need to have a convo next week about my role. If Aaron let me be an extension of him, I think I could really help him.")
  page_to_strzok(child_file, "2017-06-02T01:18:19-00:00", "--Redacted-- In other not fun news, one of the admin ladies said Aaron asked each of us to submit a resume for their records. \U0001f612")
  strzok_to_page(child_file, "2017-06-02T01:20:41-00:00", "Hahaha. That makes me laugh for some reason. I'll help. \U0001f60a")
  strzok_to_page(child_file, "2017-06-02T01:20:52-00:00", "Universe talking to you, Page.")
  page_to_strzok(child_file, "2017-06-02T01:24:09-00:00", "Btw, I meant to point out to you today, you used the expression \"horse sense\" in reference to \"any agent's horse sense will tell them x...\" See? Horse sense. It's an expression for a reason... :)")
  strzok_to_page(child_file, "2017-06-02T01:25:02-00:00", "Ha. You're absolutely right. I had no notion of doing it when I did.")
  strzok_to_page(child_file, "2017-06-02T01:49:02-00:00", "Aaron said he was going to talk to Carl tomorrow. I told him that, --Redacted-- some call he had with --Redacted-- these are the 10-14 days of hurt feelings and tears. At the point of moving past nice, just saying how it is.")
  page_to_strzok(child_file, "2017-06-02T10:54:20-00:00", "Think we are having the 9:15 this am?")
  strzok_to_page(child_file, "2017-06-02T10:54:46-00:00", "We're not. Was going to ask if you want to walk over.")
  page_to_strzok(child_file, "2017-06-02T10:56:23-00:00", "Have to do the class review doc first.")
  strzok_to_page(child_file, "2017-06-02T13:37:36-00:00", "And I just picked up on what you said when you answered the phone. What were/are you talking about?")
  page_to_strzok(child_file, "2017-06-02T13:38:15-00:00", "SC job vs staying")
  strzok_to_page(child_file, "2017-06-02T13:39:21-00:00", "What does he think - yes for you, no for me?")
  page_to_strzok(child_file, "2017-06-02T13:44:32-00:00", "Torn like I am. Agrees that andy and you need to talk.")
  strzok_to_page(child_file, "2017-06-02T13:46:27-00:00", "I am too, Lis. Kind of really depends on that conversation you have with Aaron.\n\n--Redacted-- running late with Bill. I'll call you when I'm done. Haven't heard back from Aaron, maybe we just walk over (again)")
  page_to_strzok(child_file, "2017-06-02T13:47:23-00:00", "So is Bill free? I have a r0 second question")
  
  # Page 470
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-02T13:48:06-00:00", "No - he switched meeting times with me because he has to run to State. Amd now he's late.")
  strzok_to_page(child_file, "2017-06-02T16:43:26-00:00", "You free?")
  strzok_to_page(child_file, "2017-06-02T16:51:31-00:00", "Talking to --Redacted-- We need to talk")
  page_to_strzok(child_file, "2017-06-02T16:58:10-00:00", "Sorry, just found my phone. Not much to do right now re --Redacted-- but okay.")
  strzok_to_page(child_file, "2017-06-02T17:53:17-00:00", "Two redactions I need to doscuss, let me know when you're back")
  strzok_to_page(child_file, "2017-06-02T19:34:27-00:00", "Please call me before you leave SC")
  page_to_strzok(child_file, "2017-06-02T19:39:25-00:00", "Am at desk here")
  strzok_to_page(child_file, "2017-06-02T21:12:14-00:00", "Thanks for bringing those two things back. :)")
  strzok_to_page(child_file, "2017-06-02T21:42:44-00:00", "You still here? I have hill contact dates for you")
  strzok_to_page(child_file, "2017-06-02T22:15:20-00:00", "I talked with Aaron, call me if you can")
  page_to_strzok(child_file, "2017-06-02T22:23:50-00:00", "Will call you on the way home. Got a drink with baker. Needed his good counsel.")
  page_to_strzok(child_file, "2017-06-02T22:24:09-00:00", "Talked to him about you too, so he's going to think about it and will reach out.")
  strzok_to_page(child_file, "2017-06-02T22:25:25-00:00", "Man I can NEVER get him to go out. I've got that --Redacted-- jealousy you mentioned.;)")
  page_to_strzok(child_file, "2017-06-02T23:23:46-00:00", "Hope things are okay. Please do what you think is best re job. Don't sweat me. I'll just have to talk to --Redacted-- about it if the decision presents itself.")
  strzok_to_page(child_file, "2017-06-02T23:42:36-00:00", "What do you want. Don't think. What's your immediate gut?")
  strzok_to_page(child_file, "2017-06-02T23:47:10-00:00", "I can probably talk in 10 min or so")
  page_to_strzok(child_file, "2017-06-02T23:50:32-00:00", "I really don't know. Jim got me squarely back into support sc, but that changes minute by minute.")
  page_to_strzok(child_file, "2017-06-02T23:50:50-00:00", "I would love to, but not sure I can. --Redacted-- ")
  strzok_to_page(child_file, "2017-06-02T23:52:37-00:00", "Got it.\n\nI think where I am is exactly what YOU thought. \U0001f636\n\nI can only take this up to a point. After that, Mueller and the bright attorneys will drive it, not me.")
  strzok_to_page(child_file, "2017-06-02T23:53:53-00:00", "W/r/t you, I think it's a bit different. I think you will be a trusted part of the team, but maybe never in the core leadership. BUT, because you're an attorney, this is an entirely different developmental opportunity. This helps you immeasurably in your future legal career.")
  page_to_strzok(child_file, "2017-06-03T00:02:02-00:00", "Yes, I'm sure that is true.")
  strzok_to_page(child_file, "2017-06-03T00:06:12-00:00", "How will your ego be if you wnd up working as a more \"junior\" arrorney in this? (Not saying you will, just think that's the unlikely worst case for you).")
  
  # Page 471
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-03T00:12:08-00:00", "I talked about that with Jim. He has a nice way of framing that I'm not there to compeat with --Redacted-- so don't try to write some magnificent appellate brief.")
  page_to_strzok(child_file, "2017-06-03T00:17:19-00:00", "And let's face it, I WILL be a junior attorney. We've got the freaking titans of law joining this thing.")
  strzok_to_page(child_file, "2017-06-03T00:19:50-00:00", "Exactly. I see that. I wanted to see if you saw the same. And if you're comfortable maybe coming off the bench on the all star team rather being one of the star starters on team FBI.")
  page_to_strzok(child_file, "2017-06-03T00:22:07-00:00", "Ha. Jim had a similar analogy. You might not be on the line, but there are a lot of people who are necessary to keep the team on the field.")
  strzok_to_page(child_file, "2017-06-03T00:22:18-00:00", "You haven't asked, but I think you should go. It is an experience unlike any other you're going to get. Life changing.\n\nThats the ONLY thing seriously keeping me considering it.")
  page_to_strzok(child_file, "2017-06-03T00:22:54-00:00", "I know you are right.")
  # page_to_strzok(child_file, "2017-06-03T00:23:45-00:00", "It's just hard to be untethered to the Bureau and Andy right now. It's been bad enough without Comey, this just feels like another loss.")
  strzok_to_page(child_file, "2017-06-03T00:24:06-00:00", "Well i know he was smart. \U0001f609\n\nTo my question: how do you feel when they call the meeting, not just Meuller aaron and Quarles, but a couple of attorneys, but not you?")
  strzok_to_page(child_file, "2017-06-03T00:24:44-00:00", "Oh this project? You'll feel am integral part of a family team before the 4th of July. You'll be working too hard not to.")
  strzok_to_page(child_file, "2017-06-03T00:26:10-00:00", "And therein's the rub. How much have you enjoyed your --Redacted--\n\nMy biggest drawback is I'm just am agent on an attorney-driven team.")
  strzok_to_page(child_file, "2017-06-03T00:27:01-00:00", "I want to talk to Baker. I'm curious how he addresses the not being part of the true leadership team and the end of the day, how I have a greater potential to give in the FBI.")
  page_to_strzok(child_file, "2017-06-03T00:34:25-00:00", "I won't like it one bit. Jim says I need to be patient, that I will earn their trust and make it into the room eventualy.")
  strzok_to_page(child_file, "2017-06-03T00:40:11-00:00", "I wouldn't either.")
  strzok_to_page(child_file, "2017-06-03T00:41:08-00:00", "And I completely get your feeling of untethered, of yet another loss.")
  strzok_to_page(child_file, "2017-06-03T00:41:28-00:00", "But Andy's going right around the corner. In a blink of an eye.")
  page_to_strzok(child_file, "2017-06-03T00:47:57-00:00", "And what does SC do to your --Redacted--")
  strzok_to_page(child_file, "2017-06-03T01:54:35-00:00", "Watcha doing?\n\nI've lost all motivation. Didn't edit - let alone send - email to Jim. --Redacted--")
  
  # Page 472
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-03T01:54:59-00:00", "--Redacted-- displays on my work iPhone and I never cleared. --Redacted--")
  page_to_strzok(child_file, "2017-06-03T01:55:46-00:00", "Why not send it? Jim cares about you. Jim only pays the attention that he does to me because I'm pushy and I show up.")
  m = strzok_to_page(child_file, "2017-06-03T02:16:02-00:00", "Well I don't wnat to do it now, it's late. Let me make the edit and re-send to you.\n\nI'm sorry about the imsg. Thats good to know about the lock screen.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2017-06-03T03:31:31-00:00", "I get more uncertain as times goes on.\n\nYou get shy more clarity?")
  strzok_to_page(child_file, "2017-06-03T03:31:56-00:00", "Any not shy")
  strzok_to_page(child_file, "2017-06-03T11:13:04-00:00", "This is turning out to be a really hard decision. Are you settling on one place or another?")
  strzok_to_page(child_file, "2017-06-03T11:31:36-00:00", "Because I'm really torn. I though sleep would help, but nope. I guess I'm still leaning don't go.\n\nWhere are you with you?")
  page_to_strzok(child_file, "2017-06-03T11:42:34-00:00", "I'm just going to stay for now, do what they want me to do.")
  strzok_to_page(child_file, "2017-06-03T11:47:19-00:00", "Good!")
  strzok_to_page(child_file, "2017-06-03T11:48:00-00:00", "You feeling at peace with that?")
  page_to_strzok(child_file, "2017-06-03T11:51:36-00:00", "No, but I'm going to try to get there.")
  strzok_to_page(child_file, "2017-06-03T11:53:10-00:00", "I get it. --Redacted--")
  strzok_to_page(child_file, "2017-06-03T11:53:37-00:00", "And you need to tell me one last time it's not presumptuous to email JB...")
  page_to_strzok(child_file, "2017-06-03T11:58:44-00:00", "It is not. You can even tell him I told you to email jim.")
  strzok_to_page(child_file, "2017-06-03T12:00:40-00:00", "Well, I sent it. And promptly realized I forgot to change \"this evening\" to \"yesterday.\" \U0001f612")
  strzok_to_page(child_file, "2017-06-03T16:16:35-00:00", "And no response from Jim and I feel foolish...maybe it's the universe, along with you, telling me to stay the course...")
  page_to_strzok(child_file, "2017-06-03T16:32:21-00:00", "He almost never checks on the weekend. Wait until the evening. And stop worrying. He cares about you.")
  strzok_to_page(child_file, "2017-06-03T16:35:12-00:00", "Ok \U0001f615")
  strzok_to_page(child_file, "2017-06-03T20:21:44-00:00", "5 is today? That's more than I've heard...any FBI there?")
  strzok_to_page(child_file, "2017-06-03T20:21:59-00:00", "Agents, I mean")

  # Page 473
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-03T20:22:35-00:00", "Or you mean the daily 5s?\n\nIf it makes you feel any better, I've had no calls and no emails since Aaron yesterday at 530.")
  page_to_strzok(child_file, "2017-06-03T20:24:13-00:00", "The daily 5:00s.")
  strzok_to_page(child_file, "2017-06-03T20:24:34-00:00", "Oh. Have those started?")
  strzok_to_page(child_file, "2017-06-03T20:25:00-00:00", "I haven't heard anything about them. I was just going to show up.")
  page_to_strzok(child_file, "2017-06-03T20:25:38-00:00", "--Redacted-- asked me where I substantively want to land on the team. I just don't know the answer. Maybe under Andrew on --Redacted-- At least I know him.")
  strzok_to_page(child_file, "2017-06-03T20:25:44-00:00", "How did you find out? From him?\n\nThough I confess this is steering me firmly onto the stay the course path.")
  page_to_strzok(child_file, "2017-06-03T20:26:14-00:00", "I'm guessing you haven't been invited because they don't want it to be --Redacted-- if you leave. Yea, they happen every day.")
  page_to_strzok(child_file, "2017-06-03T20:26:56-00:00", "I'm at SC. Had a mtg with az, --Redacted-- and --Redacted-- at 1:30.")
  strzok_to_page(child_file, "2017-06-03T20:27:06-00:00", "Is \"chief of staff\" or \"assistant to Aaron\" tenable?\n\nAaron told me they were going to have them. Just hadn't heard they had started.")
  strzok_to_page(child_file, "2017-06-03T20:27:48-00:00", "Any agents around?\n\nI'm telling you, this may cement it for me.")
  page_to_strzok(child_file, "2017-06-03T20:27:48-00:00", "He asked --Redacted-- to start coming to them at the end of our meeting.")
  strzok_to_page(child_file, "2017-06-03T20:28:17-00:00", "Any indication to you about whether or not he wanted you there?")
  page_to_strzok(child_file, "2017-06-03T20:28:26-00:00", "In the ofc? No. But that doesn't mean. They're not working at hq.")
  strzok_to_page(child_file, "2017-06-03T20:28:50-00:00", "I'd do --Redacted-- or --Redacted-- If you can't do some leadership element thing.")
  page_to_strzok(child_file, "2017-06-03T20:29:04-00:00", "He certainly didn't tell me to start showing up, so I didn't ask.")
  strzok_to_page(child_file, "2017-06-03T20:29:35-00:00", "I think it's ultimately OK for you even if you're on the bench. But you ego's gonna need some TLC.")
  page_to_strzok(child_file, "2017-06-03T20:31:53-00:00", "Yeah, tell me about it. \U0001f614")
  strzok_to_page(child_file, "2017-06-03T20:33:42-00:00", "Think of it this way - coming down off of DD staff to this is a HELL of a lot better than coming down to OGC somewhere....")
  strzok_to_page(child_file, "2017-06-03T20:34:30-00:00", "But no doubt about it, it sucks. I can feel MY urge to want in, right now, even though I'm in some non-committed tdy limbo.")
  strzok_to_page(child_file, "2017-06-03T20:39:16-00:00", "How long are you staying? Will people be around if I stop by before the Valor game? (That'll impress the hell.out of them!)")
  page_to_strzok(child_file, "2017-06-03T20:40:44-00:00", "I'm at hq now, but JQ and AW are there.")
  strzok_to_page(child_file, "2017-06-03T20:44:50-00:00", "I wouldn't be there for another hour, plus I doubt my card works.")

  # Page 474
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-03T20:55:58-00:00", "Do you want to be --Redacted-- Andrew? Why not with --Redacted-- where there are at --Redacted-- and you might get assigned one?\n\nBut I don't know. Thats a tough call.")
  page_to_strzok(child_file, "2017-06-03T21:00:35-00:00", "I'm scared of --Redacted-- Andrew is at least a known quantity? I don't know...")
  strzok_to_page(child_file, "2017-06-03T21:18:22-00:00", "Yeah I know. --Redacted-- though. Plus you know CI better than all attys....")
  strzok_to_page(child_file, "2017-06-03T21:21:11-00:00", "Driving if you can talk.")
  strzok_to_page(child_file, "2017-06-03T21:21:40-00:00", "Truly that might be your niche - work the --Redacted--")
  strzok_to_page(child_file, "2017-06-03T21:21:46-00:00", "Angle")
  m = page_to_strzok(child_file, "2017-06-03T23:05:51-00:00", "Crap! I forgot my eras. \U0001f621\U0001f621\U0001f621")
  m.addnote("eras - Enterprise Remote Access System")
  strzok_to_page(child_file, "2017-06-03T23:06:18-00:00", "Dude. It's all unclassified.")
  strzok_to_page(child_file, "2017-06-03T23:06:37-00:00", "Type on home computer and email to yourself.")
  page_to_strzok(child_file, "2017-06-03T23:06:58-00:00", "Okay. But it would help to have what I wrote. But fair enough.")
  #strzok_to_page(child_file, "2017-06-03T23:07:04-00:00", "Subj in custody, btw. First ML arrest of the Trump era")
  strzok_to_page(child_file, "2017-06-03T23:08:09-00:00", "Yeah. --Redacted--")
  page_to_strzok(child_file, "2017-06-03T23:12:34-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-04T01:13:36-00:00", "I'm trying to write an email back to --Redacted-- but don't know what to say after, thanks for the heads up. How would you finish that email?")
  page_to_strzok(child_file, "2017-06-04T01:15:06-00:00", "Maybe just hope this gets resolved soon? I have no idea.")
  page_to_strzok(child_file, "2017-06-04T01:17:15-00:00", "I'm going to mention --Redacted-- And I'm going to tell him --Redacted-- has to grow a pair and start correcting people when they say Andy.")
  strzok_to_page(child_file, "2017-06-04T01:20:42-00:00", "Yep")
  strzok_to_page(child_file, "2017-06-04T01:21:23-00:00", "He just needs to send a message. Amd --Redacted-- needs to stand up and get people in line. Thats his job, not JR's.")
  page_to_strzok(child_file, "2017-06-04T01:25:27-00:00", "Please, when you get a chance, plug with Aaron all the behind the scenes work I did with Andy, Jim, etc. to get this result. Andy was NOT going to do it just based on Mueller's convo with him - he just didn't understand what the problem was. AND I did a lot of work to help them understand that --Redacted-- was also not the right guy.")
  page_to_strzok(child_file, "2017-06-04T01:25:42-00:00", "Thank you. \U0001f636")
  strzok_to_page(child_file, "2017-06-04T01:26:36-00:00", "Of course I will. \U0001f636")

  # Page 475
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-04T01:29:37-00:00", "I worry they think I'm too loyal to Andy or Comey, won't truly trust me because of that. Maybe this will help.")
  page_to_strzok(child_file, "2017-06-04T01:29:39-00:00", "?")
  page_to_strzok(child_file, "2017-06-04T01:29:42-00:00", "I dunno.")
  strzok_to_page(child_file, "2017-06-04T01:35:17-00:00", "I wouldn't worry about that")
  strzok_to_page(child_file, "2017-06-04T01:35:20-00:00", "Just be you")
  strzok_to_page(child_file, "2017-06-04T01:35:44-00:00", "That will be enough \U0001f60a\U0001f636")
  page_to_strzok(child_file, "2017-06-04T01:39:15-00:00", "It hasn't been yet.")
  strzok_to_page(child_file, "2017-06-04T01:40:57-00:00", "This is true.\n\nAnd I don't think it's that they don't trust you because of Andy or Comey. I think they just don't trust, generally. You will work you way in. Patience.")
  strzok_to_page(child_file, "2017-06-04T01:49:57-00:00", "And sigh. Ok.\n\nDon't worry too much about Mueller and Aaron. You're going to be ok. :)")
  strzok_to_page(child_file, "2017-06-04T15:38:29-00:00", "Just talked to Jim for 40 minutes. He's a good man. He strongly thinks I should go.")
  page_to_strzok(child_file, "2017-06-04T17:12:33-00:00", "He is an incredibly good man.")
  strzok_to_page(child_file, "2017-06-04T17:45:04-00:00", "Yeah")
  page_to_strzok(child_file, "2017-06-05T01:25:56-00:00", "So did you ever get an invite to tomorrow strategy mtg? And Aaron ever call you back?")
  strzok_to_page(child_file, "2017-06-05T01:27:40-00:00", "Yeah me too, re tired.\n\nAaron did call. Think it's still a little early for strategy meeting, so will just do the ops update followed by the oca/OPA wrap")
  strzok_to_page(child_file, "2017-06-05T01:29:20-00:00", "I talked through what he'd envision were I to stay. I asked what my role would be, especially in terms of the leadership group. He thought i would be, but wanted to confirm with RM.")
  strzok_to_page(child_file, "2017-06-05T01:29:46-00:00", "Looks like all hands svtc on Tues and strategy meeting either Tues or Wed.")
  page_to_strzok(child_file, "2017-06-05T01:35:31-00:00", "He ask you to stay for oca/ops wrap?")
  page_to_strzok(child_file, "2017-06-05T01:40:42-00:00", "Super.\n\nI'm glad for you at least.")
  strzok_to_page(child_file, "2017-06-05T01:40:58-00:00", "And morning meetings, but not tomorrow so he can run past RM. He said those have been largely admin in nature.")
  page_to_strzok(child_file, "2017-06-05T01:41:39-00:00", "So you joining the team? I need to talk to --Redacted-- if so.")
  strzok_to_page(child_file, "2017-06-05T01:41:59-00:00", "I don't know.")
  strzok_to_page(child_file, "2017-06-05T01:43:12-00:00", "I told him I wanted to be part of the leadership team if I stayed, because otherwise i didn't know if it would be worth it for me.\n\nI think we do 30 and try things on for size, which I guess was the plan anyway.")

  # Page 476
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-05T01:44:56-00:00", "Let's see what RM says first. If it's not going to work out, then no need to go there")
  page_to_strzok(child_file, "2017-06-05T01:49:32-00:00", "--Redacted-- it'll be fine.")
  strzok_to_page(child_file, "2017-06-05T01:56:04-00:00", "My sense is it will be. All of this is based on earned trust from competence, anyway. I'd have the advantage of being the senior bureau person, which also helps.\n\nI want to talk to you again, obviously. I was surprised how strong and unanimious both JB and Bill were. And if I do after all that, need to talk to Andy.")
  page_to_strzok(child_file, "2017-06-05T02:00:27-00:00", "Okay.")
  strzok_to_page(child_file, "2017-06-05T02:01:51-00:00", "I don't want to go to sleep, because if I do, then next thing I'll wake up and it will be time for work :(")
  page_to_strzok(child_file, "2017-06-05T02:06:05-00:00", "At least at a job in which you're wanted.")
  strzok_to_page(child_file, "2017-06-05T10:06:06-00:00", "Hi there. They do want you, Lisa. Just gotta figure your spot.")
  page_to_strzok(child_file, "2017-06-05T10:10:22-00:00", "Right")
  strzok_to_page(child_file, "2017-06-05T10:11:59-00:00", "You going to talk to Aaron about it? Or just dive in and see what organically develops?")
  page_to_strzok(child_file, "2017-06-05T10:13:21-00:00", "That's starting to seem a little pushy and desperate.")
  strzok_to_page(child_file, "2017-06-05T10:14:44-00:00", "Yeah I agree. So the latter, then. I'm telling you, you'll prove your worth a thousand times, quickly.\n\nGod there are like a million extra bird and nature sounds. Not sure what's up this morning..")
  page_to_strzok(child_file, "2017-06-05T10:16:22-00:00", "I can't prove my worth if I don't have anything to do worthwhile to do, but sure.")
  strzok_to_page(child_file, "2017-06-05T10:17:24-00:00", "Don't you have the --Redacted-- You can use my car to go over there to talk if you want.\n\nYou mentioned worry about becoming his admin person. I wouldn't worry about that too much.")
  strzok_to_page(child_file, "2017-06-05T10:18:24-00:00", "Just keep getting whatever done and ask for more. Do what you do naturally. Be tireless and bright and curious.")
  strzok_to_page(child_file, "2017-06-05T10:18:38-00:00", "Be you \U0001f636")
  strzok_to_page(child_file, "2017-06-05T11:51:42-00:00", "How long is the task that Aaron gave you going to take? The --Redacted-- one?")
  page_to_strzok(child_file, "2017-06-05T12:20:45-00:00", "No clue. No one knows what it entails yet.")
  strzok_to_page(child_file, "2017-06-05T13:27:20-00:00", "Just talked with Aaron, call me when you can")
  page_to_strzok(child_file, "2017-06-05T13:28:16-00:00", "I will.")
  strzok_to_page(child_file, "2017-06-05T13:29:11-00:00", "I'm frustrated. I know you must be too.")
  strzok_to_page(child_file, "2017-06-05T13:47:55-00:00", "Hey are you on phone ? np if so, just want to know whether to hang or not. Have a couple of things for you then I need to hit bubble and SC.")

  # Page 477
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-05T13:51:57-00:00", "I am with --Redacted-- You coming to 10 am?")
  strzok_to_page(child_file, "2017-06-05T13:53:21-00:00", "Shit")
  strzok_to_page(child_file, "2017-06-05T13:53:24-00:00", "Yes. Where?")
  page_to_strzok(child_file, "2017-06-05T13:53:55-00:00", "You can skip it. Ogc conf. Room. I'm not even sure oca is coming.")
  strzok_to_page(child_file, "2017-06-05T13:55:36-00:00", "Got some things I need to run past you, I'll com")
  strzok_to_page(child_file, "2017-06-05T13:55:38-00:00", "Come")
  page_to_strzok(child_file, "2017-06-05T16:45:50-00:00", "Checking out.")
  strzok_to_page(child_file, "2017-06-05T16:46:50-00:00", "Rgr")
  strzok_to_page(child_file, "2017-06-05T18:44:10-00:00", "So this great. Walked over here around 2, they're all in a meeting (I think) and I've been kind of sitting/waiting. \U0001f612")
  # page_to_strzok(child_file, "2017-06-05T19:00:42-00:00", "Let me talk to SC about --Redacted-- I just spoke to Rybicki about them and where things stand.")
  # Unredacted version in lync messages page 34
  # strzok_to_page(child_file, "2017-06-05T19:01:41-00:00", "I just talked to Aaron. He said --Redacted-- in other words, --Redacted--")
  page_to_strzok(child_file, "2017-06-05T19:02:13-00:00", "Call me?")
  strzok_to_page(child_file, "2017-06-05T19:05:06-00:00", "Hey so are you gong to come over in between? If so, I'll wait to talk to Aaron until you get here.")
  page_to_strzok(child_file, "2017-06-05T19:05:31-00:00", "Yes, going to leave momentarily.")
  m = strzok_to_page(child_file, "2017-06-05T19:10:13-00:00", "Ok bring --Redacted--. Just talked to --Redacted-- we can conference call her and mark it up, then get it to Bill for stamp. Put a cover EC and put them in the file.")
  m.addnote("EC - Electronic Communication")
  strzok_to_page(child_file, "2017-06-05T21:23:19-00:00", "And for now, I'm not in the 5:00s...\U0001f612...Aaron told him he recommended yes, but no answer yet.")
  strzok_to_page(child_file, "2017-06-05T22:45:27-00:00", "Hey you still at work? I'm finishing up with Aaron. He's trying to call Scott S now")
  strzok_to_page(child_file, "2017-06-05T22:46:03-00:00", "And --Redacted-- has an office, you better try and hop on one quick")
  page_to_strzok(child_file, "2017-06-05T22:46:32-00:00", "I am still here. I'll hit you up shortly.")
  strzok_to_page(child_file, "2017-06-05T22:47:04-00:00", "Ok I'm in Aarons office, if I don't answer that's why")
  page_to_strzok(child_file, "2017-06-05T22:47:22-00:00", "Should I come over?")
  strzok_to_page(child_file, "2017-06-05T22:47:53-00:00", "Don't think so, I think I'm about to head out.")
  page_to_strzok(child_file, "2017-06-05T22:52:37-00:00", "In with baker.")

  # Page 478
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-05T22:53:18-00:00", "Hey Aaron asked what your second issue was - we both remember op ed/pre-pub review. Can we conference call you?")
  page_to_strzok(child_file, "2017-06-05T22:53:35-00:00", "I'm in with baker.")
  page_to_strzok(child_file, "2017-06-05T22:53:53-00:00", "Was re Stephen Kelly sitting in closed with comey.")
  page_to_strzok(child_file, "2017-06-05T22:53:57-00:00", "Not a big deal.")
  page_to_strzok(child_file, "2017-06-05T22:54:09-00:00", "But need to talk to.him about foia too")
  strzok_to_page(child_file, "2017-06-05T22:55:07-00:00", "Yep. Do you want to conference call, come over, talk tomorrow? Why don't I propose meeting a little bit before the 10?")
  strzok_to_page(child_file, "2017-06-05T22:55:17-00:00", "That way,just all walk up...")
  strzok_to_page(child_file, "2017-06-05T22:56:39-00:00", "Ok, so just proposed to aaron we meet at 945 in my office.\n\nSolved!\n\n:) I've got you....")
  strzok_to_page(child_file, "2017-06-05T23:11:18-00:00", "Heading back --Redacted-- call me whenever")
  page_to_strzok(child_file, "2017-06-05T23:17:29-00:00", "I can't talk right now. I'll call you back shortly.")
  strzok_to_page(child_file, "2017-06-05T23:30:22-00:00", "Hey I'm getting ready to leave. If you're finishing, I'll sit tight, otherwise call me on cell.")
  page_to_strzok(child_file, "2017-06-05T23:36:03-00:00", "In with Andy, leaving now")
  strzok_to_page(child_file, "2017-06-05T23:36:40-00:00", "K I'm still here. You leaving leaving or just going back to office?")
  page_to_strzok(child_file, "2017-06-05T23:47:05-00:00", "Office. Headed there now.")
  m = strzok_to_page(child_file, "2017-06-06T01:01:40-00:00", "Clear imsg...")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2017-06-06T01:36:59-00:00", "Boo where'd you go?")
  page_to_strzok(child_file, "2017-06-06T01:47:16-00:00", "Sorry, this was in my lit bag. Still at work.")
  page_to_strzok(child_file, "2017-06-06T01:48:11-00:00", "Aaron and --Redacted-- were here reading --Redacted-- Aaron asked if you would be willing to take a copy to Bob tomorrow am when you get in. He gets in around 730/745.")
  strzok_to_page(child_file, "2017-06-06T01:48:20-00:00", "Oh Jesus. Really? You get to.talk to aaron?")
  strzok_to_page(child_file, "2017-06-06T01:49:04-00:00", "Marked?\n\nWe get an answer, re --Redacted--?")
  strzok_to_page(child_file, "2017-06-06T01:49:15-00:00", "Guessing yes since they were reading them")
  page_to_strzok(child_file, "2017-06-06T01:49:28-00:00", "Yes marked. Yes to the SC team, no answer yet re --Redacted--.")
  strzok_to_page(child_file, "2017-06-06T01:52:35-00:00", "Sorry i missed it, interested in their thoughts / reaction.\n\nI'll be there at 730 with a copy for him.")
  strzok_to_page(child_file, "2017-06-06T01:52:44-00:00", "They say anything?")

  # Page 479
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-06T01:54:11-00:00", "Not really. Just small timing questions along the way.")
  strzok_to_page(child_file, "2017-06-06T01:56:49-00:00", "You should come meet M with me and --Redacted--")
  page_to_strzok(child_file, "2017-06-06T01:57:52-00:00", "I can't be there that early. And why would I? I am just going to drop them off.")
  strzok_to_page(child_file, "2017-06-06T01:59:09-00:00", "Sit there while he reads. Thats what I'm planning to do.\n\nUntil.he says, thanks, you can go....")
  page_to_strzok(child_file, "2017-06-06T02:00:07-00:00", "He is not going to have you sit there. At best you'll be in your cube waiting for him to finish since they are --Redacted-- and he --Redacted--")
  page_to_strzok(child_file, "2017-06-06T02:00:37-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-06T02:03:52-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-06T02:04:40-00:00", "And ha, I had NO idea about all that DOJ classified space restrictions.\n\nI'm going to have to research that...")
  page_to_strzok(child_file, "2017-06-06T02:12:49-00:00", "Dummy...")
  strzok_to_page(child_file, "2017-06-06T02:22:58-00:00", "We German tourists aren't always that savvy")
  strzok_to_page(child_file, "2017-06-06T02:23:22-00:00", "And who told Andrew about me? You?")
  page_to_strzok(child_file, "2017-06-06T02:39:16-00:00", "A long time ago, so he probably doesn't remember. I'd guess Aaron.")
  strzok_to_page(child_file, "2017-06-06T10:04:22-00:00", "Ok now I'm not happy about the early morning doc delivery. \U0001f62a\U0001f629")
  page_to_strzok(child_file, "2017-06-06T10:06:11-00:00", "Aaron was under the assumption that you are in at 7:45 anyway, did you not tell him that?")
  strzok_to_page(child_file, "2017-06-06T10:17:02-00:00", "That's sometimes aspirational, as you know.\U0001f60b")
  page_to_strzok(child_file, "2017-06-06T10:24:00-00:00", "Ha. So you've got no one to blame but yourself.\U0001f60a")
  strzok_to_page(child_file, "2017-06-06T10:37:05-00:00", "Double\U0001f60b")
  page_to_strzok(child_file, "2017-06-06T11:11:43-00:00", "Hey do you have stuff to discuss at the 9:40 as well? Az seemed to believe it was your meeting.")
  strzok_to_page(child_file, "2017-06-06T11:13:10-00:00", "Ha. Not really but I'll come up with stuff. I said you had some items (which is why I cautioned you last night to save some for today)")
  page_to_strzok(child_file, "2017-06-06T11:14:03-00:00", "I didn't discuss any last night - but he thinks this is a you and he meeting and I had to mention that I would be there too.")
  strzok_to_page(child_file, "2017-06-06T11:15:01-00:00", "I specifically asked for the meeting in the context of you having items to talk about that we didn't get to. I went through my list, and we turn to the things you had, and I said I didn't know many of them, and that we should all sit down and meet.")
  strzok_to_page(child_file, "2017-06-06T11:15:18-00:00", "That's frustrating.")
  
  # Page 480
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-06T11:15:32-00:00", "I'm happy to remind him.")
  page_to_strzok(child_file, "2017-06-06T11:15:42-00:00", "So you're going to have to level set the purpose when we sit down.")
  page_to_strzok(child_file, "2017-06-06T11:15:45-00:00", "Yeah, thanks.")
  strzok_to_page(child_file, "2017-06-06T11:16:33-00:00", "I will. One of the items is, legitimately, how to approach Andy about the people that Bob is going to want a sign to the team. That discussion has to occur before I go making any calls. Maybe we can strategize about that.")
  page_to_strzok(child_file, "2017-06-06T11:18:54-00:00", "Why do you think Andy is going to care at all? I'm sure you can get whomever you want. Do you mean whether Andy or bowdich should tell the field offices first?")
  page_to_strzok(child_file, "2017-06-06T11:19:19-00:00", "And I think bowdich can make the calls to angry sacs. It certainly doesn't need to be andy.")
  strzok_to_page(child_file, "2017-06-06T11:20:54-00:00", "All of those issues. Bowdich hasn't been part of the conversations but absolutely. Bob tells Andy, Andy tells Dave make it happen.")
  page_to_strzok(child_file, "2017-06-06T11:23:53-00:00", "That's how I think think should go.")
  strzok_to_page(child_file, "2017-06-06T11:27:56-00:00", "OGCs gotta get done whatever work they need to do to satisfy everyone at HQ. I want to start calling people this week to tell them to plan on reporting on the 23rd")
  strzok_to_page(child_file, "2017-06-06T12:40:36-00:00", "Dropped off --Redacted-- with Bob. Good. (Btw, --Redacted-- was already here at 745)\n\nHe closed the door to read. \U0001f612\n\nWent and discussed --Redacted-- and access and strategy with --Redacted-- and --Redacted-- Good\n\nAaron came in, then Bob pulled everyone but me into his morning meeting. \U0001f612\n\nBefore closing the door, he said he'd get with me in a bit; I asked him if that meant he wanted me to sit tight. He said yes. So I'm at my cube.")
  page_to_strzok(child_file, "2017-06-06T12:57:57-00:00", "How exceptionally irritating.")
  strzok_to_page(child_file, "2017-06-06T12:58:25-00:00", "Yep.\n\nStill waiting.")
  page_to_strzok(child_file, "2017-06-06T12:58:49-00:00", "Aaron and --Redacted-- have a call with me and --Redacted-- at 9, so it has to end soon.")
  strzok_to_page(child_file, "2017-06-06T12:59:12-00:00", "'Cause Murphys law, the minute I call.you, he'll free up")
  page_to_strzok(child_file, "2017-06-06T12:59:13-00:00", "No I got here at 8. Been in with Rybicki and --Redacted--")
  strzok_to_page(child_file, "2017-06-06T12:59:26-00:00", "Oh.")
  strzok_to_page(child_file, "2017-06-06T13:00:27-00:00", "Any consensus opinion about --Redacted--? I told --Redacted-- and --Redacted-- they had to give a heads up about what you me and --Redacted-- were doing.")
  page_to_strzok(child_file, "2017-06-06T13:02:14-00:00", "What do you mean consensus opinion?")
  page_to_strzok(child_file, "2017-06-06T13:02:31-00:00", "I'm not following this text at all.")

  # Page 481
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-06T13:02:48-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-06T13:03:14-00:00", "--Redacted-- a jerk ;)")
  strzok_to_page(child_file, "2017-06-06T13:04:44-00:00", "Will explain when I see you. Too much for here")
  page_to_strzok(child_file, "2017-06-06T13:08:17-00:00", "I'll meet you at 930?")
  page_to_strzok(child_file, "2017-06-06T13:08:29-00:00", "In hq?")
  strzok_to_page(child_file, "2017-06-06T13:08:59-00:00", "Yep. If I'm done with Bob. They're still behind closed doors.")
  page_to_strzok(child_file, "2017-06-06T13:09:20-00:00", "They are going to be on this call until 930")
  strzok_to_page(child_file, "2017-06-06T13:11:11-00:00", "Oh. Didn't realize that's what they're doing. So should I just head back?")
  strzok_to_page(child_file, "2017-06-06T13:11:34-00:00", "I kind of want to send th message I'm not able to just sit around for an hour")
  page_to_strzok(child_file, "2017-06-06T13:11:45-00:00", "I think so.")
  page_to_strzok(child_file, "2017-06-06T13:11:59-00:00", "You've got a mtg with az at 940, over here.")
  m = strzok_to_page(child_file, "2017-06-06T13:15:09-00:00", "Yep. F^ck it, told his EA I had a 930 at hq and I would find him later.\n\n--Redacted--")
  m.addnote("EA - Executive Assistant")
  strzok_to_page(child_file, "2017-06-06T13:18:03-00:00", "Done. Come to your office or mine?")
  page_to_strzok(child_file, "2017-06-06T13:19:04-00:00", "Not sure. --Redacted--")
  strzok_to_page(child_file, "2017-06-06T13:22:05-00:00", "Ok I'll just go to my office and start. I thought mtg with Aaron was 945")
  strzok_to_page(child_file, "2017-06-06T13:22:17-00:00", "Your meeting on track to end by 930?")
  page_to_strzok(child_file, "2017-06-06T13:22:34-00:00", "We are, for now. But who the f knows.")
  strzok_to_page(child_file, "2017-06-06T13:22:52-00:00", "You in your office with Stephen?")
  page_to_strzok(child_file, "2017-06-06T13:23:08-00:00", "In Stephen's ofc.")
  strzok_to_page(child_file, "2017-06-06T13:23:51-00:00", "Ok. Food just got done. I'll just go to my office.")
  page_to_strzok(child_file, "2017-06-06T16:44:21-00:00", "Hey call when you are off")
  strzok_to_page(child_file, "2017-06-06T17:03:03-00:00", "Sc --Redacted-- mentioned it when Bill was there, but not the name. That only went to Carl.\U0001f612")
  page_to_strzok(child_file, "2017-06-06T22:04:42-00:00", "For you and aaron.")
  strzok_to_page(child_file, "2017-06-06T22:05:27-00:00", "Yep he'd on the phone right now, want me to call when he's off?")
  page_to_strzok(child_file, "2017-06-06T22:05:43-00:00", "Can you step out and call m")

  # Page 482
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-06T22:05:48-00:00", "Or I can just ask it if you want to send")
  strzok_to_page(child_file, "2017-06-06T22:05:56-00:00", "Y")
  strzok_to_page(child_file, "2017-06-06T22:36:47-00:00", "Sigh. Still waiting to talk to Aaron....")
  page_to_strzok(child_file, "2017-06-06T22:37:41-00:00", "Yeah, I'm about to leave. I'll touch base with Andy tomorrow. Whatevs.")
  strzok_to_page(child_file, "2017-06-06T22:38:33-00:00", "Funny I'm right there with you.\n\nYou discuss working with Andrew with him?")
  strzok_to_page(child_file, "2017-06-06T22:39:07-00:00", "Thanks, btw, for shagging that stuff for me with --Redacted--)")
  page_to_strzok(child_file, "2017-06-06T22:39:50-00:00", "Yeah, though baker doesn't think that's the best place to land.")
  strzok_to_page(child_file, "2017-06-06T22:40:50-00:00", "Why? A specific case vs generalist idea? Or Andrew/that case?")
  strzok_to_page(child_file, "2017-06-06T22:41:34-00:00", "Aaron just told Dreeban we've set up a --Redacted--")
  page_to_strzok(child_file, "2017-06-06T22:42:15-00:00", "Sure whatever.")
  page_to_strzok(child_file, "2017-06-06T22:42:35-00:00", "More just that case. Just going to be a bunch of --Redacted-- etc.")
  strzok_to_page(child_file, "2017-06-06T22:46:07-00:00", "That's true re case. I think --Redacted-- is the place for you.")
  strzok_to_page(child_file, "2017-06-06T22:47:34-00:00", "I think --Redacted-- is smack square in your wheelhouse.")
  page_to_strzok(child_file, "2017-06-06T22:50:12-00:00", "You're going to follow up with --Redacted-- re sf86 restrictions on use, yes?")
  strzok_to_page(child_file, "2017-06-06T22:53:43-00:00", "Yes. She just emailed that --Redacted-- was not aware of any restriction other than before affirmative use we seek OPM approval since they own the info.")
  strzok_to_page(child_file, "2017-06-06T22:54:51-00:00", "And give JB credit, he's going through personnel issues and reach back into CD and FBI and the rest of it.\n\n(And i suspect I owe you some thanks for that \U0001f60a)")
  strzok_to_page(child_file, "2017-06-06T23:04:17-00:00", "And JB I think gave you a plug at the end")
  page_to_strzok(child_file, "2017-06-06T23:05:07-00:00", "Not following")
  page_to_strzok(child_file, "2017-06-06T23:08:47-00:00", "A plug for what? And to whom?")
  strzok_to_page(child_file, "2017-06-06T23:11:22-00:00", "A plug by JB about you to Aaron")
  page_to_strzok(child_file, "2017-06-06T23:17:14-00:00", "Oh. I didn't realize that personnel convo was with aaron, not just you. What's he say?")
  strzok_to_page(child_file, "2017-06-06T23:23:29-00:00", "Oh it was just JB and Aaron. I only heard part of Aaron's side")
  page_to_strzok(child_file, "2017-06-06T23:28:36-00:00", "Ah.")
  strzok_to_page(child_file, "2017-06-06T23:42:48-00:00", "Just Td you up for 702 education for the team (is it a problem/litigation issue, do we need to avoid searching against it, etc)")
  
  # Page 483
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-06T23:43:42-00:00", "--Redacted-- might also be smart on the issue.")
  page_to_strzok(child_file, "2017-06-06T23:48:49-00:00", "How do you know baker was talking about me?")
  strzok_to_page(child_file, "2017-06-06T23:52:53-00:00", "Too long to explain here. Conco had turned to --Redacted-- if things. Aaron mentioned thoughts and structure of something I had described. A couple of things were said,, and the convo was wrapping up, then Aaron said she IS good or something to that effect. Just my gut.")
  page_to_strzok(child_file, "2017-06-07T00:16:46-00:00", "Oh geez, dreeben is going to explain --Redacted-- than any human on the planet.")
  strzok_to_page(child_file, "2017-06-07T00:18:21-00:00", "A word missing \"better\"?")
  strzok_to_page(child_file, "2017-06-07T00:26:36-00:00", "Finally leaving. I hope you're not still at work....")
  page_to_strzok(child_file, "2017-06-07T00:27:16-00:00", "Nope. I left at 7. Of course I ran tino --Redacted-- when he was leaving. At 5:30.")
  strzok_to_page(child_file, "2017-06-07T02:31:24-00:00", "--Redacted-- \U0001f60a\U0001f60a\nC) I have no idea who the two agents are --Redacted-- asked for. They're not associated with the team and I may need to say \"no.\" I'll do research and talk with her but I worry they're NY, in the same way Andrew worried about NY agents. And he had the sense to talk to me about what he wanted, and balance his request against those already on the team.\nD) curious comment Andrew made as I stepped out, prompting your 20 year agent comment. My sense was he wasn't necessarily happy.")
  page_to_strzok(child_file, "2017-06-07T09:59:50-00:00", "--Redacted-- C) So just sit down and talk to her honestly about it. It's okay to say no, especially since that subject NEEDS a strong CI look as well.\nD) Jesus, relax about the comment. Andrew had been making fun of himself, you stepped out to make a call, Andrew said on no, I've scared him. I said you're a 20 year agent, you're fine. It was all a joke. That's it.")
  page_to_strzok(child_file, "2017-06-07T10:43:06-00:00", "C) Been thinking. Let me prep the battlefield with --Redacted-- first, like I did with Andrew.")
  page_to_strzok(child_file, "2017-06-07T10:43:42-00:00", "Who you are, why she can trust you, considerations to think about.")
  # page_to_strzok(child_file, "2017-06-07T10:44:26-00:00", "And jesus, did you see that the networks are carrying Comey's testimony? Interrupting regular tv to broadcast...")
  strzok_to_page(child_file, "2017-06-07T10:45:07-00:00", "C) it's fine. I can do it - you and I have essentially the same relationship with her whereas you know Andrew much much better.")
  strzok_to_page(child_file, "2017-06-07T10:45:57-00:00", "I was going to find her early and talk, truly, I'm not worried nor do I think it will be adversarial in the least. If you have personal reasons for you and team to do it, that's a different story.")

  # Page 484
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-07T10:46:52-00:00", "It's truly going to be \"the most watched Washington event since Watergate.\"\n\nWhere are we watching (yes damn right I'm watching with you)")
  page_to_strzok(child_file, "2017-06-07T10:47:54-00:00", "I would just prefer to, gives me a reason to pop in and say hi too.")
  page_to_strzok(child_file, "2017-06-07T10:48:34-00:00", "I think I'm watching with --Redacted-- just quietly in --Redacted-- office.")
  strzok_to_page(child_file, "2017-06-07T10:49:28-00:00", "My reluctance is I want her to see me as the lead - I appreciate you doing it with Andrew since he's close to.you, but I with her I guess I'd rather just directly have the conversation. Let's talk")
  strzok_to_page(child_file, "2017-06-07T10:49:51-00:00", "--Redacted-- invited everyone to the D's conference room. Is --Redacted-- not going to be there?")
  page_to_strzok(child_file, "2017-06-07T10:51:32-00:00", "No --Redacted-- didn't. That is for today - Andy's hearing.")
  strzok_to_page(child_file, "2017-06-07T10:52:20-00:00", "Oh")
  page_to_strzok(child_file, "2017-06-07T10:52:22-00:00", "No one is going to mistake me for you as the lead, but that's fine.")
  strzok_to_page(child_file, "2017-06-07T10:54:06-00:00", "I just have had email back and forth with her about it, as well as with Aaron and the team on staffing, I don't want her to suddenly think I'm inserting a proxy before we actually just sit down and talk. Truly, I think I'd prefer to talk to her if that's ok.")
  # strzok_to_page(child_file, "2017-06-07T10:55:27-00:00", "And I've gotta say I'm a little bummed abour Dir C testimony. Is what it is.")
  # page_to_strzok(child_file, "2017-06-07T10:56:24-00:00", "Yup, it's fine.")
  page_to_strzok(child_file, "2017-06-07T10:57:12-00:00", "They don't want to make it a big scene viewing, which I get, but would be understood. So --Redacted-- and I had already discussed.")
  m = strzok_to_page(child_file, "2017-06-07T11:31:51-00:00", "I get, re --Redacted-- it's going to be emotional for all of us.\n\nI'm disappointed because i see a solid, unbroken line from mye to announcement to --Redacted-- to election to momentous this --Redacted--")
  m.addnote("mye - Midyear Exam (Hillary Clinton)")
  page_to_strzok(child_file, "2017-06-07T11:34:56-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-07T11:35:19-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-07T11:54:32-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-07T11:55:36-00:00", "50 work things to tell you. --Redacted-- need to tell you back story")
  page_to_strzok(child_file, "2017-06-07T11:57:37-00:00", "I'm in the car if you want to talk.")
  strzok_to_page(child_file, "2017-06-07T12:01:27-00:00", "Wait 1")
  strzok_to_page(child_file, "2017-06-07T12:57:11-00:00", "Hey can you bring extra copies of the spreadsheet I printed for you? Thanks")

  # Page 485
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-07T16:50:41-00:00", "Are yoy close or still waiting to link up with --Redacted-- If you are, i don't want to be a jerk and I'll wait. If not, I'm just going to head over.")
  page_to_strzok(child_file, "2017-06-07T16:56:40-00:00", "We're not going over.")
  strzok_to_page(child_file, "2017-06-07T16:57:07-00:00", "Ok. You need me to do anything for you?")
  strzok_to_page(child_file, "2017-06-07T16:57:21-00:00", "(over there I mean)?")
  strzok_to_page(child_file, "2017-06-07T16:58:09-00:00", "Well actually wherever but you get my point.")
  strzok_to_page(child_file, "2017-06-07T16:59:54-00:00", "Great. My cube has literally 9 chairs in it now.\U0001f612")
  strzok_to_page(child_file, "2017-06-07T17:00:55-00:00", "Is --Redacted-- cool with me? I know that wasn't the subject of --Redacted-- stay behind (at least I certainly hope it wasnt), just was getting a really weird vibe from --Redacted--")
  strzok_to_page(child_file, "2017-06-07T17:18:05-00:00", "Oh good. --Redacted-- really hard to read sometimes. This isn't me wanting everyone to like me (though obviously I do) - I just like and respect --Redacted-- a lot.")
  strzok_to_page(child_file, "2017-06-07T17:19:47-00:00", "Also - not for --Redacted-- talking about engaging and (at least trying to) doing interviews soon along the lines of what we discussed earlier. I think --Redacted-- is going to take on --Redacted-- until they find someone.")
  page_to_strzok(child_file, "2017-06-07T17:20:42-00:00", "Try to see if I am on that one, since I have no idea. \U0001f612")
  strzok_to_page(child_file, "2017-06-07T17:23:04-00:00", "I know, Lis, I know. It's super frustrating.\n\nCan you come over and just start hanging out? You need to just be here for the, hey, you, can you run this down for me/let me do that for yous.")
  page_to_strzok(child_file, "2017-06-07T17:27:41-00:00", "Sure, I just don't have anything that I can really do over there.")
  # strzok_to_page(child_file, "2017-06-07T17:31:14-00:00", "Aaron would like you and --Redacted-- to explore --Redacted-- along the lines we discussed on that one answer")
  page_to_strzok(child_file, "2017-06-07T17:31:39-00:00", "Yeah I really think we need to.")
  strzok_to_page(child_file, "2017-06-07T17:31:48-00:00", "Aaron asked me to ask you and --Redacted-- to take the lead on drafting something and then discuss it.")
  strzok_to_page(child_file, "2017-06-07T17:32:04-00:00", "So see, yay, something for you to do. :)")
  page_to_strzok(child_file, "2017-06-07T17:32:14-00:00", "Yeah, amazing.")
  strzok_to_page(child_file, "2017-06-07T17:32:25-00:00", "--Redacted-- talking to Aaron now")
  page_to_strzok(child_file, "2017-06-07T17:32:42-00:00", "Yeah, I'm in here. What mtg is he going to?")
  strzok_to_page(child_file, "2017-06-07T17:32:45-00:00", "Something about --Redacted-- but I'll try and listen in to the follow on")
  strzok_to_page(child_file, "2017-06-07T20:18:03-00:00", "Where are --Redacted-- physically now?")

  # Page 486
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-07T20:31:49-00:00", "Which ones? --Redacted-- to the best of my understanding.")
  strzok_to_page(child_file, "2017-06-07T20:34:57-00:00", "Yes. Ok, that's what Paul just briefed. I wasn't sure if the move to --Redacted-- office was imminent/going to happen.\n\nThey reaffirmed we ultimately need to get them --Redacted--\n\nThanks")
  page_to_strzok(child_file, "2017-06-07T20:42:06-00:00", "There is no move to --Redacted-- ofc. Just can't be --Redacted-- without his approval.")
  strzok_to_page(child_file, "2017-06-07T20:45:58-00:00", "Oh. Perfectm")
  strzok_to_page(child_file, "2017-06-07T21:01:39-00:00", "You coming over here at all?")
  page_to_strzok(child_file, "2017-06-07T21:01:56-00:00", "Should I?")
  strzok_to_page(child_file, "2017-06-07T21:05:46-00:00", "Unless you've got something going, I would. We're starting obstruction team brief but just come. Sit in on whatever comes next.")
  page_to_strzok(child_file, "2017-06-07T21:06:57-00:00", "Who is in it?")
  strzok_to_page(child_file, "2017-06-07T21:08:32-00:00", "Don't then.")
  strzok_to_page(child_file, "2017-06-07T21:09:21-00:00", "I'm just saying, come over here and stick your head in. I've gotten more the past couple of days after hours talking wiht Aaron and --Redacted-- then all day the past week and a half")
  strzok_to_page(child_file, "2017-06-07T21:09:36-00:00", "Was not suggesting it for any particular reason, just a dive in sort of thing")
  strzok_to_page(child_file, "2017-06-07T21:10:02-00:00", "If you have work to do, I'd say do it.")
  page_to_strzok(child_file, "2017-06-07T23:06:11-00:00", "I left. F it. There's no amount of time I can spend and finish everything. Whatevs")
  strzok_to_page(child_file, "2017-06-07T23:22:12-00:00", "Hi. I know. I'm sorry. :(")
  strzok_to_page(child_file, "2017-06-08T09:50:10-00:00", "Dir C's gotta have some nervous anticipation")
  strzok_to_page(child_file, "2017-06-08T10:45:20-00:00", "Hey does his testimony actually start at 10 or 1030?")
  page_to_strzok(child_file, "2017-06-08T10:45:52-00:00", "10")
  strzok_to_page(child_file, "2017-06-08T10:50:24-00:00", "You ok? The trained investigator in me notes the sum total of four words this morning. Still feeling unmoored?")
  page_to_strzok(child_file, "2017-06-08T10:58:02-00:00", "Yup. Super busy but with unclear purpose. It's the best.")
  strzok_to_page(child_file, "2017-06-08T11:18:15-00:00", "I'm firmly in the --Redacted-- camp. Pete's take, pulling from my Army days: embrace the suck.\n\nOrder will emerge, and specifically for you. You're too good, too energetic, too competent.\n\nJust BE YOU. And trust. Yourself. The righteousness of all this.\n\nIt will be OK. I pinky promise. Which is the opposite of tough guy army sayings. I'm comples that way ;)")
  
  # Page 487
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-08T12:02:02-00:00", "Yay. Got a commitment from --Redacted-- He was a great case agent on my squad.")
  strzok_to_page(child_file, "2017-06-08T12:52:36-00:00", "And I'm sitting outside the closed door waiting to get 2 minutes before they all have their various 9:00s...\U0001f612")
  page_to_strzok(child_file, "2017-06-08T12:53:00-00:00", "Nice.")
  page_to_strzok(child_file, "2017-06-08T12:53:35-00:00", "Baker just told me about what Rybicki told you. You're going to mention to Aaron, right?")
  strzok_to_page(child_file, "2017-06-08T12:54:16-00:00", "Yeah I'm feeling great about it.\n\nYes, it's one of the reasons I'm waiting, cabana-boy style. \U0001f612\U0001f612\U0001f612")
  strzok_to_page(child_file, "2017-06-08T12:54:42-00:00", "You get my vm?")
  strzok_to_page(child_file, "2017-06-08T13:06:40-00:00", "And I'm still waiting \U0001f621")
  strzok_to_page(child_file, "2017-06-08T18:05:50-00:00", "I assume there's nothing operational/I don't need to be on the call?")
  strzok_to_page(child_file, "2017-06-08T18:06:06-00:00", "Because, again, who knows...")
  page_to_strzok(child_file, "2017-06-08T18:06:39-00:00", "Oh, don't worry. I'm not even on speaker. \U0001f612")
  strzok_to_page(child_file, "2017-06-08T18:07:36-00:00", "What?!?\U0001f61e\n\nGod I want to keep telling you to hang in there but it's hard....")
  strzok_to_page(child_file, "2017-06-08T18:08:01-00:00", "Nevertheless.\n\nHang in there.\n\nYour country needs you.")
  page_to_strzok(child_file, "2017-06-08T18:09:14-00:00", "Nope. Sent me an email yesterday about the call bc it deals with his --Redacted-- but here I am.")
  page_to_strzok(child_file, "2017-06-08T18:09:32-00:00", "Oh boy. Nope, you boys are going to need to --Redacted-- soon...")
  page_to_strzok(child_file, "2017-06-08T18:09:37-00:00", "!!!!!")
  strzok_to_page(child_file, "2017-06-08T18:10:04-00:00", "Should I come in?")
  m = strzok_to_page(child_file, "2017-06-09T00:06:08-00:00", "Pls clr imsg.\n\nThanks for staying for personnel discussion.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2017-06-09T00:35:03-00:00", "You up for a convo about --Redacted--?")
  strzok_to_page(child_file, "2017-06-09T01:24:29-00:00", "Just got done talking to --Redacted-- Gosh I've been blessed to have worked with great agents.\n\nThank you for reminding me all those times that I wouldn't trade what I've done for a different path.\U0001f636\n\nI don't always deserve the goodness that I have.")
  #page_to_strzok(child_file, "2017-06-09T01:56:52-00:00", "Great --Redacted-- just called me to say that Rachel Maddow just listed by name each of the people the Director listed a having discussed the matter with, but she that I was the only one they hadn't identified yet but that they were working on it.\U0001f612")
  # https://www.msnbc.com/transcripts/rachel-maddow-show/2017-06-08-msna1001331
  # https://www.msnbc.com/transcripts/rachel-maddow-show/2017-06-09-msna1001336
  strzok_to_page(child_file, "2017-06-09T01:58:59-00:00", "Oh crap")

  # Page 488
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-09T01:59:02-00:00", "Won't take long.")
  strzok_to_page(child_file, "2017-06-09T01:59:10-00:00", "Welcome to the club.\U0001f612")
  strzok_to_page(child_file, "2017-06-09T02:00:54-00:00", "What's the immediate impact? Things i worried were, in order:\n1) crazies\n2) enemies lists\n3) subpoenas\n4) frivolous lawsuits/foias\n\nFrankly, though, I wouldn't worry TOO much about it.")
  strzok_to_page(child_file, "2017-06-09T02:01:17-00:00", "And you know --Redacted-- and --Redacted-- know. But they might be cool enough not to run your name.")
  strzok_to_page(child_file, "2017-06-09T02:01:26-00:00", "How are you feeling about it?")
  # strzok_to_page(child_file, "2017-06-09T02:02:15-00:00", "And we do need to discuss your role in --Redacted-- Not sure if I'm overthinking that.")
  strzok_to_page(child_file, "2017-06-09T02:02:59-00:00", "And \U0001f60a something for --Redacted-- to.brag about and to be proud of in a couple of generations.")
  # page_to_strzok(child_file, "2017-06-09T02:04:49-00:00", "I don't think I know a lot of enemies/crazies. Well, there is one.")
  page_to_strzok(child_file, "2017-06-09T02:05:31-00:00", "I'm sure they won't hesitate to out me. They outed --Redacted--")
  strzok_to_page(child_file, "2017-06-09T02:07:24-00:00", "Who's the one?")
  strzok_to_page(child_file, "2017-06-09T02:07:37-00:00", "Who's --Redacted--?")
  page_to_strzok(child_file, "2017-06-09T02:07:51-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-09T02:08:05-00:00", "You should be able to figure that out. \U0001f612")
  strzok_to_page(child_file, "2017-06-09T02:10:10-00:00", "A) they did? I didn't know that\nB) ah. Got it. \U0001f614")
  strzok_to_page(child_file, "2017-06-09T02:10:54-00:00", "So how you feeling about it? Hopefully not too worried?")
  page_to_strzok(child_file, "2017-06-09T02:15:20-00:00", "Not happy about it, but obviously nothing I can do about it.")
  page_to_strzok(child_file, "2017-06-09T02:17:45-00:00", "Alright, I'm going --Redacted--")
  strzok_to_page(child_file, "2017-06-09T02:19:22-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-09T02:20:02-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-09T06:53:10-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-09T06:57:35-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-09T09:55:12-00:00", "--Redacted--\n\nGotta talk at all hands at 10 then at Agency at 1. Neither have anything to do with SC. Doing too many things poorly. Life is great.")
  page_to_strzok(child_file, "2017-06-09T10:07:56-00:00", "You should stay for the dull all hands. Sends a better message.")

  # Page 489
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-09T10:12:21-00:00", "Yeah I guess.")
  strzok_to_page(child_file, "2017-06-09T10:12:57-00:00", "Didn't see your name in any news feeds. Hopefully they let it go. Who knows.")
  m = strzok_to_page(child_file, "2017-06-09T10:21:40-00:00", "Imsg?")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  page_to_strzok(child_file, "2017-06-09T10:26:44-00:00", "Go ahead")
  m = strzok_to_page(child_file, "2017-06-09T12:12:29-00:00", "Still ok to imsg, or call?")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  m = page_to_strzok(child_file, "2017-06-09T12:30:40-00:00", "You can imsg.")
  m.addnote("imsg - Strzok/Page had private iPhones to communicate without leaving evidence")
  strzok_to_page(child_file, "2017-06-09T12:34:53-00:00", "Crap of course I didn't bring that phone. Nothing urgent. Just a convo with Bill, his feelings, and my general sense of this feeling of unease permeating a lot more broadly than I was thinking about.")
  strzok_to_page(child_file, "2017-06-09T12:42:25-00:00", "And my kick in the nuts rush for 2 minutes with Aaron and --Redacted-- to bring up things with Mueller before they walk in and shut the door. \U0001f612\U0001f612\U0001f612\U0001f612")
  strzok_to_page(child_file, "2017-06-09T15:38:37-00:00", "Hi. Got a sec.")
  page_to_strzok(child_file, "2017-06-09T15:44:12-00:00", "I'm walking out of SC now. Stand by.")
  strzok_to_page(child_file, "2017-06-09T16:39:17-00:00", "No --Redacted-- today")
  strzok_to_page(child_file, "2017-06-09T17:29:30-00:00", "Just got an Agency coin")
  strzok_to_page(child_file, "2017-06-09T17:29:30-00:00", "With Brennan's signature;)")
  strzok_to_page(child_file, "2017-06-09T18:11:59-00:00", "Hi. You go to R?")
  strzok_to_page(child_file, "2017-06-09T20:40:13-00:00", "This is what I'm talking about! Divide and conquer. And c'mon --Redacted-- wtf.")
  strzok_to_page(child_file, "2017-06-09T20:52:11-00:00", "Btw, we still haven't talked....He's outside swapping cars")
  strzok_to_page(child_file, "2017-06-09T22:06:13-00:00", "And --Redacted-- just ran out like Cinderella about to hit midnight...")
  strzok_to_page(child_file, "2017-06-09T23:43:44-00:00", "Just leaving. This won't end well.")
  page_to_strzok(child_file, "2017-06-10T00:07:39-00:00", "What won't, your participation? And why so late, just when he finally made time? Was Bob still there? I seem to remember that Andy was going to some black tie affair honoring Mueller tonight...")
  strzok_to_page(child_file, "2017-06-10T00:14:21-00:00", "Oh god.")
  strzok_to_page(child_file, "2017-06-10T03:34:05-00:00", "Hey")
  page_to_strzok(child_file, "2017-06-10T15:49:47-00:00", "I didn't you last comment about what he was angry about. Just hit me up there when you can.")

  # Page 490
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-10T15:53:19-00:00", "Finally, I don't like not including that one person. He is NOT recused, Bill should not be making that call for him. He can make that decision himself. He always takes a conservative approach and can be trusted to do the right thing.")
  page_to_strzok(child_file, "2017-06-10T18:39:09-00:00", "I'll call you back later.")
  page_to_strzok(child_file, "2017-06-10T18:39:28-00:00", "On a call, I'll call you back.")
  strzok_to_page(child_file, "2017-06-10T19:09:01-00:00", "Still talking?\U0001f636\n\nI'm still waiting for Aaron....")
  page_to_strzok(child_file, "2017-06-10T19:12:55-00:00", "Yes, I called Trisha, just to chat.")
  strzok_to_page(child_file, "2017-06-10T19:13:50-00:00", "God she cant get back soon enough...I hope she doesn't run off with the rest of the mass exodus....")
  page_to_strzok(child_file, "2017-06-10T19:19:14-00:00", "Okay, I'm off.")
  strzok_to_page(child_file, "2017-06-10T19:32:57-00:00", "Talking to Aaron and --Redacted--")
  strzok_to_page(child_file, "2017-06-10T19:33:35-00:00", "Will call you then Bill")
  strzok_to_page(child_file, "2017-06-11T02:48:23-00:00", "I sent a dial in for tomorrow. We have to talk to him first.")
  m = strzok_to_page(child_file, "2017-06-11T02:48:51-00:00", "Given the publicity, I don't think we can get ssci to change dates.")
  m.addnote("ssci - Senate Select Committee on Intelligence" )
  strzok_to_page(child_file, "2017-06-11T02:49:11-00:00", "Hi hi hi")
  page_to_strzok(child_file, "2017-06-11T02:50:40-00:00", "Is his open or closed?")
  strzok_to_page(child_file, "2017-06-11T02:51:01-00:00", "I couldn't tell from reporting")
  m = strzok_to_page(child_file, "2017-06-11T17:50:55-00:00", "Eras work?")
  m.addnote("Eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2017-06-11T18:15:49-00:00", "Trying it now.")
  page_to_strzok(child_file, "2017-06-11T18:16:29-00:00", "Honestly I think it is a waste of --Redacted-- talents to bring him to the team...")
  page_to_strzok(child_file, "2017-06-11T18:21:47-00:00", "First attempt was a failure. :(")
  page_to_strzok(child_file, "2017-06-11T18:22:14-00:00", "On the very first screen, the bitlocker, what are you supposed to enter?")
  page_to_strzok(child_file, "2017-06-11T18:38:07-00:00", "Officially didn't work. \U0001f621 I'm going in in an hour. \U0001f620\U0001f620\U0001f620\U0001f620\U0001f620\U0001f620\U0001f620\U0001f620")
  strzok_to_page(child_file, "2017-06-11T19:42:54-00:00", "I'm sorry")
  strzok_to_page(child_file, "2017-06-11T19:43:50-00:00", "I think so too, re --Redacted-- I'm going to talk to him anyway")
  m = strzok_to_page(child_file, "2017-06-11T19:44:40-00:00", "Sorry about the eras. Couldn't tell you what the steps are, it's been that long...")
  m.addnote("eras - Enterprise Remote Access System")
  page_to_strzok(child_file, "2017-06-11T19:46:27-00:00", "Yeah well I'm driving in now...")

  # Page 491
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-11T19:50:15-00:00", "I'm sorry. That sucks. Im trying to reach Aaron about --Redacted-- because we suck and won't have an answer until tomorrow.")
  strzok_to_page(child_file, "2017-06-11T20:37:54-00:00", "Just talked to Bill, who had talked with Carl. Bill *thinks* Carl has spoken with Andy. Bill and --Redacted-- are going to make the call to --Redacted-- tomorrow then figure out how to get the material and see what's on there.\n\nNow going to go track down Aaron...")
  strzok_to_page(child_file, "2017-06-11T20:58:22-00:00", "Bill mentioned EADs and above are gone tomorrow at some leadership retreat \U0001f612. You going to talk to Andy?")
  strzok_to_page(child_file, "2017-06-11T20:59:14-00:00", "Frankly gotta say I'm curious what's been relayed to him...")
  page_to_strzok(child_file, "2017-06-11T21:03:44-00:00", "He is going too. But yes, I'll try to talk to him before hand.")
  strzok_to_page(child_file, "2017-06-11T21:28:43-00:00", "We need to get Baker to do some award presentation for --Redacted--")
  page_to_strzok(child_file, "2017-06-11T21:29:03-00:00", "I agree.")
  page_to_strzok(child_file, "2017-06-11T21:29:35-00:00", "Have five things I don't have the figures for. Maybe I'll come back tonight...")
  page_to_strzok(child_file, "2017-06-11T21:36:49-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-11T21:43:51-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-12T10:37:49-00:00", "--Redacted-- I hope the meeting between Aaron and Carl resolves some of my uncertainty/stress.")
  page_to_strzok(child_file, "2017-06-12T10:42:48-00:00", "You shouldn't stay on, regardless of what happens.")
  strzok_to_page(child_file, "2017-06-12T10:44:17-00:00", "You're right, of course.\n\nWhat are you thinking about you? No change?")
  page_to_strzok(child_file, "2017-06-12T11:26:39-00:00", "I'm serious about you. Imagine the scene, head held high at the 30 day mark, just a string handshake and a good luck. As opposed to a \"can I pretty please sit in on these meetings?\" F it Pete. You can do better than this.")
  strzok_to_page(child_file, "2017-06-12T11:27:23-00:00", "I know. \U0001f614")
  strzok_to_page(child_file, "2017-06-12T11:30:08-00:00", "Had the same thought when you sent me --Redacted-- I don't want a significant portion of my time spent tracking down stuff that should have been sent, or included, or invited, on behalf of the investigators.")
  page_to_strzok(child_file, "2017-06-12T11:53:46-00:00", "Exactly. I honestly think it is an easy decision, regardless of what comes next at Fbi.")
  strzok_to_page(child_file, "2017-06-12T12:07:37-00:00", "I'm grumpy")
  page_to_strzok(child_file, "2017-06-12T12:12:29-00:00", "Yup, join the club.")
  strzok_to_page(child_file, "2017-06-12T12:23:50-00:00", "I am starting to hedge off of my certainly that you should go....")
  page_to_strzok(child_file, "2017-06-12T12:26:27-00:00", "Yeah but I don't have great options. Maybe I can do this for a year...")

  # Page 492
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-12T12:36:54-00:00", "Just talked to --Redacted-- called --Redacted-- yesterday, he was having a call with Dave and Carl later about --Redacted-- so someone clearly decided to include him, which is good.\n\n--Redacted-- hasn't talked to him since, which isn't great, particularly with a call with --Redacted-- in 55 minutes. 7th floor in a vacuum....")
  strzok_to_page(child_file, "2017-06-12T22:19:41-00:00", "Hi sorry just saw this. In --Redacted-- office with --Redacted-- Aaron walked in about 5 ago.")
  strzok_to_page(child_file, "2017-06-12T22:24:27-00:00", "And Jesus god --Redacted-- is not concise")
  page_to_strzok(child_file, "2017-06-12T22:28:12-00:00", "Yeah, well --Redacted-- kicked me out of the recap he was giving for Mueller and --Redacted--")
  page_to_strzok(child_file, "2017-06-12T22:28:33-00:00", "That's what I was coming to say. And I'll tell you re your email later.")
  strzok_to_page(child_file, "2017-06-12T22:28:49-00:00", "Jims")
  strzok_to_page(child_file, "2017-06-12T22:28:49-00:00", "Doors open stop by quick")
  strzok_to_page(child_file, "2017-06-13T00:51:31-00:00", "Hey anticipating you may be a bit so I'm going to jet. Give me a call, of course, eager to hear how it went.... :)")
  page_to_strzok(child_file, "2017-06-13T01:09:01-00:00", "Still in with him. Having a very good open convo. Thinking --Redacted-- plus --Redacted-- He's on board, it's others who may not yet be comfortable with the idea.")
  strzok_to_page(child_file, "2017-06-13T01:09:57-00:00", "Excellent! !!\U0001f60a\n\nOthers = --Redacted-- attys?")
  strzok_to_page(child_file, "2017-06-13T01:10:31-00:00", "Aaron's --Redacted-- or Muellers?")
  page_to_strzok(child_file, "2017-06-13T01:10:51-00:00", "It would need to be mueller's to make sense.")
  page_to_strzok(child_file, "2017-06-13T01:10:54-00:00", "Stand by.")
  strzok_to_page(child_file, "2017-06-13T01:11:08-00:00", "Agreed. Is Bob ok with that?")
  strzok_to_page(child_file, "2017-06-13T01:31:52-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-13T01:32:48-00:00", "Sorry. Walking out of SC now, but probably not smart to walk down the street on my phone.")
  strzok_to_page(child_file, "2017-06-13T01:34:36-00:00", "K. --Redacted--")
  page_to_strzok(child_file, "2017-06-13T01:35:29-00:00", "We should talk now then bc I have to go up to the ofc and lock up.")
  strzok_to_page(child_file, "2017-06-13T01:53:32-00:00", "Thinking about it, that was a really good conversation. It shows me that Aaron trusts and respects you. :)")
  page_to_strzok(child_file, "2017-06-13T01:58:48-00:00", "Yeah, I think that's right. At least I hope so.")
  strzok_to_page(child_file, "2017-06-13T02:03:57-00:00", "Oh, for sure. \U0001f60a")
  page_to_strzok(child_file, "2017-06-13T02:04:28-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-13T02:05:43-00:00", "--Redacted--")

  # Page 493
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-13T09:09:44-00:00", "Been up since 345. This is GREAT.\n\nRealized I need an answer from Aaron/Mueller about my role. If I'm not in the --Redacted-- then im out. I'm frustrated that they're talking about all this restructuring and various --Redacted-- for you (or anyone) and I can't, as lead fbi person, get an answer to a question I asked a week ago.")
  page_to_strzok(child_file, "2017-06-13T12:30:57-00:00", "Ah. News just said police activity on constitution ave. Awesome.")
  strzok_to_page(child_file, "2017-06-13T12:32:51-00:00", "Super!\n\nAnd guess what! The 830 started! Without me!\n\nIn mitigation, it's still just bob --Redacted-- Aaron and --Redacted--")
  strzok_to_page(child_file, "2017-06-13T12:43:45-00:00", "And double grumble. I just asked Aaron, hey can I attend Hill prep at 5. Loooong pause. Then, \"OK, I *think* that's fine. It's not going to be what you think it is.\"\n\nHonestly, Lisa. \U0001f612")
  strzok_to_page(child_file, "2017-06-13T12:44:37-00:00", "I'm walking out. I'll wait to order. Just going to enjoy the morning outside before it gets oppressively hot...")
  page_to_strzok(child_file, "2017-06-13T12:45:49-00:00", "I know dude. I don't know what else to say.")
  strzok_to_page(child_file, "2017-06-13T19:26:05-00:00", "Whoops. Misfire. Back. Had a SC feeling he really needed guidance. Which is fine.\n\nDid I miss anything?")
  strzok_to_page(child_file, "2017-06-13T23:50:01-00:00", "Just talked to aaron")
  page_to_strzok(child_file, "2017-06-13T23:50:24-00:00", "What's up? Just got home.")
  strzok_to_page(child_file, "2017-06-13T23:51:06-00:00", "It'll wait. Discussion of --Redacted--")
  strzok_to_page(child_file, "2017-06-13T23:51:36-00:00", "Need to talk to you before you talk to him so you know what I said")
  strzok_to_page(child_file, "2017-06-13T23:52:51-00:00", "(Which was nothing, but we need to coordinate)\n\nHe knows who has them now but not how they got them")
  strzok_to_page(child_file, "2017-06-13T23:53:15-00:00", "My inclination is not to disclose who took them, but I'm not sure about that.")
  page_to_strzok(child_file, "2017-06-13T23:53:35-00:00", "We can talk tomorrow.")
  m = strzok_to_page(child_file, "2017-06-14T00:00:00-00:00", "--Redacted--")
  m.addnote("The TIME was redacted!!!")
  page_to_strzok(child_file, "2017-06-14T01:27:05-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-14T01:40:42-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-14T01:41:15-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-14T01:41:42-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-14T01:42:03-00:00", "--Redacted--")

  # Page 494
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-14T01:50:42-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-14T01:57:46-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-14T17:49:22-00:00", "Hey you still at lunch or SC? Have a sec?")
  page_to_strzok(child_file, "2017-06-14T18:37:20-00:00", "Hey there, sorry. Will be back at my desk in 2.")
  strzok_to_page(child_file, "2017-06-14T18:37:55-00:00", "K I'll swing by. Couple of things before my 3")
  page_to_strzok(child_file, "2017-06-14T18:39:02-00:00", "Just call? Everyone is going to be walking up before the 3")
  strzok_to_page(child_file, "2017-06-14T18:39:22-00:00", "Ok lync")
  page_to_strzok(child_file, "2017-06-14T20:00:21-00:00", "Sorry, I've been over at SC since about 3:15")
  page_to_strzok(child_file, "2017-06-14T20:01:13-00:00", "Definitely had to fight back tears with --Redacted-- almost with Aaron. I just don't know what to do, Pete.")
  strzok_to_page(child_file, "2017-06-14T23:33:08-00:00", "Gmail you something?")
  strzok_to_page(child_file, "2017-06-14T23:35:00-00:00", "Been talking to Bill since we got off the phone. He really thinks insult go, provided I can be I'm the room. I told him about tonight and that I just didn't see that happening.")
  strzok_to_page(child_file, "2017-06-14T23:50:47-00:00", "Nevermind re gmail")
  page_to_strzok(child_file, "2017-06-14T23:54:13-00:00", "And again I return to the fact that you are having an hour long conversation about whether you should go is completely asinine.")
  strzok_to_page(child_file, "2017-06-14T23:54:53-00:00", "You misunderstand. I walked in there in the first thing I said was, I've decided I shouldn't go and don't want to go.")
  strzok_to_page(child_file, "2017-06-14T23:55:10-00:00", "Bill then asked if I wanted to trade with him.")
  strzok_to_page(child_file, "2017-06-15T00:40:11-00:00", "I know.\n\nI just dug the email draft out of deleted items and sent it.")
  page_to_strzok(child_file, "2017-06-15T00:44:00-00:00", "Thanks.\n\nSaw your politico article too. God help me I don't think I can take much more of this.")
  strzok_to_page(child_file, "2017-06-15T00:44:42-00:00", "I know")
  page_to_strzok(child_file, "2017-06-15T11:24:51-00:00", "Hey. See Aaron's email. My guess is that is intended to exclude me, but let's discuss before you say anything.")
  strzok_to_page(child_file, "2017-06-15T11:33:12-00:00", "I didn't see you on the cc line (thanks Samsung\U0001f612) and already told Aaron I would right now. I'll hedge in the wording and say there me be adds/drops.\n\nI'm sure this came about in the discussion I had the door closed in my face \U0001f621")
  # page_to_strzok(child_file, "2017-06-15T11:35:30-00:00", "Or because of the nyt story saying that SC seems to be pursuing potus in light of these interviews.")
  strzok_to_page(child_file, "2017-06-15T11:42:22-00:00", "Wp had it first. And it's as likely to be --Redacted-- leaking. All of which I would have walked through, if I had been in the room. Because, you know, media leaks is what I do for a living.")

  # Page 495
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-15T11:43:32-00:00", "Oh yeah, that's right.")
  page_to_strzok(child_file, "2017-06-15T18:10:53-00:00", "No, doing ethics training. Most everyone us here.")
  page_to_strzok(child_file, "2017-06-15T18:48:23-00:00", "I'm walking out now if you still need to talk.")
  page_to_strzok(child_file, "2017-06-15T18:53:32-00:00", "Never mind . Walking into my next mtg.")
  strzok_to_page(child_file, "2017-06-15T19:01:10-00:00", "Dang sorry was in sioc. Walking back over")
  # strzok_to_page(child_file, "2017-06-15T19:46:48-00:00", "WP picked your name up in an online blog, citing Wired. \"Right Turn,\" 9:15 today")
  # strzok_to_page(child_file, "2017-06-15T19:48:16-00:00", "And you're on Wiki\n\nhttps://en.m.wikipedia.org/wiki/2017_Special_Counsel_for_the_United_States_Department_of_Justice_team")
  strzok_to_page(child_file, "2017-06-15T20:14:16-00:00", "Btw, your iPhone is here")
  page_to_strzok(child_file, "2017-06-15T20:39:59-00:00", "Hey. Walking back now.")
  strzok_to_page(child_file, "2017-06-15T20:40:50-00:00", "K. :)\n\nTalking to --Redacted-- and --Redacted-- but I think we're wrapping up")
  strzok_to_page(child_file, "2017-06-15T20:42:54-00:00", "Good FOIA meeting? :D")
  page_to_strzok(child_file, "2017-06-15T20:43:25-00:00", "FOIA is hell.")
  strzok_to_page(child_file, "2017-06-15T23:10:16-00:00", "F*CK\n\nDon't go")
  page_to_strzok(child_file, "2017-06-15T23:10:41-00:00", "Uh. Okay. What's up?")
  strzok_to_page(child_file, "2017-06-15T23:11:23-00:00", "Case is open")
  page_to_strzok(child_file, "2017-06-15T23:11:40-00:00", "Oh jesus. By whom?")
  strzok_to_page(child_file, "2017-06-15T23:12:23-00:00", "--Redacted-- Calling Aaron now if you want to stop by")
  strzok_to_page(child_file, "2017-06-15T23:12:25-00:00", "It's worse. ...")
  page_to_strzok(child_file, "2017-06-15T23:15:01-00:00", "I'm outside")
  strzok_to_page(child_file, "2017-06-16T00:38:27-00:00", "God I'm so disappointed in us as an organization. I want to send 10 polygraphers to --Redacted-- and poly the whole office. Or do every, Single. Last. Employee.")
  strzok_to_page(child_file, "2017-06-16T00:42:36-00:00", "Because the thing this one is we're SO bad that no one down here (or a couple of people in CID) knew. So you could literally just do the field office.")
  page_to_strzok(child_file, "2017-06-16T00:47:58-00:00", "So f it, let's do it.")
  strzok_to_page(child_file, "2017-06-16T00:50:32-00:00", "Have the A/DD pull the trigger....")
  page_to_strzok(child_file, "2017-06-16T00:51:17-00:00", "Yeah well I hold no sway over that guy.")

  # Page 496
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-16T00:51:25-00:00", "Plus, that will get out, and go a long way in the court of public opinion. Maybe. That, or evidence of just how f'ed up we are")
  strzok_to_page(child_file, "2017-06-16T00:52:05-00:00", "--Redacted-- said we fired some --Redacted-- in NY for leaking a few months ago. They sure were quiet about it.")
  page_to_strzok(child_file, "2017-06-16T02:54:09-00:00", "https://www.google.com/amp/www.newyorker.com/magazine/2017/05/15/taking-down-terrorists-in-court/amp")
  page_to_strzok(child_file, "2017-06-16T10:36:37-00:00", "The link is a HUGE profile of --Redacted/Zainab Ahmad-- in the New Yorker from last month.")
  page_to_strzok(child_file, "2017-06-16T10:37:22-00:00", "And the guardian has a ref to me now which is completely exaggerated and overblown.")
  page_to_strzok(child_file, "2017-06-16T10:37:24-00:00", "Very")
  strzok_to_page(child_file, "2017-06-16T10:37:56-00:00", "Ooh!:) Link?")
  page_to_strzok(child_file, "2017-06-16T10:38:02-00:00", "Guardian suggests I am a Russia OC expert. It's ridiculous.")
  strzok_to_page(child_file, "2017-06-16T10:37:56-00:00", "That's not necessarily good for you, from the perspective that Russians and Russion OC people in particular aren't always nice. Guess you can cross those plans to visit St Petersburg off the list...")
  strzok_to_page(child_file, "2017-06-16T10:46:01-00:00", "Hmm. Just read it. I understand the various motivations - both in the media and maybe even Peter - but I see various risks.")
  page_to_strzok(child_file, "2017-06-16T10:47:24-00:00", "I sent it to Peter, said it was all wrong. He said he (obviously) couldn't work with this outlet but to keep letting him know when things are wrong.")
  # strzok_to_page(child_file, "2017-06-16T10:47:36-00:00", "I don't know how you correct it - realistically you probably dont. And it would probably be a good thing --Redacted--")
  page_to_strzok(child_file, "2017-06-16T10:49:01-00:00", "What about --Redacted-- I don't know anyone who knows more than him.")
  # strzok_to_page(child_file, "2017-06-16T10:49:06-00:00", "You saw you're in the print nyt, right?")
  # strzok_to_page(child_file, "2017-06-16T10:49:30-00:00", "I was talking prosecutors, but maybe. --Redacted-- Can he be trusted?")
  page_to_strzok(child_file, "2017-06-16T10:50:12-00:00", "Yes. Absolutely. I thought he was actually --Redacted--")
  strzok_to_page(child_file, "2017-06-16T10:49:30-00:00", "I'll call him today.")
  page_to_strzok(child_file, "2017-06-16T11:34:06-00:00", "That profile on --Redacted/Ahmad-- was massively long. Was up until 11:15 reading and still didn't finish.")
  strzok_to_page(child_file, "2017-06-16T11:35:41-00:00", "I read a few paras and stopped")
  strzok_to_page(child_file, "2017-06-16T11:36:39-00:00", "Funny how flavors run. Clearly an \"article 3 courts work\" agenda. Would have loved a tenth as much fawning from --Redacted--")
  page_to_strzok(child_file, "2017-06-16T11:58:43-00:00", "Yup. It's unbelievably fawning. And learned that she's exactly my age. Maybe one more or less years as a lawyer. And --Redacted-- is the exact same year as me, 2006 law school grad.")
  
  # Page 497
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-16T12:05:29-00:00", "So you need to be --Redacted-- And get an office. \U0001f612")
  strzok_to_page(child_file, "2017-06-16T12:06:38-00:00", "And worry less about being REALLY good. \U0001f636")
  page_to_strzok(child_file, "2017-06-16T12:09:31-00:00", "Yeah, that's not happening. I think mostly I just need to get over myself.")
  page_to_strzok(child_file, "2017-06-16T12:10:02-00:00", "Let go of the fact that I'm not going to be in the room for most things and just accept that.")
  page_to_strzok(child_file, "2017-06-16T12:12:55-00:00", "I also need to screw up the courage to tell Aaron about my vacation. It's in less than two weeks and the house owner just said phone reception isn't great there and has a landline for emergencies.")
  strzok_to_page(child_file, "2017-06-16T12:24:52-00:00", "Re your vacation, I'd rip off that bandaid today. Want me to nudge you?")
  strzok_to_page(child_file, "2017-06-17T02:07:00-00:00", "Also, --Redacted-- They'll be more agreeable to get out for the weekend.")
  page_to_strzok(child_file, "2017-06-17T02:09:02-00:00", "Yes, but not if we keep them until 5 in the summer.")
  strzok_to_page(child_file, "2017-06-17T02:11:27-00:00", "Fair point. Settles it --Redacted-- then.")
  page_to_strzok(child_file, "2017-06-17T02:11:42-00:00", "But yes, --Redacted-- is where Aaron and I landed too.")
  strzok_to_page(child_file, "2017-06-17T02:19:15-00:00", "A) --Redacted-- is right.\nB --Redacted--")
  page_to_strzok(child_file, "2017-06-17T02:20:43-00:00", "And nope lots of reasons --Redacted-- is preferable.")
  strzok_to_page(child_file, "2017-06-17T02:23:37-00:00", "--Redacted-- B) Why Fri?\n\n--Redacted--")
  page_to_strzok(child_file, "2017-06-18T17:11:15-00:00", "Aaron just called to say he had spoken to some people (nfi) and had come up with a plan to have me fully integrated as --Redacted-- and asked me to give him two weeks to implement (ie --Redacted--. It's funny, because now I truly don't want it anymore, but I feel like I'm stuck.")
  # page_to_strzok(child_file, "2017-06-18T17:11:59-00:00", "I must have really freaked him out on Friday when I told him I wanted to join the --Redacted--")
  strzok_to_page(child_file, "2017-06-18T17:31:31-00:00", "Hmm")
  strzok_to_page(child_file, "2017-06-18T17:33:53-00:00", "I worry he's freaking out because he doesn't want to track all the nickle-dime admin items that he hopes to give to you.\n\nDo YOU want that?")
  strzok_to_page(child_file, "2017-06-18T17:35:04-00:00", "Did you tell him you really wanted on the --Redacted-- When he and I spoke earlier in the week, he said he really thought the best place for you long term was --Redacted--")
  # strzok_to_page(child_file, "2017-06-18T17:36:19-00:00", "Wonder what changed.\n\nI worry it's the FOIA yuck, with a realization there will be a hundred things like that he doesn't want.")
  strzok_to_page(child_file, "2017-06-18T17:38:02-00:00", "On my end, it's getting harder to let go as I get the access I wanted and build the team...\U0001f615\n\nDespite that, you still think my better play is to go back?")
  
  # Page 498
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-18T18:04:54-00:00", "No, I don't! I really had found acceptance of my decision! And yeah, sure, I'll be in a couple of more meetings, but I'm still not going to be truly in. I don't want this, yet here I am.")
  page_to_strzok(child_file, "2017-06-18T18:05:47-00:00", "Have been thinking that maybe I'd offer --Redacted-- That'd be a good developmental post for --Redacted-- Though I'm sure they won't let me do that either.")
  page_to_strzok(child_file, "2017-06-18T18:06:51-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-18T18:20:18-00:00", "You should tell Aaron that. Let him know what you really want before --Redacted-- Did you tell him today?")
  strzok_to_page(child_file, "2017-06-18T18:21:16-00:00", "Good idea with --Redacted-- They just might, let them interview --Redacted--")
  page_to_strzok(child_file, "2017-06-18T18:26:38-00:00", "No. I'll talk to him tomorrow. It was literally a five minute conversation, and I was --Redacted-- so I didn't feel like talking further.")
  strzok_to_page(child_file, "2017-06-18T18:33:42-00:00", "Perfect.\n\nDid you bounce the idea of SC off of --Redacted--?")
  page_to_strzok(child_file, "2017-06-18T18:33:56-00:00", "Nope. Aaron called well after.")
  strzok_to_page(child_file, "2017-06-18T18:34:47-00:00", "I truly don't think you want what they envision for --Redacted-- They want a talented young detail oriented task master. I think you REALLY want case work. Even if that means you miss some meetings.")
  page_to_strzok(child_file, "2017-06-18T18:35:24-00:00", "Yup, I know. I'm there too.")
  strzok_to_page(child_file, "2017-06-18T18:35:30-00:00", "FOIA and macros and tracking due outs and the rest. You're more senior than that.")
  strzok_to_page(child_file, "2017-06-18T18:36:27-00:00", "Plus I think --Redacted--'s senior enough you could be partners and also be Ok with her mentoring you. Makes a lot more sense than Andrew.")
  page_to_strzok(child_file, "2017-06-18T18:37:42-00:00", "And we talked for about an hour on Friday night and used exactly that word, partners. With a plan to give the grunt work to two of the younger attorneys.")
  strzok_to_page(child_file, "2017-06-18T18:45:41-00:00", "Yeah, I think you two would be super good together.\n\nAnd I'm getting you great agents and analysts...")
  page_to_strzok(child_file, "2017-06-18T19:10:13-00:00", "I know it! That's why I kinda just want to take it on, you know?")
  strzok_to_page(child_file, "2017-06-18T19:25:46-00:00", "I DO know!")
  strzok_to_page(child_file, "2017-06-18T19:26:26-00:00", "I'd be tempted to just work cases on this, too! --Redacted--")
  strzok_to_page(child_file, "2017-06-18T21:24:44-00:00", "And wooo! Just got --Redacted-- on board. \U0001f60a")
  page_to_strzok(child_file, "2017-06-18T23:48:00-00:00", "Who is that?")
  strzok_to_page(child_file, "2017-06-18T23:48:34-00:00", "--Redacted-- in SF")
  strzok_to_page(child_file, "2017-06-18T23:48:58-00:00", "--Redacted-- for a while, knows --Redacted--")
  
  # Page 499
  # OUTBOX == Page
  # INBOX == Strzok
  strzok_to_page(child_file, "2017-06-19T23:18:38-00:00", "You'll be thrilled to learn I TOLD THEM THIS AT THE --Redacted-- MEETING!\U0001f621")
  page_to_strzok(child_file, "2017-06-19T23:18:47-00:00", "Stop smiling when he says that. He's completely insulting out boss.")
  page_to_strzok(child_file, "2017-06-19T23:20:24-00:00", "The sucking all the air out of the room, talking too much.")
  strzok_to_page(child_file, "2017-06-19T23:23:13-00:00", "Oh. I completely get he's insulting him. And that bothers me. I'm NOT agreeing with him.\n\nAnd I don't remember him saying that recently in the conversation.")
  strzok_to_page(child_file, "2017-06-19T23:24:06-00:00", "That's why I explained the D's background in going.")
  strzok_to_page(child_file, "2017-06-19T23:54:06-00:00", "Did you correct his perception or let him know that maybe he wanted extra witnesses?")
  page_to_strzok(child_file, "2017-06-19T23:56:14-00:00", "Huh? He said it like 5 times. We must be talking about different things.")
  strzok_to_page(child_file, "2017-06-19T23:58:07-00:00", "Talk in 3?")
  page_to_strzok(child_file, "2017-06-19T23:59:53-00:00", "I guess. It's not that important.") 
  strzok_to_page(child_file, "2017-06-20T00:30:23-00:00", "Hi. Hoping you got a chance to talk to Aaron about you. Of course wnat to hear about it if you did.")
  page_to_strzok(child_file, "2017-06-20T01:59:08-00:00", "--Redacted--'ve been in with Aaron for the last two hours. Another very good honest conversation.") 
  strzok_to_page(child_file, "2017-06-20T02:26:09-00:00", "--Redacted-- absolutely want to hear about your convo with Aaron. I'm glad it went well. Where did you end up?\n\n(other than that, Mrs. Lincoln, how was the olay?)")
  strzok_to_page(child_file, "2017-06-20T02:26:16-00:00", "Play. Olay is not a word. \U0001f621")
  page_to_strzok(child_file, "2017-06-20T02:27:47-00:00", "Not a clear answer but an honest conversation about what I want ideally. A definite commitment to hire a number 2 for the chief of staff role.") 
  strzok_to_page(child_file, "2017-06-20T02:29:53-00:00", "A number 2 for you if you take it? Are you taking it?")
  page_to_strzok(child_file, "2017-06-20T02:31:28-00:00", "Maybe, maybe not. Honestly, were just going to try it out while still trying to keep me on --Redacted-- team. And I got us both invited to the case deep dives they are going every day this week.") 
  strzok_to_page(child_file, "2017-06-20T02:42:41-00:00", "Thanks for the deep dives. I knew Andrew was going today but had our meeting as a conflict and didn't have a chance to say I should be there.")
  strzok_to_page(child_file, "2017-06-20T02:43:19-00:00", "The only way I knew it was --Redacted-- Forgot to mention. Frankly, forgot all about it.")
  strzok_to_page(child_file, "2017-06-20T02:44:03-00:00", "Now that I remember, it pisses me off. The FBI doesn't have a role in discussing the deep dives/path forward?")
  page_to_strzok(child_file, "2017-06-20T02:44:07-00:00", "Yeah, well Aaron just forgot about you but immediately added you, I had to push, quite directly, for me.") 
  page_to_strzok(child_file, "2017-06-20T02:44:50-00:00", "It does --Redacted-- will be there in the future, and you/your role.") 
  strzok_to_page(child_file, "2017-06-20T17:29:47-00:00", "I'm sorry I missed Z's walk thru. Though I guess I better get past that")

  # Page 500
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-20T17:30:05-00:00", "Ah. Got it. Yeah, I guess we can talk later. You coming in?")
  strzok_to_page(child_file, "2017-06-20T17:30:18-00:00", "Aaron was super apologetic about not having included on the initial invite")
  strzok_to_page(child_file, "2017-06-20T17:30:54-00:00", "Thinking about it.")
  page_to_strzok(child_file, "2017-06-20T17:31:07-00:00", "Yeah, he felt very badly when he told me too.")
  strzok_to_page(child_file, "2017-06-20T21:02:22-00:00", "And I deeply sincerely meant it earlier when I said I simply want you happy.")
  page_to_strzok(child_file, "2017-06-20T21:08:45-00:00", "Then don't join the team.")
  strzok_to_page(child_file, "2017-06-20T21:48:20-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-20T22:28:47-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-20T22:31:49-00:00", "--Redacted--")
  page_to_strzok(child_file, "2017-06-20T22:32:51-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-21T00:20:33-00:00", "And helpful, Moffa says HQ is completely f*cked up.")
  page_to_strzok(child_file, "2017-06-21T00:34:41-00:00", "Stop debating. Stop trying to reason it out. There's no reasoning. --Redacted-- don't want to work with you. Go help Bill make CD better, leave it better off than it was.")
  strzok_to_page(child_file, "2017-06-21T00:47:49-00:00", "Well with mtg pushed to Fri there is time. Lisa, I'm PULLED to the mission and the team, for the right reasons. You saw it! You know what it is inside me and that it's pure and I'm good and you admire it! --Redacted-- Maybe I'm being dumb about throwing myself entirely and with my whole heart into a project may be exactly what that needs --Redacted-- And I take all of the points you made about my inability to control, prevent or even predict that.")
  page_to_strzok(child_file, "2017-06-21T00:53:48-00:00", "It doesn't NEED you. And I don't care if it does. Every conversation I've had with you about this still stands, and now I've asked you, begged you, not to. You do what you want.")
  strzok_to_page(child_file, "2017-06-21T02:27:10-00:00", "You have. --Redacted-- \U0001f614")
  page_to_strzok(child_file, "2017-06-21T04:41:33-00:00", "--Redacted--")
  strzok_to_page(child_file, "2017-06-21T09:54:04-00:00", "Are we on for 930 congressional timeline? And can we please talk today?")

  # Page 501
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-21T09:55:36-00:00", "No, no one ever responded besides --Redacted-- and now I have a 10.")
  strzok_to_page(child_file, "2017-06-21T09:58:39-00:00", "Yeah, sorry, I'm guilty, I didn't either.")
  # page_to_strzok(child_file, "2017-06-22T12:48:15-00:00", "I'm thinking I might leave SC. Maybe hold to say something.")
  page_to_strzok(child_file, "2017-06-22T16:23:55-00:00", "Let me know when you are free.")
  strzok_to_page(child_file, "2017-06-22T16:36:54-00:00", "Free")
  strzok_to_page(child_file, "2017-06-22T16:37:04-00:00", "At desk at sco")
  page_to_strzok(child_file, "2017-06-22T16:37:21-00:00", "Number?")
  page_to_strzok(child_file, "2017-06-22T17:09:13-00:00", "One sec")
  page_to_strzok(child_file, "2017-06-22T19:17:24-00:00", "You go to --Redacted--")
  strzok_to_page(child_file, "2017-06-22T19:29:55-00:00", "Yes. There now")
  strzok_to_page(child_file, "2017-06-22T19:30:43-00:00", "But I want to hear about --Redacted-- \U0001f615\n--Redacted-- was on beachhead team, right?")
  page_to_strzok(child_file, "2017-06-22T19:32:42-00:00", "Headed up engagement --Redacted--")
  strzok_to_page(child_file, "2017-06-22T19:33:29-00:00", "The whole --Redacted--?")
  page_to_strzok(child_file, "2017-06-22T19:33:48-00:00", "Pretty sure.")
  page_to_strzok(child_file, "2017-06-22T19:34:02-00:00", "I could be wrong, but pretty sure.")
  strzok_to_page(child_file, "2017-06-22T19:34:21-00:00", "I remember that too")
  page_to_strzok(child_file, "2017-06-22T22:30:13-00:00", "--Redacted-- didn't get the job. Don't say anything to anyone. This place really does suck sometimes.")
  strzok_to_page(child_file, "2017-06-22T22:33:29-00:00", "What?#?!?")
  strzok_to_page(child_file, "2017-06-22T22:33:55-00:00", "That's bullsh*t")
  strzok_to_page(child_file, "2017-06-22T22:37:39-00:00", "Hey if you decide re sco let me know --Redacted--")
  page_to_strzok(child_file, "2017-06-22T22:37:57-00:00", "Just tell --Redacted-- I'm not going.")
  strzok_to_page(child_file, "2017-06-22T23:03:39-00:00", "Let's sleep on it")
  strzok_to_page(child_file, "2017-06-22T23:05:59-00:00", "--Redacted-- tomorrow makes as much sense.")
  strzok_to_page(child_file, "2017-06-22T23:06:41-00:00", "Bill told me about --Redacted-- Does --Redacted-- know?\n\naAnd that board decision is a slap not only against --Redacted-- but also Andy. \U0001f621")

  # Page 502
  # OUTBOX == Page
  # INBOX == Strzok
  page_to_strzok(child_file, "2017-06-22T23:08:46-00:00", "Yes --Redacted-- told me.")
  strzok_to_page(child_file, "2017-06-22T23:09:54-00:00", "Damn\n\nWas hoping Andy might overturn it. It makes me SO mad. F this place")
  page_to_strzok(child_file, "2017-06-22T23:10:32-00:00", "Well, --Redacted-- heard from Carl, so I don't know if it went to Andy yet. Maybe so.")
  strzok_to_page(child_file, "2017-06-22T23:27:21-00:00", "It sucks for --Redacted--. I want to call --Redacted-- but I'll wait --Redacted-- \U0001f636\U0001f621\U0001f614")
  page_to_strzok(child_file, "2017-06-25T14:32:59-00:00", "Please don't ever text me again.")

  # Completed
  return None

def create_media(t: truxton.TruxtonObject) -> truxton.TruxtonMedia:

  global Crossfire_Typhoon
  global Crossfire_Razor
  global Crossfire_Fury
  global Crossfire_Dragon

  Crossfire_Typhoon = create_typhoon(t)
  Crossfire_Razor = create_razor(t)
  Crossfire_Fury = create_fury(t)
  Crossfire_Dragon = create_dragon(t)

  media = t.newmedia()

  media.name = "Public Documents"
  media.description = "Everything released by the government, books, news organizations and blogs"
  media.case = "DC-SNAFU-2016.2020"
  media.evidencebag = "EV-0937459386623-a"
  media.originator = "Jeffrey Jensen"
  media.latitude = 38.897661
  media.longitude = -77.036458
  media.type = truxton.MEDIA_TYPE_LOGICAL_FILES

  if not media.save():
    print("Media not saved")
  else:
    print("Media created")

  return media

def create_typhoon(t: truxton.TruxtonObject) -> truxton.TruxtonMedia:
  media = t.newmedia()

  media.name = "Crossfire Typhoon"
  media.description = "George Papadopoulos"
  media.case = "97F-HQ-2067748"
  media.evidencebag = "None"
  media.originator = "Jeffrey Jensen"
  media.latitude = 38.897661
  media.longitude = -77.036458
  media.type = truxton.MEDIA_TYPE_LOGICAL_FILES

  if not media.save():
    print("Crossfire Typhoon media not saved")
  else:
    print("Crossfire Typhoon media created")

  return media

def create_razor(t: truxton.TruxtonObject) -> truxton.TruxtonMedia:
  media = t.newmedia()

  media.name = "Crossfire Razor"
  media.description = "Michael Flynn"
  media.case = "97F-NY-2069860"
  media.evidencebag = "None"
  media.originator = "Jeffrey Jensen"
  media.latitude = 38.897661
  media.longitude = -77.036458
  media.type = truxton.MEDIA_TYPE_LOGICAL_FILES

  if not media.save():
    print("Crossfire Razor media not saved")
  else:
    print("Crossfire Razor media created")

  return media

def create_fury(t: truxton.TruxtonObject) -> truxton.TruxtonMedia:
  media = t.newmedia()

  media.name = "Crossfire Fury"
  media.description = "Paul Manafort"
  media.case = "97F-HQ-2067749"
  media.evidencebag = "None"
  media.originator = "Paul Manafort"
  media.latitude = 38.897661
  media.longitude = -77.036458
  media.type = truxton.MEDIA_TYPE_LOGICAL_FILES

  if not media.save():
    print("Crossfire Fury media not saved")
  else:
    print("Crossfire Fury media created")

  return media

def create_dragon(t: truxton.TruxtonObject) -> truxton.TruxtonMedia:
  media = t.newmedia()

  media.name = "Crossfire Dragon"
  media.description = "Carter Page"
  media.case = "97F-HQ-2067747"
  media.evidencebag = "None"
  media.originator = "Carter Page"
  media.latitude = 38.897661
  media.longitude = -77.036458
  media.type = truxton.MEDIA_TYPE_LOGICAL_FILES

  if not media.save():
    print("Crossfire Dragon media not saved")
  else:
    print("Crossfire Dragon media created")

  return media

# defined constants
EVENT_TYPE_CAMPAIGN = 20000
EVENT_TYPE_FBI = 20001
EVENT_TYPE_CIA = 20002
EVENT_TYPE_DNI = 20003
EVENT_TYPE_WIKILEAKS = 20004
EVENT_TYPE_MUELLER = 20005
EVENT_TYPE_STRZOK_PAGE_MESSAGE = 20006
EVENT_TYPE_MIFSUD = 20007
EVENT_TYPE_STEELE = 20008
EVENT_TYPE_FISA = 20009
EVENT_TYPE_DOWNER = 20010
EVENT_TYPE_RICE = 20011
EVENT_TYPE_POWER = 20012
EVENT_TYPE_GCHQ = 20013
EVENT_TYPE_NSA = 20014
EVENT_TYPE_OBAMA = 20015
EVENT_TYPE_UNMASK = 20016
EVENT_TYPE_DOJ = 20017
EVENT_TYPE_FLYNN = 20018
EVENT_TYPE_HILLARY = 20019
EVENT_TYPE_DANCHENKO = 20020
EVENT_TYPE_MCCABE_PAGE_MESSAGE = 20021

MCCABE_PHONE_NUMBER = "2025551111"
STRZOK_PHONE_NUMBER = "2025552222"
PAGE_PHONE_NUMBER   = "2025553333"

# Create our artifact types
def create_artifact_types(t: truxton.TruxtonObject) -> None:
  create_artifact_type(t, 1101, "Leak", "A leak" )
  return None

# Create our types
def create_event_types(t: truxton.TruxtonObject) -> None:
  create_event_type(t, EVENT_TYPE_CAMPAIGN, "Trump Campaign" )
  create_event_type(t, EVENT_TYPE_FBI, "FBI Actions" )
  create_event_type(t, EVENT_TYPE_CIA, "CIA Actions" )
  create_event_type(t, EVENT_TYPE_DNI, "DNI Actions" )
  create_event_type(t, EVENT_TYPE_WIKILEAKS, "Wikileaks Actions" )
  create_event_type(t, EVENT_TYPE_MUELLER, "Mueller Actions" )
  create_event_type(t, EVENT_TYPE_STRZOK_PAGE_MESSAGE, "Strzok Page Message" )
  create_event_type(t, EVENT_TYPE_MIFSUD, "Mifsud Actions" )
  create_event_type(t, EVENT_TYPE_STEELE, "Steele Report" )
  create_event_type(t, EVENT_TYPE_FISA, "FISA/FISC" )
  create_event_type(t, EVENT_TYPE_DOWNER, "Alexander Downer Actions" )
  create_event_type(t, EVENT_TYPE_RICE, "Susan Rice Actions" )
  create_event_type(t, EVENT_TYPE_POWER, "Samantha Power Actions" )
  create_event_type(t, EVENT_TYPE_GCHQ, "GCHQ Actions" )
  create_event_type(t, EVENT_TYPE_NSA, "NSA Actions" )
  create_event_type(t, EVENT_TYPE_OBAMA, "Obama Actions" )
  create_event_type(t, EVENT_TYPE_UNMASK, "Flynn Unmasking" )
  create_event_type(t, EVENT_TYPE_DOJ, "DOJ Actions" )
  create_event_type(t, EVENT_TYPE_FLYNN, "Flynn Actions" )
  create_event_type(t, EVENT_TYPE_HILLARY, "Hillary Clinton Campaign" )
  create_event_type(t, EVENT_TYPE_DANCHENKO, "Danchenko" )
  create_event_type(t, EVENT_TYPE_MCCABE_PAGE_MESSAGE, "McCabe Page Message" )

  print("Custom event types created")
  return None

def set_primary_photo(parent_file: truxton.TruxtonChildFileIO, subject: truxton.TruxtonSubject, filename: str) -> None:
  child_file = add_file(parent_file, filename)
  relation = child_file.newrelation()
  relation.a = child_file.id
  relation.atype = truxton.OBJECT_TYPE_FILE
  relation.b = subject.id
  relation.btype = truxton.OBJECT_TYPE_SUSPECT
  relation.relation = truxton.RELATION_PRIMARY_PHOTO
  relation.save()
  return None

def create_subjects(t: truxton.TruxtonObject) -> None:
  print("Creating Subjects")

  s = t.newsubject()
  s.id = "00138955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Alexander Downer"
  s.description = "Australian High Commissioner to the United Kingdom. Heard Papadopoulos mention Clinton Emails and reported it."
  ff = datetime.fromisoformat("1951-09-09T00:00:00-00:00")
  s.birthday = datetime.fromisoformat("1951-09-09T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Alexander Downer.png")
  s.save()
  s.tag("AUS", "Australia is also known as the Friendly Foreign Government", truxton.TAG_ORIGIN_HUMAN)

  s = t.newsubject()
  s.id = "00238955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Andrew G. McCabe"
  s.description = "Deputy Director (DD) FBI"
  s.birthday = datetime.fromisoformat("1968-03-18T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Andrew McCabe.png")
  s.save()

  s = t.newsubject()
  s.id = "00338955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Edward William 'Bill' Priestap"
  s.description = "Deputy Counterintelligence Division (DCD) FBI"
  s.birthday = datetime.fromisoformat("1969-04-05T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Bill Priestap.png")
  # Email account "ewpriestap" according to Page 86 of 460365255-Flynn-motion-to-dismiss.pdf
  s.save()

  s = t.newsubject()
  s.id = "00438955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Christopher Steele"
  # 456600733-FISA-footnotes.pdf
  s.description = "Former MI-6, aka CROWN (FBI), FBI Confidential Human Source (CHS) paid $95,000"
  s.birthday = datetime.fromisoformat("1964-06-24T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Christopher Steele.png")
  s.save()

  s = t.newsubject()
  s.id = "00538955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Dana Boente"
  s.description = "Acting Attorney General"
  s.birthday = datetime.fromisoformat("1954-02-07T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Dana Boente.png")
  s.save()

  s = t.newsubject()
  s.id = "00638955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "David Kramer"
  s.description = "Aide to Senator John McCain"
  s.custom = "Went to London to receive dossier from Christopher Steele, leaked it to Buzzfeed"
  s.birthday = datetime.fromisoformat("1964-12-01T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/David Kramer.png")
  s.save()

  s = t.newsubject()
  s.id = "00738955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Erika Thompson"
  s.description = "Assistant to High Commissioner Alexander Downer in London"
  s.custom = "Her fiance, Christian Cantor (Israeli diplomat), knew Papadapolous and suggested her boss, Alexander Downer, meet him"
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Erika Thompson.png")
  s.save()

  s = t.newsubject()
  s.id = "00748955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Christian Cantor"
  s.description = "Political Counselor at the Embassy of Israel in London"
  s.custom = "His idea for Papadapolous to meet Downer. His fiance, Erika Thompson worked for Australian High Commissioner Alexander Downer"
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Christian Cantor.png")
  s.save()

  s = t.newsubject()
  s.id = "00838955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "George Papadopoulos"
  s.description = "Trump Campaign Aide, AKA Crossfire Typhoon"
  s.birthday = datetime.fromisoformat("1987-08-19T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/George Papadopoulos.png")
  s.save()

  s = t.newsubject()
  s.id = "00938955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Glenn Simpson"
  s.description = "Founder of Fusion GPS"
  s.birthday = datetime.fromisoformat("1964-01-01T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Glenn Simpson.png")
  s.save()

  s = t.newsubject()
  s.id = "01038955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Jean Camp"
  s.description = "Computer Security Researcher and Clinton supporter, told FBI about 2700 DNS name lookups from Alfa bank for FISA warrant"
  s.custom = "Her DNS research is at http://www.ljean.com/NetworkData.php"
  s.birthday = datetime.fromisoformat("1964-09-19T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Jean Camp.png")
  s.save()

  s = t.newsubject()
  s.id = "01138955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "John Brennan"
  s.description = "Director CIA"
  s.birthday = datetime.fromisoformat("1955-09-22T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/John Brennan.png")
  s.save()

  s = t.newsubject()
  s.id = "01238955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "John P. Carlin"
  s.description = "Assistant Attorney General"
  s.custom = "Head of the Department of Justice's National Security Division (NSD)"
  s.birthday = datetime.fromisoformat("1907-01-01T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/John Carlin.png")
  s.save()

  s = t.newsubject()
  s.id = "01338955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Joseph Mifsud"
  s.description = "Probable CIA Asset. Page 312 of FBI FISA IG Report states 'no evidence Mifsud has ever acted as an FBI CHS'"
  s.custom = "Told Papadapolous about Clinton email before Papadapolous met Alexander Downer"
  s.birthday = datetime.fromisoformat("1960-01-01T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Joseph Mifsud.png")
  s.save()

  s = t.newsubject()
  s.id = "01438955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Kevin Clinesmith"
  s.description = "Lawyer FBI, Convicted of lying on FISA warrant against Carter Page"
  s.custom = "Author of 'Resistence' text message, altered FISA warrant on Page"
  s.birthday = datetime.fromisoformat("1982-05-18T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Kevin Clinesmith.png")
  s.save()

  s = t.newsubject()
  s.id = "01538955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Lisa C. Page"
  s.description = "Lawyer FBI, McCabe's Legal Counsel"
  s.custom = "Husband: Joseph Burrow"
  s.birthday = datetime.fromisoformat("1980-08-02T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Lisa Page.png")
  s.save()

  s = t.newsubject()
  s.id = "01638955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Michael Gaeta"
  s.description = "Assistant FBI Legal Attaché (legat) in Rome, aka 'Handling Agent 1' in FBI IG Report"
  s.custom = "Former member of the FBI's Eurasian Organized Crime unit, Steele's handler, possibly Mifsud's handler"
  #s.birthday = datetime.fromisoformat("1980-08-02T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Michael Gaeta.png")
  s.save()

  s = t.newsubject()
  s.id = "01738955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Peter P. Strzok II"
  s.description = "FBI, worked on Flynn case and Clinton EMail Case (Midyear Exam)"
  s.custom = "Wife: Melissa Hodgman"
  s.birthday = datetime.fromisoformat("1970-03-07T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Peter Strzok.png")
  s.save()

  s = t.newsubject()
  s.id = "01838955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Sir Richard Dearlove"
  s.description = "Director BSIS (MI-6)"
  s.birthday = datetime.fromisoformat("1945-01-23T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Richard Dearlove.png")
  s.save()

  s = t.newsubject()
  s.id = "01938955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Robert Hannigan"
  s.description = "Director GCHQ"
  s.custom = "Resigned from GCHQ due to his helping paedophile priest avoid jail"
  s.birthday = datetime.fromisoformat("1965-01-01T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Robert Hannigan.png")
  s.save()

  s = t.newsubject()
  s.id = "02038955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Samantha Power"
  s.description = "United States UN Ambassador"
  s.custom = "Prolific SIGINT unmasker"
  s.birthday = datetime.fromisoformat("1970-09-21T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Samantha Power.png")
  s.save()

  s = t.newsubject()
  s.id = "02138955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Sergey Ivanovich Kislyak"
  s.description = "Russia Ambassador"
  s.custom = "Had phone calls with Flynn"
  s.birthday = datetime.fromisoformat("1950-09-07T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Sergey Ivanovich Kislyak.png")
  s.save()

  s = t.newsubject()
  s.id = "02238955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Sir Andrew Wood"
  s.description = "British Ambassador to Russia"
  s.custom = "Told John McCain of the Steele Dossier"
  s.birthday = datetime.fromisoformat("1940-01-02T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Sir Andrew Wood.png")
  s.save()

  s = t.newsubject()
  s.id = "02338955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Stefan Halper"
  s.description = "FBI Asset, was sent as CHS to target Carter Page and Papadapolous, aka 'Source 2' in FBI IG Report"
  s.custom = "Paid over $400,000 by U.S. government"
  s.birthday = datetime.fromisoformat("1944-06-04T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Stefan Halper.png")
  s.save()

  s = t.newsubject()
  s.id = "02438955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Susan E. Rice"
  s.description = "National Security Advisor"
  s.birthday = datetime.fromisoformat("1964-11-17T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Susan Rice.png")
  s.save()

  s = t.newsubject()
  s.id = "02538955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "Carter Page"
  s.description = "Trump Campaign Aide and former CIA informant. AKA Crossfire Dragon"
  s.birthday = datetime.fromisoformat("1971-06-03T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Carter Page.png")
  s.save()

  s = t.newsubject()
  s.id = "02638955-133D-D2C1-A9E9-ADFF27FA80F4"
  s.name = "James Clapper"
  s.description = "Director National Intelligence (DNI)"
  s.birthday = datetime.fromisoformat("1941-03-14T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/James Clapper.png")
  s.save()

  s = t.newsubject()
  s.id = "02786B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Igor 'Iggy' Yurievich Danchenko"
  s.description = "Steele's primary sub source, Paid FBI informant, worked at Brookings Institute"
  s.birthday = datetime.fromisoformat("1978-05-05T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Igor Danchenko.png")
  s.save()

  s = t.newsubject()
  s.id = "08886B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Olga Galkina"
  s.description = "Igor Danchenko's primary source. Aka Source 3 in February 9, 2017 Electronic Communication.pdf"
  # s.birthday = datetime.fromisoformat("1978-05-05T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Olga Galkina.png")

  s = t.newsubject()
  s.id = "02886B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Joseph 'Joe' Pientka III"
  # Facts we know about Joe
  # From https://gw.geneanet.org/tdowling?lang=en&pz=erica+marie&nz=tork&p=joe&n=pientka&oc=2
  # Wife: Melissa Anne Bristow
  # Daughter: Jillian Marie Pientka
  # Daughter: Madeleine Jolie Pientka
  # Son: Ethan Sawyer Pientka
  # He lived at 3227 20th Road N, Arlington VA from 2005-08-26 until 2020-07-03 when the gov't bought his house through LEXICON GOVERNMENT SERVICES LLC (N-DREA Not a market Sale)
  s.description = "FBI Supervisory Special Agent (SSA), Ran Crossfire Hurricane, interviewed Flynn at White House, gave Flynn defensive briefing"
  s.birthday = datetime.fromisoformat("1976-01-01T00:00:00-00:00")
  s.save()

  s = t.newsubject()
  s.id = "02986B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Michael Flynn"
  s.description = "Lt. General US Army, AKA Crossfire Razor"
  s.birthday = datetime.fromisoformat("1958-12-24T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Michael Flynn.png")
  s.save()

  s = t.newsubject()
  s.id = "03086B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "William J. Barnett"
  s.description = "FBI Special Agent handled Flynn investigation then assigned to Special Counsel's Office (SCO)"
  s.save()

  s = t.newsubject()
  s.id = "03186B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Robert 'Bob' S. Litt"
  s.description = "General Counsel to DNI Clapper, first person to have thought of Logan Act of 1799"
  s.birthday = datetime.fromisoformat("1950-01-01T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Robert Litt.png")
  s.save()

  s = t.newsubject()
  s.id = "03286B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Jeffery 'Jeff' Wiseman"
  s.description = "FBI CHS #3, wore a wire, went to MGM Grand DC with George Papadopoulos, at the time he worked for Cerner Corporation in Chicago"
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Jeffery Wiseman.png")
  s.save()

  s = t.newsubject()
  s.id = "03386B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "James A. Baker"
  s.description = "FBI General Counsel"
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/James Baker.png")
  # Email account "james.baker" according to Page 85 of 460365255-Flynn-motion-to-dismiss.pdf
  s.save()

  s = t.newsubject()
  s.id = "03486B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Michael Sussman"
  s.description = "Partner at Perkins Coie Privacy and Data Security Practice. Fed Alfa Bank/Trump Campaign link to James Baker at FBI"
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Michael Sussman.png")
  s.save()

  s = t.newsubject()
  # https://www.mylife.com/kathleen-kavalec/e435913687320
  s.id = "88486B2F-A5E1-37E8-B7E4-C6B9D30E8623"
  s.name = "Kathleen Kavalec"
  s.description = "Deputy Assistant Secretary, Bureau of European and Eurasian Affairs, Department of State. Met with Steele."
  s.birthday = datetime.fromisoformat("1958-08-06T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Kathleen Kavalec.png")
  s.save()

  s = t.newsubject()
  s.id = "880CA7DF-334D-402A-B3CF-7CDE15EED8BE"
  s.name = "Charles Halliday Dolan, Jr."
  s.description = "Hillary Campaign PR-Executive-1. Started the pee tapes rumor, fed it to Danchenko. Works for kglobal and Prism Public Affairs"
  s.birthday = datetime.fromisoformat("1950-06-12T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Charles Dolan.png")
  s.save()
  # 1730 N Huntington Street, Arlington, VA 22205-2709

  # Rudolph Contreras, https://www.24hourcampfire.com/ubbthreads/ubbthreads.php/topics/12723193/re-strzok-page-fisa-judge-entanglement-text-messsages
  # Events to add
  #  Strzok Page message about Rudy being appointed to FISC
  #  Contreras accepting plea
  #  Contreras stepping down from Flynn case
  # https://everipedia.org/wiki/lang_en/Rudolph_Contreras
  s = t.newsubject()
  s.id = "6B80336C-9110-4868-A64E-E3DC1548164F"
  s.name = "Rudolph (Rudy) Contreras"
  s.description = "FISC judge in contact with Strzok and Page"
  s.birthday = datetime.fromisoformat("1962-12-06T00:00:00-00:00")
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Rudolph Contreras.png")
  s.save()

  s = t.newsubject()
  s.id = "880EBE24-B157-7CC1-465F-8C6579731253"
  s.name = "Kevin Helson"
  s.description = "FBI Agent, WFO, Danchenko's handler"
  s.save()
  
# https://www.washingtonexaminer.com/news/fbis-case-agent-1-stephen-somma-primarily-responsible-for-fisa-failures
# States that Case Agent 1 in IG Report is Stephen Somma
  s = t.newsubject()
  s.id = "61E2A86F-098F-254B-386E-5B9F53B1785A"
  s.name = "Stephen (Steve) Somma"
  s.description = "FBI Agent, Crossfire Hurricane team"
  s.save()
  
  s = t.newsubject()
  s.id = "5BBCCB7C-2231-BA83-20D9-06F0401375C6"
  s.name = "Brian Auten"
  s.description = "FBI Intelligence Analyst, Crossfire Hurricane team"
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/Brian Auten.png")
  s.save()

  s = t.newsubject()
  s.id = "394AD0B8-7E59-70DB-9991-1D44CF993510"
  s.name = "David L. Bowdich"
  s.description = "Deputy Director FBI, as of February 2021 he is Chief Security Officer of Disney"
  s.picture = b64(SUPPORT_DOCUMENTS_FOLDER + "Images/David Bowdich.jpg")
  s.save()

  print("The subjects of the investigation (aka suspects/players/persons of interest) created")
  return None

def create_tags(t: truxton.TruxtonObject) -> None:
  t.createtag("AUS", "Actions probably taken by Australia")
  t.createtag("CIA", "Actions probably taken by CIA")
  t.createtag("Court Filing", "This item was part of a court filing")
  t.createtag("Crossfire Dragon", "FBI's investigation of Carter Page")
  t.createtag("Crossfire Fury", "FBI's investigation of Paul Manafort")
  t.createtag("Crossfire Razor", "FBI's investigation of Michael Flynn")
  t.createtag("Crossfire Typhoon", "FBI's investigation of George Papadopoulos")
  t.createtag("FD-1057", "FBI Electronic Communication")
  t.createtag("FD-302", "FBI Interview Notes")
  t.createtag("FD-1087", "FBI Collected Item Log")
  t.createtag("FISA Abuse", "Things related to FISA abuse")
  t.createtag("Hatred", "Expression of hatred of Trump")
  t.createtag("Leak", "Information leaked to the press")
  t.createtag("Memo", "This item is part of a memo")
  t.createtag("Midyear Exam", "FBI's investigation of Hillary Clinton Email Server")
  t.createtag("News Article", "This items is part of a news article")
  t.createtag("Steele Report", "Information about the Steele Report")
  t.createtag("Testimony", "This is part of testimony")
  t.createtag("Unhappy", "All is not well in Hurricane-ville")
  print("Created Tags")
  return None

# Utility Functions
def unix_millisecond_epoch_to_ticks(unix_epoch: int) -> int:
  NUMBER_OF_FILETIME_TICKS_IN_ONE_SECOND = 10000
  FILETIME_OF_1970_01_01 = 116444736000000000
  return FILETIME_OF_1970_01_01 + (unix_epoch * NUMBER_OF_FILETIME_TICKS_IN_ONE_SECOND)

def date_to_filetime(dt: int) -> int:
  return unix_millisecond_epoch_to_ticks(timegm(dt.timetuple()) * 1000)

def ticks(iso8601: str) -> int:
  return date_to_filetime(datetime.fromisoformat(iso8601))
  
def filetime_to_datetime(filetime: int) -> datetime:
  FILETIME_OF_1970_01_01 = 116444736000000000
  HUNDREDS_OF_NANOSECONDS = 10000000
  # Get seconds and remainder in terms of Unix epoch
  s, ns100 = divmod(filetime - FILETIME_OF_1970_01_01, HUNDREDS_OF_NANOSECONDS)
  # Convert to datetime object, with remainder as microseconds.
  return datetime.utcfromtimestamp(s).replace(microsecond=(ns100 // 10))

def b64(filename: str) -> str:
  with open( filename, "rb" ) as input_file:
    data = input_file.read()
    # It is suprisingly difficult to get a base64 string
    # b64encode returns a byte array. Converting that to a string with str()
    # adds crap to the string. We need to strip off the "b'" at the beginning
    # and the ' at the end.
    return str(base64.b64encode(data))[2:-1]

def create_event_type(t: truxton.TruxtonObject, id: int, name: str) -> None:
  event_type = t.neweventtype()
  event_type.id = id
  event_type.name = name
  event_type.save()
  return None

def create_artifact_type(t: truxton.TruxtonObject, id: int, shortname: str, longname: str) -> None:
  artifact_type = t.newartifacttype()
  artifact_type.id = id
  artifact_type.shortname = shortname
  artifact_type.longname = longname
  artifact_type.save()
  return None

def add_file(parent_truxton_file: truxton.TruxtonChildFileIO, filename: str) -> truxton.TruxtonChildFileIO:
  child = parent_truxton_file.newchild()
  with open(filename, "rb") as source_file:
    child.name = Path(filename).name
    shutil.copyfileobj(source_file, child)
    child.save()
  return child

def add_event(parent_file: truxton.TruxtonChildFileIO, start: str, end: str, title: str, description: str, type: int) -> truxton.TruxtonEvent:
  assert isinstance(parent_file, truxton.TruxtonChildFileIO)
  event = parent_file.newevent()
  assert isinstance(event, truxton.TruxtonEvent)
  event.start = datetime.fromisoformat(start)
  event.end = datetime.fromisoformat(end)
  event.title = title
  event.description = description
  event.type = type
  event.save()
  return event

def add_group(child_file: truxton.TruxtonChildFileIO, name: str) -> truxton.TruxtonArtifact:
  group = child_file.newartifact()
  group.type = truxton.ENTITY_TYPE_GROUP
  group.value = name
  group.datatype = truxton.DATA_TYPE_ASCII
  group.length = len(group.value)
  group.save()
  return group

def add_name_and_email(child_file: truxton.TruxtonChildFileIO, name: str, email: str) -> None:
  person = child_file.newartifact()
  person.type = truxton.ENTITY_TYPE_PERSON
  person.value = name
  person.datatype = truxton.DATA_TYPE_ASCII
  person.length = len(person.value)
  person.save()
  
  email_address = child_file.newartifact()
  email_address.type = truxton.ENTITY_TYPE_EMAIL_ADDRESS
  email_address.value = email
  email_address.datatype = truxton.DATA_TYPE_ASCII
  email_address.length = len(email_address.value)
  email_address.save()
  
  relation = child_file.newrelation();
  relation.a = email_address.id
  relation.atype = truxton.OBJECT_TYPE_ENTITY
  relation.b = person.id
  relation.btype = truxton.OBJECT_TYPE_ENTITY
  relation.relation = truxton.RELATION_MESSAGE_ADDRESS
  relation.save()
  return None
  
def entitle(old_title: str) -> str:
  event_title = old_title.replace("\r", " ").replace("\n", " ").replace("  ", " ")
   
  maximum_event_title_length = 50

  if ( len(event_title) > maximum_event_title_length ):
    event_title = event_title[0:maximum_event_title_length] + "..."

  return event_title
  
def mccabe_to_page(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  assert isinstance(parent_file, truxton.TruxtonChildFileIO)
  communication = parent_file.newcommunication()
  assert isinstance(communication, truxton.TruxtonCommunication)
  communication.sent = datetime.fromisoformat(sent);
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()
  
  mccabe_combined_id = communication.addparticipant(MCCABE_PHONE_NUMBER, "Andrew G. McCabe", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER)
  page_combined_id = communication.addparticipant(PAGE_PHONE_NUMBER, "Lisa C. Page", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER)
  communication.finished()
  
  global mccabe_page_associations_were_made

  if mccabe_page_associations_were_made == False:
    # Now associate the numbers with faces

    relation = parent_file.newrelation()
    assert isinstance(relation, truxton.TruxtonRelation)
    relation.a = mccabe_combined_id
    relation.atype = truxton.OBJECT_TYPE_COMBINED_ID
    relation.b = "00238955-133D-D2C1-A9E9-ADFF27FA80F4"
    relation.btype = truxton.OBJECT_TYPE_SUSPECT
    relation.relation = truxton.RELATION_COMBINED_ID
    relation.save()

    mccabe_page_associations_were_made = True

  event_time = communication.sent
  event_title = entitle("McCabe to Page: " + subject)

  add_event(parent_file, str(event_time), str(event_time), event_title, subject, EVENT_TYPE_MCCABE_PAGE_MESSAGE)

  return communication

def page_to_mccabe(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  communication = parent_file.newcommunication()
  communication.sent = datetime.fromisoformat(sent);
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  communication.addparticipant(MCCABE_PHONE_NUMBER, "Andrew G. McCabe", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.addparticipant(PAGE_PHONE_NUMBER, "Lisa Page", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.finished()
  event_time = communication.sent
  
  event_title = entitle("Page to McCabe: " + subject)
    
  add_event( parent_file, str(event_time), str(event_time), event_title, subject, EVENT_TYPE_MCCABE_PAGE_MESSAGE)
  return communication

def strzok_to_page(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  assert isinstance(parent_file, truxton.TruxtonChildFileIO)
  communication = parent_file.newcommunication()
  assert isinstance(communication, truxton.TruxtonCommunication)
  communication.sent = datetime.fromisoformat(sent);
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  strzok_combined_id = communication.addparticipant(STRZOK_PHONE_NUMBER, "Peter P. Strzok II", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER)
  page_combined_id = communication.addparticipant(PAGE_PHONE_NUMBER, "Lisa C. Page", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER)
  communication.finished()

  global strzok_page_associations_were_made

  if strzok_page_associations_were_made == False:
    # Now associate the numbers with faces

    relation = parent_file.newrelation()
    assert isinstance(relation, truxton.TruxtonRelation)
    relation.a = strzok_combined_id
    relation.atype = truxton.OBJECT_TYPE_COMBINED_ID
    relation.b = "01738955-133D-D2C1-A9E9-ADFF27FA80F4"
    relation.btype = truxton.OBJECT_TYPE_SUSPECT
    relation.relation = truxton.RELATION_COMBINED_ID
    relation.save()

    relation = parent_file.newrelation()
    relation.a = page_combined_id
    relation.atype = truxton.OBJECT_TYPE_COMBINED_ID
    relation.b = "01538955-133D-D2C1-A9E9-ADFF27FA80F4"
    relation.btype = truxton.OBJECT_TYPE_SUSPECT
    relation.relation = truxton.RELATION_COMBINED_ID
    relation.save()

    strzok_page_associations_were_made = True

  event_time = communication.sent
  event_title = entitle("Strzok to Page: " + subject)

  add_event(parent_file, str(event_time), str(event_time), event_title, subject, EVENT_TYPE_STRZOK_PAGE_MESSAGE)

  return communication

def strzok_to_page_unix_epoch(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  assert isinstance(parent_file, truxton.TruxtonChildFileIO)
  communication = parent_file.newcommunication()
  assert isinstance(communication, truxton.TruxtonCommunication)
  communication.sent = filetime_to_datetime(unix_millisecond_epoch_to_ticks(sent));
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  strzok_combined_id = communication.addparticipant(STRZOK_PHONE_NUMBER, "Peter P. Strzok II", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER)
  page_combined_id = communication.addparticipant(PAGE_PHONE_NUMBER, "Lisa C. Page", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER)
  communication.finished()
  
  event_time = communication.sent
  event_title = entitle("Strzok to Page: " + subject)
    
  add_event( parent_file, str(event_time), str(event_time), event_title, subject, EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  return communication

def page_to_strzok(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  communication = parent_file.newcommunication()
  communication.sent = datetime.fromisoformat(sent);
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  communication.addparticipant(STRZOK_PHONE_NUMBER, "Peter Strzok", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.addparticipant(PAGE_PHONE_NUMBER, "Lisa Page", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.finished()
  event_time = str(communication.sent)
  
  event_title = entitle("Page to Strzok: " + subject)
    
  add_event( parent_file, event_time, event_time, event_title, subject, EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  return communication

def page_to_strzok_unix_epoch(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  communication = parent_file.newcommunication()
  communication.sent = filetime_to_datetime(unix_millisecond_epoch_to_ticks(sent));
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  communication.addparticipant(STRZOK_PHONE_NUMBER, "Peter Strzok", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.addparticipant(PAGE_PHONE_NUMBER, "Lisa Page", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.finished()

  event_time = communication.sent
  
  event_title = entitle("Page to Strzok: " + subject)

  add_event( parent_file, str(event_time), str(event_time), event_title, subject, EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  return communication

def mccabe_to_page_unix_epoch(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  assert isinstance(parent_file, truxton.TruxtonChildFileIO)
  communication = parent_file.newcommunication()
  assert isinstance(communication, truxton.TruxtonCommunication)
  communication.sent = filetime_to_datetime(unix_millisecond_epoch_to_ticks(sent));
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  strzok_combined_id = communication.addparticipant(STRZOK_PHONE_NUMBER, "Peter P. Strzok II", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER)
  page_combined_id = communication.addparticipant(PAGE_PHONE_NUMBER, "Lisa C. Page", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER)
  communication.finished()
  
  event_time = communication.sent
  event_title = entitle("Strzok to Page: " + subject)
    
  add_event( parent_file, str(event_time), str(event_time), event_title, subject, EVENT_TYPE_STRZOK_PAGE_MESSAGE)
  return communication

def unknown_to_strzok(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  communication = parent_file.newcommunication()
  communication.sent = datetime.fromisoformat(sent);
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  communication.addparticipant(STRZOK_PHONE_NUMBER, "Peter Strzok", truxton.MESSAGE_PARTICIPANT_TO, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.finished()
  return communication

def strzok_to_unknown(parent_file: truxton.TruxtonChildFileIO, sent: str, subject: str) -> truxton.TruxtonCommunication:
  communication = parent_file.newcommunication()
  communication.sent = datetime.fromisoformat(sent);
  communication.received = communication.sent
  communication.subject = subject
  communication.type = truxton.MESSAGE_TYPE_SMS
  communication.save()

  communication.addparticipant(STRZOK_PHONE_NUMBER, "Peter Strzok", truxton.MESSAGE_PARTICIPANT_FROM, truxton.ENTITY_TYPE_PHONE_NUMBER )
  communication.finished()
  return communication

if __name__ == "__main__":
  main()

# If Azra Turk was FBI, why is there no 302?

# Flynn/Kislyak call leaked to Adam Entous of Washington Post on Jan 5, 2017... https://technofog.substack.com/p/revisiting-the-flynnkislyak-leak
# Lots of details https://theconservativetreehouse.com/blog/2018/07/23/indicted-senate-staffer-james-wolfe-leaked-a-2017-copy-of-full-fisa-warrant-against-carter-page-to-reporter-ali-watkins/
