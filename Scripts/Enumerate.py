# This script demonstrates how to enumerate things in Truxton

# This will convert all of the items in Truxton to JSON format

import sys
import json
sys.path.append('C:/Program Files/Truxton/SDK')
import truxton

trux = truxton.create()
artifact_type_names = json.loads(trux.entitytypenames())
content_status_names = json.loads(trux.contentstatusnames())
data_type_names = json.loads(trux.datatypenames())
event_type_names = json.loads(trux.eventtypenames())
location_type_names = json.loads(trux.locationtypenames())
media_status_names = json.loads(trux.mediastatusnames())
media_type_names = json.loads(trux.mediatypenames())
message_type_names = json.loads(trux.messagetypenames())
object_type_names = json.loads(trux.objecttypenames())
origin_names = json.loads(trux.originnames())
participant_type_names = json.loads(trux.messageaddresstypenames())
url_method_names = json.loads(trux.websitevisitmethodnames())
url_type_names = json.loads(trux.urltypenames())
file_type_names = json.loads(trux.filetypenames())
file_mime_types = json.loads(trux.filemimetypes())

def main():
 investigations = trux.newenumerator()
 investigations.target = truxton.Type_Investigation

 print("[")
 instance = 0
 for investigation in investigations:
  dump_investigation(investigation, instance)
  instance += 1
 print("]")
 
def get_citation(enumerator: truxton.TruxtonEnumeration) -> dict:
 citation = dict()

 if enumerator.currentfile is not None:
  md5 = dict()
  md5["algorithm"] = "md5"
  
  if enumerator.currentfile.md5 is not None:
   md5["value"] = enumerator.currentfile.md5.upper()

  sha1 = dict()
  sha1["algorithm"] = "sha1"
  
  if enumerator.currentfile.sha1 is not None:
   sha1["value"] = enumerator.currentfile.sha1.upper()

  hashes = []
  hashes.append(md5)
  hashes.append(sha1)

  file_citation = dict()
  file_citation["id"] = enumerator.currentfile.id.lower()
  file_citation["hash"] = hashes

  citation["file"] = file_citation

 if enumerator.currentmedia is not None:
  media_citation = dict()
  media_citation["id"] = enumerator.currentmedia.id.lower()
  media_citation["created"] = F"{enumerator.currentmedia.created:%Y-%m-%dT%H:%M:%SZ}"
  citation["media"] = media_citation

  return citation

def artifact_dictionary(artifact: truxton.TruxtonArtifact) -> dict:
 d = dict()
 d["id"] = artifact.id
 d["datatype"] = str(artifact.datatype)
 d["datatypename"] = data_type_names[str(artifact.datatype)]
 d["mediaid"] = artifact.mediaid.lower()
 d["fileid"] = artifact.fileid.lower()
 d["length"] = str(artifact.length)
 d["objectid"] = artifact.objectid.lower()
 d["objecttype"] = str(artifact.objecttype)
 d["objecttypename"] = object_type_names[str(artifact.objecttype)]
 d["offset"] = str(artifact.offset)
 d["type"] = str(artifact.type)
 d["typename"] = artifact_type_names[str(artifact.type)]
 d["value"] = artifact.value

 object_name = dict()
 object_name["artifact"] = d;
 return object_name

def communication_dictionary(communication: truxton.TruxtonCommunication) -> dict:
 d = dict()
 d["id"] = communication.id
 d["mediaid"] = communication.mediaid.lower()
 d["fileid"] = communication.fileid.lower()
 d["received"] = F"{communication.received:%Y-%m-%dT%H:%M:%SZ}"
 d["sent"] = F"{communication.sent:%Y-%m-%dT%H:%M:%SZ}"
 d["type"] = str(communication.type)
 d["typename"] = message_type_names[str(communication.type)]
 d["subject"] = communication.subject

 message_bodies = trux.newenumerator()
 message_bodies.scope = truxton.Type_Message
 message_bodies.scopeid = communication.id
 message_bodies.target = truxton.Type_Message_Body

 b = []

 for message_body in message_bodies:
  b.append(file_dictionary(message_body))

 d["bodies"] = b

 message_attachments = trux.newenumerator()
 message_attachments.scope = truxton.Type_Message
 message_attachments.scopeid = communication.id
 message_attachments.target = truxton.Type_Message_Attachment

 a = []

 for message_attachment in message_attachments:
  a.append(file_dictionary(message_attachment))

 d["attachments"] = a

 object_name = dict()
 object_name["message"] = d;

 participants(communication)

 return object_name

