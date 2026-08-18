FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY tools ./tools
COPY skill ./skill
RUN pip install --no-cache-dir .
RUN mkdir -p /app/outputs
EXPOSE 8000
CMD ["fortune-liuyao-mcp"]
