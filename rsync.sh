#! /bin/bash -v
rsync  --progress --stats -az ~/repos/a301_students_eoas/_build/html/  -e ssh n8jov:/home/jovyan/repos/a301_students_eoas/book_html_source

