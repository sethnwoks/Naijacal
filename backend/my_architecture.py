# my_architecture.py
from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Client
from diagrams.programming.framework import React, Django
from diagrams.onprem.database import PostgreSQL
from diagrams.custom import Custom

# We will use Custom for Gemini since it's not a default icon
gemini_icon_url = "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg"

with Diagram("NaijaCal Detailed Docker Architecture", show=False, direction="LR"):
    user = Client("Mobile / Web User")

    with Cluster("Docker app-network"):
        
        with Cluster("React Container (Port 3000)"):
            frontend = React("SPA Frontend\n(Local Storage JWT)")
            
        with Cluster("Backend Container (Port 8000)"):
            django_api = Django("Django REST API")
            
            with Cluster("Internal Services"):
                jwt_auth = Custom("SimpleJWT Auth", "https://img.icons8.com/color/48/000000/json-web-token.png")
                food_analyzer = Custom("Food Interpreter", "https://img.icons8.com/color/48/000000/python.png")
                
        with Cluster("Database Container (Port 5432)"):
            db = PostgreSQL("PostgreSQL 16\n(Foods & Users)")

    # External APIs
    gemini_api = Custom("Google Gemini API\n(gemini-2.5-flash)", gemini_icon_url)

    # Define User Flow
    user >> Edge(label="Visits UI") >> frontend
    
    # Define Frontend to Backend REST calls
    frontend >> Edge(label="POST /api/token\nPOST /parse-log") >> django_api
    
    # Backend internal logic flows
    django_api >> Edge(label="Validates Token") >> jwt_auth
    django_api >> Edge(label="Reads/Writes Data") >> db
    django_api >> Edge(label="Log Processing") >> food_analyzer
    
    # Backend to External API
    food_analyzer >> Edge(label="Extracts food text to JSON") >> gemini_api
