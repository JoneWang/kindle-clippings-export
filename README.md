kindle-clippings-export
=======================

Export your kindle clippings,and custom outfile.Only *kindle paperwhite* tested.

Example
=======

    python outkindle.py -f "/home/jone/My Clippings.txt" -b "Le Petit Prince" -t 1
    
```My Clippings.txt is ./documents/My Clippings.txt in kindle-device.```

The current directory ouput myclippings.out file:

    Le Petit Prince
    ==========

    time:2013-02-30 14:54:24
    page:63-63
    Highlight content: At that moment I caught a gleam of light in the impenetrable mystery of his presence

    time:2013-02-30 14:54:24
    page:63-63
    Highlight content: I demanded, abruptly
    
    The above is content.

Export Parameters
=======

 - -f input file path       (option)  (default: "My Clippings.txt")
 - -o output file path      (option)  (default: "myclippings.out")
 - -b export specified book (option)  (default: export all book)
 - -t export specified type (option)  (values: 1 (Highlight) , 2 (Note) | default: export all type)

Custom Out Template
=======

Modify EXPORT_BOOK_HEAD, EXPORT_BOOK_BODY, EXPORT_BOOK_FOOT custom your outfile template.

default:

    EXPORT_BOOK_HEAD = """{{ title }}\n==========\n\n"""
    EXPORT_BOOK_BODY = """time:{{ time }}\npage:{{ page }}\n{{ type }}: {{ text }}\n\n"""
    EXPORT_BOOK_FOOT = """The above is content."""

variable:

    {{ title }} # book name
    {{ type }}  # clipping type
    {{ page }}  # page number
    {{ time }}  # time
    {{ text }}  # highlight or note content
