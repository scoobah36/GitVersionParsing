__author__ = 'ajdanelz'
import subprocess
from datetime import *
from dateutil.relativedelta import relativedelta

pipeline = []
pipeline.append("git tag")
pipeline.append("xargs -I@ git log --format=format:'%ai @%n' -1 @")
pipeline.append("sort")
pipeline.append("awk '{print $1,$4}'")
command = "|".join(pipeline)

out, err = subprocess.Popen(command, stdout=subprocess.PIPE,
        shell=True).communicate()

tags = []
dates = []
collect = False
#print out
for row in out.split('\n'):
    if row != '':
        arDate = row.split(' ')[0].split('-')
        tagDate = date(int(arDate[0]), int(arDate[1]), int(arDate[2]))
        tag = row.split(' ')[1]
        startDate = date.today() - relativedelta(months=3)

        if tagDate > startDate:
            collect = True

        if collect:
            if tag != '':
                dates.append(tagDate)
                tags.append(tag)

output = 'date,version,files_changed,lines_changed\n'
while len(tags) > 1:
    begin = "refs/tags/" + tags[0]
    end = "refs/tags/" + tags[1]
    output += dates[1].strftime("%m/%d/%y") + ","
    output += tags[1] + ","

    p = subprocess.Popen(["git", "diff", "--numstat", begin, end], stdout=subprocess.PIPE)
    out, err = p.communicate()
    files = 0
    lines = 0
    for file in out.split('\n'):
        if file != '':
            files += 1
            add = file.split("\t")[0]
            rem = file.split("\t")[1]
            if add.isdigit():
                lines += int(filter(str.isdigit, add))
            if rem.isdigit():
                lines += int(filter(str.isdigit, rem))

    output += str(files) + ","
    output += str(lines) + "\n"
    dates.remove(dates[0])
    tags.remove(tags[0])


with open('GitVersionChanges.csv', 'w+') as F:
    F.write(output)

print output
