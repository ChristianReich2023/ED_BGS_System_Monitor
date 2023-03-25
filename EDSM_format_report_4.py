import datetime
import pytz
import numpy as np
import matplotlib.pyplot as plt
import EDSM_config_reader

#Colors
colorBackground = '#FFFFFF'
colorTextDark = '#2D3748'
colorTextLight = 'white'
colorHeader = '#87909A'
colorRowEven = '#F7FAFC'
colorRowOdd = '#E2EAF2'
colorYellow = '#FBE169'
colorLightGreen = '#C0D5B2'
colorGreen = '#9ABD84'
colorDarkGreen = '#74A257'
colorRed1 = '#E16D3C'
colorRed2 = '#EFD299'

def render_report4(data, 
                col_width=[2.7, 1.8, 2.0, 1.0],
                row_height=0.4,
                font_size=14,
                header_color=colorHeader, 
                row_colors=[colorRowOdd, colorRowEven], 
                edge_color=colorHeader,
                bbox=[0, 0, 1, 1], 
                header_columns=0,
                ax=None, 
                **kwargs):

    # If an `ax` parameter is not passed, create a plot figure and axis
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([max(col_width), row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    #ax.set_facecolor(colorBackground)
    font = {'family' : 'sans',
            'weight' : 'normal',
            'size'   : '14'}
    plt.rc('font', **font)  # pass in the font dict as kwargs
    
    # Create the table from the plt object, with column widths set to auto
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, colWidths = col_width, **kwargs)
    
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)
    
    cellDict = mpl_table.get_celld()
    colSystem = data.columns.get_loc('system')
    colStatus = data.columns.get_loc('status')
    
    
    # Set colors based on header or value and set the edge color
    for key in mpl_table._cells:  
        cell = mpl_table._cells[key]
        cell.set_edgecolor(edge_color)
        if key[0] == 0 or key[1] < header_columns:
            cell.set_text_props(weight='bold', color=colorTextLight)
            cell.set_facecolor(header_color)
        else:
            isinstance(data.iloc[int(key[0] % len(key)),int(key[1])], str)
            cell.set_facecolor(row_colors[key[0]%len(row_colors)])

        if key[0] == 0 or key[1] < header_columns:
            continue
        else: 
            # for the status allign cewnter and mark grenn, when OK
            if key[1] == colStatus:             
                if data.iloc[key[0]-1, key[1]] == 'update needed':
                    cell_style = colorYellow
                else:
                    cell_style = colorLightGreen                
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                cellDict[key].set_facecolor(cell_style)
            if key[1] == colSystem:
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'left'})
            else:
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
            
    #get the current date
    utc = pytz.utc
    now = datetime.datetime.now(tz=utc).strftime("%b %d, %Y - %H:%M")
    
    #get the report name
    report_name = EDSM_config_reader.get_report_name('EDSM_config.ini', 4)
        
    #assign the report name to report
    str_message = f'{report_name} - from {now} UTC'
    
    # Save the plot as an image and return axis
    ax.set_title(str_message)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig('report_4.png', format='png')

    return ax
