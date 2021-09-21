#!/bin/bash

main='index.html'

# Create an entry for a note file on the main page
# $1 link to note page
# $2 note title
# $3 note date
function enter_main {
	echo "<div><h2><a class=\"lklink\" href=\"$1\"><div>$2<span class=\"date\">$3</span></div></a></h2></div>" >> $main
}

# Add a short header to the notes page
# $1 note title
# $2 note date
# $3 html file
function add_header {
	echo "<div><h1><div>$1<span class=\"date\">$2</span></div></h1></div>" >> $3
}

# Main processing script
# $1 note md file
function process {
	base="$(basename -- $1 .md)" # note.md --> note
	html="$(echo notes/$base.html)"

	header="$(head -1 $1)" # get the first line
	IFS='|' read -r -a info <<< "$header" # split header by '|'

	title="${info[0]:2}" # remove the '# ' from the title
	date="${info[1]}"
	contents="$(tail -n +2 $1)" # remove the first line

	# remove last 2 lines of note.html
	sed "$(( $(wc -l <templates/note.html)-1)),$ d" "templates/note.html" > $html

	# write the title and content
	echo "<title>LK $date</title>" >> $html
	add_header "$title" "$date" $html
	echo "$contents" | markdown-it --linkify >> $html
	echo '</body></html>' >> $html

	# fix mermaid blocks from pre/code tags to div tags
	gawk -i inplace '{print gensub(/<pre><code class="language-mermaid">([^<]+)<\/code><\/pre>/, "<div class=\"mermaid\">\\1</div>", "g");}' RS="" $html

	enter_main $html "$title" "$date"
	echo $title $date
}

# remove the last 2 lines of main.html
sed "$(( $(wc -l <templates/main.html)-1)),$ d" "templates/main.html" > $main

for file in "$1"/*; do
    process $file
done

echo '</body></html>' >> $main