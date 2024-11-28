from cipher.plugins import CipherPlugin, CipherAPI
import os, platform

class neofetch(CipherPlugin):
    def __init__(self, api: CipherAPI, config):
        super().__init__(api, config)
        self.register_commands()

    def on_enable(self):
        print("neofetch enabled.")

    def on_disable(self):
        print("neofetch disabled.")
        
    def register_commands(self):
        @CipherPlugin.command(name="neofetch")
        def neofetch(args):
            print("OS: "+platform.system()+" "+platform.version()+" "+platform.machine())