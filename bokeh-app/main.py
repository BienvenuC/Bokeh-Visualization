from os.path import join, dirname
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import row,column
from bokeh.io import curdoc # for bokeh server
from bokeh.models import Select # for Callback
from bokeh.models.widgets import Paragraph, PreText, Div
#from bokeh.models import Paragraph
from scipy import stats # for pearsonr

import pandas as pd

#from bokeh.embed import components # export as html

div = Div(text="""Do you remember our <a href="https://bienvenuc.github.io/MyProjects/EDA_cars.html"> Exploratory_Data_Analysis on Auto Data Set</a>? 
          Here you can have some<b> Interactive Visualization</b>.
           Feel free to <b>Select</b> the different <b>variables</b> you'd like to view, and you have the scatter plot along with Pearson Correlation and P-value. """,
width=1000, height=50)

#output_notebook()
df=pd.read_csv(join(dirname(__file__), 'data/Auto_visual.csv'))
# Define the columndatasource
source = ColumnDataSource(data = {'x': df['length'],
                                  'y': df['price'],
                                  'drive_wheels':df['drive_wheels']
                                })

# Make a list of the unique values from the drive_wheels column: drive_wheels_list
drive_wheels_list = df.drive_wheels.unique().tolist()
# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=drive_wheels_list, palette=Spectral6)

# Creating the plot
plot = figure(height=500 , width=300, title="length vs price",sizing_mode='stretch_width')

# Add circle glyphs to the plot
plot.circle(x='x', y='y', fill_alpha=0.9, source=source, size=3,
            color={'field': 'drive_wheels','transform': color_mapper},line_width=5, legend_field='drive_wheels')

plot.xaxis.axis_label = 'length'
plot.yaxis.axis_label = 'price'
#plot.legend.location = 'top_left'

Intro_text = PreText(text="WELCOME TO THE AUTO DATA SET INTERACTIVE VISUALIZATION WITH BOKEH",width=1000, height=25)

# Create a dropdown Select widget for the x data: x_select
option_list= ['length','width','curb_weight', 'engine_size', 'horsepower', 
              'city_mpg','highway_mpg','wheel_base','bore','price']
x_select = Select(options=option_list,value='length',title='Select the x-axis data')


# Create a dropdown Select widget for the y data: y_select
y_select = Select(options=option_list, value='price',title='Select the y-axis data')
 
# create some widgets like adding text
#button = Button(label="Get the Pearson correlation (Cor) and the P-value between the selected variables")
output1 = Paragraph()
output2 = Paragraph()

pearson_coef, p_value = stats.pearsonr(df['length'], df['price'])
output1.text = "Pearson Correlation = " + str(pearson_coef)
output2.text = "P-value =  " + str(p_value)


#Define the callback: update_plot
def callback(attr, old, new):
    # Read the current values 2 dropdowns: x, y
    new_data_dict = {'x': df[x_select.value],'y': df[y_select.value],'drive_wheels':df['drive_wheels']}
    source.data = new_data_dict
    
    pearson_coef, p_value = stats.pearsonr(df[x_select.value], df[y_select.value])
    output1.text = "Pearson Correlation = " + str(pearson_coef)
    output2.text = "P-value =  " + str(p_value)
    
    # Set the range of all axes
    plot.x_range.start = min(df[x_select.value])
    plot.x_range.end = max(df[x_select.value])
    plot.y_range.start = min(df[y_select.value])
    plot.y_range.end = max(df[y_select.value])

    plot.xaxis.axis_label = x_select.value
    plot.yaxis.axis_label = y_select.value
    plot.title.text = x_select.value + " vs " + y_select.value 

# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', callback)

#Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', callback)
    
# Create layout and add to current document
#layout = column(div,row(widgetbox(x_select, y_select,output1,output2), plot))
#layout = row(column(x_select, y_select,output1,output2), plot)
layout = column(row(x_select, y_select,output1,output2), plot)
# add the layout to curdoc
curdoc().add_root(Intro_text)
curdoc().add_root(div)
curdoc().add_root(layout)
#curdoc().add_root(plot)
