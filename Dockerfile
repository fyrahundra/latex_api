# ---- Base image ----
FROM python:3.11-slim

# ---- Environment variables ----
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# ---- Install system dependencies + LaTeX ----
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        ca-certificates \
        sudo \
        \
        # --- LaTeX core ---
        texlive \
        texlive-latex-extra \
        texlive-xetex \
        \
        # --- Fonts ---
        texlive-fonts-recommended \
        texlive-fonts-extra \
        texlive-fonts-extra-links \
        \
        # --- TeX Gyre fonts (includes tgpagella) ---
        fonts-texgyre \
        \
        # --- Language support ---
        texlive-lang-european \
        \
        # --- Bibliography ---
        texlive-bibtex-extra \
        biber \
        \
        # --- Build tool ---
        latexmk \
        \
        # --- System font dependencies ---
        fontconfig \
        libfreetype6 \
        libpng16-16 \
        libjpeg62-turbo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
# ---- Create non-root user ----
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

USER appuser
WORKDIR /app

# ---- Install Python deps ----
COPY --chown=appuser:appuser requirements.txt .
RUN python -m pip install --upgrade pip --user && \
    python -m pip install --user -r requirements.txt

# ---- Copy app ----
COPY --chown=appuser:appuser . .

# ---- Expose port ----
EXPOSE 8080

# ---- Run app ----
CMD ["python", "app.py"]