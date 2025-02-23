from enums.texttype import TextType
from enums.nodetype import NodeType
from enums.delimitertype import DelimiterType
import re
import os


# for debugging purposes
def are_nodes_equal(node_obj_1, node_obj_2):
    return node_obj_1 == node_obj_2
# for debugging purposes

# for debugging purposes
def str_representation_of_node(node_obj):
    return repr(node_obj)
# for debugging purposes

def extract_title(html_string):
    # return "title", html_string
    found = False
    # loop through html - look for first h1 tag and extract title
    # if no h1 tag found, raise exception
    for i in range(0, len(html_string)):
        text_to_check = html_string[i]
        if text_to_check.startswith("<h1>") and text_to_check.endswith("</h1>"):
            title = re.sub(r'<[^>]+>', '', text_to_check)
            title = title.strip()
            found = True
            break
    if found == False:
        raise Exception("Markdown must contain a title (h1 header)")
    else:
        return title, html_string
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_content_items = os.listdir(dir_path_content)
    for item in dir_path_content_items:
        # if item is file, add dir_path_content + item for path of md file
        # template path should stay the same
        # destination will = dest_dir_path + item
        # path_to_item = f"{dir_path_content}{item}"
        path_to_item = os.path.join(dir_path_content, item)
        if os.path.isfile(path_to_item):
            print(f"{item} is a file")
            # if item is a file - generate a page
            generate_page(path_to_item, template_path, dest_dir_path, item)
        else:
            updated_dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(path_to_item, template_path, updated_dest_path)


def generate_page(from_path, template_path, dest_path, file_item):
    # get the markdown file
    # md_file = open("src/content/index.md", "r+") #for vs code
    # md_file = open("./content/index.md", "r+") # for terminal
    md_file = open(from_path, "r+")

    # get markdown file content
    md_content = md_file.read()
    md_file.close()

    # get html file
    # template_file = open("template.html", "r+") #for vs code
    # template_file = open("../template.html", "r+") # for terminal
    template_file = open(template_path, "r+")
    
    # get html file content
    html_content = template_file.read()
    
    # start process of extracting markdown and converting to required html
    split_markdown = markdown_to_blocks(md_content)
    md_block_to_block_type = block_to_block_type(split_markdown)
    html_nodes = build_html_nodes_after_markdown_split(md_block_to_block_type)
    
    html_title, html_string_data = extract_title(html_nodes)
    content_html = attach_html_to_parent_div(html_string_data)
    
    # modify template.html with correct title and additional content for <article>
    modifed_html_content = html_content.replace("{{ Title }}", html_title)
    modifed_html_content = modifed_html_content.replace("{{ Content }}", content_html)
    
    template_file.close()

    cwd = os.getcwd() 
    print("Current working directory:", cwd)
    # create new index.html file with modified content from template
    
    
    # filepath = os.path.join(dest_path["folder"], dest_path["file"])
    
    # create new index.html file with modified content from template
    
    md_file_item = file_item.endswith(".md")

    # md_file_item = from_path.endswith(".md")
    if md_file_item:
        html_file_item = file_item.replace(".md", ".html")
    filepath = os.path.join(dest_path, html_file_item)

    # dest_path, file_item

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    updated_html_file = open(filepath, "w")
    updated_html_file.seek(0)
    updated_html_file.write(modifed_html_content)
    updated_html_file.truncate()
    updated_html_file.close()

def markdown_to_blocks(markdown):
    # split_markdown = markdown.splitlines()
    split_markdown = markdown.split("\n\n")
    cleaned_markdown = []
    for md_item in split_markdown:
        stripped_text = md_item.strip()
        if md_item != "" and stripped_text != "":
            cleaned_markdown.append(stripped_text)
    return cleaned_markdown
    # split_sentences = split_paragraph_into_sentences(cleaned_markdown)
    # print(split_sentences)
    # return split_sentences

''' This is currently not being used ***
def split_paragraph_into_sentences(paragraph):
    sentences = []
    current_sentence = ""
    i = 0
    n = len(paragraph)
    
    while i < n:
        if paragraph[i] == '.':
            # Check if the next character is a space, newline, or the end of the paragraph
            if i + 1 >= n or paragraph[i+1] in ' \n':
                # Check if the current sentence is part of an ordered list
                if not (current_sentence.strip().startswith(tuple(f"{num}." for num in range(1, 10)))):
                    current_sentence += '.'
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                    i += 1
                    continue
        current_sentence += paragraph[i]
        i += 1
    
    # Append any remaining text as the last sentence
    if current_sentence:
        sentences.append(current_sentence.strip())
    
    return sentences
'''

''' This is currently not being used ***
def is_there_a_list_in_split_md(markdown):
    list_found = False
    edited_md = None
    for i in range(0, len(markdown)):
        if markdown[i][0] == "1" and markdown[i][1] == "." and markdown[i][2] == " ":
            list_found = True
            edited_md = markdown[i:]
            break
    if list_found:
        return check_for_list_and_combine(edited_md, markdown)
    else:
        return markdown
'''

def block_to_block_type(markdown):
    text_nodes_from_markdown = []
    # check for a title - if a title is there then you don't want to split the string via delimiters
    for md_item in markdown:
        #check the first character
        if md_item[0] == "#":
            #need to get count of '#' to determine heading type
            target = "#"
            count = 0
            #loop through letters and check for target (#)
            for c in md_item:
                if c == target:
                    count += 1
            #check to see if there is empty space after getting count of target (#)
            space_after_target = md_item[count]
            if space_after_target == " ":
                #need to build the html for appropriate heading (h1-h6)
                #create appropriate 'h' tag
                header_type = f"h{count}"
                #get just the text
                heading_text = md_item[count+1:]
                # print(heading_text)
                heading_text_node = create_heading_text_node(header_type, heading_text)
                # print(heading_text_node)
                text_nodes_from_markdown.append(heading_text_node)
            else:
                # TODO: create a text node if no heading match
                #build generic paragraph?
                text_nodes_from_markdown.append("paragraph")
        
        else:
            # is there a link?
            # link_item = extract_markdown_links(md_item)
            # print(link_item)
            #if md_item isn't a heading, now need to split using delimiters, and then build html
            split_md_items = text_to_textnodes(md_item)
            if split_md_items:
                #we have the text type here so can build html?
                text_nodes_from_markdown.append(split_md_items)

    return text_nodes_from_markdown

