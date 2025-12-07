# Production Deployment Guide - Low-Latency Optimized

Complete guide for deploying the Hackathon project with optimal performance.

## Architecture Overview

- **Frontend**: Docusaurus static site (GitHub Pages/Vercel)
- **Backend**: FastAPI + Gunicorn + Uvicorn workers
- **Database**: Neon (serverless PostgreSQL)
- **Vector DB**: Qdrant Cloud
- **Caching**: In-memory LRU cache

## Performance Optimizations Implemented ✅

### Backend Optimizations
1. ✅ **GZIP Compression**: Responses > 1KB automatically compressed
2. ✅ **PostgreSQL Connection Pooling**: 10 persistent + 20 overflow connections
3. ✅ **Async Qdrant Client**: Parallel vector search operations
4. ✅ **Response Streaming**: Server-Sent Events for chat (`/api/chat/stream`)
5. ✅ **Embedding Cache**: In-memory LRU cache (1000 entries)
6. ✅ **CORS Preflight Caching**: 1-hour cache for OPTIONS requests
7. ✅ **HTTP Keep-Alive**: 5-second connection reuse
8. ✅ **Multi-Worker Server**: 4+ Uvicorn workers via Gunicorn

### Server Configuration
- **Workers**: Auto-configured (2-4 per CPU core)
- **Timeout**: 120s for AI requests
- **Keep-Alive**: 5s
- **Graceful Shutdown**: 30s

---

## Backend Deployment (Render) - Recommended

### 1. Prerequisites
- Render account
- GitHub repository connected
- Environment variables ready

### 2. Create Web Service on Render

**Settings:**
- **Build Command**: `pip install -r backend/requirements-prod.txt`
- **Start Command**: `cd backend && bash start.sh`
- **Environment**: Python 3.11
- **Instance Type**: Standard (512MB+ RAM recommended)

**Environment Variables:**
```bash
NEON_DATABASE_URL=postgresql://user:pass@host/dbname
QDRANT_URL=https://your-instance.cloud.qdrant.io
QDRANT_API_KEY=your_api_key
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your_256_bit_secret
WEB_CONCURRENCY=4
```

**Region Selection** (for low latency):
- **US Users**: Oregon (US-West) or Ohio (US-East)
- **EU Users**: Frankfurt (EU-Central)
- **Asia Users**: Singapore (Asia-Pacific)

### 3. Deploy
Render automatically deploys on git push. Monitor deployment logs for:
```
✓ Database connection verified
✓ Qdrant connection verified
✓ Backend initialization completed successfully
✓ Starting Gunicorn with 4 Uvicorn workers
```

### 4. Verify Health
```bash
curl https://your-app.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "qdrant": "connected (N collections)"
  }
}
```

---

## Backend Deployment (Railway) - Alternative

### 1. Install Railway CLI
```bash
npm i -g @railway/cli
railway login
```

### 2. Initialize Project
```bash
cd backend
railway init
```

### 3. Set Environment Variables
```bash
railway variables set NEON_DATABASE_URL="..."
railway variables set QDRANT_URL="..."
railway variables set QDRANT_API_KEY="..."
railway variables set OPENAI_API_KEY="..."
railway variables set JWT_SECRET_KEY="..."
railway variables set WEB_CONCURRENCY=4
```

### 4. Deploy
```bash
railway up
```

Railway will detect Python and use `start.sh` automatically.

---

## Frontend Deployment (GitHub Pages)

### 1. Update Backend URL

Edit `docusaurus-book/.env.production`:
```env
REACT_APP_API_URL=https://your-backend.onrender.com
```

### 2. Update Backend CORS

Add your frontend URL to `backend/src/main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:3001",
    "https://nabeerak.github.io/hackathon/",
    "https://nabeerak.github.io",
],
```

### 3. Build and Deploy
```bash
cd docusaurus-book
npm run build
npx gh-pages -d build
```

Or use GitHub Actions (already configured in repository).

---

## Frontend Deployment (Vercel) - Alternative

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Configure Environment
Create `docusaurus-book/.env.production`:
```env
REACT_APP_API_URL=https://your-backend.onrender.com
```

### 3. Deploy
```bash
cd docusaurus-book
vercel --prod
```

