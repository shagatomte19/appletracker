
# Job Application Tracker

A comprehensive job application tracking system built with Streamlit and SQLite.

## Features

- 📊 Interactive dashboard with key metrics
- 📈 Visual charts and analytics
- 🔍 Advanced filtering and search
- 📝 Add, edit, and delete applications
- 📁 Export data to CSV
- 💾 Persistent SQLite database
- 📱 Responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shagatomte19/appletracker
cd appletracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Add your job applications using the sidebar form
2. View analytics and charts on the main dashboard
3. Filter and search through your applications
4. Export your data for external analysis

## Project Structure

- `app.py` - Main Streamlit application
- `database.py` - Database operations and management
- `models.py` - Data models and structures
- `utils.py` - Utility functions for charts and calculations
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration

## Deployment Options

### 1. Streamlit Cloud (Recommended for beginners)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

### 2. Heroku Deployment

Create these additional files:

**Procfile:**
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

**runtime.txt:**
```
python-3.13
```

### 3. Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**docker-compose.yml:**
```yaml
version: '3.13'
services:
  job-tracker:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_PATH=/app/data/job_applications.db
```

### 4. Railway Deployment

1. Connect your GitHub repo to Railway
2. Add these environment variables:
   - `PORT=8501`
3. Railway will auto-deploy!

### 5. Local Network Access

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## Production Enhancements

### Authentication (Optional)
Add user authentication for multi-user environments:

```python
# Add to requirements.txt
streamlit-authenticator==0.2.3

# In app.py
import streamlit_authenticator as stauth

# Add authentication logic
```

### Database Upgrades
For production with multiple users:

```python
# Switch to PostgreSQL
# Update requirements.txt:
psycopg2-binary==2.9.7
sqlalchemy==2.0.19

# Update database.py to use PostgreSQL
```

### Advanced Features
- **Email notifications** for interview reminders
- **Calendar integration** (Google Calendar API)
- **Document upload** (resume versions, cover letters)
- **Salary analysis** and market research integration
- **Company research** integration (Glassdoor API)

### Performance Optimization
- **Caching** with `@st.cache_data`
- **Lazy loading** for large datasets  
- **Database connection pooling**
- **Background tasks** for data processing

### Security Considerations
- **Environment variables** for sensitive configs
- **Input sanitization** and validation
- **Rate limiting** for API calls
- **HTTPS** enforcement in production

## Environment Variables

Create a `.env` file for production:

```bash
DATABASE_URL=sqlite:///job_applications.db
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production
DEBUG=False
```

## Monitoring & Logging

Add logging for production:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Backup Strategy

Automated database backups:

```python
import shutil
from datetime import datetime

def backup_database():
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2('job_applications.db', f'backups/{backup_name}')
```

## Testing

Add unit tests:

```bash
# Add to requirements.txt
pytest==7.4.0
pytest-streamlit==1.0.0

# Create test files
mkdir tests/
touch tests/test_database.py
touch tests/test_utils.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Troubleshooting

### Common Issues:

1. **Database locked error**: Restart the app
2. **Module not found**: Check requirements.txt installation
3. **Charts not displaying**: Clear browser cache
4. **Slow performance**: Enable caching decorators

### Support

- Create an issue on GitHub
- Check the [Streamlit documentation](https://docs.streamlit.io)
- Join the [Streamlit community](https://discuss.streamlit.io)

## License

This project is open source and available under the MIT License.

## Changelog

### v1.0.0
- Initial release with core functionality
- SQLite database integration
- Interactive charts and metrics
- Export functionality

### Future Releases
- v1.1.0: User authentication
- v1.2.0: Email notifications
- v1.3.0: Calendar integration
- v2.0.0: Multi-user support with PostgreSQL

