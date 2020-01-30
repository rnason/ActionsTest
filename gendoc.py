############
# Imports: #
############
# Import Pip Installed Modules:
from jinja2 import Template, Environment, FileSystemLoader
from termcolor import colored, cprint
import hcl, yaml, requests
'''from github import Github'''

# Import Base Python Modules
from datetime import datetime
from pathlib import Path
import json, os, sys, ntpath, logging

logging.basicConfig(filename='gendoc.log', filemode='w', format='%(levelname)s:    %(message)s', level=logging.DEBUG)


##############
# Functions: #
##############
def FetchGithubData(RepoURL, AccessToken=None):
    '''Function that will collect repo information from githubs API'''
    try:
        # Make the request to fetch the repo info
        # GH = Github("1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234")
        # RepoData = GH.get_repo("{}/{}".format(NameSpace, RepoName))
        # print(RepoData)

        # If an AccessToken was passed then create the header.
        if AccessToken is not None:
            headers = {'Authorization': 'token {}'.format(AccessToken)}
        else:
            headers = {}
        logging.debug("Github repository request headers have been set.")
        
        # Make the request
        logging.info("Sending Github repository request...")
        r = requests.get(RepoURL, headers=headers)
        response = json.loads(r.text)
        logging.info("GitHub Request Response Code: [{}]".format(r.status_code))
        logging.debug("GitHub Request Response Message: {}".format(json.dumps(response, indent=4, sort_keys=True)))

        # Check the response code, if 200 then return data, if not 200 return error.
        if r.status_code == 200:
            return response
        else:
            cprint(" WARNING ENCOUNTERED: ", 'grey', 'on_yellow')
            cprint("Error encountered attempting to the Github request to: {}".format(RepoURL), 'yellow')
            cprint("GitHub repo data will be unavailable when rendering documentation.\n", 'yellow')
            cprint("GitHub Response Code: [{}]".format(r.status_code), 'blue')
            cprint("GitHub Response Message: {}\n".format(json.dumps(response, indent=4, sort_keys=True)), 'blue')
            logging.warning("Unable to retrieve repository details from GitHub:")
            logging.warning("GitHub repository data will not be availabe for generating the repo documentation.")
            return "INVALID_RESPONSE: {}/{}".format(r.status_code, response)
    except Exception as e:
        cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error encountered attempting to send repository request to Github:\n\nException: {}".format(str(e)), 'red')
        logging.error("Unknown Exception occurred: {}".format(str(e)))
        logging.error("GitHub Repository data will not be used to construct the repo documentation")
        pass


def BuildDirTree(DirPath: Path, DirPrefix: str=''):
    try:
        # Designate Directory Tree Prefix Symbols
        SpacePrefix =  '    '
        BranchPrefix = '│   '
        TeePrefix =    '├── '
        FinalPrefix =   '└── '

        # Create the Directory List
        Contents = list(DirPath.iterdir())
        # Remove virtualenv and git directories, as these won't be committed to the repo and shouldn't be in the module documentation.
        for item in Contents:
            if 'venv' in str(item) or '.git' in str(item):
                Contents.remove(item)
        # Set Pointers
        Pointers = [TeePrefix] * (len(Contents) - 1) + [FinalPrefix]
        # Build the Tree Generator
        for Pointer, Path in zip(Pointers, Contents):
            yield DirPrefix + Pointer + Path.name
            if Path.is_dir():
                Extension = BranchPrefix if Pointer == TeePrefix else SpacePrefix 
                yield from BuildDirTree(Path, DirPrefix=DirPrefix+Extension)
    except Exception as e:
        cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Error encountered attempting to build directory tree:\n\nException: {}".format(str(e)), 'red')
        logging.error("Unknown Exception occurred attempting to build the directory structure tree:")
        logging.error(str(e))
        pass


