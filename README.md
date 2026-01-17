# Nebula Proxy

A modern web-based reverse proxy application built with FastAPI (Python) and React that allows you to access local network web applications through a unified dashboard with iframe embedding. Perfect for use with Tailscale to securely access your home lab applications remotely.

## Features

✨ **Key Features:**
- 🔄 Full reverse proxy with intelligent URL rewriting
- 🖼️ iframe embedding with automatic header manipulation
- 📱 Modern React dashboard for managing proxies
- 🔒 Prepared for Tailscale integration
- 🐳 Complete Docker containerization
- ⚡ Async request handling with FastAPI
- 🎨 Beautiful dark-mode UI with shadcn/ui components

## Architecture

**Backend:** FastAPI with httpx for async proxying and Beautiful Soup for HTML rewriting
**Frontend:** React with Tailwind CSS and shadcn/ui
**Container:** Docker with docker-compose

## How It Works

1. **Proxy Management:** Add your local network applications (e.g., `http://192.168.1.100:8123`)
2. **URL Rewriting:** All requests and HTML content are rewritten to pass through the proxy
3. **Header Manipulation:** Removes X-Frame-Options, CSP restrictions, and adds CORS headers
4. **iframe Display:** Apps load seamlessly in iframes with proper routing
5. **Tailscale Ready:** Install Tailscale on the host to access remotely

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Local network applications you want to proxy

### Installation

1. **Clone the project:**
```bash
git clone https://github.com/dcbert/NebulaProxy.git
cd NebulaProxy
```

2. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

3. **Access the dashboard:**
Open your browser to `http://localhost:8000`

### First-Time Setup

1. Click "**+ Add Proxy**" in the sidebar
2. Enter your application details:
   - **Name:** Friendly name (e.g., "Home Assistant")
   - **Target URL:** Full URL with protocol (e.g., `http://192.168.1.100:8123`)
   - **Description:** Optional description
3. Click "**Add Proxy**"
4. Select the proxy from the sidebar to view it in the iframe

## Configuration

### Manual Configuration

You can manually edit the proxy configuration file:

```bash
# Copy the example config
cp config/proxies.example.json config/proxies.json

# Edit with your proxies
nano config/proxies.json
```

Example configuration:
```json
[
  {
    "id": "homeassistant",
    "name": "Home Assistant",
    "target_url": "http://192.168.1.100:8123",
    "enabled": true,
    "description": "Smart home control"
  },
  {
    "id": "plex",
    "name": "Plex Media Server",
    "target_url": "http://192.168.1.101:32400",
    "enabled": true,
    "description": "Media streaming"
  }
]
```

## Tailscale Integration

To access your local apps remotely through Tailscale:

1. **Install Tailscale on the host machine:**
```bash
# macOS
brew install tailscale

# Linux
curl -fsSL https://tailscale.com/install.sh | sh
```

2. **Start Tailscale:**
```bash
sudo tailscale up
```

3. **Get your Tailscale IP:**
```bash
tailscale ip -4
```

4. **Access from anywhere:**
Navigate to `http://[tailscale-ip]:8000` from any device on your Tailscale network

## Development

### Running Locally (Without Docker)

**Backend:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run FastAPI server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
# Install Node dependencies
cd frontend
npm install

# Run React dev server
npm start
```

The React dev server will proxy API requests to the FastAPI backend.

### Project Structure

```
ReverseProxyUmbrel/
├── backend/
│   └── main.py                 # FastAPI application with proxy logic
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js              # Main React component
│   │   ├── App.css             # Styling
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── config/
│   └── proxies.example.json    # Example proxy configuration
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container image definition
├── requirements.txt            # Python dependencies
└── README.md
```

## Technical Details

### Proxy Features

**Header Manipulation:**
- Removes `X-Frame-Options` to allow iframe embedding
- Modifies `Content-Security-Policy` frame-ancestors
- Adds CORS headers for cross-origin requests
- Rewrites `Host`, `Referer`, and other headers

**URL Rewriting:**
- Rewrites all `href` attributes in `<a>` and `<link>` tags
- Rewrites all `src` attributes in `<img>`, `<script>`, `<iframe>`, etc.
- Rewrites form `action` attributes
- Adds base tag for relative URL resolution
- Handles both absolute and relative URLs

**Supported Methods:**
- GET, POST, PUT, DELETE, PATCH, OPTIONS

### Known Limitations

Some applications may not work perfectly in iframes due to:
- JavaScript-based frame-busting code
- Complex WebSocket implementations
- Single-page apps with aggressive client-side routing
- Apps that use postMessage with origin checking

For best results, use with:
- Traditional server-rendered web apps
- Dashboard applications
- Content management systems
- Media servers

## API Endpoints

### Proxy Management

- `GET /api/proxies` - List all proxies
- `POST /api/proxies` - Create a new proxy
- `PUT /api/proxies/{proxy_id}` - Update a proxy
- `DELETE /api/proxies/{proxy_id}` - Delete a proxy

### Proxying

- `ANY /proxy/{proxy_id}/{path}` - Proxy requests to target application

## Troubleshooting

**App not loading in iframe:**
- Check browser console for errors
- Verify the target URL is accessible from the container
- Some apps have strict frame-busting that can't be bypassed

**CORS errors:**
- The proxy should handle CORS automatically
- Check backend logs for proxy errors

**Connection refused:**
- Ensure target URL uses correct protocol (http/https)
- Verify the target application is running
- Check firewall rules on target machine

**View logs:**
```bash
docker-compose logs -f reverse-proxy
```

## Security Notes

⚠️ **Important Security Considerations:**

- This proxy bypasses security headers (X-Frame-Options, CSP)
- Only expose through Tailscale, not directly to the internet
- Configure proper authentication on your proxied applications
- Review and limit which apps you expose through this proxy
- Keep the container and dependencies updated

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - use freely for personal and commercial projects.

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [httpx](https://www.python-httpx.org/) - Async HTTP client
- [React](https://react.dev/) - UI framework
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Tailscale](https://tailscale.com/) - Secure network access