''' currently not in use
def check_for_list_and_combine(edited_markdown, full_markdown):
    processed_list = []
    start_position_in_markdown_split = []
    expected_number = 1

    for i in range(0, len(edited_markdown)):
        stripped_item = edited_markdown[i].strip()

        if stripped_item.startswith(f"{expected_number}. "):
            start_position_in_markdown_split.append(i+1)
            processed_list.append(stripped_item)
            expected_number += 1
        else:
            break
    
    rebuilt_markdown = rebuild_markdown_list(processed_list, full_markdown, start_position_in_markdown_split)
    
    return rebuilt_markdown
'''

'''
def rebuild_markdown_list(ordered_list, full_markdown, initial_position):
    ordered_list_string = ""
    for list_item in ordered_list:
        if list_item in full_markdown:
            full_markdown.remove(list_item)
            ordered_list_string = ordered_list_string + " " + list_item

    full_markdown.insert(initial_position[0], ordered_list_string)
    return full_markdown
'''

def text_to_textnodes(text):
    node = create_text_node(TextType.TEXT, text)
    # lists first, if found leave checks for embedded styles for later?
    new_nodes_u_list_split, list_found = split_nodes_delimiter([node], DelimiterType.U_LIST_STAR_DEL, TextType.U_LIST)
    if list_found:
        return new_nodes_u_list_split
    
    new_nodes_u_dash_list_split, list_found = split_nodes_delimiter([node], DelimiterType.U_LIST_DASH_DEL, TextType.U_LIST)
    if list_found:
        return new_nodes_u_dash_list_split
    
    new_nodes_o_list_split, list_found = split_nodes_delimiter([node], DelimiterType.O_LIST_DEL, TextType.O_LIST)
    if list_found:
        return new_nodes_o_list_split
    # lists first, if found leave checks for embedded styles for later?
    new_nodes_bold_split, list_found = split_nodes_delimiter([node], DelimiterType.BOLD_DEL, TextType.BOLD)
    new_nodes_italic_split, list_found = split_nodes_delimiter(new_nodes_bold_split, DelimiterType.ITALIC_DEL, TextType.ITALIC)
    new_nodes_code_split, list_found = split_nodes_delimiter(new_nodes_italic_split, DelimiterType.CODE_DEL, TextType.CODE)
    new_nodes_quote_split, list_found = split_nodes_delimiter(new_nodes_code_split, DelimiterType.QUOTE_DEL, TextType.QUOTE)
    new_nodes_image_split, list_found = split_nodes_image(new_nodes_quote_split)
    new_nodes_complete_split, list_found = split_nodes_link(new_nodes_image_split)
    #Order matters!?
    # new_nodes_bold_split = split_nodes_delimiter([node], DelimiterType.BOLD_DEL, TextType.BOLD)
    # new_nodes_italic_split = split_nodes_delimiter(new_nodes_bold_split, DelimiterType.ITALIC_DEL, TextType.ITALIC)
    # new_nodes_code_split = split_nodes_delimiter(new_nodes_italic_split, DelimiterType.CODE_DEL, TextType.CODE)
    # new_nodes_quote_split = split_nodes_delimiter(new_nodes_code_split, DelimiterType.QUOTE_DEL, TextType.QUOTE)
    # new_nodes_u_list_split = split_nodes_delimiter(new_nodes_quote_split, DelimiterType.U_LIST_STAR_DEL, TextType.U_LIST)
    # new_nodes_o_list_split = split_nodes_delimiter(new_nodes_u_list_split, DelimiterType.O_LIST_DEL, TextType.O_LIST)
    # new_nodes_image_split = split_nodes_image(new_nodes_o_list_split)
    # new_nodes_complete_split = split_nodes_link(new_nodes_image_split)
    #Order matters!?
    return new_nodes_complete_split

def build_html_nodes_after_markdown_split_old(node):
    nested_node = node[0]
    if len(nested_node) == 1:
        html_string_container_for_main_parent_div = []
        parent_node = build_parent_with_children(node)
        html_string = node_to_html(parent_node)
        html_string_container_for_main_parent_div.append(html_string)

        print(html_string_container_for_main_parent_div)
    if len(nested_node) > 1:
        for item in node:
            parent_node = build_parent_with_children(node)

def build_html_nodes_after_markdown_split(node):
    html_string_container_for_main_parent_div = []
    # TODO: check for image node and build accordingly - handled?
    for text_node in node:
        if not isinstance(text_node, list) and "h" in text_node["text_type"].value:
            html_header_string = heading_node_to_html(text_node)
            html_string_container_for_main_parent_div.append(html_header_string)
        elif text_node[0]["text_type"] == TextType.U_LIST or text_node[0]["text_type"] == TextType.O_LIST:                
            list_html_container = list_node_to_html(text_node)
            html_string_container_for_main_parent_div.append(list_html_container)
        elif len(text_node) > 1:
            no_lists = True
            found_list_index = None
            
            for i in range(0, len(text_node)):
                if isinstance(text_node[i], list):
                    no_lists = False
                    found_list_index = i
            if no_lists == False:
                new_parent = text_node[found_list_index]
                text_node.remove(text_node[found_list_index])
                parent_node = build_parent_with_children(text_node)
                html_string = node_to_html(parent_node)
                html_string_container_for_main_parent_div.append(html_string)

                parent_node = None
                parent_node = build_parent_with_children(new_parent)
                html_string = node_to_html(parent_node)
                html_string_container_for_main_parent_div.append(html_string)
            else:
                if text_node[0]["text_type"] == TextType.BOLD and text_node[0]["text"] != "":
                    # this is a hack for bold text
                    parent_node = build_parent_with_children(text_node[0])
                    html_string = node_to_html(parent_node)
                    html_string_container_for_main_parent_div.append(html_string)
                    text_node.remove(text_node[0])
                    parent_node = None

                parent_node = build_parent_with_children(text_node)
                html_string = node_to_html(parent_node)
                html_string_container_for_main_parent_div.append(html_string)
        elif len(text_node) == 1:
            parent_node = None
            parent_node = build_parent_with_children(text_node)
            html_string = node_to_html(parent_node)
            html_string_container_for_main_parent_div.append(html_string)
    
    return html_string_container_for_main_parent_div

