import time

class VoiceManager:
    def __init__(self):
        self.devices = {}  # {ip: {id, last_seen}}
        self.signaling_box = []

    def update_device(self, client_ip, device_id):
        self.devices[client_ip] = {"id": device_id, "last_seen": time.time()}
        # 缩短超时时间，确保列表极速更新
        now = time.time()
        self.devices = {ip: d for ip, d in self.devices.items() if now - d['last_seen'] < 5}

    def push_signal(self, signal):
        self.signaling_box.append(signal)
        if len(self.signaling_box) > 100: self.signaling_box.pop(0)

    def pull_signals(self, target_id):
        # 提取发给我的信令并立即清空
        res = [s for s in self.signaling_box if s.get('to') == target_id]
        self.signaling_box = [s for s in self.signaling_box if s.get('to') != target_id]
        return res

    def get_online_list(self):
        return list(self.devices.values())

manager = VoiceManager()