##########################
# Load Yaml Config File: #
##########################
try:
    # Check if an argument was given. sys.argv[0] is the script name.
    if len(sys.argv) > 1:
        ConfigFile = sys.argv[1]
        # Verify the file path that was given is valid.
        if os.path.exists(ConfigFile):
            logging.debug("Using provided config file: [{}]".format(ConfigFile))
            try:
                # Separate the file name from the given path, then, validate the extention.
                ConfigFilePath, ConfigFileName = ntpath.split(ConfigFile)
                logging.debug("Config File Path: [{}]".format(ConfigFilePath))
                logging.debug("Config File Name: [{}]".format(ConfigFileName))
                ConfigFileExt = os.path.splitext(ConfigFileName)[1]
                logging.debug("Config File Extension: [{}]".format(ConfigFileExt))
                
                # Verify that the file passed has the .yaml or .yml extension
                if ConfigFileExt == '.yaml' or ConfigFileExt == '.yml':
                    # Attempt to open the file, err on exception
                    with open(ConfigFile) as YamlFile:
                        Config = yaml.load(YamlFile, Loader=yaml.FullLoader)
                    logging.info("Config loaded successfully from given file path.")
                    logging.debug(Config)
                else:
                    # If the passed file name isn't a yaml file
                    cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
                    cprint("Error encountered attempting to open the specified config file: [{}]".format(ConfigFile), 'red')
                    cprint("Invalid file type specified. Config file must be of type .yaml or .yml\n", 'red')
                    logging.error("Invalid file specified. Config file must be of type .yaml or .yml")
                    sys.exit()
            except Exception as e:
                cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
                cprint("Exception encountered attempting to open the specified config file: [{}]\n\nException: {}\n".format(ConfigFile, str(e)), 'red')
                logging.error("Unable to open the specified config file path.")
                logging.error(str(e))
                raise
        else:
            cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
            cprint("Error encountered attempting to open the specified file: [{}]".format(ConfigFile), 'red')
            cprint("The specified file: [{}] was not found. Please verify the given file path and try again.\n".format(ConfigFile), 'red')
            logging.error("The provided file: [{}] was either not found or is not a valid file.".format(ConfigFile))
            sys.exit()
    else:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("Required config file path argument not provided.\n", 'red')
        cprint("Example: python gendoc.py gendoc.yaml\n", 'blue')
        logging.error("No Config file path was provided. GenDoc must be provided a properly formatted <configfile>.yaml file.")
        sys.exit()
except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to open the specified config file:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unknown Exception occurred: {}".format(str(e)))
    raise


##########################
# Fetch Repo Info:       #
##########################
try:
    # Construct the Github API URL, and then call the FetchGithubData() to get Repo Data
    RepoConfig = Config.get('Repository')
    GithubApiUrl = "https://api.github.com/repos/{}/{}".format(RepoConfig.get('NameSpace'), RepoConfig.get('RepoName'))
    logging.info("Setting GitHub API URL: {}".format(GithubApiUrl))

    # TODO: Do some better checking to validate the token, like length or some other check.
    # If only using Github Actions, then this may not even be necessary.
    if len(sys.argv) == 3:
        AccessToken = sys.argv[2]
        logging.info("AccessToken: Provided")
    else:
        AccessToken = None
        logging.info("AccessToken: Not Provided")

    # Make a request to Github for repository details.
    logging.info("Attempting request to Github for repository details...")
    RepoBaseData = FetchGithubData(GithubApiUrl, AccessToken)
    # Set a flag to include or exclude repository data
    if 'INVALID_RESPONSE' in RepoBaseData:
        IncludeRepoData = False
    else:
        IncludeRepoData = True

    # Make a request to Github for repository releases.
    GithubApiUrl = "{}/releases/latest".format(GithubApiUrl)
    logging.info("Attempting request to Github for repository releases...")
    RepoReleaseData = FetchGithubData(GithubApiUrl, AccessToken)
    # Set a flag to include or exclude release data
    if 'INVALID_RESPONSE' in RepoReleaseData:
        IncludeReleaseData = False
    else:
        IncludeReleaseData = True
except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to set GitHub API URL:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unknown Exception occurred attempting to set the GitHub API URL: {}".format(str(e)))
    raise


