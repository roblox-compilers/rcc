import log, requests, json, os, zipfile
# Download from wally 
info = log.info
error = log.error

def get(author, name, isDependant=False):
    # Use wally and download the zip and unpack it
    info(f"Getting @{author}/{name} metadata")
    wallyurl = "https://api.wally.run/v1/"

    # first get package metadata should look like:
    metadataurl = wallyurl+"package-metadata/"+author+"/"+name
    data = requests.get(metadataurl).text
    jsondata = json.loads(data)
    
    if 'message' in jsondata:
        error("wally raised, " + jsondata["message"])
    jsondata = json.loads(data)["versions"]
    #get latest version and dependencies
    latestver = jsondata[0]
    vernum = latestver["package"]["version"]
    dependencies = latestver["dependencies"]
    
    for i in dependencies:
        dependency = dependencies[i]
        print("Downloading dependency "+dependency+"...")
        get(dependency.split("/")[0], dependency.split("/")[1].split("@")[0], True)

    # Download the package
    if not isDependant:
        info(f"Downloading @{author}/{name} v{vernum}")
    url = wallyurl+"/package-contents/"+author+"/"+name+"/"+vernum
    headers = {"Wally-Version": "1.0.0"} 
    response = requests.get(url, headers=headers).content
    
    # create new file in cwd/dependencies called author_name_version.zip and unzip it
    info("Saving package...")
    #### if dependencies folder doesnt exist, create it
    if not os.path.exists(os.path.join(os.getcwd(), "include")):
        os.makedirs(os.path.join(os.getcwd(), "include"))
    ####
    open(os.path.join(os.getcwd(), "include", "@"+author+"."+name+".zip"), "x").close()
    with open(os.path.join(os.getcwd(), "include", "@"+author+"."+name+".zip"), "wb") as file:
        file.write(response)
    # unzip
    info("Unzipping package...")
    with zipfile.ZipFile(os.path.join(os.getcwd(), "include", "@"+author+"."+name+".zip"), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(os.getcwd(), "include", "@"+author+"."+name))
    # delete the zip
    info("Deleting uneeded resources...")
    os.remove(os.path.join(os.getcwd(), "include", "@"+author+"."+name+".zip"))