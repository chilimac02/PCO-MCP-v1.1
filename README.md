# PCO MCP Server v1.1

A Model Context Protocol (MCP) server for Planning Center Online (PCO) API.

## Features

- Exposes PCO API functionality via MCP JSON-RPC
- Supports:
  - Listing service types
  - Getting plans (events) for a service type
  - Getting headcounts for a plan
  - Getting aggregated attendance
- Dockerized for easy deployment

## Docker Deployment

### Quick Start

```bash
# 1. Configure environment variables
cp .env.example .env
nano .env  # Fill in your PCO_APP_ID and PCO_SECRET

# 2. Build and run
docker compose up --build

# 3. Access at http://localhost:8000
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| PCO_APP_ID | Yes | Your PCO App ID |
| PCO_SECRET | Yes | Your PCO App Secret |
| PORT | No (default: 8000) | Server port |
| LOG_LEVEL | No (default: info) | Logging level |

## MCP Methods

### `get_service_types`
Returns a list of all service types (e.g., Sunday Worship, Children's Check-in).

- **Parameters:** None
- **Returns:** Array of service type objects with `id` and `name`.

### `get_plans`
Get plans (service instances) for a service type.

- **Parameters:**
  - `service_type_id` (string): The service type ID
  - `start_date` (string, optional): Start date filter (ISO format: YYYY-MM-DD)
  - `end_date` (string, optional): End date filter (ISO format: YYYY-MM-DD)
- **Returns:** Array of plan objects.

### `get_headcounts`
Get headcount data for a specific plan time.

- **Parameters:**
  - `plan_time_id` (string): The plan time ID
- **Returns:** Array of headcount objects.

### `get_aggregated_attendance`
Get aggregated attendance across multiple service types for a date range.

- **Parameters:**
  - `service_type_ids` (array): List of service type IDs
  - `start_date` (string): Start date (ISO format: YYYY-MM-DD)
  - `end_date` (string): End date (ISO format: YYYY-MM-DD)
- **Returns:** Object mapping date strings to total attendance counts.

### `get_year_over_year_comparison`
Get year-over-year attendance comparison.

- **Parameters:**
  - `service_type_ids` (array): List of service type IDs
  - `reference_date` (string): Reference date (ISO format: YYYY-MM-DD)
  - `lookback_days` (integer, optional): How many days back to compare (default: 90)
- **Returns:** Object with `current` and `previous_year` attendance data.

## Running Without Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn app.main:app --reload --port 8000

# Test with curl
curl -X POST http://localhost:8000/mcp/initialize
```

## Security

- Never commit `.env` file to version control
- Use `.env.example` as a template
- Environment variables are loaded automatically from `.env`

## License

MIT License - See LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the maintainers.
