#!/usr/bin/env python

import argparse
import json


def strip_lines(_lines):
    new_lines = []
    for _line in _lines:
        if _line.strip():
            new_lines.append(_line.strip())
    return new_lines


def remove_separators(_lines):
    new_lines = []
    for _line in _lines:
        if len(_line) > 2:
            if not is_separator(_line):
                new_lines.append(_line)
    return new_lines


def is_separator(_line):
    for char in _line:
        if char != "=":
            return False
    return True


def is_subsection_header(_line):
    if _line[0:2] == "##":
        return True
    return False


def is_item(_line):
    if _line[0:2] == "- ":
        return True
    return False


def create_headers(_lines):
    headers = []
    _header = ""
    prev_line = ""
    for _line in strip_lines(_lines):
        if is_separator(_line):
            _header = prev_line
        else:
            if _header:
                headers.append((_header, _line))
            prev_line = _line
    return headers


def create_section(headers):
    section = {}

    for (header, line) in headers:
        if header in section:
            section.get(header).append(line)
        else:
            section.update({header: [line]})

    return section


def strip_section(sections):
    i = len(sections.keys())
    for header in sections:
        section = sections.get(header)
        if i <= 1:
            break
        sections.update({header: section[:-1]})
        i -= 1
    return sections


def item_with_metadata(item):
    item = item.split(":", 1)
    item[0] = item[0][2:]
    return tuple(item)


def create_subsection(section, metadata=True):
    subsection = {}
    header = "main"
    subsection = {header: []}
    information = ""
    item_no = 0
    for item in section:
        if is_subsection_header(item):
            header = item[3:]
            subsection = {header: []}
        if is_item(item):
            subsection[header].append(item)
        else:
            try:
                subsection[header][item_no] += item
            except:
                IndexError

    if metadata:
        for key in subsection:
            for (i, item) in enumerate(subsection[key]):
                subsection[key][i] = item_with_metadata(item)

    return subsection


def create_health_report(lines, metadata=True):
    checkhealth = {}
    headers = create_headers(lines)
    section = create_section(headers)
    section_stripped = strip_section(section)

    for (header, values) in section_stripped.items():
        checkhealth[header] = create_subsection(values, metadata)

    return checkhealth


def main():
    parser = argparse.ArgumentParser(description="Parse nvim checkhealth output.")
    parser.add_argument("path", type=str, help="path to the checkhealth file")
    parser.add_argument(
        "--json", type=bool, default=True, help="get json output (default: true)"
    )
    parser.add_argument(
        "--split",
        type=bool,
        default=False,
        help="split items into tuples (default: false)",
    )
    args = parser.parse_args()

    with open(args.path, "r") as f:
        lines = f.readlines()

    checkhealth = create_health_report(lines, args.split)

    if args.json:
        print(json.dumps(checkhealth))
    else:
        print(checkhealth)


if __name__ == "__main__":
    main()
