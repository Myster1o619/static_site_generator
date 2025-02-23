import os 
import shutil
cwd = os.getcwd()
from nodes import generate_page, generate_pages_recursive, main 
print("Current working directory:", cwd)

def check_current_directory():
    cwd = os.getcwd() 
    if "content" in os.listdir(cwd):
        print("content folder found")
        print("navigating to root")
        os.chdir("../")
        cwd = os.getcwd() 
        print("Current working directory:", cwd)
    print("checking for public folder")
    check_for_public_folder()

def check_for_public_folder():
    # check to see if public folder exists:
    public_folder = os.path.exists("public")
    if public_folder:
        # delete public folder
        directory = "public"
        print(f"Public folder exists")
        print(f"Removing. . .")
        shutil.rmtree(directory)
        print("Does public_folder_older Exists:")
        print(os.path.exists(directory))
        print("Building Public folder")
        build_new_public_folder()
    else:
        print("Public folder DOESN'T exists")
        print("Building Public folder")
        build_new_public_folder()



def build_new_public_folder():
    # get current directory, make sure it contains src folder
    cwd = os.getcwd() 
    print(f"Current Directory: {cwd}")
    print("is src folder here:")
    print(os.path.exists('src'))
    src_available = os.path.exists("src")
    if src_available:
        print("Correct directory - proceed to public folder creation")
        os.mkdir("public")
        print("Does public folder exist:")
        # print(f"{os.path.exists("public")}")
        proceed_to_copy = do_static_and_public_exist()
        website_folder_available = does_website_exist()
        if proceed_to_copy:
            src_folder = "static"
            dest_folder = "public"
            print("Copying items from static folder to public folder")
            copy_static_move_to_public(src_folder, dest_folder)
        else:
            raise Exception("public and/or static folders are not present") 
        
        if website_folder_available:
            src_folder = "website"
            dest_folder = "public"
            print("Copying index.html from website folder to public folder")
            copy_website_move_to_public(src_folder, dest_folder)
        else:
            raise Exception("public and/or website folders are not present")

    else:
        raise Exception("src folder not present, unable to create public folder")


def do_static_and_public_exist():
    is_there_public_folder = os.path.exists("public")
    is_there_static_folder = os.path.exists("static")
    return is_there_public_folder and is_there_static_folder

def does_website_exist():
    is_there_website_folder = os.path.exists("website")
    return is_there_website_folder

def copy_static_move_to_public(source_folder, destination_folder):
    # make sure destination folder exists, if not: create folder
    if not os.path.exists(destination_folder):
        os.mkdirs(destination_folder)

    # list contents of source file
    for item in os.listdir(source_folder):
        # build the paths for copying
        src_item_path = os.path.join(source_folder, item) #example: "static/item"
        dest_item_path = os.path.join(destination_folder, item) #example: "public/item"

        if os.path.isdir(src_item_path):
            # if item is a folder, create a folder in the destination directory and recruse
            print(f"{item} is a directory, creating in: {dest_item_path}")
            os.makedirs(dest_item_path, exist_ok=True)
            copy_static_move_to_public(src_item_path, dest_item_path)
        else:
            # if item is not a folder, copy it to the destination
            print(f"COPYING FILE: {item}")
            shutil.copy2(src_item_path, dest_item_path)

def copy_website_move_to_public(source_folder, destination_folder):
    # make sure destination folder exists, if not: create folder
    if not os.path.exists(destination_folder):
        os.mkdirs(destination_folder)
    
    for item in os.listdir(source_folder):
        src_item_path = os.path.join(source_folder, item) #example: "website/item"
        dest_item_path = os.path.join(destination_folder, item) #example: "public/item"
        # print(f"COPYING FILE: {item}")
        # shutil.copy2(src_item_path, dest_item_path)

        if os.path.isdir(src_item_path):
            # if item is a folder, create a folder in the destination directory and recurse
            print(f"{item} is a directory, creating in: {dest_item_path}")
            os.makedirs(dest_item_path, exist_ok=True)
            copy_website_move_to_public(src_item_path, dest_item_path)
        else:
            # if item is not a folder, copy it to the destination
            print(f"COPYING FILE: {item}")
            shutil.copy2(src_item_path, dest_item_path)




# check_for_public_folder()
# check_current_directory()
# md_file = open("src/content/index.md", "r+") #for vs code
# md_file = open("./content/index.md", "r+") # for terminal

# template_file = open("template.html", "r+") #for vs code
# template_file = open("../template.html", "r+") # for terminal

# generate_page(from_path = "src/content/index.md", template_path = "template.html", dest_path = {
#     "folder": "website",
#     "file": "index.html"
# })

check_current_directory()
main(dir_path_content = "src/content/", template_path = "template.html", dest_dir_path = "website")
# generate_pages_recursive(dir_path_content = "src/content/", template_path = "template.html", dest_dir_path = "website") 









