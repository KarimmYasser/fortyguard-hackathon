# Authentication - FortyGuard Temperature API®

> **Official Docs Source:** [https://docs-api.fortyguard.com/docs/authentication](https://docs-api.fortyguard.com/docs/authentication)

FortyGuard's Enterprise API uses direct **API key-based authentication** to ensure secure and controlled access to all endpoints.

Every request to the API must include a valid API Key provided upon registration or via your organization's FortyGuard dashboard.

---

## 🔒 Header Specification

Include your API key in the HTTP request header:

```http
api-key: YOUR_API_KEY
```

- **Header Name:** `api-key` (case-insensitive in HTTP/1.1 and HTTP/2)
- **Value:** Your active FortyGuard API Key string
- **Protocol:** HTTPS (All non-TLS requests are rejected)

---

## 🛡️ Security Best Practices

1. **Keep Keys Confidential:** Never expose API keys in client-side applications (browsers, mobile apps) or commit them to public version control repositories.
2. **Use Environment Variables:** Store keys in secure environment variables (`FORTYGUARD_API_KEY`) or secret management vaults (AWS Secrets Manager, GCP Secret Manager, Doppler).
3. **Server-Side Proxy:** Route frontend requests through your own backend server to inject the `api-key` header securely.

---

## 💻 Code Examples

### cURL
```bash
curl -X POST https://api.fortyguard.com/v1/heatmap \
  -H "api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"granularity": 100, ...}'
```

### Python
```python
import os
import requests

api_key = os.environ.get("FORTYGUARD_API_KEY", "YOUR_API_KEY")
headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

response = requests.get("https://api.fortyguard.com/v1/status/test_id", headers=headers)
```

### Node.js / JavaScript
```javascript
const apiKey = process.env.FORTYGUARD_API_KEY || "YOUR_API_KEY";

const response = await fetch("https://api.fortyguard.com/v1/heatmap", {
  method: "POST",
  headers: {
    "api-key": apiKey,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ ... })
});
```
