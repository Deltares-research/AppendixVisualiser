import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib import colors as mplcolors
import json
from datetime import datetime, timedelta
from typing import Union, List
from pathlib import Path 
from copy  import copy



class ExportToAV:
    linestyle_map = {"-": "solid", 
                     "-.": "dashdot", 
                     '--': "dash",
                     ":": "dot"}

    marker_map = {"o": "circle",
                  "s": "square",
                  "v": "triangle-down",
                  "^": "triangle-up",
                  "<": "triangle-left",
                  ">": "triangle-right",
                  "1": "y-down"}

    def __init__(self, figures:list=None):
        self._output_dict = {"reference":"Add reference to report",
                             "contact":"koen.berends@deltares.nl",
                             "appendices":[]}

        
        if figures is not None:
            self.addAppendix(name="appendix")
            self.addFiguresToAppendix(figures, 0)

    def to_json(self, path:Union[str, Path]):
        with open(path, 'w') as f:
            json.dump(self._output_dict, f, indent=2)

    def addAppendix(self, name:str="appendix", appendixtype="graphs",paragraph:str=None):
        if paragraph is None:
            paragraph = r"""# About
Use this section to describe the figures or tables in this appendix. 
This section supports markdown code, like **bold text**,  *italicized text*,
    > blockquote
and more
## header 2
sample text
### header 3
sample text
"""

        appendix_dict = {"name": name, "type": appendixtype, "paragraphs":list(), "graphs":list(), "tables":list()}
        appendix_dict['paragraphs'] = paragraph
        self._output_dict.get('appendices').append(appendix_dict)

    def getAppendix(self, index):
        return self._output_dict.get('appendices')[index]

    def setAppendix(self, index, appendix_dict):
        self._output_dict.get('appendices')[index] = appendix_dict

    def setParagraph(self, markdown:str, appendix_index:int=0):
        """
        Add a paragraph (description) to an appendix. 

        markdown: str with markdown markup

        """
        self._output_dict.get('appendices')[appendix_index]['paragraphs'] = paragraph

    def addTablesToAppendix(self, tables, appendix:Union[int, str]=0):
        if isinstance(appendix, str):
            appendix = self._get_appendix_index_by_name(appendix)

        appendix_dict = self.getAppendix(appendix)
        for table in tables:
            appendix_dict.get("tables").append(table)

        self.setAppendix(appendix, appendix_dict)

    def getTablesFromCSV(self, fnamelist, titlelist:List[str]=["NO TITLE"]):
        tables = []
        for i, fname in enumerate(fnamelist):
        
            data = []        
            with open(fname, 'r') as f:
                for line in f:
                    data.append(line.split(','))
            table = {"title": titlelist[i],
                     "data": copy(data)
                     }
            tables.append(table)
        return tables

    def addFiguresToAppendix(self, figs, appendix:Union[int, str]=0):
        if isinstance(appendix, str):
            appendix = self._get_appendix_index_by_name(appendix)

        appendix_dict = self.getAppendix(appendix)
        for fig in figs:
            for ax in fig.axes:
                # get lines
                title = ax.get_title()
                xlim = self._get_xlim(ax)
                appendix_dict.get("graphs").append(
                        {"xlabel": ax.get_xlabel(),
                         "ylabel": ax.get_ylabel(),
                         "xlim": xlim,
                         "ylim": ax.get_ylim(),
                         "title": title,
                         "data": [],
                         "annotations": [],
                        }
                        )
                for line in ax.lines:
                    color = line.get_color()
                    mode = self._get_mode(line)
                    
                    try:
                        dash = self.linestyle_map[line.get_linestyle()]
                    except KeyError:
                        print (f"linestyle {line.get_linestyle()} not supported")
                        dash = "solid"
                    
                    try:
                        marker_symbol = self.marker_map[line.get_marker()]
                    except KeyError:
                        print (f"marker symbol {line.get_marker()} not supported. defaulting to circle")
                        marker_symbol = "circle"

                    # Get xy data
                    xdata = line.get_xdata()
                    ydata = line.get_ydata()
                    if len(xdata) == 0:
	                    # empty line, break
	                    continue
	                    
                    xdata, ydata = self._transform_to_data_coordinates(line, xdata, ydata, ax)

                    # Convert timeseries
                    if isinstance(xdata[0], datetime):
                        xdata = [t.strftime("%Y-%m-%d %H:%M:%S") for t in line.get_xdata()] 
                    if isinstance(xdata[0], np.datetime64):
                        xdata = [pd.to_datetime(t).strftime("%Y-%m-%d %H:%M:%S") for t in line.get_xdata()] 
                    
                    # convert np.float32 types (these are not serialiazble, but float64 is..)
                    if isinstance(xdata[0], np.float32): 
                        xdata = [np.float64(x) for x in xdata]
                    if isinstance(ydata[0], np.float32): 
                        ydata = [np.float64(y) for y in ydata]

                    
                    datadict = {'x': list(xdata),
                        'y': list(ydata),
                        "mode": mode,
                        "line": {"color": f"rgb{mplcolors.to_rgb(color)}", 
                                "dash": dash,
                                "width": line.get_linewidth()*1},
                        "marker" :  {"symbol": marker_symbol,
                                    "color": f"rgb{mplcolors.to_rgb(line.get_markerfacecolor())}",
                                    "size": line.get_markersize(),
                                    "line": {'color': f"rgb{mplcolors.to_rgb(line.get_markeredgecolor())}",
                                             'width': line.get_markeredgewidth()}
                        }}
                    label =  line.get_label()
                    if label[0] != "_":
                        datadict["name"] = label
                        datadict["showlegend"] = True
                    else:
                        datadict["showlegend"] = False
                    appendix_dict.get('graphs')[-1].get('data').append(datadict)
                for text in ax.texts:
	                # Convert timeseries
	                textx = text._x
	                if isinstance(text._x, datetime):
	                    textx = text._x.strftime("%Y-%m-%d %H:%M:%S")
	                if isinstance(text._x, np.datetime64):
	                    textx = pd.to_datetime(text._x).strftime("%Y-%m-%d %H:%M:%S")

	                # If arrowprops, it is an annotation
	                try: 
	                    arrow = text.arrowprops
	                    textax = text.xy[0]
	                    if isinstance(textax, datetime):
	                        textax = textax.strftime("%Y-%m-%d %H:%M:%S")
	                    if isinstance(textax, np.datetime64):
	                        textax = pd.to_datetime(textax).strftime("%Y-%m-%d %H:%M:%S")
	                    
	                    # Location of annotation
	                    if text.anncoords == "offset points":
	                        textx, texty = self._transform_to_data_coordinates(text, [text.xyann[0]], [text.xyann[1]], ax)
	                        texty = float(texty[0])
	                        textx = textx[0]
	                    else:
	                        textx = text.xyann[0]*9  # we assume nine pixels per point
	                        texty = text.xyann[1]*9

	                    appendix_dict.get('graphs')[-1].get('annotations').append(
	                        {'x': textx,  # geen textx, werkt niet met offset coordinates
	                            'y': texty,
	                            "xref": "x",
	                            "yref": "y",
	                            "axref": "x",
	                            "ayref": "y",
	                            "xanchor": "left",
	                            "ax": textax,
	                            "ay": text.xy[1],
	                            "text": text._text,
	                            "showarrow": False,   # does not work with  pixel coordinates yet
	                            "arrowhead": 4,
	                            "textfont": {"color": f"rgb{mplcolors.to_rgb(text._color)}"}
	                        }
	                    )
	                except AttributeError:
	                    appendix_dict.get('graphs')[-1].get('data').append(
	                        {'x': [textx],
	                        'y': [text._y],
	                        "mode": "text",
	                        "showlegend": False,
	                        "text": [text._text],
	                        "textposition": self._get_textposition(text),
	                        "textfont": {"color": f"rgb{mplcolors.to_rgb(text._color)}"}
	                        })
                    
                    
                
        
        self.setAppendix(appendix, appendix_dict)

    def _get_textposition(self, textobject):
        th = textobject._horizontalalignment
        tv = textobject._verticalalignment

        alignment_map = {"baseline": "bottom",
                         "top": "top",
                         "left": "left",
                         "right": "right",
                         "bottom": "bottom",
                         "center": "center"
                        }
        return f"{alignment_map[th]} {alignment_map[tv]}"

    def _get_mode(self, line):
        if line.get_marker() == 'None':
            return "lines"
        elif (line.get_marker() != 'None') and (line.get_linestyle() != 'None'):
            return "lines+markers"
        else:
            return "markers"

    def _ax_is_datetime(self, ax):
        for line in ax.lines:
            try:
                x = line.get_xdata()[0]
            except IndexError:
                x = None
                
            if isinstance(x, (datetime, np.datetime64)):
                return True
        return False

    def _get_xlim(self, ax):
        xlim = ax.get_xlim()
        if self._ax_is_datetime(ax):
            xlim = [mdates.num2date(xl).strftime("%Y-%m-%d %H:%M:%S") for xl in xlim]

        return xlim

    def _transform_to_data_coordinates(self, obj, xdata, ydata, ax):
        
        if obj.get_transform() != obj.axes.transData:
            points = np.array([xdata, ydata]).T
            transform = mpl.transforms.composite_transform_factory(
                obj.get_transform(), obj.axes.transData.inverted()
            )
            transfdata =  transform.transform(points).T
            if self._ax_is_datetime(ax):
                transfdata = [[mdates.num2date(xl).strftime("%Y-%m-%d %H:%M:%S") for xl in transfdata[0]],
                              transfdata[1]]
            return np.array(transfdata)
        return xdata, ydata

    def _get_appendix_index_by_name(self, appendixname):
        for i, ap in enumerate(self._output_dict.get("appendices")):
            if ap['name'] == appendixname:
                return i
        
        # if not returned by now, appendix is unknown
        raise IndexError(f"unknown appendix '{appendixname}'")
