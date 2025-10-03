# API Contract

This document defines the API endpoints, request/response formats, and error handling conventions for the Movie Recommender System.

---

## Base URL

https://<service-url>/api/v1


---

## Endpoints

### 1. **GET /health**
- **Purpose**: Verify service availability.  
- **Request**: None.  
- **Response**:
```json
{
  "status": "ok",
  "uptime": "12345s"
}
```

### 2. **POST /recommend**
- **Purpose**: Fetch movie recommendations for a given user. 
- **Request Body**:  
```json
{
  "user_id": "12345",
  "num_recs": 5
}
```
- **Response**:  
```json
{
  "user_id": "12345",
  "recommendations": [
    {"movie_id": "m101", "title": "Inception", "score": 0.97},
    {"movie_id": "m205", "title": "The Matrix", "score": 0.95}
  ]
}
```
## 3. **POST /feedback**
- **Purpose**: Log user feedback on a recommendation (used for model retraining).
- **Request Body**:  
```json
{
  "user_id": "12345",
  "movie_id": "m101",
  "feedback": "like"   // values: "like", "dislike"
}
```
- **Response**:  
```json
{
  "status": "success",
  "message": "Feedback recorded"
}
```
## Input / Output Conventions

- All requests/responses use JSON.
- Required fields must be present; optional fields may be omitted.
- Timestamps use ISO 8601 format.
- IDs are strings.

## Error Handling

- **Error Response Format**:
```json
{
  "error": {
    "code": 400,
    "message": "Invalid request payload"
  }
}
```
- **Common Error Codes**:

- 400 Bad Request: Malformed request or missing required fields.
- 401 Unauthorized: Invalid or missing authentication token.
- 404 Not Found: Resource not found.
- 500 Internal Server Error: Unexpected backend issue.

## Notes

- Future versions may include /train or /metrics endpoints.
- API should remain backward compatible within v1.