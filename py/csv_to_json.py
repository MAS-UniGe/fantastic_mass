import csv, json
from fileinput import filename
import sys

data = list()
fname = str()

try:
	fname = sys.argv[1]
except:
	exit(1)

with open(fname) as file:
	csv_reader = csv.DictReader(file, delimiter=";")
	new_data = []
	
	for rows in csv_reader:
		data.append(rows)

	for dicts in data:
		new_dict = dict()
		del dicts["ID"]
		del dicts["Start time"]
		del dicts["Completion time"]
		del dicts["Email"]
		del dicts["Name"]
		del dicts["Your first name"]
		del dicts["Your family name"]
		del dicts["Your email address"]
		del dicts["Your affiliation, if any\n"]
		del dicts["Your country (the country of your university/company, or where you carry your professional activity out)\n"]
		del dicts["A few words about you (you might add the link to your web page here, or add a short bio, or leave empty!)"]

		if dicts["What you developed is (PLEASE SELECT ONE ANSWER TO SEE THE OTHER QUESTIONS IN THE FORM!)\n"] == "a publicly available framework for engineering MASs " or dicts["What you developed is (PLEASE SELECT ONE ANSWER TO SEE THE OTHER QUESTIONS IN THE FORM!)\n"] == "a publicly available framework for building MASs ":
			new_dict["frameworkMasExtension"] = 0
		elif dicts["What you developed is (PLEASE SELECT ONE ANSWER TO SEE THE OTHER QUESTIONS IN THE FORM!)\n"] == "a publicly available add-on/extension/library for an existing framework for building MASs ":
			new_dict["frameworkMasExtension"] = 2
		elif dicts["What you developed is (PLEASE SELECT ONE ANSWER TO SEE THE OTHER QUESTIONS IN THE FORM!)\n"] == "a publicly available MAS (or set of MASs) developed using some existing framework":
			new_dict["frameworkMasExtension"] = 1
		else:
			new_dict["frameworkMasExtension"] = -1	# other

		fme = new_dict["frameworkMasExtension"]

		new_dict["projectName"] = dicts["Name of the artefact you developed\n"]
		new_dict["description"] = dicts["Key-phrase #1 describing your artefact\n"]
		new_dict["projectType"] = dicts["Which option better describes the artefact (framework, extension of a framework, MAS) that you developed?\n"]
		new_dict["projectType"] = new_dict["projectType"].replace(" (you developed a MAS, or a framework/library/add-on to simulate physical and natural phenomena)", "") 
		new_dict["projectType"] = new_dict["projectType"].replace(" (you developed a MAS that is the \"real\" system, for example for implementing decision support systems/solving industrial problems/implementing smart systems, or a framework/library/add-on to develop such real MASs)", "")
		new_dict["keyPhrases"] = [dicts["Key-phrase #2\n"], dicts["Key-phrase #3\n"], dicts["Key-phrase #4\n"], dicts["Key-phrase #5\n"]]
		if fme == 0:
			new_dict["frameworkURL"] = dicts["Public url of the framework you developed (the framework should be available for download from there)\n"]
		elif fme == 1:
			new_dict["masURL"] = dicts["Comma separated list of publicly available urls of the MAS/MASs you developed (the MASs should be available for download from there). Please note that inserting all the links in this answer makes ..."]
		elif fme == 2:
			new_dict["extensionURL"] = dicts["Public url of the add-on/extension/library you developed (it should be available for download from there)"]
		
		if fme == 0:
			new_dict["frameworkCommunityAvailabilty"] = dicts["Is the source code of your framework available to the community?"]
		elif fme == 1:
			new_dict["masCommunityAvailabilty"] = dicts["Is the source code of your MASs available to the community?"]
		elif fme == 2:
			new_dict["extensionCommunityAvailability"] = dicts["Is the source code of your add-on/extension/library available to the community?"]

		if fme == 0:
			new_dict["frameworkPreviousVersionsAvailability"] = "Yes" if dicts["Are there previous versions of the framework (previous commits, or independent repositories, or similar), available to the community?"].startswith("Yes") else "No"
		elif fme == 1:
			new_dict["masPreviousVersionsAvailability"] = "Yes" if dicts["Are there previous versions of the MASs (previous commits, or independent repositories, or similar), available to the community?"].startswith("Yes") else "No"
		elif fme == 2:
			new_dict["extensionPreviousVersionsAvailability"] = "Yes" if dicts["Are there previous versions of the\xa0add-on/extension/library (previous commits, or independent repositories, or similar), available to the community?"].startswith("Yes") else "No"

		if fme == 0:
			new_dict["frameworkPreviousVersionsURL"] = dicts["Link to previous versions of the framework (previous commits, or  independent repositories, or similar), if any\n"]
		elif fme == 1:
			new_dict["masPreviousVersionsURL"] = dicts["Link to previous versions of the MASs (previous commits, or  independent repositories, or similar), if any\n"]
		elif fme == 2:
			new_dict["extensionPreviousVersionsURL"] = dicts["Link to previous versions of the\xa0add-on/extension/library (previous commits, or  independent repositories, or similar), if any\n"]

		if fme == 0:
			new_dict["frameworkLicense"] = dicts["Under which licence is the framework shared with the community?"]
		elif fme == 1:
			new_dict["masLicense"] = dicts["Under which licence is/are the MAS/MASs shared with the community?"]
		elif fme == 2:
			new_dict["extensionLicense"] = dicts["Under which licence is the add-on/extension/library shared with the community?"]

		# da rivedere vvvv
		if fme == 0:
			new_dict["frameworkListOfBugs"] = "Yes" if dicts["Does the public repo of the framework include a list of bugs with their fix history?"] == "Yes" else "No"
		elif fme == 1:
			new_dict["masListOfBugs"] = "Yes" if dicts["Does the public repo of the MASs include a list of bugs with their fix history?"] == "Yes" else "No"
		elif fme == 2:
			new_dict["extensionListOfBugs"] = "Yes" if dicts["Does the public repo of the\xa0add-on/extension/library include a list of bugs with their fix history?"] == "Yes" else "No"

		if fme == 1:
			new_dict["masDevelopedWithFramework"] = dicts["Name of the MAS development platform you exploited for the development of your MASs (ex: JADE, Jason, Jadex, NetLogo, AnyLogic, ....)"]
			new_dict["masLinkToFramework"] = dicts["URL of the MAS development platform you used to develop your MAS/MASs"]
			new_dict["masFrameworkVersion"] = dicts["Version of the MAS development platform you used to develop your MAS/MASs"]

		if fme == 2:
			new_dict["extensionOfFramework"] = dicts["Name of the MAS development platform extended via this\xa0add-on/extension/library (ex: JADE, Jason, Jadex, NetLogo, AnyLogic, ....)"]
			new_dict["extensionLinkToExtendedFramework"] = dicts["URL of the MAS development platform you extended thanks to your add-on/extension/library"]
		
		if fme == 0:
			new_dict["frameworkRealApplication"] = dicts["Are you aware of scientists/companies using the framework? If yes, may you list them with a brief explanation of the applications they developed?"]
		elif fme == 1:
			new_dict["masRealApplication"] = dicts["Are you aware of scientists/companies using the MAS/MASs? If yes, may you list them with a brief explanation of the applications they developed?"]
		elif fme == 2:
			new_dict["extensionRealApplication"] = dicts["Are you aware of scientists/companies using the add-on/extension/library you developed? If yes, may you list them with a brief explanation of the applications they developed?"]

		if fme == 0:
			new_dict["frameworkDocumentation"] = dicts["Does documentation supporting users exist? If yes, which kind?\n2"]
		elif fme == 1:
			new_dict["masDocumentation"] = dicts["Does documentation supporting users exist? If yes, which kind?\n"]
		elif fme == 2:
			new_dict["extensionDocumentation"] = dicts["Does documentation supporting users exist? If yes, which kind?\n3"]

		if fme == 0:
			new_dict["frameworkTechnicalAssistance"] = dicts["Does a technical assistance support for your framework exist? If yes, may you provide the email or form to be used for obtaining assistance?\n"]
		elif fme == 1:
			new_dict["masTechnicalAssistance"] = dicts["Does a technical assistance support for your MASs exist? If yes, may you provide the email or form to be used for obtaining assistance support?\n"]
		elif fme == 2:
			new_dict["extensionTechnicalAssistance"] = dicts["Does a technical assistance support for your\xa0add-on/extension/library exist? If yes, may you provide the email or form to be used for obtaining assistance support?\n"]

		if fme == 0:
			new_dict["frameworkDependencies"] = dicts["May you list here the third party tools/libraries etc to be installed (along with a link to download them if they cannot be included in the repo) to have your framework running -- for example DB m..."]
		elif fme == 1:
			new_dict["masDependencies"] = dicts["May you list here the third party tools/libraries etc to be installed (along with a link to download them if they cannot be included in the repo) to have your MAS running -- for example DB manager..."]
		elif fme == 2:
			new_dict["extensionDependecies"] = dicts["May you list here the third party tools/libraries etc to be installed (along with a link to download them if they cannot be included in the repo) to have your add-on/extension/library running -- f..."]

		if fme == 0:
			new_dict["frameworkTesting"] = "Yes" if dicts["Did you perform any form of testing of the framework?"].startswith("Yes") else "No"
		elif fme == 1:
			new_dict["masTesting"] = "Yes" if dicts["Did you perform any form of testing of the MAS?"].startswith("Yes") else "No"
		elif fme == 2:
			new_dict["extensionTesting"] = "Yes" if dicts["Did you perform some form of testing of the add-on/extension/library?"].startswith("Yes") else "No"

		if fme == 0:
			new_dict["frameworkTestingResources"] = dicts["May you share the link for accessing the testing resources, if any?"]
		elif fme == 1:
			new_dict["masTestingResources"] = dicts["May you share the link for accessing the testing resources, if any?"]
		elif fme == 2:
			new_dict["extensionTestingResources"] = dicts["May you share the link for accessing the testing resources, if any?"]

		if fme == 0:
			new_dict["frameworkSoftwareEngineeringApproach"] = dicts["For implementing your framework, did you follow any software engineering methodology? If yes, which one?\n"]
		elif fme == 1:
			new_dict["masSoftwareEngineeringApproach"] = dicts["For implementing your MAS, did you follow any software engineering methodology? If yes, which one?"]
		elif fme == 2:
			new_dict["extensionSoftwareEngineeringApproach"] = dicts["For implementing your add-on/extension/library, did you follow any software engineering methodology? If yes, which one?"]

		if fme == 0:
			new_dict["frameworkPrimaryPaper"] = dicts["Primary paper describing the framework and/or a few lines of description of the framework: its main features, purpose, etc\n"]
		elif fme == 1:
			new_dict["masPrimaryPaper"] = dicts["Primary paper describing the MAS/MASs and/or a few lines of description of the MAS (the problem it solves, its main features, how many agent types, how many agent instances, etc)\n"]
		elif fme == 2:
			new_dict["extensionPrimaryPaper"] = dicts["Primary paper describing the add-on/extension/library and/or a few lines of description of the contribution\n"]

		if fme == 0:
			new_dict["frameworkSecondaryPaper"] = dicts["Secondary paper describing the framework, if any"]
		elif fme == 1:
			new_dict["masSecondaryPaper"] = dicts["Secondary paper describing the MAS/MASs, if any"]
		elif fme == 2:
			new_dict["extensionSecondaryPaper"] = dicts["Secondary paper describing the\xa0add-on/extension/library if any"]

		if fme == 0:
			new_dict["frameworkMasBuiltUsingFramework"] = dicts["If the framework is aimed at building MASs, are MASs developed using the framework publicly available to the community? If yes, it would be great if you could submit this form, and then fill it on..."]
		new_dict["comments"] = dicts["Optional comments"]

		new_data.append(new_dict)
	
	with open("./data.json", "w") as jsfile:
		jsfile.write(json.dumps(new_data, indent=4))