def build_parent_with_children(text_node):
    # text_decoration_holder = []
    # for i in range(0, len(text_node)):
    #     for j in range(0, len(text_node[i])):
    #         match text_node[i][j]["text_type"]:
    #             case TextType.BOLD:
    #                 bold_parent = text_node_to_parent_html_node(text_node[i][j])
    #                 child_text_node = create_text_node(TextType.TEXT, text_node[i][j]["text"])
    #                 bold_parent["children"] = text_node_to_html_node(child_text_node)
    #                 text_decoration_holder.append(bold_parent)
    #                 break


    parent_node = None
    children_of_parent = []
    # parent_node = text_node[0][0] 
    # parent_text = parent_node["text"].strip()

    # if parent_text != "":
    #     #the text here becomes a leaf node:
    #     child_text_node = create_text_node(TextType.TEXT, parent_node["text"])
    #     children_of_parent.append(text_node_to_html_node(child_text_node))

    # parent_node = text_node_to_parent_html_node(parent_node)

    # for i in range(1, len(text_node[0])):
    #     child_node = text_node_to_html_node(text_node[0][i])
    #     children_of_parent.append(child_node)
    
    # parent_node["children"] = children_of_parent

    # return parent_node
    if isinstance(text_node, list):
        parent_node = text_node[0]
    else:
        parent_node = text_node
    if parent_node and parent_node["text"]:
        parent_text = parent_node["text"].strip()
        if parent_text != "":
            #the text here becomes a leaf node:
            child_text_node = create_text_node(TextType.TEXT, parent_node["text"])
            children_of_parent.append(text_node_to_html_node(child_text_node))
    if parent_node:
        parent_node = text_node_to_parent_html_node(parent_node)
                # start loop at 1/second item => the first item is the parent built above
    if parent_node and isinstance(text_node, list):
        # for i in range(1, len(parent_node) -1):
        for i in range(1, len(text_node)):
            child_node = text_node_to_html_node(text_node[i])
            children_of_parent.append(child_node)
    elif parent_node and not isinstance(text_node, list):
        child_node = text_node_to_html_node(child_text_node)
    if parent_node:
        parent_node["children"] = children_of_parent

    # print(parent_node)
    return parent_node


def attach_html_to_parent_div(html_string_container):
    main_parent_container_opening = "<div>"
    main_parent_container_closing = "</div>"
    children_html = ""
    if html_string_container:
        
        for string in html_string_container:
            children_html += string
        return main_parent_container_opening + children_html + main_parent_container_closing
    return main_parent_container_opening + children_html + main_parent_container_closing

        

def create_text_node(text_type, text, url = None, alt_text = None, href = None):
    return {
        "text_type": text_type, 
        "text": text,
        "url/img": url,
        "alt_text": alt_text,
        "href": href
    }


# every data member should be optional:
# An HTMLNode without a tag will just render as raw text
# An HTMLNode without a value will be assumed to have children
# An HTMLNode without children will be assumed to have a value
# An HTMLNode without props simply won't have any attributes
def create_html_node(tag = None, value = None, children = None, props = None):
    return {
        "tag": tag,
        "value": value, 
        "children": children,
        "props": props
    }

def create_leaf_node(node_type, value, tag = None, props = None):
    return {
        "node_type": node_type,
        "tag": tag,
        "value": value, # required* 
        "props": props,
    }

def create_parent_node(node_type, tag, children, props = None,):
    return {
        "node_type": node_type,
        "tag": tag, # required*
        "children": children, # [] of leaf nodes - required*
        "props": props
    }

# {
#     "href": "https://www.google.com",
#     "target": "_blank",
# }
# props_to_html should return:
#  href="https://www.google.com" target="_blank" 
# leading space character before href and before target. 
# This is important. HTML attributes are always separated by spaces.
def props_to_html(props):
    props_to_string = ""
    for key, value in props.items():
        props_to_string += "".join(f" {key}='{value}'")
    return props_to_string

def heading_node_to_html(node):
    #build opening and closing tags corresponding to heading value
    embedded_formatting_node_update = check_for_embedded_style(node)
    match embedded_formatting_node_update["text_type"]:
        case TextType.HEADING_1:
            open_tag = f"<{TextType.HEADING_1.value}>"
            closing_tag = f"</{TextType.HEADING_1.value}>"
            html_string = open_tag + embedded_formatting_node_update["text"] + closing_tag
            return html_string
        case TextType.HEADING_2:
            open_tag = f"<{TextType.HEADING_2.value}>"
            closing_tag = f"</{TextType.HEADING_2.value}>"
            html_string = open_tag + embedded_formatting_node_update["text"] + closing_tag
            return html_string
        case TextType.HEADING_3:
            open_tag = f"<{TextType.HEADING_3.value}>"
            closing_tag = f"</{TextType.HEADING_3.value}>"
            html_string = open_tag + embedded_formatting_node_update["text"] + closing_tag
            return html_string
        case TextType.HEADING_4:
            open_tag = f"<{TextType.HEADING_4.value}>"
            closing_tag = f"</{TextType.HEADING_4.value}>"
            html_string = open_tag + embedded_formatting_node_update["text"] + closing_tag
            return html_string
        case TextType.HEADING_5:
            open_tag = f"<{TextType.HEADING_5.value}>"
            closing_tag = f"</{TextType.HEADING_5.value}>"
            html_string = open_tag + embedded_formatting_node_update["text"] + closing_tag
            return html_string
        case TextType.HEADING_6:
            open_tag = f"<{TextType.HEADING_6.value}>"
            closing_tag = f"</{TextType.HEADING_6.value}>"
            html_string = open_tag + embedded_formatting_node_update["text"] + closing_tag
            return html_string
        
