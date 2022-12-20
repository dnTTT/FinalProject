class ClientDataDelete:
    mac_address = ""
    active = False

    def __init__(self, mac_address, active):
        self.mac_address = mac_address
        self.active = active