def event_dictionary(event: truxton.TruxtonEvent) -> dict:
 d = dict()
 d["id"] = event.id
 d["type"] = str(event.type)
 d["typename"] = event_type_names[str(event.type)]
 d["start"] = F"{event.start:%Y-%m-%dT%H:%M:%SZ}"
 d["end"] = F"{event.end:%Y-%m-%dT%H:%M:%SZ}"
 d["title"] = event.title
 d["description"] = event.description
 d["mediaid"] = event.mediaid.lower()
 d["fileid"] = event.fileid.lower()

 object_name = dict()
 object_name["event"] = d;
 return object_name
 
def exif_dictionary(camera_information: truxton.TruxtonEXIF) -> None:
 d = dict()
 d["id"] = camera_information.id
 d["mediaid"] = camera_information.mediaid.lower()
 d["fileid"] = camera_information.fileid.lower()
 d["make"] = camera_information.make
 d["model"] = camera_information.model
 d["bodyserialnumber"] = camera_information.bodyserialnumber
 d["latitude"] = str(camera_information.latitude)
 d["longitude"] = str(camera_information.longitude)
 d["altitude"] = str(camera_information.altitude)
 d["heading"] = str(camera_information.heading)
 d["focallength"] = str(camera_information.focallength)
 d["shuttercount"] = str(camera_information.shuttercount)
 d["gpstime"] = F"{camera_information.gpstime:%Y-%m-%dT%H:%M:%SZ}"
 d["devicetime"] = F"{camera_information.devicetime:%Y-%m-%dT%H:%M:%SZ}"
 d["offset"] = str(camera_information.offset)

 object_name = dict()
 object_name["exif"] = d
 return object_name

def file_dictionary(file_information: truxton.TruxtonFileIO) -> dict:
 d = dict()
 d["id"] = file_information.id.lower()
 d["mediaid"] = file_information.mediaid.lower()
 d["name"] = file_information.name
 d["accessed"] = F"{file_information.accessed:%Y-%m-%dT%H:%M:%SZ}"
 d["created"] = F"{file_information.created:%Y-%m-%dT%H:%M:%SZ}"
 d["modified"] = F"{file_information.modified:%Y-%m-%dT%H:%M:%SZ}"
 d["attributes"] = file_information.attributes
 d["children"] = file_information.children
 d["diskoffset"] = file_information.diskoffset
 d["entropy"] = file_information.entropy
 d["originid"] = file_information.origin
 d["origin"] = origin_names[str(file_information.origin)]
 d["parentid"] = file_information.parentid.lower()
 d["path"] = file_information.path
 d["size"] = file_information.size
 d["status"] = content_status_names[str(file_information.status)]
 type_dict = dict()
 type_dict["id"] = file_information.type
 type_dict["name"] = file_type_names[str(file_information.type)]
 type_dict["mimetype"] = file_mime_types[str(file_information.type)]
 d["type"] = type_dict

 md5 = dict()
 md5["algorithm"] = "md5"
 md5["value"] = file_information.md5.lower()

 sha1 = dict()
 sha1["algorithm"] = "sha1"
 sha1["value"] = file_information.sha1.lower()

 hashes = []
 hashes.append(md5)
 hashes.append(sha1) 

 d["hash"] = hashes
 return d

def output_file(file_information: truxton.TruxtonFileIO) -> None:
 object_name = dict()
 object_name["file"] = file_dictionary(file_information);

 print("," + json.dumps(object_name, ensure_ascii = False, sort_keys = True))