def list_node_to_html(node):
    embedded_formatting_node_update = check_for_embedded_style(node)
    match embedded_formatting_node_update[0]["text_type"]:
        case TextType.U_LIST:
            ul_container_tag = "<ul>"
            ul_container_tag_closing = "</ul>"
            list_item_tag = "<li>"
            list_item_closing = "</li>"
            html_string = ""
            for list_item in embedded_formatting_node_update:
                if list_item["text"].endswith("\n"):
                    stripped_text = list_item["text"].replace("\n", "")
                    html_string += list_item_tag + stripped_text + list_item_closing
                else:
                    html_string += list_item_tag + list_item["text"] + list_item_closing
            complete_html_list_string = ul_container_tag + html_string + ul_container_tag_closing
            return complete_html_list_string
        case TextType.O_LIST:
            ul_container_tag = "<ol>"
            ul_container_tag_closing = "</ol>"
            list_item_tag = "<li>"
            list_item_closing = "</li>"
            html_string = ""
            for list_item in embedded_formatting_node_update:
                if list_item["text"].endswith("\n"):
                    stripped_text = list_item["text"].replace("\n", "")
                    html_string += list_item_tag + stripped_text + list_item_closing
                else:
                    html_string += list_item_tag + list_item["text"] + list_item_closing
            complete_html_list_string = ul_container_tag + html_string + ul_container_tag_closing
            return complete_html_list_string


def node_to_html(node):
    match node["node_type"]:
        case NodeType.LEAF_NODE:
            if not node["value"]:
                raise ValueError("Leaf node must have a value.")
            if not node["tag"]:
                # return raw string
                value = rf"{node["value"]}"
                return value
            if node["tag"] and node["value"] and not node["props"]:
                # no attributes to generate
                open_tag = f"<{node["tag"]}>"
                closing_tag = f"</{node["tag"]}>"
                html_string = open_tag + node["value"] + closing_tag
                return html_string
            
            closing_tag = f"</{node["tag"]}>"
            # generate attributes (props)
            convert_props_to_html = props_to_html(node["props"])
            open_tag = f"<{node["tag"]+convert_props_to_html}>"
            html_string = open_tag + node["value"] + closing_tag
            return html_string
        
        case NodeType.PARENT_NODE:
            if not node["tag"]:
                raise ValueError("Parent node must have a tag.")
            if not node["children"] and not node["tag"] == "img":
                raise ValueError("Parent node requires at least one child object.")
            if not node["props"]:
                # no attributes to generate
                open_tag = f"<{node["tag"]}>"
                closing_tag = f"</{node["tag"]}>"
                converted_text = ""
                for child_node in node["children"]:
                    converted_text += node_to_html(child_node)
                html_string = open_tag + converted_text + closing_tag
                return html_string
            
            
            if node["tag"] == "img":
                convert_props_to_html = props_to_html(node["props"])
                open_tag = f"<{node["tag"]+convert_props_to_html}>"
                return open_tag
                
            closing_tag = f"</{node["tag"]}>"
            # generate attributes (props)
            convert_props_to_html = props_to_html(node["props"])
            open_tag = f"<{node["tag"]+convert_props_to_html}>"
            converted_text = ""
            for child_node in node["children"]:
                converted_text += node_to_html(child_node)
            html_string = open_tag + converted_text + closing_tag
            return html_string
        case _:
            raise Exception("Incorrect node type.")


# take text node and convert to leaf node depending on type
# this is for building the parent?
def text_node_to_parent_html_node(text_node):
    match text_node["text_type"]:
        case TextType.TEXT:
            return create_parent_node(NodeType.PARENT_NODE, tag = "p", children = [])
        case TextType.BOLD:
            return create_parent_node(NodeType.PARENT_NODE, tag = "b", children = [])
        case TextType.ITALIC:
            return create_parent_node(NodeType.PARENT_NODE, tag = "i", children = [])
        case TextType.CODE:
            return create_parent_node(NodeType.PARENT_NODE, tag = "code", children = [])
        case TextType.QUOTE:
            return create_parent_node(NodeType.PARENT_NODE, tag = "blockquote", children = [])
        case TextType.LINK:
            if text_node["text"] == "" and text_node["alt_text"] != "":
                text_node["text"] = text_node["alt_text"]
            return create_parent_node(NodeType.PARENT_NODE, tag = "a", children = [], props = {"href": text_node["href"]})
        case TextType.IMAGE:
            return create_parent_node(NodeType.PARENT_NODE, tag = "img", children = [], props = {
                "src": text_node["url/img"],
                "alt": text_node["alt_text"]
            })
        case TextType.PARAGRAPH:
            return create_parent_node(NodeType.PARENT_NODE, tag = "p", children = [], value = text_node["text"])
        case _:
            raise Exception("Invalid Text Type provided.")