Vercel provides:
- Global CDN
- HTTP/2 & HTTP/3
- Automatic compression
- Edge caching

---

## Optimal Hosting Regions

### For US-Based Users
- **Backend**: Render US-West (Oregon) or US-East (Ohio)
- **Database**: Neon US-East
- **Qdrant**: US-East or US-West
- **Expected Latency**: 20-60ms (same region)

### For European Users
- **Backend**: Render EU-Central (Frankfurt)
- **Database**: Neon EU-West
- **Qdrant**: EU-Central
- **Expected Latency**: 20-60ms (same region)

### For Global Users
- **Backend**: Multi-region (Render supports)
- **Frontend**: CDN with global edge nodes (Vercel recommended)
- **Database**: Neon with read replicas
- **Qdrant**: Region closest to primary users

**Cross-Region Latencies:**
- US ↔ EU: 80-150ms
- US ↔ Asia: 150-300ms
- EU ↔ Asia: 180-350ms

---

## CDN Configuration

### GitHub Pages (Built-in CDN)
- Automatic global distribution
- HTTPS enabled by default
- Configure caching via headers

### Vercel (Recommended for CDN)
Vercel provides:
- Automatic edge caching
- Brotli + Gzip compression
- HTTP/2 & HTTP/3
- Global PoPs (85+ locations)

Create `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/(.*).html",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, must-revalidate"
        }
      ]
    }
  ]
}
```

### Cloudflare (Free Alternative)
1. Add domain to Cloudflare
2. Enable:
   - Auto Minify (JS, CSS, HTML)
   - Brotli compression
   - HTTP/2, HTTP/3
   - Browser Cache TTL: 4 hours

3. Page Rules:
   - `*.js`, `*.css`: Cache Everything, TTL 1 month
   - `*.html`: Bypass cache

---

## Performance Testing

### Load Testing Backend
```bash
# Install Apache Bench
# Windows: Download from Apache binaries
# Linux: apt-get install apache2-utils
# Mac: brew install httpd

# Test health endpoint
ab -n 1000 -c 10 https://your-backend.onrender.com/api/health

# Test chat endpoint
ab -n 100 -c 5 -p chat-request.json -T application/json \
  https://your-backend.onrender.com/api/chat
```

Create `chat-request.json`:
```json
{
  "message": "What is Physical AI?",
  "conversation_id": null
}
```

### Expected Metrics
- **Health endpoint**: < 100ms p95
- **Chat endpoint**: 1-3s p95 (OpenAI dependent)
- **Streaming chat**: First byte < 500ms
- **Vector search**: < 200ms p95
- **Database query**: < 50ms p95

### Frontend Performance
Use Lighthouse or WebPageTest:
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Total Page Size**: < 2MB

---

## Monitoring & Logging

### Render Built-in Monitoring
- Real-time logs
- Metrics dashboard
- Auto-restart on failure

### Optional: Sentry Integration

Add to `backend/requirements-prod.txt`:
```
sentry-sdk==1.40.0
```

Configure in `backend/src/main.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
)
```

---

## Scaling Recommendations

### Backend Horizontal Scaling
1. **Render**: Increase instance count in dashboard
2. **Railway**: Deploy to multiple regions
3. **Load Balancer**: Use Render's built-in LB

### Backend Vertical Scaling
- Upgrade instance size (more CPU/RAM)
- Typical needs: 512MB-2GB RAM for 100-1000 users

### Database Scaling
- **Neon Autoscaling**: Automatically handles load
- **Connection Pooling**: Already configured (10+20)
- **Read Replicas**: Add for heavy read workloads

### Cache Scaling
- Current: In-memory LRU (1000 entries)
- Upgrade to: Redis (distributed caching)
- Benefits: Shared cache across workers

---

## Cost Optimization

### Estimated Monthly Costs
| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Render Web Service | $0 (limited) | $7-25/mo |
| Neon Database | $0 (0.5GB) | $19+/mo |
| Qdrant Cloud | $0 (1GB) | $25+/mo |
| OpenAI API | Pay-per-use | $10-100/mo |
| **Total** | ~$10-20/mo | $50-150/mo |