def output_investigation(investigation: truxton.TruxtonInvestigation, instance: int) -> None:
 if instance > 0:
  print(",")

 d = dict()
 d["id"] = investigation.id.lower()
 d["name"] = investigation.name
 d["case"] = investigation.case
 d["description"] = investigation.description
 d["jurisdiction"] = str(investigation.jurisdiction)
 d["opened"] = F"{investigation.opened:%Y-%m-%dT%H:%M:%SZ}"
 d["status"] = str(investigation.status)
 d["type"] = str(investigation.type)

 object_name = dict()
 object_name["investigation"] = d;
 print(json.dumps(object_name, ensure_ascii = False, sort_keys = True))

def location_dictionary(location: truxton.TruxtonLocation) -> dict:
 d = dict()
 d["id"] = location.id.lower()
 d["mediaid"] = location.mediaid.lower()
 d["fileid"] = location.fileid.lower()
 d["type"] = str(location.type)
 d["typename"] = location_type_names[str(location.type)]
 d["when"] = F"{location.when:%Y-%m-%dT%H:%M:%SZ}"
 d["label"] = location.label
 d["latitude"] = str(location.latitude)
 d["longitude"] = str(location.longitude)
 d["altitude"] = str(location.altitude)
 # d["source"] = get_citation()

 object_name = dict()
 object_name["location"] = d;
 return object_name

def output_media(media: truxton.TruxtonMedia) -> None:
 d = dict()
 d["id"] = media.id.lower()
 d["name"] = media.name
 d["case"] = media.case
 d["loadconfiguration"] = str(media.configid)
 d["created"] = F"{media.created:%Y-%m-%dT%H:%M:%SZ}"
 d["description"] = media.description
 d["evidencebag"] = media.evidencebag
 d["expires"] = F"{media.expires:%Y-%m-%dT%H:%M:%SZ}"
 d["generatedfolderid"] = media.generatedfolderid.lower()
 d["latitude"] = str(media.latitude)
 d["longitude"] = str(media.longitude)
 d["originator"] = media.originator
 d["percentcomplete"] = str(media.percentcomplete)
 d["rootid"] = media.rootid.lower()
 d["status"] = str(media.status)
 d["statusname"] = media_status_names[str(media.status)]
 d["type"] = str(media.type)
 d["typename"] = media_type_names[str(media.type)]
 d["updated"] = F"{media.updated:%Y-%m-%dT%H:%M:%SZ}"

 object_name = dict()
 object_name["media"] = d;
 print("," + json.dumps(object_name, ensure_ascii = False, sort_keys = True))

def output_participant(participant: truxton.TruxtonMessageParticipant) -> None:
 d = dict()
 d["id"] = participant.id.lower()
 d["mediaid"] = participant.mediaid.lower()
 d["fileid"] = participant.fileid.lower()
 d["type"] = str(participant.type)
 d["typename"] = participant_type_names[str(participant.type)]
 d["account"] = participant.account
 d["combinedguid"] = participant.combinedguid.lower()
 d["combinedid"] = str(participant.combinedid)
 d["messageaddressid"] = participant.messageaddressid.lower()
 d["messageid"] = participant.messageid.lower()
 d["name"] = participant.name
 d["server"] = participant.server

 object_name = dict()
 object_name["participant"] = d;
 print("," + json.dumps(object_name, ensure_ascii = False, sort_keys = True))

def url_dictionary(url: truxton.TruxtonUrl) -> None:
 d = dict()
 d["id"] = url.id.lower()
 d["mediaid"] = url.mediaid.lower()
 d["fileid"] = url.fileid.lower()
 d["account"] = url.account
 d["accountoffset"] = str(url.accountoffset)
 d["format"] = str(url.format)
 d["localfilename"] = url.localfilename
 d["method"] = str(url.method)
 d["methodname"] = url_method_names[str(url.method)]
 d["offset"] = str(url.offset)
 d["type"] = str(url.type)
 d["typename"] = url_type_names[str(url.type)]
 d["url"] = url.url
 d["when"] = F"{url.when:%Y-%m-%dT%H:%M:%SZ}"

 object_name = dict()
 object_name["url"] = d;

 return object_name
 
