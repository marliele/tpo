from locust import HttpUser, task, between
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenBmcUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.auth = ('root', '0penBmc')
        self.client.verify = False

    @task(1)
    def get_system_info(self):
        response = self.client.get("https://localhost:2443/redfish/v1/Systems/system")
        if response.ok:
            system_state = response.json().get('Status')
            print(f"System state: {system_state}")

    @task(1)
    def get_power_state(self):
        response = self.client.get("https://localhost:2443/redfish/v1/Systems/system")
        if response.ok:
            power_state = response.json().get("PowerState")
            print(f"PowerState: {power_state}")

class PublicApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def get_posts(self):
        response = self.client.get("https://jsonplaceholder.typicode.com/posts")
        if response.ok:
            rsp = response.json()
            #print(f"JSONPlaceholder: {rsp}")
        else:
            print(f"Error: Status code {response.status_code}")
            
    @task(1)
    def get_weather(self):
        try:        
            response = self.client.get("https://wttr.in/Novosibirsk?format=j1", timeout=3, name="/Novosibirsk?format=j1", catch_response=True)           
            if response.ok:        
                rsp = response.json()        
                print(f"wttr: {rsp}")        
            else:        
                print(f"Error: Status code {response.status_code}")        
                    
        except requests.exceptions.Timeout or requests.exceptions.ReadTimeout or requests.exceptions.ConnectionError:        
            print("Error: Request timed out")        
            response.failure("Request timed out")
    

                
