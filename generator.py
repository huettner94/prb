#!/usr/bin/env python
import sys
import os
import logging
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


JINJAENV = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml']),
    extensions=['jinja2.ext.do']
)


def get_data(path="data"):
    data = {}
    for filename in os.listdir(path):
        p = os.path.join(path, filename)
        if os.path.isdir(p):
            data[filename] = get_data(p)
        elif p.endswith(".yml"):
            name = ".".join(filename.split(".")[:-1])
            with open(p) as f:
                data[name] = yaml.load(f, Loader=yaml.FullLoader)
    return data


def get_descriptor():
    with open("descriptor.yml") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def copy_static(output_dir):
    shutil.copytree("general/", output_dir, dirs_exist_ok=True)
    staticpath = os.path.join(output_dir, "static")
    shutil.copytree("static/", staticpath, dirs_exist_ok=True)


def generate_page(output_dir, name, template, data, itemdata=None):
    logger.debug("Creating page %s with template %s" % (name, template))
    template = JINJAENV.get_template(template)
    output = template.render(name=name, data=data, itemdata=itemdata)
    outputpath = os.path.join(output_dir, name)
    with open(outputpath, "w") as out:
        out.write(output)


def generate_pages(output_dir, descriptor, data):
    for page in descriptor["pages"]:
        if "foreach" in page:
            for itemname, itemdata in data[page["foreach"]].items():
                pagename = page["name"].replace("{{name}}", itemname)
                generate_page(output_dir, pagename, page["template"], data,
                              itemdata)
        else:
            generate_page(output_dir, page["name"], page["template"], data)


def output_site(descriptor, data):
    output_dir = "output/"
    try:
        shutil.rmtree(output_dir)
    except FileNotFoundError:
        pass
    os.mkdir(output_dir)
    copy_static(output_dir)
    generate_pages(output_dir, descriptor, data)


if __name__ == '__main__':
    logger.info("Hello world")
    descriptor = get_descriptor()
    logger.debug("DESCRIPTOR: %s" % descriptor)
    data = get_data()
    logger.debug("DATA: %s" % data)
    output_site(descriptor, data)
