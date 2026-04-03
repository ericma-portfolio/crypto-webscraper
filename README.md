# crypto-webscraper

## Overview
An end-to-end data pipeline that scrapes real-time cryptocurrency data
from CoinMarketCap, stores it in AWS S3, and loads it into a Redshift
cluster for analysis and visualization in Tableau.

## Architecture
CoinMarketCap API → AWS S3 → Apache Airflow (DAGs) → Amazon Redshift → Tableau

## Features
- Automated daily data ingestion via Airflow DAGs on a cron schedule
- Tracks top 10 cryptocurrencies by market cap
- Daily price % differences and market trend tracking
- CI/CD pipeline with GitHub Actions and Super-Linter for code quality enforcement

## Tech Stack
- **Orchestration:** Apache Airflow
- **Storage:** AWS S3
- **Data Warehouse:** Amazon Redshift
- **Visualization:** Tableau
- **CI/CD:** GitHub Actions, Super-Linter
- **Language:** Python

## Project Status
🚧 In progress — pipeline and DAGs complete, Tableau dashboard integration ongoing