#########################
# Load Jinja Templates: #
#########################
try:
    if os.path.isdir('./templates'):
        # Set Jinja Templates
        logging.debug("./templates directory FOUND.. Loading Templates....")
        TplLoader = FileSystemLoader('templates')
        Templates = Environment(loader=TplLoader, trim_blocks=True, lstrip_blocks=True)

        # Load ReadMe if template exists
        if os.path.exists('./templates/README.j2'):
            ReadMeTpl = Templates.get_template('README.j2')
            logging.info("README jinja template loaded successfully.")
        else:
            cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
            cprint("The expected README.j2 jinja2 template file was not found in the ./templates directory.\n", 'red')
            logging.info("The expected README.j2 jinja2 template file was not found in the ./templates directory.")
            sys.exit()
        
        # Load Changelog if template exists
        if os.path.exists('./templates/CHANGELOG.j2'):
            ChangeLogTpl = Templates.get_template('CHANGELOG.j2')
            logging.info("CHANGELOG jinja template loaded successfully.")
        else:
            cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
            cprint("The expected CHANGELOG.j2 jinja2 template file was not found in the ./templates directory.\n", 'red')
            logging.info("The expected CHANGELOG.j2 jinja2 template file was not found in the ./templates directory.")
            sys.exit()
    else:
        cprint(" ERROR ENCOUNTERED: ", 'grey', 'on_red')
        cprint("The required ./templates directory was not found.\n", 'red')
        logging.error("The required ./templates directory was not found")
        sys.exit()
except (OSError, IOError) as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to load jinja templates:\n\nException: {} NOT FOUND!\n".format(str(e)), 'red')
    logging.error("Unable to load jinja template: {}".format(str(e)))
    raise


############################################
# Construct Template Variables Dictionary: #
############################################
try:
    logging.debug("Constructing Template Variable Dictionary...")
    TemplateDict = {}
    TemplateDict.update(Config=Config)
    logging.debug("Config added under [Config] key")

    if IncludeRepoData:
        TemplateDict.update(Repo=RepoBaseData)
        logging.debug("Repository Data added under [Repo] key")
    else:
        TemplateDict.update(Repo={})
        logging.debug("Repository Data excluded from variable dictionary")

    if IncludeReleaseData:
        TemplateDict.update(Release=RepoReleaseData)
        logging.debug("Repository Release Data added under [Release] key")
    else:
        TemplateDict.update(Release={})
        logging.debug("Repository Release Data excluded from variable dictionary")
except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to construct template variable dictionary:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unexpected Error occurred attempting to construct template variable dictionary.")
    logging.error(str(e))
    raise


###################################
# Build Directory Structure Tree: #
###################################
try:
    logging.debug("Attempting to build directory tree variable...")
    # Set a variable for the Directory tree, and then call the Directory Tree Generator
    DirTree = ".\n"
    for line in BuildDirTree(Path('.')):
        if line != "":
            DirTree += "{}\n".format(line)
    logging.debug("Directory Tree variable created successfully:")
    logging.debug("\n{}".format(DirTree))

    # Add the Dir Tree Variable to the Template Dictionary:
    TemplateDict.update({ 'Tree' : DirTree })

except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to construct directory structure tree variable:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unexpected Error occurred attempting to construct directory structure tree variable.")
    logging.error(str(e))
    raise


########################
# Gather TF File List: #
########################
try:
    ProjectFiles = []
    logging.debug("Gathering list of all Terraform Files ending in the [.tf] file extension")
    for root, dirs, files in os.walk("."):
        # Strip the current directory designations
        dirpath = root.replace(".", "")
        dirpath = dirpath.replace("./", "")
        for filename in files:
            # If the file is a TF file, then append it to the list.
            if '.tf' in filename:
                ProjectFiles.append(os.path.join(dirpath, filename))

    logging.debug("File List Collected Successfully")
    logging.debug(ProjectFiles)
except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to construct terraform file list:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unexpected Error occurred attempting to construct terraform file list.")
    logging.error(str(e))
    raise


