import sys
import json
sys.path.append('C:/Program Files/Truxton/SDK')
import truxton

# Only enumerate PDF files (Type_Adobe_PDF)

def files(media: truxton.TruxtonMedia) -> None:
 files_in_media = trux.newenumerator()
 files_in_media.scope = truxton.Type_Media
 files_in_media.scopeid = media.id
 files_in_media.target = truxton.Type_File
 files_in_media.filetype = truxton.Type_Adobe_PDF

 for file_information in files_in_media:
  output_file(file_information)

trux = truxton.create()
content_status_names = json.loads(trux.contentstatusnames())
media_status_names = json.loads(trux.mediastatusnames())
media_type_names = json.loads(trux.mediatypenames())
origin_names = json.loads(trux.originnames())
file_type_names = json.loads(trux.filetypenames())
file_mime_types = json.loads(trux.filemimetypes())

def main() -> None:
 investigations = trux.newenumerator()
 investigations.target = truxton.Type_Investigation

 print("[")
 instance = 0
 for investigation in investigations:
  dump_investigation(investigation, instance)
  instance += 1
 print("]")
 
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

if __name__ == "__main__":
 sys.exit(main())