# Tests 
if __name__ == "__main__":
    """
    Test Cases
    """
    figs = []

    # TEST CASE 1: LINESTYLES
    # ------------------------------------
    fig, ax = plt.subplots(1)

    x = np.linspace(0, 2*np.pi, 100)

    ax.plot(x, np.sin(x), '-', color='m', label='Solid')
    ax.plot(x, np.cos(x), '-.', color="b", label='Dot-Dash')
    ax.plot(x, np.cos(x+0.25*np.pi), '--', color="y", label='Dashed')
    ax.plot(x, np.cos(x+0.5*np.pi), linestyle='dotted', color="r", label='Dotted')
    ax.set_title('Linestyles')

    figs.append(fig)

    # TEST CASE 2: COLOURS
    # ------------------------------------
    fig, ax = plt.subplots(1)

    x = np.linspace(0, 2*np.pi, 100)

    for s in np.linspace(0, np.pi, 10):
        ax.plot(x, np.sin(x+s), '-', color=plt.cm.viridis(s/np.pi))
    ax.set_title('Colors')

    figs.append(fig)
    
    # TEST CASE 3: LineWidths
    # ------------------------------------
    fig, ax = plt.subplots(1)

    x = np.linspace(0, 2*np.pi, 100)

    # test if float32 are correctly handled
    x = np.array([np.float32(xi) for xi in x])

    for s in np.linspace(0, np.pi, 10):
        ax.plot(x, np.sin(x+s), '-', linewidth=5*s/np.pi)
    ax.set_title('LineWidths')

    figs.append(fig)

    # TEST CASE 4: TimeSeries
    # ------------------------------------
    fig, ax = plt.subplots(1)
    start_t = datetime(year=2020, month=1, day=1)
    x = np.linspace(0, 2*np.pi, 50)
    t = [start_t+i for i in map(timedelta, x)]

    ax.plot(t, np.sin(x)/2, '--', color='r', label='sin2(x)', linewidth=3)
    ax.plot(t, np.cos(x), '.-', color="c", label='Cos2ine')

    ax.text(t[5], np.sin(x)[5], 'Text')
    ax.annotate("annotation", xy=(t[6], np.sin(x)[6]), xytext=(t[6], np.sin(x)[8]), textcoords='offset points',
                                arrowprops=dict(arrowstyle="->"))

    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')
    ax.set_title('TimeSeries')
    
    figs.append(fig)

    # TEST CASE 5: AXHLINE
    # ------------------------------------
    fig, ax = plt.subplots(1)
    start_t = datetime(year=2020, month=1, day=1)
    x = np.linspace(0, 2*np.pi, 50)
    t = [start_t+i for i in map(timedelta, x)]

    
    ax.plot(t, np.sin(x)/2, '--', color='r', label='sin2(x)', linewidth=3)
    ax.plot(t, np.cos(x), '.-', color="c", label='Cos2ine')
    ax.axhline(y=0.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')
    ax.set_title('HLINES')

    figs.append(fig)


    # TEST CASE 5: Markers
    # ------------------------------------
    fig, ax = plt.subplots(1)
    start_t = datetime(year=2020, month=1, day=1)
    x = np.linspace(0, 2*np.pi, 10)
    
    markers = list(ExportToAV.marker_map.keys())
    for s, marker in zip(np.linspace(0, np.pi, len(markers)), markers):
        ax.plot(x, np.sin(x+s), linestyle='None', marker=marker, linewidth=5*s/np.pi, label=marker)

    ax.set_title('Markers')

    figs.append(fig)

    # TEST CASE 6: Annotations
    # ------------------------------------
    fig, ax = plt.subplots(1)
    start_t = datetime(year=2020, month=1, day=1)
    x = np.linspace(0, 2*np.pi, 10)
    
    ax.plot(x, np.sin(x)) # just someline

    ax.text(x[5], np.sin(x)[5], 'Half Way')
    ax.annotate("annotation", xy=(x[6], np.sin(x)[6]), xytext=(x[6], np.sin(x)[8]), textcoords='offset points',
                                arrowprops=dict(arrowstyle="->"))
    ax.text(8, 1, 'Out of ax')
    ax.set_title('Annotations')

    figs.append(fig)

    # TEST CASE 7: Scatterplot
    # ------------------------------------
    fig, ax = plt.subplots(1)
    start_t = datetime(year=2020, month=1, day=1)
    x = np.linspace(0, 2*np.pi, 10)
    
    ax.scatter(x, np.sin(x)) # just someline

    ax.set_title('Scatter')

    figs.append(fig)

    # How to Use Export
    # ------------------------------------

    # ExportToAV(figs).to_json("ExportToAV.json")
    table = [
          ['Index', 'Data1', 'Data2', 'Data3'],
          [1, 'b3ba90', '7c95f7', '9a3853'],
          [2, 'ec0b78', 'ba045d', 'ecf03c'],
          [3, '63788d', 'a8c325', 'aab418'],
          [4, 'hf7y8c', '4rghjk', 'cgnhik']
        ],

    exporter = ExportToAV()
    exporter.addAppendix(name="Figures")
    exporter.addFiguresToAppendix([figs[-1]], "Figures")
    exporter.addAppendix(name="Tables",  paragraph="# Tables", appendixtype="tables")
    tables = exporter.getTablesFromCSV(["tables.csv"], title="test_table")
    exporter.addTablesToAppendix(tables, "Tables")
    
    exporter.to_json("ExportToAV.json")




