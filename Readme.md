# SRE Take-Home Exercise - Endpoint Availability Monitor

This Python script monitors the availability of all HTTP endpoints in the YAML configuration file. It runs and logs availability results every 15 seconds with necessary constraints.

## How to Install and Run

### 1. Clone the Repository
```bash
git clone https://github.com/janeresh/sre-availability-monitor
cd sre-availability-monitor
```

### 2. Set Up a Virtual Environment (Optional)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
The requirements.txt includes pyyaml and requests packages.
### 4. Run the Monitor
```bash
python main.py <configuration.yaml>
```
For example, I have attached the sample configuration yaml file - `sample.yaml`. We can use that as mentioned below.

```bash
python main.py sample.yaml
```

---

## How Issues Were Identified and Changes Made

### Issue 1: If HTTP method field is omitted, the default should be set to GET.
- **Problem**: Missing `method` field would pass `None` to `requests.request`.
- **Fix**: Added `method = endpoint.get('method', 'GET')`.

### Issue 2: If HTTP field is omitted, no headers need to be added to or modified in the HTTP request.
- **Problem**: If `headers` was omitted, it defaulted to `None`.
- **Fix**: Added `headers = endpoint.get('headers', {})`.

### Issue 3: Must ignore port numbers when determining domain
- **Problem**: Splitting URLs only with (`split('//')`, `split(':')`) fails with cases where port is present.
- **Fix**: Added logic to remove port using `split(":")`

### Issue 4: Endpoints are only considered available if they meet the following conditions: Endpoint responds in 500ms or less
- **Problem**: The previous condition only checks if the response status code is between 200 and 299. 
- **Fix**: Added logic to also check if endpoint responds in 500ms or less.

### Check: If body field is omitted, no body is sent in the request.
- **Fix**: Added safe check to parse the body field only when present.
