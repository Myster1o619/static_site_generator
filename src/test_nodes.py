import unittest

from nodes import create_text_node, create_html_node, props_to_html, create_leaf_node, create_parent_node, node_to_html, text_node_to_html_node, str_representation_of_node
from enums.texttype import TextType
from enums.nodetype import NodeType

import re


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = create_text_node("This is a text node", TextType.BOLD)
        node2 = create_text_node("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = create_text_node("This is a text node", TextType.BOLD)
        node2 = create_text_node("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_no_url_provided(self):
        node = create_text_node("This is a text node", TextType.BOLD, "www.w.com")
        node2 = create_text_node("This is a text node", TextType.BOLD)
        self.assertIs(node["url/img"], "www.w.com")
        self.assertIs(node2["url/img"], None)

    def test_invalid_text_type(self):
        with self.assertRaises(AttributeError):
            create_text_node("this is a text node", TextType.WRONG, "www.hello.com")

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = create_html_node(props= {
        "href": "https://www.google.com",
        "target": "_blank",
    })
        node2 = node = create_html_node(props= {
        "href": "https://www.google.com",
        "target": "_blank",
    })
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = create_html_node(tag="<p>")
        node2 = create_html_node(tag="<div>")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = create_html_node(props= {
        "href": "https://www.google.com",
        "target": "_blank",
    })
        props_to_string = props_to_html(node["props"])
        self.assertEqual(props_to_string, " href='https://www.google.com' target='_blank'", "Values aren't equal")

class TestParentNode(unittest.TestCase):
    def test_nested_parent(self):
        nested_parent_node = create_parent_node(node_type=NodeType.PARENT_NODE, tag="div", children=[
            create_leaf_node(
                node_type=NodeType.LEAF_NODE,
                tag="p",
                value="This is a leaf node inside the first parent.",
                props={"class": "text"}
            ),
            create_parent_node(
                node_type=NodeType.PARENT_NODE,
                tag="section",
                children=[
                    create_leaf_node(
                        node_type=NodeType.LEAF_NODE,
                        tag="span",
                        value="This is a leaf node inside the nested parent.",
                        props={"class": "highlight"}
                    ),
                    create_leaf_node(
                        node_type=NodeType.LEAF_NODE,
                        tag="a",
                        value="Click me",
                        props={"href": "https://example.com"}
                    )
                ],
                props={"id": "nested-section"}
            ),
        ],
        props={"id": "main-div"}
)
            
        parent_node_to_string = node_to_html(nested_parent_node)
        self.assertEqual(parent_node_to_string, "<div id='main-div'><p class='text'>This is a leaf node inside the first parent.</p><section id='nested-section'><span class='highlight'>This is a leaf node inside the nested parent.</span><a href='https://example.com'>Click me</a></section></div>", "Values aren't equal")

class TestParentNode(unittest.TestCase):
    def test_leaf_creation_from_txt_node(self):
        normal_node = create_text_node(TextType.TEXT, "this is a normal leaf node")
        normal_to_html = text_node_to_html_node(normal_node)
        string_representation = str_representation_of_node(normal_to_html)
        self.assertEqual(string_representation, "{'node_type': <NodeType.LEAF_NODE: 'leaf_node'>, 'tag': '', 'value': 'this is a normal leaf node', 'props': None}", "Values aren't equal")

        links_node = create_text_node(TextType.LINK, "this is a links node", href = "www.somethingcool.co.uk")
        links_to_html = text_node_to_html_node(links_node)
        string_representation = str_representation_of_node(links_to_html)
        self.assertEqual(string_representation, "{'node_type': <NodeType.LEAF_NODE: 'leaf_node'>, 'tag': 'a', 'value': 'this is a links node', 'props': {'href': 'www.somethingcool.co.uk'}}", "Values aren't equal")

class MarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        test_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        regex_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        extracted_text = re.findall(rf"{regex_pattern}", test_text)
        self.assertEqual(extracted_text, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], "Values aren't equal")

    def test_extract_markdown_links(self):
        test_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        regex_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        extracted_text = re.findall(rf"{regex_pattern}", test_text)
        self.assertEqual(extracted_text, [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], "Values aren't equal")
            



if __name__ == "__main__":
    unittest.main()