# take text node and convert to leaf node depending on type
# this is for building the children?
def text_node_to_html_node(text_node):
    match text_node["text_type"]:
        case TextType.TEXT:
            return create_leaf_node(NodeType.LEAF_NODE, tag = "", value = text_node["text"])
        case TextType.BOLD:
            return create_leaf_node(NodeType.LEAF_NODE, tag = "b", value = text_node["text"])
        case TextType.ITALIC:
            return create_leaf_node(NodeType.LEAF_NODE, tag = "i", value = text_node["text"])
        case TextType.QUOTE:
            return create_leaf_node(NodeType.LEAF_NODE, tag = "blockquote", value = text_node["text"])
        case TextType.CODE:
            return create_leaf_node(NodeType.LEAF_NODE, tag = "code", value = text_node["text"])
        case TextType.LINK:
            if text_node["text"] == "" and text_node["alt_text"] != "":
                text_node["text"] = text_node["alt_text"]
            return create_leaf_node(NodeType.LEAF_NODE, tag = "a", value = text_node["text"], props = {"href": text_node["href"]})
        case TextType.IMAGE:
            return create_leaf_node(NodeType.LEAF_NODE, tag = "img", value = "", props = {
                "src": text_node["url/img"],
                "alt": text_node["alt_text"]
            })
        case TextType.PARAGRAPH:
            return create_leaf_node(NodeType.PARENT_NODE, tag = "p", value = text_node["text"])
        case _:
            raise Exception("Invalid Text Type provided.")
        
def create_heading_text_node(h_num_type, heading_details):
    match h_num_type:
        case TextType.HEADING_1.value:
            return create_text_node(TextType.HEADING_1, heading_details)
        case TextType.HEADING_2.value:
            return create_text_node(TextType.HEADING_2, heading_details)
        case TextType.HEADING_3.value:
            return create_text_node(TextType.HEADING_3, heading_details)
        case TextType.HEADING_4.value:
            return create_text_node(TextType.HEADING_4, heading_details)
        case TextType.HEADING_5.value:
            return create_text_node(TextType.HEADING_5, heading_details)
        case TextType.HEADING_6.value:
            return create_text_node(TextType.HEADING_6, heading_details)
        case _:
            raise Exception("Invalid heading type provided - must be h1-h6")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    list_found = False

    for node in old_nodes:
        if node["text_type"] is not TextType.TEXT:
            new_node_list.append(node)
        else:
            match delimiter:
                case DelimiterType.CODE_DEL:
                    pattern = r"(`[^`]+`)"
                    split_node_text = re.split(pattern, node["text"])
                    for txt in split_node_text:
                        index = txt.find(DelimiterType.CODE_DEL.value)
                        if index == -1:
                            new_node_list.append(
                                create_text_node(TextType.TEXT, txt)
                            )
                        else:
                            new_txt = txt.replace(DelimiterType.CODE_DEL.value, "")
                            new_node_list.append(
                                create_text_node(text_type, new_txt)
                            )
                case DelimiterType.BOLD_DEL:
                    pattern = r"(\*\*[^*]+\*\*)"
                    split_node_text = re.split(pattern, node["text"])
                    for txt in split_node_text:
                        index = txt.find(DelimiterType.BOLD_DEL.value)
                        if index == -1:
                            new_node_list.append(
                                create_text_node(TextType.TEXT, txt)
                            )
                        else:
                            new_txt = txt.replace(DelimiterType.BOLD_DEL.value, "")
                            new_node_list.append(
                                create_text_node(text_type, new_txt)
                            )
                case DelimiterType.ITALIC_DEL:
                    # pattern = r"(\*[^*]+\*)" This one was causing issues with unordered list
                    pattern = r"(\*[^*\s][^*]*\*)" # should exclude if there is a "space" after *
                    # pattern = r"(?=\* )"
                    split_node_text = re.split(pattern, node["text"])
                    for txt in split_node_text:
                        # index = txt.find(DelimiterType.ITALIC_DEL.value)
                        print(txt)
                        found_symbol = txt.startswith(DelimiterType.ITALIC_DEL.value) and txt.endswith(DelimiterType.ITALIC_DEL.value)

                        #make sure there is something directly after * symbol
                        # if index != -1 and txt[1] != " ":
                        if found_symbol and txt[1] != " ":
                            new_txt = txt.replace(DelimiterType.ITALIC_DEL.value, "")
                            new_node_list.append(
                                create_text_node(text_type, new_txt)
                            ) 
                        if found_symbol == False:
                            new_node_list.append(
                                create_text_node(TextType.TEXT, txt)
                            )
                case DelimiterType.QUOTE_DEL:
                    split_node_text = re.split(r'(?=\n> )', node["text"])
                    for txt in split_node_text:
                        index = txt.find(DelimiterType.QUOTE_DEL.value)
                        if index == -1:
                                new_node_list.append(
                                    create_text_node(TextType.TEXT, txt)
                            )
                        else:
                            new_txt = txt.replace(DelimiterType.QUOTE_DEL.value, "")
                            new_node_list.append(
                                create_text_node(text_type, new_txt)
                            )
                case DelimiterType.U_LIST_STAR_DEL:
                    # pattern = r'(?<=\* )'
                    # pattern = r"(?=\* )"

                    # pattern = r"(?=\* .*\n\* )"
                    
                    pattern = r"(?<=\n)(?=\* )|(?<=^)(?=\* )"
                    # pattern = r"(?<=\n)\* |^\* "
                    
                    extract_pattern = r"^\* (.*?)(\n|$)"
                    # extract_pattern = r"\* (.*?)(\n|$)"

                    # result = []
                    matches = []
                    split_node_text = re.split(pattern, node["text"])
                    for txt in split_node_text:
                        if txt == "" or txt == " ":
                            continue
                        # match = re.findall(pattern, txt)
                        # matches = re.findall(extract_pattern, txt)
                        # matches.extend(re.findall(extract_pattern, txt))
                        match = re.match(extract_pattern, txt)
                        if match:
                            matches.append(match.group(1).strip())
                            list_found = True
                        # loop through the matches and add to new node list accordingly
                    if matches:
                        for match in matches:
                            # extracted_value = match[0].strip()
                            new_node_list.append(
                                # create_text_node(text_type, extracted_value)
                                create_text_node(text_type, match)
                            )
                    else:
                        for txt in split_node_text:
                            if txt != "" or txt != " ":
                                new_node_list.append(
                                    create_text_node(TextType.TEXT, txt)
                                )

                    # for txt in split_node_text:
                    #     index = txt.find(DelimiterType.U_LIST_STAR_DEL.value)
                    #     if index == -1 and txt != "":
                    #         new_node_list.append(
                    #             create_text_node(TextType.TEXT, txt)
                    #         )
                    #     else:
                    #         list_found = True
                    #         new_txt = txt.replace(DelimiterType.U_LIST_STAR_DEL.value, "")
                    #         if new_txt != "":
                    #             new_node_list.append(
                    #                 create_text_node(text_type, new_txt)
                    #             )
                case DelimiterType.U_LIST_DASH_DEL:

                    pattern = r"(?<=\n)(?=- )|(?<=^)(?=- )"

                    extract_pattern = r"- (.*?)(\n|$)"

                    # result = []
                    matches = []
                    split_node_text = re.split(pattern, node["text"])
                    for txt in split_node_text:
                        if txt == "" or txt == " ":
                            continue
                        # match = re.findall(pattern, txt)
                        # matches = re.findall(extract_pattern, txt)
                        matches.extend(re.findall(extract_pattern, txt))
                    if matches:
                        list_found = True
                        # loop through the matches and add to new node list accordingly
                        for match in matches:
                            extracted_value = match[0].strip()
                            new_node_list.append(
                                create_text_node(text_type, extracted_value)
                            )
                    else:
                        for txt in split_node_text:
                            if txt != "" or txt != " ":
                                new_node_list.append(
                                    create_text_node(TextType.TEXT, txt)
                                )

                    # for txt in split_node_text:
                    #     index = txt.find(DelimiterType.U_LIST_DASH_DEL.value)
                    #     if index == -1 and txt != "":
                    #         new_node_list.append(
                    #             create_text_node(TextType.TEXT, txt)
                    #         )
                    #     else:
                    #         list_found = True
                    #         new_txt = txt.replace(DelimiterType.U_LIST_DASH_DEL.value, "")
                    #         if new_txt != "":
                    #             new_node_list.append(
                    #                 create_text_node(text_type, new_txt)
                    #             )
                case DelimiterType.O_LIST_DEL:
                    #markdown needs to match specific pattern, checking for nums 1 - 99
                    # 1. - 9.
                    # 10. - 99.
                    pattern = r'(\d+\. )([^\d]+)'
                    matches = re.findall(pattern, node["text"])
                    result = []
                    if matches:
                        for match in matches:
                            for item in match:
                                result.append(item)
                    if result:
                        #take the matches and now check if the numbers are sequential
                        sequential_list = check_for_sequential_numbers(result)
                        if sequential_list:
                            # this is an ordered list, grab list item values and build accordingly
                            list_found = True
                            for i in range(1, len(result)):
                                # the way the list (result) is split
                                # all the text (list items) will be at an odd index value
                                if i % 2 != 0:
                                    new_node_list.append(
                                        create_text_node(text_type, result[i])
                                    )

                    else:
                        # dont we just append the text as is?
                        new_node_list.append(create_text_node(TextType.TEXT, node["text"]))

                case _:
                    raise Exception(f"Invalid markdown delimiter given: {delimiter}")
            
    return new_node_list, list_found

