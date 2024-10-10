# models/o1_analyzer.py

import streamlit as st
import plotly.graph_objects as go
from .o1_preview import O1PreviewModel

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
                time_complexity = self.model.generate_code(time_instruction)

                # Generate space complexity
                space_instruction = (
                    f"As a software engineer, analyze the following {model_name} generated code and provide its "
                    f"space complexity using Big O notation. Only provide the Big O notation without explanation.\n\n"
                    f"```{code}```"
                )
                space_complexity = self.model.generate_code(space_instruction)

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
        Generates a bar graph comparing time and space complexities across different models.

        Parameters:
            analysis_results (dict): The complexity analysis results.

        Returns:
            plotly.graph_objects.Figure: The generated graph.
        """
        models = []
        time_complexities = []
        space_complexities = []

        for model, complexities in analysis_results.items():
            if complexities["error"]:
                continue  # Skip models with errors
            models.append(model)
            time_complexities.append(self.parse_complexity(complexities["time_complexity"]))
            space_complexities.append(self.parse_complexity(complexities["space_complexity"]))

        fig = go.Figure(data=[
            go.Bar(name='Time Complexity', x=models, y=time_complexities, marker_color='indianred'),
            go.Bar(name='Space Complexity', x=models, y=space_complexities, marker_color='lightsalmon')
        ])

        # Change the bar mode
        fig.update_layout(
            barmode='group',
            title='Time and Space Complexity Comparison',
            xaxis_title='Models',
            yaxis_title='Big O Notation (Numeric Representation)',
            legend_title='Complexity Type'
        )

        return fig

    def parse_complexity(self, complexity_str):
        """
        Parses Big O notation into a numeric value for graphing purposes.

        Parameters:
            complexity_str (str): The Big O notation string.

        Returns:
            int: A numeric representation of the complexity.
        """
        # Simplistic parsing; can be expanded for more accurate representations
        mapping = {
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4,
            "O(n^2)": 5,
            "O(n^3)": 6,
            "O(2^n)": 7,
            "O(n!)": 8
        }
        return mapping.get(complexity_str.strip(), 0)  # Default to 0 if not found

