# Services
## ButtonInputService
## CommandInterpreterService
## LightManagerService
## MusicManagerService
## TerminalInputService
## WakeOnLanManagerService
# System Configuration
## Wake-On-Lan (WOL)
In order for WOL to work, the computer needs to be configured to do so. This might require extra steps depending on your motherboard and OS. Using my setup, I had to modify both my Windows settings and my BIOS:
### Windows Configuration
In "Device Manager", select "Network Adapters" and double-click on your network adapter. In the tab "Power Management", make sure you've checked "Allow this device to wake the computer". If you have an Intel network card, click on the "Advanced" tab, select "Wake on Magic Packet" and select the value "Enabled". If you do not see this option, it might be necessary to download the latest Intel Network Adapters from [here](https://downloadcenter.intel.com/download/25016/Ethernet-Intel-Network-Adapter-Driver-for-Windows-10?product=82186).

In "Power & Sleep Settings", click on "Additional Power Settings". Then, in "Power Options", click on "Chose what the power buttons do". Then, in "System Settings", click on "Change Settings that are currently unavailable" and uncheck "Turn on fast startup (recommended)". 

### BIOS Configuration
Consult your motherboard guide on how to turn on WOL. For instance, for an Asus motherboard, you have to go in "Advanced > APM Configuration", set "ErP Ready" to "Disabled" and "Power On By PCI-E/PCI" to "Enabled".
