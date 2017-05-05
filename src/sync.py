import os
import yaml
import shutil

with open("../data/members.yml", "r") as m:
	members = yaml.load(m)

#for member in members:
#	print member["github_username"]

url = "https://github.com/%s/blog"
basedir = os.path.dirname(os.path.realpath(__file__))

repositories = os.listdir("../members")

repositoriesWithUpdates = []

for member in members:
	print("Working for member %s" % member["name"])
	#print( url % member["github_username"])
	if member["name"] not in repositories:
		print("Clone the repository for member: %s" % member["name"])
		print(os.getcwd())
		os.mkdir("../members/%s" % member["name"])
		os.chdir("../members/%s" % member["name"])
		blogurl = url % member["github_username"]
		os.system("git clone %s" % blogurl )
		os.chdir(basedir)
		
	else:
		print("Repository already exits, pull the new changes")
		print("Pull the repository for member: %s" % member["name"])
		os.chdir("../members/%s/blog" % member["name"])
		status = os.system("git pull")
		if status != "Already up-to-date." :
			repositoriesWithUpdates.append(member["name"])
			print("%s has made new commits. Take a look at it" % member["name"])
		else:
			print("No changes made by %s" % member["name"])
		print(os.getcwd())
		os.chdir(basedir)
		print(os.getcwd())

# Download of individual website is complete now copy the relevant posts to madclab website.
for member in members:
	print("Working for members %s" % member["name"])
	dir_path = "../members/" + member["name"] + "/blog/_posts"
	dst_path = "../madclab/_posts"
	posts = os.listdir(dir_path)
	print(posts)
	print(os.getcwd())
	for post in posts:
		src_file_path = dir_path+"/"+post
		#print(src_file_path)
		p = open(src_file_path, "r")
		t = open("temp.yml","w")
		line = p.readline()
		line = p.readline()
		#print(line)
		while line != "---" :
			t.write(line)
			line = p.readline(3)

		t = open("temp.yml","r")
		publish_post = yaml.load(t)
		categories = publish_post["categories"]
		print categories

		if "madclab" in categories:
			print("New post found:"+src_file_path)
			shutil.copy(src_file_path,dst_path) 