def check_for_embedded_style(node):
    # TODO: does this cover everything? bold/italics/code
    # Regex pattern to match text wrapped in asterisks and backticks
    bold_pattern = r"\*\*[^*]+\*\*"
    italics_pattern = r"(?<!\*)\*[^*\s][^*]*\*(?!\*)"
    code_pattern = r"`[^`]+`"
    # pattern = r"\*[^*]+\*"

    bold_found = False
    italics_found = False
    code_found = False

    if isinstance(node, list):
        for item in node:
            italics_found = re.search(italics_pattern, item["text"])
            if italics_found:
                break

        for item in node:
            bold_found = re.search(bold_pattern, item["text"])
            if bold_found:
                break
        
        for item in node:
            code_found = re.search(code_pattern, item["text"])
            if code_found:
                break
    else:
        italics_found = re.search(italics_pattern, node["text"])
        bold_found = re.search(bold_pattern, node["text"])
        code_found = re.search(code_pattern, node["text"])

    if italics_found and isinstance(node, list):
        for item in node:
            pattern = r"(\*[^*]+\*)"
            split_node_text = re.split(pattern, item["text"])
            if len(split_node_text) == 1:
                # clean split, continue?
                continue
            # for j in range(0, len(split_node_text)):
            #     # remove empty strings
            #     if split_node_text[j] == "" or split_node_text[j] == " ":
            #         split_node_text.remove(split_node_text[j])
            for i in range(0, len(split_node_text)):
                # remove markdown and build necessary html
                found_symbol = split_node_text[i].startswith(DelimiterType.ITALIC_DEL.value) and split_node_text[i].endswith(DelimiterType.ITALIC_DEL.value)
                if found_symbol:
                    new_txt = split_node_text[i].replace(DelimiterType.ITALIC_DEL.value, "")
                    new_txt = f"<i>{new_txt}</i>"
                    split_node_text.remove(split_node_text[i])
                    split_node_text.insert(i, new_txt)
                    updated_tag_text = ''.join(split_node_text)
                    item["text"] = updated_tag_text
            # for j in range(0, len(split_node_text)):
            #     # remove empty strings
            #     if split_node_text[j] == "" or split_node_text[j] == " ":
            #         split_node_text.remove(split_node_text[j])
    elif italics_found and not isinstance(node, list):
            pattern = r"(\*[^*]+\*)"
            split_node_text = re.split(pattern, node["text"])
            if len(split_node_text) == 1:
                # clean split, continue?
                return node
            # for j in range(0, len(split_node_text)):
            #     # remove empty strings
            #     if split_node_text[j] == "" or split_node_text[j] == " ":
            #         split_node_text.remove(split_node_text[j])
            for i in range(0, len(split_node_text)):
                # remove markdown and build necessary html
                found_symbol = split_node_text[i].startswith(DelimiterType.ITALIC_DEL.value) and split_node_text[i].endswith(DelimiterType.ITALIC_DEL.value)
                if found_symbol:
                    new_txt = split_node_text[i].replace(DelimiterType.ITALIC_DEL.value, "")
                    new_txt = f"<i>{new_txt}</i>"
                    split_node_text.remove(split_node_text[i])
                    split_node_text.insert(i, new_txt)
                    updated_tag_text = ''.join(split_node_text)
                    node["text"] = updated_tag_text

    if bold_found and isinstance(node, list):
        for item in node:
            pattern = r"(\*\*[^*]+\*\*)"
            split_node_text = re.split(pattern, item["text"])
            if len(split_node_text) == 1:
                # clean split, continue?
                continue
            # for j in range(0, len(split_node_text)):
            #     # remove empty strings
            #     if split_node_text[j] == "" or split_node_text[j] == " ":
            #         split_node_text.remove(split_node_text[j])
            for i in range(0, len(split_node_text)):
                # remove markdown and build necessary html
                found_symbol = split_node_text[i].startswith(DelimiterType.BOLD_DEL.value) and split_node_text[i].endswith(DelimiterType.BOLD_DEL.value)
                if found_symbol:
                    new_txt = split_node_text[i].replace(DelimiterType.BOLD_DEL.value, "")
                    new_txt = f"<strong>{new_txt}</strong>"
                    split_node_text.remove(split_node_text[i])
                    split_node_text.insert(i, new_txt)
                    updated_tag_text = ''.join(split_node_text)
                    item["text"] = updated_tag_text
            # for j in range(0, len(split_node_text)):
            #     # remove empty strings
            #     if split_node_text[j] == "" or split_node_text[j] == " ":
            #         split_node_text.remove(split_node_text[j])

    elif bold_found and not isinstance(node, list):
        pattern = r"(\*\*[^*]+\*\*)"
        split_node_text = re.split(pattern, node["text"])
        if len(split_node_text) == 1:
            # clean split, continue?
            return node
        # for j in range(0, len(split_node_text)):
        #     # remove empty strings
        #     if split_node_text[j] == "" or split_node_text[j] == " ":
        #         split_node_text.remove(split_node_text[j])
        for i in range(0, len(split_node_text)):
            # remove markdown and build necessary html
            found_symbol = split_node_text[i].startswith(DelimiterType.BOLD_DEL.value) and split_node_text[i].endswith(DelimiterType.BOLD_DEL.value)
            if found_symbol:
                new_txt = split_node_text[i].replace(DelimiterType.BOLD_DEL.value, "")
                new_txt = f"<strong>{new_txt}</strong>"
                split_node_text.remove(split_node_text[i])
                split_node_text.insert(i, new_txt)
                updated_tag_text = ''.join(split_node_text)
                node["text"] = updated_tag_text

    if code_found and isinstance(node, list):
        for item in node:
            pattern = r"(`[^`]+`)"
            split_node_text = re.split(pattern, item["text"])
            if len(split_node_text) == 1:
                # clean split, continue?
                continue
            # for j in range(0, len(split_node_text)):
            #     # remove empty strings
            #     if split_node_text[j] == "" or split_node_text[j] == " ":
            #         split_node_text.remove(split_node_text[j])
            for i in range(0, len(split_node_text)):
                # remove markdown and build necessary html
                found_symbol = split_node_text[i].startswith(DelimiterType.CODE_DEL.value) and split_node_text[i].endswith(DelimiterType.CODE_DEL.value)
                if found_symbol:
                    new_txt = split_node_text[i].replace(DelimiterType.CODE_DEL.value, "")
                    new_txt = f"<code>{new_txt}</code>"
                    split_node_text.remove(split_node_text[i])
                    split_node_text.insert(i, new_txt)
                    updated_tag_text = ''.join(split_node_text)
                    item["text"] = updated_tag_text

    elif code_found and not isinstance(node, list):
        pattern = r"(`[^`]+`)"
        split_node_text = re.split(pattern, node["text"])
        if len(split_node_text) == 1:
            # clean split, continue?
            return node
        # for j in range(0, len(split_node_text)):
        #     # remove empty strings
        #     if split_node_text[j] == "" or split_node_text[j] == " ":
        #         split_node_text.remove(split_node_text[j])
        for i in range(0, len(split_node_text)):
            # remove markdown and build necessary html
            found_symbol = split_node_text[i].startswith(DelimiterType.CODE_DEL.value) and split_node_text[i].endswith(DelimiterType.CODE_DEL.value)
            if found_symbol:
                new_txt = split_node_text[i].replace(DelimiterType.CODE_DEL.value, "")
                new_txt = f"<code>{new_txt}</code>"
                split_node_text.remove(split_node_text[i])
                split_node_text.insert(i, new_txt)
                updated_tag_text = ''.join(split_node_text)
                node["text"] = updated_tag_text

    return node

