# CheapTAS
### *The poor man's replay device for SNES console verification*
---

CheapTAS is a little project I threw together while I was waiting for my TAStm32 to arrive. It's based off of GhostSonic's Arduino replay device, but updated with a new protocol, new interface, improved reliability, and support for standard .r16m input dumps. GhostSonic's legacy .TAS format, while deprecated, is also still supported.

I wanted to merge the user experience of top-tier replay devices (such as the TAStm32 by Ownasaurus, TASLink by micro500, or total's PSoC5 replay device) with the accessibility of the AVR platform. (They're cheap and *everywhere!*)

## Requirements
CheapTAS does not currently have its own custom PCB; I'd eventually like to design a nice tiny board, though, that either connects directly to the SNES controller port (with a 3D-printed housing) or that uses TASLink-style RJ45 cables.

You will need:
- an AVR-based development board. (This was tested on an ATMega328p with my trusty Arduino Uno, and GhostSonic's original device used a Mega 2560. Other AVRs might require some interrupt or I/O port modifications.)
- Python 3 with pySerial (`pip3 install pyserial` if you haven't already installed it)
- Some method of connecting to the SNES controller port. CheapTAS doesn't currently support using the two additional SNES data lines, so don't worry about going out of your way to get 7-wire cables. Here's a few methods:
	- Chop the cable off of a controller. This is relatively easy to get your hands on, but is unshielded (susceptible to interference) and is only a five-wire connection in 99% of controllers.
	- TASLink-style RJ45 cables. micro500 defined a connection standard with the TASLink board that is used with pretty much every modern replay device today: essentially a CAT5e or CAT6 shielded patch cable terminated with a controller connector on one end. Well-made cables are hard to find (often, you must build them yourself), but are the ultimate solution: 7 wires, durable, and shielded from interference.

## Usage
1. *Flash the firmware.* For simplicity, this is done using the Arduino environment.
2. *Establish a serial connection between your PC and the AVR.* You probably already did this in step 1...unless you programmed your AVR using an AVRISP or similar.
3. ***TODO***

## Scripts
The CheapTAS scripts are a work in progress; they're currently just a slightly hacked version of GhostSonic's original scripts. Current scripts available are:
- `r16mplay.py`: Initial .r16m playback script. It works, but there's lots of room for improvement.
- `SNES_TASPlayer.py`: Legacy .TAS playback script.
- `SNES_TASPlayer_console.py`: Slightly hacked .TAS playback script to select file via console arguments.
- `SNES_Keyboard_Control.py`: Legacy Windows-only (requires pywin32) tool to pipe keyboard controls through CheapTAS.
- `SNES_Keyboard_Control_Recorder.py`: Same thing as above, but simultaneously records keyboard inputs to `recording.TAS` as well.

GhostSonic's keyboard bindings: WASD for directions, N for SNES Y, M for SNES B, K for SNES A, J for SNES X, Q for SNES L, R for SNES R, ENTER for SNES Start, BACKSPACE for SNES Select.

## Wishlist
- Improve buffering
- Implement SPI hardware-accelerated bitbanging
- Make keyboard control platform-independent
- Add gamepad support to keyboard control
- Convert recording scripts to .r16m



## Appendix: GhostSonic's legacy .TAS format
GhostSonic's .TAS format is essentially a quite-stripped-down .r16m. Where .r16m stores 16 bytes per latch (2 bytes/controller * 4 controllers/port * 2 ports), .TAS only stores the two bytes for port 1, controller 1. Additionally, it flips the entire 16-bit word around: the buttons are ordered `0000RLXA rlduSsYB` instead of `BYsSudlr AXLR0000` as they are in .r16m. 

(This is something that *still* baffles me about .r16m to this day: it stores the button bits in the *opposite* order of how they are sent to the SNES. GhostSonic's .TAS format actually makes a bit more sense in this respect, hah.)

Around this time, Ilari created a Lua script for the lsnes emulator to dump a .TAS file from an LSNES movie. It's still available here: http://tasvideos.org/forum/viewtopic.php?p=327260#327260