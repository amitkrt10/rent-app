import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

@st.cache_resource
def plot_table_with_total(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    headClr = []
    cellClr = []
    footclr = []
    for i in range(len(column_headers)):
        headClr.append('royalblue')
        footclr.append('#CCD9C7')
        if i == 0:
            cellClr.append('paleturquoise')
        else:
            cellClr.append('white')
    cellColours = []
    for i in range(len(cellText)-1):
        cellColours.append(cellClr)
    cellColours.append(footclr)

    the_table = ax.table(cellText=cellText,
                        cellColours = cellColours,
                        colWidths = colWidths,
                        colLabels = column_headers,
                        colColours = headClr,
                        colLoc = 'center',
                        loc='center')
    the_table.scale(1, scaleY)

    the_table.auto_set_font_size(False)
    cells_align = the_table.properties()["celld"]
    for i in range(1,len(cellText)+1):
        for j in range(len(column_headers)):
            cells_align[i, j].set_text_props(ha=alignList[j])
    # Fade the cells
    for cell in the_table.get_children():
        cell_text = cell.get_text().get_text()
        cell.set_edgecolor('black')
        if cell_text in column_headers:
            cell.get_text().set_weight('bold')
            cell.get_text().set_color('white')
            cell.get_text().set_fontsize(headerFontSize)
            cell.get_text().set_fontstyle('italic')
        elif cell_text in cellText[-1]:
            cell.get_text().set_weight('bold')
            cell.get_text().set_color('black')
            cell.get_text().set_fontsize(headerFontSize)
            cell.get_text().set_fontstyle('italic')
        else:
            cell.get_text().set_color('black')
            cell.get_text().set_fontsize(cellFontSize)
            cell.get_text().set_fontstyle('italic')
    st.pyplot(fig)

@st.cache_resource
def plot_table(column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')

    headClr = []
    cellClr = []
    for i in range(len(column_headers)):
        headClr.append('royalblue')
        if i == 0:
            cellClr.append('paleturquoise')
        else:
            cellClr.append('white')
    cellColours = []
    for i in range(len(cellText)):
        cellColours.append(cellClr)

    the_table = ax.table(cellText=cellText,
                        cellColours = cellColours,
                        colWidths = colWidths,
                        colLabels = column_headers,
                        colColours = headClr,
                        colLoc = 'center',
                        loc='center')
    the_table.scale(1, scaleY)

    the_table.auto_set_font_size(False)
    cells_align = the_table.properties()["celld"]
    for i in range(1,len(cellText)+1):
        for j in range(len(column_headers)):
            cells_align[i, j].set_text_props(ha=alignList[j])
    # Fade the cells
    for cell in the_table.get_children():
        cell_text = cell.get_text().get_text()
        cell.set_edgecolor('black')
        if cell_text in column_headers:
            cell.get_text().set_weight('bold')
            cell.get_text().set_color('white')
            cell.get_text().set_fontsize(headerFontSize)
            cell.get_text().set_fontstyle('italic')
        else:
            cell.get_text().set_color('black')
            cell.get_text().set_fontsize(cellFontSize)
            cell.get_text().set_fontstyle('italic')
    st.pyplot(fig)

@st.cache_resource
def plot_table_with_title_total(title_text,subtitle_text,column_headers,cellText,colWidths,scaleY,headerFontSize,cellFontSize,alignList):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    headClr = []
    cellClr = []
    footclr = []
    for i in range(len(column_headers)):
        headClr.append('royalblue')
        footclr.append('#CCD9C7')
        if i == 0:
            cellClr.append('paleturquoise')
        else:
            cellClr.append('white')
    cellColours = []
    for i in range(len(cellText)-1):
        cellColours.append(cellClr)
    cellColours.append(footclr)

    the_table = ax.table(cellText=cellText,
                        cellColours = cellColours,
                        colWidths = colWidths,
                        colLabels = column_headers,
                        colColours = headClr,
                        colLoc = 'center',
                        loc='center')
    the_table.scale(1, scaleY)
    
    # Add subtitle
    plt.figtext(0.5, 1.3,
                title_text,
                weight='bold',
                horizontalalignment='center',
                size=50,
                color='royalblue'
            )
    plt.figtext(0.5, -0.4,
                subtitle_text,
                horizontalalignment='center',
                size=30, style='italic',
                color='red'
            )
    the_table.auto_set_font_size(False)
    cells_align = the_table.properties()["celld"]
    for i in range(1,len(cellText)+1):
        for j in range(len(column_headers)):
            cells_align[i, j].set_text_props(ha=alignList[j])
    # Fade the cells
    for cell in the_table.get_children():
        cell_text = cell.get_text().get_text()
        cell.set_edgecolor('black')
        if cell_text in column_headers:
            cell.get_text().set_weight('bold')
            cell.get_text().set_color('white')
            cell.get_text().set_fontsize(headerFontSize)
            cell.get_text().set_fontstyle('italic')
        elif cell_text in cellText[-1]:
            cell.get_text().set_weight('bold')
            cell.get_text().set_color('black')
            cell.get_text().set_fontsize(headerFontSize)
            cell.get_text().set_fontstyle('italic')
        else:
            cell.get_text().set_color('black')
            cell.get_text().set_fontsize(cellFontSize)
            cell.get_text().set_fontstyle('italic')
    plt.draw()
    st.pyplot(fig)

@st.cache_resource
def plot_bar(title,_x_data,_y_data,bar_width,x_rotate,fontsize):
    # colour = [ "red", "blue", "green", "yellow", "purple", "orange", "royalblue", "#AD688E", "#CCD9C7", "#96ABA0" ]
    # rand_colours = [random.choice(colour) for i in range(len(y_data))]
    fig, ax = plt.subplots()
    ax.bar(_x_data,_y_data,bar_width)
    ax.set_title(f'{title}\n')
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        space = 5
        label = "{:.0f}".format(y_value)
        ax.annotate(
            label,
            (x_value, y_value),
            xytext=(0, space),
            textcoords="offset points",
            ha='center',
            va = 'bottom',
            rotation=90,
            fontsize=fontsize)
    plt.xticks(rotation = x_rotate)
    st.pyplot(fig)

@st.cache_resource
def add_stream_url(phone_num):
    return [f'tel:+91{n}' for n in phone_num]

@st.cache_resource
def make_clickable(url):
    text = url[-10:]
    return f'<a target="_blank" href="{url}">{text}</a>'