def check_for_sequential_numbers(split_text):
    # if the first item doesn't follow MD format, can immediately return 
    MD_LIST_ITEM_ONE_CHECK = "1. "
    numbers = [] 
    if split_text[0] != MD_LIST_ITEM_ONE_CHECK:
        return numbers
    
    # loop and get the numbers - this is only checking 1-99 - recursion for more?
    for item in split_text:
        if item[0].isnumeric() and item[1] == "." and item[2] == " ":
            numbers.append(int(item[0]))
        if item[0].isnumeric() and item[1].isnumeric() and item[2] == "." and item[3] == " ":
            numbers.append(int(item[0:2]))

    if len(numbers) == 1 and numbers[0] == MD_LIST_ITEM_ONE_CHECK:
        # only one item, but it's an OL?
        return numbers
    
    if len(numbers) > 1:
        # are the number in order - 1 => x?
        sequential_list = sorted(numbers) == list(range(min(numbers), max(numbers)+1))
        if sequential_list:
            return numbers
        else:
            # if not sequential, clear what's inside numbers and return empty list
            numbers.clear()
    return numbers

''' Currently not in use
def extract_markdown_images(text):
    # images
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    extracted_text = re.findall(rf"{pattern}", text)
    return extracted_text

def extract_markdown_links(text):
    # regular links
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    extracted_text = re.findall(rf"{pattern}", text)
    return extracted_text
'''

