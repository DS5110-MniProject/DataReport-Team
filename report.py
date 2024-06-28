import attr
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

@attr.s
class ReportGenerator:
    """Generates different plotly figures based on data"""

    data = attr.ib(type=pd.DataFrame)

    def histogram(self, x_axis: str, y_axis: str = 'count', histfunc: str = 'avg', nbins: int = 10, top_most: int = None) -> go.Figure:
        """
        Build a histogram based off of data with the parameters provided

        Args:
            x_axis (str): Name of the dataframe column to be used as x axis
            y_axis (str): Name of the dataframe column to be used as y axis. If empty, it will default to count
            histfunc (str): Operation used to aggregate data on y_axis (sum, avg, min, max, count)
            nbins (int): Number of bins in histogram, applies only to non-categorical data
            top_most (int): Grabs the top number (or bottom if param is negative) of entries in the dataframe when sorted by y_axis

        Returns: 
            a histogram figure `go.Figure`. Call `.show()` to render

        Raises:
            Error: Failure calling `px.histogram`
        """
        args = self.data[x_axis].value_counts().reset_index() if y_axis == 'count' else self.data
        kwargs = {'x': x_axis, 
                  'y': y_axis, 
                  'log_y': True, 
                  'histfunc': histfunc, 
                  'nbins': nbins
                  }
        
        if top_most and args[x_axis].dtype in ['category', 'object']:
            args = args.sort_values(by=y_axis, ascending= top_most<=0).head(int(np.sqrt(top_most**2)))
        
        return px.histogram(args, **kwargs).update_layout(bargap=0.02)
