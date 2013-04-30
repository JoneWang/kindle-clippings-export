#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re, time, copy

EXPORT_BOOK_HEAD = """{{ title }}\n==========\n\n"""
EXPORT_BOOK_BODY = """time:{{ time }}\npage:{{ page }}\n{{ type }}: {{ text }}\n\n"""
EXPORT_BOOK_FOOT = """The above is content."""

class MarkType():
    Highlight = {'pid': '1', 'render': 'Highlight content'}
    Note = {'pid': '2','render': 'Note content'}

class Kindle():
    """
    Kindle class
    Export kindle's notes and highlight data.

    import_file: input file path
    book_name: export book name
    export_type: export type id
    out_file: export path
    """
    def __init__(self, import_file='My Clippings.txt', book_name=None, export_type=None, out_file='myclippings.out'):
        self.import_file = import_file
        self.book_name = book_name
        self.export_type = export_type
        self.out_file = out_file
        self.render_data = {}

    def type_filter(self, mark):
        if not self.export_type: return True
        if mark.type['pid'] == self.export_type:
            return True
        else:
            return False

    def book_filter(self, mark):
        if not self.book_name: return True
        if contains(self.book_name, mark.title):
            return True
        else:
            return False

    def _split(self, content):
        return content.split('==========')

    def handle(self):
        content = self._open_file()
        datas = self._split(content)
        for data in datas:
            mark = MarkModle(data)
            if not mark.type or not self.book_filter(mark): continue
            if not self.type_filter(mark): continue

            if not self.render_data.has_key(mark.title):
                self.render_data[mark.title] = []

            self.render_data[mark.title].append(mark)

        for title in copy.copy(self.render_data):
            if not len(self.render_data[title]):
                del self.render_data[title]

        out_content = self._render()
        if self.out_file: 
            self._write_file(out_content)

    def _render(self):
        out_content = ''
        for title in self.render_data:
            mark = self.render_data[title][0]
            if out_content:
                out_content += '\n\n'
            out_content += EXPORT_BOOK_HEAD
            out_content = self._replace(out_content, mark)
            for mark in self.render_data[title]:
                out_content += EXPORT_BOOK_BODY
                out_content = self._replace(out_content, mark)

            out_content += EXPORT_BOOK_FOOT
            out_content = self._replace(out_content, mark)

        return out_content

    def _replace(self, content, data):
        content = content.replace('{{ title }}', data.title)
        content = content.replace('{{ type }}', data.type['render'])
        content = content.replace('{{ page }}', data.page)
        content = content.replace('{{ time }}', data.time)
        content = content.replace('{{ text }}', data.text)
        return content

    def _open_file(self):
        f = open(self.import_file, 'r')
        content = f.read()
        f.close()
        return content

    def _write_file(self, out_content):
        if not self.out_file: 
            print out_content 
            return
        out_f = open(self.out_file, 'w')
        out_f.write(out_content)
        out_f.close()

    def run(self):
        self.handle()

TYPE_PARSE_KEYS = {'Highlight': MarkType.Highlight, 'Note': MarkType.Note, '标注': MarkType.Highlight, '笔记': MarkType.Note}

class MarkModle():
    def __init__(self, mark):
        self.title = ''
        self.type = {'pid': '0', 'render': ''}
        self.page = ''
        self.time = ''
        self.text = ''
        self.info = ''
        self._parse(mark)

    def _parse(self, mark):
        data = mark.split('\r\n')
        data = [i for i in data if i]
        if not data: return

        if len(data) == 2: data.append('')
        self.title, self.info, self.text = data

        info_data = self.info.split(' | ')

        info = info_data[0]
        for key in TYPE_PARSE_KEYS.keys():
            if contains(key, info):
                self.type = TYPE_PARSE_KEYS[key]
                break

        page_data = info.split(' ')[-1]
        time_data = info_data[1]
        if len(page_data) != len(page_data.decode('utf-8')):
            self.page = page_data[9:]
            time_data = time_data.split(' ', 1)[-1].split(' ')
            del time_data[1]
            self.time = self._convert_time(' '.join(time_data), '%Y年%m月%d日 %H:%M:%S', '%Y-%m-%d %H:%M:%S')
        else:
            self.page = page_data
            self.time = self._convert_time(time_data.split(', ', 1)[-1], '%B %d, %Y %I:%M:%S %p', '%Y-%m-%d %H:%M:%S')


    def _note_parse(self):
        pass

    def _highlight_parse(self):
        pass

    def _convert_time(self, str_time, old_format, new_format):
        return str(time.strftime(new_format, time.strptime(str_time, old_format)))


def contains(seq, aset):
    return bool(re.search(seq, aset, re.IGNORECASE))


def execute(args):
    args = args[1:]
    args_length = len(args)

    kindle = Kindle()
    attrs = {'-f': 'import_file', '-b': 'book_name', '-t': 'export_type', '-o': 'out_file'}

    for i in xrange(args_length):
        if i > 0 and args[i-1][0] == '-':
            continue
        if i+1 != args_length and attrs.has_key(args[i]):
            exec("kindle.%s = '%s'" % (attrs[args[i]], args[i+1]))

    kindle.run()


if __name__ == "__main__":
    execute(sys.argv)