def split_nodes_image(old_nodes):
    new_node_list = []
    list_found = False
    for node in old_nodes:
        original_text = node["text"]
        # split_pattern = r"(!\[[^\]]*\]\(https?://[^\s)]+\))"
        # split_text = re.split(split_pattern, original_text)
        # match_pattern = r"!\[([^\]]+)\]\((https?://[^\s)]+)\)"
        pattern = r'!\[(.*?)\]\((.*?)\)'
        # match = re.match(match_pattern, original_text)
        matches = re.findall(pattern, original_text)
        if matches:
            for match in matches:
                alt_text = match[0]
                image_url = match[1]
                print(f"Alt Text: {alt_text}")
                print(f"Image URL: {image_url}")
                new_node_list.append(
                create_text_node(TextType.IMAGE, "", url = image_url, alt_text = alt_text)
                )
        elif original_text and original_text != "" or original_text != " ":
            new_node_list.append(node)
        # if matches:
        #     image_alt = matches.group(1)  # Extract alt text
        #     image_link = matches.group(2)  # Extract image URL
        #     new_node_list.append(
        #         create_text_node(TextType.IMAGE, "", url = image_link, alt_text = image_alt)
        #         )
        # if len(split_text) == 1:
        #     #a clean split, just check the text and add the node?
        #     text = split_text[0]
        #     if text and text.strip() != "":
        #         new_node_list.append(node)
        #     else:
        #         continue
        # else:
            # regular text may be part of a split that contains image text as well
            # need to create new text node with the regular text
            # match_pattern = r"!\[([^\]]+)\]\((https?://[^\s)]+)\)"
            # for txt in split_text:
            #     match = re.match(match_pattern, txt)
            #     if match:
            #         image_alt = match.group(1)  # Extract alt text
            #         image_link = match.group(2)  # Extract image URL
            #         new_node_list.append(
            #             create_text_node(TextType.IMAGE, "", url = image_link, alt_text = image_alt)
            #     )
            #     elif txt and txt.strip() != "":
            #         new_node_list.append(create_text_node(
            #             TextType.TEXT, txt
            #         ))
    return new_node_list, list_found

def split_nodes_link(old_nodes):
    new_node_list = []
    list_found = False
    for node in old_nodes:
        original_text = node["text"]
        #if the node is an IMAGE, want to skip the regex
        #and append to new list immediately
        #this is why order of functions is NB?
        if node["text_type"] == TextType.IMAGE:
            new_node_list.append(node)
        if original_text == "" or original_text == " ":
            continue
        else:
            split_pattern = r"(\[[^\]]+\]\(.*?\))"
            match_pattern_external = r"\[([^\]]+)\]\((https?://[^\s)]+)\)"
            match_pattern_internal = r"\[([^\]]+)\]\((?!https?://)([^)]+)\)"
            split_text = re.split(split_pattern, original_text)
            if len(split_text) == 1:
                # a clean split, just check the text and add the node?
                text = split_text[0]
                if text and text.strip() != "":
                    new_node_list.append(node)
                else:
                    continue
            else:
                link_container = []
                # we have a link? split separately from other nodes and append??????
                for txt in split_text:
                    if txt == "":
                        continue
                    # matches_ex = []
                    # matches_in = []
                    # found_ex = re.findall(match_pattern_external, txt)
                    # found_in = re.findall(match_pattern_internal, txt)
                    # if found_ex:
                    #     matches_ex.extend(found_ex)
                    # if found_in:
                    #     matches_in.extend(found_in)
                    
                    matches_ex = re.findall(match_pattern_external, txt)
                    matches_in = re.findall(match_pattern_internal, txt)
                # if we have a match, take the text and extract url and alt text
                # else build a new text node with the text
                    if matches_ex:
                        text = matches_ex[0][0]  # Extract alt text
                        href = matches_ex[0][1]  # Extract URL
                        # link_container.append(
                        #     create_text_node(TextType.LINK, text = text, url = None, alt_text = None, href = href)
                        # )
                        new_node_list.append(
                            create_text_node(TextType.LINK, text = text, url = None, alt_text = None, href = href)
                        )
                    elif matches_in:
                        text = matches_in[0][0]  # Extract alt text
                        href = matches_in[0][1]  # Extract URL
                        # link_container.append(
                        #     create_text_node(TextType.LINK, text = text, url = None, alt_text = None, href = href)
                        # )
                        new_node_list.append(
                            create_text_node(TextType.LINK, text = text, url = None, alt_text = None, href = href)
                        )    
                    elif txt and txt.strip() != "":
                        # link_container.append(create_text_node(
                        # TextType.TEXT, txt
                        # ))
                        new_node_list.append(create_text_node(
                        TextType.TEXT, txt
                        ))
                # print(link_container)
                # new_node_list.append(link_container)
    return new_node_list, list_found

def main(dir_path_content, template_path, dest_dir_path):
# def main():
#     generate_pages_recursive(dir_path_content = "src/content/", template_path = "template.html", dest_dir_path = "website") 
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path) 

# main()
