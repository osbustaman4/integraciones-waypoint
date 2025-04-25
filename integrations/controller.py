import traceback
from integrations.integration import Integration
def integration_controller():
    try:
        Integration.get_points()
    except Exception as e:
        print(f"Error: {e}")

