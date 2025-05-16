from supabase import create_client, Client
from dotenv import load_dotenv
import os

class DataBase():
    load_dotenv()
    url = "https://eywvcvsyhxfgjahzuemt.supabase.co"
    Supabase_key = os.getenv("Supabase_key")
    supabase: Client = create_client(url, Supabase_key)
    TOP10_Data = []
    
    def Get_Score_By_Name(self, name):
        response = self.supabase.table("Score").select("Score").eq("Name", name).execute()
        if response.data:
            return response.data[0]["Score"]
        else:
            return -1
        
    def Update_Score(self, name, score):
        data = {
            "Name": name,
            "Score": score
        }
        if not name or not isinstance(score,int):
            return "Error: Name can't be empty and Score should be integer"
        
        Old_Score = self.Get_Score_By_Name(name)
        
        if Old_Score == -1: # 還沒有這個Name的紀錄
            self.supabase.table("Score").insert(data).execute()
        elif Old_Score < score:
            self.supabase.table("Score").update(data).eq("Name", name).execute()
        return "Success"

    def Get_Top10(self):    
        response = self.supabase.table("Score").select("*").order("Score", desc=True).limit(10).execute()
        data = list(response.data)
        # [{'Name': '老姐', 'Score': 1000}, {'Name': 'Lynn', 'Score': 20}]
        return data
        