### Cost Saving Tips
1. ✅ Cache embeddings to reduce OpenAI calls (already implemented)
2. ✅ Use Neon's free tier for development
3. ✅ Optimize Qdrant queries to reduce latency
4. Use streaming to improve UX without extra cost
5. Monitor and optimize slow database queries
6. Reduce worker count if traffic is low

---

## Security Checklist

- [x] HTTPS enabled (Render/Vercel automatic)
- [x] Environment variables secured (not in code)
- [x] JWT secret is strong (256-bit minimum)
- [x] Database uses SSL connections
- [x] CORS configured for specific origins only
- [x] Input validation on all endpoints
- [x] SQL injection protection (SQLAlchemy ORM)
- [ ] Rate limiting (add if needed)
- [ ] API key rotation policy
- [ ] Regular dependency updates

### Add Rate Limiting (Optional)

Install:
```bash
pip install slowapi
```

Configure in `main.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat_endpoint(...):
    ...
```

---

## Troubleshooting

### High Latency
1. **Check region proximity**:
   - Backend ↔ Database in same region?
   - Backend ↔ Qdrant in same region?
   - Users ↔ Backend reasonable distance?

2. **Enable query logging**:
   ```python
   engine = create_engine(..., echo=True)
   ```

3. **Profile slow queries**:
   - Check Neon query insights
   - Look for N+1 queries
   - Add database indexes if needed

4. **Monitor OpenAI latency**:
   - Typical: 1-3s per request
   - Use streaming for better UX

### Memory Issues
1. Reduce worker count: `WEB_CONCURRENCY=2`
2. Lower pool size in `database.py`:
   ```python
   pool_size=5, max_overflow=10
   ```
3. Reduce cache size in `cache_service.py`:
   ```python
   CacheService(max_size=500)
   ```

### Connection Errors
1. **Database**: Verify Neon connection string format
2. **Qdrant**: Check API key and URL
3. **CORS**: Ensure all origins are whitelisted
4. **Firewall**: Check cloud provider security settings

### Deployment Failures
1. **Build fails**: Check Python version (3.11)
2. **Start fails**: Check `start.sh` permissions (chmod +x)
3. **Import errors**: Verify all dependencies in requirements
4. **Port binding**: Use `${PORT:-8000}` for cloud platforms

---

## Post-Deployment Checklist

- [ ] Backend deployed and healthy (`/api/health` returns 200)
- [ ] Database migrations run successfully
- [ ] Qdrant connected and collections exist
- [ ] Frontend deployed and accessible
- [ ] Frontend → Backend connectivity working
- [ ] CORS configured correctly
- [ ] Authentication flow works (sign up, sign in, sign out)
- [ ] Chat functionality works (regular + streaming)
- [ ] Conversation history persists
- [ ] User data features work (bookmarks, notes, progress)
- [ ] Performance meets targets (see metrics above)
- [ ] Error monitoring configured (optional)
- [ ] SSL/HTTPS enabled
- [ ] Environment variables secured
- [ ] Backups configured (Neon automatic)

---

## Next Steps After Deployment

1. **Custom Domain** (Optional):
   - Configure on Render/Vercel
   - Update CORS settings
   - Enable automatic SSL

2. **CI/CD Pipeline**:
   - GitHub Actions for auto-deploy
   - Run tests before deployment
   - Automatic rollback on failure

3. **Enhanced Monitoring**:
   - Set up Sentry for error tracking
   - Configure uptime monitoring (UptimeRobot)
   - Set up alerting for failures

4. **Performance Optimization**:
   - Analyze real user metrics
   - Optimize slow endpoints
   - Add Redis caching if needed

5. **Backup Strategy**:
   - Neon: Automatic point-in-time recovery
   - Export chat histories periodically
   - Version control for code changes

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Neon Docs**: https://neon.tech/docs
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Docusaurus Docs**: https://docusaurus.io/

---

## Current Deployment Status

- ✅ Backend: Optimized for production (connection pooling, compression, streaming)
- ✅ Frontend: Ready for deployment
- ✅ Database: PostgreSQL with connection pooling
- ✅ Vector DB: Async Qdrant client
- ✅ Caching: In-memory LRU cache for embeddings
- ✅ Deployment scripts: Gunicorn + Uvicorn configuration
- ⚠️  Monitoring: Optional (Sentry integration available)
- ⚠️  Rate limiting: Not configured (add if needed)