##############################################
# Construct Terraform Module Variable Lists: #
##############################################
try:
    # Define Variables that will hold the Required and Optional Variables.
    TFRequiredVars = []
    TFOptionalVars = []
    # Define Variables to track the length of each variable so that spacing can be set correctly in the documentation
    TFReqMaxLen = 0
    TFOptMaxLen = 0
    logging.info("Building module variable list...")
    for tf in ProjectFiles:
        if 'variables.tf' in tf and 'example' not in tf and 'examples' not in tf:
            logging.debug("variables.tf file FOUND: [{}]".format(tf))
            with open(tf, 'r') as VarFile:
                Vars = hcl.load(VarFile)
            logging.debug("variables.tf file open, parsing, sorting, and storing variables...")
            logging.debug(json.dumps(Vars, indent=4, sort_keys=True))
            
            # For each variable in the variables.tf file:
            # Check the config for additional variable data, then:
            # Put the variable into either the Required, or Optional lists based on the existence or absence of a default value.
            for k, v in Vars.get('variable').items():
                # Create a base VarObject to pass to the template containing the data collected from parsing the variables.tf file
                VarObject = {
                    'Name': k,
                    'Type': v.get('type', type(v)),
                    'Description': v.get('description', "No Description Provided"),
                    'ExampleValue': "Example Value"
                }

                # Check if Required Var
                if v.get('default') == None:       
                    # Check the length of the current item, and if its larger then the current max, then set the new max.
                    if len(k) > TFReqMaxLen:
                        TFReqMaxLen = len(k)

                    # Fetch any additional data for the variable defined in the config file.
                    VarConfigData = Config.get('Readme').get('Variables').get('Required').get(k)

                    # Check for additional data and add it to the variable object
                    if VarConfigData is not None:
                        for key, value in VarConfigData.items():
                            VarObject.update({k: v})

                    # Log the required var and append to the required vars list.
                    logging.debug("Added {} to TFRequiredVars list.".format(k))
                    TFRequiredVars.append(VarObject)
                
                # If its not a Required Var, then it must be an Optional Var
                else:
                    # Check the length of the current item, and if its larger then the current max, then set the new max.
                    if len(k) > TFOptMaxLen:
                        TFOptMaxLen = len(k)

                    # Add the default value to the VarObject
                    VarObject.update(DefaultValue=v.get('default'))
                    
                    # Fetch any additional data for the variable defined in the config file.
                    VarConfigData = Config.get('Readme').get('Variables').get('Optional').get(k)

                    # Check for additional data and add it to the variable object
                    if VarConfigData is not None:
                        for key, value in VarConfigData.items():
                            VarObject.update({k: v})

                    # Log the optional var and append to the optional vars list.
                    logging.debug("Added {} to TFOptionalVars list.".format(k))
                    TFOptionalVars.append(VarObject)

    # Log all the things
    logging.info("Variable lists completed:")
    logging.info("{} Required Variables Collected: {}".format(len(TFRequiredVars), TFRequiredVars))
    logging.info("Longest Required Variable Length: {}".format(TFReqMaxLen))
    logging.info("{} Optional Variables Collected: {}".format(len(TFOptionalVars), TFOptionalVars))
    logging.info("Longest Optional Variable Length: {}".format(TFOptMaxLen))

    # Add the Variable Lists to the Template Dictionary
    logging.debug("Adding Lists to Template Dictionary")
    TemplateDict.update(TFRequiredVars=TFRequiredVars)
    TemplateDict.update(TFRequiredVars_MaxLength=TFReqMaxLen)
    TemplateDict.update(TFOptionalVars=TFOptionalVars)
    TemplateDict.update(TFOptionalVars_MaxLength=TFOptMaxLen)
except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to construct terraform file list:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unexpected Error occurred attempting to construct terraform file list.")
    logging.error(str(e))
    raise


###########################
# Render README Template: #
###########################
try:
    logging.info("Rendering README Template...")
    ReadMe = ReadMeTpl.render(
            var=TemplateDict
            )
    logging.info("README.md rendered successfully!")
except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to render README template:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unexpected Error occurred attempting to render the README.md template")
    logging.error(str(e))
    raise


##########################
# Write README Template: #
##########################
try:
    logging.info("Writing README.md from rendered template...")
    ReadMeOut = open("README.md", "w")
    ReadMeOut.write(ReadMe)
    ReadMeOut.close()
    logging.info("README.md wrote successfully")
except Exception as e:
    cprint(" EXCEPTION ENCOUNTERED: ", 'grey', 'on_red')
    cprint("Error encountered attempting to write README.md file:\n\nException: {}\n".format(str(e)), 'red')
    logging.error("Unexpected Error occurred attempting to write README.md file to the current directory.")
    logging.error(str(e))
    raise