def artifacts(media: truxton.TruxtonMedia) -> None:
 artifacts_in_media = trux.newenumerator()
 artifacts_in_media.scope = truxton.Type_Media
 artifacts_in_media.scopeid = media.id
 artifacts_in_media.target = truxton.Type_Artifact

 for artifact in artifacts_in_media:
  d = artifact_dictionary(artifact)
  d["artifact"]["source"] = get_citation(artifacts_in_media)
  print("," + json.dumps(d, ensure_ascii = False, sort_keys = True))

def communication(media: truxton.TruxtonMedia) -> None:
 communications_in_media = trux.newenumerator()
 communications_in_media.scope = truxton.Type_Media
 communications_in_media.scopeid = media.id
 communications_in_media.target = truxton.Type_Message

 for communication in communications_in_media:
  d = communication_dictionary(communication)
  d["message"]["source"] = get_citation(communications_in_media)
  print("," + json.dumps(d, ensure_ascii = False, sort_keys = True))

def events(media: truxton.TruxtonMedia) -> None:
 events_in_media = trux.newenumerator()
 events_in_media.scope = truxton.Type_Media
 events_in_media.scopeid = media.id
 events_in_media.target = truxton.Type_Event

 for e in events_in_media:
  d = event_dictionary(e)
  d["event"]["source"] = get_citation(events_in_media)
  print("," + json.dumps(d, ensure_ascii = False, sort_keys = True))

def exif(media: truxton.TruxtonMedia) -> None:
 exif_in_media = trux.newenumerator()
 exif_in_media.scope = truxton.Type_Media
 exif_in_media.scopeid = media.id
 exif_in_media.target = truxton.Type_Camera_Information

 for camera_information in exif_in_media:
  d = exif_dictionary(camera_information)
  d["exif"]["source"] = get_citation(exif_in_media)
  print("," + json.dumps(d, ensure_ascii = False, sort_keys = True))

def files(media: truxton.TruxtonMedia) -> None:
 files_in_media = trux.newenumerator()
 files_in_media.scope = truxton.Type_Media
 files_in_media.scopeid = media.id
 files_in_media.target = truxton.Type_File

 for file_information in files_in_media:
  output_file(file_information)

def locations(media: truxton.TruxtonMedia) -> None:
 locations_in_media = trux.newenumerator()
 locations_in_media.scope = truxton.Type_Media
 locations_in_media.scopeid = media.id
 locations_in_media.target = truxton.Type_Location

 for location in locations_in_media:
  d = location_dictionary(location)
  d["location"]["source"] = get_citation(locations_in_media)
  print("," + json.dumps(d, ensure_ascii = False, sort_keys = True))

def participants(communication: truxton.TruxtonCommunication) -> None:
 participants_in_message = trux.newenumerator()
 participants_in_message.scope = truxton.Type_Message
 participants_in_message.scopeid = communication.id
 participants_in_message.target = truxton.Type_Participant

 for participant in participants_in_message:
  output_participant(participant)

def urls(media: truxton.TruxtonMedia) -> None:
 urls_in_media = trux.newenumerator()
 urls_in_media.scope = truxton.Type_Media
 urls_in_media.scopeid = media.id
 urls_in_media.target = truxton.Type_Website_Visit

 for url in urls_in_media:
  d = url_dictionary(url)
  d["url"]["source"] = get_citation(urls_in_media)
  print("," + json.dumps(d, ensure_ascii = False, sort_keys = True))

def dump_investigation(investigation: truxton.TruxtonInvestigation, instance: int) -> None:
 output_investigation(investigation, instance)

 investigation_media = trux.newenumerator()
 investigation_media.scope = truxton.Type_Investigation
 investigation_media.scopeid = investigation.id
 investigation_media.target = truxton.Type_Media

 for media in investigation_media:
  dump_media(media)

def dump_media(media: truxton.TruxtonMedia) -> None:
 output_media(media)
 files(media)
 artifacts(media)
 events(media)
 locations(media)
 urls(media)
 exif(media)
 communication(media)

if __name__ == "__main__":
 sys.exit(main())
