from pydantic_settings import BaseSettings
from pydantic import BaseModel
from typing import Dict
from typing_extensions import TypedDict

class Settings(BaseSettings):
    # app_name: str = "Awesome API"
    # admin_email: str
    # items_per_user: int = 50
    app_name: str = "tesla-http-api-over-ble"
    version: str = "0.0.1"
    commands: Dict = {
        'unlock': 'Unlock vehicle', 
        'lock': 'Lock vehicle',
        'drive': 'Remote start vehicle',
        'climate-on': 'Turn on climate control',
        'climate-off': 'Turn off climate control',
        'climate-set-temp': 'Set temperature (celsius)',
        'honk': 'Honk horn',
        'ping': 'Ping vehicle',
        'flash-lights': 'Flash lights',
        'charging-set-limit': 'Set charge limit to PERCENT',
        'charging-set-amps': 'Set charge current to AMPS',
        'charging-start': 'Start charging',
        'charging-stop': 'Stop charging',
        'charging-schedule': 'Schedule charging to MINS minutes after midnight and enable daily scheduling',
        'charging-schedule-cancel': 'Cancel scheduled charge start',
        'media-set-volume': 'Set volume',
        'software-update-start': 'Start software update after DELAY',
        'software-update-cancel': 'Cancel a pending software update',
        'sentry-mode': 'Set sentry mode to STATE (on of off)',
        'trunk-open': 'Open vehicle trunk',
        'trunk-move': 'Toggle trunk open/closed',
        'trunk-close': 'Closes vehicle trunk',
        'frunk-open': 'Open vehicle frunk',
        'charge-port-open': 'Open charge port',
        'charge-port-close': 'Close charge port',
        'autosecure-modelx': 'Close falcon-wing doors and lock vehicle. Model X only',
        'set-heater': 'Set seat heater at POSITION to LEVEL',
        'steering-wheel-heater': 'Set steering wheel mode to STATE (on or off)',
        'auto-seat-and-climate': 'Turn on automatic seat heating and HVAC',        
    }
    docker_image_tesla_vehicle_command: str = 'test:latest'
    # Tesla specific
    vin: str = "VIN"
    private_key_file: str = 'private.pem'