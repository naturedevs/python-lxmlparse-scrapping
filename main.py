from lxml import etree
import json
import copy

initdata = {
    "statusType":"",
    "statusDateTime":"",
    "mime_type":"",
    "focus_value":"",
    "product_category_value":"",
    "publication_datetime":"",
    "org_details"    : {
        "OrganizationName": "",
        "OrganizationType": "",
        "People": [],
    },
    "sector_data"    : [],
    "securities"     : [],
    "region_data"    : [],
    "regions"        : [],
    "subject"        : "",
    "synopsis"       : "",
    "title"          : "",
    "url"            : "",
}
data = {}
def etree_to_dict(tree):
    root = tree.getroot()
    return {root.tag: _element_to_dict(root)}

def basetag(tag):
    return tag.split("}")[-1]

def _element_to_dict(element):
    result = {}
    for child in element:
        child_dict = _element_to_dict(child)
        # print(dir(child))
        # print(basetag(child.tag))
        if basetag(child.tag) == "OrganizationName" and child_dict["@attributes"]["nameType"] == "Display":
            # print(child_dict)
            data["org_details"]["OrganizationName"] = child_dict["text"]
        elif basetag(child.tag) == "Organization" and child_dict["@attributes"]["primaryIndicator"] == "Yes":
            data["org_details"]["OrganizationType"] = child_dict["@attributes"]["type"]
        elif basetag(child.tag) == "PersonGroupMember":
            person = {}
            person["CountryCode"] = child_dict["Person"][0]["ContactInfo"][0]["Phone"][0]["CountryCode"][0]["text"]
            person["Email"] = child_dict["Person"][0]["ContactInfo"][0]["Email"][0]["text"]
            person["FamilyName"] = child_dict["Person"][0]["FamilyName"][0]["text"]
            person["GivenName"] = child_dict["Person"][0]["GivenName"][0]["text"]
            person["JobRole"] = child_dict["Person"][0]["JobTitle"][0]["text"]
            person["Division"] = child_dict["Person"][0]["Division"][0]["text"]
            person["PersonID"] = child_dict["Person"][0]["@attributes"]["personID"]
            person["PhoneNumber"] = child_dict["Person"][0]["ContactInfo"][0]["Phone"][0]["Number"][0]["text"]
            # print(child_dict["Person"][0]["ContactInfo"][0]["Email"][0]["text"])
            data["org_details"]["People"].append(person)
        elif basetag(child.tag) == "Region":
            region = {}
            region["primaryIndicator"] = child_dict["@attributes"]["primaryIndicator"]
            region["regionType"] = child_dict["@attributes"]["regionType"]
            data["region_data"].append(region)
        elif basetag(child.tag) == "ProductClassifications":
            for SectorIndustry in child_dict["SectorIndustry"] if "SectorIndustry" in child_dict else []: 
                sector = {}
                sector["classificationType"] = SectorIndustry["@attributes"]["classificationType"]
                sector["code"] = SectorIndustry["@attributes"]["code"]
                sector["focusLevel"] = SectorIndustry["@attributes"]["focusLevel"]
                sector["level"] = SectorIndustry["@attributes"]["level"]
                sector["name"] = SectorIndustry["Name"][0]["text"]
                sector["primaryIndicator"] = SectorIndustry["@attributes"]["primaryIndicator"]
                data["sector_data"].append(sector)
        elif basetag(child.tag) == "Content":
            
            data["mime_type"] = child_dict["Resource"][0]["MIMEType"][0]["text"] if "MIMEType" in child_dict["Resource"][0] else ""
            data["title"] = child_dict["Title"][0]["text"]
            data["synopsis"] = child_dict["Synopsis"][0]["text"]
            data["url"] = child_dict["Resource"][0]["URL"][0]["text"] if "URL" in child_dict["Resource"][0] else ""
            data["data"] = child_dict["Resource"][0]["Data"][0]["text"] if "Data" in child_dict["Resource"][0] else ""
        elif basetag(child.tag) == "StatusInfo":
            data["statusType"] = child_dict["@attributes"]["statusType"]
            data["statusDateTime"] = child_dict["@attributes"]["statusDateTime"]
        
        elif basetag(child.tag) == "Issuer":
            data["Issuer"] = {
                "securities" : []
            }
            security = {}
            security["IssuerName"] = child_dict["IssuerName"][0]["NameValue"][0]["text"]
            # security["Description"] = child_dict["Description"][0]["text"]
            security["SecurityName"] = child_dict["SecurityDetails"][0]["Security"][0]["SecurityFinancials"][0]["@attributes"]["displayName"]
            security["SecurityType"] = child_dict["SecurityDetails"][0]["Security"][0]["SecurityType"][0]["@attributes"]["securityType"]
            security["AssetClass"] = child_dict["SecurityDetails"][0]["Security"][0]["AssetClass"][0]["@attributes"]["assetClass"]
            security["AssetType"] = child_dict["SecurityDetails"][0]["Security"][0]["AssetType"][0]["@attributes"]["assetType"]
            for securityid in child_dict["SecurityDetails"][0]["Security"][0]["SecurityID"]:
                security["SecurityID_" + securityid["@attributes"]["idType"]] = securityid["@attributes"]["idValue"]
            data["Issuer"]["securities"].append(security)
        
        elif basetag(child.tag) == "ProductDetails":
            data["focus_value"] = child_dict["ProductFocus"][0]["@attributes"]["focus"]
            data["product_category_value"] = child_dict["ProductCategory"][0]["@attributes"]["productCategory"]
            data["publication_datetime"] = child_dict["@attributes"]["publicationDateTime"]
        
        if basetag(child.tag) not in result:
            result[basetag(child.tag)] = []
        result[basetag(child.tag)].append(child_dict)
    if element.attrib:
        result["@attributes"] = element.attrib
    if element.text:
        result["text"] = element.text
    return result

# json_data = json.dumps(xml_data, indent=4)
# print(xml_data)
# print(json_data)
data1 = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

for i in range(1,6):
    print(i)
    tree = etree.parse("resource/ex" + str(i) + ".xml")
    data = copy.deepcopy(initdata)
    xml_data = etree_to_dict(tree)
    json_data = json.dumps(data, indent=4)
    output = str(i) + ".txt"
    # Save the JSON data to a file
    with open(output, 'w') as file:
        file.write(json_data)