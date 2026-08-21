# prusa_mk4s_module

A MADSci node module for integrating Prusa MK4S 3D printers and OpenCV optical sensors into an automated/autonomous laboratory.

## Configuration

All configuration is done via environment variables (prefixed `NODE_`), a `settings.yaml` file, or a `.env` file. See [docs/Configuration.md](docs/Configuration.md) for the full reference and `.env.example` for a commented template.

The most important settings to configure:

| Variable | Default | Purpose |
|---|---|---|
| `NODE_PRUSA_IP` | _(required)_ | IP address of the Prusa MK4S |
| `NODE_PRUSA_API_KEY` | _(required)_ | PrusaLink API key for authentication |
| `NODE_URL` | `http://127.0.0.1:2006/` | URL the node binds to and advertises |
| `NODE_NODE_NAME` | _(class name)_ | Human-readable name registered with MADSci |
| `NODE_NODE_ID` | _(auto-generated)_ | Stable node identifier (ULID); set to persist identity across restarts |

Configuration is loaded in priority order: environment variables > `.env` file > `settings.yaml`. A minimal `settings.yaml` might look like:

## Changing Print:

The beauty of this module and additive manufacturing is the fact that anything can be created! In order to change the model being iterated on, follow these steps:
1. Create model in onshape
2. In UpdateOnshape_to_STL.py, change the DID, EID, and WID variables to correspond with the new url
3. If you want to change the printing setting:
   3a. Create new settings in PrusaSlicer and save as a .ini file 
   3b. import into the "configs" file
   3c. change config_file variable in STL_To_PRUSAPRINT.py to new file path
4. In Prusa_Automation.py add/change parametrized variables based on your needs, currently set to recieve a "length" variable

## Printer Errors 
Due to the nature of the code, it is common for a filament stuck error or "FINDA Didn't Trigger" to display on the printer, here is how to fix it.
0. The printer may give an option to "unload filament". Allow the printer to try to fix the issue this mechanically before manually trying anything.
   0a. Good rule of thumb is to wait until the printer displays "HELP" and a QR code + error message
1. Unscrew the tube connecting the MMU unit to the nozzle
2. Retract the filament manually until it is no longer in the Nozzle and MMU Units 
3. Cut the end of the filament at a 45 degree angle
4. Manual insert the filament back though so that the end of the filament is lined up with the exit hole of its stationary MMU track
5. Reattach the disconnected tube and RESET printer
6. Run Print 

```yaml
node_name: prusa_alpha
node_description: Prusa MK4S node in the RPL workcell
node_id: 01HPNMZF3SPK48EWA1VXMVYHWV
prusa_ip: 146.137.240.52
prusa_api_key: jjehZqxQ542F9pQ
node_url: "[http://127.0.0.1:2006/](http://127.0.0.1:2006/)

