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


def render_report2(data, 
                col_width=[1.8, 2.05, 0.8, 1.5, 0.7, 1.5, 1.2, 0],
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
    colCurInf = data.columns.get_loc("influence")
    colLastUpdate = data.columns.get_loc('last update (UTC)')
    colActiveState = data.columns.get_loc('active states')
    colDaysWon = data.columns.get_loc('days won')
    colHelpCount = data.columns.get_loc('relevant')
    
    current_value = None
    current_row_color = None

    # Define a list of strings that you want to check against:
    highlightedStates = ['Election', 'War']

    # Set colors based on header or value and set the edge color
    for key in mpl_table._cells:  
        cell = mpl_table._cells[key]
        cell.set_edgecolor(edge_color)
        
        # for the Help Count
        if key[1] == colHelpCount:      
            cellDict[key].get_text().set_visible(False)        

        # format the header
        if key[0] == 0 or key[1] < header_columns:
            cell.set_text_props(weight='bold', color=colorTextLight)
            cell.set_facecolor(header_color)
        
        # Check first column value and set row color accordingly
        elif key[1] == 0:
            value = data.iloc[key[0]-1, key[1]]
            if value != current_value:
                current_row_color = row_colors.pop(0)
                row_colors.append(current_row_color)
                current_value = value
            cell.set_facecolor(current_row_color)
        else:
            cell.set_facecolor(current_row_color)
       
        # Skip formatting if the cell is in the header row
        if key[0] == 0:
            continue
        
        # for the Current Influence 
        elif key[1] == colCurInf:
            influence_value = data.iloc[key[0]-1, key[1]]
            influence_str = "{:.2f}".format(influence_value)

            if influence_value < 5:
                cell_style = colorYellow
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'right'})
            else:
                cell_style = current_row_color
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'right'})
            cellDict[key].set_facecolor(cell_style)
            cellDict[key].get_text().set_text(influence_str) 
                
        # for the active State
        elif key[1] == colActiveState:
            cellDict[key].get_text().set_ha('left')
            if data.iloc[key[0]-1, key[1]] in highlightedStates:
                if data.iloc[key[0]-1, key[1]+4] == 'X':
                    cell_style = colorYellow
                    cellDict[key].set_facecolor(cell_style)                    
                    cellDict[key[0],key[1]-2].set_facecolor(cell_style) #cloumn Faction
                    cellDict[key[0],key[1]-3].set_facecolor(cell_style) #column System                    

        # for the Days Won centered and yellow if active state is relevent
        elif key[1] == colDaysWon:
            cellDict[key].get_text().set_ha('center')            
            if data.iloc[key[0]-1, key[1]-1] in highlightedStates:                
                cell_style = colorYellow #for relevant actives states
            else:
                cell_style = current_row_color
            cellDict[key].set_facecolor(cell_style)
                
        #for the last Update centered
        elif key[1] == colLastUpdate:
            cellDict[key].get_text().set_ha('center')

        else:
            # Align all the rest values to left alignment 
            cellDict[key].get_text().set_ha('left')

    #get the current date
    utc = pytz.utc
    now = datetime.datetime.now(tz=utc).strftime("%b %d, %Y - %H:%M")
    
    #get the report name
    report_name = EDSM_config_reader.get_report_name('EDSM_config.ini', 2)
        
    #assign the report name to report
    str_message = f'{report_name} - from {now} UTC'
    
    # Save the plot as an image and return axis
    ax.set_title(str_message)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig('report_2.png', format='png')

    return ax
