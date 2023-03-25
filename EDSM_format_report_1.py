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

def render_report1(data, 
                col_width=[1.95, 1.05, 0.8, 1.7, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.2],
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
    colDeltaInf = data.columns.get_loc("delta inf")
    colPopulation = data.columns.get_loc('population')
    colLastUpdate = data.columns.get_loc('last update UTC')
    colClearedSystems = data.columns.get_loc('aproval')
    colMaxInf = data.columns.get_loc('appx max inf')
    colBGSactivities = data.columns.get_loc('operations')
    colLastInfluence = data.columns.get_loc('last inf')

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
    
    # Align all string values to left and all numeric values to right with two digits 
    [cellDict[key].get_text().set_ha('left') for key in cellDict if (isinstance(data.iloc[int(key[0] % len(key)),int(key[1])], str) and key[0] > 0)] 
    [cellDict[key].get_text().set_ha('right') for key in cellDict if (isinstance(data.iloc[int(key[0] % len(key)),int(key[1])], int) and key[0] > 0)] 

    # Set colors based on header or value and set the edge color
    for key in mpl_table._cells:  
        cell = mpl_table._cells[key]
        cell.set_edgecolor(edge_color)
        if key[0] == 0 or key[1] < header_columns:
            continue
        else: 
            # for the Current Influence
            if key[1] == colCurInf:  
                influence_value = data.iloc[key[0]-1, key[1]]
                influence_str = "{:.2f}".format(influence_value)

                if data.iloc[key[0]-1, key[1]] < 50:
                    cell_style = colorRed2
                    cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                elif data.iloc[key[0]-1, key[1]] >= 50 and data.iloc[key[0]-1, key[1]] <= 60:
                    cell_style = colorGreen
                    cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                else:
                    cell_style = colorRed1
                    cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                cellDict[key].set_facecolor(cell_style)
                cellDict[key].get_text().set_text(influence_str)
            
            # for the Delta Influence
            elif key[1] == colDeltaInf:  
                influence_value = data.iloc[key[0]-1, key[1]]
                influence_str = "{:.2f}".format(influence_value)
                
                cell_style = colorYellow if data.iloc[key[0]-1, key[1]] == 0 else row_colors[key[0] % len(row_colors)]
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                cellDict[key].set_facecolor(cell_style)
                cellDict[key].get_text().set_text(influence_str)
            
            # for the Population
            elif key[1] == colPopulation:  
                cellDict[key].get_text().set_ha('right') 

            # for the last Update
            elif key[1] == colLastUpdate:      
                cellDict[key].get_text().set_ha('center') 

            # format the cleared systems Column
            elif key[1] == colClearedSystems: 
                cell_style = colorGreen if data.iloc[key[0]-1, key[1]] == 'OK' else row_colors[key[0] % len(row_colors)]
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                cellDict[key].set_facecolor(cell_style)
            
            # format the possible max Influence
            elif key[1] == colMaxInf:
                influence_value = data.iloc[key[0]-1, key[1]]
                influence_str = "{:.2f}".format(influence_value)

                if data.iloc[key[0]-1, key[1]] >= 70:
                    cell_style = colorRed1
                    cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                elif data.iloc[key[0]-1, key[1]] >= 65 and data.iloc[key[0]-1, key[1]] < 70:
                    cell_style = colorYellow
                    cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                else:
                    cell_style = row_colors[key[0] % len(row_colors)]
                    cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                cellDict[key].set_facecolor(cell_style)
                cellDict[key].get_text().set_text(influence_str)
            
            # format the BGS activities Column
            elif key[1] == colBGSactivities: 
                if data.iloc[key[0]-1, key[1]] == 30:
                    cell_style = colorDarkGreen
                elif data.iloc[key[0]-1, key[1]] == 10:
                    cell_style = colorLightGreen
                else: 
                    cell_style = colorGreen if data.iloc[key[0]-1, key[1]] > 0 else row_colors[key[0] % len(row_colors)]
                operations = data.iloc[key[0]-1, key[1]]
                operations_int = "{:.0f}".format(operations)                
                cellDict[key].set_text_props(**{'color' : colorTextDark, 'ha': 'center'})
                cellDict[key].set_facecolor(cell_style)
                cellDict[key].get_text().set_text(operations_int)  
            
            # format the Last Influence
            elif key[1] == colLastInfluence:
                influence_value = data.iloc[key[0]-1, key[1]]
                influence_str = "{:.2f}".format(influence_value) 
                cellDict[key].get_text().set_ha('center')
                cellDict[key].get_text().set_text(influence_str)  
            
    #get the current date
    utc = pytz.utc
    now = datetime.datetime.now(tz=utc).strftime("%b %d, %Y - %H:%M")
    
    #get the report name
    report_name = EDSM_config_reader.get_report_name('EDSM_config.ini', 1)
        
    #assign the report name to report
    str_message = f'{report_name} - from {now} UTC'
    

    # Save the plot as an image and return axis
    ax.set_title(str_message)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig('report_1.png', format='png')

    return ax
