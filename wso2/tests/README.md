# WSO2 Integration Testing

Automated backend tests use temporary RSA keys and mocked JWKS resolution; they do not require WSO2. The scripts in `../scripts` are the manual boundary tests after APIM is installed, configured, deployed, published, subscribed, and issued a temporary access token.

Never run rate-limit tests against production. A successful end-to-end gateway claim requires a real request to travel through WSO2, FastAPI, PostgreSQL, and back; automated unit tests do not make that claim.
