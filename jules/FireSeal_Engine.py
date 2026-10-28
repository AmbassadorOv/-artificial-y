import hmac
import hashlib
import json
import uuid
from datetime import datetime, timezone

class FireSealEngine:
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key

    def generate_seal(self, agent_id: str, target_coords: tuple, constellation: str, action: str) -> dict:
        """
        מנפיק חותמת אש קריפטוגרפית המאשרת את מיקום ופעולת הסוכן.
        """
        seal_data = {
            "agent_id": agent_id,
            "issued_at": datetime.now(timezone.utc).isoformat(),
            "seal_id": str(uuid.uuid4()),
            "target_coordinates": target_coords,
            "constellation_azimuth": constellation,
            "action_type": action
        }

        # יצירת חתימת HMAC-SHA256
        payload_str = json.dumps(seal_data, sort_keys=True).encode('utf-8')
        signature = hmac.new(self.secret_key, payload_str, hashlib.sha256).hexdigest()

        seal_data["hmac_signature"] = signature
        return seal_data

    def verify_seal(self, seal: dict) -> bool:
        """
        מאמת את החותמת מול הנתונים. מחזיר True אם תקין.
        """
        received_sig = seal.pop("hmac_signature", None)
        if not received_sig:
            return False

        payload_str = json.dumps(seal, sort_keys=True).encode('utf-8')
        expected_sig = hmac.new(self.secret_key, payload_str, hashlib.sha256).hexdigest()

        # החזרת החתימה למקומה למקרה של שימוש עתידי
        seal["hmac_signature"] = received_sig

        return hmac.compare_digest(received_sig, expected_sig)
