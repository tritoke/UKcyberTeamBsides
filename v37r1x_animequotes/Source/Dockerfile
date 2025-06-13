FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Copy application files
COPY app.py quotes.json requirements.txt ./
COPY views/ ./views/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create flag file
RUN echo "FLAG{Serv3r_S1d3_T3mpl4t3_Inj3cti0n_SuP3rMaCy!}" > /flag.txt
RUN chmod 644 /flag.txt

# Create non-root user
RUN adduser -D ctfuser
USER ctfuser

# Expose port
EXPOSE 5000

# Start application with unbuffered output for logging
CMD ["python", "-u", "app.py"]