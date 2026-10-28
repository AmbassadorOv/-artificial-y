import pandas as pd
import numpy as np
from FireSeal_Engine import FireSealEngine

class SwarmExcelConnector:
    def __init__(self, secret_key: bytes):
        self.seal_engine = FireSealEngine(secret_key)

    def initialize_swarm_grid(self, num_agents: int, output_path: str):
        """
        מייצר את קובץ האקסל (ה-Grid) עם 10,000 סוכנים.
        כל סוכן מקבל קואורדינטות X, Y, Z, חיבור לניצוץ (Spark), וקונסטלציה.
        """
        print(f"[SWARM] מייצר גריד של {num_agents} סוכנים...")

        # יצירת קואורדינטות אקראיות בתוך מרחב 288 הניצוצות
        np.random.seed(42) # לקבלת דטרמיניזם
        data = []

        for i in range(1, num_agents + 1):
            agent_id = f"Agent_{i:05d}"
            # קואורדינטות XYZ אקראיות בטווח של 0-100
            x = np.random.uniform(0, 100)
            y = np.random.uniform(0, 100)
            z = np.random.uniform(0, 100)

            # חיבור לניצוץ (Spark ID 1-288)
            spark_id = np.random.randint(1, 289)

            # קביעת קונסטלציה
            constellation = "Leo_40deg" if i % 2 == 0 else "Taurus_120deg"

            # הנפקת חותמת אש ראשונית (MOVE)
            seal = self.seal_engine.generate_seal(
                agent_id=agent_id,
                target_coords=(round(x, 4), round(y, 4), round(z, 4)),
                constellation=constellation,
                action="MOVE"
            )

            # הוספת הנתונים לשורה
            data.append({
                "Agent_ID": agent_id,
                "X": round(x, 4),
                "Y": round(y, 4),
                "Z": round(z, 4),
                "Spark_Node": spark_id,
                "Constellation": constellation,
                "Seal_ID": seal["seal_id"],
                "HMAC_Signature": seal["hmac_signature"],
                "Status": "ACTIVE"
            })

        # יצירת DataFrame ושמירה לאקסל
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        print(f"[SWARM] הגריד נשמר בהצלחה בקובץ: {output_path}")
        return df

    def process_movement(self, input_excel_path: str, output_excel_path: str):
        """
        קורא את האקסל, מייצר תנועה חדשה לכל סוכן, ומנפיק חותמות אש חדשות.
        """
        print(f"[SWARM] קורא אקסל ומפעיל תנועה: {input_excel_path}")
        df = pd.read_excel(input_excel_path)

        for index, row in df.iterrows():
            # שינוי קואורדינטות קל (תנועה)
            new_x = row["X"] + np.random.uniform(-1, 1)
            new_y = row["Y"] + np.random.uniform(-1, 1)
            new_z = row["Z"] + np.random.uniform(-1, 1)

            # הנפקת חותמת אש חדשה
            new_seal = self.seal_engine.generate_seal(
                agent_id=row["Agent_ID"],
                target_coords=(round(new_x, 4), round(new_y, 4), round(new_z, 4)),
                constellation=row["Constellation"],
                action="MOVE"
            )

            # עדכון השורה
            df.at[index, "X"] = round(new_x, 4)
            df.at[index, "Y"] = round(new_y, 4)
            df.at[index, "Z"] = round(new_z, 4)
            df.at[index, "Seal_ID"] = new_seal["seal_id"]
            df.at[index, "HMAC_Signature"] = new_seal["hmac_signature"]
            df.at[index, "Status"] = "MOVED"

        df.to_excel(output_excel_path, index=False)
        print(f"[SWARM] התנועה הושלמה. הקובץ נשמר ב: {output_excel_path}")

# ==========================================
# הרצה (Execution)
# ==========================================
import os

if __name__ == "__main__":
    secret = os.environ.get("FIRE_SEAL_SECRET_KEY", "Suzuki_Emperor_Sovereign_Key_2026")
    SECRET_KEY = secret.encode('utf-8') if isinstance(secret, str) else secret

    connector = SwarmExcelConnector(SECRET_KEY)

    # 1. יצירת הגריד הראשוני
    connector.initialize_swarm_grid(num_agents=10000, output_path="swarm_grid_initial.xlsx")

    # 2. הפעלת תנועה על כל הסוכנים
    connector.process_movement(input_excel_path="swarm_grid_initial.xlsx", output_excel_path="swarm_grid_moved.xlsx")
