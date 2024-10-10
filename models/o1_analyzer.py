# models/o1_analyzer.py

import streamlit as st
import plotly.graph_objects as go
from .o1_preview import O1PreviewModel
import math

class O1Analyzer:
    def __init__(self, api_key, base_url="https://api.aimlapi.com"):
        self.model = O1PreviewModel(api_key=api_key, base_url=base_url)

    def analyze_complexity(self, code_snippets):
        """
        Analyzes the time and space complexity of given code snippets.

        Parameters:
            code_snippets (dict): A dictionary where keys are model names and values are code strings.

        Returns:
            dict: A dictionary containing complexity analysis for each code snippet.
        """
        analysis_results = {}

        for model_name, code in code_snippets.items():
            if code.startswith("Error"):
                analysis_results[model_name] = {
                    "time_complexity": "N/A",
                    "space_complexity": "N/A",
                    "error": code
                }
                continue

            try:
                # Generate time complexity
                time_instruction = (
                    f"As a software engineer, analyze the following {model_name} generated code and provide its "
                    f"time complexity using Big O notation. Only provide the Big O notation without explanation.\n\n"
                    f"```{code}```"
                )
                time_complexity = self.model.generate_code(time_instruction).strip()

                # Generate space complexity
                space_instruction = (
                    f"As a software engineer, analyze the following {model_name} generated code and provide its "
                    f"space complexity using Big O notation. Only provide the Big O notation without explanation.\n\n"
                    f"```{code}```"
                )
                space_complexity = self.model.generate_code(space_instruction).strip()

                analysis_results[model_name] = {
                    "time_complexity": time_complexity,
                    "space_complexity": space_complexity,
                    "error": None
                }

            except Exception as e:
                analysis_results[model_name] = {
                    "time_complexity": "Error analyzing time complexity.",
                    "space_complexity": "Error analyzing space complexity.",
                    "error": str(e)
                }

        return analysis_results

    def generate_complexity_graph(self, analysis_results):
        """
        Generates a grouped bar graph comparing time and space complexities across different models.

        Parameters:
            analysis_results (dict): The complexity analysis results.

        Returns:
            plotly.graph_objects.Figure: The generated graph.
        """
        models = []
        time_complexities = []
        space_complexities = []
        time_tooltips = []
        space_tooltips = []

        for model, complexities in analysis_results.items():
            if complexities["error"]:
                continue  # Skip models with errors
            time_o = self.parse_complexity(complexities["time_complexity"])
            space_o = self.parse_complexity(complexities["space_complexity"])
            if time_o is not None and space_o is not None:
                models.append(model)
                time_complexities.append(time_o)
                space_complexities.append(space_o)
                time_tooltips.append(f"Time Complexity: {complexities['time_complexity']}")
                space_tooltips.append(f"Space Complexity: {complexities['space_complexity']}")

        if not models:
            st.warning("No valid complexity data to display.")
            return None

        # Create the grouped bar chart with customized tooltips
        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Time Complexity',
            x=models,
            y=time_complexities,
            text=time_tooltips,
            hoverinfo='text',
            marker_color='indianred',
            opacity=0.7
        ))

        fig.add_trace(go.Bar(
            name='Space Complexity',
            x=models,
            y=space_complexities,
            text=space_tooltips,
            hoverinfo='text',
            marker_color='lightsalmon',
            opacity=0.7
        ))

        # Update layout for better aesthetics
        fig.update_layout(
            barmode='group',
            title='Time and Space Complexity Comparison',
            xaxis_title='Models',
            yaxis_title='Complexity Level',
            yaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5, 6, 7, 8],
                ticktext=[
                    "O(1)",
                    "O(log n)",
                    "O(n)",
                    "O(n log n)",
                    "O(n²)",
                    "O(n³)",
                    "O(2ⁿ)",
                    "O(n!)"
                ],
                range=[0, 9]  # Extend the range for better spacing
            ),
            legend_title='Complexity Type',
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='closest',
            margin=dict(l=40, r=40, t=60, b=40)
        )

        # Add gridlines for better readability
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')

        # Add horizontal lines for each Big O level
        for i in range(1, 9):
            fig.add_shape(
                type="line",
                x0=-0.5, y0=i, x1=len(models)-0.5, y1=i,
                line=dict(color="lightgrey", width=1, dash="dot"),
                layer="below"
            )

        # Customize the font
        fig.update_layout(
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="black"
            )
        )

        return fig

    def parse_complexity(self, complexity_str):
        """
        Parses Big O notation into a numeric value for graphing purposes.

        Parameters:
            complexity_str (str): The Big O notation string.

        Returns:
            int or None: A numeric representation of the complexity or None if not found.
        """
        mapping = {
            "O(1)": 1,
            "O(LOG N)": 2,
            "O(LOG N)": 2,
            "O(LOG(N))": 2,
            "O(N)": 3,
            "O(N LOG N)": 4,
            "O(N LOG(N))": 4,
            "O(N²)": 5,
            "O(N^2)": 5,
            "O(N³)": 6,
            "O(N^3)": 6,
            "O(2^N)": 7,
            "O(2^N)": 7,
            "O(N!)": 8,
            "O(N!)": 8,
            # Add more complex mappings as needed
        }
        return mapping.get(complexity_str.upper(), None)  # Return None if not found
