import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import socket
import time

class BluetoothAudioApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bluetooth Audio Device Manager (FreeBSD)")
        self.master.geometry("450x400")

        # Listbox to display available devices
        self.device_listbox = tk.Listbox(master, width=50, height=12)
        self.device_listbox.pack(pady=15)

        # Scan button to discover devices
        self.scan_button = tk.Button(master, text="Scan for Devices", command=self.scan_devices)
        self.scan_button.pack(pady=5)

        # Connect button to initiate the connection
        self.connect_button = tk.Button(master, text="Connect", command=self.connect_device, state=tk.DISABLED)
        self.connect_button.pack(pady=5)

        # Disconnect button to disconnect the device
        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect_device, state=tk.DISABLED)
        self.disconnect_button.pack(pady=5)

        # Store devices and selected device
        self.device_list = []
        self.selected_device = None

    def scan_devices(self):
        """Scans for Bluetooth devices using `hccontrol`."""
        try:
            result = subprocess.run(["sudo", "hccontrol", "-n", "ubt0hci", "inquiry"], capture_output=True, text=True)

            if result.returncode != 0:
                messagebox.showerror("Error", f"Failed to scan for devices: {result.stderr}")
                return

            # Parse onnect button to initiate the connection

            self.device_list = self.parse_bluetooth_inquiry(result.stdout)

            if not self.device_list:
                messagebox.showinfo("No Devices", "No Bluetooth devices found.")
                return

            # Update the Listbox with available devices
            self.device_listbox.delete(0, tk.END)  # Clear previous devices
            for device in self.device_list:
                self.device_listbox.insert(tk.END, f"{device['name']} ({device['bd_addr']})")

            # Enable connect button
            self.connect_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def parse_bluetooth_inquiry(self, inquiry_output):
        """Parse Bluetooth inquiry output."""
        devices = []
        lines = inquiry_output.splitlines()

        for line in lines:
            if "BD_ADDR:" in line:
                bd_addr = line.split("BD_ADDR:")[1].strip()
                name = "Unnamed Device"
                if "name:" in line:
                    name = line.split("name:")[1].strip()
                devices.append({"bd_addr": bd_addr, "name": name})

        return devices

    def pair_device(self, bd_addr):
        """Pair the Bluetooth device before connection (using `hccontrol` on FreeBSD)."""
        try:
            result = subprocess.run(["sudo", "hccontrol", "-n", "ubt0hci", "pair", bd_addr], capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Pairing Error", f"Failed to pair device: {result.stderr}")
                return False
            return True
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during pairing: {str(e)}")
            return False

    def connect_device(self):
        """Connect to the selected Bluetooth device."""
        try:
            selected_index = self.device_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select a device to connect.")
                return

            self.selected_device = self.device_list[selected_index[0]]
            bd_addr = self.selected_device["bd_addr"]

            # Pair the device if not already paired
            if not self.pair_device(bd_addr):
                return

            # Enable authentication and pair if necessary
            self.enable_bluetooth_authentication()
            self.create_bluetooth_alias(bd_addr)

            # Connect using hccontrol
            result = subprocess.run(["sudo", "hccontrol", "-n", "ubt0hci", "create_connection", bd_addr], capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Connection Error", f"Failed to connect: {result.stderr}")
                return

            # Set PulseAudio or virtual_oss
            self.setup_audio_output(bd_addr)

            # Enable the disconnect button
            self.disconnect_button.config(state=tk.NORMAL)
            messagebox.showinfo("Connected", f"Successfully connected to {self.selected_device['name']}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def enable_bluetooth_authentication(self):
        """Enable Bluetooth authentication via hccontrol (FreeBSD)."""
        try:
            result = subprocess.run(["sudo", "hccontrol", "-n", "ubt0hci", "write_authentication_enable", "1"], capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Authentication Error", f"Failed to enable authentication: {result.stderr}")
            else:
                print("Bluetooth authentication enabled.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_bluetooth_alias(self, bd_addr):
        """Create a Bluetooth alias in /etc/bluetooth/hosts (FreeBSD)."""
        hosts_file = '/etc/bluetooth/hosts'
        if not os.path.exists(hosts_file):
            messagebox.showerror("Error", f"{hosts_file} does not exist.")
            return

        with open(hosts_file, "r") as f:
            hosts_data = f.readlines()

        alias_exists = False
        for line in hosts_data:
            if bd_addr in line:
                alias_exists = True
                break

        if not alias_exists:
            with open(hosts_file, "a") as f:
                hostname = socket.gethostname()
                f.write(f"{bd_addr} {hostname}\n")

    def setup_audio_output(self, bd_addr):
        """Configure PulseAudio or virtual_oss to output to Bluetooth device (FreeBSD)."""
        try:
            # Check for PulseAudio with pactl
            result = subprocess.run(["which", "pactl"], capture_output=True, text=True)
            if result.returncode == 0:
                result = subprocess.run(["pactl", "list", "sinks"], capture_output=True, text=True)
                if result.returncode == 0:
                    sinks = result.stdout.splitlines()
                    for line in sinks:
                        if bd_addr in line:
                            result = subprocess.run(["pacctl", "set-default-sink", line.split()[0]], capture_output=True, text=True)
                            if result.returncode != 0:
                                messagebox.showerror("PulseAudio Error", f"Failed to set PulseAudio output: {result.stderr}")
                            else:
                                messagebox.showinfo("Audio Output", "PulseAudio output set to Bluetooth device.")

                            # Restart PulseAudio to apply changes
                            subprocess.run(["pulseaudio", "--kill"])
                            subprocess.run(["pulseaudio", "--start"])

                            return
                    messagebox.showerror("PulseAudio Error", "Bluetooth sink not found.")
            else:
                # Fall back to virtual_oss
                self.setup_virtual_oss_audio(bd_addr)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while setting audio output: {str(e)}")

    def setup_virtual_oss_audio(self, bd_addr):
        """Configure virtual_oss for audio output on FreeBSD."""
        try:
            command = f"sudo virtual_oss -T /dev/sndstat -S -a o,-4 -C 2 -c 2 -r 44100 -b 16 -s 1024 -R /dev/dsp0 -P /dev/bluetooth/{bd_addr} -d dsp -t vdsp.ctl"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Virtual OSS Error", f"Failed to set virtual_oss output: {result.stderr}")
            else:
                messagebox.showinfo("Audio Output", "Virtual OSS output set to Bluetooth device.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while setting virtual_oss output: {str(e)}")

    def disconnect_device(self):
        """Disconnect the Bluetooth device (using `hccontrol` on FreeBSD)."""
        try:
            if not self.selected_device:
                messagebox.showwarning("No Connection", "No device is currently connected.")
                return

            # Check if the device is already disconnected
            result = subprocess.run(["sudo", "hccontrol", "-n", "ubt0hci", "info", self.selected_device["bd_addr"]], capture_output=True, text=True)
            if "not connected" in result.stdout:
                messagebox.showinfo("Already Disconnected", "Bluetooth device is already disconnected.")
                return

            result = subprocess.run(["sudo", "hccontrol", "-n", "ubt0hci", "disconnect", self.selected_device["bd_addr"]], capture_output=True, text=True)
            if result.returncode != 0:
                messagebox.showerror("Disconnect Error", f"Failed to disconnect: {result.stderr}")
                return

            self.disconnect_button.config(state=tk.DISABLED)
            self.selected_device = None
            messagebox.showinfo("Disconnected", "Bluetooth device disconnected successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while disconnecting: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothAudioApp(root)
    root.mainloop()

