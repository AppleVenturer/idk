from django.shortcuts import render
import re
import requests


def home(request):
    return render(request, 'generator/homes.html')


def about(request):
    return render(request, 'generator/about.html')


def network_diagram(request):
    message2 = request.GET.get('diagram_components')

    # All regular expression stuff
    match1 = re.compile(r'(\([a-zA-Z0-9_]+(, [a-zA-Z0-9_]+)+\))-([a-zA-Z0-9_]+)')
    match2 = re.compile(r'(\([a-zA-Z0-9_]+(, [a-zA-Z0-9_]+)+\))-(\([a-zA-Z0-9_]+(, [a-zA-Z0-9_]+)+\))')
    match3 = re.compile(r'([a-zA-Z0-9_]+)-(\([a-zA-Z0-9_]+(, [a-zA-Z0-9_]+)+\))')

    mo1 = match1.findall(message2)
    if bool(mo1):
        for i in mo1:
            # previous values to remove
            removable = f'{i[0]}-{i[2]}'
            message2 = message2.replace(removable, '')

            # additional value
            mo1_left = i[0].replace('(', '')
            mo1_left = mo1_left.replace(')', '')
            mo1_left = mo1_left.split(', ')
            mo1_right = i[2]
            for j in mo1_left:
                part = f' {j}-{mo1_right}'
                message2 += part

    mo2 = match2.findall(message2)
    if bool(mo2):
        for i in mo2:
            # previous values to remove
            removable = f'{i[0]}-{i[2]}'
            message2 = message2.replace(removable, '')

            # additional values
            mo2_left = i[0].replace('(', '')
            mo2_left = mo2_left.replace(')', '')
            mo2_left = mo2_left.split(', ')

            mo2_right = i[2].replace('(', '')
            mo2_right = mo2_right.replace(')', '')
            mo2_right = mo2_right.split(', ')

            for a in mo2_left:
                for b in mo2_right:
                    part = f' {a}-{b}'
                    message2 += part

    mo3 = match3.findall(message2)
    if bool(mo3):
        for i in mo3:
            # previous values to remove
            removable = f'{i[0]}-{i[1]}'
            message2 = message2.replace(removable, '')

            # additional value
            mo3_left = i[0]

            mo3_right = i[1].replace('(', '')
            mo3_right = mo3_right.replace(')', '')
            mo3_right = mo3_right.split(', ')

            for j in mo3_right:
                part = f' {mo3_left}-{j}'
                message2 += part

    # to remove more than single spaces in between connections
    message2 = ' '.join(message2.split())
    # Regular expression stuff ends.

    message2 = message2.strip()
    message2 = message2.replace("-", "->")
    message2 = message2.replace(" ", ";")

    url = f"https://quickchart.io/graphviz?graph=digraph{{{message2};}}"

    # If user inputted nothing, then, we do nothing (thus, we return it)
    if url == "https://quickchart.io/graphviz?graph=digraph{;}":
        url = 'https://quickchart.io/graphviz?graph=digraph{}'

    return render(request, 'generator/network_diagram.html', {'diagram_components': url})

