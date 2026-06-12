# prusa_mk4s_module

A MADSci node module for integrating Prusa MK4S 3D printers and OpenCV optical sensors into an automated/autonomous laboratory.

## Configuration

All configuration is done via environment variables (prefixed `NODE_`), a `settings.yaml` file, or a `.env` file. See [docs/Configuration.md](docs/Configuration.md) for the full reference and `.env.example` for a commented template.

The most important settings to configure:

| Variable | Default | Purpose |
|---|---|---|
| `NODE_PRUSA_IP` | _(required)_ | IP address of the Prusa MK4S |
| `NODE_PRUSA_API_KEY` | _(required)_ | PrusaLink API key for authentication |
| `NODE_URL` | `http://127.0.0.1:2000/` | URL the node binds to and advertises |
| `NODE_NODE_NAME` | _(class name)_ | Human-readable name registered with MADSci |
| `NODE_NODE_ID` | _(auto-generated)_ | Stable node identifier (ULID); set to persist identity across restarts |

Configuration is loaded in priority order: environment variables > `.env` file > `settings.yaml`. A minimal `settings.yaml` might look like:

```yaml
node_name: prusa_alpha
node_description: Prusa MK4S node in the RPL workcell
node_id: 01HPNMZF3SPK48EWA1VXMVYHWV
prusa_ip: 192.168.1.100
prusa_api_key: jjehZqxQ542F9pQ
node_url: "[http://127.0.0.1:2000/](http://127.0.0.1:2000/)"
