import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
        Generates a bar graph comparing time and space complexities across different models.

        Parameters:
            analysis_results (dict): The complexity analysis results.

        Returns:
            plotly.graph_objects.Figure: The generated graph.
        """
        models = []
        time_complexities = []
        space_complexities = []
        time_labels = []
        space_labels = []
        errors = []

        for model, complexities in analysis_results.items():
            if complexities["error"]:
                errors.append(model)
                continue  # Skip models with errors in the main bars
            models.append(model)
            parsed_time = self.parse_complexity(complexities["time_complexity"])
            parsed_space = self.parse_complexity(complexities["space_complexity"])
            time_complexities.append(parsed_time)
            space_complexities.append(parsed_space)
            time_labels.append(complexities["time_complexity"])
            space_labels.append(complexities["space_complexity"])

        # Create a grouped bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Time Complexity',
            x=models,
            y=time_complexities,
            text=time_labels,
            textposition='auto',
            marker_color='rgba(55, 128, 191, 0.7)',
            hovertemplate='<b>%{x}</b><br>Time Complexity: %{text}<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            name='Space Complexity',
            x=models,
            y=space_complexities,
            text=space_labels,
            textposition='auto',
            marker_color='rgba(219, 64, 82, 0.7)',
            hovertemplate='<b>%{x}</b><br>Space Complexity: %{text}<extra></extra>'
        ))

        # Add error annotations
        if errors:
            fig.add_trace(go.Scatter(
                x=errors,
                y=[0]*len(errors),
                mode='markers',
                marker=dict(
                    color='grey',
                    symbol='x',
                    size=12
                ),
                name='Errors',
                hovertemplate='<b>%{x}</b><br>Error: %{text}<extra></extra>',
                text=[analysis_results[model]['error'] for model in errors]
            ))

        # Update layout with a professional template
        fig.update_layout(
            template='plotly_white',
            barmode='group',
            title={
                'text': 'Time and Space Complexity Comparison',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title='Models',
            yaxis_title='Complexity Level',
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 9)),
                ticktext=[
                    "O(1)", "O(log n)", "O(n)", "O(n log n)",
                    "O(n²)", "O(n³)", "O(2ⁿ)", "O(n!)"
                ],
                range=[0, 9]
            ),
            legend_title='Complexity Type',
            hovermode='closest',
            margin=dict(l=40, r=40, t=80, b=40)
        )

        # Add a custom y-axis scale for better representation
        fig.update_yaxes(
            tickmode='array',
            tickvals=list(range(1, 9)),
            ticktext=[
                "O(1)", "O(log n)", "O(n)", "O(n log n)",
                "O(n²)", "O(n³)", "O(2ⁿ)", "O(n!)"
            ],
            title='Complexity'
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
        # Enhanced parsing to handle more variations and common notations
        mapping = {
            "O(1)": 1,
            "O(1)": 1,
            "O(1)": 1,
            "O(log n)": 2,
            "O(n)": 3,
            "O(n log n)": 4,
            "O(n²)": 5,
            "O(n^2)": 5,
            "O(n³)": 6,
            "O(n^3)": 6,
            "O(2^n)": 7,
            "O(n!)": 8
        }
        # Normalize the input
        normalized = complexity_str.replace('^', '').replace(' ', '').lower()
        for key in mapping:
            normalized_key = key.replace('^', '').replace(' ', '').lower()
            if normalized == normalized_key:
                return mapping[key]
        return 0  # Default to 0 if not found

